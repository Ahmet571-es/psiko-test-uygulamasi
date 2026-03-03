import streamlit as st
import time
import os
import base64

# DÜZELTME: repair_database de import edildi (Supabase uyumu)
from db_utils import init_db, login_student, register_student, reset_student_password, repair_database

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(
    page_title="EĞİTİM CHECK UP",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 🛠️ VERİTABANI BAŞLATMA
# =========================================================
init_db()

# =========================================================
# 🎨 LOGO YÜKLEME FONKSİYONU
# =========================================================
@st.cache_data
def get_logo_base64():
    """
    Logo dosyasını base64 formatında döndürür.
    Proje kök dizininde 'logo.png' veya 'logo.jpeg' arar.
    Bulamazsa None döner.
    """
    for fname in ["logo.png", "logo.jpeg", "logo.jpg", "assets/logo.png", "assets/logo.jpeg"]:
        if os.path.exists(fname):
            with open(fname, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            ext = fname.rsplit(".", 1)[-1]
            mime = "image/png" if ext == "png" else "image/jpeg"
            return f"data:{mime};base64,{data}"
    return None


# =========================================================
# 🎨 MERKEZ TASARIM SİSTEMİ (CSS)
# =========================================================
st.markdown("""
<style>
    /* ========== GENEL SIFIRLAMA ========== */
    .stApp {
        background: linear-gradient(135deg, #F4F6F9 0%, #E8EDF3 50%, #F4F6F9 100%);
    }
    
    /* ========== BUTON STİLLERİ ========== */
    .stButton > button {
        border-radius: 10px;
        height: 3em;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        border: none;
        letter-spacing: 0.3px;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #1B2A4A 0%, #2E86C1 100%);
        color: white;
    }
    .stButton > button[kind="secondary"] {
        background: #ffffff;
        color: #1B2A4A;
        border: 2px solid #1B2A4A;
    }
    
    /* ========== AUTH CONTAINER ========== */
    .auth-container {
        background: #ffffff;
        border: 1px solid #E0E4EA;
        padding: 40px 35px;
        border-radius: 20px;
        max-width: 600px;
        margin: 0 auto;
        box-shadow: 0 8px 30px rgba(27, 42, 74, 0.08);
        position: relative;
        overflow: hidden;
    }
    .auth-container::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #1B2A4A, #C0392B, #2E86C1);
    }
    
    /* ========== LOGO VE BAŞLIK ========== */
    .brand-area {
        text-align: center;
        padding: 20px 0 10px 0;
    }
    .brand-area img {
        max-height: 90px;
        margin-bottom: 8px;
    }
    .brand-title {
        font-size: 2.6rem;
        font-weight: 900;
        color: #1B2A4A;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 0;
        line-height: 1.2;
    }
    .brand-subtitle {
        font-size: 1.05rem;
        color: #C0392B;
        font-weight: 500;
        margin-top: 4px;
        letter-spacing: 0.5px;
    }
    
    /* ========== DIVIDER ========== */
    .brand-divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #1B2A4A, #C0392B, #1B2A4A, transparent);
        margin: 15px auto 25px auto;
        max-width: 400px;
        border-radius: 2px;
    }
    
    /* ========== FORM STİLLERİ ========== */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1.5px solid #D5DAE1;
        padding: 10px 14px;
        font-size: 0.95rem;
        transition: border-color 0.3s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: #2E86C1;
        box-shadow: 0 0 0 3px rgba(46, 134, 193, 0.15);
    }
    .stNumberInput > div > div > input {
        border-radius: 10px;
    }
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    
    /* ========== VERSION BADGE ========== */
    .version-badge {
        position: fixed;
        bottom: 10px;
        right: 15px;
        background: rgba(27, 42, 74, 0.08);
        color: #1B2A4A;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        letter-spacing: 0.5px;
    }
    
    /* ========== SIDEBAR İYİLEŞTİRME ========== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B2A4A 0%, #2C3E6B 100%);
    }
    /* Tüm metin beyaz */
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    /* Expander başlıkları */
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 8px;
        margin-bottom: 8px;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] summary {
        color: #FFFFFF !important;
        font-weight: 600;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] svg {
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
    }
    /* Butonlar */
    [data-testid="stSidebar"] .stButton > button,
    [data-testid="stSidebar"] .stDownloadButton > button {
        background: rgba(255,255,255,0.15) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover,
    [data-testid="stSidebar"] .stDownloadButton > button:hover {
        background: rgba(255,255,255,0.25) !important;
    }
    /* Bilgi/uyarı kutuları */
    [data-testid="stSidebar"] [data-testid="stAlert"] {
        background: rgba(255,255,255,0.10) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    [data-testid="stSidebar"] [data-testid="stAlert"] p,
    [data-testid="stSidebar"] [data-testid="stAlert"] span {
        color: #FFFFFF !important;
    }
    /* Checkbox */
    [data-testid="stSidebar"] [data-testid="stCheckbox"] label span {
        color: #FFFFFF !important;
    }
    /* Multiselect */
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] label,
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] span {
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] > div > div {
        background: rgba(255,255,255,0.1) !important;
        border-color: rgba(255,255,255,0.3) !important;
    }
    /* Caption */
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: rgba(255,255,255,0.7) !important;
    }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
        color: rgba(255,255,255,0.7) !important;
    }
    /* Ayırıcı çizgi */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.2) !important;
    }
    
    /* ========== ANİMASYONLAR ========== */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .animate-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* ========== GİZLİ STREAMLIT ELEMANLARI ========== */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# --- SESSION STATE (OTURUM DEĞİŞKENLERİ) ---
if 'role' not in st.session_state:
    st.session_state.role = None
if 'student_id' not in st.session_state:
    st.session_state.student_id = None
if 'student_name' not in st.session_state:
    st.session_state.student_name = None
if 'login_phase' not in st.session_state:
    st.session_state.login_phase = 1
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'register'


# --- NAVİGASYON FONKSİYONLARI ---
def go_to_login():
    st.session_state.auth_mode = 'login'

def go_to_register():
    st.session_state.auth_mode = 'register'

def go_to_teacher():
    st.session_state.auth_mode = 'teacher'

def go_to_forgot_password():
    st.session_state.auth_mode = 'forgot_password'


# --- ÖĞRETMEN ŞİFRESİ ALMA FONKSİYONU ---
def get_teacher_password():
    """Öğretmen şifresini güvenli şekilde alır."""
    try:
        if "teacher_password" in st.secrets:
            return st.secrets["teacher_password"]
    except Exception:
        pass
    env_pw = os.getenv("TEACHER_PASSWORD")
    if env_pw:
        return env_pw
    return None


# =========================================================
# 🏠 MARKA BAŞLIK ALANI
# =========================================================
def render_brand_header():
    """Logo + başlık + alt başlık alanını oluşturur."""
    logo_b64 = get_logo_base64()

    # Inline Anka Kuşu SVG — harici dosya gerektirmez
    phoenix_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="90" height="90">
      <defs>
        <linearGradient id="wing_grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#C0392B"/>
          <stop offset="50%" stop-color="#E74C3C"/>
          <stop offset="100%" stop-color="#F39C12"/>
        </linearGradient>
        <linearGradient id="body_grad" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#1B2A4A"/>
          <stop offset="100%" stop-color="#2E86C1"/>
        </linearGradient>
        <linearGradient id="tail_grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#E74C3C"/>
          <stop offset="40%" stop-color="#F39C12"/>
          <stop offset="100%" stop-color="#F1C40F"/>
        </linearGradient>
        <filter id="glow">
          <feGaussianBlur stdDeviation="2" result="blur"/>
          <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
      </defs>
      <!-- Alev halesi -->
      <ellipse cx="100" cy="95" rx="55" ry="60" fill="none" stroke="#F39C12" stroke-width="1.5" opacity="0.2"/>
      <!-- Sol kanat -->
      <path d="M100,85 Q60,40 30,55 Q45,30 65,25 Q50,15 70,10 Q80,25 85,45 Q90,60 100,85Z"
            fill="url(#wing_grad)" opacity="0.9" filter="url(#glow)"/>
      <!-- Sağ kanat -->
      <path d="M100,85 Q140,40 170,55 Q155,30 135,25 Q150,15 130,10 Q120,25 115,45 Q110,60 100,85Z"
            fill="url(#wing_grad)" opacity="0.9" filter="url(#glow)"/>
      <!-- Gövde -->
      <path d="M100,60 Q90,80 88,110 Q90,135 100,155 Q110,135 112,110 Q110,80 100,60Z"
            fill="url(#body_grad)"/>
      <!-- Baş -->
      <circle cx="100" cy="58" r="14" fill="url(#body_grad)"/>
      <!-- Gaga -->
      <path d="M100,68 L96,75 L100,73 L104,75Z" fill="#F39C12"/>
      <!-- Gözler -->
      <circle cx="93" cy="55" r="2.5" fill="#F1C40F"/>
      <circle cx="107" cy="55" r="2.5" fill="#F1C40F"/>
      <circle cx="93.5" cy="55" r="1" fill="#1B2A4A"/>
      <circle cx="107.5" cy="55" r="1" fill="#1B2A4A"/>
      <!-- Tepe tüyü / alev -->
      <path d="M100,44 Q97,32 100,22 Q103,32 100,44Z" fill="#E74C3C" opacity="0.9"/>
      <path d="M100,44 Q93,35 91,26 Q96,33 100,44Z" fill="#F39C12" opacity="0.7"/>
      <path d="M100,44 Q107,35 109,26 Q104,33 100,44Z" fill="#F39C12" opacity="0.7"/>
      <!-- Kuyruk tüyleri -->
      <path d="M100,155 Q90,165 80,185 Q92,175 100,165Z" fill="url(#tail_grad)" opacity="0.8"/>
      <path d="M100,155 Q100,170 100,190 Q100,175 100,165Z" fill="url(#tail_grad)" opacity="0.9"/>
      <path d="M100,155 Q110,165 120,185 Q108,175 100,165Z" fill="url(#tail_grad)" opacity="0.8"/>
      <!-- Kanat ucu kıvılcımları -->
      <circle cx="32" cy="53" r="2" fill="#F39C12" opacity="0.6"/>
      <circle cx="168" cy="53" r="2" fill="#F39C12" opacity="0.6"/>
      <circle cx="70" cy="12" r="1.5" fill="#E74C3C" opacity="0.5"/>
      <circle cx="130" cy="12" r="1.5" fill="#E74C3C" opacity="0.5"/>
    </svg>'''

    if logo_b64:
        st.markdown(f"""
            <div class="brand-area animate-in">
                <img src="{logo_b64}" alt="Eğitim Check Up Logo" />
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="brand-area animate-in">
                <div style="margin-bottom: 6px;">{phoenix_svg}</div>
                <div class="brand-title">EĞİTİM CHECK UP</div>
                <div class="brand-subtitle">Kişisel Eğitim & Kariyer Analiz Merkezi</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="brand-divider"></div>', unsafe_allow_html=True)


# =========================================================
# 🔐 ANA GİRİŞ SİSTEMİ
# =========================================================
def main_auth_flow():
    render_brand_header()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # ---------------------------------------------------------
        # 1. MOD: KAYIT OL
        # ---------------------------------------------------------
        if st.session_state.auth_mode == 'register':
            st.markdown("<div class='auth-container animate-in'>", unsafe_allow_html=True)
            st.markdown("#### 📝 Yeni Öğrenci Kaydı")
            st.info("💡 Testlere katılmak için önce profilini oluştur. Sadece 1 dakika!")
            
            with st.form("register_form"):
                name = st.text_input("👤 Ad Soyad", placeholder="Tam adını yaz...")
                c1, c2, c3 = st.columns(3)
                age = c1.number_input("🎂 Yaş", min_value=5, max_value=99, step=1, value=15)
                grade = c2.selectbox("🎓 Sınıf", options=[5, 6, 7, 8, 9, 10, 11, 12], index=3)
                gender = c3.selectbox("⚧ Cinsiyet", ["Kız", "Erkek"])
                
                st.markdown("---")
                new_user = st.text_input("📧 E-posta Adresi", placeholder="ornek@email.com")
                new_pw = st.text_input("🔒 Şifre Belirle", type="password", placeholder="En az 4 karakter")
                secret_word = st.text_input(
                    "🛡️ Gizli Kurtarma Kelimesi",
                    placeholder="Şifreni unutursan bu kelime lazım olacak",
                    help="Şifreni sıfırlamak istediğinde bu kelimeyi soracağız."
                )
                
                submit = st.form_submit_button("🚀 Kayıt Ol", type="primary")
                
                if submit:
                    import re
                    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                    if not name or not new_user or not new_pw or not secret_word:
                        st.warning("⚠️ Lütfen tüm alanları doldurunuz.")
                    elif len(new_pw) < 4:
                        st.warning("⚠️ Şifre en az 4 karakter olmalıdır.")
                    elif not re.match(email_pattern, new_user.strip()):
                        st.warning("⚠️ Geçerli bir e-posta adresi giriniz. (Örn: ornek@email.com)")
                    else:
                        success, result = register_student(
                            name.title(), new_user.strip().lower(), new_pw,
                            age, gender, secret_word.lower().strip(), grade
                        )
                        if success:
                            st.success("✅ Kayıt Başarılı! Giriş ekranına yönlendiriliyorsun...")
                            time.sleep(1.5)
                            st.session_state.auth_mode = 'login'
                            st.rerun()
                        else:
                            st.error(result)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            link_col1, link_col2 = st.columns(2)
            link_col1.button("🔑 Zaten hesabın var mı? GİRİŞ YAP", on_click=go_to_login)
            link_col2.button("👨‍🏫 Öğretmen / Yönetici Girişi", on_click=go_to_teacher)

        # ---------------------------------------------------------
        # 2. MOD: ÖĞRENCİ GİRİŞİ
        # ---------------------------------------------------------
        elif st.session_state.auth_mode == 'login':
            st.markdown("<div class='auth-container animate-in'>", unsafe_allow_html=True)
            st.markdown("#### 🔑 Öğrenci Girişi")
            st.caption("E-posta adresin ve şifrenle giriş yap.")
            
            with st.form("login_form"):
                user = st.text_input("📧 E-posta Adresi", placeholder="E-posta adresini gir...")
                pw = st.text_input("🔒 Şifre", type="password", placeholder="Şifreni gir...")
                
                submit = st.form_submit_button("Giriş Yap ➡️", type="primary")
                
                if submit:
                    if not user or not pw:
                        st.warning("⚠️ E-posta ve şifre boş bırakılamaz.")
                    else:
                        status, student_obj = login_student(user.strip().lower(), pw)
                        if status:
                            st.success(f"🎉 Hoşgeldin {student_obj.name}!")
                            st.session_state.role = "student"
                            st.session_state.student_id = student_obj.id
                            st.session_state.student_name = student_obj.name
                            st.session_state.student_age = student_obj.age
                            st.session_state.student_grade = student_obj.grade
                            st.session_state.login_phase = student_obj.login_count
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("❌ E-posta adresi veya şifre hatalı.")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            col_a.button("📝 Hesabın yok mu? KAYIT OL", on_click=go_to_register)
            col_b.button("❓ Şifremi Unuttum", on_click=go_to_forgot_password)

        # ---------------------------------------------------------
        # 3. MOD: ŞİFREMİ UNUTTUM
        # ---------------------------------------------------------
        elif st.session_state.auth_mode == 'forgot_password':
            st.markdown("<div class='auth-container animate-in'>", unsafe_allow_html=True)
            st.markdown("#### 🔐 Şifre Sıfırlama")
            st.info("Kayıt olurken belirlediğin gizli kurtarma kelimesini kullanarak yeni şifre belirleyebilirsin.")
            
            with st.form("forgot_password_form"):
                user = st.text_input("📧 E-posta Adresi", placeholder="Kayıtlı e-posta adresini gir...")
                secret = st.text_input("🛡️ Gizli Kurtarma Kelimesi", type="password")
                new_pw = st.text_input("🔒 Yeni Şifre Belirle", type="password")
                
                submit = st.form_submit_button("Şifremi Yenile ✅", type="primary")
                
                if submit:
                    if not user or not secret or not new_pw:
                        st.warning("⚠️ Lütfen tüm alanları doldurunuz.")
                    elif len(new_pw) < 4:
                        st.warning("⚠️ Yeni şifre en az 4 karakter olmalıdır.")
                    else:
                        success, msg = reset_student_password(user.strip().lower(), secret.lower().strip(), new_pw)
                        if success:
                            st.success("✅ Şifren güncellendi! Yönlendiriliyorsun...")
                            time.sleep(1.5)
                            st.session_state.auth_mode = 'login'
                            st.rerun()
                        else:
                            st.error(msg)
                            
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.button("⬅️ Giriş Ekranına Dön", on_click=go_to_login)

        # ---------------------------------------------------------
        # 4. MOD: ÖĞRETMEN GİRİŞİ
        # ---------------------------------------------------------
        elif st.session_state.auth_mode == 'teacher':
            st.markdown("<div class='auth-container animate-in'>", unsafe_allow_html=True)
            st.markdown("#### 🔒 Yönetici / Öğretmen Girişi")
            st.caption("Bu alan yalnızca yetkili personel içindir.")
            
            with st.form("teacher_form"):
                pw = st.text_input("🔑 Yönetici Şifresi", type="password")
                submit = st.form_submit_button("Panele Git ➡️", type="primary")
                
                if submit:
                    secret_pass = get_teacher_password()
                    if secret_pass is None:
                        st.error("⚠️ Yönetici şifresi yapılandırılmamış. Sistem yöneticisiyle iletişime geçin.")
                    elif pw == secret_pass:
                        st.session_state.role = "teacher"
                        st.rerun()
                    else:
                        st.error("❌ Hatalı şifre.")
            
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.button("⬅️ Öğrenci Ekranına Dön", on_click=go_to_register)
    
    st.markdown('<div class="version-badge">EĞİTİM CHECK UP v2.0</div>', unsafe_allow_html=True)


# =========================================================
# 🚀 YÖNLENDİRME MANTIĞI
# =========================================================
if st.session_state.role is None:
    main_auth_flow()

elif st.session_state.role == "student":
    import student_view
    student_view.app()

elif st.session_state.role == "teacher":
    import teacher_view
    teacher_view.app()


# =========================================================
# 📌 SIDEBAR — OTURUM AÇIKKEN
# =========================================================
if st.session_state.role:
    with st.sidebar:
        role_label = "👨‍🏫 Yönetici" if st.session_state.role == "teacher" else "🎓 Öğrenci"
        user_name = st.session_state.get('student_name', 'Yönetici')
        
        st.markdown(f"""
            <div style="text-align:center; padding: 10px 0;">
                <div style="font-size: 2rem;">{'👨‍🏫' if st.session_state.role == 'teacher' else '🎓'}</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #FFFFFF; margin-top: 5px;">{user_name}</div>
                <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7); margin-top: 2px;">{role_label}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Öğretmen ise veritabanı onarım butonu
        # DÜZELTME: Artık SQLite dosya silme yerine repair_database() kullanıyor
        if st.session_state.role == "teacher":
            if st.button("🔧 Veritabanını Onar", help="Veritabanı hatası alırsanız buna basın"):
                if repair_database():
                    st.success("✅ Veritabanı onarıldı!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Onarım başarısız oldu.")
            st.markdown("---")
        
        # Çıkış Butonu
        if st.button("🚪 Güvenli Çıkış"):
            st.session_state.clear()
            st.session_state.auth_mode = 'register'
            st.rerun()
        
        st.markdown("---")
        st.markdown("""
            <div style="text-align:center; font-size: 0.7rem; color: rgba(255,255,255,0.5); padding-top: 10px;">
                EĞİTİM CHECK UP v2.0<br/>
                Kişisel Eğitim & Kariyer Analiz Merkezi
            </div>
        """, unsafe_allow_html=True)
