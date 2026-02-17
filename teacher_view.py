import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os
from dotenv import load_dotenv
from db_utils import get_all_students_with_results, reset_database, delete_specific_students, save_holistic_analysis, get_student_analysis_history

# --- API AYARLARI ---
load_dotenv()

# API Key Kontrolü
if "ANTHROPIC_API_KEY" in st.secrets:
    ANTHROPIC_API_KEY = st.secrets["ANTHROPIC_API_KEY"]
else:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def get_claude_client():
    """Claude API istemcisini başlatır."""
    if not ANTHROPIC_API_KEY:
        return None
    try:
        from anthropic import Anthropic
        return Anthropic(api_key=ANTHROPIC_API_KEY)
    except ImportError:
        return None

# --- YARDIMCI FONKSİYONLAR ---

def get_ai_analysis(prompt):
    """
    Claude API ile analiz üretir.
    Model: claude-opus-4-6 (İsteğe özel yapılandırılmış)
    """
    client = get_claude_client()
    if not client:
        return "⚠️ Hata: Claude API Key bulunamadı veya 'anthropic' kütüphanesi eksik."
    
    try:
        # İstenen Özel Model ID'si
        model_id = "claude-opus-4-6" 
        
        response = client.messages.create(
            model=model_id,
            max_tokens=4000,
            temperature=0.3, # Analitik derinlik ve tutarlılık için ideal
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        return f"Analiz sırasında bir hata oluştu: {str(e)}"

def plot_scores(data_dict, title):
    """
    Test sonuçlarını görselleştirmek için akıllı Bar Grafiği oluşturur.
    test_data.py'den gelen farklı veri yapılarını (Nested Dicts) otomatik tanır ve çizer.
    """
    if not data_dict or not isinstance(data_dict, dict):
        return None
    
    # --- VERİ TEMİZLEME VE HAZIRLAMA ---
    plot_data = {}
    
    # 1. Durum: 'categories' anahtarı varsa (Çalışma Davranışı, Sınav Kaygısı)
    if "categories" in data_dict and isinstance(data_dict["categories"], dict):
        plot_data = data_dict["categories"]
        
    # 2. Durum: 'scores' anahtarı varsa (Çoklu Zeka vb.)
    elif "scores" in data_dict and isinstance(data_dict["scores"], dict):
        temp_data = {}
        for k, v in data_dict["scores"].items():
            if isinstance(v, dict) and "pct" in v:
                temp_data[k] = v["pct"]
            elif isinstance(v, (int, float)):
                temp_data[k] = v
        plot_data = temp_data if temp_data else data_dict["scores"]

    # 3. Durum: 'percentages' anahtarı varsa (Holland)
    elif "percentages" in data_dict:
        plot_data = data_dict["percentages"]
        
    # 4. Durum: Düz sözlük (Sağ-Sol Beyin, VARK)
    else:
        for k, v in data_dict.items():
            if isinstance(v, (int, float)) and k not in ["id", "user_id"]:
                # Sağ-Sol beyin için toplam sayıları değil yüzdeleri alalım
                if "yuzde" in k: 
                    label = "Sağ Beyin" if "sag" in k else "Sol Beyin"
                    plot_data[label] = v
                elif "beyin" not in k and "dominant" not in k and "total" not in k: 
                    plot_data[k] = v

    if not plot_data:
        return None

    # Veriyi hazırla
    labels = [str(k) for k in plot_data.keys()]
    values = [float(v) for v in plot_data.values()]

    # Grafik Ayarları
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Renk paleti
    sns.barplot(x=values, y=labels, ax=ax, palette="viridis", orient='h')
    
    ax.set_title(f"{title}", fontsize=12, fontweight='bold')
    ax.set_xlabel("Puan / Yüzde")
    
    plt.tight_layout()
    return fig

# --- ANA ÖĞRETMEN UYGULAMASI ---

def app():
    # --- CSS VE ARAYÜZ AYARLARI ---
    st.markdown("""
    <style>
        .stSelectbox div, .stMultiSelect div { cursor: pointer !important; }
        div[data-baseweb="select"] { cursor: pointer !important; }
        div[role="listbox"] li { cursor: pointer !important; }
        .stRadio > label { font-weight: bold; font-size: 16px; color: #2E86C1; cursor: pointer !important; }
        .stRadio div[role="radiogroup"] > label { cursor: pointer !important; }
        .archive-box { background-color: #f8f9fa; border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
        .report-header { color: #155724; background-color: #d4edda; padding: 10px; border-radius: 5px; margin-bottom: 10px; border: 1px solid #c3e6cb; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

    st.title("👨‍🏫 Öğretmen Yönetim Paneli")
    st.markdown("---")

    # Veritabanından verileri çek
    data = get_all_students_with_results()
    student_names_all = [d["info"].name for d in data] if data else []

    # --- SIDEBAR: YÖNETİM ---
    with st.sidebar:
        st.header("⚙️ Yönetim Araçları")
        
        with st.expander("🗑️ Öğrenci Dosyası Sil"):
            if not student_names_all:
                st.info("Sistemde kayıtlı öğrenci yok.")
            else:
                st.warning("Seçilen öğrencilerin tüm verileri (testler, raporlar) silinecektir.")
                selected_to_delete = st.multiselect("Silinecekleri Seç:", options=student_names_all)
                
                if selected_to_delete:
                    if st.button("SEÇİLENLERİ KALICI OLARAK SİL", type="primary"):
                        if delete_specific_students(selected_to_delete):
                            st.success("Kayıtlar başarıyla silindi.")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Silme işlemi başarısız oldu.")

        st.markdown("---")
        
        with st.expander("⚠️ Fabrika Ayarlarına Dön"):
            st.error("DİKKAT: Bu işlem tüm veritabanını temizler.")
            if st.button("TÜM SİSTEMİ SIFIRLA"):
                if reset_database():
                    st.success("Sistem tamamen sıfırlandı.")
                    time.sleep(1)
                    st.rerun()

    # --- ANA EKRAN AKIŞI ---
    if not data:
        st.info("📂 Henüz kayıtlı öğrenci verisi bulunmamaktadır.")
        return

    # 1. ÖĞRENCİ SEÇİMİ
    st.subheader("📂 Öğrenci Dosyası Görüntüle")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_name = st.selectbox(
            "İncelemek İstediğiniz Öğrenciyi Seçiniz:", 
            student_names_all, 
            index=None, 
            placeholder="Listeden bir öğrenci seçin..."
        )
    
    if not selected_name:
        st.info("👆 Lütfen analizlerini görmek istediğiniz öğrenciyi yukarıdaki listeden seçiniz.")
        return

    # Seçilen öğrenci verileri
    student_data = next(d for d in data if d["info"].name == selected_name)
    info = student_data["info"]
    tests = student_data["tests"]

    # 2. ÖĞRENCİ KİMLİK KARTI
    with st.container():
        st.markdown(f"### 🆔 {info.name}")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Yaş / Cinsiyet", f"{info.age} / {info.gender}")
        c1.caption("Demografik Bilgi")
        c2.metric("Kullanıcı Adı", info.username)
        c2.caption("Sistem Girişi")
        c3.write(f"**Şifre:** {info.password}")
        c3.caption("Güvenlik")
        c4.metric("Toplam Giriş", info.login_count)
        c4.caption("Aktiflik Durumu")
    
    st.divider()

    # ============================================================
    # 3. KAYITLI RAPOR ARŞİVİ (Grafikli)
    # ============================================================
    st.subheader("📂 Kayıtlı Rapor Arşivi")
    
    history = get_student_analysis_history(info.id)
    
    if not history:
        st.info("Bu öğrenci için henüz oluşturulmuş analiz raporu bulunmamaktadır.")
    else:
        st.markdown(f"Bu öğrenci için **{len(history)} adet** kayıtlı rapor bulundu.")
        
        for idx, record in enumerate(history):
            btn_label = f"📄 Rapor {idx+1}: {record['combination']} ({record['date']})"
            
            with st.expander(btn_label):
                st.markdown(f"<div class='report-header'>ANALİZ KAPSAMI: {record['combination']}</div>", unsafe_allow_html=True)
                
                # --- ARŞİV GRAFİKLERİ ---
                archived_test_names = record['combination'].split(' + ')
                archived_test_data = [t for t in tests if t["test_name"] in archived_test_names]
                
                if archived_test_data:
                    st.markdown("#### 📊 Grafik Özeti")
                    g_cols = st.columns(2)
                    for i, t_data in enumerate(archived_test_data):
                        if t_data["scores"]:
                            fig = plot_scores(t_data["scores"], t_data["test_name"])
                            if fig:
                                g_cols[i % 2].pyplot(fig)
                    st.markdown("---")
                
                st.markdown(record['report'])
                st.download_button(
                    label=f"📥 Raporu İndir ({idx+1})",
                    data=record['report'],
                    file_name=f"{info.name}_Rapor_{idx+1}.txt",
                    mime="text/plain",
                    key=f"dl_{idx}"
                )

    st.divider()

    # ============================================================
    # 4. YENİ ANALİZ OLUŞTURMA
    # ============================================================
    st.subheader("⚡ Yeni Analiz Oluştur")
    
    if not tests:
        st.warning("⚠️ Bu öğrenci henüz hiç test çözmemiş. Analiz yapılamaz.")
    else:
        all_completed_tests = [t["test_name"] for t in tests]
        
        st.write("Analiz raporu oluşturmak istediğiniz testleri seçiniz:")
        selected_tests = st.multiselect(
            "Test Listesi:", 
            options=all_completed_tests, 
            default=all_completed_tests 
        )
        
        if selected_tests:
            st.markdown("---")
            st.write("📊 **Analiz Yöntemini Seçiniz:**")
            
            analysis_mode = st.radio(
                "Nasıl bir rapor istiyorsunuz?",
                options=["BÜTÜNCÜL (Harmanlanmış) Rapor", "AYRI AYRI (Tekil) Raporlar"],
                index=0,
                help="Bütüncül: Seçilen tüm testleri birleştirip 'Büyük Resim' sentezi yapar.\nAyrı Ayrı: Seçilen her test için sırayla detaylı psikometrik analiz yapar."
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 ANALİZİ BAŞLAT (Claude Opus 4.6)", type="primary"):
                analyzed_data = [t for t in tests if t["test_name"] in selected_tests]
                
                # --- GRAFİKLERİ GÖSTER ---
                st.markdown("### 📊 Puan Grafikleri")
                gc = st.columns(2)
                for i, t in enumerate(analyzed_data):
                    if t["scores"]:
                        fig = plot_scores(t["scores"], t["test_name"])
                        if fig:
                            gc[i % 2].pyplot(fig)
                        else:
                            gc[i % 2].info(f"{t['test_name']} için grafik verisi yok.")

                # ====================================================
                # MOD 1: BÜTÜNCÜL (HARMANLANMIŞ) SENTEZ ANALİZİ
                # ====================================================
                if analysis_mode == "BÜTÜNCÜL (Harmanlanmış) Rapor":
                    
                    st.info(f"⏳ Claude Opus, seçilen **{len(selected_tests)} testi** derinlemesine harmanlıyor, çelişkileri ve gizli bağlantıları analiz ediyor. Lütfen bekleyin...")
                    
                    with st.spinner("Stratejik Eğitim Koçu verileri sentezliyor..."):
                        ai_input = []
                        for t in analyzed_data:
                            ai_input.append({
                                "TEST ADI": t["test_name"], 
                                "TARİH": str(t["date"]),
                                "SONUÇLAR": t["scores"] if t["scores"] else t["raw_answers"]
                            })
                        
                        # --- GÜÇLENDİRİLMİŞ HARMANLANMIŞ PROMPT (SENTEZ ODAKLI) ---
                        prompt = f"""
                        SEN: Öğrenciyi bir bütün olarak ele alan, parçaları birleştirip "büyük resmi" gören stratejik bir eğitim koçusun.
                        GÖREV: Farklı test sonuçlarını BİRLEŞTİREREK (Sentezleyerek) öğrencinin zihin haritasını çıkar.

                        🛑 SENTEZ KURALLARI (HALÜSİNASYON ENGELLEYİCİ):
                        1. **TEKRAR ETME:** Testleri tek tek anlatma (bunu zaten yaptık). Testler arası İLİŞKİYİ anlat.
                        2. **ÇELİŞKİLERİ BUL:** Öğrencinin "İstekli" (Test A) ama "Kaygılı" (Test B) olduğu durumları tespit et.
                        3. **NEDEN-SONUÇ KUR:** "Ders çalışamıyor" deme; "VARK sonucu Kinestetik olduğu için masa başında sıkılıyor" de (Veriyi bağla).
                        4. **YAŞA UYGUNLUK:** Öğrenci {info.age} yaşında. Tavsiyeler bu yaşın gerçekliğine uygun olsun.

                        ÖĞRENCİ: {info.name}, {info.age}, {info.gender}
                        TÜM VERİLER (JSON):
                        {json.dumps(ai_input, ensure_ascii=False, indent=2)}

                        RAPOR FORMATI:

                        # 🚀 BÜYÜK RESİM: {info.name} Kimdir?
                        (Giriş paragrafı: Öğrencinin en baskın karakteristiğini, tüm testlerin ortak paydasını bir hikaye gibi anlat.)

                        # 🧩 1. ZİHİNSEL SENTEZ (Bağlantılar)
                        - **Potansiyel vs Performans:** (Zeka puanları ile Çalışma Davranışı/Kaygı arasındaki ilişkiyi yorumla).
                        - **Öğrenme DNA'sı:** (Sağ/Sol beyin ve VARK sonuçlarını birleştir. Nasıl öğreniyor?)
                        - **İlgi ve Yetenek Uyumu:** (Holland RIASEC ile Çoklu Zeka örtüşüyor mu?)

                        # ⚖️ 2. KRİTİK DENGE TABLOSU (Markdown)
                        | Güçlü Yanı (Hangi Testten?) | Önündeki Engel (Hangi Testten?) | Çözüm Stratejisi |
                        |-----------------------------|---------------------------------|------------------|
                        | Örn: Müzik Zekası (Çoklu Zeka) | Odaklanma Sorunu (D2 Testi) | Müzik eşliğinde ders çalışmalı |

                        # 🎯 3. STRATEJİK YOL HARİTASI
                        ### 🎓 Akademik Başarı İçin:
                        - (Test sonuçlarına özel, öğrencinin öğrenme stiline %100 uygun çalışma metodunu yaz.)

                        ### 🧠 Duygusal ve Sosyal Gelişim:
                        - (Kaygı, kişilik ve sosyal test sonuçlarına göre tavsiye.)

                        ### 👨‍👩‍👦 Ebeveyn İçin Özel Not:
                        > (Çocuğun "Kullanma Kılavuzu" niteliğinde, aileyi yönlendiren, suçlayıcı olmayan, motive edici bir paragraf.)
                        
                        Dil: Türkçe. Üslup: Profesyonel Koçluk.
                        """
                        
                        final_report = get_ai_analysis(prompt)
                        save_holistic_analysis(info.id, selected_tests, final_report)
                        
                        st.success("✅ Kapsamlı sentez analizi tamamlandı ve kaydedildi.")
                        time.sleep(1.5)
                        st.rerun()

                # ====================================================
                # MOD 2: AYRI AYRI DETAYLI ANALİZLER (TEKİL)
                # ====================================================
                else:
                    progress_text = "Testler sırayla analiz ediliyor..."
                    my_bar = st.progress(0, text=progress_text)
                    total_ops = len(analyzed_data)
                    
                    for idx, t in enumerate(analyzed_data):
                        test_name = t["test_name"]
                        my_bar.progress((idx + 1) / total_ops, text=f"**{test_name}** analiz ediliyor... ({idx+1}/{total_ops})")
                        
                        ai_input = [{
                            "TEST ADI": test_name, 
                            "TARİH": str(t["date"]),
                            "SONUÇLAR": t["scores"] if t["scores"] else t["raw_answers"]
                        }]
                        
                        # --- GÜÇLENDİRİLMİŞ TEKİL PROMPT (HALÜSİNASYON KORUMALI) ---
                        prompt = f"""
                        SEN: 20 yıllık deneyime sahip, veriye dayalı konuşan kıdemli bir eğitim psikoloğusun.
                        GÖREV: Aşağıdaki test sonucunu analiz et.

                        🛑 SIKI KURALLAR (HALÜSİNASYON ENGELLEYİCİ):
                        1. **SADECE VERİ:** JSON içinde görmediğin hiçbir sayı veya özellik hakkında yorum yapma.
                        2. **KANIT GÖSTER:** Bir özellikten bahsediyorsan parantez içinde puanını yaz. Örn: "Görsel hafızan güçlü (Puan: 85)."
                        3. **AŞIRI YORUM YOK:** Puan %40-60 arasındaysa "Dengeli/Ortalama", %80 üzerindeyse "Baskın", %30 altındaysa "Gelişmeli" de. Aşırı uç ifadeler kullanma.
                        4. **TIBBİ TANI YASAK:** "DEHB", "Disleksi", "Depresyon" gibi kelimeleri ASLA kullanma.

                        ÖĞRENCİ: {info.name}, {info.age}, {info.gender}
                        TEST ADI: {test_name}
                        VERİLER: {json.dumps(ai_input, ensure_ascii=False)}

                        ANALİZ ÇERÇEVESİ (Buna göre yorumla):
                        - **Sağ/Sol Beyin:** Sağ yüksekse (Yaratıcı, Görsel, Sezgisel), Sol yüksekse (Mantıksal, Analitik, Planlı).
                        - **Çoklu Zeka:** En yüksek 3 puanı "Süper Güç", en düşük 2 puanı "Desteklenmeli" olarak al.
                        - **VARK:** Öğrenme stili (Görsel, İşitsel, Okuma, Kinestetik). Nasıl ders çalışmalı buna odaklan.
                        - **Holland RIASEC:** Meslek eğilimi. Yüksek skorlar hangi meslek grubuna giriyor?
                        - **Sınav Kaygısı:** Yüksekse "Rahatlama Teknikleri", Düşükse "Rehavet Uyarısı" ver.

                        RAPOR FORMATI:

                        ### 1. 📊 Sonuç Özeti
                        - Testin ana sonucunu TEK cümleyle, net bir yargıyla özetle.
                        - Görsel (ASCII):
                          [Kategori] : ████████░░ (Puan)

                        ### 2. 🧠 Veriye Dayalı Psikolojik Analiz
                        - (Burada "Neden?" sorusuna cevap ver. Puanların öğrencinin günlük hayatına etkisini anlat. Metafor kullan: "Zihnin bir orkestra şefi gibi..." gibi.)

                        ### 3. 🌟 Kanıtlanmış Güçlü Yönler
                        - ✅ [Özellik Adı]: (Açıklama - Kanıt Puanı)
                        - ✅ [Özellik Adı]: (Açıklama - Kanıt Puanı)

                        ### 4. 🚀 Gelişim Fırsatları
                        - ⚠️ [Özellik Adı]: (Nasıl geliştirilir?)

                        ### 5. 🎯 Nokta Atışı Tavsiyeler (Bu Teste Özel)
                        - (Öğrencinin yaşına ({info.age}) uygun, hemen uygulanabilir 3 somut taktik.)
                        
                        Dil: Türkçe.
                        """
                        
                        single_report = get_ai_analysis(prompt)
                        save_holistic_analysis(info.id, [test_name], single_report)
                    
                    my_bar.empty()
                    st.success(f"✅ {total_ops} test başarıyla detaylı analiz edildi ve Arşiv'e eklendi.")
                    time.sleep(2)
                    st.rerun()

    # 5. GEÇMİŞ TABLOSU
    st.divider()
    with st.expander("🗂️ Test Geçmişi ve Ham Veriler (Liste)"):
        if tests:
            df_tests = pd.DataFrame(tests)
            df_tests['date'] = pd.to_datetime(df_tests['date']).dt.strftime('%d.%m.%Y')
            st.dataframe(df_tests[["test_name", "date"]], use_container_width=True)
