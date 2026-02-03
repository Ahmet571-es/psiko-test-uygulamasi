import streamlit as st
from database import init_db
from db_utils import get_or_create_student

# Sayfa Ayarları (EN ÜSTTE OLMALI)
st.set_page_config(
    page_title="Psikometrik Test Platformu",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Veritabanını Başlat
init_db()

# CSS İyileştirmeleri
st.markdown("""
<style>
    .big-font { font-size: 20px !important; }
    .stButton>button { border-radius: 10px; height: 3em; }
    div[data-testid="stForm"] { border: 2px solid #f0f2f6; padding: 20px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# Session State Başlangıç
if 'role' not in st.session_state: st.session_state.role = None
if 'student_id' not in st.session_state: st.session_state.student_id = None
if 'student_name' not in st.session_state: st.session_state.student_name = None

# --- GİRİŞ SAYFASI ---
def login_page():
    st.title("🧠 Psikometrik Test ve Analiz Merkezi")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    # --- SOL: ÖĞRENCİ GİRİŞİ ---
    with col1:
        st.header("🎓 Öğrenci Girişi")
        st.info("Testlere başlamak için Adınızı ve Soyadınızı giriniz.")
        
        with st.form("student_login"):
            name_input = st.text_input("Adınız Soyadınız:", placeholder="Örn: Ahmet Yılmaz")
            submitted = st.form_submit_button("Giriş Yap", type="primary", use_container_width=True)
            
            if submitted:
                # Temizle ve Baş Harfleri Büyüt
                clean_name = name_input.strip().title()
                
                # KONTROL: En az 2 kelime (Ad + Soyad) var mı?
                if len(clean_name.split()) < 2:
                    st.error("⚠️ Lütfen hem Adınızı hem de Soyadınızı tam giriniz. (Örn: Ali Kaya)")
                elif len(clean_name) < 5: # Çok kısa isim kontrolü
                    st.error("⚠️ Lütfen geçerli bir isim giriniz.")
                else:
                    # Giriş Başarılı
                    s_id, s_name = get_or_create_student(clean_name)
                    st.session_state.role = "student"
                    st.session_state.student_id = s_id
                    st.session_state.student_name = s_name
                    st.rerun()

    # --- SAĞ: ÖĞRETMEN GİRİŞİ ---
    with col2:
        st.header("👨‍🏫 Öğretmen Girişi")
        st.info("Yönetim paneli erişimi.")
        
        with st.form("teacher_login"):
            password_input = st.text_input("Yönetici Şifresi:", type="password")
            submitted_t = st.form_submit_button("Yönetim Paneline Git", type="secondary", use_container_width=True)
            
            if submitted_t:
                # Şifre kontrolü: Önce st.secrets (Cloud), yoksa 'admin123'
                secret_pass = "admin123"
                if "teacher_password" in st.secrets:
                    secret_pass = st.secrets["teacher_password"]
                
                if password_input == secret_pass:
                    st.session_state.role = "teacher"
                    st.rerun()
                else:
                    st.error("⛔ Hatalı şifre.")

# --- SAYFA YÖNLENDİRME ---
if st.session_state.role is None:
    login_page()

elif st.session_state.role == "student":
    import student_view
    student_view.app()

elif st.session_state.role == "teacher":
    import teacher_view
    teacher_view.app()

# ÇIKIŞ BUTONU (SIDEBAR)
with st.sidebar:
    if st.session_state.role:
        st.write(f"Kullanıcı: **{st.session_state.get('student_name', 'Yönetici')}**")
        if st.button("Çıkış Yap"):
            st.session_state.clear()
            st.rerun()
