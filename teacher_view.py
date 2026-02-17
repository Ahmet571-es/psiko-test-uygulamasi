import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import time
from db_utils import get_all_students_with_results, reset_database, delete_specific_students, save_holistic_analysis, get_student_analysis_history

# --- CLAUDE API BAĞLANTISI (GROK YERİNE) ---
import os
from dotenv import load_dotenv
load_dotenv()

# API Key: önce secrets.toml, sonra .env
if "ANTHROPIC_API_KEY" in st.secrets:
    ANTHROPIC_API_KEY = st.secrets["ANTHROPIC_API_KEY"]
else:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def get_claude_client():
    """Claude API client oluşturur."""
    if not ANTHROPIC_API_KEY:
        return None
    try:
        from anthropic import Anthropic
        return Anthropic(api_key=ANTHROPIC_API_KEY)
    except ImportError:
        return None

# --- YARDIMCI FONKSİYONLAR ---

def get_ai_analysis(prompt):
    """Claude API ile analiz üretir. (Eski get_ai_analysis fonksiyonunun yerine)"""
    client = get_claude_client()
    if not client:
        return "Hata: Claude API Key bulunamadı veya 'anthropic' paketi yüklü değil. Lütfen 'pip install anthropic' yapın ve ANTHROPIC_API_KEY ayarlayın."
    try:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        return f"Analiz sırasında bir hata oluştu: {str(e)}"

def plot_scores(data_dict, title):
    """Test sonuçlarını görselleştirmek için Bar Grafiği oluşturur."""
    if not data_dict or not isinstance(data_dict, dict):
        return None
    
    labels = [str(k) for k in data_dict.keys()]
    try:
        values = [float(v) for v in data_dict.values()]
    except:
        return None 

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=values, y=labels, ax=ax, palette="viridis", orient='h')
    ax.set_title(f"{title}", fontsize=12, fontweight='bold')
    ax.set_xlabel("Puan / Yüzde")
    plt.tight_layout()
    return fig

# --- ANA ÖĞRETMEN UYGULAMASI ---

def app():
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

    data = get_all_students_with_results()
    student_names_all = [d["info"].name for d in data] if data else []

    # --- SIDEBAR ---
    with st.sidebar:
        st.header("⚙️ Yönetim Araçları")
        
        with st.expander("🗑️ Öğrenci Dosyası Sil"):
            if not student_names_all:
                st.info("Sistemde kayıtlı öğrenci yok.")
            else:
                st.warning("Seçilen öğrencilerin tüm verileri silinecektir.")
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

    # --- ANA EKRAN ---
    if not data:
        st.info("📂 Henüz kayıtlı öğrenci verisi bulunmamaktadır.")
        return

    st.subheader("📂 Öğrenci Dosyası Görüntüle")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_name = st.selectbox("İncelemek İstediğiniz Öğrenciyi Seçiniz:", student_names_all, index=None, placeholder="Listeden bir öğrenci seçin...")
    
    if not selected_name:
        st.info("👆 Lütfen analizlerini görmek istediğiniz öğrenciyi yukarıdaki listeden seçiniz.")
        return

    student_data = next(d for d in data if d["info"].name == selected_name)
    info = student_data["info"]
    tests = student_data["tests"]

    # --- ÖĞRENCİ KİMLİK KARTI ---
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
    # KAYITLI RAPOR ARŞİVİ
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
                
                archived_test_names = record['combination'].split(' + ')
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
    # YENİ ANALİZ OLUŞTURMA
    # ============================================================
    st.subheader("⚡ Yeni Analiz Oluştur")
    
    if not tests:
        st.warning("⚠️ Bu öğrenci henüz hiç test çözmemiş. Analiz yapılamaz.")
    else:
        all_completed_tests = [t["test_name"] for t in tests]
        st.write("Analiz raporu oluşturmak istediğiniz testleri seçiniz:")
        selected_tests = st.multiselect("Test Listesi:", options=all_completed_tests, default=all_completed_tests)
        
        if selected_tests:
            st.markdown("---")
            st.write("📊 **Analiz Yöntemini Seçiniz:**")
            
            analysis_mode = st.radio(
                "Nasıl bir rapor istiyorsunuz?",
                options=["BÜTÜNCÜL (Harmanlanmış) Rapor", "AYRI AYRI (Tekil) Raporlar"],
                index=0,
                help="Bütüncül: Seçilen tüm testleri birleştirip tek bir sentez rapor yazar.\nAyrı Ayrı: Seçilen her test için sırayla ayrı ayrı raporlar oluşturur."
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 ANALİZİ BAŞLAT", type="primary"):
                analyzed_data = [t for t in tests if t["test_name"] in selected_tests]
                
                # Grafikleri göster
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
                # MOD 1: BÜTÜNCÜL ANALİZ (CLAUDE API)
                # ====================================================
                if analysis_mode == "BÜTÜNCÜL (Harmanlanmış) Rapor":
                    st.info(f"⏳ Claude AI, seçilen **{len(selected_tests)} testi** birbiriyle ilişkilendirerek bütüncül bir rapor yazıyor...")
                    
                    with st.spinner("Veriler sentezleniyor..."):
                        ai_input = []
                        for t in analyzed_data:
                            ai_input.append({
                                "TEST ADI": t["test_name"], 
                                "TARİH": str(t["date"]),
                                "SONUÇLAR": t["scores"] if t["scores"] else t["raw_answers"]
                            })
                        
                        prompt = f"""Sen Türkiye'de bir eğitim klinik merkezinde çalışan uzman bir eğitim psikologusun.

ÖĞRENCİ: {info.name}, Yaş: {info.age}, Cinsiyet: {info.gender}

ANALİZ EDİLECEK TEST SONUÇLARI:
{json.dumps(ai_input, ensure_ascii=False, indent=2)}

GÖREV: Bu öğrencinin tüm test sonuçlarını birbiriyle harmanlayarak bütüncül bir gelişim raporu yaz.

KURALLAR:
1. Testler arası gizli bağlantıları bul (Örn: Enneagram tipi ile öğrenme stili arasındaki ilişki)
2. Somut, uygulanabilir öneriler ver — jenerik tavsiyeler YASAK
3. Her önerinin yanına "Neden?" açıklaması ekle
4. Dil sade, sıcak ve çocuk/ergen dostu olsun
5. ASLA klinik tanı koyma
6. Uç yorumlardan kaçın — dengeli ve cesaretlendirici ol
7. Progress bar gösterimi: ████████░░ (%80) formatı kullan
8. Markdown tabloları kullan

RAPOR FORMATI:
1. 🧠 BÜTÜNCÜL PROFİL HARİTASI (Tablo: Özellik | Tespit | Etki Düzeyi)
2. 💪 SÜPER GÜÇLERİN SENTEZİ (Progress bar ile)
3. 🚧 GİZLİ ENGELLER VE KİLİT ÇÖZÜMLER (🔴 Sorun -> 🟢 Çözüm)
4. 🎓 KİŞİYE ÖZEL ÖĞRENME STRATEJİSİ (Tablo: Yöntem | Araç | Sıklık)
5. 🚀 GELECEK VİZYONU VE KARİYER (En uygun 3 meslek ⭐ ile)
6. 👨‍👩‍👦 AİLE VE ÖĞRETMENE NOT (Blockquote)

Dil: Türkçe. Üslup: Profesyonel, akıcı, görsel olarak zengin."""
                        
                        final_report = get_ai_analysis(prompt)
                        save_holistic_analysis(info.id, selected_tests, final_report)
                        st.success("✅ Bütüncül analiz tamamlandı ve Arşiv'e kaydedildi.")
                        time.sleep(1.5)
                        st.rerun()

                # ====================================================
                # MOD 2: AYRI AYRI ANALİZLER (CLAUDE API)
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
                        
                        prompt = f"""Sen uzman bir eğitim psikoloğusun.
                        
ÖĞRENCİ: {info.name}, Yaş: {info.age}, Cinsiyet: {info.gender}
TEST: {test_name}
VERİLER: {json.dumps(ai_input, ensure_ascii=False)}

GÖREV: Sadece bu teste odaklanarak derinlemesine bir yorum yap.

KURALLAR:
- Sade, çocuk/ergen dostu dil
- Asla klinik tanı koyma
- Somut, uygulanabilir öneriler ver

RAPOR FORMATI:
1. 📊 Test Sonucunun Anlamı (Kısa Özet)
2. 💪 Güçlü Yönler (İkonlu maddeler)
3. 🚧 Gelişim Alanları
4. 🎯 Bu Teste Özel Somut Tavsiyeler

Dil: Türkçe."""
                        
                        single_report = get_ai_analysis(prompt)
                        save_holistic_analysis(info.id, [test_name], single_report)
                    
                    my_bar.empty()
                    st.success(f"✅ {total_ops} test başarıyla analiz edildi ve Arşiv'e eklendi.")
                    time.sleep(2)
                    st.rerun()

    # --- TEST GEÇMİŞİ ---
    st.divider()
    with st.expander("🗂️ Test Geçmişi ve Ham Veriler"):
        if tests:
            df_tests = pd.DataFrame(tests)
            df_tests['date'] = pd.to_datetime(df_tests['date']).dt.strftime('%d.%m.%Y')
            st.dataframe(df_tests[["test_name", "date"]], use_container_width=True)
