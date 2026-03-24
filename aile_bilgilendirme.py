"""
Aile Bilgilendirme Modulu — Egitim Check-Up
============================================
Ogretmenin AI analiz raporundan aileye yonelik ozet olusturmasini saglar.
- Prompt builder (Claude API icin)
- Konu basligi / test eslemesi
- UI bilesenleri
"""

import json

# ============================================================
# KONU BASLIKLARI VE TEST ESLEMESI
# ============================================================

ALL_TOPICS = [
    "Genel Degerlendirme",
    "Ogrenme Stili ve Tercihleri",
    "Guclu Yonler",
    "Gelisim Alanlari",
    "Motivasyon ve Ilgi Alanlari",
    "Calisma Aliskanliklari",
    "Sinav Kaygisi Durumu",
    "Dikkat ve Odaklanma",
    "Sosyal-Duygusal Gelisim",
    "Kariyer Yonelimleri",
    "Evde Yapilabilecek Destekler",
    "Profesyonel Destek Onerileri",
]

# Her zaman aktif olan basliklar
ALWAYS_ACTIVE = {
    "Genel Degerlendirme",
    "Guclu Yonler",
    "Gelisim Alanlari",
    "Evde Yapilabilecek Destekler",
    "Profesyonel Destek Onerileri",
    "Motivasyon ve Ilgi Alanlari",
    "Sosyal-Duygusal Gelisim",
}

# Teste bagli basliklar — hangi test(ler) yapildiysa aktif olur
TOPIC_TEST_MAP = {
    "Sinav Kaygisi Durumu": ["Sinav Kaygisi Olcegi"],
    "Dikkat ve Odaklanma": ["P2 Dikkat Testi"],
    "Kariyer Yonelimleri": ["Holland Mesleki Ilgi Envanteri"],
    "Ogrenme Stili ve Tercihleri": [
        "VARK Ogrenme Stilleri Testi",
        "Coklu Zeka Testi",
        "Sag-Sol Beyin Dominansi Testi",
    ],
    "Calisma Aliskanliklari": ["Calisma Davranisi Olcegi"],
}


def get_available_topics(test_names):
    """
    Yapilan testlere gore aktif konu basliklarini belirler.
    Donus: [(baslik, aktif_mi), ...]
    """
    result = []
    for topic in ALL_TOPICS:
        if topic in ALWAYS_ACTIVE:
            result.append((topic, True))
        elif topic in TOPIC_TEST_MAP:
            required_tests = TOPIC_TEST_MAP[topic]
            is_active = any(
                _test_name_matches(t, required_tests) for t in test_names
            )
            result.append((topic, is_active))
        else:
            result.append((topic, True))
    return result


def _test_name_matches(test_name, required_list):
    """Test adinin gerekli listede olup olmadigini esnek sekilde kontrol eder."""
    test_lower = test_name.lower()
    for req in required_list:
        req_lower = req.lower()
        # Tam eslesme veya icerik eslesmesi
        if req_lower in test_lower or test_lower in req_lower:
            return True
        # Anahtar kelime eslesmesi
        req_words = req_lower.split()
        if all(w in test_lower for w in req_words if len(w) > 3):
            return True
    return False


# ============================================================
# CLAUDE API PROMPT SABLONU
# ============================================================

def build_family_summary_prompt(student_name, student_age, student_gender,
                                selected_topics, teacher_note,
                                analysis_report, test_names, student_grade=None):
    """Aile bilgilendirme ozeti icin Claude API prompt'u olusturur."""
    grade_text = f", {student_grade}. sinif ogrencisi" if student_grade else ""

    topics_text = "\n".join(f"- {t}" for t in selected_topics)
    tests_text = ", ".join(test_names) if test_names else "Belirtilmemis"

    prompt = f"""Sen deneyimli bir egitim psikologusun. Asagida bir ogrencinin
psikometrik test analiz raporu var. Bu rapora dayanarak, ogretmenin sectigi
konu basliklari icin AILEYE YONELIK bir bilgilendirme ozeti hazirla.

## YAZIM KURALLARI — COK ONEMLI:
- Yalin, sade ve akici Turkce kullan — karmasik cumlelerden kacin
- Teknik psikolojik terim kullanma; kullanirsan parantez icinde anlasilir sekilde acikla
- Aileyi yargilamayan, destekleyici ve umut verici bir ton kullan
- Her konu basligi 4-6 cumle olsun — kisa ve oz, ama icerikli
- Somut, uygulanabilir tavsiyeler ver (soyut kalma)
- "Cocugunuz" yerine ogrencinin adini ({student_name}) kullan
- Olumsuzmluklari "gelisim alani" olarak cercevele — asla "zayif", "basarisiz", "yetersiz" gibi kelimeler kullanma
- Her basligin sonunda "Pratik Oneri:" altinda 1-2 somut, bugun uygulanabilir oneri ekle
- Rapor bir A4 sayfayi gecmesin — oz ve etkili ol
- Samimi ama profesyonel bir dil kullan, sanki veli toplantisinda konusuyormuzsun gibi

## OGRENCI BILGILERI:
- Ad: {student_name}
- Yas: {student_age}
- Cinsiyet: {student_gender}{grade_text}

## YAPILAN TESTLER:
{tests_text}

## AI ANALIZ RAPORU (kaynak veri):
{analysis_report}

## OGRETMEN TARAFINDAN SECILEN KONU BASLIKLARI:
{topics_text}

## OGRETMENIN EK NOTU:
{teacher_note if teacher_note else "Ogretmen ek not eklememistir."}

## CIKTI FORMATI:
Her secilen konu basligi icin:

### [Baslik Emoji] [Konu Basligi]
[4-6 cumlelik yalin, akici Turkce ozet]

**Pratik Oneri:** [1-2 somut oneri]

---

Son olarak, saygili bir kapanis paragrafi yaz:
"Bu ozet, {student_name}'in psikometrik degerlendirme sonuclarina dayanmaktadir.
Daha detayli bilgi icin ogretmeninizle gorusmenizi oneririz."
"""
    return prompt
