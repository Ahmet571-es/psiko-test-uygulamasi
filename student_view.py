import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import time
from db_utils import check_test_completed, save_test_result_to_db

# --- API VE AYARLAR ---
load_dotenv()
if "GROK_API_KEY" in st.secrets:
    GROK_API_KEY = st.secrets["GROK_API_KEY"]
else:
    GROK_API_KEY = os.getenv("GROK_API_KEY")

client = OpenAI(api_key=GROK_API_KEY, base_url="https://api.x.ai/v1")

# --- FAZ SİSTEMİ TEST LİSTELERİ ---
# Öğrenci giriş sayısına göre bu listelerden birini görecek.
PHASE_1_TESTS = [
    "Enneagram Kişilik Testi",
    "Çalışma Davranışı Ölçeği (Baltaş)",
    "Sağ-Sol Beyin Dominansı Testi"
]

PHASE_2_TESTS = [
    "Sınav Kaygısı Ölçeği (DuSKÖ)",
    "VARK Öğrenme Stilleri Testi"
]

PHASE_3_TESTS = [
    "Çoklu Zeka Testi (Gardner)",
    "Holland Mesleki İlgi Envanteri (RIASEC)"
]

# --- PROMPTLAR ---
SORU_URETIM_PROMPT = """
Sen dünyanın en iyi Türk psikometrik test tasarımcısı, çocuk/ergen psikolojisi uzmanı ve ölçme-değerlendirme otoritesisin.

GÖREV: Sadece belirtilen test için, orijinal testin soru sayısı, yapısı ve ölçek tipine %100 sadık kalarak, tamamen özgün, yeni ve benzersiz sorular üret.

ZORUNLU GENEL KURALLAR (ASLA İHLAL ETME):
- Tüm sorular kusursuz, akıcı ve doğal Türkçe olsun. Cümleler kısa, net ve sade olsun.
- Ortaokul-lise öğrencisinin rahatça anlayabileceği dil kullan; karmaşık kelimelerden kaçın.
- Sorular tamamen tarafsız, objektif ve yargısız olsun. Hiçbir yönlendirme, duygu yüklemesi veya değer yargısı içermesin.
- Her soru, psikolojik derinlik taşıyarak üst düzey analizlere olanak tanısın ama anlaşılırlığı asla feda etme.
- Tüm sorular 5'li Likert ölçeğine mükemmel uyumlu olsun: Kesinlikle Katılmıyorum (1) - Katılmıyorum (2) - Kararsızım (3) - Katılıyorum (4) - Kesinlikle Katılıyorum (5).
- Aynı veya benzer ifadeler ASLA tekrarlanmasın. Maksimum çeşitlilik sağla.
- Çıktıda kesinlikle başka hiçbir metin, açıklama, başlık, markdown veya ek bilgi yazma. Sadece geçerli JSON üret.

TESTLERE ÖZGÜ ZORUNLU KURALLAR:
- Çoklu Zeka Testi (Gardner): Tam 80 soru üret. 8 zeka alanı için tam 10'ar soru: Sözel, Mantıksal, Görsel, Müziksel, Bedensel, Sosyal, İçsel, Doğacı. Her soruya ilgili "area" alanı ekle.
- Holland Mesleki İlgi Envanteri (RIASEC): Tam 90 soru üret. 6 tip için tam 15'er soru: Gerçekçi, Araştırmacı, Yaratıcı, Sosyal, Girişimci, Düzenli. Her soruya ilgili "area" alanı ekle.
- VARK Öğrenme Stilleri Testi: Tam 16 soru üret. Orijinal VARK tarzında.
- Sağ-Sol Beyin Dominansı Testi: Tam 30 soru üret. 15 sol beyin + 15 sağ beyin özelliği.
- Çalışma Davranışı Ölçeği (Baltaş): Tam 73 soru üret.
- Sınav Kaygısı Ölçeği (DuSKÖ): Tam 50 soru üret.

JSON ÇIKTI FORMATI (KESİNLİKLE BU ŞEKİLDE OLSUN):
{{
  "type": "likert",
  "questions": [
    {{"id": 1, "text": "Soru metni burada"}} 
  ]
}}

Sadece istenen test için soru üret. Çıktı %100 geçerli JSON olsun.
Test adı: {test_adi}
"""

TEK_RAPOR_PROMPT = """
Sen dünyanın en iyi psikometrik test analizi ve yorumlama uzmanısın. Çocuk/ergen psikolojisi konusunda çok deneyimlisin.

GÖREV: Sadece verilen JSON verilerine dayanarak test sonucunu analiz et. 
ASLA genel geçer bilgi ekleme. Sadece kullanıcının verilerinden yola çık.

Rapor tamamen tarafsız, nesnel ve yargısız olsun. 
Dil ÇOK sade, yalın ve herkesin anlayabileceği bir Türkçe olsun. Ortaokul öğrencisi bile rahatça okuyabilsin.
Bol grafiksel betimleme kullan (Sözel olarak grafiği anlat, görsel değil).

Test adı: {test_adi}
Veriler: {cevaplar_json}

ZORUNLU RAPOR FORMATI:
1. **Genel Değerlendirme**
2. **Detaylı Puan Dağılımı** (Sayısal veriler)
3. **Baskın Özellikler ve Güçlü Yönler**
4. **Gelişim Alanları ve Potansiyel Zorluklar**
5. **Günlük Hayat Yansımaları** (Okul, ev, arkadaşlık)
6. **Pratik Öneriler** (Hemen uygulanabilir adımlar)
7. **Sonuç Özeti ve Motivasyon**

Çıktı sadece bu başlıklarla yapılandırılmış metin olsun.
"""

# --- SABİT ENNEAGRAM VERİLERİ (HIZ VE GÜVENLİK İÇİN LOKAL) ---
ENNEAGRAM_QUESTIONS = {
    1: [
        "Kendimi hata yaptığımda çok eleştiririm.", "Doğru ve yanlış konusunda güçlü bir içgüdüm vardır.",
        "Mükemmellik için çok çaba gösteririm.", "Disiplinli ve adil davranmaktan gurur duyarım.",
        "Kişisel bütünlük benim için çok önemlidir.", "Genellikle mantıklı düşünürüm, duygusal değilim.",
        "Çok ciddi olabilirim ve eğlenmeyi unuturum.", "Kendimi en çok ben eleştiririm.",
        "Bir şeyin yanlış olduğunu hemen fark ederim.", "İşlerimi mükemmel yapmaya çalışırım.",
        "Düzenli ve dakik olmayı çok önemserim.", "Ahlak kuralları benim için çok değerlidir.",
        "Sorunları ve eksikleri çabuk görürüm.", "Detayların doğru olmasını isterim.",
        "Stresli zamanlarda katı ve talepkar olurum.", "Rahatken daha anlayışlı ve kabul edici olurum.",
        "Başkaları tarafından yanlış anlaşılmaktan korkarım.", "Affetmek bana zor gelir.",
        "Her şeyi siyah-beyaz görürüm, gri alanları kabul etmekte zorlanırım.", "Yanlış olduğumu kabul etmek bana zor gelir."
    ],
    2: [
        "İlişkiler hayatımın en önemli parçasıdır.", "Başkalarına yardım etmekten ve onları mutlu etmekten keyif alırım.",
        "Hayır demek bana zor gelir.", "Vermek bana almaktan daha kolay gelir.",
        "İnsanlarla yakın olmak isterim.", "Başkalarının bana ihtiyaç duymasını severim.",
        "Dışa dönük ve sıcakkanlı bir yapım vardır.", "Olumsuz duygularımı pek göstermem.",
        "Takdir edilmek beni çok motive eder.", "Başkalarının bana bağımlı olmasını severim.",
        "Sevdiğimi söylemek ve duymak benim için önemlidir.", "İnsanlar bana sorunlarını rahatça anlatır.",
        "İlişkilerimi korumak için çok çaba gösteririm.", "Stresli zamanlarda talepkar olurum.",
        "Rahatken sevgi dolu ve destekleyici olurum.", "İnsanları kolayca severim.",
        "Takdir görmediğimde üzülürüm.", "Yardım ederken kendimi iyi hissederim.",
        "Sevilmek ve bağlantı kurmak benim için önemlidir.", "Endişelendiğimde fazla fedakar olurum."
    ],
    3: [
        "Kendimi iyi tanıtır ve pazarlarım.", "Birden fazla işi aynı anda yapmayı severim.",
        "Başarılı olmayı ve öne çıkmayı isterim.", "Çalışmak ve üretken olmak benim için önemlidir.",
        "Hedeflerime odaklanırım.", "İyi görünmeye ve iyi izlenim bırakmaya önem veririm.",
        "Rekabetten önce harekete geçmeyi tercih ederim.", "İnsanlarla birlikte olmayı severim.",
        "En etkili yolu bulmakta iyiyim.", "Bazen fazla söz veririm.",
        "Duygularımı pek göstermem.", "Rekabet etmek beni motive eder.",
        "Kariyerimde zirveye çıkmayı isterim.", "Stresli zamanlarda kendimi fazla överim.",
        "Rahatken dürüst ve çekici olurum.", "Olumsuz duyguları işe engel görürüm.",
        "Yeni durumlara kolay uyum sağlarım.", "Başarılı insanları desteklerim.",
        "En iyisi olmaya çalışırım.", "Başarı ile motive olurum."
    ],
    4: [
        "Yaratıcı bir yapım vardır.", "Kendimi başkalarından farklı hissederim.",
        "Melankolik ruh hallerim olur.", "Çok hassas bir insanım.",
        "Hayatımda bir şey eksikmiş gibi hissederim.", "Başkalarının başarılarına kıskançlık duyabilirim.",
        "Yaratıcılığımı ifade etmekten hoşlanırım.", "Yanlış anlaşıldığımda içe kapanırım.",
        "Romantik bir yapım vardır.", "Hayal kurmayı severim.",
        "Benzersiz şeylere sahip olmayı isterim.", "Yoğun deneyimlere çekilirim.",
        "Stresli zamanlarda huysuz olurum.", "Rahatken şefkatli ve destekleyici olurum.",
        "Eleştiriye çok duyarlıyım.", "Hayatın anlamını düşünürüm.",
        "Sıradan olmaktan kaçınırım.", "İyi zevklere önem veririm.",
        "Bazen dramatik davranırım.", "Duyguları anlamayı önemli bulurum."
    ],
    5: [
        "Duygusal ortamlardan rahatsız olurum.", "Analiz yapmakta ve araştırmakta iyiyim.",
        "İçe dönük ve utangaç olabilirim.", "Fikirlerimi duygulardan daha kolay ifade ederim.",
        "Konuşmadan önce düşünürüm.", "Çatışmalardan kaçınırım.",
        "Yalnız çalışmaktan zevk alırım.", "Eleştiriye duyarlıyım ama göstermem.",
        "Bağımsız olmayı severim.", "Özel hayatımı paylaşmayı pek sevmem.",
        "Düşüncelerim karmaşık olabilir.", "Zamanımı ve alanımı kontrol etmek isterim.",
        "Bilgisiz davranışlardan rahatsız olurum.", "Her konuda fikrim vardır.",
        "Benzer ilgi alanları olan insanlarla sosyalleşirim.", "Stresli zamanlarda mesafeli olurum.",
        "Rahatken objektif ve içgörülü olurum.", "Entellektüel tartışmalara girebilirim.",
        "Yalnız çalışmayı tercih ederim.", "Kararları mantıkla alırım."
    ],
    6: [
        "Sorumluluk bilincim yüksektir.", "Her ihtimale hazırlıklı olmaya çalışırım.",
        "Başkalarının niyetlerinden şüphe ederim.", "Karar vermekte zorlanırım.",
        "Güvenlik benim için önemlidir.", "Kendi kararlarımdan şüphe duyarım.",
        "Gruba ait olmayı önemserim.", "Her şeyin yoluna gireceğine inanırım ama endişelenirim.",
        "Aile ve arkadaşlarım bana destek olur.", "Küçük sorunlara fazla tepki verebilirim.",
        "Yeni insanlara hemen güvenmem.", "Tehlikeleri önceden fark ederim.",
        "Stresli zamanlarda kaygılı olurum.", "Rahatken sıcak ve sadık olurum.",
        "Kaygılı olduğumda kontrolcü olurum.", "Rahatken dostça davranırım.",
        "İlişkilerde bağlılığa güvenmekte zorlanırım.", "Korkumu yenmek için çaba gösteririm.",
        "Çoğu insandan daha fazla endişelenirim.", "Güvenlik ve destekle motive olurum."
    ],
    7: [
        "Hayattan keyif almayı önemserim.", "Neşeli ve konuşkan bir yapım vardır.",
        "Seçeneklerimi açık tutmayı severim.", "Çok arkadaşım vardır.",
        "Yeni ve heyecan verici şeyler severim.", "İyimser bir insanım.",
        "Eğlendirmeyi ve güldürmeyi severim.", "Çok enerjik olabilirim.",
        "Farklı şeyler denemekten hoşlanırım.", "Sıkılmaktan nefret ederim.",
        "Aşırıya kaçabilirim.", "Kısıtlanmaktan rahatsız olurum.",
        "Stresli zamanlarda disiplinsiz olurum.", "Rahatken eğlenceli ve hayalperest olurum.",
        "Sevdiğim işte çok üretken olurum.", "Acıdan kaçınırım.",
        "Yeterli zaman olmaması beni üzür.", "Olumsuz insanlardan hoşlanmam.",
        "Planları hemen uygulamak isterim.", "Heyecan ve mutlulukla motive olurum."
    ],
    8: [
        "İstediklerim için mücadele ederim.", "Cesur ve lider bir yapım vardır.",
        "Bağımsız ve güçlü olmayı severim.", "Kararsız insanlardan sabırsızlanırım.",
        "Rekabet etmeyi ve kazanmayı severim.", "Sevdiklerimi korurum.",
        "Kontrolü elimde tutmayı severim.", "Güven kazanmak gerekir.",
        "Risk almaktan hoşlanırım.", "Sıkı çalışırım.",
        "Meydan okumayı severim.", "Saygı duyulmayı tercih ederim.",
        "Grupta liderlik yaparım.", "Doğrudan konuşurum.",
        "Stresli zamanlarda kontrolcü olurum.", "Rahatken enerjik ve yardımcı olurum.",
        "Duygularımı pek göstermem.", "Güvendiğimde hassas olurum.",
        "Eğlenceye düşkün olabilirim.", "Kendimi korumakla motive olurum."
    ],
    9: [
        "Çatışmadan kaçınırım.", "Rahat ve iyimser bir yapım vardır.",
        "İyi bir dinleyiciyim.", "Ertelemeye meyilliyim.",
        "Rutinlerden hoşlanırım.", "Karar vermekte zorlanırım.",
        "Yapı ve rutin bana yardımcı olur.", "Detayları unutabilirim.",
        "Öfkemi pek göstermem.", "Dinlenmeyi severim.",
        "Evde vakit geçirmekten hoşlanırım.", "Uyum ararım.",
        "Dırdır edilmekten hoşlanmam.", "Önemsiz işlerle oyalanırım.",
        "Stresli zamanlarda inatçı olurum.", "Rahatken sabırlı ve açık fikirli olurum.",
        "Başkalarını memnun etmeye çalışırım.", "Çok karar vermek beni yorar.",
        "Herkesle iyi geçinirim.", "Huzur ve uyumla motive olurum."
    ]
}

ENNEAGRAM_DATA = {
    1: {"title": "Tip 1: Reformcu", "role": "Mükemmeliyetçi, Düzenleyici", "fear": "Hata yapmak, yozlaşmak.", "desire": "Doğruyu yapmak.", "stress": 4, "growth": 7, "desc": "Dünyayı düzeltmeye çalışan idealist.", "strengths": ["Disiplinli", "Adil", "Etik"], "weaknesses": ["Yargılayıcı", "Esnek olmayan"], "work_style": "Yapılandırılmış, net kuralları olan işler.", "relationship_style": "Dürüstlük ve sadakat ararsın.", "danger_signals": ["Sürekli düzeltme ihtiyacı.", "Öfkeyi bastırma."], "prescription": ["Hata Yapma İzni ver.", "Gri Alanları gör."]},
    2: {"title": "Tip 2: Yardımcı", "role": "Şefkatli, İlgi Gösteren", "fear": "Sevilmemek.", "desire": "İhtiyaç duyulmak.", "stress": 8, "growth": 4, "desc": "Başkalarını önceleyen fedakar.", "strengths": ["Empatik", "Cömert"], "weaknesses": ["Hayır diyememek", "Alınganlık"], "work_style": "İnsan odaklı işler.", "relationship_style": "Partnerinin ihtiyaçlarını sezersin.", "danger_signals": ["Tükenmişlik."], "prescription": ["Hayır demeyi öğren.", "Kendi ihtiyaçlarını sor."]},
    3: {"title": "Tip 3: Başarılı", "role": "Odaklı, Performansçı", "fear": "Başarısızlık.", "desire": "Değerli hissetmek.", "stress": 9, "growth": 6, "desc": "Başarı odaklı, hedef insanı.", "strengths": ["Verimli", "Motive edici"], "weaknesses": ["İşkoliklik", "Rekabetçilik"], "work_style": "Hedef odaklı, yükselme şansı olan işler.", "relationship_style": "İlişkiyi proje gibi görme riski.", "danger_signals": ["Duyguları hissetmemek."], "prescription": ["Durma egzersizi yap.", "Maskesiz ol."]},
    4: {"title": "Tip 4: Bireyci", "role": "Romantik, Özgün", "fear": "Sıradan olmak.", "desire": "Eşsiz olmak.", "stress": 2, "growth": 1, "desc": "Derin duyguları olan hassas kişi.", "strengths": ["Yaratıcı", "Otantik"], "weaknesses": ["Melankoli", "Kıskançlık"], "work_style": "Yaratıcı, rutin olmayan işler.", "relationship_style": "Derin ve tutkulu bağ ararsın.", "danger_signals": ["Depresif ruh hali."], "prescription": ["Rutin oluştur.", "Bedenle bağ kur."]},
    5: {"title": "Tip 5: Araştırmacı", "role": "Gözlemci, Uzman", "fear": "Yetersiz olmak.", "desire": "Dünyayı anlamak.", "stress": 7, "growth": 8, "desc": "Enerjisini koruyan zihin insanı.", "strengths": ["Analitik", "Objektif"], "weaknesses": ["İzolasyon", "Duygusal kopukluk"], "work_style": "Uzmanlık gerektiren, bağımsız işler.", "relationship_style": "Bağımsızlığa saygı beklersin.", "danger_signals": ["İnsanlardan kopmak."], "prescription": ["Eyleme geç.", "Duygusal risk al."]},
    6: {"title": "Tip 6: Sadık", "role": "Sorgulayıcı, Güvenilir", "fear": "Güvensiz kalmak.", "desire": "Güvende olmak.", "stress": 3, "growth": 9, "desc": "Her senaryoyu düşünen sadık kişi.", "strengths": ["Sorumlu", "Sadık"], "weaknesses": ["Aşırı kaygı", "Kararsızlık"], "work_style": "Risk analizi yapılan güvenli ortamlar.", "relationship_style": "Güven her şeydir.", "danger_signals": ["Sürekli kötü senaryo düşünmek."], "prescription": ["Düşünceyi durdur.", "İçgüdüne güven."]},
    7: {"title": "Tip 7: Hevesli", "role": "Maceracı, Vizyoner", "fear": "Acı çekmek.", "desire": "Mutlu olmak.", "stress": 1, "growth": 5, "desc": "Hazza koşan, enerjik kişi.", "strengths": ["İyimser", "Hızlı öğrenen"], "weaknesses": ["Odaklanma sorunu", "Sözünü tutamama"], "work_style": "Çeşitlilik sunan hızlı işler.", "relationship_style": "Eğlenceli ve spontane.", "danger_signals": ["Projeleri bitirememek."], "prescription": ["Bir işi bitir.", "Negatif duyguda kalmayı dene."]},
    8: {"title": "Tip 8: Meydan Okuyan", "role": "Lider, Koruyucu", "fear": "Kontrol edilmek.", "desire": "Kontrol etmek.", "stress": 5, "growth": 2, "desc": "Güçlü, iradeli doğal lider.", "strengths": ["Cesur", "Adil"], "weaknesses": ["Baskıcı", "Öfke"], "work_style": "Liderlik yapabildiğin yerler.", "relationship_style": "Tutkulu ve koruyucu.", "danger_signals": ["Düşman yaratmak."], "prescription": ["Kırılgan ol.", "Dinlemeyi öğren."]},
    9: {"title": "Tip 9: Barışçı", "role": "Uzlaştırıcı, Diplomat", "fear": "Çatışma.", "desire": "Huzur.", "stress": 6, "growth": 3, "desc": "Uyum arayan sakin liman.", "strengths": ["Sabırlı", "Kabul edici"], "weaknesses": ["Erteleme", "İnatçılık"], "work_style": "Rekabetin düşük olduğu huzurlu ortamlar.", "relationship_style": "Uyumlu ve destekleyici.", "danger_signals": ["Pasif-agresiflik."], "prescription": ["Önceliklendir.", "Kendi fikrini söyle."]}
}

WING_DESCRIPTIONS = {
    "1w9": "Daha sakin ve filozofik mükemmeliyetçi.", "1w2": "Daha yardımsever ve dışa dönük.",
    "2w1": "Daha prensipli ve sorumlu yardımcı.", "2w3": "Daha hırslı ve sosyal.",
    "3w2": "Daha ilişki odaklı ve sıcakkanlı.", "3w4": "Daha sanatsal ve bireysel.",
    "4w3": "Daha hırslı ve performans odaklı.", "4w5": "Daha analitik ve içe dönük.",
    "5w4": "Daha yaratıcı ve duygusal araştırmacı.", "5w6": "Daha planlı ve sadık.",
    "6w5": "Daha bağımsız ve mesafeli.", "6w7": "Daha sosyal ve iyimser.",
    "7w6": "Daha sorumlu ve grup odaklı.", "7w8": "Daha lider ruhlu ve kararlı.",
    "8w7": "Daha enerjik ve eğlenceli lider.", "8w9": "Daha barışçıl ve sakin güç.",
    "9w8": "Daha iddialı ve kararlı barışçı.", "9w1": "Daha disiplinli ve idealist."
}

# --- YARDIMCI FONKSİYONLAR ---
def get_data_from_ai(prompt):
    if not GROK_API_KEY: return "Hata: API Key yok."
    try:
        response = client.chat.completions.create(
            model="grok-4-1-fast-reasoning",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        content = response.choices[0].message.content.strip()
        if "```json" in content: content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content: content = content.split("```")[1].split("```")[0].strip()
        return content
    except Exception as e: return f"Hata: {e}"

def calculate_enneagram_report(all_answers):
    scores = {t: 0 for t in range(1, 10)}
    for q_id, val in all_answers.items():
        tip = int(q_id.split('_')[0])
        scores[tip] += val
    
    max_score = 20 * 5
    normalized = {t: round(s / max_score * 100, 1) for t, s in scores.items()}
    
    main_type = max(scores, key=scores.get)
    main_score = normalized[main_type]
    
    if main_type == 1: wings = [9, 2]
    elif main_type == 9: wings = [8, 1]
    else: wings = [main_type - 1, main_type + 1]
    
    wing_type = max(wings, key=lambda w: normalized[w])
    wing_score = normalized[wing_type]
    full_type_str = f"{main_type}w{wing_type}" if wing_score > main_score * 0.7 else f"{main_type} (Saf Tip)"
    
    data = ENNEAGRAM_DATA[main_type]
    wing_txt = WING_DESCRIPTIONS.get(f"{main_type}w{wing_type}", "Dengeli kanat.")
    
    report = f"""
    # 🌟 ENNEAGRAM SONUÇ RAPORU 🌟
    **Baskın Tip:** {data['title']} (%{main_score})
    **Profil:** {full_type_str}
    
    ---
    **Kimsin Sen?** {data['desc']}
    **Kanat Etkisi:** {wing_txt}
    **Süper Güçler:** {', '.join(data['strengths'])}
    **Gelişim Alanları:** {', '.join(data['weaknesses'])}
    **Çalışma Tarzın:** {data['work_style']}
    **Reçete:** {', '.join(data['prescription'])}
    """
    return scores, report

# --- ANA APP FONKSİYONU ---
def app():
    st.markdown("""
    <style>
        .stButton > button { width: 100%; border-radius: 12px; height: 60px; font-size: 18px; font-weight: bold; }
        .success-box { background-color: #dcfce7; padding: 25px; border-radius: 12px; border: 2px solid #16a34a; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

    if "page" not in st.session_state: st.session_state.page = "home"
    
    # --- FAZ SİSTEMİ MANTIĞI ---
    lc = st.session_state.get('login_phase', 1)
    
    if lc <= 1: # İlk kayıt ve ilk giriş
        current_tests = PHASE_1_TESTS
        phase_name = "1. AŞAMA: Kişilik ve Zihin Yapısı"
    elif lc == 2: # İkinci giriş
        current_tests = PHASE_2_TESTS
        phase_name = "2. AŞAMA: Öğrenme ve Kaygı Durumu"
    else: # Üçüncü ve sonraki girişler
        current_tests = PHASE_3_TESTS
        phase_name = "3. AŞAMA: Yetenek ve Kariyer Eğilimi"

    # --- SAYFA 1: ANA MENÜ (HOME) ---
    if st.session_state.page == "home":
        st.markdown(f"## 👤 Merhaba, {st.session_state.student_name}")
        st.info(f"Şu an **{phase_name}** testlerini görüntülüyorsunuz.")
        st.write("Lütfen çözmek istediğiniz testi seçiniz:")
        
        col1, col2 = st.columns(2)
        
        # Testleri dinamik listele
        for idx, test in enumerate(current_tests):
            is_done = check_test_completed(st.session_state.student_id, test)
            target_col = col1 if idx % 2 == 0 else col2
            
            if is_done:
                target_col.button(f"✅ {test} (Tamamlandı)", disabled=True, key=test)
            else:
                if target_col.button(f"👉 {test}", type="primary", key=test):
                    st.session_state.selected_test = test
                    st.session_state.intro_passed = False
                    
                    with st.spinner("Test Yükleniyor..."):
                        if "Enneagram" in test:
                            st.session_state.enneagram_type_idx = 1
                            st.session_state.enneagram_answers = {}
                            st.session_state.current_test_data = {"type": "enneagram_fixed"}
                        else:
                            # Grok'tan soru çek
                            prompt = SORU_URETIM_PROMPT.format(test_adi=test)
                            raw = get_data_from_ai(prompt)
                            try:
                                td = json.loads(raw)
                                td["type"] = "likert"
                                st.session_state.current_test_data = td
                                st.session_state.cevaplar = {}
                                st.session_state.sayfa = 0
                            except:
                                st.error("Test soruları yüklenirken hata oluştu.")
                                return
                    
                    st.session_state.page = "test"
                    st.rerun()

    # --- SAYFA 2: BAŞARI EKRANI ---
    elif st.session_state.page == "success_screen":
        st.markdown("<div class='success-box'><h1>🎉 Tebrikler!</h1><p>Testi başarıyla tamamladınız. Sonuçlar öğretmen paneline iletildi.</p></div>", unsafe_allow_html=True)
        st.markdown("---")
        c1, c2 = st.columns(2)
        if c1.button("🏠 Ana Menüye Dön"):
            st.session_state.page = "home"
            st.rerun()
        if c2.button("🚪 Güvenli Çıkış"):
            st.session_state.clear()
            st.rerun()

    # --- SAYFA 3: TEST ÇÖZME EKRANI ---
    elif st.session_state.page == "test":
        t_name = st.session_state.selected_test
        
        # Giriş
        if not st.session_state.intro_passed:
            st.title(f"📘 {t_name}")
            st.info("Lütfen tüm soruları samimiyetle cevaplayınız. Boş bırakılan sorular sistem tarafından tespit edilir.")
            if st.button("TESTİ BAŞLAT", type="primary"):
                st.session_state.intro_passed = True
                st.rerun()
        
        # Sorular
        else:
            data = st.session_state.current_test_data
            q_type = data.get("type")

            # --- TİP 1: LIKERT TESTLERİ (Grok) ---
            if q_type == "likert":
                qs = data["questions"]
                PER_PAGE = 10
                tot_p = (len(qs)//PER_PAGE) + 1
                start = st.session_state.sayfa * PER_PAGE
                curr_qs = qs[start:start+PER_PAGE]
                
                st.progress((st.session_state.sayfa+1)/tot_p)
                
                # Sayfa içi boş kontrolü için ID listesi
                page_q_ids = []
                
                opts = {"Kesinlikle Katılmıyorum": 1, "Katılmıyorum": 2, "Kararsızım": 3, "Katılıyorum": 4, "Kesinlikle Katılıyorum": 5}
                
                for q in curr_qs:
                    st.write(f"**{q['text']}**")
                    page_q_ids.append(q['id'])
                    k = f"q_{q['id']}"
                    
                    saved = st.session_state.cevaplar.get(q['id'])
                    idx = list(opts.values()).index(saved) if saved else None
                    
                    val = st.radio("Cevap", list(opts.keys()), key=k, index=idx, horizontal=True, label_visibility="collapsed")
                    if val: st.session_state.cevaplar[q['id']] = opts[val]
                    st.divider()
                
                c1, c2 = st.columns(2)
                
                # Navigasyon
                if st.session_state.sayfa < tot_p - 1:
                    if c2.button("İleri ➡️"):
                        # Sayfa içi kontrol
                        missing = [qid for qid in page_q_ids if qid not in st.session_state.cevaplar]
                        if missing:
                            st.error("⚠️ Lütfen bu sayfadaki tüm soruları cevaplayınız!")
                        else:
                            st.session_state.sayfa += 1
                            st.rerun()
                else:
                    if c2.button("Bitir ve Gönder ✅", type="primary"):
                        # Final kontrol
                        missing_q = next((q for q in qs if q['id'] not in st.session_state.cevaplar), None)
                        if missing_q:
                            st.error("⚠️ Eksik sorular var! Lütfen kontrol ediniz.")
                            # İstenirse burada sayfa yönlendirmesi de yapılabilir ama sayfa içi kontrol olduğu için gerek kalmayabilir.
                        else:
                            with st.spinner("Analiz yapılıyor..."):
                                rep = get_data_from_ai(TEK_RAPOR_PROMPT.format(test_adi=t_name, cevaplar_json=json.dumps(st.session_state.cevaplar)))
                                save_test_result_to_db(st.session_state.student_id, t_name, st.session_state.cevaplar, None, rep)
                                st.session_state.page = "success_screen"
                                st.rerun()

            # --- TİP 2: ENNEAGRAM (Sabit) ---
            elif q_type == "enneagram_fixed":
                curr_type = st.session_state.enneagram_type_idx
                questions = ENNEAGRAM_QUESTIONS[curr_type]
                
                st.progress(curr_type / 9)
                st.subheader(f"Bölüm {curr_type}: Tip {curr_type} Soruları")
                
                opts = [1, 2, 3, 4, 5]
                labels = ["1 (Hiç)", "2", "3", "4", "5 (Çok)"]
                all_answered = True
                
                for i, q_text in enumerate(questions):
                    q_key = f"{curr_type}_{i}"
                    st.write(f"**{i+1}. {q_text}**")
                    prev = st.session_state.enneagram_answers.get(q_key)
                    val = st.radio(f"Soru {i+1}", opts, key=f"rad_{q_key}", index=opts.index(prev) if prev else None, horizontal=True, format_func=lambda x: labels[x-1], label_visibility="collapsed")
                    
                    if val: st.session_state.enneagram_answers[q_key] = val
                    else: all_answered = False
                    st.divider()
                
                c1, c2 = st.columns(2)
                if curr_type < 9:
                    if c2.button("Sonraki Bölüm ➡️"):
                        if not all_answered:
                            st.error("⚠️ Lütfen bu bölümdeki tüm soruları cevaplayınız!")
                        else:
                            st.session_state.enneagram_type_idx += 1
                            st.rerun()
                else:
                    if c2.button("Bitir ✅", type="primary"):
                        if not all_answered:
                            st.error("⚠️ Lütfen tüm soruları cevaplayınız!")
                        else:
                            with st.spinner("Kişilik analizi yapılıyor..."):
                                scores, rep = calculate_enneagram_report(st.session_state.enneagram_answers)
                                save_test_result_to_db(st.session_state.student_id, t_name, st.session_state.enneagram_answers, scores, rep)
                                st.session_state.page = "success_screen"
                                st.rerun()
