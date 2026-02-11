import streamlit as st
import time
from database import init_db
from db_utils import login_student, register_student

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(
    page_title="BALABAN EĞİTİM-KOÇLUK",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Veritabanını başlat
init_db()

# --- CSS VE TASARIM AYARLARI ---
st.markdown("""
<style>
    .stButton>button { border-radius: 8px; height: 3em; font-weight: bold; width: 100%; }
    .auth-container { border: 2px solid #e0e0e0; padding: 40px; border-radius: 15px; background-color: #ffffff; max-width: 600px; margin: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    
    /* BAŞLIK STİLLERİ */
    .header-text { 
        text-align: center; 
        color: #2E86C1; 
        margin-top: 10px; 
        margin-bottom: 5px; 
        font-weight: 700; 
    }
    
    .brand-text { 
        text-align: center; 
        color: #1F618D; 
        font-size: 1.8rem; 
        font-weight: 800; 
        letter-spacing: 1px; 
        margin-top: 0;
        margin-bottom: 20px;
        border-bottom: 3px solid #AED6F1;
        display: inline-block;
        padding-bottom: 5px;
    }
    
    .sub-link { text-align: center; margin-top: 10px; cursor: pointer; color: #555; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE (OTURUM DEĞİŞKENLERİ) ---
if 'role' not in st.session_state: st.session_state.role = None
if 'student_id' not in st.session_state: st.session_state.student_id = None
if 'student_name' not in st.session_state: st.session_state.student_name = None
if 'login_phase' not in st.session_state: st.session_state.login_phase = 1

# Sayfa Modu Kontrolü (Varsayılan: 'register')
if 'auth_mode' not in st.session_state: st.session_state.auth_mode = 'register' 

# --- NAVİGASYON FONKSİYONLARI ---
def go_to_login():
    st.session_state.auth_mode = 'login'

def go_to_register():
    st.session_state.auth_mode = 'register'

def go_to_teacher():
    st.session_state.auth_mode = 'teacher'

# --- ANA GİRİŞ SİSTEMİ ---
def main_auth_flow():
    # --- KURUMSAL BAŞLIK ALANI (DÜZELTİLDİ: Logo Altta) ---
    st.markdown("""
        <div style="padding: 20px; text-align: center;">
            <h1 class='header-text'>🧠 Psikometrik Test ve Analiz Merkezi</h1>
            <div class='brand-text'>BALABAN EĞİTİM-KOÇLUK</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Ortalamak için kolon yapısı
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # ---------------------------------------------------------
        # 1. MOD: KAYIT OL (VARSAYILAN AÇILIŞ)
        # ---------------------------------------------------------
        if st.session_state.auth_mode == 'register':
            st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
            st.subheader("📝 Yeni Öğrenci Kaydı")
            st.info("Testlere katılmak için önce profilinizi oluşturun.")
            
            with st.form("register_form"):
                name = st.text_input("Ad Soyad (Tam İsim)")
                c1, c2 = st.columns(2)
                age = c1.number_input("Yaş", min_value=5, max_value=99, step=1, value=15)
                gender = c2.selectbox("Cinsiyet", ["Kız", "Erkek"])
                
                st.markdown("---")
                new_user = st.text_input("Kullanıcı Adı Belirle")
                new_pw = st.text_input("Şifre Belirle", type="password")
                
                submit = st.form_submit_button("Kayıt Ol", type="primary")
                
                if submit:
                    if not name or not new_user or not new_pw:
                        st.warning("Lütfen tüm alanları doldurunuz.")
                    else:
                        success, result = register_student(name.title(), new_user, new_pw, age, gender)
                        if success:
                            st.success("✅ Kayıt Başarılı! Giriş ekranına yönlendiriliyorsunuz...")
                            time.sleep(2)
                            st.session_state.auth_mode = 'login' # Otomatik yönlendirme
                            st.rerun()
                        else:
                            st.error(result)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Alt Linkler
            st.markdown("---")
            if st.button("Zaten hesabın var mı? OTURUM AÇ ➡️", on_click=go_to_login): pass
            if st.button("👨‍🏫 Öğretmen Girişi", type="secondary", on_click=go_to_teacher): pass

        # ---------------------------------------------------------
        # 2. MOD: ÖĞRENCİ GİRİŞİ
        # ---------------------------------------------------------
        elif st.session_state.auth_mode == 'login':
            st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
            st.subheader("🔑 Öğrenci Girişi")
            
            with st.form("login_form"):
                user = st.text_input("Kullanıcı Adı")
                pw = st.text_input("Şifre", type="password")
                
                submit = st.form_submit_button("Giriş Yap", type="primary")
                
                if submit:
                    status, student_obj = login_student(user, pw)
                    if status:
                        st.success(f"Hoşgeldin {student_obj.name}!")
                        st.session_state.role = "student"
                        st.session_state.student_id = student_obj.id
                        st.session_state.student_name = student_obj.name
                        st.session_state.login_phase = student_obj.login_count
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Kullanıcı adı veya şifre hatalı.")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Alt Linkler
            st.markdown("---")
            if st.button("⬅️ Hesabın yok mu? KAYIT OL", on_click=go_to_register): pass

        # ---------------------------------------------------------
        # 3. MOD: ÖĞRETMEN GİRİŞİ
        # ---------------------------------------------------------
        elif st.session_state.auth_mode == 'teacher':
            st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
            st.subheader("🔒 Yönetici Girişi")
            
            with st.form("teacher_form"):
                pw = st.text_input("Yönetici Şifresi", type="password")
                submit = st.form_submit_button("Panele Git")
                
                if submit:
                    secret_pass = "admin123"
                    if "teacher_password" in st.secrets:
                        secret_pass = st.secrets["teacher_password"]
                    
                    if pw == secret_pass:
                        st.session_state.role = "teacher"
                        st.rerun()
                    else:
                        st.error("Hatalı şifre.")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Alt Linkler
            st.markdown("---")
            if st.button("⬅️ Öğrenci Ekranına Dön", on_click=go_to_register): pass

# --- YÖNLENDİRME MANTIĞI ---
if st.session_state.role is None:
    main_auth_flow()

elif st.session_state.role == "student":
    import student_view
    student_view.app()

elif st.session_state.role == "teacher":
    import teacher_view
    teacher_view.app()

# --- ÇIKIŞ İŞLEMİ ---
if st.session_state.role:
    with st.sidebar:
        st.write(f"Kullanıcı: **{st.session_state.get('student_name', 'Yönetici')}**")
        if st.button("Güvenli Çıkış", type="secondary"):
            st.session_state.clear()
            st.session_state.auth_mode = 'register' 
            st.rerun()
