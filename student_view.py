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

# --- GELİŞMİŞ, FEW-SHOT DESTEKLİ PROMPTLAR ---
SORU_URETIM_PROMPT = """
Sen dünyanın en iyi çocuk ve ergen psikolojisi uzmanı, aynı zamanda ödüllü bir test tasarımcısısın.

GÖREV: Belirtilen test ({test_adi}) için, orijinal yapısına sadık kalarak YEPYENİ sorular üret.

⚠️ KRİTİK KURALLAR (HAYATİ ÖNEM TAŞIR):
1. **DİL VE ANLATIM (İLKOKUL SEVİYESİ):** Sorular o kadar sade, duru ve net olsun ki, ilkokula giden bir çocuk bile tek seferde anlasın. Asla "akademik" kelime kullanma.
2. **MANİPÜLASYON KALKANI:** Öğrencinin "bunu seçersem havalı görünürüm" diyemeyeceği, **dolaylı** ve **zekice** kurgulanmış durumlar sun.
3. **PSİKOLOJİK DERİNLİK:** Dil basit olsun ama ölçtüğü şey derin olsun.

---
### 🌟 REFERANS ÖRNEK HAVUZU (FEW-SHOT EXAMPLES) 🌟
(Soruları üretirken aşağıdaki örneklerin sadeliğini, doğallığını ve dolaylı anlatım tarzını kopyala. Asla sıkıcı olma!)

**Örnek 1 (Çoklu Zeka - Mantıksal):**
❌ Kötü Soru: "Matematik problemlerini çözmeyi severim." (Çok bariz)
✅ İyi Soru: "Sayılarla oynamak bana bulmaca çözmek gibi eğlenceli gelir."

**Örnek 2 (Çoklu Zeka - Sosyal):**
❌ Kötü Soru: "Liderlik özelliklerim vardır."
✅ İyi Soru: "Arkadaşlarım bir oyun oynayacağı zaman kuralları genelde ben koyarım."

**Örnek 3 (Çoklu Zeka - İçsel):**
❌ Kötü Soru: "Kendi duygularımın farkındayımdır."
✅ İyi Soru: "Bazen odama çekilip 'Bugün neler hissettim?' diye düşünmeyi severim."

**Örnek 4 (Çoklu Zeka - Doğacı):**
❌ Kötü Soru: "Botanik ile ilgilenirim."
✅ İyi Soru: "Yerdeki farklı taşları veya yaprakları toplayıp incelemek hoşuma gider."

**Örnek 5 (Holland - Gerçekçi):**
❌ Kötü Soru: "Mekanik aletleri tamir ederim."
✅ İyi Soru: "Bozulan bir oyuncağın içini açıp 'Bu nasıl çalışıyor?' diye bakmak isterim."

**Örnek 6 (Holland - Araştırmacı):**
❌ Kötü Soru: "Bilimsel deneyleri severim."
✅ İyi Soru: "Gökyüzündeki yıldızların veya karıncaların nasıl yaşadığını merak edip araştırırım."

**Örnek 7 (Holland - Yaratıcı):**
❌ Kötü Soru: "Sanatsal faaliyetlere katılırım."
✅ İyi Soru: "Boş bir kağıt gördüğümde dayanamam, hemen renkli kalemlerle bir şeyler çizerim."

**Örnek 8 (Sınav Kaygısı):**
❌ Kötü Soru: "Sınavlarda fizyolojik semptomlar gösteririm."
✅ İyi Soru: "Sınav kağıdı önüme gelince kalbim sanki yerinden çıkacakmış gibi hızlı atar."

**Örnek 9 (Sınav Kaygısı):**
❌ Kötü Soru: "Odaklanma sorunu yaşarım."
✅ İyi Soru: "Sınavda bildiğim soruları bile heyecandan unutur, sonra hatırlarım."

**Örnek 10 (VARK - Görsel):**
❌ Kötü Soru: "Görerek öğrenirim."
✅ İyi Soru: "Bir yeri bulmak için bana adres tarif edilmesi yerine harita gösterilmesini isterim."

**Örnek 11 (VARK - Kinestetik):**
❌ Kötü Soru: "Dokunarak öğrenirim."
✅ İyi Soru: "Müzedeki eşyalara dokunmak yasak olduğunda orayı gezmekten sıkılırım."

**Örnek 12 (Sağ-Sol Beyin):**
❌ Kötü Soru: "Analitik düşünürüm."
✅ İyi Soru: "Odamdaki eşyaların her zaman aynı yerde ve düzenli durmasını isterim."

**Örnek 13 (Sağ-Sol Beyin):**
❌ Kötü Soru: "Sezgiselimdir."
✅ İyi Soru: "Birinin yalan söylediğini, o konuşmasa bile yüzünden anlarım."

**Örnek 14 (Çalışma Davranışı):**
❌ Kötü Soru: "Planlı çalışırım."
✅ İyi Soru: "Ödevlerimi son güne bırakmam, azar azar yapıp bitiririm."

**Örnek 15 (Çalışma Davranışı):**
❌ Kötü Soru: "Ders çalışırken dikkatim dağılır."
✅ İyi Soru: "Dersin başındayken aklım sürekli telefona veya oyuna gidiyor."

**Örnek 16 (Holland - Girişimci):**
❌ Kötü Soru: "Satış yapmayı severim."
✅ İyi Soru: "Eski eşyalarımı veya yaptığım bileklikleri başkalarına satmak hoşuma gider."

**Örnek 17 (Çoklu Zeka - Müziksel):**
❌ Kötü Soru: "Müzik kulağım iyidir."
✅ İyi Soru: "Duyduğum bir şarkının ritmini hemen parmaklarımla tutmaya başlarım."

**Örnek 18 (Çoklu Zeka - Bedensel):**
❌ Kötü Soru: "Spor aktivitelerinde başarılıyımdır."
✅ İyi Soru: "Sıramda otururken bile ayaklarımı sallar veya elimle bir şeylerle oynarım, duramam."

**Örnek 19 (Holland - Sosyal):**
❌ Kötü Soru: "İnsanlara yardım ederim."
✅ İyi Soru: "Sınıfta biri üzgünse hemen yanına gidip onu güldürmeye çalışırım."

**Örnek 20 (Çalışma Davranışı):**
❌ Kötü Soru: "Motivasyonum yüksektir."
✅ İyi Soru: "Zor bir ödevle karşılaşınca pes etmem, 'Bunu çözeceğim' derim."
---

TESTLERE ÖZEL YAPILANDIRMA:
- **Çoklu Zeka (Gardner):** 80 soru. 8 zeka türü için 10'ar adet. Her soruya "area" etiketi ekle.
- **Holland (RIASEC):** 90 soru. 6 tip için 15'er adet. Her soruya "area" etiketi ekle.
- **VARK:** 16 soru.
- **Sağ-Sol Beyin:** 30 soru.
- **Çalışma Davranışı:** 73 soru.
- **Sınav Kaygısı:** 50 soru.

JSON ÇIKTI FORMATI:
{{
  "type": "likert",
  "questions": [
    {{"id": 1, "text": "Üretilen soru..."}} 
  ]
}}

Sadece JSON formatında çıktı ver.
Test Adı: {test_adi}
"""

TEK_RAPOR_PROMPT = """
Sen öğrencilerin en sevdiği, onları çok iyi anlayan uzman bir psikologsun.

GÖREV: Verilen test sonuçlarını analiz et ve öğrenciye özel bir rapor yaz.

---
### 🌟 RAPOR DİLİ ÖRNEĞİ (FEW-SHOT) 🌟
(Raporu yazarken aynen bu tonu ve samimiyeti kullan)

**Örnek Giriş:**
"Merhaba! Test sonuçlarına baktım ve gerçekten çok ilginç şeyler gördüm. Sanki zihninin içinde kocaman, rengarenk bir kütüphane var ama bazen aradığın kitabı bulmakta zorlanıyorsun gibi..."

**Örnek Güçlü Yön Anlatımı:**
"Sayısal zekan harika çıkmış! Bu ne demek biliyor musun? Sen olaylara bir dedektif gibi bakıyorsun. Başkalarının 'çok karışık' dediği problemleri sen parçalara ayırıp şıp diye çözüyorsun."

**Örnek Gelişim Alanı Anlatımı:**
"Biraz sınav kaygın var gibi görünüyor. Sınav kağıdı önüne gelince, aslında bildiğin şeyler saklambaç oynuyor gibi aklından kaçıyor olabilir. Ama merak etme, bunu basit nefes taktikleriyle yeneceğiz."
---

RAPOR FORMATI:
1. **Senin Dünyan (Genel Bakış):** Sonuçların özeti.
2. **Sayısal Tablo:** Puanların listesi.
3. **Süper Güçlerin:** En iyi olduğun alanlar ve hayattaki karşılığı.
4. **Geliştirebileceğin Yanlar:** Zorlandığın yerler ve çözüm yolları.
5. **Hayatına Yansımaları:** Okulda, evde, arkadaşlarınla nasılsın?
6. **Sana Özel Tavsiyeler:** Hemen bugün yapabileceğin basit öneriler.
7. **Son Söz:** Motive edici kapanış.

Test: {test_adi}
Veriler: {cevaplar_json}
"""

# --- SABİT ENNEAGRAM VERİLERİ (DEĞİŞMEDİ) ---
ENNEAGRAM_QUESTIONS = {
    1: [
        "Hata yaptığımda kendime çok kızarım.", "Neyin doğru neyin yanlış olduğunu hemen hissederim.",
        "Yaptığım işin kusursuz olması için çok uğraşırım.", "Kurallara uymak ve adil olmak benim için çok önemlidir.",
        "Sözümün eri olmak, dürüst olmak her şeyden önce gelir.", "Duygularımla değil, mantığımla hareket etmeyi severim.",
        "Bazen o kadar ciddi olurum ki eğlenmeyi unutabilirim.", "Beni en çok eleştiren kişi yine benim.",
        "Bir ortamda bir şey düzgün değilse hemen gözüme batar.", "İşlerimi baştan savma değil, tam olması gerektiği gibi yaparım.",
        "Randevularıma sadık kalmaya ve düzenli olmaya çok dikkat ederim.", "Ahlaklı olmak benim kırmızı çizgimdir.",
        "Başkalarının göremediği eksiklikleri şıp diye görürüm.", "Detayların atlanmasından hiç hoşlanmam.",
        "İşler karışınca biraz sert ve kuralcı olabilirim.", "Rahatladığımda ise çok daha anlayışlı ve neşeli olurum.",
        "Yanlış anlaşılmaktan çok korkarım.", "Bana yapılan yanlışı affetmekte bazen zorlanırım.",
        "Benim için olaylar ya siyahtır ya beyaz, griyi pek sevmem.", "Haksız olduğumu kabul etmek bana biraz zor gelir."
    ],
    2: [
        "Hayatımdaki en önemli şey sevdiklerimle olan ilişkimdir.", "İnsanlara yardım etmek beni çok mutlu eder.",
        "Biri benden bir şey isteyince 'Hayır' demekte zorlanırım.", "Hediye vermeyi, hediye almaktan daha çok severim.",
        "İnsanlarla samimi ve yakın olmayı isterim.", "Başkalarının bana ihtiyaç duyması hoşuma gider.",
        "Genelde sıcakkanlı ve güler yüzlüyümdür.", "Üzgün olduğumu pek belli etmem, hep güçlü görünmeye çalışırım.",
        "Yaptığım iyiliğin fark edilmesi ve 'Teşekkür' duymak beni motive eder.", "Sevdiklerimin her an yanımda olmasını isterim.",
        "'Seni seviyorum' demekten ve duymaktan hiç çekinmem.", "Arkadaşlarım dertlerini hep bana anlatır, iyi bir sırdaşımdır.",
        "Arkadaşlıklarımı korumak için kendimden çok ödün veririm.", "Çok strese girersem biraz sitemkar olabilirim.",
        "Mutluysam etrafıma neşe ve sevgi saçarım.", "İnsanları sevmeye çok hazırım.",
        "İlgi görmediğim zaman içten içe kırılırım.", "Birinin işini kolaylaştırmak beni iyi hissettirir.",
        "Sevilmek ve bir gruba ait olmak benim için hava, su kadar önemlidir.", "Endişelendiğimde insanlara daha çok yardım etmeye çalışırım."
    ],
    3: [
        "Girdiğim ortamlarda kendimi iyi ifade ederim.", "Aynı anda birkaç işi birden yönetebilirim.",
        "Başarılı olmak ve parmakla gösterilmek isterim.", "Boş durmayı sevmem, üretken olmak beni canlı tutar.",
        "Bir hedef koyduysam ona kilitlenirim.", "Dışarıdan nasıl göründüğüme ve imajıma önem veririm.",
        "Rakiplerimden önce harekete geçmeyi severim.", "Takım çalışmasını severim ama lider olmak isterim.",
        "Bir işin en kısa ve en pratik yolunu hemen bulurum.", "Bazen heyecanlanıp yapabileceğimden fazla söz verebilirim.",
        "Duygularımı işime karıştırmayı pek sevmem.", "Yarışma ortamları beni daha çok çalışmaya iter.",
        "Okulda veya işte en tepede olmayı hayal ederim.", "Çok stresliysem başkalarını biraz küçümseyebilirim.",
        "Rahatsam çok dürüst ve herkesi motive eden biri olurum.", "Olumsuz düşüncelerin beni yavaşlatmasına izin vermem.",
        "Yeni bir ortama girdiğimde hemen uyum sağlarım.", "Başarılı insanlarla arkadaşlık etmeyi severim.",
        "Yaptığım her işin 'En İyisi' olmaya çalışırım.", "Başardığımı görmek benim yakıtımdır."
    ],
    4: [
        "Hayal gücüm çok geniştir, kafamda filmler çekerim.", "Kendimi çoğu insandan biraz farklı ve özel hissederim.",
        "Bazen sebepsiz yere hüzünlenirim, melankoliyi severim.", "Çok hassas bir kalbim vardır, çabuk etkilenirim.",
        "Sanki hayatımda bir parça eksikmiş gibi hissederim.", "Başkalarının mutluluğunu görünce bazen 'Neden ben değil?' derim.",
        "Duygularımı sanatla, müzikle veya yazıyla ifade etmeyi severim.", "Beni anlamadıklarını düşündüğümde kabuğuma çekilirim.",
        "Romantik ve duygusal filmlerden/kitaplardan hoşlanırım.", "Sıradan ve herkes gibi olmak benim korkulu rüyamdır.",
        "Kimsede olmayan, orijinal eşyalara sahip olmayı severim.", "Duyguları çok yoğun yaşarım, ya hep ya hiç.",
        "Stresliyken biraz huysuz ve mesafeli olabilirim.", "Rahatsam çok şefkatli ve anlayışlı olurum.",
        "Eleştirildiğim zaman çok alınırım.", "Hayatın anlamını ve derinliğini sık sık düşünürüm.",
        "Sürüden ayrılmayı, kendi tarzımı yaratmayı severim.", "Estetik ve güzellik benim için çok önemlidir.",
        "Bazen olayları biraz dramatik hale getirebilirim.", "Duyguların samimi olması benim için her şeyden önemlidir."
    ],
    5: [
        "Çok vıcık vıcık duygusal ortamlardan kaçarım.", "Bir konuyu en ince detayına kadar araştırmayı severim.",
        "Biraz utangaç olabilirim, kalabalıkta kaybolmayı tercih ederim.", "Duygularımı anlatmaktansa fikirlerimi anlatmayı severim.",
        "Bir şey söylemeden önce kafamda tartar, öyle konuşurum.", "Kavgadan ve gürültüden nefret ederim.",
        "Tek başıma vakit geçirmek benim için şarj olmak gibidir.", "Eleştiriye gelemem ama bunu dışarı pek belli etmem.",
        "Kimseye muhtaç olmadan, kendi ayaklarımın üzerinde durmak isterim.", "Özel hayatımı ve sırlarımı kolay kolay paylaşmam.",
        "Kafamın içinde sürekli projeler, fikirler döner durur.", "Zamanımı ve odamı kimsenin işgal etmesini istemem.",
        "Bilmeden konuşan insanlara tahammül edemem.", "İlgi duyduğum konularda ayaklı kütüphane gibiyimdir.",
        "Sadece kafamın uyuştuğu, zeki insanlarla konuşmayı severim.", "Stresliyken insanlardan tamamen kopabilirim.",
        "Rahatsam bilgimi paylaşan, çok zeki ve esprili biri olurum.", "Derin ve felsefi tartışmalara bayılırım.",
        "Grup ödevi yerine bireysel ödevi tercih ederim.", "Kararlarımı hislerimle değil, aklımla veririm."
    ],
    6: [
        "Sorumluluklarımı asla aksatmam, ödevimi son ana bırakmam.", "Her zaman 'B planım', hatta 'C planım' vardır.",
        "İnsanların niyetini hemen anlamam, biraz şüpheciyimdir.", "Karar verirken çok düşünürüm, hata yapmaktan korkarım.",
        "Güvende hissetmek benim için en önemli şeydir.", "Kendi kararımdan emin olamayıp başkalarına danışırım.",
        "Bir gruba veya takıma ait olmak beni rahatlatır.", "Kötü bir şey olacakmış gibi endişelenirim.",
        "Ailem ve arkadaşlarım benim güvenli limanımdır.", "Küçük sorunları kafamda büyütüp felaket senaryoları yazabilirim.",
        "Yeni tanıştığım insanlara hemen güvenmem, zaman tanırım.", "Tehlikeyi ve riski önceden sezerim.",
        "Stresliyken çok kaygılı ve evhamlı olurum.", "Rahatsam dünyanın en sadık ve eğlenceli dostu olurum.",
        "Korktuğum zaman ya donup kalırım ya da saldırganlaşabilirim.", "Kurallara uyan, düzenli biriyimdir.",
        "Biri bana söz verip tutmazsa çok sinirlenirim.", "Korkularımın üzerine gitmek için çabalarım.",
        "Çoğu insandan daha tedbirliyimdir.", "Bana destek olan, arkamda duran insanları asla bırakmam."
    ],
    7: [
        "Hayatın tadını çıkarmak, eğlenmek benim işim.", "Çok konuşkan, neşeli ve fıkır fıkır biriyimdir.",
        "Planlarımın kesinleşmesinden hoşlanmam, seçeneklerim açık olsun isterim.", "Çevrem geniştir, her yerden arkadaşım vardır.",
        "Sürekli yeni şeyler denemek, maceralara atılmak isterim.", "Geleceğe hep umutla bakarım, bardağın dolu tarafını görürüm.",
        "İnsanları güldürmeyi, hikayeler anlatmayı severim.", "Yerimde duramam, enerjim hiç bitmez.",
        "Farklı hobiler, farklı tatlar denemeye bayılırım.", "Sıkılmak benim en büyük düşmanımdır.",
        "Bazen ölçüyü kaçırıp aşırıya kaçabilirim (çok yemek, çok gezmek).", "Özgürlüğümün kısıtlanmasına asla gelemem.",
        "Stresliyken daldan dala atlar, hiçbir işi bitiremem.", "Rahatsam çok yaratıcı ve vizyoner olurum.",
        "Sevdiğim bir işse harikalar yaratırım ama sıkılırsam bırakırım.", "Acıdan, üzüntüden kaçmak için kendimi eğlenceye veririm.",
        "Bir güne çok fazla plan sığdırmaya çalışırım.", "Negatif ve sürekli şikayet eden insanlardan kaçarım.",
        "Aklıma bir fikir gelince hemen yapmak isterim.", "Mutluluk ve heyecan benim yakıtımdır."
    ],
    8: [
        "İstediğim şeyi almak için sonuna kadar mücadele ederim.", "Doğuştan liderimdir, yönetmeyi severim.",
        "Güçlü görünmek hoşuma gider, zayıflıktan nefret ederim.", "Mızmız ve kararsız insanlara tahammülüm yoktur.",
        "Yarışmayı ve kazanmayı severim, kaybetmek kitabımda yazmaz.", "Sevdiklerimi canım pahasına korurum, onlara laf ettirmem.",
        "İplerin elimde olmasını, kontrolün bende olmasını isterim.", "Saygı benim için sevgiden önce gelir.",
        "Risk almaktan korkmam, cesurumdur.", "Çok çalışırım, yorulmak nedir bilmem.",
        "Biri bana meydan okursa cevabını fazlasıyla alır.", "Lafı dolandırmam, neysem oyum, yüzüne söylerim.",
        "Bir grubun başına geçip organize etmekte iyiyimdir.", "Dobra konuşurum, bazen bu yüzden insanlar kırılabilir.",
        "Stresliyken çok baskıcı ve sinirli olabilirim.", "Rahatsam koca yürekli, koruyucu bir kahraman olurum.",
        "Duygularımı göstermeyi zayıflık olarak görürüm.", "Sadece gerçekten güvendiğim insanlara kalbimi açarım.",
        "Hayatı dolu dolu, yüksek sesle yaşamayı severim.", "Haksızlığa asla gelemem, hemen müdahale ederim."
    ],
    9: [
        "Kavgadan, gürültüden hiç hoşlanmam, huzur isterim.", "Herkes 'Çok sakinsin' der, kolay kolay sinirlenmem.",
        "İnsanları çok iyi dinlerim, herkesin derdini anlarım.", "Önemli işleri son ana kadar erteleyebilirim.",
        "Alışkanlıklarımı severim, düzenimin bozulmasını istemem.", "Karar vermek bana zor gelir, 'Fark etmez' demek daha kolaydır.",
        "Acele ettirilmekten nefret ederim, kendi hızımda gitmek isterim.", "Bazen detayları unuturum, dalgın olabilirim.",
        "Öfkemi içime atarım, dışarı pek yansıtmam.", "Boş zamanımda hiçbir şey yapmadan uzanmayı severim.",
        "Evde vakit geçirmek, kendi halimde olmak hoşuma gider.", "Ortam gerilmesin diye alttan alırım.",
        "Birinin bana sürekli ne yapacağımı söylemesi beni inatçı yapar.", "Önemsiz işlerle oyalanıp asıl işi kaçırabilirim.",
        "Stresliyken pasifleşirim, hiçbir şey yapasım gelmez.", "Rahatsam çok üretken ve herkesi birleştiren biri olurum.",
        "Başkalarını memnun etmek için kendi isteğimden vazgeçebilirim.", "Çok fazla seçenek arasında kalmak beni yorar.",
        "Herkesle iyi geçinmeye çalışırım, düşmanım yoktur.", "Huzurlu ve sakin bir hayat hayalimdir."
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
    "1w9": "Sakin ve barışçıl mükemmeliyetçi.", "1w2": "Yardımsever ve dışa dönük reformcu.",
    "2w1": "Prensipli ve ciddi yardımcı.", "2w3": "Hırslı ve popüler yardımcı.",
    "3w2": "Sıcakkanlı ve insan odaklı başarılı.", "3w4": "Sanatsal ve duygusal başarılı.",
    "4w3": "Hırslı ve sahne ışığı seven bireyci.", "4w5": "İçe dönük ve entelektüel bireyci.",
    "5w4": "Yaratıcı ve hayalperest araştırmacı.", "5w6": "Planlı ve güvenilir araştırmacı.",
    "6w5": "Bağımsız ve ciddi sadık.", "6w7": "Eğlenceli ve sosyal sadık.",
    "7w6": "Sorumluluk sahibi ve dost canlısı maceracı.", "7w8": "Lider ruhlu ve cesur maceracı.",
    "8w7": "Enerjik ve dışa dönük lider.", "8w9": "Sakin güç ve babacan lider.",
    "9w8": "Kararlı ve sınır koyan barışçı.", "9w1": "İdealist ve düzenli barışçı."
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
    # 🌟 ENNEAGRAM KİŞİLİK RAPORU 🌟
    **Senin Tipin:** {data['title']} (%{main_score})
    **Tam Profilin:** {full_type_str}
    
    ---
    ### 📖 Sen Kimsin?
    {data['desc']}
    
    ### 🦅 Kanat Etkisi
    {wing_txt}
    
    ### 💪 Süper Güçlerin (Bunları Kullan!)
    {', '.join(data['strengths'])}
    
    ### 🚧 Dikkat Etmen Gerekenler
    {', '.join(data['weaknesses'])}
    
    ### 💊 Sana Özel Taktikler
    {', '.join(data['prescription'])}
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
    
    if lc <= 1: 
        current_tests = PHASE_1_TESTS
        phase_name = "1. AŞAMA: Kişilik ve Zihin Yapısı"
    elif lc == 2: 
        current_tests = PHASE_2_TESTS
        phase_name = "2. AŞAMA: Öğrenme ve Kaygı Durumu"
    else: 
        current_tests = PHASE_3_TESTS
        phase_name = "3. AŞAMA: Yetenek ve Kariyer Eğilimi"

    # --- SAYFA 1: ANA MENÜ (HOME) ---
    if st.session_state.page == "home":
        st.markdown(f"## 👤 Merhaba, {st.session_state.student_name}")
        st.info(f"Şu an **{phase_name}** ekranındasınız.")
        st.write("Lütfen çözmek istediğiniz testi seçiniz:")
        
        col1, col2 = st.columns(2)
        
        for idx, test in enumerate(current_tests):
            is_done = check_test_completed(st.session_state.student_id, test)
            target_col = col1 if idx % 2 == 0 else col2
            
            if is_done:
                target_col.button(f"✅ {test} (Tamamlandı)", disabled=True, key=test)
            else:
                if target_col.button(f"👉 {test}", type="primary", key=test):
                    st.session_state.selected_test = test
                    st.session_state.intro_passed = False
                    
                    with st.spinner("Yapay Zeka Senin İçin Özel Sorular Hazırlıyor..."):
                        if "Enneagram" in test:
                            st.session_state.enneagram_type_idx = 1
                            st.session_state.enneagram_answers = {}
                            st.session_state.current_test_data = {"type": "enneagram_fixed"}
                        else:
                            # Grok'tan YENİ ve GÜÇLÜ Prompt ile soru çek
                            prompt = SORU_URETIM_PROMPT.format(test_adi=test)
                            raw = get_data_from_ai(prompt)
                            try:
                                td = json.loads(raw)
                                td["type"] = "likert"
                                st.session_state.current_test_data = td
                                st.session_state.cevaplar = {}
                                st.session_state.sayfa = 0
                            except:
                                st.error("Test soruları yüklenirken bir hata oluştu. Lütfen tekrar deneyin.")
                                return
                    
                    st.session_state.page = "test"
                    st.rerun()

    # --- SAYFA 2: BAŞARI EKRANI ---
    elif st.session_state.page == "success_screen":
        st.markdown("<div class='success-box'><h1>🎉 Harika İş Çıkardın!</h1><p>Testi başarıyla tamamladın. Sonuçların öğretmenine iletildi.</p></div>", unsafe_allow_html=True)
        st.markdown("---")
        c1, c2 = st.columns(2)
        if c1.button("🏠 Diğer Teste Geç"):
            st.session_state.page = "home"
            st.rerun()
        if c2.button("🚪 Çıkış Yap"):
            st.session_state.clear()
            st.rerun()

    # --- SAYFA 3: TEST ÇÖZME EKRANI ---
    elif st.session_state.page == "test":
        t_name = st.session_state.selected_test
        
        # Giriş
        if not st.session_state.intro_passed:
            st.title(f"📘 {t_name}")
            st.info("Lütfen tüm soruları içtenlikle cevapla. Doğru veya yanlış cevap yok, sadece SEN varsın. Boş bırakılan soruları sistem otomatik yakalar.")
            if st.button("HAZIRIM, BAŞLA!", type="primary"):
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
                            st.error("⚠️ Hop! Bu sayfada boş bıraktığın sorular var. Onları doldurmadan geçemezsin. 😉")
                        else:
                            st.session_state.sayfa += 1
                            st.rerun()
                else:
                    if c2.button("Testi Bitir ✅", type="primary"):
                        # Final kontrol
                        missing_q = next((q for q in qs if q['id'] not in st.session_state.cevaplar), None)
                        if missing_q:
                            st.error("⚠️ Eksik sorular var! Lütfen kontrol et.")
                        else:
                            with st.spinner("Yapay zeka sonuçlarını analiz ediyor..."):
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
                            st.error("⚠️ Lütfen bu bölümdeki tüm soruları cevapla.")
                        else:
                            st.session_state.enneagram_type_idx += 1
                            st.rerun()
                else:
                    if c2.button("Bitir ve Gönder ✅", type="primary"):
                        if not all_answered:
                            st.error("⚠️ Lütfen tüm soruları cevapla.")
                        else:
                            with st.spinner("Kişilik haritan çıkarılıyor..."):
                                scores, rep = calculate_enneagram_report(st.session_state.enneagram_answers)
                                save_test_result_to_db(st.session_state.student_id, t_name, st.session_state.enneagram_answers, scores, rep)
                                st.session_state.page = "success_screen"
                                st.rerun()
