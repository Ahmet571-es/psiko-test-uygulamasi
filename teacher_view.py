import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import time
from db_utils import get_all_students_with_results, reset_database, delete_specific_students, get_holistic_analysis, save_holistic_analysis
from openai import OpenAI
import os
from dotenv import load_dotenv

# --- API AYARLARI ---
load_dotenv()
if "GROK_API_KEY" in st.secrets:
    GROK_API_KEY = st.secrets["GROK_API_KEY"]
else:
    GROK_API_KEY = os.getenv("GROK_API_KEY")

client = OpenAI(api_key=GROK_API_KEY, base_url="https://api.x.ai/v1")

# --- YARDIMCI FONKSİYONLAR ---

def get_ai_analysis(prompt):
    """Grok API'ye analiz isteği gönderir."""
    if not GROK_API_KEY:
        return "Hata: API Key bulunamadı."
    try:
        response = client.chat.completions.create(
            model="grok-4-1-fast-reasoning",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Analiz Hatası: {e}"

def plot_scores(data_dict, title):
    """Skor verilerini görselleştirir (Bar Grafiği)."""
    if not data_dict or not isinstance(data_dict, dict):
        return None
    
    # Veriyi hazırla
    labels = [str(k) for k in data_dict.keys()]
    try:
        values = [float(v) for v in data_dict.values()]
    except:
        return None 

    # Grafik Ayarları
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=values, y=labels, ax=ax, palette="viridis", orient='h')
    
    ax.set_title(f"{title} - Puan Dağılımı", fontsize=14, fontweight='bold')
    ax.set_xlabel("Puan / Yüzde")
    ax.set_ylabel("Kategoriler / Tipler")
    plt.tight_layout()
    return fig

# --- ANA ÖĞRETMEN UYGULAMASI ---

def app():
    # --- CSS: MOUSE İŞARETÇİSİ VE STİL AYARLARI ---
    st.markdown("""
    <style>
        .stSelectbox div, .stMultiSelect div, div[data-baseweb="select"], div[role="listbox"] li, div[data-baseweb="tag"] {
            cursor: pointer !important;
        }
        .saved-report-box {
            background-color: #f0fdf4;
            border: 2px solid #22c55e;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
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
                st.info("Kayıtlı öğrenci yok.")
            else:
                st.warning("Veriler silinecektir.")
                selected_to_delete = st.multiselect("Silinecekleri Seç:", options=student_names_all)
                if selected_to_delete:
                    if st.button("SİL"):
                        if delete_specific_students(selected_to_delete):
                            st.success("Silindi.")
                            time.sleep(1)
                            st.rerun()
        
        st.markdown("---")
        with st.expander("⚠️ Fabrika Ayarları"):
            if st.button("SIFIRLA"):
                if reset_database():
                    st.success("Sıfırlandı.")
                    time.sleep(1)
                    st.rerun()

    if not data:
        st.info("📂 Henüz kayıtlı öğrenci verisi bulunmamaktadır.")
        return

    # 1. ÖĞRENCİ SEÇİMİ
    st.subheader("📂 Öğrenci Dosyası Görüntüle")
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_name = st.selectbox("Öğrenci Seçiniz:", student_names_all, index=None, placeholder="Listeden seçin...")
    
    if not selected_name:
        st.info("👆 Lütfen analizlerini görmek istediğiniz öğrenciyi yukarıdaki listeden seçiniz.")
        return

    student_data = next(d for d in data if d["info"].name == selected_name)
    info = student_data["info"]
    tests = student_data["tests"]

    # 2. KİMLİK KARTI
    with st.container():
        st.markdown(f"### 🆔 {info.name}")
        c1, c2, c3, c4 = st.columns(4)
        c1.write(f"Yaş/Cinsiyet: **{info.age} / {info.gender}**")
        c2.write(f"Kullanıcı: **{info.username}**")
        c3.write(f"Şifre: **{info.password}**")
        c4.write(f"Durum: **{info.login_count}. Giriş**")
    
    st.divider()

    # 3. TEST ANALİZ VE RAPORLAMA
    st.subheader("🧩 Çoklu Test Analizi")

    if not tests:
        st.warning("⚠️ Bu öğrenci henüz hiç test tamamlamamış.")
    else:
        st.write("Aşağıdaki listeden analiz etmek istediğiniz testleri seçin.")
        test_names = [t["test_name"] for t in tests]
        selected_tests = st.multiselect("Analize Dahil Edilecek Testler:", options=test_names, default=test_names)
        
        # ANALİZ BUTONU VE MANTIĞI
        if st.button("🧠 ANALİZİ GÖRÜNTÜLE", type="primary"):
            if not selected_tests:
                st.error("Lütfen en az bir test seçiniz.")
            else:
                analyzed_data = [t for t in tests if t["test_name"] in selected_tests]
                
                # A. GRAFİK
                st.markdown("### 📊 Grafiksel Sonuçlar")
                cols = st.columns(2)
                for idx, t in enumerate(analyzed_data):
                    if t["scores"]:
                        fig = plot_scores(t["scores"], t["test_name"])
                        if fig: cols[idx % 2].pyplot(fig)
                        else: cols[idx % 2].info(f"{t['test_name']} grafik verisi yok.")
                
                # B. RAPOR (KAYITLI MI YOKSA YENİ Mİ?)
                st.markdown("### 📝 Bütüncül Analiz Raporu")
                
                # 1. Önce Veritabanına Bak: Bu kombinasyon için rapor var mı?
                saved_report = get_holistic_analysis(info.id, selected_tests)
                
                if saved_report:
                    # VARSA DİREKT GÖSTER (API Harcamaz)
                    st.markdown(f"<div class='saved-report-box'>💾 <b>KAYITLI RAPOR GETİRİLDİ</b><br>Bu test kombinasyonu için daha önce oluşturulmuş analiz aşağıdadır.</div>", unsafe_allow_html=True)
                    st.markdown(saved_report)
                    report_to_download = saved_report
                else:
                    # YOKSA YENİ OLUŞTUR
                    with st.spinner("Yeni analiz yapılıyor ve öğrenci dosyasına kaydediliyor..."):
                        ai_input_data = []
                        for t in analyzed_data:
                            ai_input_data.append({
                                "Test Adı": t["test_name"],
                                "Tarih": str(t["date"]),
                                "Puanlar/Sonuçlar": t["scores"] if t["scores"] else t["raw_answers"]
                            })
                        
                        prompt = f"""
                        Sen uzman bir eğitim psikoloğu ve rehberlikçisin.
                        ÖĞRENCİ: {info.name}, {info.age} yaş, {info.gender}.
                        VERİLER: {json.dumps(ai_input_data, ensure_ascii=False)}
                        GÖREV: Bu verileri BİRLEŞTİREREK bütüncül analiz yaz.
                        FORMAT:
                        1. Öğrenci Profil Özeti
                        2. Güçlü Yönlerin Sentezi
                        3. Gelişim Alanları
                        4. Öğrenme Stratejisi
                        5. Kariyer Eğilimleri
                        6. Tavsiyeler
                        """
                        
                        new_report = get_ai_analysis(prompt)
                        st.markdown(new_report)
                        report_to_download = new_report
                        
                        # VERİTABANINA KAYDET
                        save_holistic_analysis(info.id, selected_tests, new_report)
                        st.success("✅ Rapor öğrenci dosyasına başarıyla kaydedildi.")

                # İNDİRME BUTONU
                st.download_button(
                    label="📥 Raporu İndir (.txt)",
                    data=report_to_download,
                    file_name=f"{info.name}_Analiz_Raporu.txt",
                    mime="text/plain"
                )

    # 4. GEÇMİŞ TABLOSU
    st.divider()
    with st.expander("🗂️ Test Geçmişi ve Ham Veriler"):
        if tests:
            df_tests = pd.DataFrame(tests)
            df_tests['date'] = pd.to_datetime(df_tests['date']).dt.strftime('%d.%m.%Y')
            st.dataframe(df_tests[["test_name", "date"]], use_container_width=True)
