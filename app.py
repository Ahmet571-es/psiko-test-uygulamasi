import streamlit as st
import time
from database import init_db
from db_utils import login_student, register_student

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(
    page_title="Psikometrik Test Platformu",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Veritabanını başlat
init_db()

# --- CSS VE TASARIM AYARLARI ---
st.markdown("""
<style>
    .stButton>button { border-radius: 8px; height: 3em; font-weight: bold; }
    div[data-testid="stForm"] { border: 2px solid #e0e0e0; padding: 30px; border-radius: 15px; background-color: #f9f9f9; }
    .header-text { text-align: center; color: #2E86C1; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'role' not in st.session_state: st.session_state.role = None
if 'student_id' not in st.session_state: st.session_state.student_id = None
if 'student_name' not in st.session_state: st.session_state.student_name = None
if 'login_phase' not in st.session_state: st.session_state.login_phase = 1

# --- ANA GİRİŞ EKRANI FONKSİYONU ---
def main_login():
    st.markdown("<h1 class='header-text'>🧠 Psikometrik Test ve Analiz Merkezi</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # 3 Sekmeli Yapı
    tab1, tab2, tab3 = st.tabs(["🔑 Öğrenci Girişi", "📝 Yeni Öğrenci Kaydı", "👨‍🏫 Öğretmen Girişi"])
    
    # --- SEKME 1: ÖĞRENCİ GİRİŞİ ---
    with tab1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.subheader("Öğrenci Girişi 👋")
            with st.form("student_login_form"):
                user = st.text_input("Kullanıcı Adı")
                pw = st.text_input("Şifre", type="password")
                submitted = st.form_submit_button("Giriş Yap", type="primary", use_container_width=True)
                
                if submitted:
                    status, student_obj = login_student(user, pw)
                    if status:
                        st.success(f"Giriş başarılı! Hoşgeldin {student_obj.name}")
                        st.session_state.role = "student"
                        st.session_state.student_id = student_obj.id
                        st.session_state.student_name = student_obj.name
                        st.session_state.login_phase = student_obj.login_count
                        st.rerun()
                    else:
                        st.error("Kullanıcı adı veya şifre hatalı.")

    # --- SEKME 2: ÖĞRENCİ KAYIT (OTOMATİK YÖNLENDİRMELİ) ---
    with tab2:
        st.subheader("Yeni Hesap Oluştur 🚀")
        st.info("Testlere başlamak için lütfen aşağıdaki formu doldurarak kayıt olun.")
        
        with st.form("register_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Ad Soyad (Tam İsim)")
                age = st.number_input("Yaş", min_value=5, max_value=99, step=1, value=15)
                gender = st.selectbox("Cinsiyet", ["Kız", "Erkek"])
            with c2:
                new_user = st.text_input("Kullanıcı Adı Belirle (Giriş için gerekli)")
                new_pw = st.text_input("Şifre Belirle", type="password")
            
            st.markdown("---")
            reg_submit = st.form_submit_button("Kayıt Ol ve Başla", type="secondary", use_container_width=True)
            
            if reg_submit:
                if not name or not new_user or not new_pw:
                    st.warning("Lütfen tüm alanları doldurunuz.")
                else:
                    # register_student artık (Durum, Nesne/Mesaj) döndürüyor
                    success, result = register_student(name.title(), new_user, new_pw, age, gender)
                    
                    if success:
                        # result burada yeni oluşturulan student objesidir
                        st.success(f"Kayıt Başarılı! Hoşgeldin {result.name}. Test Paneline Yönlendiriliyorsun...")
                        
                        # Otomatik Giriş İşlemi
                        st.session_state.role = "student"
                        st.session_state.student_id = result.id
                        st.session_state.student_name = result.name
                        st.session_state.login_phase = 1 # Yeni kayıt olduğu için 1. Faz
                        
                        time.sleep(1.5) # Kullanıcı mesajı okusun diye kısa bekleme
                        st.rerun()      # Sayfayı yenile ve öğrenci paneline git
                    else:
                        # result burada hata mesajıdır
                        st.error(result)

    # --- SEKME 3: ÖĞRETMEN GİRİŞİ ---
    with tab3:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.subheader("Yönetici Erişimi 🔒")
            with st.form("teacher_login_form"):
                password_input = st.text_input("Yönetici Şifresi:", type="password")
                submitted_t = st.form_submit_button("Yönetim Paneline Git", type="secondary", use_container_width=True)
                
                if submitted_t:
                    secret_pass = "admin123"
                    if "teacher_password" in st.secrets:
                        secret_pass = st.secrets["teacher_password"]
                    
                    if password_input == secret_pass:
                        st.session_state.role = "teacher"
                        st.rerun()
                    else:
                        st.error("Hatalı şifre.")

# --- SAYFA YÖNLENDİRME MANTIĞI ---
if st.session_state.role is None:
    main_login()

elif st.session_state.role == "student":
    import student_view
    student_view.app()

elif st.session_state.role == "teacher":
    import teacher_view
    teacher_view.app()

# --- SIDEBAR: ÇIKIŞ BUTONU ---
if st.session_state.role:
    with st.sidebar:
        st.write(f"Kullanıcı: **{st.session_state.get('student_name', 'Yönetici')}**")
        if st.button("Güvenli Çıkış", type="secondary"):
            st.session_state.clear()
            st.rerun()
