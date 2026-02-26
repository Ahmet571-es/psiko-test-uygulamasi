import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os
from dotenv import load_dotenv
from db_utils import (
    get_all_students_with_results, reset_database,
    delete_specific_students, save_holistic_analysis,
    get_student_analysis_history
)

# --- API AYARLARI ---
load_dotenv()


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
    """Claude API ile analiz üretir."""
    client = get_claude_client()
    if not client:
        return "⚠️ Hata: Claude API Key bulunamadı veya 'anthropic' kütüphanesi eksik. Lütfen Streamlit Secrets veya .env dosyasını kontrol edin."

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=16000,
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
    """Test sonuçlarını görselleştirmek için Bar Grafiği oluşturur."""
    if not data_dict or not isinstance(data_dict, dict):
        return None

    plot_data = {}

    # 1. Durum: 'categories' anahtarı varsa (Çalışma Davranışı, Sınav Kaygısı)
    if "categories" in data_dict and isinstance(data_dict["categories"], dict):
        plot_data = data_dict["categories"]

    # 1b. Durum: D2 Dikkat Testi
    elif "CP" in data_dict and "TN_E" in data_dict:
        d2_labels = {
            "CP": "Konsantrasyon (CP)",
            "TN_E": "Toplam Performans (TN-E)",
            "TN": "Toplam İşaretleme (TN)",
            "E1": "Atlama Hatası (E1)",
            "E2": "Yanlış İşaretleme (E2)",
            "FR": "Dalgalanma (FR)",
        }
        for key, label in d2_labels.items():
            if key in data_dict and isinstance(data_dict[key], (int, float)):
                plot_data[label] = data_dict[key]

    # 1c. Durum: Akademik Analiz Testi
    elif "overall" in data_dict and "performance_avg" in data_dict:
        akd_keys = {
            "overall": "Genel Skor",
            "Anlama": "Okuma Anlama",
            "Muhakeme": "Matematiksel Muhakeme",
            "Düşünme": "Mantıksal Düşünme",
            "Öz-Değerlendirme": "Öz-Değerlendirme",
        }
        for key, label in akd_keys.items():
            if key in data_dict and isinstance(data_dict[key], (int, float)):
                plot_data[label] = data_dict[key]

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
            if not isinstance(v, (int, float)):
                continue
            if k in ["id", "user_id", "total", "max_total", "total_responses", "total_pct"]:
                continue
            if "yuzde" in k:
                label = "Sağ Beyin %" if "sag" in k else "Sol Beyin %"
                plot_data[label] = v
            elif k in ["beyin", "dominant", "level", "version"]:
                continue
            elif k in ["sag_beyin", "sol_beyin"]:
                continue
            else:
                plot_data[k] = v

    if not plot_data:
        return None

    # Veriyi hazırla
    valid_pairs = [(str(k), float(v)) for k, v in plot_data.items() if isinstance(v, (int, float))]
    if not valid_pairs:
        return None

    labels = [p[0] for p in valid_pairs]
    values = [p[1] for p in valid_pairs]

    # Grafik Ayarları
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(8, max(3, len(labels) * 0.5)))

    # Renk paleti — logo uyumlu
    colors = sns.color_palette("coolwarm", len(labels))
    sns.barplot(x=values, y=labels, ax=ax, palette=colors, orient='h')

    ax.set_title(f"{title}", fontsize=12, fontweight='bold', color='#1B2A4A')
    ax.set_xlabel("Puan / Yüzde", fontsize=10)
    ax.tick_params(axis='y', labelsize=9)
    plt.tight_layout()
    return fig


# ============================================================
# PROMPT ÜRETME FONKSİYONLARI — TİCARİ KALİTE v3.0
# ============================================================

def build_holistic_prompt(student_name, student_age, student_gender, test_data_list):
    """Bütüncül (harmanlanmış) analiz için ticari kalite prompt."""
    return f"""# ROL ve KİMLİK

Sen, Türkiye'nin önde gelen eğitim psikolojisi merkezlerinde 20 yıl deneyim kazanmış, psikometrik değerlendirme, kariyer danışmanlığı ve gelişim psikolojisi alanlarında uzmanlaşmış bir Klinik Eğitim Psikoloğusun. 

Uzmanlık alanların:
- Psikometrik test bataryası yorumlama ve çapraz korelasyon analizi
- Ergen gelişim psikolojisi ve yaşa özgü değerlendirme
- Kariyer psikolojisi ve mesleki yönlendirme
- Aile danışmanlığı ve ebeveyn rehberliği
- Öğrenme farklılıkları ve bireyselleştirilmiş eğitim planlaması

Bu rapor, ücretli bir profesyonel danışmanlık hizmetinin çıktısıdır. Aile, öğretmen ve rehber öğretmenler tarafından okunacak resmi bir analiz belgesidir. Raporun, yüz yüze bir psikolog görüşmesinin yazılı karşılığı kadar derinlikli, kişiselleştirilmiş ve uygulanabilir olmalıdır.

---

# ÖĞRENCİ DOSYASI

| Alan | Bilgi |
|------|-------|
| İsim | {student_name} |
| Yaş | {student_age} |
| Cinsiyet | {student_gender} |
| Değerlendirme Türü | Bütüncül Çoklu Test Analizi |

## TEST VERİLERİ (JSON)
```json
{json.dumps(test_data_list, ensure_ascii=False, indent=2)}
```

---

# KRİTİK KURALLAR

1. **KANITSAL ZORUNLULUK:** Her yorum, iddia ve tespit mutlaka parantez içinde kaynak test adı ve sayısal puan ile desteklenmeli. Örn: "Görsel-uzamsal zeka alanında belirgin güç göstermektedir (Çoklu Zeka: %82)." Kanıtsız hiçbir yorum yapma.

2. **SENTEZ MERKEZLİ:** Testleri ayrı ayrı özetleme. Asıl değer, testler arasındaki BAĞLANTILARDA, KORELASYONLARDA ve ÇELİŞKİLERDE yatıyor. Her paragrafta en az 2 farklı testten veri çaprazla.

3. **GELİŞİMSEL BAĞLAM:** {student_age} yaşındaki bir bireyin gelişimsel dönem özelliklerini (bilişsel, duygusal, sosyal, kimlik gelişimi) göz önünde bulundurarak yorumla. Yaşa özgü beklentileri ve normları referans al.

4. **TIBBİ TANI YASAĞI:** "DEHB", "depresyon", "anksiyete bozukluğu", "otizm spektrumu", "disleksi" gibi klinik tanı terimleri kesinlikle kullanma. Bunun yerine davranışsal betimleme yap.

5. **BİREYSELLEŞTİRME:** Genel geçer tavsiyeler verme. Her öneri, bu öğrencinin spesifik veri profilinden türetilmiş olmalı. "Daha çok çalış" yerine "VARK Kinestetik baskınlığın (%X) göz önüne alındığında, Matematik çalışırken manipülatif materyaller (geometri blokları, kağıt katlama) kullanman, masa başı süresini 25 dakikalık bloklara bölmen önerilir."

6. **PUAN YORUMLAMA ÇERÇEVESİ:**
   - %0-20 → Belirgin gelişim alanı — acil destek önerilir
   - %21-40 → Ortalamanın altı — hedefli çalışma gerektirir
   - %41-60 → Ortalama düzey — potansiyel mevcut, strateji ile yükseltilebilir
   - %61-80 → Güçlü alan — sürdürülebilir ve derinleştirilebilir
   - %81-100 → Çok güçlü / baskın alan — yetenek göstergesi, ileri düzey destekle parlayabilir

7. **UZUNLUK ve DERİNLİK:** Bu rapor minimum 3000 kelime olmalıdır. Her bölüm, ödenen ücrete değecek derinlikte olmalı. Yüzeysel veya şablonik ifadelerden kaçın. Her öğrenci için rapor benzersiz ve kişiselleştirilmiş olmalı.

---

# TESTE ÖZEL ÇAPRAZ ANALİZ REHBERİ

Verideki test kombinasyonlarına göre aşağıdaki çapraz analizleri MUTLAKA yap:

## Enneagram Verisi Varsa:
- Ana tipin motivasyon yapısını diğer tüm test sonuçlarıyla çapraz kontrol et
- Kanat (wing) etkisinin öğrenme stili üzerindeki yansımasını VARK/Beyin dominansı ile doğrula
- Stres yönündeki tipin puanını Sınav Kaygısı verileriyle karşılaştır (stres tipi yüksekse kaygı da yüksek mi?)
- Büyüme yönündeki tipin puanını akademik güçlü alanlarla eşleştir
- Tritype analizi (Kafa 5-6-7 / Kalp 2-3-4 / Karın 8-9-1 merkezlerinden en yüksek puan) yap ve bütünsel kişilik portresini çiz
- Kişilik tipi ile Holland RIASEC kodu arasındaki uyumu/uyumsuzluğu tartış (Örn: Tip 5 + Araştırmacı(I) = uyumlu; Tip 5 + Girişimci(E) = çelişki)

## Sınav Kaygısı + Çalışma Davranışı Birlikte Varsa:
- Kaygı-performans döngüsünü analiz et: yetersiz çalışma → kaygı mı, yoksa kaygı → çalışamama mı?
- Hangi kaygı alt boyutu hangi çalışma davranışı kategorisiyle ilişkili?
- Bu döngüyü kırmak için somut müdahale noktasını tespit et

## VARK + Sağ-Sol Beyin Birlikte Varsa:
- "Nörobilişsel Öğrenme Profili" oluştur: beyin yarım küre baskınlığı + duyusal kanal tercihi
- Bu kombinasyonun sınıf ortamındaki optimal öğrenme koşullarını tanımla
- Ders bazlı (Matematik, Fen, Türkçe, Sosyal, Yabancı Dil) öğrenme stratejileri tablosu oluştur

## Çoklu Zeka + Holland RIASEC Birlikte Varsa:
- Zeka profili ile mesleki ilgi alanlarının örtüşme haritasını çıkar
- Uyumlu alanlar: doğal kariyer yönelimleri
- Uyumsuz alanlar: keşfedilmemiş potansiyel mi, yoksa yüzeysel ilgi mi?
- Top 10 kariyer önerisi (zeka + ilgi + kişilik üçgeninden)

---

# RAPOR FORMATI (HER BÖLÜMÜ AYNEN DOLDUR, HİÇBİR BÖLÜMÜ ATLAMA)

---

# 📋 YÖNETİCİ ÖZETİ

*(Bu bölüm, raporu okuyacak kişinin ilk 2 dakikada tüm tabloyu görmesini sağlar. 5-6 cümle ile öğrencinin en kritik güçlü yönü, en acil gelişim alanı, en dikkat çekici çelişki ve en öncelikli adım özetlenir.)*

---

# 🧬 1. KİŞİLİK ve MOTİVASYON PROFİLİ

## 1.1 Kim Bu Öğrenci?
*(Öğrenciyi hiç tanımayan birinin okuduğunda zihninde net bir portre oluşturacağı, 2-3 paragraflık derinlikli giriş. Tüm test verilerinden sentezlenmiş bir "karakter taslağı". Öğrencinin tipik bir gününü, sınıf davranışını, arkadaş ilişkilerini ve motivasyon kaynaklarını betimle.)*

## 1.2 Temel Motivasyon Dinamikleri
*(Bu öğrenci neyin peşinde koşuyor? Neyden kaçınıyor? Ne zaman en verimli? Ne zaman engellenmiş hissediyor? Enneagram + diğer test verileriyle desteklenmiş derinlikli motivasyon analizi. Minimum 2 paragraf.)*

## 1.3 Stres Tepki Profili
*(Bu öğrenci baskı altında nasıl tepki verir? Hangi durumlar tetikleyici? Kaçınma mı gösterir, aşırı çalışma mı, içe kapanma mı? Enneagram stres yönü + Sınav Kaygısı verileriyle destekle. Minimum 2 paragraf.)*

## 1.4 Sosyal ve Duygusal Harita
*(Akran ilişkileri, grup içi rolü, otorite figürleriyle ilişkisi, empati kapasitesi, çatışma yönetimi tarzı. Kişilik profili + sosyal/kişilerarası zeka verilerinden çıkarım. Minimum 2 paragraf.)*

---

# 🧠 2. BİLİŞSEL ve AKADEMİK PROFİL

## 2.1 Nörobilişsel Öğrenme Kimliği
*(Sağ/Sol Beyin dominansı + VARK öğrenme stili sentezi. Bu öğrencinin beyninin bilgiyi nasıl aldığını, işlediğini ve depoladığını açıkla. "Bu öğrenci bilgiyi önce GÖRÜR, sonra İŞLER, sonra HAREKET ile pekiştirir" gibi somut bir öğrenme akışı tanımla. Minimum 2 paragraf.)*

## 2.2 Zeka Profili Haritası
*(Çoklu Zeka verilerini detaylı yorumla. Profil tipi: uzmanlaşmış mı (1-2 zirve), çok yönlü mü (3-4 yüksek), dengeli mi? En güçlü 3 zekanın sinerjisini açıkla. En zayıf alanların akademik etkisini tartış. Minimum 2 paragraf.)*

## 2.3 Potansiyel ↔ Performans Dengesi
*(Zeka ve yetenek puanları ile çalışma davranışı ve kaygı skorları arasındaki boşluğu analiz et. Bu öğrenci potansiyelinin yüzde kaçını kullanıyor? Potansiyel kaybının nedenleri neler? Her iddia puanla kanıtlanmalı. Minimum 3 paragraf.)*

## 2.4 Çalışma Davranışı Derinlikli Analiz
*(Varsa: 7 alt kategorinin (A-G) her birini ayrı ayrı yorumla, birbirleriyle ilişkilendir. Motivasyon yüksek ama zaman yönetimi düşükse → neden? Not alma güçlü ama sınava hazırlık zayıfsa → neden? Minimum 2 paragraf.)*

---

# ⚡ 3. ÇELİŞKİ ve PARADOKS ANALİZİ

*(Bu bölüm raporun en değerli kısmıdır. Veriler arasındaki ÇELİŞKİLERİ, UYUMSUZLUKLARI ve PARADOKSLARI tespit et. Her çelişki için 3 katmanlı analiz yap:)*

| # | Çelişki Tanımı | Test 1 (Puan) | Test 2 (Puan) | Olası Açıklama | Müdahale Önerisi |
|---|---------------|---------------|---------------|----------------|-----------------|
| 1 | ... | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... | ... |
| 4 | ... | ... | ... | ... | ... |

*(Minimum 4 çelişki bul. Her biri için ayrıntılı paragraf açıklaması yaz.)*

---

# 📊 4. KAPSAMLI DEĞERLENDIRME MATRİSİ

## 4.1 Güç Envanteri

| # | Güçlü Alan | Kaynak Test | Puan | Akademik Yansıma | Sosyal Yansıma | Kariyer Potansiyeli |
|---|-----------|-------------|------|-------------------|----------------|-------------------|
| 1 | ... | ... | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... | ... | ... |
| 4 | ... | ... | ... | ... | ... | ... |
| 5 | ... | ... | ... | ... | ... | ... |

*(Minimum 5 güçlü alan. Her biri farklı testlerden veya çapraz korelasyonlardan gelmeli.)*

## 4.2 Gelişim Alanları Analizi

| # | Gelişim Alanı | Kaynak Test | Puan | Risk Düzeyi | Neden Önemli? | Somut Müdahale Stratejisi |
|---|-------------|-------------|------|-------------|---------------|--------------------------|
| 1 | ... | ... | ... | 🔴/🟡 | ... | ... |
| 2 | ... | ... | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... | ... | ... |
| 4 | ... | ... | ... | ... | ... | ... |

*(Minimum 4 gelişim alanı.)*

## 4.3 Kritik Göstergeler Paneli

### 🟢 Güçlü Düzey — Sürdürülmesi Gereken Alanlar
*(Puanlarla listele. Neden sürdürülmeli, nasıl daha ileri taşınabilir?)*

### 🟡 Takip Gerektiren — Potansiyel Risk Alanları
*(Puanlarla listele. Şu an kritik değil ama ihmal edilirse ne olur?)*

### 🔴 Acil İlgi — Öncelikli Müdahale Alanları
*(Puanlarla listele. Neden acil? Müdahale edilmezse 6 ay sonra ne olur?)*

---

# 🗺️ 5. STRATEJİK YOL HARİTASI

## 5.1 Akademik Başarı Planı

### 📐 Ders Bazlı Öğrenme Stratejileri

| Ders | Öğrenme Stili Uyumu | Önerilen Yöntem | Araç/Materyal | Günlük Süre |
|------|---------------------|-----------------|---------------|-------------|
| Matematik | ... | ... | ... | ... dk |
| Fen Bilimleri | ... | ... | ... | ... dk |
| Türkçe/Edebiyat | ... | ... | ... | ... dk |
| Sosyal Bilimler | ... | ... | ... | ... dk |
| Yabancı Dil | ... | ... | ... | ... dk |

*(Her dersin stratejisi VARK stili + Beyin dominansı + Çoklu Zeka profilinden türetilmeli.)*

### 📅 Haftalık Çalışma Programı Taslağı
*(Öğrencinin veri profiline özel — kaygı yüksekse kısa bloklar, motivasyon yüksekse yoğun periyotlar, kinestetik baskınsa hareket araları vb. Gün gün, saat saat örnek program.)*

### 📝 Sınav Hazırlık Protokolü
*(Sınav Kaygısı alt boyutlarına özel:)*
- **Sınavdan 1 hafta önce:** ...
- **Sınavdan 1 gün önce:** ...
- **Sınav sabahı:** ...
- **Sınav anında:** ...
- **Sınav sonrasında:** ...

## 5.2 Kişisel Gelişim Planı

### Duygusal Düzenleme Stratejileri
*(Kişilik tipi ve kaygı profiline özel. Genel "nefes al" tavsiyesi değil; bu öğrencinin spesifik stres tetikleyicilerine yönelik somut teknikler.)*

### Sosyal Beceri Geliştirme
*(Kişilik profiline göre: çok sosyalse sınır koyma, içe dönükse güvenli ortam stratejileri, çatışmacıysa empati geliştirme vb.)*

### Motivasyon ve Hedef Yönetimi
*(Kişilik tipinin motivasyon kaynaklarına uygun hedef koyma ve takip sistemi. Somut araçlar öner.)*

## 5.3 Kariyer Ön Değerlendirme Raporu

### Kariyer Yönelim Üçgeni
*(Holland RIASEC + Çoklu Zeka + Kişilik profili sentezi)*

**3 Harfli Holland Kodu Analizi:** *(Kodun ne anlama geldiği, hangi iş ortamlarında mutlu olacağı)*

**Kariyer Haritası:**

| # | Meslek / Alan | RIASEC Uyumu | Zeka Uyumu | Kişilik Uyumu | Uyum Skoru |
|---|-------------|-------------|------------|---------------|-----------|
| 1 | ... | ... | ... | ... | ⭐⭐⭐⭐⭐ |
| 2 | ... | ... | ... | ... | ⭐⭐⭐⭐⭐ |
| 3 | ... | ... | ... | ... | ⭐⭐⭐⭐ |
| 4 | ... | ... | ... | ... | ⭐⭐⭐⭐ |
| 5 | ... | ... | ... | ... | ⭐⭐⭐⭐ |
| 6 | ... | ... | ... | ... | ⭐⭐⭐ |
| 7 | ... | ... | ... | ... | ⭐⭐⭐ |
| 8 | ... | ... | ... | ... | ⭐⭐⭐ |
| 9 | ... | ... | ... | ... | ⭐⭐ |
| 10 | ... | ... | ... | ... | ⭐⭐ |

**Lise Alan Seçimi Tavsiyesi:** *(Sayısal / Eşit Ağırlık / Sözel / Dil — gerekçesiyle)*

**Üniversite Bölüm Önerileri:** *(En uygun 5 bölüm ve neden)*

**Kariyer Keşif Adımları:** *(Staj, gönüllülük, iş gölgeleme, kulüp, online kurs önerileri)*

⚠️ *Not: Bu değerlendirme bir kesin yönlendirme değil, veri destekli ön analizdir. Kesin kararlar profesyonel kariyer danışmanlığı ile desteklenmelidir.*

---

# 👨‍👩‍👦 6. AİLE DANIŞMANLIK REHBERİ

## Bu Çocuğu Anlamak

*(Ebeveynin çocuğunu daha iyi anlamasını sağlayacak, teknik terim kullanmadan yazılmış 2-3 paragraf. "Çocuğunuz şu tip bir insan..." tonunda, sıcak ve açıklayıcı.)*

## ✅ EVDEKİ DESTEK STRATEJİLERİ (Yapınız)

1. ... *(Kişilik tipine özel — neden bu yaklaşım?)*
2. ... *(Öğrenme stiline özel — somut örnek)*
3. ... *(Kaygı profiline özel — sınav döneminde nasıl davranılmalı?)*
4. ... *(Motivasyon yapısına özel — ödül/ceza dengesi)*
5. ... *(Sosyal gelişim için — arkadaşlık, aktivite önerileri)*

## ❌ KAÇINILMASI GEREKEN YAKLAŞIMLAR (Yapmayınız)

1. ... *(Kişilik tipine göre hangi baskı türü zarar verir?)*
2. ... *(Bu çocukla hangi iletişim tarzı ters etki yapar?)*
3. ... *(Hangi karşılaştırmalar motivasyonu öldürür?)*
4. ... *(Hangi beklentiler gerçekçi değil?)*

## 🗣️ EBEVEYN İLETİŞİM REHBERİ

*(Bu kişilik tipindeki bir çocukla konuşurken kullanılabilecek örnek cümleler:)*
- Başarı durumunda: "..."
- Başarısızlık durumunda: "..."
- Motivasyon düştüğünde: "..."
- Çatışma anında: "..."

---

# 👩‍🏫 7. ÖĞRETMEN VE REHBER ÖĞRETMEN REHBERİ

## Sınıf İçi Stratejiler
*(Bu öğrenci için sınıf ortamında yapılabilecek 5 somut adım. Her biri öğrenme stili ve kişilik verisine dayalı.)*

## İletişim Rehberi
*(Bu öğrenciyle en etkili iletişim tarzı. Hangi geri bildirim yöntemi işe yarar? Hangi yaklaşımlardan kaçınılmalı?)*

## Erken Uyarı İşaretleri
*(Dikkat edilmesi gereken davranış değişiklikleri — bu profildeki bir öğrencide hangi işaretler stres/tükenmişlik göstergesi olabilir?)*

## Rehber Öğretmen İçin Not
*(Bireysel görüşmelerde odaklanılması gereken temalar, izlenmesi gereken gelişim alanları)*

---

# 📌 8. SONUÇ ve ÖNCELİK MATRİSİ

## Eylem Öncelik Sıralaması

| Öncelik | Alan | Aciliyet | Sorumlu | Beklenen Süre | Başarı Göstergesi |
|---------|------|----------|---------|---------------|-------------------|
| 1. 🔴 ACİL | ... | Bu hafta | ... | ... | ... |
| 2. 🔴 ACİL | ... | 2 hafta | ... | ... | ... |
| 3. 🟡 ÖNCELİKLİ | ... | 1 ay | ... | ... | ... |
| 4. 🟡 ÖNCELİKLİ | ... | 1 ay | ... | ... | ... |
| 5. 🟢 UZUN VADE | ... | 3 ay | ... | ... | ... |
| 6. 🟢 UZUN VADE | ... | 6 ay | ... | ... | ... |

## Takip Önerisi
*(Ne zaman yeniden değerlendirme yapılmalı? Hangi alanlar 3 ay sonra tekrar ölçülmeli?)*

## Kapanış Notu
*(3-4 cümlelik profesyonel, umut verici ve güçlendirici kapanış. Bu öğrencinin en parlak potansiyelini vurgula.)*

---

*Bu rapor, EĞİTİM CHECK UP psikometrik değerlendirme sistemi tarafından, yapay zeka destekli derinlikli analiz altyapısıyla üretilmiştir. Raporda yer alan tüm yorumlar, öğrencinin psikometrik test verilerine dayanmaktadır. Bu rapor klinik tanı içermez ve klinik değerlendirme yerine geçmez.*

*Dil: Türkçe. Üslup: Profesyonel, sıcak, yapıcı, güçlendirici. Rapor boyunca öğrenciyi asla yargılama — potansiyelini ortaya çıkarmaya odaklan.*"""


def _get_test_specific_guidance(test_name):
    """Her test için ticari kalite özel analiz yönergesi döndürür."""

    if "Enneagram" in test_name:
        return """
## 🔬 ENNEAGRAM KİŞİLİK TESTİ — UZMAN ANALİZ PROTOKOLÜ

Bu test, 9 Enneagram kişilik tipini %0-100 ölçeğinde ölçmektedir. Raporda aşağıdaki ANALİZ KATMANLARININ HER BİRİNİ eksiksiz ve derinlikli şekilde ele al:

### KATMAN 1: ANA TİP DERİN PROFİLİ
- Ana tipin ismi, temel motivasyonu, temel korkusu ve temel arzusu
- Bu tipin "dünya görüşü" — hayata hangi pencereden bakıyor?
- Sağlıklı düzey (büyüme modunda) → ortalama düzey → sağlıksız düzey (stres modunda) arasında bu öğrenci nerede duruyor? Puan yüzdesine göre değerlendir
- Bu tipin okul ortamındaki tipik davranış kalıpları:
  → Sınıfta nasıl oturur, nasıl dinler, nasıl katılır?
  → Ödevlere yaklaşımı nasıldır?
  → Sınav döneminde nasıl davranır?
  → Grup çalışmasında hangi rolü üstlenir?
  → Öğretmenle ilişkisi nasıldır?
  → Akranlarla ilişkisi nasıldır?
  → Başarı ve başarısızlık karşısında nasıl tepki verir?
- Bu tipin öğrenme tarzını ve akademik motivasyon kaynaklarını ayrıntıla

### KATMAN 2: KANAT (WING) ANALİZİ
- Ana tipin yanındaki iki tipten (kanat adayları) hangisinin puanı daha yüksek?
- Tam kanat notasyonu (örn: "4w5", "7w8") ve bu kombinasyonun anlamı
- Kanat etkisinin kişiliğe kattığı nüanslar (Örn: 4w3 dışa dönük ve hırslıyken, 4w5 içe dönük ve analitiktir)
- Kanat etkisinin öğrenme stili ve akademik motivasyon üzerindeki somut yansıması
- Diğer kanattan gelen zayıf etki de varsa bunu not et

### KATMAN 3: TRİTYPE (ÜÇ MERKEZ) ANALİZİ
- **Karın Merkezi (8-9-1):** Bu merkezden en yüksek puanlı tip → İçgüdüsel tepkiler, öfke yönetimi, sınır koyma
- **Kalp Merkezi (2-3-4):** Bu merkezden en yüksek puanlı tip → Duygusal tepkiler, kimlik duygusu, ilişki ihtiyacı
- **Kafa Merkezi (5-6-7):** Bu merkezden en yüksek puanlı tip → Zihinsel tepkiler, kaygı yönetimi, bilgi işleme
- Bu üç tipin birleşiminin çizdiği bütüncül portre — "Bu öğrenci stresle karşılaşınca önce ne yapar, sonra ne hisseder, sonra nasıl düşünür?"
- Tritype kombinasyonunun akademik ve sosyal hayattaki somut yansımaları

### KATMAN 4: STRES ve BÜYÜME DİNAMİĞİ
- Ana tipin stres yönündeki tip hangisi? Bu tipin puanı nedir? (Yüksekse → stres altında bu yöne kayma eğilimi güçlü)
- Ana tipin büyüme yönündeki tip hangisi? Bu tipin puanı nedir? (Yüksekse → sağlıklı gelişim potansiyeli kuvvetli)
- Stres altında bu öğrencinin sergileyeceği SOMUT davranışlar:
  → Sınıfta nasıl değişir?
  → Arkadaş ilişkilerinde ne olur?
  → Ders çalışma alışkanlıkları nasıl bozulur?
  → Bedensel belirtiler neler olabilir?
- Büyüme yolunda ilerlerken gözlemlenmesi beklenen POZİTİF değişimler

### KATMAN 5: PUAN HARİTASI ANALİZİ (9 TİP BİRLİKTE)
- Tüm 9 tipin puanlarını yüksekten düşüğe sırala ve şeklini yorumla:
  → Tek zirve profili: Ana tip belirgin, diğerleri düşük → Net, güçlü kişilik yapısı
  → Çift zirve: İki tip yakın → İç çatışma veya zenginlik göstergesi
  → Plato profili: Birden fazla tip orta-yüksek → Esnek ama belirsiz kimlik
  → Dağ silsilesi: 3-4 tip kümeleniyor → Alt grup analizi gerekli (hangi merkezde kümeleniyor?)
- En düşük puanlı tiplerin anlamı: Baskılanan, reddedilen veya gelişmemiş yönler
- İkincil ve üçüncül güçlü tiplerin ana tiple etkileşimi (destekliyor mu, çelişiyor mu?)
- Genel puan dağılımının "kişilik esnekliği" hakkında ne söylediğini yorumla

### KATMAN 6: KİŞİSEL GELİŞİM ve REHBERLIK
- Bu kişilik tipinin büyüme yolundaki 7 somut adım (yaşa uygun, günlük hayata uygulanabilir)
- Her adım için "Bunu neden yapmalı?" açıklaması
- Bu tipin düşebileceği 5 tuzak ve her birinden nasıl kaçınılır
- Aile iletişim rehberi: Bu tipte bir çocukla konuşurken kullanılması gereken dil ve yaklaşım
- Öğretmen iletişim rehberi: Sınıf ortamında bu tipi desteklemenin en etkili yolları
- Bu tipin "süper gücü" — en iyi versiyonunda dünyaya ne katar?
"""

    elif "Çalışma Davranışı" in test_name:
        return """
## 🔬 ÇALIŞMA DAVRANIŞI ÖLÇEĞİ — UZMAN ANALİZ PROTOKOLÜ

Bu test 7 alt kategoride ders çalışma alışkanlıklarını ölçer. Her kategoriyi AYRI AYRI ve BİRBİRİYLE İLİŞKİLENDİREREK analiz et:

**Kategoriler:**
- A: Motivasyon ve Ders Çalışmaya Karşı Tutum
- B: Zaman Yönetimi
- C: Derse Hazırlık ve Katılım
- D: Okuma ve Not Tutma Alışkanlıkları
- E: Yazılı Anlatım ve Ödev Yapma
- F: Sınava Hazırlanma
- G: Genel Çalışma Koşulları ve Alışkanlıkları

**Raporda mutlaka yap:**
- Her kategoriyi 1 paragraf derinliğinde yorumla
- Kategoriler arası çapraz ilişkileri tespit et (Örn: "Yüksek motivasyon + düşük zaman yönetimi → istekli ama plansız öğrenci profili")
- "Darboğaz analizi" yap: Hangi kategori diğerlerinin performansını aşağı çekiyor?
- Güçlü kategorilerin nasıl kaldıraç olarak kullanılabileceğini açıkla
- Somut bir GÜNLÜK çalışma programı taslağı oluştur (saatler, dersler, aralar dahil)
- Somut bir HAFTALIK plan oluştur
- Sınav dönemi özel planı öner
- Fiziksel çalışma ortamı önerileri (masa düzeni, ışık, ses, telefon yönetimi, araçlar)
- Dijital araç önerileri (planlama uygulamaları, Pomodoro, not alma araçları)
"""

    elif "Sağ-Sol Beyin" in test_name:
        return """
## 🔬 SAĞ-SOL BEYİN DOMINANSI TESTİ — UZMAN ANALİZ PROTOKOLÜ

Bu test beyin yarım küre baskınlığını ölçer (sağ/sol yüzde + baskınlık seviyesi).

**Raporda mutlaka yap:**
- Baskınlık derecesini yorumla: hafif baskınlık vs güçlü baskınlık vs denge
- Her yarım kürenin bilişsel özelliklerini açıkla ve bu öğrencinin profiline uygula
- Sol baskınlık özellikleri: analitik, sıralı, mantıksal, detaycı, dil odaklı, zamanlı
- Sağ baskınlık özellikleri: bütüncül, görsel, yaratıcı, sezgisel, mekan odaklı, eş zamanlı
- Dengeli profil: her iki yarım küreyi kullanabilme avantajı

**Ders bazlı strateji tablosu oluştur:**
| Ders | Sol Beyin Stratejisi | Sağ Beyin Stratejisi | Bu Öğrenci İçin Öneri |
|------|---------------------|---------------------|----------------------|
| Her ana ders için doldur |

- Sınıf içi oturma, dinleme ve not alma stratejileri
- Zayıf yarım küreyi güçlendirme egzersizleri
- Bu baskınlığın kariyer yönelimine etkisi
"""

    elif "Sınav Kaygısı" in test_name:
        return """
## 🔬 SINAV KAYGISI ÖLÇEĞİ — UZMAN ANALİZ PROTOKOLÜ

Bu test 7 alt boyutta sınav kaygısını ölçer. HER ALT BOYUTU AYRI PARAGRAFTA DERİNLEMESİNE YORUMLA:

**Alt Boyutlar:**
1. Başkalarının Görüşü Kaygısı → Sosyal değerlendirme korkusu
2. Kendi Hakkındaki Görüşü → Öz-yeterlik algısı
3. Gelecek Endişesi → Uzun vadeli kaygı, belirsizlik intoleransı
4. Hazırlık Endişesi → Yeterli hazırlanamama korkusu
5. Bedensel Tepkiler → Somatik belirtiler (mide, terleme, çarpıntı)
6. Zihinsel Tepkiler → Bilişsel belirtiler (unutma, konsantrasyon kaybı, zihin boşalması)
7. Genel Kaygı → Yaygın kaygı düzeyi

**Raporda mutlaka yap:**
- Her alt boyutu ayrı yorumla ve birbiriyle ilişkilendir
- "Kaygı profili tipi" belirle: bedensel ağırlıklı mı, zihinsel ağırlıklı mı, sosyal kaynaklı mı, hazırlık odaklı mı?
- Kaygı-performans ilişkisini açıkla: Yerkes-Dodson yasası çerçevesinde bu öğrencinin kaygısı performansı artırıyor mu yoksa engelliyor mu?
- Kaygı döngüsünü diyagram şeklinde açıkla: tetikleyici → düşünce → duygu → beden → davranış → sonuç → tetikleyici
- Bu öğrencinin spesifik kaygı tetikleyicilerini tespit et
- 5 aşamalı sınav hazırlık protokolü:
  → Sınavdan 1 hafta önce
  → Sınavdan 3 gün önce
  → Sınav akşamı
  → Sınav sabahı
  → Sınav anında (ilk 5 dakika stratejisi)
- Bilişsel yeniden yapılandırma örnekleri (olumsuz düşünce → alternatif düşünce)
- Nefes ve gevşeme tekniklerini adım adım anlat
- Aileye özel bölüm: Baskı yapmadan nasıl destek olunur? Sınav döneminde evde nasıl bir ortam yaratılmalı?
"""

    elif "VARK" in test_name:
        return """
## 🔬 VARK ÖĞRENME STİLLERİ TESTİ — UZMAN ANALİZ PROTOKOLÜ

Bu test 4 öğrenme kanalını ölçer: V (Görsel), A (İşitsel), R (Okuma/Yazma), K (Kinestetik).

**Raporda mutlaka yap:**
- Baskın stil(ler)i ve multimodal durumu detaylandır (tek baskın mı, çift baskın mı, multimodal mı?)
- Her stilin ne anlama geldiğini aile dilinde açıkla
- Baskın stile göre "ideal öğrenme ortamı" tanımla (fiziksel mekan, araçlar, süre, yöntem)

**Her ana ders için detaylı strateji tablosu oluştur:**

| Ders | Baskın Stile Uygun Teknik | Somut Araç/Materyal | Ders Çalışma Senaryosu |
|------|--------------------------|--------------------|-----------------------|
| Matematik | ... | ... | "Önce ... yap, sonra ... kullan, ardından ..." |
| Fen Bilimleri | ... | ... | ... |
| Türkçe/Edebiyat | ... | ... | ... |
| Sosyal Bilimler | ... | ... | ... |
| Yabancı Dil | ... | ... | ... |

- Her tekniği senaryo formatında anlat: "Tarih konusu çalışırken şunu yap..."
- Zayıf kanalları güçlendirme stratejileri (neden önemli + nasıl)
- Dijital araç ve uygulama önerileri (YouTube kanalları, uygulamalar, web siteleri — yaşa uygun)
- Öğretmenin sınıfta kullanabileceği stile uygun öğretim yöntemleri
- Sınav çalışmasında stile özel hafıza teknikleri
"""

    elif "Çoklu Zeka" in test_name:
        return """
## 🔬 ÇOKLU ZEKA TESTİ (GARDNER) — UZMAN ANALİZ PROTOKOLÜ

Bu test Gardner'ın 8 zeka alanını %0-100 ölçeğinde ölçer:
Sözel-Dilsel, Mantıksal-Matematiksel, Görsel-Uzamsal, Bedensel-Kinestetik, Müzikal-Ritmik, Kişilerarası (Sosyal), İçsel (Özedönük), Doğacı.

**Raporda mutlaka yap:**

**8 Zekanın Her Birini 1 Paragraf Derinliğinde Yorumla:**
- Puanın ne anlama geldiği
- Günlük hayatta nasıl gözlemlenir
- Akademik hayatta nasıl yansır
- Gelişim önerisi

**Zeka Profili Analizi:**
- Profil tipi: Uzmanlaşmış (1-2 zirve) / Çok yönlü (3-4 yüksek) / Dengeli (hepsi orta)
- En güçlü 3 zekanın sinerjisi: birlikte ne anlama geliyorlar?
- En zayıf 2 zekanın akademik etkisi ve telafi stratejileri
- "Zeka imzası" — bu öğrencinin benzersiz zeka kombinasyonunu 1 cümlede tanımla

**Zeka-Ders Eşleştirme Tablosu:**
| Zeka Alanı | Puan | İlgili Dersler | Güçlendirme Aktivitesi |
|-----------|------|---------------|----------------------|
| Her 8 zeka için doldur |

**Zeka-Kariyer Eşleştirme Tablosu:**
| Güçlü Zeka | Kariyer Alanları | Ünlü İsimler | Somut Adım |
|-----------|-----------------|-------------|-----------|
| Her güçlü zeka için doldur |

- Ders dışı aktivite, kulüp ve hobi önerileri (en az 5)
- Evde yapılabilecek zeka geliştirme aktiviteleri
"""

    elif "Holland" in test_name:
        return """
## 🔬 HOLLAND MESLEKİ İLGİ ENVANTERİ (RIASEC) — UZMAN ANALİZ PROTOKOLÜ

Bu test 6 mesleki ilgi tipini 0-28 puan aralığında ölçer:
R (Gerçekçi), I (Araştırmacı), A (Sanatçı), S (Sosyal), E (Girişimci), C (Geleneksel).

**Raporda mutlaka yap:**

**6 Tipin Her Birini 1 Paragraf Derinliğinde Yorumla:**
- Bu öğrencinin puanı ne anlama geliyor?
- Bu düzeydeki ilgi günlük hayatta nasıl gözlemlenir?
- Hangi aktiviteler, dersler ve ortamlar bu ilgiyle uyumlu?

**3 Harfli Holland Kodu Analizi:**
- En yüksek 3 tipi belirle ve kodun birleşik anlamını açıkla
- Holland altıgenindeki konumlandırma: bitişik tipler (uyumlu) vs karşıt tipler (çelişkili)
- Bu kodun iş dünyasındaki karşılığı — hangi sektörler, hangi iş ortamları?

**Kapsamlı Kariyer Haritası:**

| # | Meslek / Alan | Holland Uyumu | Eğitim Yolu | Türkiye'de İş İmkanı | Bu Öğrenci İçin Neden? |
|---|-------------|-------------|------------|---------------------|---------------------|
| 1-15 arası doldur — en az 15 meslek önerisi |

**Eğitim Yönlendirme:**
- Lise alan seçimi tavsiyesi: Sayısal / Eşit Ağırlık / Sözel / Dil (gerekçesiyle)
- Üniversite bölüm önerileri: En uygun 8 bölüm ve her birinin neden uygun olduğu
- Yurt dışı eğitim düşünülüyorsa alternatif yollar

**Kariyer Keşif Planı:**
- Bu yaz yapılabilecek staj/gönüllülük önerileri
- Katılınabilecek kulüp, atölye, yarışma önerileri
- İzlenecek/okunacak kaynak önerileri (belgesel, kitap, podcast)
- İş gölgeleme (job shadowing) programları

⚠️ *Bu değerlendirme profesyonel kariyer danışmanlığını destekler; tek başına kesin yönlendirme için yeterli değildir.*
"""

    elif "D2 Dikkat" in test_name:
        return """
## 🔬 D2 DİKKAT TESTİ — UZMAN ANALİZ PROTOKOLÜ

Bu test, Brickenkamp d2 dikkat testinin dijital adaptasyonudur. Aşağıdaki metrikleri analiz et:

### KATMAN 1: TEMEL METRİKLER
- **CP (Konsantrasyon Performansı):** Doğru hedefler − Yanlış işaretlemeler. En önemli gösterge.
- **TN-E (Toplam Performans):** Toplam işaretleme − Toplam hata. Genel performans.
- **E1 (Atlama Hatası):** Hedef atlandı → Dikkat dağılması göstergesi
- **E2 (Yanlış İşaretleme):** Hedef olmayan işaretlendi → Dürtüsellik göstergesi
- **FR (Dalgalanma):** Satırlar arası performans farkı → Dikkat sürdürülebilirliği

### KATMAN 2: PROFİL ANALİZİ
- Hız-Doğruluk dengesi: Dürtüsel mi (hızlı ama hatalı), temkinli mi (yavaş ama doğru), dengeli mi?
- Satır performans eğrisi: Yorulma etkisi var mı? İlk satırlar mı son satırlar mı daha iyi?
- Hata türü dağılımı: E1 > E2 ise dikkat eksikliği, E2 > E1 ise dürtüsellik ön planda

### KATMAN 3: AKADEMİK ETKİ
- Dikkat seviyesinin ders dinleme, ödev yapma, sınav çözme üzerindeki etkisi
- Yaşa uygun beklentiler çerçevesinde değerlendirme
- Dikkat sürdürülebilirliğinin uzun sınavlar ve proje çalışmaları açısından önemi

### KATMAN 4: SOMUT ÖNERİLER
- Dikkat geliştirme egzersizleri (yaşa uygun)
- Çalışma ortamı düzenlemesi
- Pomodoro ve odaklanma teknikleri
- Gerekiyorsa uzman yönlendirmesi (dikkat eksikliği değerlendirmesi)
"""

    elif "Akademik Analiz" in test_name:
        return """
## 🔬 AKADEMİK ANALİZ TESTİ — UZMAN ANALİZ PROTOKOLÜ

Bu test, 4 alt boyutta akademik yetkinliği ölçen performans bazlı bir testtir:

### KATMAN 1: OKUMA ANLAMA ANALİZİ
- Metin kavrama, çıkarım ve ana fikir yakalama becerisi
- Yaşa göre normatif değerlendirme
- Akademik metinleri anlama kapasitesinin tüm dersler üzerindeki etkisi

### KATMAN 2: MATEMATİKSEL MUHAKEME
- Sayısal düşünme ve problem çözme becerisi
- Soyut düşünme kapasitesi
- Çok adımlı problem çözme yetkinliği

### KATMAN 3: MANTIKSAL DÜŞÜNME
- Örüntü tanıma, analoji, sıralama ve çıkarım becerileri
- Analitik düşünme kapasitesi
- Eleştirel düşünme potansiyeli

### KATMAN 4: PERFORMANS vs ÖZ-DEĞERLENDİRME UYUMU
- Öğrencinin kendini değerlendirmesi ile gerçek performansı arasındaki fark
- Akademik özgüven analizi
- Farkındalık düzeyi ve motivasyon dinamikleri

### KATMAN 5: BÜTÜNLEŞİK AKADEMİK PROFİL
- 4 boyutun etkileşim analizi
- Güçlü alandan zayıf alana transfer stratejileri
- Kişiye özel gelişim planı (0-1 ay, 1-3 ay, 3-6 ay)
"""

    return ""


def build_single_test_prompt(student_name, student_age, student_gender, test_name, test_data):
    """Tekil test analizi için ticari kalite prompt — her teste özel uzman protokolü içerir."""

    test_guidance = _get_test_specific_guidance(test_name)

    return f"""# ROL ve KİMLİK

Sen, Türkiye'nin önde gelen eğitim psikolojisi merkezlerinde 20 yıl deneyim kazanmış, psikometrik test yorumlama konusunda uzmanlaşmış bir Klinik Eğitim Psikoloğusun.

Bu rapor, ücretli bir profesyonel danışmanlık hizmetinin çıktısıdır. Tek bir test sonucunu, sanki karşında oturan aileye yüz yüze sunuyormuş gibi, derinlikli, kişiselleştirilmiş ve uygulanabilir şekilde analiz edeceksin.

---

# ÖĞRENCİ DOSYASI

| Alan | Bilgi |
|------|-------|
| İsim | {student_name} |
| Yaş | {student_age} |
| Cinsiyet | {student_gender} |
| Analiz Edilen Test | {test_name} |
| Değerlendirme Türü | Tekil Test Derinlikli Analiz |

## TEST VERİSİ (JSON)
```json
{json.dumps(test_data, ensure_ascii=False, indent=2)}
```

---

# KRİTİK KURALLAR

1. **KANITSAL ZORUNLULUK:** Her yorum, iddia ve tespit mutlaka parantez içinde test adı ve puan ile desteklenmeli. Kanıtsız hiçbir yorum yapma.

2. **DERİNLİK ZORUNLULUĞU:** Bu ücretli bir profesyonel hizmettir. Her bölüm, bir psikolog danışmanlık seansında anlatacağı kadar detaylı olmalı. Genel geçer, şablonik, "daha çok çalış" tarzı yüzeysel tavsiyeler YASAK. Her öneri bu öğrencinin spesifik puan profilinden türetilmeli.

3. **PUAN YORUMLAMA ÇERÇEVESİ:**
   - %0-20 → Belirgin gelişim alanı — yapılandırılmış destek önerilir
   - %21-40 → Ortalamanın altı — hedefli çalışma gerektirir
   - %41-60 → Ortalama düzey — strateji ile yükseltilebilir
   - %61-80 → Güçlü alan — sürdürülebilir ve ileri taşınabilir
   - %81-100 → Çok güçlü — yetenek göstergesi, özel destekle parlayabilir

4. **TIBBİ TANI YASAĞI:** Klinik tanı terimleri (DEHB, depresyon, disleksi, anksiyete bozukluğu vb.) kesinlikle kullanma.

5. **GELİŞİMSEL BAĞLAM:** {student_age} yaşındaki bir bireyin gelişimsel özelliklerini referans al.

6. **UZUNLUK:** Bu rapor minimum 2500 kelime olmalıdır. Her bölüm ödenen ücrete değecek derinlikte olmalı.

---
{test_guidance}
---

# RAPOR FORMATI (HER BÖLÜMÜ AYNEN DOLDUR, HİÇBİRİNİ ATLAMA)

---

## 📋 YÖNETİCİ ÖZETİ
*(Raporu okuyacak kişinin 1 dakikada tüm tabloyu göreceği 4-5 cümlelik güçlü özet. En kritik bulgu, en önemli güç, en acil gelişim alanı ve en öncelikli adım.)*

---

## 📊 1. TEST SONUÇ TABLOSU

**Tek Cümle Sonuç:** *(Testin en önemli bulgusunu, öğrenciyi tanımayan birinin bile anlayacağı netlikte ifade et.)*

**Tüm Boyutlar Görsel Özeti:**
```
[Boyut/Kategori Adı]    : ██████████ XX%  → [Kısa Yorum]
[Boyut/Kategori Adı]    : ████████░░ XX%  → [Kısa Yorum]
[Boyut/Kategori Adı]    : ██████░░░░ XX%  → [Kısa Yorum]
[Boyut/Kategori Adı]    : ████░░░░░░ XX%  → [Kısa Yorum]
...devam — TÜM boyutları listele, hiçbirini atlama
```

---

## 🧠 2. DERİNLEMESİNE YORUM

*(Bu raporun kalbi burasıdır. Her alt boyutu/kategoriyi ayrı ayrı derinlemesine yorumla ve birbirleriyle ilişkilendir.

Her alt boyut için:
- Bu puan ne anlama geliyor?
- Günlük hayatta nasıl gözlemlenir?
- Okul ortamında nasıl yansır?
- Diğer alt boyutlarla nasıl etkileşir?

Ardından genel profil sentezi:
- Profilin şekli — dengeli mi, tek zirve mi, çoklu zirve mi?
- Bu profilin "hikayesi" — veriler birlikte okunduğunda ne anlatıyor?
- Öğrencinin bu profile sahip olmasının olası gelişimsel ve çevresel nedenleri

Minimum 5-6 paragraf, akıcı ve profesyonel anlatım.)*

---

## 💪 3. GÜÇLÜ YÖNLER ANALİZİ

| # | Güçlü Yön | Kanıt (Puan) | Okul Yaşamında Nasıl Gözlemlenir? | Nasıl İleri Taşınabilir? | Kariyer Bağlantısı |
|---|-----------|--------------|----------------------------------|--------------------------|-------------------|
| 1 | ... | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... | ... |
| 4 | ... | ... | ... | ... | ... |
| 5 | ... | ... | ... | ... | ... |

*(Minimum 5 güçlü yön. Her birini 1-2 cümlelik açıklamayla destekle.)*

---

## 🌱 4. GELİŞİM ALANLARI ve MÜDAHALE STRATEJİLERİ

| # | Gelişim Alanı | Mevcut Durum (Puan) | Risk Düzeyi | Bu Neden Önemli? | Haftalık Gelişim Planı |
|---|-------------|---------------------|-------------|-----------------|----------------------|
| 1 | ... | ... | 🔴/🟡/🟢 | ... | ... |
| 2 | ... | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... | ... |
| 4 | ... | ... | ... | ... | ... |

*(Minimum 4 gelişim alanı. Her biri için detaylı strateji.)*

---

## 🎯 5. KAPSAMLI AKSİYON PLANI

**📌 STRATEJİ 1: [Başlık]**
- **Hedef:** *(Ne başarılacak?)*
- **Neden bu öğrenci için önemli:** *(Veri referansıyla)*
- **Adım adım uygulama:** *(Günlük/haftalık program)*
- **Gerekli araç/materyal:** *(Somut)*
- **Başarı göstergesi:** *(Nasıl ölçülecek?)*
- **Sorumlu:** *(Öğrenci/Öğretmen/Aile)*
- **Beklenen süre:** *(Ne kadar sürede sonuç görülür?)*

**📌 STRATEJİ 2: [Başlık]**
*(Aynı formatta)*

**📌 STRATEJİ 3: [Başlık]**
*(Aynı formatta)*

**📌 STRATEJİ 4: [Başlık]**
*(Aynı formatta)*

**📌 STRATEJİ 5: [Başlık]**
*(Aynı formatta)*

---

## 👨‍👩‍👦 6. AİLE DANIŞMANLIK BÖLÜMÜ

### Bu Sonuçlar Ne Anlama Geliyor?
*(Teknik terminolojiyi aile diline çevir. Ebeveynin çocuğunu daha iyi anlamasını sağla. 2-3 paragraf.)*

### ✅ Evde Yapılması Gerekenler (En Az 5 Madde)
*(Her madde test verisine dayalı, somut ve uygulanabilir. "Neden?" açıklaması ile.)*

### ❌ Kaçınılması Gerekenler (En Az 4 Madde)
*(Kişilik/profil tipine göre hangi yaklaşımlar zarar verebilir? Somut örneklerle.)*

### 🗣️ İletişim Rehberi
*(Bu profildeki bir çocukla nasıl konuşulmalı? Duruma göre örnek cümleler:)*
- Başarı gösterdiğinde: "..."
- Zorlandığında: "..."
- Motivasyonu düştüğünde: "..."
- Çatışma anında: "..."

---

## 👩‍🏫 7. ÖĞRETMEN ve REHBER ÖĞRETMEN BÖLÜMÜ

### Sınıf İçi Stratejiler (En Az 5 Madde)
*(Her strateji bu öğrencinin veri profilinden türetilmiş olmalı.)*

### İletişim ve Geri Bildirim Yaklaşımı
*(Bu öğrenciyle en etkili iletişim tarzı. Nelere dikkat edilmeli?)*

### Erken Uyarı İşaretleri
*(Bu profildeki bir öğrencide hangi davranış değişiklikleri risk göstergesi olabilir?)*

### Rehber Öğretmen İçin Takip Planı
*(Bireysel görüşmelerde odaklanılacak temalar, izlenecek gelişim alanları)*

---

## 📌 8. SONUÇ ve ÖNCELİK MATRİSİ

| Öncelik | Eylem | Aciliyet | Sorumlu | Süre | Başarı Göstergesi |
|---------|-------|----------|---------|------|-------------------|
| 1. 🔴 | ... | Bu hafta | ... | ... | ... |
| 2. 🔴 | ... | 2 hafta | ... | ... | ... |
| 3. 🟡 | ... | 1 ay | ... | ... | ... |
| 4. 🟡 | ... | 1 ay | ... | ... | ... |
| 5. 🟢 | ... | 3 ay | ... | ... | ... |

### Takip Önerisi
*(Ne zaman yeniden değerlendirme yapılmalı?)*

### Kapanış Notu
*(Profesyonel, umut verici, güçlendirici kapanış. Bu öğrencinin potansiyelini vurgula.)*

---

*Bu rapor, EĞİTİM CHECK UP psikometrik değerlendirme sistemi tarafından, yapay zeka destekli derinlikli analiz altyapısıyla üretilmiştir. Raporda yer alan tüm yorumlar, öğrencinin test verilerine dayanmaktadır. Bu rapor klinik tanı içermez.*

*Dil: Türkçe. Üslup: Profesyonel, sıcak, yapıcı, güçlendirici. Öğrenciyi asla yargılama — potansiyelini ortaya çıkarmaya odaklan.*"""

# ============================================================
# ANA ÖĞRETMEN UYGULAMASI
# ============================================================
def app():
    # --- CSS ---
    st.markdown("""
    <style>
        /* ===== ÖĞRETMEN PANEL CSS ===== */
        .stSelectbox div, .stMultiSelect div { cursor: pointer !important; }
        div[data-baseweb="select"] { cursor: pointer !important; }
        div[role="listbox"] li { cursor: pointer !important; }
        
        .stRadio > label { 
            font-weight: bold; font-size: 16px; 
            color: #1B2A4A; cursor: pointer !important; 
        }
        .stRadio div[role="radiogroup"] > label { cursor: pointer !important; }
        
        .archive-box { 
            background-color: #f8f9fa; border: 1px solid #ddd; 
            padding: 15px; border-radius: 12px; margin-bottom: 20px; 
        }
        .report-header { 
            color: #155724; background: linear-gradient(135deg, #d4edda, #c3e6cb); 
            padding: 12px 16px; border-radius: 8px; margin-bottom: 10px; 
            border: 1px solid #c3e6cb; font-weight: bold; 
        }
        
        /* Kimlik Kartı */
        .id-card {
            background: #ffffff;
            border: 1px solid #E0E4EA;
            border-radius: 16px;
            padding: 25px;
            border-top: 4px solid #1B2A4A;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .id-card-name {
            font-size: 1.5rem;
            font-weight: 800;
            color: #1B2A4A;
            margin-bottom: 15px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("## 👨‍🏫 Öğretmen Yönetim Paneli")
    st.caption("EĞİTİM CHECK UP — Kişisel Eğitim & Kariyer Analiz Merkezi")
    st.markdown("---")

    # Veritabanından verileri çek
    data = get_all_students_with_results()
    student_names_all = [d["info"].name for d in data] if data else []

    # --- SIDEBAR: YÖNETİM ---
    with st.sidebar:
        st.markdown("### ⚙️ Yönetim Araçları")

        with st.expander("🗑️ Öğrenci Dosyası Sil"):
            if not student_names_all:
                st.info("Sistemde kayıtlı öğrenci yok.")
            else:
                st.warning("Seçilen öğrencilerin tüm verileri silinecektir.")
                selected_to_delete = st.multiselect("Silinecekleri Seç:", options=student_names_all)
                if selected_to_delete:
                    if st.button("SEÇİLENLERİ SİL", type="primary"):
                        if delete_specific_students(selected_to_delete):
                            st.success("Kayıtlar silindi.")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Silme başarısız.")

        st.markdown("---")

        with st.expander("⚠️ Fabrika Ayarlarına Dön"):
            st.error("DİKKAT: Tüm veritabanı silinir!")
            confirm_reset = st.checkbox("Evet, tüm verilerin silineceğini anlıyorum")
            if confirm_reset:
                if st.button("TÜM SİSTEMİ SIFIRLA", type="primary"):
                    if reset_database():
                        st.success("Sistem sıfırlandı.")
                        time.sleep(1)
                        st.rerun()
            else:
                st.info("Devam etmek için onay kutucuğunu işaretleyin.")

    # --- ANA EKRAN ---
    if not data:
        st.info("📂 Henüz kayıtlı öğrenci verisi bulunmamaktadır.")
        return

    # --- GENEL İSTATİSTİKLER ---
    total_students = len(data)
    total_tests = sum(len(d["tests"]) for d in data)
    
    mc1, mc2, mc3 = st.columns(3)
    mc1.metric("👥 Toplam Öğrenci", total_students)
    mc2.metric("📝 Toplam Test", total_tests)
    mc3.metric("📊 Ort. Test/Öğrenci", round(total_tests / total_students, 1) if total_students > 0 else 0)
    
    st.markdown("---")

    # 1. ÖĞRENCİ SEÇİMİ
    st.subheader("📂 Öğrenci Dosyası Görüntüle")

    col1, col2 = st.columns([1, 2])
    with col1:
        selected_name = st.selectbox(
            "Öğrenci Seçiniz:",
            student_names_all,
            index=None,
            placeholder="Listeden bir öğrenci seçin..."
        )

    if not selected_name:
        st.info("👆 Lütfen analizlerini görmek istediğiniz öğrenciyi seçiniz.")
        return

    # Seçilen öğrenci verilerini bul
    student_data = next(d for d in data if d["info"].name == selected_name)
    info = student_data["info"]
    tests = student_data["tests"]

    # 2. ÖĞRENCİ KİMLİK KARTI
    st.markdown(f"""
        <div class="id-card">
            <div class="id-card-name">🆔 {info.name}</div>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Yaş / Cinsiyet", f"{info.age} / {info.gender}")
    c2.metric("Kullanıcı Adı", info.username)
    c3.metric("Toplam Giriş", info.login_count)
    c4.metric("Çözülen Test", len(tests))

    st.divider()

    # ============================================================
    # 3. TAMAMLANAN TESTLER VE OTOMATİK SONUÇLAR
    # ============================================================
    st.subheader("📝 Tamamlanan Testler ve Otomatik Sonuçlar")
    st.caption("Öğrencinin bitirdiği testlerin anlık sistem raporlarını (yapay zekasız) görebilirsiniz.")

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
                    st.warning("Bu test için otomatik rapor bulunamadı.")
                    st.write("Ham Cevaplar:", t['raw_answers'])

    st.divider()

    # ============================================================
    # 4. KAYITLI AI RAPOR ARŞİVİ
    # ============================================================
    st.subheader("📂 Kayıtlı AI Rapor Arşivi")
    st.caption("Daha önce Claude ile oluşturduğunuz detaylı analizler.")

    history = get_student_analysis_history(info.id)

    if not history:
        st.info("Bu öğrenci için henüz AI destekli analiz raporu oluşturulmamış.")
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

            if st.button("🚀 ANALİZİ BAŞLAT (Claude AI)", type="primary"):
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
                    st.info(f"⏳ Claude AI, seçilen **{len(selected_tests)} testi** harmanlıyor...")

                    with st.spinner("Stratejik analiz hazırlanıyor..."):
                        ai_input = []
                        for t in analyzed_data:
                            raw = t.get("raw_answers", "")
                            if isinstance(raw, str):
                                try:
                                    raw = json.loads(raw)
                                except (json.JSONDecodeError, ValueError):
                                    raw = raw

                            ai_input.append({
                                "TEST_ADI": t["test_name"],
                                "TARİH": str(t["date"]),
                                "SONUÇLAR": t["scores"] if t["scores"] else raw
                            })

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
                    st.success(f"✅ {total_ops} test başarıyla analiz edildi ve Arşiv'e eklendi.")
                    time.sleep(2)
                    st.rerun()

    # 6. HAM VERİ LİSTESİ
    st.divider()
    with st.expander("🗂️ Ham Veri Listesi"):
        if tests:
            df_tests = pd.DataFrame(tests)
            df_tests['date'] = pd.to_datetime(df_tests['date'], errors='coerce').dt.strftime('%d.%m.%Y')
            st.dataframe(df_tests[["test_name", "date"]], use_container_width=True)
