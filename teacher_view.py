import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import time  # <--- İşte hatayı çözen sihirli satır burası
from db_utils import get_all_students_with_results, reset_database, delete_specific_students
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
    
    # Renk paleti
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
        /* Selectbox (Açılır Liste) üzerine gelince el işareti çıksın */
        div[data-baseweb="select"] {
            cursor: pointer !important;
        }
        /* Dropdown içindeki öğelere de el işareti */
        div[role="listbox"] li {
            cursor: pointer !important;
        }
        .stSelectbox > div > div {
            cursor: pointer !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("👨‍🏫 Öğretmen Yönetim Paneli")
    st.markdown("---")

    # Verileri Çek
    data = get_all_students_with_results()
    
    # Öğrenci İsim Listesi
    student_names_all = [d["info"].name for d in data] if data else []

    # --- SIDEBAR: YÖNETİM VE SİLME ---
    with st.sidebar:
        st.header("⚙️ Yönetim Araçları")
        
        # 1. ÖĞRENCİ SİLME MODÜLÜ
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
                            time.sleep(1) # Artık hata vermeyecek
                            st.rerun()
                        else:
                            st.error("Silme başarısız.")

        st.markdown("---")
        
        # 2. TAM SIFIRLAMA
        with st.expander("⚠️ Fabrika Ayarlarına Dön"):
            st.error("DİKKAT: Her şey silinir.")
            if st.button("TÜM SİSTEMİ SIFIRLA"):
                if reset_database():
                    st.success("Sistem sıfırlandı.")
                    time.sleep(1)
                    st.rerun()

    # --- ANA EKRAN İÇERİĞİ ---
    
    if not data:
        st.info("📂 Henüz kayıtlı öğrenci verisi bulunmamaktadır.")
        return

    # 1. ÖĞRENCİ SEÇİMİ (VARSAYILAN BOŞ VE İŞARET PARMAĞI İKONLU)
    st.subheader("📂 Öğrenci Dosyası Görüntüle")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        # index=None ile varsayılan boş gelir
        selected_name = st.selectbox(
            "İncelemek İstediğiniz Öğrenciyi Seçiniz:", 
            student_names_all, 
            index=None, 
            placeholder="Listeden bir öğrenci seçin..."
        )
    
    # EĞER SEÇİM YAPILMADIYSA BURADA DUR VE BİLGİ VER
    if not selected_name:
        st.info("👆 Lütfen analizlerini görmek istediğiniz öğrenciyi yukarıdaki listeden seçiniz.")
        return

    # SEÇİM YAPILDIYSA DEVAM ET
    student_data = next(d for d in data if d["info"].name == selected_name)
    info = student_data["info"]
    tests = student_data["tests"]

    # 2. ÖĞRENCİ KİMLİK KARTI
    with st.container():
        st.markdown(f"### 🆔 {info.name}")
        c1, c2, c3, c4 = st.columns(4)
        c1.caption("Yaş / Cinsiyet")
        c1.write(f"**{info.age} / {info.gender}**")
        
        c2.caption("Kullanıcı Adı")
        c2.write(f"**{info.username}**")
        
        c3.caption("Şifre")
        c3.write(f"**{info.password}**")
        
        c4.caption("Durum")
        c4.write(f"**{info.login_count}. Giriş**")
    
    st.divider()

    # 3. TEST ANALİZ VE RAPORLAMA
    st.subheader("🧩 Çoklu Test Analizi")

    if not tests:
        st.warning("⚠️ Bu öğrenci henüz hiç test tamamlamamış.")
    else:
        st.write("Aşağıdaki listeden analiz etmek istediğiniz testleri seçin.")
        
        test_names = [t["test_name"] for t in tests]
        selected_tests = st.multiselect(
            "Analize Dahil Edilecek Testler:",
            options=test_names,
            default=test_names
        )
        
        if st.button("🧠 SEÇİLEN TESTLERİ ANALİZ ET", type="primary"):
            if not selected_tests:
                st.error("Lütfen en az bir test seçiniz.")
            else:
                analyzed_data = [t for t in tests if t["test_name"] in selected_tests]
                
                # --- A. GRAFİK GÖSTERİMİ ---
                st.markdown("### 📊 Grafiksel Sonuçlar")
                cols = st.columns(2)
                for idx, t in enumerate(analyzed_data):
                    if t["scores"]:
                        fig = plot_scores(t["scores"], t["test_name"])
                        if fig:
                            cols[idx % 2].pyplot(fig)
                        else:
                            cols[idx % 2].info(f"{t['test_name']} için grafik verisi yok.")
                
                # --- B. YAPAY ZEKA RAPORU ---
                st.markdown("### 📝 Yapay Zeka Destekli Bütüncül Rapor")
                
                with st.spinner("Yapay zeka verileri harmanlıyor ve raporu yazıyor..."):
                    ai_input_data = []
                    for t in analyzed_data:
                        ai_input_data.append({
                            "Test Adı": t["test_name"],
                            "Tarih": str(t["date"]),
                            "Puanlar/Sonuçlar": t["scores"] if t["scores"] else t["raw_answers"]
                        })
                    
                    prompt = f"""
                    Sen uzman bir eğitim psikoloğu ve rehberlikçisin.
                    
                    ÖĞRENCİ PROFİLİ:
                    Ad: {info.name}, Yaş: {info.age}, Cinsiyet: {info.gender}
                    
                    YAPILAN TESTLER VE SONUÇLARI:
                    {json.dumps(ai_input_data, ensure_ascii=False)}
                    
                    GÖREV:
                    Yukarıdaki test sonuçlarını BİRLEŞTİREREK (Sentezleyerek) bu öğrenci için bütüncül bir analiz raporu yaz.
                    Testleri tek tek anlatma; sonuçların birbiriyle ilişkisini kur.
                    
                    RAPOR DİLİ:
                    Son derece yalın, akıcı, motive edici ve anlaşılır bir Türkçe kullan.
                    
                    RAPOR BAŞLIKLARI:
                    1. **Öğrenci Profil Özeti:** (Kişilik, zeka ve ilgi alanlarının özeti)
                    2. **Güçlü Yönlerin Sentezi:** (Farklı testlerden gelen güçlü yanların uyumu)
                    3. **Gelişim Alanları ve Destek Noktaları:** (Dikkat edilmesi gerekenler)
                    4. **Öğrenme ve Çalışma Stratejisi:** (Bu öğrenci en iyi nasıl öğrenir?)
                    5. **Kariyer ve İlgi Eğilimleri:** (Hangi alanlara yatkın?)
                    6. **Öğretmene ve Aileye Özel Tavsiyeler**
                    """
                    
                    report_text = get_ai_analysis(prompt)
                    st.markdown(report_text)
                    
                    st.download_button(
                        label="📥 Bu Raporu İndir (.txt)",
                        data=report_text,
                        file_name=f"{info.name}_Bütüncül_Analiz_Raporu.txt",
                        mime="text/plain"
                    )

    # 4. GEÇMİŞ TABLOSU
    st.divider()
    with st.expander("🗂️ Test Geçmişi ve Ham Veriler (Detaylı Liste)"):
        if tests:
            df_tests = pd.DataFrame(tests)
            df_tests['date'] = pd.to_datetime(df_tests['date']).dt.strftime('%d.%m.%Y')
            st.dataframe(df_tests[["test_name", "date"]], use_container_width=True)
