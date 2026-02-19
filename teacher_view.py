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


# DÜZELTME: API key artık modül yüklendiğinde değil, her çağrıda okunuyor.
# Streamlit Cloud'da secrets bazen modül import sırasında henüz hazır olmayabilir.
def get_claude_client():
    """
    Claude API istemcisini başlatır.
    Öncelik: st.secrets → .env dosyası → ortam değişkeni
    """
    try:
        if "ANTHROPIC_API_KEY" in st.secrets:
            api_key = st.secrets["ANTHROPIC_API_KEY"]
        else:
            api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not api_key:
            return None
        
        from anthropic import Anthropic
        return Anthropic(api_key=api_key)
    except ImportError:
        return None
    except Exception:
        return None


# --- AI ANALİZ FONKSİYONU ---

def get_ai_analysis(prompt):
    """
    Claude API ile analiz üretir.
    Model: claude-opus-4-6
    """
    client = get_claude_client()
    if not client:
        return "⚠️ Hata: Claude API Key bulunamadı veya 'anthropic' kütüphanesi eksik. Lütfen Streamlit Secrets veya .env dosyasını kontrol edin."
    
    try:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    except Exception as e:
        err = str(e)
        if "authentication" in err.lower():
            return "⚠️ API Key hatalı veya geçersiz. Lütfen Streamlit Secrets'taki ANTHROPIC_API_KEY değerini kontrol edin."
        elif "invalid_request" in err.lower() or "model" in err.lower():
            return f"⚠️ Model hatası: {err}"
        elif "rate_limit" in err.lower():
            return "⚠️ API istek limiti aşıldı. Lütfen birkaç dakika bekleyip tekrar deneyin."
        else:
            return f"⚠️ Analiz sırasında bir hata oluştu: {err}"


# --- GRAFİK FONKSİYONU ---

def plot_scores(data_dict, title):
    """
    Test sonuçlarını görselleştirmek için akıllı Bar Grafiği oluşturur.
    DÜZELTME: Holland test sonuçları 'holland_code' string key'ini içeriyor.
              Bu key float() cast'inde ValueError'a yol açıyordu. Artık filtreleniyor.
    """
    if not data_dict or not isinstance(data_dict, dict):
        return None
    
    plot_data = {}
    
    # 1. Durum: 'categories' anahtarı varsa (Çalışma Davranışı, Sınav Kaygısı)
    if "categories" in data_dict and isinstance(data_dict["categories"], dict):
        plot_data = data_dict["categories"]
        
    # 2. Durum: 'scores' anahtarı varsa (Çoklu Zeka)
    elif "scores" in data_dict and isinstance(data_dict["scores"], dict):
        temp_data = {}
        for k, v in data_dict["scores"].items():
            if isinstance(v, dict) and "pct" in v:
                temp_data[k] = v["pct"]
            elif isinstance(v, (int, float)):
                temp_data[k] = v
        plot_data = temp_data if temp_data else data_dict["scores"]

    # 3. Durum: Düz sözlük (Sağ-Sol Beyin, VARK, Holland)
    else:
        for k, v in data_dict.items():
            # DÜZELTME: Sadece sayısal değerleri al, string key'leri atla
            # Holland'da 'holland_code' gibi string değerler crash'e yol açıyordu
            if not isinstance(v, (int, float)):
                continue
            if k in ["id", "user_id", "total", "max_total", "total_responses", "total_pct"]:
                continue
            
            # Sağ-Sol beyin: yüzde değerlerini güzel isimle göster
            if "yuzde" in k:
                label = "Sağ Beyin %" if "sag" in k else "Sol Beyin %"
                plot_data[label] = v
            elif k in ["beyin", "dominant", "level", "version"]:
                continue
            elif k in ["sag_beyin", "sol_beyin"]:
                continue  # Ham sayılar yerine yüzdeleri kullan
            else:
                plot_data[k] = v

    if not plot_data:
        return None

    # Veriyi hazırla
    labels = [str(k) for k in plot_data.keys()]
    values = []
    for v in plot_data.values():
        try:
            values.append(float(v))
        except (TypeError, ValueError):
            continue  # DÜZELTME: String değerleri sessizce atla, crash yok

    if not values or len(values) != len(labels):
        # Uzunluk eşleşmiyorsa güvenli versiyon
        valid_pairs = [(k, v) for k, v in plot_data.items() if isinstance(v, (int, float))]
        if not valid_pairs:
            return None
        labels = [str(p[0]) for p in valid_pairs]
        values = [float(p[1]) for p in valid_pairs]

    # Grafik Ayarları
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=values, y=labels, ax=ax, palette="viridis", orient='h')
    ax.set_title(f"{title}", fontsize=12, fontweight='bold')
    ax.set_xlabel("Puan / Yüzde")
    plt.tight_layout()
    return fig


# ============================================================
# PROMPT ÜRETME FONKSİYONLARI (GELİŞTİRİLMİŞ)
# ============================================================

def build_holistic_prompt(student_name, student_age, student_gender, test_data_list):
    """
    Bütüncül (harmanlanmış) analiz için geliştirilmiş prompt.
    Yenilikler:
    - Daha net rol tanımı ve beklenti yönetimi
    - Çelişki tespiti için yapılandırılmış talimat
    - Tıbbi terim yasağı ve etik sınırlar
    - Ebeveyn ve öğretmen için ayrı bölümler
    - Somut, hemen uygulanabilir öneri formatı
    """
    return f"""Sen, Türkiye'de çalışan deneyimli bir eğitim psikoloğu ve öğrenci koçusun. Psikometrik verileri sentezleyerek öğrenci hakkında bütünsel bir tablo çıkarıyorsun.

---

## 📋 ÖĞRENCİ BİLGİLERİ
- **İsim:** {student_name}
- **Yaş:** {student_age}
- **Cinsiyet:** {student_gender}

## 📊 TEST VERİLERİ (JSON)
```json
{json.dumps(test_data_list, ensure_ascii=False, indent=2)}
```

---

## 🛑 ZORUNLU KURALLAR

1. **VERİ BAĞLILIĞI:** Yalnızca JSON içindeki somut puanlara dayanan yorumlar yap. Her iddiayı veriyle destekle.
2. **SENTEZ ODAKLI:** Testleri tek tek özetleme — testler ARASI ilişkileri ve örüntüleri analiz et.
3. **ÇELİŞKİ TESPİTİ:** Öğrencinin güçlü yönleri ile zayıf yönleri çelişiyorsa (örn. yüksek zeka + yüksek kaygı) bunu açıkça işaretle.
4. **TIBBİ TANI YASAĞI:** "DEHB", "depresyon", "anksiyete bozukluğu", "disleksi" gibi klinik tanı terimleri kesinlikle kullanma.
5. **YAŞA UYGUNLUK:** {student_age} yaşındaki bir öğrenci için gerçekçi ve uygulanabilir tavsiyeler ver.
6. **NEDEN-SONUÇ BAĞLANTISI:** "Ders çalışamıyor" gibi sonuç ifadeleri değil, "VARK Kinestetik skoru yüksek olduğu için masa başında uzun süre odaklanmakta güçlük çekiyor" gibi veri destekli nedenler kullan.

---

## 📝 RAPOR FORMATI (Bu formatı değiştirme)

# 🚀 BÜYÜK RESİM: {student_name} Kimdir?

*(2-3 cümlelik güçlü giriş: Tüm testlerin ortak paydasını, öğrencinin en belirgin karakteristiğini anlat. Bir cümleyle öğrencinin "öğrenme imzasını" tanımla.)*

---

# 🧩 ZİHİNSEL SENTEZ

### Potansiyel ↔ Performans Dengesi
*(Zeka/yetenek puanları ile çalışma davranışı/kaygı skorları arasındaki ilişki. Potansiyel kullanılıyor mu?)*

### Öğrenme DNA'sı
*(Sağ/Sol Beyin + VARK sonuçlarını birleştir. "Bu öğrenci en iyi nasıl öğreniyor?" sorusunu cevapla.)*

### İlgi ↔ Yetenek Uyumu
*(Holland RIASEC kodu ile Çoklu Zeka güçlü yönleri örtüşüyor mu? Meslek yönelimi netleşiyor mu?)*

---

# ⚖️ DENGE TABLOSU

| 💪 Kanıtlanmış Güç (Test + Puan) | 🚧 Kritik Engel (Test + Puan) | 🎯 Çözüm Stratejisi |
|----------------------------------|-------------------------------|---------------------|
| Örn: Müzik Zekası (Çoklu Zeka %82) | Sınav Kaygısı Zihinsel (%70) | Müzik ile ezber, nefes teknikleri |
| ... | ... | ... |

*(En az 3 satır doldur. Puan olmadan güç veya engel yazma.)*

---

# 🗺️ STRATEJİK YOL HARİTASI

### 🎓 Akademik Başarı İçin (Bu Haftadan İtibaren Uygulanabilir)
- **[Çalışma Ortamı]:** ... *(VARK ve Sağ/Sol Beyin verilerine özel)*
- **[Zaman Planlaması]:** ... *(Çalışma Davranışı verilerine özel)*
- **[Sınav Hazırlığı]:** ... *(Sınav Kaygısı verilerine özel)*

### 🧠 Duygusal ve Sosyal Gelişim
- ... *(Kaygı skoru yüksekse mutlaka rahatlama tekniği öner)*

### 👨‍👩‍👦 Ebeveyn Rehberi
> *(Aileye yönelik, suçlamayan, motive edici, somut 2-3 madde. "Yapın / Yapmayın" formatında.)*

### 👩‍🏫 Öğretmen Notu
> *(Sınıf ortamında dikkat edilmesi gerekenler. Öğretmenin yapabileceği 1-2 somut adım.)*

---

*Dil: Türkçe. Üslup: Profesyonel, sıcak, yapıcı. Öğrenciyi yargılama, güçlendirmeye odaklan.*"""


def build_single_test_prompt(student_name, student_age, student_gender, test_name, test_data):
    """
    Tekil test analizi için geliştirilmiş prompt.
    Yenilikler:
    - Test türüne özel yorum çerçevesi
    - ASCII bar grafik zorunluluğu (sayısal netlik)
    - Puan aralıkları için standart yorumlama kriterleri
    - Pratik tavsiye formatı (hemen uygulanabilir)
    """
    return f"""Sen, Türkiye'de çalışan deneyimli bir eğitim psikoloğusun. Tek bir psikolojik test sonucunu derinlemesine analiz ediyorsun.

---

## 📋 ÖĞRENCİ BİLGİLERİ
- **İsim:** {student_name}
- **Yaş:** {student_age}
- **Cinsiyet:** {student_gender}
- **Analiz Edilen Test:** {test_name}

## 📊 TEST VERİSİ (JSON)
```json
{json.dumps(test_data, ensure_ascii=False, indent=2)}
```

---

## 🛑 ZORUNLU KURALLAR

1. **SADECE VERİ:** JSON içinde görmediğin hiçbir puan veya özellik hakkında yorum yapma.
2. **KANIT ZORUNLU:** Güçlü/zayıf yön belirtirken parantez içinde puanı yaz. Örn: "Görsel zeka güçlü (pct: 78)"
3. **PUAN YORUMLAMA STANDARDI:**
   - %0-30 → "Gelişime çok açık"
   - %31-50 → "Ortalama altı, geliştirilebilir"
   - %51-70 → "Ortalama / dengeli"
   - %71-85 → "Güçlü"
   - %86-100 → "Çok güçlü / baskın"
4. **TIBBİ TANI YASAĞI:** Klinik tanı terimleri (DEHB, depresyon, disleksi vb.) kesinlikle kullanma.
5. **YAŞA UYGUN TAVSİYE:** {student_age} yaşındaki bir öğrenci için gerçekçi öneriler ver.
6. **TEST BAĞLAMINA SADIK KAL:** Sadece bu testin ölçtüğü alanı yorumla, dışına çıkma.

## 🔍 TEST TÜRÜNE ÖZEL YORUM ÇERÇEVESİ
- **Sağ/Sol Beyin:** Sağ yüksekse (Yaratıcı, Görsel, Sezgisel, Bütüncül), Sol yüksekse (Mantıksal, Analitik, Sıralı, Planlı)
- **Çoklu Zeka:** En yüksek 3 puan = "Süper Güç", en düşük 2 puan = "Keşfedilmeyi Bekliyor"
- **VARK:** Baskın stil = Ders çalışma yöntemi tavsiyesi odağı
- **Holland RIASEC:** En yüksek 3 harf kodu = Meslek yönelimi ve eğitim tercihleri
- **Sınav Kaygısı:** Alt boyutlarda yüksek puan (>%60) = O alana özel teknik öner
- **Çalışma Davranışı:** Kategorilere göre spesifik çalışma alışkanlığı tavsiyeleri

---

## 📝 RAPOR FORMATI (Bu formatı değiştirme)

### 1. 📊 TEST ÖZETİ

**Tek Cümle Sonuç:** *(Testin en önemli bulgusu, net ve doğrudan.)*

**Görsel Özet:**
```
[Kategori / Boyut Adı] : ████████░░ XX%
[Kategori / Boyut Adı] : ██████░░░░ XX%
[Kategori / Boyut Adı] : ████░░░░░░ XX%
```
*(Tüm kategorileri ekle, puanlara göre doldurulan bar uzunluklarını ayarla.)*

---

### 2. 🧠 DERİN YORUM

*(Bu kısımda "NEDEN?" sorusuna cevap ver. Puanların günlük hayata etkisini somut örneklerle açıkla.
Bir metafor veya analoji kullan — karmaşık psikolojik kavramı sıradan dile çevir.
2-3 paragraf, akıcı anlatım.)*

---

### 3. 💪 KANITA DAYALI GÜÇLÜ YÖNLER

| # | Güçlü Yön | Kanıt (Puan) | Günlük Yansıması |
|---|-----------|--------------|-----------------|
| 1 | ... | ... | ... |
| 2 | ... | ... | ... |
| 3 | ... | ... | ... |

*(Puan yoksa tabloya ekleme.)*

---

### 4. 🌱 GELİŞİM FIRSATLARI

| # | Alan | Mevcut Durum | Nasıl Geliştirilir? |
|---|------|--------------|---------------------|
| 1 | ... | ... | ... |
| 2 | ... | ... | ... |

---

### 5. 🎯 HEMEN UYGULANABİLİR TAVSİYELER

*(Bu teste özgü, {student_age} yaşına uygun, bu haftadan itibaren başlanabilecek 3 somut eylem.)*

**📌 TAVSİYE 1:** [Başlık]
→ *(Adım adım ne yapılacak, ne zaman, nasıl)*

**📌 TAVSİYE 2:** [Başlık]
→ *(Adım adım ne yapılacak, ne zaman, nasıl)*

**📌 TAVSİYE 3:** [Başlık]
→ *(Adım adım ne yapılacak, ne zaman, nasıl)*

---

*Dil: Türkçe. Üslup: Profesyonel, içten, yapıcı.*"""


# ============================================================
# ANA ÖĞRETMEN UYGULAMASI
# ============================================================

def app():
    # --- CSS ---
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
            st.error("DİKKAT: Bu işlem tüm veritabanını kalıcı olarak siler!")
            
            # DÜZELTME: Çift onay mekanizması — tek tıkla silme engellendi
            confirm_reset = st.checkbox("Evet, tüm verilerin silineceğini anlıyorum")
            if confirm_reset:
                if st.button("TÜM SİSTEMİ SIFIRLA", type="primary"):
                    if reset_database():
                        st.success("Sistem tamamen sıfırlandı.")
                        time.sleep(1)
                        st.rerun()
            else:
                st.info("Devam etmek için onay kutucuğunu işaretleyin.")

    # --- ANA EKRAN ---
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

    # Seçilen öğrenci verilerini bul
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
        # DÜZELTME: Şifre artık ekranda gösterilmiyor
        c3.write("🔒 Şifre korumalı")
        c3.caption("Güvenlik")
        c4.metric("Toplam Giriş", info.login_count)
        c4.caption("Aktiflik Durumu")
    
    st.divider()

    # ============================================================
    # 3. TAMAMLANAN TESTLER VE OTOMATİK SONUÇLAR
    # ============================================================
    st.subheader("📝 Tamamlanan Testler ve Otomatik Sonuçlar")
    st.info("Burada öğrencinin bitirdiği testlerin **anlık sistem raporlarını** (yapay zekasız) görebilirsiniz.")
    
    if not tests:
        st.warning("⚠️ Bu öğrenci henüz hiç test çözmemiş.")
    else:
        for idx, t in enumerate(tests):
            btn_label = f"✅ {t['test_name']} (Tarih: {t['date']})"
            
            with st.expander(btn_label):
                if t['scores']:
                    fig = plot_scores(t['scores'], t['test_name'])
                    if fig:
                        st.pyplot(fig)
                
                st.markdown("### 📄 Sistem Raporu")
                if t.get('report'):
                    st.markdown(t['report'])
                else:
                    st.warning("Bu test için otomatik rapor metni bulunamadı.")
                    st.write("Ham Cevaplar:", t['raw_answers'])

    st.divider()

    # ============================================================
    # 4. KAYITLI AI RAPOR ARŞİVİ
    # ============================================================
    st.subheader("📂 Kayıtlı Yapay Zeka (AI) Rapor Arşivi")
    st.info("Burada daha önce **Claude Opus** kullanarak oluşturduğunuz detaylı ve bütüncül analizleri bulabilirsiniz.")
    
    history = get_student_analysis_history(info.id)
    
    if not history:
        st.info("Bu öğrenci için henüz oluşturulmuş AI destekli bir analiz raporu bulunmamaktadır.")
    else:
        st.markdown(f"**{len(history)} adet** kayıtlı rapor bulundu.")
        
        for idx, record in enumerate(history):
            btn_label = f"🤖 AI Raporu {idx+1}: {record['combination']} ({record['date']})"
            
            with st.expander(btn_label):
                st.markdown(f"<div class='report-header'>ANALİZ KAPSAMI: {record['combination']}</div>", unsafe_allow_html=True)
                
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
                    file_name=f"{info.name}_AI_Rapor_{idx+1}.txt",
                    mime="text/plain",
                    key=f"dl_{idx}"
                )

    st.divider()

    # ============================================================
    # 5. YENİ AI ANALİZİ OLUŞTURMA
    # ============================================================
    st.subheader("⚡ Yeni AI Analizi Oluştur")
    
    if not tests:
        st.write("Analiz yapılacak veri yok.")
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
            
            if st.button("🚀 ANALİZİ BAŞLAT (Claude Opus)", type="primary"):
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
                # MOD 1: BÜTÜNCÜL ANALİZ
                # ====================================================
                if analysis_mode == "BÜTÜNCÜL (Harmanlanmış) Rapor":
                    
                    st.info(f"⏳ Claude Opus, seçilen **{len(selected_tests)} testi** derinlemesine harmanlıyor. Lütfen bekleyin...")
                    
                    with st.spinner("Stratejik analiz hazırlanıyor..."):
                        # Test verilerini prompt için hazırla
                        ai_input = []
                        for t in analyzed_data:
                            # Ham cevapları güvenli şekilde parse et
                            raw = t.get("raw_answers", "")
                            if isinstance(raw, str):
                                try:
                                    raw = json.loads(raw)
                                except (json.JSONDecodeError, ValueError):
                                    raw = raw  # parse edilemezse string olarak bırak
                            
                            ai_input.append({
                                "TEST_ADI": t["test_name"],
                                "TARİH": str(t["date"]),
                                "SONUÇLAR": t["scores"] if t["scores"] else raw
                            })
                        
                        # GELİŞTİRİLMİŞ PROMPT
                        prompt = build_holistic_prompt(
                            student_name=info.name,
                            student_age=info.age,
                            student_gender=info.gender,
                            test_data_list=ai_input
                        )
                        
                        final_report = get_ai_analysis(prompt)
                        save_holistic_analysis(info.id, selected_tests, final_report)
                        
                        st.success("✅ Bütüncül analiz tamamlandı ve arşive kaydedildi.")
                        time.sleep(1.5)
                        st.rerun()

                # ====================================================
                # MOD 2: AYRI AYRI TEKİL ANALİZLER
                # ====================================================
                else:
                    progress_text = "Testler sırayla analiz ediliyor..."
                    my_bar = st.progress(0, text=progress_text)
                    total_ops = len(analyzed_data)
                    
                    for idx, t in enumerate(analyzed_data):
                        test_name = t["test_name"]
                        my_bar.progress(
                            (idx + 1) / total_ops,
                            text=f"**{test_name}** analiz ediliyor... ({idx+1}/{total_ops})"
                        )
                        
                        # Ham cevapları güvenli şekilde parse et
                        raw = t.get("raw_answers", "")
                        if isinstance(raw, str):
                            try:
                                raw = json.loads(raw)
                            except (json.JSONDecodeError, ValueError):
                                raw = raw
                        
                        test_data_for_prompt = {
                            "TEST_ADI": test_name,
                            "TARİH": str(t["date"]),
                            "SONUÇLAR": t["scores"] if t["scores"] else raw
                        }
                        
                        # GELİŞTİRİLMİŞ PROMPT
                        prompt = build_single_test_prompt(
                            student_name=info.name,
                            student_age=info.age,
                            student_gender=info.gender,
                            test_name=test_name,
                            test_data=test_data_for_prompt
                        )
                        
                        single_report = get_ai_analysis(prompt)
                        save_holistic_analysis(info.id, [test_name], single_report)
                    
                    my_bar.empty()
                    st.success(f"✅ {total_ops} test başarıyla detaylı analiz edildi ve Arşiv'e eklendi.")
                    time.sleep(2)
                    st.rerun()

    # 6. HAM VERİ LİSTESİ
    st.divider()
    with st.expander("🗂️ Ham Veri Listesi"):
        if tests:
            df_tests = pd.DataFrame(tests)
            df_tests['date'] = pd.to_datetime(df_tests['date']).dt.strftime('%d.%m.%Y')
            st.dataframe(df_tests[["test_name", "date"]], use_container_width=True)
