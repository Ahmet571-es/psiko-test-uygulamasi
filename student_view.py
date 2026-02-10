import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import matplotlib.pyplot as plt
import numpy as np
import time
import random
from db_utils import check_daily_limit, check_test_completed, save_test_result_to_db

# --- API VE AYARLAR ---
load_dotenv()
if "GROK_API_KEY" in st.secrets:
    GROK_API_KEY = st.secrets["GROK_API_KEY"]
else:
    GROK_API_KEY = os.getenv("GROK_API_KEY")

client = OpenAI(api_key=GROK_API_KEY, base_url="https://api.x.ai/v1")

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
- Aynı veya benzer ifadeler ASLA tekrarlanmasın. Maksimum çeşitlilik sağla (farklı cümle yapıları, bağlamlar ve ifadeler kullan).
- Çıktıda kesinlikle başka hiçbir metin, açıklama, başlık, markdown, kod bloğu işareti veya ek bilgi yazma. Sadece geçerli JSON üret.

TESTLERE ÖZGÜ ZORUNLU KURALLAR:
- Çoklu Zeka Testi (Gardner): Tam 80 soru üret. 8 zeka alanı için tam 10'ar soru: Sözel, Mantıksal, Görsel, Müziksel, Bedensel, Sosyal, İçsel, Doğacı. Her soruya ilgili "area" alanı ekle.
- Holland Mesleki İlgi Envanteri (RIASEC): Tam 90 soru üret. 6 tip için tam 15'er soru: Gerçekçi, Araştırmacı, Yaratıcı, Sosyal, Girişimci, Düzenli. Sorular aktivite ve meslek ilgisi odaklı olsun. Her soruya ilgili "area" alanı ekle.
- VARK Öğrenme Stilleri Testi: Tam 16 soru üret. Orijinal VARK tarzında günlük hayat senaryoları üzerinden çoktan seçmeli tercih soruları üret (4 seçenek: Görsel, İşitsel, Okuma/Yazma, Kinestetik). Likert değil, tercih tipi olsun.
- Sağ-Sol Beyin Dominansı Testi: Tam 30 soru üret. 15 sol beyin + 15 sağ beyin özelliği. Sorular davranış ve düşünce tarzı odaklı olsun.
- Çalışma Davranışı Ölçeği (Baltaş): Tam 73 soru üret. Çalışma alışkanlıkları, motivasyon, disiplin ve zaman yönetimi odaklı olsun.
- Sınav Kaygısı Ölçeği (DuSKÖ): Tam 50 soru üret. Sınav öncesi, sırası ve sonrası kaygı belirtileri odaklı olsun.

JSON ÇIKTI FORMATI (KESİNLİKLE BU ŞEKİLDE OLSUN):
{{
  "type": "likert",
  "questions": [
    {{"id": 1, "text": "Soru metni burada"}}
  ]
}}

Sadece istenen test için soru üret. Çıktı %100 geçerli JSON olsun ve başka hiçbir karakter içermesin.

Test adı: {test_adi}
"""

TEK_RAPOR_PROMPT = """
Sen dünyanın en iyi psikometrik test analizi ve yorumlama uzmanısın. Çocuk/ergen psikolojisi konusunda çok deneyimlisin ve gençlere yol göstermeyi seviyorsun.

GÖREV: Sadece verilen JSON verilerine (puanlar, cevaplar, istatistikler) dayanarak test sonucunu çok kapsamlı ve zengin bir şekilde analiz et. 
ASLA genel geçer bilgi, dış kaynak veya varsayım ekleme. Sadece kullanıcının kendi verilerinden yola çıkarak yorum yap.

Rapor tamamen tarafsız, nesnel ve yargısız olsun. 
Dil ÇOK sade, yalın ve herkesin anlayabileceği bir Türkçe olsun. Ortaokul öğrencisi bile rahatça okuyabilsin. 
Kısa cümleler kullan. Karmaşık kelimelerden tamamen kaçın. Günlük konuşma gibi akıcı ve doğal yaz. 
Derin ve zengin analiz yap ama ifadeleri her zaman basit ve net tut. Motive edici ve destekleyici bir üslup kullan.

Test adı: {test_adi}
Veriler: {cevaplar_json}

ZORUNLU RAPOR FORMATI (Tam olarak bu başlıkları ve sırayı kullan):

1. **Genel Değerlendirme** Testin en önemli 3-4 bulgusunu kısaca özetle. Kullanıcının dikkatini hemen çekecek şekilde başla.

2. **Detaylı Puan Dağılımı** Her alan/tip için alınan puanları sayısal olarak listele. 
   En yüksek 2-3 ve en düşük 2-3 alanı vurgula. Ortalama, yüzdelik veya doğru/yanlış/atlanan sayılarını (teste göre) belirt.

3. **Baskın Özellikler ve Güçlü Yönler** Yüksek puan alınan alanlardaki özellikleri detaylı anlat. 
   Bu özelliklerin günlük hayata, okul başarısına ve kişisel ilişkilere olumlu etkilerini veri odaklı örneklerle açıkla.

4. **Gelişim Alanları ve Potansiyel Zorluklar** Düşük puan alınan alanlardaki özellikleri belirt. 
   Bunların olası zorluklarını ve hayatındaki yansımalarını veri odaklı örneklerle anlat.

5. **Puanlar Arası İlişkiler ve Çelişkiler** Farklı alanlar arasındaki ilişkileri analiz et. 
   Örneğin: Bir alanda yüksek, başka alanda düşük puan varsa bunun olası anlamı nedir? 
   İç çelişkiler veya dengesizlikler varsa vurgula.

6. **Günlük Hayat Yansımaları** Verilere dayanarak bu sonuçların okulda, arkadaşlıkta, hobilerde ve aile hayatında nasıl görünebileceğini veri odaklı örneklerle açıkla.

7. **Kişisel İçgörüler** Kullanıcının kendine dair fark edebileceği 5-6 önemli içgörü ver. 
   Her içgörü doğrudan puanlardan çıksın ve "Senin puanların gösteriyor ki..." diye başlasın.

8. **Grafik ve Görsel Öneriler** Bu test için en uygun grafik türlerini öner (radar chart, çubuk grafik vb.). 
   Hangi alanların grafikte öne çıkacağını ve neden faydalı olacağını belirt.

9. **Pratik Öneriler** Veri odaklı, uygulanabilir ve somut 6-7 öneri ver. 
   Her öneri "Senin ... puanların nedeniyle..." diye başlasın ve hemen yapılabilecek bir adım içersin.

10. **Sonuç Özeti ve Motivasyon** Tüm analizin kısa ve motive edici bir özeti. 
    Güçlü yönlerini hatırlatarak, potansiyelini vurgulayarak bitir.
"""

# --- SABİT ENNEAGRAM VERİLERİ ---
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

BURDON_SURELERI = {
    "7-8 Yaş (10 Dakika)": 600, "9-10 Yaş (8 Dakika)": 480,
    "11-12 Yaş (6 Dakika)": 360, "13-14 Yaş (4 Dakika)": 240,
    "15-16 Yaş (3 Dakika)": 180, "17+ / Yetişkin (2.5 Dakika)": 150
}

TEST_BILGILERI = {
    "Enneagram Kişilik Testi": {"amac": "Temel kişilik tipinizi belirler.", "nasil": "İfadelerin size ne kadar uyduğunu işaretleyin (1-5 Puan).", "ipucu": "Dürüst olun, cevaplar gizlidir."},
    "d2 Dikkat Testi": {"amac": "Seçici dikkatinizi ölçer.", "nasil": "d'' harflerini bulun.", "ipucu": "Hızlanın!"},
    "Burdon Dikkat Testi": {"amac": "Uzun süreli dikkat.", "nasil": "Harfleri işaretleyin.", "ipucu": "Süreye dikkat."},
    "Genel": {"amac": "Analiz.", "nasil": "Seçim yapın.", "ipucu": "Dürüst olun."}
}

TESTLER = [
    "Enneagram Kişilik Testi", "d2 Dikkat Testi", "Burdon Dikkat Testi",
    "Çoklu Zeka Testi (Gardner)", "Holland Mesleki İlgi Envanteri (RIASEC)",
    "VARK Öğrenme Stilleri Testi", "Sağ-Sol Beyin Dominansı Testi",
    "Çalışma Davranışı Ölçeği (Baltaş)", "Sınav Kaygısı Ölçeği (DuSKÖ)"
]

# --- YARDIMCI FONKSİYONLAR ---
def get_data_from_ai(prompt):
    if not GROK_API_KEY:
        return "Hata: API Key bulunamadı."
    try:
        response = client.chat.completions.create(
            model="grok-4-1-fast-reasoning", # GÜNCEL MODEL
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        content = response.choices[0].message.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return content
    except Exception as e:
        return f"Hata: {e}"

def generate_d2_grid():
    grid = []
    chars = ['d', 'p']
    for i in range(658):
        char = random.choice(chars)
        lines = random.choice([1, 2, 3, 4])
        is_target = (char == 'd' and lines == 2)
        visual_lines = "'" * lines
        grid.append({
            "id": i,
            "char": char,
            "lines": lines,
            "visual": f"{char}\n{visual_lines}", 
            "is_target": is_target
        })
    return grid

def generate_burdon_content():
    content = []
    targets = ['a', 'b', 'c', 'd', 'g']
    alpha = "abcdefghijklmnopqrstuvwxyz"
    for i in range(2000):
        is_target = random.random() < 0.30
        char = random.choice(targets) if is_target else random.choice([c for c in alpha if c not in targets])
        content.append({"id": i, "char": char, "is_target": (char in targets)})
    return content, targets

def calculate_enneagram_report(all_answers):
    # Puan Hesapla
    scores = {t: 0 for t in range(1, 10)}
    for q_id, val in all_answers.items():
        # q_id formatı: "1_0", "1_1" -> Tip_SoruIndex
        tip = int(q_id.split('_')[0])
        scores[tip] += val
    
    # Normalize et (Yüzdeye çevir)
    max_score = 20 * 5 # 20 soru, max 5 puan
    normalized = {t: round(s / max_score * 100, 1) for t, s in scores.items()}
    
    # Ana Tip Bul
    main_type = max(scores, key=scores.get)
    main_score = normalized[main_type]
    
    # Kanat Bul
    if main_type == 1: wings = [9, 2]
    elif main_type == 9: wings = [8, 1]
    else: wings = [main_type - 1, main_type + 1]
    
    wing_type = max(wings, key=lambda w: normalized[w])
    wing_score = normalized[wing_type]
    
    full_type_str = f"{main_type}w{wing_type}" if wing_score > main_score * 0.7 else f"{main_type} (Saf Tip)"
    
    # Rapor Metni Oluştur
    data = ENNEAGRAM_DATA[main_type]
    wing_txt = WING_DESCRIPTIONS.get(f"{main_type}w{wing_type}", "Dengeli kanat.")
    
    report = f"""
    # 🌟 ENNEAGRAM ANALİZ SONUCU 🌟
    
    **Baskın Tip:** {data['title']} (%{main_score})
    **Tam Profil:** {full_type_str}
    **Temel Rol:** {data['role']}
    
    ---
    ### 📖 Kimsin Sen?
    {data['desc']}
    
    **Temel Arzu:** {data['desire']}
    **Temel Korku:** {data['fear']}
    
    ---
    ### 🦅 Kanat Etkisi ({wing_type}. Tip)
    {wing_txt}
    
    ---
    ### 💪 Süper Güçlerin
    {', '.join(data['strengths'])}
    
    ### 🚧 Gelişim Alanların
    {', '.join(data['weaknesses'])}
    
    ---
    ### 💼 Çalışma Tarzın
    {data['work_style']}
    
    ### ❤️ İlişki Tarzın
    {data['relationship_style']}
    
    ---
    ### ⚠️ Tükenmişlik Sinyalleri
    {', '.join(data['danger_signals'])}
    
    ### 💊 Sana Özel Reçete
    {', '.join(data['prescription'])}
    
    ---
    **Stres Anında:** Tip {data['stress']} gibi davranabilirsin.
    **Büyüme Anında:** Tip {data['growth']} özelliklerini gösterirsin.
    """
    
    return scores, report

# --- CALLBACK FONKSİYONLARI ---
def toggle_burdon_selection(item_id, current_chunk):
    if current_chunk not in st.session_state.burdon_isaretlenen:
        st.session_state.burdon_isaretlenen[current_chunk] = set()
    s = st.session_state.burdon_isaretlenen[current_chunk]
    if item_id in s: s.remove(item_id)
    else: s.add(item_id)

def toggle_d2_selection(item_id):
    s = st.session_state.d2_isaretlenen
    if item_id in s: s.remove(item_id)
    else: s.add(item_id)

def next_chunk_callback(): st.session_state.current_chunk += 1
def finish_burdon_callback(): st.session_state.test_bitti = True

# --- ANA ÖĞRENCİ UYGULAMASI (APP) ---
def app():
    # CSS
    st.markdown("""
    <style>
        .stButton > button { width: 100%; border-radius: 10px; height: 50px; font-weight: 600; }
        [data-testid="column"] div.stButton > button { height: 60px; font-size: 22px; margin: 1px; }
        .success-box { background-color: #dcfce7; padding: 20px; border-radius: 10px; border: 1px solid #16a34a; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

    # Session State
    if "page" not in st.session_state: st.session_state.page = "home"
    if "intro_passed" not in st.session_state: st.session_state.intro_passed = False
    if "test_finished" not in st.session_state: st.session_state.test_finished = False

    # 1. LIMIT KONTROLÜ (Test bitince tekrar kontrol edilmeli)
    if st.session_state.page == "home":
        if not check_daily_limit(st.session_state.student_id):
            st.error("⚠️ Günlük test çözme limitinize (2 adet) ulaştınız. Yarın tekrar bekleriz.")
            if st.button("🚪 Çıkış Yap", type="secondary"):
                st.session_state.clear()
                st.rerun()
            return

    # 2. SAYFA: HOME (Test Seçimi)
    if st.session_state.page == "home":
        st.markdown(f"## 👤 Merhaba, {st.session_state.student_name}")
        st.write("Lütfen uygulamak istediğiniz testi seçin.")
        
        selected_test = st.selectbox("Test Listesi:", TESTLER, index=None, placeholder="Bir test seçiniz...")
        
        if st.button("SEÇİMİ ONAYLA VE BAŞLA ➡️", type="primary"):
            if not selected_test:
                st.error("Lütfen bir test seçin.")
            else:
                # GEÇMİŞ KONTROLÜ
                if check_test_completed(st.session_state.student_id, selected_test):
                    st.warning(f"⛔ '{selected_test}' testini daha önce tamamladınız. Tekrar çözemezsiniz.")
                    return

                st.session_state.selected_test = selected_test
                st.session_state.intro_passed = False
                st.session_state.test_finished = False
                
                with st.spinner("Test hazırlanıyor..."):
                    # ÖZEL ENNEAGRAM DURUMU
                    if "Enneagram" in selected_test:
                        st.session_state.enneagram_type_idx = 1 # Tip 1'den başla
                        st.session_state.enneagram_answers = {} # Cevapları tut
                        st.session_state.current_test_data = {"type": "enneagram_fixed"} # Özel tip
                    
                    # DİĞER TESTLER
                    elif "d2" in selected_test.lower():
                        st.session_state.current_test_data = {"type": "d2", "questions": generate_d2_grid()}
                        st.session_state.d2_isaretlenen = set()
                        st.session_state.d2_basla = False
                        st.session_state.d2_bitti = False
                        st.session_state.d2_current_row = 0
                    elif "burdon" in selected_test.lower():
                        d, t = generate_burdon_content()
                        st.session_state.current_test_data = {"type": "burdon", "questions": d}
                        st.session_state.burdon_targets = t
                        st.session_state.burdon_basla = False
                        st.session_state.burdon_isaretlenen = {}
                        st.session_state.current_chunk = 0
                        st.session_state.burdon_limit = 600
                        st.session_state.test_bitti = False
                    else:
                        # GROK API İLE SORU ÜRET (Diğer testler için)
                        prompt = SORU_URETIM_PROMPT.format(test_adi=selected_test)
                        raw = get_data_from_ai(prompt)
                        try:
                            test_data = json.loads(raw)
                            test_data["type"] = "likert" # Standart Likert
                            st.session_state.current_test_data = test_data
                            st.session_state.cevaplar = {}
                            st.session_state.sayfa = 0
                        except:
                            st.error("Test üretilirken hata oluştu. Lütfen tekrar deneyin.")
                            return
                
                st.session_state.page = "test"
                st.rerun()

    # 3. SAYFA: TEST BİTİŞ EKRANI (BAŞARI EKRANI)
    elif st.session_state.page == "success_screen":
        st.markdown("""
        <div class="success-box">
            <h1>🎉 Tebrikler!</h1>
            <p>Testi başarıyla tamamladınız.</p>
            <p>Sonuçlarınız analiz edilmek üzere öğretmeninize iletildi.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Ne yapmak istersiniz?")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏠 Ana Sayfaya Dön (Yeni Test)", type="primary"):
                st.session_state.page = "home"
                st.session_state.test_finished = False
                st.rerun()
                
        with col2:
            if st.button("🚪 Çıkış Yap"):
                st.session_state.clear()
                st.rerun()

    # 4. SAYFA: TEST EKRANI
    elif st.session_state.page == "test":
        test_name = st.session_state.selected_test
        
        # Giriş / Bilgilendirme
        if not st.session_state.intro_passed:
            st.markdown(f"# 📘 {test_name}")
            info = TEST_BILGILERI.get(test_name, TEST_BILGILERI["Genel"])
            st.info(f"**Amaç:** {info['amac']}\n\n**Nasıl:** {info['nasil']}\n\n**İpucu:** {info['ipucu']}")
            
            if "Burdon" in test_name:
                yas = st.selectbox("Yaş Grubu:", list(BURDON_SURELERI.keys()))
                st.session_state.burdon_limit = BURDON_SURELERI[yas]

            if st.button("✅ TESTİ BAŞLAT", type="primary"):
                st.session_state.intro_passed = True
                if "d2" in test_name:
                    st.session_state.d2_basla = True
                    st.session_state.d2_row_start_time = time.time()
                if "Burdon" in test_name:
                    st.session_state.burdon_basla = True
                    st.session_state.start_time = time.time()
                st.rerun()

        # Soru Ekranları
        else:
            data = st.session_state.current_test_data
            q_type = data.get("type", "likert")

            # --- 1. ÖZEL ENNEAGRAM TESTİ (SABİT SORULAR) ---
            if q_type == "enneagram_fixed":
                curr_type = st.session_state.enneagram_type_idx
                questions = ENNEAGRAM_QUESTIONS[curr_type]
                
                st.progress(curr_type / 9)
                st.subheader(f"Bölüm {curr_type}: Tip {curr_type} Soruları")
                st.caption("Aşağıdaki ifadelere ne kadar katılıyorsunuz? (1: Neredeyse Hiç - 5: Neredeyse Her Zaman)")
                
                # Cevapları al
                opts = [1, 2, 3, 4, 5]
                labels = ["1 (Hiç)", "2", "3", "4", "5 (Çok)"]
                
                all_answered = True
                
                # Form elemanları
                for i, q_text in enumerate(questions):
                    q_key = f"{curr_type}_{i}" # Unique ID: Tip_SoruIndex
                    st.write(f"**{i+1}. {q_text}**")
                    
                    prev_val = st.session_state.enneagram_answers.get(q_key, None)
                    val = st.radio(f"Soru {i+1}", opts, key=f"rad_{q_key}", index=opts.index(prev_val) if prev_val else None, horizontal=True, format_func=lambda x: labels[x-1], label_visibility="collapsed")
                    
                    if val:
                        st.session_state.enneagram_answers[q_key] = val
                    else:
                        all_answered = False
                    st.divider()
                
                # İleri / Bitir Butonları
                c1, c2 = st.columns(2)
                
                if curr_type < 9:
                    if c2.button(f"Tip {curr_type+1}'e Geç ➡️", type="primary"):
                        if not all_answered:
                            st.error("⚠️ Lütfen bu bölümdeki tüm soruları cevaplayınız!")
                        else:
                            st.session_state.enneagram_type_idx += 1
                            st.rerun()
                else:
                    if c2.button("TESTİ BİTİR VE ANALİZ ET ✅", type="primary"):
                        if not all_answered:
                            st.error("⚠️ Lütfen tüm soruları cevaplayınız!")
                        else:
                            with st.spinner("Kişilik haritanız çıkarılıyor..."):
                                # Enneagram Özel Hesaplama
                                scores, report = calculate_enneagram_report(st.session_state.enneagram_answers)
                                
                                # Veritabanına Kayıt
                                save_test_result_to_db(
                                    st.session_state.student_id, 
                                    test_name, 
                                    st.session_state.enneagram_answers, 
                                    scores, 
                                    report
                                )
                                st.session_state.page = "success_screen"
                                st.rerun()

            # --- 2. DİĞER LIKERT TESTLERİ (Grok ile Üretilenler) ---
            elif q_type == "likert":
                qs = data["questions"]
                PER_PAGE = 10
                tot_p = (len(qs)//PER_PAGE)+1
                start = st.session_state.sayfa * PER_PAGE
                curr_qs = qs[start:start+PER_PAGE]
                
                st.progress((st.session_state.sayfa+1)/tot_p)
                
                opts = {"Kesinlikle Katılmıyorum": 1, "Katılmıyorum": 2, "Kararsızım": 3, "Katılıyorum": 4, "Kesinlikle Katılıyorum": 5}
                
                for q in curr_qs:
                    st.write(f"**{q['text']}**")
                    k = f"q_{q['id']}"
                    saved = st.session_state.cevaplar.get(q['id'])
                    # Default index ayarı
                    idx = None
                    if saved:
                        vals = list(opts.values())
                        if saved in vals:
                            idx = vals.index(saved)

                    val = st.radio("Cevap", list(opts.keys()), key=k, index=idx, horizontal=True, label_visibility="collapsed")
                    if val: st.session_state.cevaplar[q['id']] = opts[val]
                    st.divider()
                
                c1, c2 = st.columns(2)
                if st.session_state.sayfa < tot_p-1:
                    if c2.button("İleri ➡️"):
                        st.session_state.sayfa += 1
                        st.rerun()
                else:
                    if c2.button("Bitir ✅", type="primary"):
                        # EKSİK SORU KONTROLÜ VE YÖNLENDİRME
                        missing_q = None
                        missing_idx = -1
                        
                        # Tüm soruları tara
                        for i, q in enumerate(qs):
                            if q['id'] not in st.session_state.cevaplar:
                                missing_q = q
                                missing_idx = i
                                break
                        
                        if missing_q:
                            # Eksik soru varsa sayfasını bul
                            target_page = missing_idx // PER_PAGE
                            st.session_state.sayfa = target_page
                            st.error(f"⚠️ {missing_idx + 1}. soruyu boş bıraktınız. Lütfen cevaplayınız.")
                            time.sleep(1.5) # Kullanıcı hatayı görsün diye azıcık bekle
                            st.rerun()
                        else:
                            # Her şey tamsa kaydet
                            with st.spinner("Analiz ediliyor..."):
                                stats = {"Cevaplar": st.session_state.cevaplar}
                                # Grok Raporu
                                rep = get_data_from_ai(TEK_RAPOR_PROMPT.format(test_adi=test_name, cevaplar_json=json.dumps(stats)))
                                save_test_result_to_db(st.session_state.student_id, test_name, st.session_state.cevaplar, None, rep)
                                st.session_state.page = "success_screen"
                                st.rerun()

            # --- 3. D2 TESTİ ---
            elif q_type == "d2":
                questions = data["questions"] # D2 ERROR FIX İÇİN EKLENEN SATIR
                ROW_TIME = 20
                TOTAL_ROWS = 14
                
                @st.fragment(run_every=1)
                def d2_row_timer():
                    if st.session_state.get("d2_basla", False) and not st.session_state.get("d2_bitti", False):
                        elapsed = time.time() - st.session_state.d2_row_start_time
                        remaining = ROW_TIME - elapsed
                        if remaining <= 0:
                            st.session_state.d2_current_row += 1
                            if st.session_state.d2_current_row >= TOTAL_ROWS:
                                st.session_state.d2_bitti = True
                            else:
                                st.session_state.d2_row_start_time = time.time()
                            st.rerun()
                        st.progress(max(0.0, remaining / ROW_TIME))
                        st.caption(f"Satır: {st.session_state.d2_current_row + 1} / {TOTAL_ROWS}")

                @st.fragment
                def d2_grid_view(current_row_items):
                    if st.session_state.get("d2_bitti", False): return
                    cols = st.columns(10)
                    sel = st.session_state.d2_isaretlenen
                    for idx, item in enumerate(current_row_items):
                        c = cols[idx % 10]
                        is_sel = item['id'] in sel
                        c.button(item['visual'], key=f"d2_{item['id']}", type="primary" if is_sel else "secondary", on_click=toggle_d2_selection, args=(item['id'],))

                if st.session_state.get("d2_bitti", False):
                    targets = [q['id'] for q in questions if q['is_target']]
                    sel = st.session_state.d2_isaretlenen
                    hits = len(set(targets).intersection(sel))
                    false_al = len(sel - set(targets))
                    miss = len(set(targets) - sel)
                    stats = {"Doğru": hits, "Hata": false_al, "Atlanan": miss}
                    
                    with st.spinner("Sonuçlar kaydediliyor..."):
                        prompt = TEK_RAPOR_PROMPT.format(test_adi="d2 Dikkat Testi", cevaplar_json=json.dumps(stats))
                        report = get_data_from_ai(prompt)
                        save_test_result_to_db(st.session_state.student_id, test_name, {"isaretlenen_idleri": list(sel)}, stats, report)
                        st.session_state.page = "success_screen"
                        st.rerun()
                else:
                    d2_row_timer()
                    curr_r = st.session_state.d2_current_row
                    start_idx = curr_r * 47
                    current_items = questions[start_idx:start_idx + 47]
                    d2_grid_view(current_items)

            # --- 4. BURDON TESTİ ---
            elif q_type == "burdon":
                CHUNK_SIZE = 50
                total = (len(questions) // CHUNK_SIZE) + 1
                LIMIT = st.session_state.burdon_limit
                
                @st.fragment(run_every=1)
                def burdon_timer():
                    if not st.session_state.get("test_bitti", False):
                        elapsed = time.time() - st.session_state.start_time
                        rem = LIMIT - elapsed
                        if rem <= 0:
                            st.session_state.test_bitti = True
                            st.rerun()
                        st.metric("Kalan Süre", f"{int(rem)} sn")

                burdon_timer()
                
                if st.session_state.get("test_bitti", False):
                    all_sel = set()
                    for chunk in st.session_state.burdon_isaretlenen.values():
                        all_sel.update(chunk)
                    targets = [q['id'] for q in questions if q['is_target']]
                    hits = len(set(targets).intersection(all_sel))
                    missed = len(set(targets) - all_sel)
                    wrong = len(all_sel - set(targets))
                    stats = {"Doğru": hits, "Atlanan": missed, "Yanlış": wrong}
                    
                    with st.spinner("Sonuçlar kaydediliyor..."):
                        prompt = TEK_RAPOR_PROMPT.format(test_adi="Burdon Dikkat Testi", cevaplar_json=json.dumps(stats))
                        report = get_data_from_ai(prompt)
                        save_test_result_to_db(st.session_state.student_id, test_name, {"isaretlenen_idleri": list(all_sel)}, stats, report)
                        st.session_state.page = "success_screen"
                        st.rerun()
                else:
                    start = st.session_state.current_chunk * CHUNK_SIZE
                    current_items = questions[start:start + CHUNK_SIZE]
                    st.info(f"HEDEFLER: {', '.join(st.session_state.burdon_targets)}")
                    st.caption(f"Sayfa {st.session_state.current_chunk + 1} / {total}")
                    
                    cols_count = 10
                    rows = [current_items[i:i+cols_count] for i in range(0, len(current_items), cols_count)]
                    
                    for row in rows:
                        cols = st.columns(cols_count)
                        for c, item in enumerate(row):
                            is_sel = item['id'] in st.session_state.burdon_isaretlenen.get(st.session_state.current_chunk, set())
                            cols[c].button(
                                item['char'], 
                                key=f"b_{item['id']}", 
                                type="primary" if is_sel else "secondary", 
                                on_click=toggle_burdon_selection, 
                                args=(item['id'], st.session_state.current_chunk)
                            )

                    st.markdown("---")
                    c1, c2 = st.columns([1, 4])
                    
                    if st.session_state.current_chunk < total - 1:
                        c2.button("SONRAKİ SAYFA ➡️", type="primary", on_click=next_chunk_callback, key=f"next_{st.session_state.current_chunk}")
                    else:
                        c2.button("TESTİ BİTİR 🏁", type="primary", on_click=finish_burdon_callback, key="finish_btn")
