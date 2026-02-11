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

# --- API AYARLARI ---
load_dotenv()
if "GROK_API_KEY" in st.secrets:
    GROK_API_KEY = st.secrets["GROK_API_KEY"]
else:
    GROK_API_KEY = os.getenv("GROK_API_KEY")

client = OpenAI(api_key=GROK_API_KEY, base_url="https://api.x.ai/v1")

# --- YARDIMCI FONKSİYONLAR ---
def get_ai_analysis(prompt):
    if not GROK_API_KEY: return "Hata: API Key bulunamadı."
    try:
        response = client.chat.completions.create(
            model="grok-4-1-fast-reasoning",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e: return f"Analiz Hatası: {e}"

def plot_scores(data_dict, title):
    if not data_dict or not isinstance(data_dict, dict): return None
    labels = [str(k) for k in data_dict.keys()]
    try: values = [float(v) for v in data_dict.values()]
    except: return None 
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=values, y=labels, ax=ax, palette="viridis", orient='h')
    ax.set_title(f"{title} - Puan Dağılımı", fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig

# --- ANA UYGULAMA ---
def app():
    st.markdown("""
    <style>
        .stSelectbox div, .stMultiSelect div, div[data-baseweb="select"] { cursor: pointer !important; }
        .archive-box { background-color: #f8f9fa; border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
        .report-header { color: #155724; background-color: #d4edda; padding: 10px; border-radius: 5px; margin-bottom: 10px; border: 1px solid #c3e6cb; }
    </style>
    """, unsafe_allow_html=True)

    st.title("👨‍🏫 Öğretmen Yönetim Paneli")
    st.markdown("---")

    data = get_all_students_with_results()
    student_names_all = [d["info"].name for d in data] if data else []

    # --- SIDEBAR ---
    with st.sidebar:
        st.header("⚙️ Yönetim")
        with st.expander("🗑️ Öğrenci Sil"):
            if not student_names_all: st.info("Öğrenci yok.")
            else:
                to_del = st.multiselect("Seç:", student_names_all)
                if to_del and st.button("SİL"):
                    delete_specific_students(to_del)
                    st.success("Silindi."); time.sleep(1); st.rerun()
        with st.expander("⚠️ Sıfırla"):
            if st.button("TÜMÜNÜ SIFIRLA"):
                reset_database(); st.success("Sıfırlandı."); time.sleep(1); st.rerun()

    if not data:
        st.info("📂 Henüz kayıtlı veri yok.")
        return

    # 1. ÖĞRENCİ SEÇİMİ
    st.subheader("📂 Öğrenci Dosyası")
    selected_name = st.selectbox("Öğrenci Seçiniz:", student_names_all, index=None, placeholder="Listeden seçin...")
    
    if not selected_name:
        st.info("👆 Analiz için bir öğrenci seçiniz.")
        return

    student_data = next(d for d in data if d["info"].name == selected_name)
    info = student_data["info"]
    tests = student_data["tests"]

    # 2. KİMLİK KARTI
    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Öğrenci", info.name)
        c2.metric("Yaş/Cinsiyet", f"{info.age} / {info.gender}")
        c3.metric("Kullanıcı Adı", info.username)
        c4.metric("Giriş Sayısı", info.login_count)
    st.divider()

    # ============================================================
    # 3. YENİ ÖZELLİK: KAYITLI RAPOR ARŞİVİ (BURASI EKLENDİ)
    # ============================================================
    st.subheader("📂 Kayıtlı Rapor Arşivi")
    
    # Veritabanından bu öğrencinin geçmiş raporlarını çek
    history = get_student_analysis_history(info.id)
    
    if not history:
        st.info("Bu öğrenci için henüz oluşturulmuş bütüncül bir analiz raporu yok.")
    else:
        st.markdown(f"Bu öğrenci için **{len(history)} adet** kayıtlı rapor bulundu. Görüntülemek için aşağıdan seçiniz:")
        
        # Raporları listele (Expander içinde veya butonlarla)
        for idx, record in enumerate(history):
            # Başlık Örneği: "Enneagram + VARK (12.02.2024)"
            btn_label = f"📄 Rapor {idx+1}: {record['combination']} ({record['date']})"
            
            with st.expander(btn_label):
                st.markdown(f"<div class='report-header'><b>ANALİZ EDİLEN TESTLER:</b> {record['combination']}</div>", unsafe_allow_html=True)
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
    # 4. YENİ ANALİZ OLUŞTURMA MODÜLÜ
    # ============================================================
    st.subheader("⚡ Yeni Analiz Oluştur")
    
    if not tests:
        st.warning("⚠️ Bu öğrenci henüz hiç test çözmemiş. Analiz yapılamaz.")
    else:
        st.write("Yeni bir rapor oluşturmak için analiz edilecek testleri seçin:")
        
        test_names = [t["test_name"] for t in tests]
        selected_tests = st.multiselect("Testleri Seç:", options=test_names, default=test_names)
        
        if st.button("🧠 YENİ ANALİZ OLUŞTUR VE KAYDET", type="primary"):
            if not selected_tests:
                st.error("En az bir test seçmelisiniz.")
            else:
                analyzed_data = [t for t in tests if t["test_name"] in selected_tests]
                
                # Grafik
                st.markdown("### 📊 Puan Grafikleri")
                gc = st.columns(2)
                for i, t in enumerate(analyzed_data):
                    if t["scores"]:
                        fig = plot_scores(t["scores"], t["test_name"])
                        if fig: gc[i%2].pyplot(fig)

                # Yapay Zeka Analizi
                with st.spinner("Yapay zeka analiz yapıyor ve arşive kaydediyor..."):
                    ai_input = []
                    for t in analyzed_data:
                        ai_input.append({
                            "Test": t["test_name"],
                            "Tarih": str(t["date"]),
                            "Sonuçlar": t["scores"] if t["scores"] else t["raw_answers"]
                        })
                    
                    prompt = f"""
                    Sen uzman bir eğitim psikoloğusun.
                    ÖĞRENCİ: {info.name}, {info.age}, {info.gender}.
                    VERİLER: {json.dumps(ai_input, ensure_ascii=False)}
                    GÖREV: Bütüncül analiz raporu yaz.
                    BAŞLIKLAR: Profil Özeti, Güçlü Yönler, Gelişim Alanları, Öğrenme Stratejisi, Kariyer, Tavsiyeler.
                    """
                    
                    final_report = get_ai_analysis(prompt)
                    
                    # Veritabanına Kaydet
                    save_holistic_analysis(info.id, selected_tests, final_report)
                    
                    st.success("✅ Analiz tamamlandı ve arşive kaydedildi! Yukarıdaki 'Kayıtlı Rapor Arşivi' bölümünden her zaman ulaşabilirsiniz.")
                    
                    # Anlık Gösterim
                    st.markdown("### 📝 Oluşturulan Rapor")
                    st.markdown(final_report)

    # 5. HAM VERİLER TABLOSU
    st.divider()
    with st.expander("🗂️ Test Geçmişi (Liste)"):
        if tests:
            df = pd.DataFrame(tests)
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%d.%m.%Y')
            st.dataframe(df[["test_name", "date"]], use_container_width=True)
