import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import time
from db_utils import get_all_students_with_results, reset_database, delete_specific_students, save_holistic_analysis, get_student_analysis_history
from openai import OpenAI
import os
from dotenv import load_dotenv

# --- API VE BAĞLANTI AYARLARI ---
load_dotenv()
if "GROK_API_KEY" in st.secrets:
    GROK_API_KEY = st.secrets["GROK_API_KEY"]
else:
    GROK_API_KEY = os.getenv("GROK_API_KEY")

# xAI (Grok) İstemcisi
client = OpenAI(api_key=GROK_API_KEY, base_url="https://api.x.ai/v1")

# --- YARDIMCI FONKSİYONLAR ---

def get_ai_analysis(prompt):
    """
    Yapay Zekaya analiz isteği gönderir.
    Hata durumunda kullanıcıya bilgi döner.
    """
    if not GROK_API_KEY:
        return "Hata: API Key bulunamadı. Lütfen sistem yöneticisiyle görüşün."
    try:
        response = client.chat.completions.create(
            model="grok-4-1-fast-reasoning", # Akıl yürütme yeteneği en yüksek model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1 # Daha tutarlı ve analitik sonuçlar için düşük sıcaklık
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Analiz sırasında bir hata oluştu: {str(e)}"

def plot_scores(data_dict, title):
    """
    Test sonuçlarını görselleştirmek için Bar Grafiği oluşturur.
    """
    if not data_dict or not isinstance(data_dict, dict):
        return None
    
    # Veriyi hazırla
    labels = [str(k) for k in data_dict.keys()]
    try:
        values = [float(v) for v in data_dict.values()]
    except:
        return None 

    # Grafik Ayarları (Seaborn & Matplotlib)
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Renk paleti ve çizim
    sns.barplot(x=values, y=labels, ax=ax, palette="viridis", orient='h')
    
    ax.set_title(f"{title}", fontsize=12, fontweight='bold')
    ax.set_xlabel("Puan / Yüzde")
    
    plt.tight_layout()
    return fig

# --- ANA ÖĞRETMEN UYGULAMASI ---

def app():
    # --- CSS: MOUSE İŞARETÇİSİ VE ARAYÜZ İYİLEŞTİRMELERİ ---
    st.markdown("""
    <style>
        /* Tüm Seçim Kutuları (Selectbox, Multiselect) üzerine gelince el işareti çıksın */
        .stSelectbox div, .stMultiSelect div {
            cursor: pointer !important;
        }
        div[data-baseweb="select"] {
            cursor: pointer !important;
        }
        /* Açılır liste elemanları */
        div[role="listbox"] li {
            cursor: pointer !important;
        }
        /* Radyo Butonları */
        .stRadio > label {
            font-weight: bold;
            font-size: 16px;
            color: #2E86C1;
            cursor: pointer !important;
        }
        .stRadio div[role="radiogroup"] > label {
            cursor: pointer !important;
        }
        /* Rapor Arşiv Kutusu */
        .archive-box {
            background-color: #f8f9fa;
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        /* Rapor Başlıkları */
        .report-header {
            color: #155724;
            background-color: #d4edda;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
            border: 1px solid #c3e6cb;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("👨‍🏫 Öğretmen Yönetim Paneli")
    st.markdown("---")

    # Veritabanından verileri çek
    data = get_all_students_with_results()
    
    # Öğrenci İsim Listesini Oluştur
    student_names_all = [d["info"].name for d in data] if data else []

    # --- SIDEBAR: YÖNETİM VE SİLME ARAÇLARI ---
    with st.sidebar:
        st.header("⚙️ Yönetim Araçları")
        
        # 1. ÖĞRENCİ SİLME
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
        
        # 2. TAM SIFIRLAMA
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

    # 1. ÖĞRENCİ SEÇİMİ (VARSAYILAN BOŞ)
    st.subheader("📂 Öğrenci Dosyası Görüntüle")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        # index=None ile varsayılan boş gelir, placeholder görünür
        selected_name = st.selectbox(
            "İncelemek İstediğiniz Öğrenciyi Seçiniz:", 
            student_names_all, 
            index=None, 
            placeholder="Listeden bir öğrenci seçin..."
        )
    
    # EĞER SEÇİM YAPILMADIYSA BURADA DUR
    if not selected_name:
        st.info("👆 Lütfen analizlerini görmek istediğiniz öğrenciyi yukarıdaki listeden seçiniz.")
        return

    # SEÇİLEN ÖĞRENCİNİN VERİLERİNİ AL
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
    # 3. KAYITLI RAPOR ARŞİVİ (GRAFİK DESTEKLİ)
    # ============================================================
    st.subheader("📂 Kayıtlı Rapor Arşivi")
    
    # Bu öğrencinin geçmiş raporlarını veritabanından getir
    history = get_student_analysis_history(info.id)
    
    if not history:
        st.info("Bu öğrenci için henüz oluşturulmuş bütüncül veya detaylı bir analiz raporu bulunmamaktadır.")
    else:
        st.markdown(f"Bu öğrenci için **{len(history)} adet** kayıtlı rapor bulundu. Görüntülemek için aşağıdan seçim yapabilirsiniz:")
        
        for idx, record in enumerate(history):
            # Buton etiketi: Kombinasyon + Tarih
            btn_label = f"📄 Rapor {idx+1}: {record['combination']} ({record['date']})"
            
            with st.expander(btn_label):
                # Başlık
                st.markdown(f"<div class='report-header'>ANALİZ KAPSAMI: {record['combination']}</div>", unsafe_allow_html=True)
                
                # --- GRAFİK GÖSTERİMİ (ARŞİVDE) ---
                # Kayıtlı kombinasyon stringini parçala (Örn: "Enneagram + VARK" -> ["Enneagram", "VARK"])
                # Not: Split ederken tam eşleşme için dikkatli oluyoruz.
                archived_test_names = record['combination'].split(' + ')
                
                # Bu testlerin güncel verilerini (skorlarını) bul
                archived_test_data = [t for t in tests if t["test_name"] in archived_test_names]
                
                if archived_test_data:
                    st.markdown("#### 📊 İlgili Test Grafikleri")
                    g_cols = st.columns(2)
                    for i, t_data in enumerate(archived_test_data):
                        if t_data["scores"]:
                            fig = plot_scores(t_data["scores"], t_data["test_name"])
                            if fig:
                                g_cols[i % 2].pyplot(fig)
                    st.markdown("---")
                
                # Rapor Metni
                st.markdown(record['report'])
                
                # İndirme Butonu
                st.download_button(
                    label=f"📥 Raporu İndir ({idx+1})",
                    data=record['report'],
                    file_name=f"{info.name}_Rapor_{idx+1}.txt",
                    mime="text/plain",
                    key=f"dl_{idx}"
                )

    st.divider()

    # ============================================================
    # 4. YENİ ANALİZ OLUŞTURMA MERKEZİ (SEÇENEKLİ & SÜPER PROMPT)
    # ============================================================
    st.subheader("⚡ Yeni Analiz Oluştur")
    
    if not tests:
        st.warning("⚠️ Bu öğrenci henüz hiç test çözmemiş. Analiz yapılamaz.")
    else:
        # Öğrencinin çözdüğü tüm testleri listele
        all_completed_tests = [t["test_name"] for t in tests]
        
        st.write("Analiz raporu oluşturmak istediğiniz testleri seçiniz:")
        
        # Çoklu Seçim Kutusu
        selected_tests = st.multiselect(
            "Test Listesi:", 
            options=all_completed_tests, 
            default=all_completed_tests # Kolaylık olsun diye hepsi seçili gelsin
        )
        
        if selected_tests:
            st.markdown("---")
            st.write("📊 **Analiz Yöntemini Seçiniz:**")
            
            # --- YÖNTEM SEÇİMİ (RADIO BUTTON) ---
            analysis_mode = st.radio(
                "Nasıl bir rapor istiyorsunuz?",
                options=["BÜTÜNCÜL (Harmanlanmış) Rapor", "AYRI AYRI (Tekil) Raporlar"],
                index=0,
                help="Bütüncül: Seçilen tüm testleri birleştirip tek bir sentez rapor yazar.\nAyrı Ayrı: Seçilen her test için sırayla ayrı ayrı raporlar oluşturur ve kaydeder."
            )
            
            st.markdown("<br>", unsafe_allow_html=True) # Boşluk
            
            if st.button("🚀 ANALİZİ BAŞLAT", type="primary"):
                # Seçilen testlerin verilerini filtrele
                analyzed_data = [t for t in tests if t["test_name"] in selected_tests]
                
                # --- ORTAK ADIM: PUAN GRAFİKLERİNİ GÖSTER ---
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
                # MOD 1: BÜTÜNCÜL (HARMANLANMIŞ) ANALİZ
                # ====================================================
                if analysis_mode == "BÜTÜNCÜL (Harmanlanmış) Rapor":
                    
                    st.info(f"⏳ Yapay Zeka, seçilen **{len(selected_tests)} testi** birbiriyle ilişkilendirerek görselleştirilmiş bütüncül bir rapor yazıyor. Lütfen bekleyin...")
                    
                    with st.spinner("Veriler sentezleniyor ve görselleştiriliyor..."):
                        # Yapay Zekaya gidecek veriyi hazırla
                        ai_input = []
                        for t in analyzed_data:
                            ai_input.append({
                                "TEST ADI": t["test_name"], 
                                "TARİH": str(t["date"]),
                                "SONUÇLAR": t["scores"] if t["scores"] else t["raw_answers"]
                            })
                        
                        # --- DÜNYA STANDARTLARINDA SÜPER ANALİZ PROMPTU ---
                        prompt = f"""
                        Sen, dünyanın en prestijli eğitim ve psikoloji enstitülerinde (Harvard, Oxford) kullanılan, **çok boyutlu veri görselleştirme ve kişilik analizi** konusunda uzmanlaşmış kıdemli bir 'Baş Psikolog' ve 'Veri Bilimcisi'sin.

                        GÖREVİN:
                        Aşağıda verileri sunulan öğrenci için, farklı test sonuçlarını birbiriyle harmanlayan, sadece metin değil **GÖRSEL ÖĞELERLE ZENGİNLEŞTİRİLMİŞ** (Tablolar, Progress Barlar, İkonlar) bir "Bütüncül Gelişim Raporu" hazırlamak.
                        
                        ÖĞRENCİ KİMLİĞİ:
                        Ad: {info.name}, Yaş: {info.age}, Cinsiyet: {info.gender}
                        
                        ANALİZ EDİLECEK VERİLER (JSON):
                        {json.dumps(ai_input, ensure_ascii=False)}

                        ----------------------------------------------------------
                        ⚠️ ANALİZ VE GÖRSELLEŞTİRME KURALLARI:
                        
                        1. **GÖRSEL DİL KULLANIMI (MARKDOWN):**
                           - **Progress Bar:** Puanları veya etki düzeylerini göstermek için `████████░░` (%80) gibi karakterler kullan.
                           - **Tablolar:** Verileri karşılaştırırken mutlaka Markdown Tablosu kullan.
                           - **İkonlar:** Her başlığın ve önemli maddenin başına uygun emoji koy (🧠, 🚀, 💡, ⚠️).
                        
                        2. **SENTEZ VE HARMANLAMA:**
                           - Testleri birbirinden kopuk anlatma. Gizli bağlantıları bul.
                           - Örn: "Matematiksel zekan yüksek ama Tip 6 kaygın yüzünden işlem hatası yapıyorsun."

                        3. **DERİNLİK VE SOMUTLUK:**
                           - Jenerik tavsiyeler YASAK. "Kitap oku" deme; "Görsel hafızan güçlü olduğu için tarih dersini belgesel izleyerek çalış" de.

                        ----------------------------------------------------------
                        ### 🌟 ANALİZ İÇİN 'FEW-SHOT' (ÖRNEK VAKA) KÜTÜPHANESİ (30 ADET) 🌟
                        (Aşağıdaki örneklerin mantığını kopyala)

                        **1. (Tip 5 + Görsel):** "Zihnin kelimelerden çok resimlerle çalışıyor. Klasik not tutma yerine 'Zihin Haritaları' (Mind Maps) kullanmalısın."
                        **2. (Sınav Kaygısı + Tip 1):** "Kalp çarpıntın bilgisizlikten değil, Tip 1 'Hata yapma korkusundan' geliyor. Stratejin: Hata yapma izni."
                        **3. (Sosyal Düşük + İçsel Yüksek):** "Kalabalık seni yorar. Şarj olmak için yalnız kalmalısın. Sosyalleşmek için satranç kulübü gibi sakin yerleri seç."
                        **4. (Bedensel Zeka + DEHB):** "Ayak sallaman yaramazlık değil, beyninin çalışma şekli. Ders çalışırken elinde stres topu olsun."
                        **5. (Müziksel + Sözel):** "Ezber yaparken bilgileri şarkı sözüne çevirip ritimle mırıldan. Asla unutmazsın."
                        **6. (Doğacı + Tip 9):** "Kapalı alan seni boğar. Penceresi ağaca bakan bir odada veya parkta çalış."
                        **7. (Tip 3 + Mantıksal):** "Hedeflerini 'Level 1, Level 2' gibi oyunlaştır. Her başarı sana zafer hissi vermeli."
                        **8. (Tip 2 + Sosyal):** "Başkasına anlatarak öğreniyorsun. Sınıfın gönüllü hocası ol."
                        **9. (Tip 7 + Disiplinsiz):** "Sıkılmak senin doğanda var. Pomodoro yerine 'Gamification' teknikleri kullan."
                        **10. (Tip 6 + Kaygı):** "Belirsizlik düşmanın. Yapılacaklar listesi hazırla ve her biten işe tik at. Bu sana güvenlik hissi verir."
                        **11. (Görsel + Tip 4):** "Sıradan defter seni sıkar. Renkli kalemler ve çizimlerle notlarını sanat eserine dönüştür."
                        **12. (Tip 8 + Bedensel):** "Ders çalışmayı 'Otoriteye itaat' değil, 'Güç kazanma savaşı' olarak gör."
                        **13. (Sözel + Tip 1):** "Mükemmel cümle kurmaya çalışma, akışına bırak. Taslak yazmaktan korkma."
                        **14. (İçsel + Tip 5):** "İzolasyon senin süper gücün (Deep Work). Sadece dozunu kaçırma."
                        **15. (Kinestetik + Tip 7):** "Söküp takarak, dokunarak öğren. Deney setleri tam sana göre."
                        **16. (Tip 2 + Aile Baskısı):** "Sevilmek için başarılı olmak zorunda değilsin. Sen notlarından ibaret değilsin."
                        **17. (Mantıksal + Tip 6):** "Mantığını anlamadığın şeyi ezberleme. 'Neden?' diye sormaktan çekinme."
                        **18. (Müziksel + Tip 4):** "Moduna uygun 'Study Playlist' hazırla. Müzik senin duygu regülatörün."
                        **19. (Tip 9 + Eylemsizlik):** "Başlamak en zoru. 'Sadece 5 dakika bakacağım' diye otur, gerisi gelir."
                        **20. (Tip 8 + Sosyal):** "Liderlik enerjini proje ödevlerini yönetirken kullan."
                        **21. (VARK Okuma/Yazma + Tip 5):** "Bilgiyi okuyarak sünger gibi çekiyorsun. Kendi kendine özet çıkararak ve 'blog yazısı yazar gibi' not tutarak uzmanlaş."
                        **22. (Mantıksal + Tip 4):** "Sayıların içindeki estetiği gör. Matematik senin için kuru işlem değil, evrenin şiiridir."
                        **23. (Sosyal + Tip 9):** "Çatışma sevmediğin için grupta 'Barış Elçisi' olursun. Liderliği sessizce ve uzlaştırarak yap."
                        **24. (Kinestetik + Yüksek Kaygı):** "Adrenalin birikmesi seni kilitliyor. Sınavdan hemen önce 5 dakika hızlı yürüyüş yap veya zıpla."
                        **25. (Görsel + Tip 8):** "Büyük resmi görmek istersin. Odanın duvarına dev bir 'Vizyon Panosu' (Vision Board) as ve hedeflerini oraya çiz."
                        **26. (Müziksel + Düşük Odak):** "Arka planda sözsüz 'Lo-Fi' veya 'Klasik' müzik çalması, beynindeki gürültüyü susturur ve odaklanmanı sağlar."
                        **27. (İçsel + Tip 3):** "Başkalarıyla değil, dünkü kendinle yarış. Kendi rekorlarını kırmak seni motive eder."
                        **28. (Doğacı + Tip 6):** "Doğa sana güven verir. Kaygılandığında toprağa basmak veya bir bitkiyle ilgilenmek seni anında sakinleştirir."
                        **29. (Sözel + Tip 7):** "Sıkıcı tarih konularını, arkadaşlarına heyecanlı bir dedikodu veya hikaye anlatır gibi anlat. Eğlenerek öğren."
                        **30. (Mantıksal + Tip 2):** "Karmaşık problemleri çözüp arkadaşlarına yardım etmekten keyif alırsın. 'Sınıfın Problem Çözücüsü' rolünü üstlen."

                        ----------------------------------------------------------
                        
                        ### 📝 İSTENEN GÖRSEL RAPOR FORMATI (MARKDOWN):

                        1. **🧠 BÜTÜNCÜL PROFİL HARİTASI (TABLO)**
                           - Öğrencinin "Kim Olduğunun" özeti.
                           - *Format: Markdown Tablosu (Özellik | Tespit | Etki Düzeyi)*

                        2. **💪 SÜPER GÜÇLERİN SENTEZİ (GRAFİK)**
                           - En güçlü yanlar ve birbirini nasıl beslediği.
                           - *Format: Özellik Adı `████████░░` (Açıklama)*

                        3. **🚧 GİZLİ ENGELLER VE KİLİT ÇÖZÜMLER (OKLAR)**
                           - *Format: 🔴 Sorun -> 🟢 Çözüm*

                        4. **🎓 KİŞİYE ÖZEL ÖĞRENME STRATEJİSİ (TABLO)**
                           - VARK ve Zeka türüne göre somut reçete.
                           - *Format: Markdown Tablosu (Yöntem | Araç | Sıklık)*

                        5. **🚀 GELECEK VİZYONU VE KARİYER (YILDIZLAR)**
                           - En uygun 3 meslek.
                           - *Format: Meslek Adı ⭐⭐⭐⭐⭐ (Neden Uygun?)*

                        6. **👨‍👩‍👦 AİLE VE ÖĞRETMENE NOT**
                           - *Format: > Blockquote içinde motivasyon notu.*

                        Dil: Türkçe. Üslup: Profesyonel, Akıcı, Görsel Olarak Zengin.
                        """
                        
                        final_report = get_ai_analysis(prompt)
                        
                        # Veritabanına Kaydet
                        save_holistic_analysis(info.id, selected_tests, final_report)
                        
                        st.success("✅ Görselleştirilmiş bütüncül analiz tamamlandı ve Arşiv'e kaydedildi.")
                        time.sleep(1.5)
                        st.rerun()

                # ====================================================
                # MOD 2: AYRI AYRI (TEKİL) ANALİZLER
                # ====================================================
                else:
                    progress_text = "Testler sırayla analiz ediliyor. Lütfen bekleyin..."
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
                        
                        # Tekil Analiz Promptu
                        prompt = f"""
                        Sen uzman bir eğitim psikoloğusun.
                        
                        ÖĞRENCİ: {info.name}, {info.age}, {info.gender}
                        TEST: {test_name}
                        VERİLER: {json.dumps(ai_input, ensure_ascii=False)}

                        GÖREV: Sadece bu teste odaklanarak derinlemesine bir yorum yap.
                        
                        RAPOR FORMATI:
                        1. 📊 Test Sonucunun Anlamı (Kısa Özet)
                        2. 💪 Güçlü Yönler (Maddeler halinde, İkonlu)
                        3. 🚧 Gelişim Alanları
                        4. 🎯 Bu Teste Özel Somut Tavsiyeler
                        
                        Dil: Türkçe.
                        """
                        
                        single_report = get_ai_analysis(prompt)
                        
                        # Tek başına (Liste içinde tek eleman olarak) kaydet
                        save_holistic_analysis(info.id, [test_name], single_report)
                    
                    my_bar.empty()
                    st.success(f"✅ Seçilen {total_ops} test başarıyla AYRI AYRI analiz edildi ve Arşiv'e eklendi.")
                    time.sleep(2)
                    st.rerun()

    # 5. TEST GEÇMİŞİ LİSTESİ (ALT KISIM)
    st.divider()
    with st.expander("🗂️ Test Geçmişi ve Ham Veriler (Liste)"):
        if tests:
            df_tests = pd.DataFrame(tests)
            df_tests['date'] = pd.to_datetime(df_tests['date']).dt.strftime('%d.%m.%Y')
            st.dataframe(df_tests[["test_name", "date"]], use_container_width=True)
