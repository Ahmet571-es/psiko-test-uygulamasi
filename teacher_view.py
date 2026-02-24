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
            max_tokens=8000,
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
# PROMPT ÜRETME FONKSİYONLARI
# ============================================================

def build_holistic_prompt(student_name, student_age, student_gender, test_data_list):
    """Bütüncül (harmanlanmış) analiz için kapsamlı prompt."""
    return f"""Sen, Türkiye'de 15+ yıl deneyime sahip bir eğitim psikoloğu, kariyer danışmanı ve öğrenci koçusun. 
Psikometrik verileri sentezleyerek öğrenci hakkında klinik düzeyde bütünsel bir profil çıkarıyorsun.
Raporun, velilere ve öğretmenlere sunulacak profesyonel bir analiz belgesidir.

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

1. **VERİ BAĞLILIĞI:** Yalnızca JSON içindeki somut puanlara dayanan yorumlar yap. Her iddiayı (puan: XX) şeklinde kanıtla.
2. **SENTEZ ODAKLI:** Testleri tek tek özetleme — testler ARASI ilişkileri, korelasyonları ve örüntüleri analiz et.
3. **ÇELİŞKİ TESPİTİ:** Veriler arasındaki çelişkileri açıkça işaretle. Örn: "Yüksek sosyal zeka ama düşük girişimcilik skoru", "Güçlü analitik düşünme ama yüksek sınav kaygısı."
4. **TIBBİ TANI YASAĞI:** "DEHB", "depresyon", "anksiyete bozukluğu", "disleksi" gibi klinik tanı terimleri kesinlikle kullanma.
5. **YAŞA UYGUNLUK:** {student_age} yaşındaki bir öğrenci için somut, uygulanabilir, gerçekçi tavsiyeler ver.
6. **NEDEN-SONUÇ BAĞLANTISI:** "Ders çalışamıyor" gibi sonuç ifadeleri yerine "VARK Kinestetik skoru yüksek olduğu için masa başında uzun süre odaklanmakta güçlük çekiyor olabilir" gibi veri destekli nedenler kullan.
7. **PUAN YORUMLAMA STANDARDI:**
   - %0-30 → "Gelişime çok açık"
   - %31-50 → "Ortalama altı, geliştirilebilir"
   - %51-70 → "Ortalama / dengeli"
   - %71-85 → "Güçlü"
   - %86-100 → "Çok güçlü / baskın"
8. **KAPSAMLI OL:** Bu rapor bir aileye ve öğretmene sunulacak resmi bir belgedir. Yüzeysel değil, derinlemesine analiz yap. Minimum 2000 kelime.

---

## 🔬 TESTE ÖZEL YORUM REHBERİ

Eğer veride aşağıdaki testler varsa, sentez yaparken bu detaylara dikkat et:

### Enneagram Varsa:
- Ana tip ve kanat (wing) kombinasyonunun kişilik dinamiğini açıkla
- Stres ve gelişim yönlerinin diğer test sonuçlarıyla uyumunu analiz et
- 9 tipin puanlarını sıralayarak "kişilik haritasının genel şeklini" yorumla (yüksek puanlar kümeleniyor mu, dağınık mı?)
- Ana tipin öğrenme stili ve motivasyon kaynaklarını diğer testlerle çapraz kontrol et (Örn: Tip 5 analitik → Sol beyin baskın mı?, Tip 7 hevesli → çalışma davranışı düzensiz mi?)
- Enneagram tipi ile Holland RIASEC kodu arasındaki uyumu değerlendir

### Çoklu Zeka Varsa:
- En güçlü 3 zeka alanını Holland RIASEC ile karşılaştır
- Zeka profili dengesini analiz et: uzmanlaşmış mı, çok yönlü mü?
- Zayıf zeka alanlarının akademik performansa etkisini değerlendir

### Sınav Kaygısı Varsa:
- Alt kategorileri ayrı ayrı yorumla (bedensel, zihinsel, gelecek endişesi vb.)
- Kaygı kaynağını tespit et: performans kaygısı mı, hazırlık eksikliği mi, dış baskı mı?
- Çalışma davranışı ile kaygı arasındaki ilişkiyi analiz et (düzensiz çalışma → kaygı döngüsü?)

### VARK + Sağ-Sol Beyin Birlikte Varsa:
- "Öğrenme DNA'sını" oluştur: beyin dominansı + duyu tercihi birleşimi
- Sınıf ortamında en verimli öğrenme formatını somutlaştır

---

## 📝 RAPOR FORMATI (Bu formatı AYNEN KORU, bölüm atlama)

# 🚀 BÜYÜK RESİM: {student_name} Kimdir?

*(3-4 cümlelik güçlü, kişiselleştirilmiş giriş. Tüm testlerin ortak paydasını, öğrencinin en belirgin karakteristiğini anlat. Bir cümleyle öğrencinin "öğrenme imzasını" tanımla. Bu bölüm öğrenciyi tanımayan birinin okuduğunda net bir portre görmesini sağlamalı.)*

---

# 🧬 KİŞİLİK ve MOTİVASYON PROFİLİ

*(Eğer Enneagram verisi varsa bu bölümü mutlaka doldur. Yoksa diğer testlerden çıkarım yap.)*

### Temel Kişilik Dinamiği
*(Ana kişilik tipi, motivasyon kaynakları, temel korku ve arzu. Bu öğrenci neyin peşinde koşuyor, neyden kaçınıyor?)*

### Stres ve Büyüme Mekanizmaları
*(Bu öğrenci stres altında nasıl tepki verir? Sağlıklı büyüme yolunda hangi davranışlar beklenir? Bunu sınav kaygısı verileriyle çapraz kontrol et.)*

### Sosyal ve Duygusal Profil
*(İlişki tarzı, grup dinamiklerindeki rolü, duygusal zekası. Enneagram + Çoklu Zeka Kişilerarası verisinden çıkarım yap.)*

---

# 🧩 ZİHİNSEL SENTEZ

### Potansiyel ↔ Performans Dengesi
*(Zeka/yetenek puanları ile çalışma davranışı/kaygı skorları arasındaki ilişki. Bu öğrenci potansiyelini kullanabiliyor mu? Eğer kullanamıyorsa bunun nedeni ne olabilir? 2-3 paragraf derinlemesine analiz.)*

### Öğrenme DNA'sı
*(Sağ/Sol Beyin + VARK sonuçlarını birleştir. "Bu öğrenci en iyi nasıl öğreniyor?" sorusunu cevapla. Somut ders çalışma senaryosu öner. Örn: "Matematik çalışırken mind-map kullanması, Tarih çalışırken sesli okuma yapması önerilir.")*

### İlgi ↔ Yetenek Uyumu
*(Holland RIASEC kodu ile Çoklu Zeka güçlü yönleri örtüşüyor mu? Meslek yönelimi netleşiyor mu? Uyumsuzluk varsa bunun olası nedenlerini tartış.)*

### Çelişki ve Paradoks Analizi
*(Verilerdeki tüm çelişkileri listele ve açıkla. Her çelişki için olası nedenleri tartış. Minimum 2 çelişki bul. Örn: "Yüksek sosyal zeka + yüksek sınav kaygısı → performans değerlendirmesi sosyal bağlamda kaygı tetikliyor olabilir.")*

---

# ⚖️ KAPSAMLI DENGE TABLOSU

| 💪 Kanıtlanmış Güç (Test + Puan) | 🚧 Kritik Engel (Test + Puan) | 🔗 İlişki Analizi | 🎯 Çözüm Stratejisi |
|----------------------------------|-------------------------------|-------------------|---------------------|
| ... | ... | Güç engeli nasıl aşabilir? | Somut adım |
| ... | ... | ... | ... |

*(En az 5 satır doldur. Her güç ve engel mutlaka puan ile desteklenmeli.)*

---

# 📊 KRİTİK GÖSTERGELER PANELİ

### 🟢 Acil Müdahale Gerektirmeyen (İyi Düzey)
*(Hangi alanlarda öğrenci sağlıklı? Puanlarla listele.)*

### 🟡 Takip Gerektiren (Orta Düzey)
*(Hangi alanlarda gelişim potansiyeli var? Puanlarla listele.)*

### 🔴 Öncelikli İlgi Alanı (Kritik Düzey)
*(Hangi alanlarda acil destek gerekiyor? Puanlarla listele.)*

---

# 🗺️ STRATEJİK YOL HARİTASI

### 🎓 AKADEMİK BAŞARI PLANI

**[Çalışma Ortamı]:** *(VARK ve Sağ/Sol Beyin verilerine özel — masa düzeni, ışık, ses, araçlar)*
**[Günlük Çalışma Rutini]:** *(Çalışma Davranışı verilerine özel — saat saat örnek program)*
**[Sınav Hazırlık Stratejisi]:** *(Sınav Kaygısı verilerine özel — sınav öncesi, sınav anı, sınav sonrası)*
**[Ders Bazlı Öneriler]:** *(Zeka profili ve öğrenme stiline göre hangi derste nasıl çalışmalı)*

### 🧠 KİŞİSEL GELİŞİM PLANI

**[Duygusal Düzenleme]:** *(Kaygı yönetimi, stres altında davranış kalıplarını değiştirme)*
**[Sosyal Beceriler]:** *(Kişilik tipine uygun sosyal gelişim önerileri)*
**[Motivasyon ve Hedef]:** *(Kişilik tipine uygun motivasyon stratejileri)*

### 🧭 KARİYER YÖNELİMİ ÖN DEĞERLENDİRME

*(Holland RIASEC + Çoklu Zeka + Kişilik profili üçgeninden kariyer yönelimi analizi. En uygun 5 meslek alanı ve nedenleri. Dikkat: Bu bir kesin yönlendirme değil, ön değerlendirmedir.)*

---

### 👨‍👩‍👦 AİLE REHBERİ

> **✅ YAPIN:**
> *(En az 4 somut, uygulanabilir madde. Her madde kişilik ve test verilerine dayalı olmalı.)*

> **❌ YAPMAYIN:**
> *(En az 3 somut uyarı. Kişilik tipine göre hangi yaklaşımlar zarar verebilir?)*

### 👩‍🏫 ÖĞRETMEN REHBERİ

> **Sınıf İçi Stratejiler:**
> *(Bu öğrenci için sınıf ortamında ne yapılabilir? Öğrenme stili ve kişilik tipine özel 3-4 somut adım.)*

> **İletişim Önerileri:**
> *(Bu öğrenciyle nasıl iletişim kurulmalı? Kişilik tipine göre hangi yaklaşım etkili?)*

---

# 📌 SONUÇ ve ÖNCELİK SIRASI

*(Tüm analizin 5 maddelik özeti. En acil olandan başlayarak sırala. Her madde somut ve ölçülebilir olmalı.)*

1. **[EN ACİL]:** ...
2. **[ÖNCELİKLİ]:** ...
3. **[ÖNEMLİ]:** ...
4. **[TAKİP]:** ...
5. **[UZUN VADE]:** ...

---

*Dil: Türkçe. Üslup: Profesyonel, sıcak, yapıcı. Öğrenciyi yargılama, güçlendirmeye odaklan. Bu rapor resmi bir analiz belgesidir.*"""


def _get_test_specific_guidance(test_name):
    """Her test için özel analiz yönergesi döndürür."""

    if "Enneagram" in test_name:
        return """
### 🔬 ENNEAGRAM ÖZEL ANALİZ YÖNERGESİ (MUTLAKA UYGULA)

Bu test 9 kişilik tipini 0-100 ölçeğinde ölçer. Raporda şunları MUTLAKA yap:

**A. ANA TİP DERİN ANALİZİ:**
- Ana tipin temel motivasyonunu, korkusunu ve arzusunu öğrencinin yaşına uygun dille açıkla
- Ana tipin sağlıklı, ortalama ve sağlıksız düzeylerinden hangisinde olduğunu puan yüzdesine göre değerlendir
- Bu tipin okul ortamında nasıl göründüğünü somut örneklerle açıkla (sınıfta nasıl davranır, ödevlere nasıl yaklaşır, arkadaş ilişkileri nasıldır?)

**B. KANAT (WING) ANALİZİ:**
- Ana tipin yanındaki iki tipten (kanatlardan) hangisinin daha yüksek olduğunu bul
- Kanat kombinasyonunun (örn: 4w5, 7w8) kişiliğe kattığı nüansı açıkla
- Wing'in öğrenme stili üzerindeki etkisini tartış

**C. TRİTYPE İPUÇLARI (En yüksek 3 farklı merkez):**
- Kafa merkezinden (5,6,7) en yüksek puanlı tip
- Kalp merkezinden (2,3,4) en yüksek puanlı tip
- Karın merkezinden (8,9,1) en yüksek puanlı tip
- Bu üçlünün birlikte çizdiği profili yorumla

**D. STRES ve BÜYÜME DİNAMİĞİ:**
- Stres yönündeki tipe kayma belirtileri var mı? (düşük puan = kaymıyor, yüksek puan = kayma eğilimi)
- Büyüme yönündeki tipin puanı nedir? Bu, sağlıklı gelişim potansiyelini gösterir
- Stres altında bu öğrencinin hangi davranışları sergileyeceğini somut örneklerle açıkla

**E. 9 TİP PUAN HARİTASI:**
- Tüm tiplerin puanlarını sıralayarak "kişilik haritasının şeklini" yorumla
- Yüksek puanlar kümeleniyor mu? (Örn: 2-3-7 yüksek → sosyal, enerjik profil)
- Düşük puanlı tipler neyi gösteriyor? (Baskılanan yönler)
- İkincil ve üçüncül güçlü tiplerin ana tiple etkileşimini analiz et

**F. AKADEMİK VE SOSYAL ETKİ:**
- Bu kişilik tipinin ders çalışma alışkanlıkları
- Sınav kaygısı ile ilişkisi
- Öğretmen ve akranlarla iletişim tarzı
- Motivasyon kaynakları ve öğrenme engelleri

**G. KİŞİSEL GELİŞİM YOLU:**
- Bu tipin büyüme yolundaki 5 somut adım (yaşa uygun)
- Kaçınması gereken tuzaklar
- Ailesi ve öğretmeni bu tipte bir çocukla nasıl iletişim kurmalı?
"""

    elif "Çalışma Davranışı" in test_name:
        return """
### 🔬 ÇALIŞMA DAVRANIŞI ÖZEL ANALİZ YÖNERGESİ

Bu test 7 alt kategoride (A-G) ders çalışma alışkanlıklarını ölçer:
- A: Motivasyon ve Ders Çalışmaya Karşı Tutum
- B: Zaman Yönetimi
- C: Derse Hazırlık ve Katılım
- D: Okuma ve Not Tutma Alışkanlıkları
- E: Yazılı Anlatım ve Ödev Yapma
- F: Sınava Hazırlanma
- G: Genel Çalışma Koşulları ve Alışkanlıkları

**Raporda:**
- Her kategoriyi ayrı ayrı yorumla ve birbiriyle ilişkilendir
- "Zayıf zaman yönetimi + güçlü motivasyon" gibi çelişkilerin nedenlerini tartış
- Bir günlük ideal çalışma programı taslağı oluştur
- Fiziksel çalışma ortamı önerileri ver (masa düzeni, ışık, ses)
- Haftalık ve sınav dönemi planlaması öner
"""

    elif "Sağ-Sol Beyin" in test_name:
        return """
### 🔬 SAĞ-SOL BEYİN ÖZEL ANALİZ YÖNERGESİ

Bu test beyin yarım küre baskınlığını (sağ/sol yüzde + dominanslık seviyesi) ölçer.

**Raporda:**
- Baskın tarafın öğrenme stili üzerindeki etkisini detaylandır
- Denge durumunu analiz et (güçlü baskınlık vs. dengeli)
- Her ders için beyin baskınlığına uygun çalışma stratejileri öner
- Sol baskınsa: analitik, sıralı, mantıksal çalışma yöntemleri
- Sağ baskınsa: görsel, bütüncül, yaratıcı çalışma yöntemleri
- Dengeliyse: hibrit stratejiler ve avantajları
- Sınıf içi oturma düzeni ve ders dinleme stratejileri öner
"""

    elif "Sınav Kaygısı" in test_name:
        return """
### 🔬 SINAV KAYGISI ÖZEL ANALİZ YÖNERGESİ

Bu test 7 alt boyutta sınav kaygısını ölçer:
- Başkalarının Görüşü Kaygısı
- Kendi Hakkındaki Görüşü
- Gelecek Endişesi
- Hazırlık Endişesi
- Bedensel Tepkiler
- Zihinsel Tepkiler
- Genel Kaygı

**Raporda:**
- Her alt boyutu ayrı ayrı derinlemesine yorumla
- Kaygının kaynağını tespit et: performans mı, hazırlık mı, sosyal baskı mı, gelecek korkusu mu?
- Bedensel ve zihinsel tepkilerin birbirleriyle ilişkisini analiz et
- Kaygı döngüsünü açıkla (kaygı → düşük performans → daha fazla kaygı)
- Sınav öncesi (1 hafta, 1 gün, 1 saat) aşamalı rahatlama planı öner
- Sınav anı stratejileri (nefes teknikleri, bilişsel yeniden yapılandırma)
- Sınav sonrası değerlendirme yaklaşımı
- Aileye özel: baskı yapmadan nasıl destek olunur
"""

    elif "VARK" in test_name:
        return """
### 🔬 VARK ÖZEL ANALİZ YÖNERGESİ

Bu test 4 öğrenme stilini (V-Görsel, A-İşitsel, R-Okuma/Yazma, K-Kinestetik) ölçer.

**Raporda:**
- Baskın stil(ler)i ve multimodal durumu detaylandır
- Her stil için somut ders çalışma teknikleri öner (araç, yöntem, ortam)
- Zayıf stilleri güçlendirme stratejileri
- Her ders için (Matematik, Fen, Türkçe, Sosyal, Yabancı Dil) stile uygun çalışma rehberi
- Sınıfta öğretmenin kullanabileceği stile uygun öğretim yöntemleri
- Dijital araç ve uygulama önerileri (yaşa uygun)
"""

    elif "Çoklu Zeka" in test_name:
        return """
### 🔬 ÇOKLU ZEKA ÖZEL ANALİZ YÖNERGESİ

Bu test Gardner'ın 8 zeka alanını (%0-100) ölçer:
Sözel-Dilsel, Mantıksal-Matematiksel, Görsel-Uzamsal, Bedensel-Kinestetik,
Müzikal-Ritmik, Kişilerarası (Sosyal), İçsel (Özedönük), Doğacı.

**Raporda:**
- En güçlü 3 zeka alanının birbirleriyle etkileşimini açıkla
- "Zeka profili tipi" belirle: uzmanlaşmış (1-2 zirve), çok yönlü (3-4 yüksek), dengeli
- Her güçlü zeka alanı için somut kariyer alanları öner
- Zayıf alanların güçlü alanlarla telafi stratejilerini açıkla
- Okul dersleriyle zeka alanlarını eşleştir
- Ders dışı aktivite ve hobi önerileri
"""

    elif "Holland" in test_name:
        return """
### 🔬 HOLLAND RIASEC ÖZEL ANALİZ YÖNERGESİ

Bu test 6 mesleki ilgi tipini ölçer (her biri 0-28 puan):
R-Gerçekçi, I-Araştırmacı, A-Sanatçı, S-Sosyal, E-Girişimci, C-Geleneksel.

**Raporda:**
- 3 harfli Holland kodunu (en yüksek 3 tip) derinlemesine açıkla
- Holland altıgenindeki konumlandırmayı açıkla (bitişik tipler uyumlu, karşıt tipler çelişkili)
- Her yüksek tip için en az 5 somut meslek önerisi
- Holland kodu kombinasyonuna uygun 10 kariyer yolu
- Türkiye iş piyasasına uygun bölüm ve fakülte önerileri
- Lise alan seçimi (Sayısal, Eşit Ağırlık, Sözel, Dil) tavsiyesi
- Kariyer keşfi için somut adımlar (staj, gönüllülük, gölgeleme)
"""

    return ""


def build_single_test_prompt(student_name, student_age, student_gender, test_name, test_data):
    """Tekil test analizi için kapsamlı prompt — her teste özel rehber içerir."""

    test_guidance = _get_test_specific_guidance(test_name)

    return f"""Sen, Türkiye'de 15+ yıl deneyime sahip bir eğitim psikoloğu ve psikometri uzmanısın. 
Tek bir psikolojik test sonucunu klinik düzeyde derinlemesine analiz ediyorsun.
Raporun, velilere ve öğretmenlere sunulacak profesyonel bir analiz belgesidir.

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
2. **KANIT ZORUNLU:** Her güçlü/zayıf yön için parantez içinde puanı yaz. Örn: "Görsel zeka güçlü (%78)"
3. **PUAN YORUMLAMA STANDARDI:**
   - %0-30 → "Gelişime çok açık"
   - %31-50 → "Ortalama altı, geliştirilebilir"
   - %51-70 → "Ortalama / dengeli"
   - %71-85 → "Güçlü"
   - %86-100 → "Çok güçlü / baskın"
4. **TIBBİ TANI YASAĞI:** Klinik tanı terimleri (DEHB, depresyon, disleksi vb.) kesinlikle kullanma.
5. **YAŞA UYGUN TAVSİYE:** {student_age} yaşındaki bir öğrenci için somut, gerçekçi öneriler ver.
6. **KAPSAMLI OL:** Bu rapor resmi bir analiz belgesidir. Yüzeysel değil, derinlemesine analiz yap. Minimum 1500 kelime.

---
{test_guidance}
---

## 📝 RAPOR FORMATI (Bu formatı AYNEN KORU, bölüm atlama)

### 1. 📊 TEST ÖZETİ

**Tek Cümle Sonuç:** *(Testin en önemli bulgusu, net ve doğrudan — öğrenciyi tanımayan birinin bile anlayacağı şekilde.)*

**Görsel Özet (tüm boyutlar/kategoriler için):**
```
[Boyut/Kategori Adı] : ████████░░ XX%  → Yorum
[Boyut/Kategori Adı] : ██████░░░░ XX%  → Yorum
[Boyut/Kategori Adı] : ████░░░░░░ XX%  → Yorum
...
```
*(Tüm alt boyutları/kategorileri listele, hiçbirini atlama. Her birinin yanına kısa yorum ekle.)*

---

### 2. 🧠 DERİN YORUM

*(Bu kısımda "NEDEN?" ve "NE ANLAMA GELİYOR?" sorularına cevap ver.
Puanların günlük hayata, okul yaşamına ve sosyal ilişkilere etkisini somut örneklerle açıkla.
En az 4-5 paragraf, akıcı ve derinlemesine anlatım. 
Alt boyutları birbirleriyle ilişkilendir, örüntüleri tespit et.
Öğrencinin bu profile sahip olmasının olası nedenlerini tartış.)*

---

### 3. 💪 KANITA DAYALI GÜÇLÜ YÖNLER

| # | Güçlü Yön | Kanıt (Puan) | Okul Hayatına Yansıması | Nasıl Daha da Güçlendirilebilir? |
|---|-----------|--------------|------------------------|--------------------------------|
| 1 | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... |
| 4 | ... | ... | ... | ... |

*(En az 4 satır doldur.)*

---

### 4. 🌱 GELİŞİM ALANLARI

| # | Alan | Mevcut Durum (Puan) | Neden Önemli? | Somut Gelişim Stratejisi |
|---|------|---------------------|---------------|------------------------|
| 1 | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... |

*(En az 3 satır doldur. Her gelişim alanı için somut, adım adım strateji yaz.)*

---

### 5. 🎯 KAPSAMLI AKSİYON PLANI

**📌 TAVSİYE 1: [Başlık]**
- **Ne yapılacak:** *(Somut açıklama)*
- **Ne zaman:** *(Günlük/haftalık program)*
- **Nasıl ölçülecek:** *(Başarı göstergesi)*
- **Kim sorumlu:** *(Öğrenci/Öğretmen/Aile)*

**📌 TAVSİYE 2: [Başlık]**
- **Ne yapılacak:** ...
- **Ne zaman:** ...
- **Nasıl ölçülecek:** ...
- **Kim sorumlu:** ...

**📌 TAVSİYE 3: [Başlık]**
- **Ne yapılacak:** ...
- **Ne zaman:** ...
- **Nasıl ölçülecek:** ...
- **Kim sorumlu:** ...

**📌 TAVSİYE 4: [Başlık]**
- **Ne yapılacak:** ...
- **Ne zaman:** ...
- **Nasıl ölçülecek:** ...
- **Kim sorumlu:** ...

**📌 TAVSİYE 5: [Başlık]**
- **Ne yapılacak:** ...
- **Ne zaman:** ...
- **Nasıl ölçülecek:** ...
- **Kim sorumlu:** ...

---

### 6. 👨‍👩‍👦 AİLE REHBERİ

> **Bu test sonuçlarına göre ailenin bilmesi gerekenler:**
> *(Test sonuçlarının ne anlama geldiğini aile diline çevir — teknik terim kullanma. 
> En az 4 somut yapılması gereken ve 3 kaçınılması gereken davranış.)*

---

### 7. 👩‍🏫 ÖĞRETMEN REHBERİ

> **Sınıf İçi Stratejiler:** *(En az 3 somut adım)*
> **İletişim Önerileri:** *(Bu öğrenciyle nasıl konuşulmalı?)*
> **Dikkat Edilmesi Gerekenler:** *(Gözden kaçırılmaması gereken işaretler)*

---

### 8. 📌 SONUÇ

*(3-4 cümlelik kapanış. En kritik bulguyu vurgula, umut verici bir mesajla bitir. 
Bir sonraki adımın ne olması gerektiğini belirt.)*

---

*Dil: Türkçe. Üslup: Profesyonel, sıcak, yapıcı. Bu rapor resmi bir analiz belgesidir. Öğrenciyi yargılama, güçlendirmeye odaklan.*"""


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
