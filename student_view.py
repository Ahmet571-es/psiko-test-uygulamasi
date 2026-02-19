import streamlit as st
import json
import time
from db_utils import check_test_completed, save_test_result_to_db

# --- TEST VERİLERİ MODÜLÜ ---
from test_data import (
    # Sağ-Sol Beyin
    SAG_SOL_BEYIN_QUESTIONS, SAG_SOL_BEYIN_DATA,
    calculate_sag_sol_beyin,
    # Çalışma Davranışı
    CALISMA_DAVRANISI_QUESTIONS, CALISMA_DAVRANISI_CATEGORIES,
    calculate_calisma_davranisi,
    # Sınav Kaygısı
    SINAV_KAYGISI_QUESTIONS, SINAV_KAYGISI_CATEGORIES,
    calculate_sinav_kaygisi,
    # Çoklu Zeka
    COKLU_ZEKA_QUESTIONS_LISE, COKLU_ZEKA_QUESTIONS_ILKOGRETIM,
    COKLU_ZEKA_DATA, ZEKA_SIRA,
    calculate_coklu_zeka_lise, calculate_coklu_zeka_ilkogretim,
    # VARK
    VARK_QUESTIONS, VARK_SCORING, VARK_STYLES,
    calculate_vark,
    # Holland RIASEC
    HOLLAND_QUESTIONS, HOLLAND_TYPES,
    calculate_holland,
)

# ============================================================
# SABİT ENNEAGRAM VERİLERİ
# ============================================================
ENNEAGRAM_QUESTIONS = {
    1: [
        "Hata yaptığımda kendime çok kızarım.",
        "Neyin doğru neyin yanlış olduğunu hemen hissederim.",
        "Yaptığım işin kusursuz olması için çok uğraşırım.",
        "Kurallara uymak ve adil olmak benim için çok önemlidir.",
        "Sözümün eri olmak, dürüst olmak her şeyden önce gelir.",
        "Duygularımla değil, mantığımla hareket etmeyi severim.",
        "Bazen o kadar ciddi olurum ki eğlenmeyi unutabilirim.",
        "Beni en çok eleştiren kişi yine benim.",
        "Bir ortamda bir şey düzgün değilse hemen gözüme batar.",
        "İşlerimi baştan savma değil, tam olması gerektiği gibi yaparım.",
        "Randevularıma sadık kalmaya ve düzenli olmaya çok dikkat ederim.",
        "Ahlaklı olmak benim kırmızı çizgimdir.",
        "Başkalarının göremediği eksiklikleri şıp diye görürüm.",
        "Detayların atlanmasından hiç hoşlanmam.",
        "İşler karışınca biraz sert ve kuralcı olabilirim.",
        "Rahatladığımda ise çok daha anlayışlı ve neşeli olurum.",
        "Yanlış anlaşılmaktan çok korkarım.",
        "Bana yapılan yanlışı affetmekte bazen zorlanırım.",
        "Benim için olaylar ya siyahtır ya beyaz, griyi pek sevmem.",
        "Haksız olduğumu kabul etmek bana biraz zor gelir."
    ],
    2: [
        "Hayatımdaki en önemli şey sevdiklerimle olan ilişkimdir.",
        "İnsanlara yardım etmek beni çok mutlu eder.",
        "Biri benden bir şey isteyince 'Hayır' demekte zorlanırım.",
        "Hediye vermeyi, hediye almaktan daha çok severim.",
        "İnsanlarla samimi ve yakın olmayı isterim.",
        "Başkalarının bana ihtiyaç duyması hoşuma gider.",
        "Genelde sıcakkanlı ve güler yüzlüyümdür.",
        "Üzgün olduğumu pek belli etmem, hep güçlü görünmeye çalışırım.",
        "Yaptığım iyiliğin fark edilmesi ve 'Teşekkür' duymak beni motive eder.",
        "Sevdiklerimin her an yanımda olmasını isterim.",
        "'Seni seviyorum' demekten ve duymaktan hiç çekinmem.",
        "Arkadaşlarım dertlerini hep bana anlatır, iyi bir sırdaşımdır.",
        "Arkadaşlıklarımı korumak için kendimden çok ödün veririm.",
        "Çok strese girersem biraz sitemkar olabilirim.",
        "Mutluysam etrafıma neşe ve sevgi saçarım.",
        "İnsanları sevmeye çok hazırım.",
        "İlgi görmediğim zaman içten içe kırılırım.",
        "Birinin işini kolaylaştırmak beni iyi hissettirir.",
        "Sevilmek ve bir gruba ait olmak benim için hava, su kadar önemlidir.",
        "Endişelendiğimde insanlara daha çok yardım etmeye çalışırım."
    ],
    3: [
        "Girdiğim ortamlarda kendimi iyi ifade ederim.",
        "Aynı anda birkaç işi birden yönetebilirim.",
        "Başarılı olmak ve parmakla gösterilmek isterim.",
        "Boş durmayı sevmem, üretken olmak beni canlı tutar.",
        "Bir hedef koyduysam ona kilitlenirim.",
        "Dışarıdan nasıl göründüğüme ve imajıma önem veririm.",
        "Rakiplerimden önce harekete geçmeyi severim.",
        "Takım çalışmasını severim ama lider olmak isterim.",
        "Bir işin en kısa ve en pratik yolunu hemen bulurum.",
        "Bazen heyecanlanıp yapabileceğimden fazla söz verebilirim.",
        "Duygularımı işime karıştırmayı pek sevmem.",
        "Yarışma ortamları beni daha çok çalışmaya iter.",
        "Okulda veya işte en tepede olmayı hayal ederim.",
        "Çok stresliysem başkalarını biraz küçümseyebilirim.",
        "Rahatsam çok dürüst ve herkesi motive eden biri olurum.",
        "Olumsuz düşüncelerin beni yavaşlatmasına izin vermem.",
        "Yeni bir ortama girdiğimde hemen uyum sağlarım.",
        "Başarılı insanlarla arkadaşlık etmeyi severim.",
        "Yaptığım her işin 'En İyisi' olmaya çalışırım.",
        "Başardığımı görmek benim yakıtımdır."
    ],
    4: [
        "Hayal gücüm çok geniştir, kafamda filmler çekerim.",
        "Kendimi çoğu insandan biraz farklı ve özel hissederim.",
        "Bazen sebepsiz yere hüzünlenirim, melankoliyi severim.",
        "Çok hassas bir kalbim vardır, çabuk etkilenirim.",
        "Sanki hayatımda bir parça eksikmiş gibi hissederim.",
        "Başkalarının mutluluğunu görünce bazen 'Neden ben değil?' derim.",
        "Duygularımı sanatla, müzikle veya yazıyla ifade etmeyi severim.",
        "Beni anlamadıklarını düşündüğümde kabuğuma çekilirim.",
        "Romantik ve duygusal filmlerden/kitaplardan hoşlanırım.",
        "Sıradan ve herkes gibi olmak benim korkulu rüyamdır.",
        "Kimsede olmayan, orijinal eşyalara sahip olmayı severim.",
        "Duyguları çok yoğun yaşarım, ya hep ya hiç.",
        "Stresliyken biraz huysuz ve mesafeli olabilirim.",
        "Rahatsam çok şefkatli ve anlayışlı olurum.",
        "Eleştirildiğim zaman çok alınırım.",
        "Hayatın anlamını ve derinliğini sık sık düşünürüm.",
        "Sürüden ayrılmayı, kendi tarzımı yaratmayı severim.",
        "Estetik ve güzellik benim için çok önemlidir.",
        "Bazen olayları biraz dramatik hale getirebilirim.",
        "Duyguların samimi olması benim için her şeyden önemlidir."
    ],
    5: [
        "Çok vıcık vıcık duygusal ortamlardan kaçarım.",
        "Bir konuyu en ince detayına kadar araştırmayı severim.",
        "Biraz utangaç olabilirim, kalabalıkta kaybolmayı tercih ederim.",
        "Duygularımı anlatmaktansa fikirlerimi anlatmayı severim.",
        "Bir şey söylemeden önce kafamda tartar, öyle konuşurum.",
        "Kavgadan ve gürültüden nefret ederim.",
        "Tek başıma vakit geçirmek benim için şarj olmak gibidir.",
        "Eleştiriye gelemem ama bunu dışarı pek belli etmem.",
        "Kimseye muhtaç olmadan, kendi ayaklarımın üzerinde durmak isterim.",
        "Özel hayatımı ve sırlarımı kolay kolay paylaşmam.",
        "Kafamın içinde sürekli projeler, fikirler döner durur.",
        "Zamanımı ve odamı kimsenin işgal etmesini istemem.",
        "Bilmeden konuşan insanlara tahammül edemem.",
        "İlgi duyduğum konularda ayaklı kütüphane gibiyimdir.",
        "Sadece kafamın uyuştuğu, zeki insanlarla konuşmayı severim.",
        "Stresliyken insanlardan tamamen kopabilirim.",
        "Rahatsam bilgimi paylaşan, çok zeki ve esprili biri olurum.",
        "Derin ve felsefi tartışmalara bayılırım.",
        "Grup ödevi yerine bireysel ödevi tercih ederim.",
        "Kararlarımı hislerimle değil, aklımla veririm."
    ],
    6: [
        "Sorumluluklarımı asla aksatmam, ödevimi son ana bırakmam.",
        "Her zaman 'B planım', hatta 'C planım' vardır.",
        "İnsanların niyetini hemen anlamam, biraz şüpheciyimdir.",
        "Karar verirken çok düşünürüm, hata yapmaktan korkarım.",
        "Güvende hissetmek benim için en önemli şeydir.",
        "Kendi kararımdan emin olamayıp başkalarına danışırım.",
        "Bir gruba veya takıma ait olmak beni rahatlatır.",
        "Kötü bir şey olacakmış gibi endişelenirim.",
        "Ailem ve arkadaşlarım benim güvenli limanımdır.",
        "Küçük sorunları kafamda büyütüp felaket senaryoları yazabilirim.",
        "Yeni tanıştığım insanlara hemen güvenmem, zaman tanırım.",
        "Tehlikeyi ve riski önceden sezerim.",
        "Stresliyken çok kaygılı ve evhamlı olurum.",
        "Rahatsam dünyanın en sadık ve eğlenceli dostu olurum.",
        "Korktuğum zaman ya donup kalırım ya da saldırganlaşabilirim.",
        "Kurallara uyan, düzenli biriyimdir.",
        "Biri bana söz verip tutmazsa çok sinirlenirim.",
        "Korkularımın üzerine gitmek için çabalarım.",
        "Çoğu insandan daha tedbirliyimdir.",
        "Bana destek olan, arkamda duran insanları asla bırakmam."
    ],
    7: [
        "Hayatın tadını çıkarmak, eğlenmek benim işim.",
        "Çok konuşkan, neşeli ve fıkır fıkır biriyimdir.",
        "Planlarımın kesinleşmesinden hoşlanmam, seçeneklerim açık olsun isterim.",
        "Çevrem geniştir, her yerden arkadaşım vardır.",
        "Sürekli yeni şeyler denemek, maceralara atılmak isterim.",
        "Geleceğe hep umutla bakarım, bardağın dolu tarafını görürüm.",
        "İnsanları güldürmeyi, hikayeler anlatmayı severim.",
        "Yerimde duramam, enerjim hiç bitmez.",
        "Farklı hobiler, farklı tatlar denemeye bayılırım.",
        "Sıkılmak benim en büyük düşmanımdır.",
        "Bazen ölçüyü kaçırıp aşırıya kaçabilirim (çok yemek, çok gezmek).",
        "Özgürlüğümün kısıtlanmasına asla gelemem.",
        "Stresliyken daldan dala atlar, hiçbir işi bitiremem.",
        "Rahatsam çok yaratıcı ve vizyoner olurum.",
        "Sevdiğim bir işse harikalar yaratırım ama sıkılırsam bırakırım.",
        "Acıdan, üzüntüden kaçmak için kendimi eğlenceye veririm.",
        "Bir güne çok fazla plan sığdırmaya çalışırım.",
        "Negatif ve sürekli şikayet eden insanlardan kaçarım.",
        "Aklıma bir fikir gelince hemen yapmak isterim.",
        "Mutluluk ve heyecan benim yakıtımdır."
    ],
    8: [
        "İstediğim şeyi almak için sonuna kadar mücadele ederim.",
        "Doğuştan liderimdir, yönetmeyi severim.",
        "Güçlü görünmek hoşuma gider, zayıflıktan nefret ederim.",
        "Mızmız ve kararsız insanlara tahammülüm yoktur.",
        "Yarışmayı ve kazanmayı severim, kaybetmek kitabımda yazmaz.",
        "Sevdiklerimi canım pahasına korurum, onlara laf ettirmem.",
        "İplerin elimde olmasını, kontrolün bende olmasını isterim.",
        "Saygı benim için sevgiden önce gelir.",
        "Risk almaktan korkmam, cesurumdur.",
        "Çok çalışırım, yorulmak nedir bilmem.",
        "Biri bana meydan okursa cevabını fazlasıyla alır.",
        "Lafı dolandırmam, neysem oyum, yüzüne söylerim.",
        "Bir grubun başına geçip organize etmekte iyiyimdir.",
        "Dobra konuşurum, bazen bu yüzden insanlar kırılabilir.",
        "Stresliyken çok baskıcı ve sinirli olabilirim.",
        "Rahatsam koca yürekli, koruyucu bir kahraman olurum.",
        "Duygularımı göstermeyi zayıflık olarak görürüm.",
        "Sadece gerçekten güvendiğim insanlara kalbimi açarım.",
        "Hayatı dolu dolu, yüksek sesle yaşamayı severim.",
        "Haksızlığa asla gelemem, hemen müdahale ederim."
    ],
    9: [
        "Kavgadan, gürültüden hiç hoşlanmam, huzur isterim.",
        "Herkes 'Çok sakinsin' der, kolay kolay sinirlenmem.",
        "İnsanları çok iyi dinlerim, herkesin derdini anlarım.",
        "Önemli işleri son ana kadar erteleyebilirim.",
        "Alışkanlıklarımı severim, düzenimin bozulmasını istemem.",
        "Karar vermek bana zor gelir, 'Fark etmez' demek daha kolaydır.",
        "Acele ettirilmekten nefret ederim, kendi hızımda gitmek isterim.",
        "Bazen detayları unuturum, dalgın olabilirim.",
        "Öfkemi içime atarım, dışarıya pek yansıtmam.",
        "Boş zamanımda hiçbir şey yapmadan uzanmayı severim.",
        "Evde vakit geçirmek, kendi halimde olmak hoşuma gider.",
        "Ortam gerilmesin diye alttan alırım.",
        "Birinin bana sürekli ne yapacağımı söylemesi beni inatçı yapar.",
        "Önemsiz işlerle oyalanıp asıl işi kaçırabilirim.",
        "Stresliyken pasifleşirim, hiçbir şey yapasım gelmez.",
        "Rahatsam çok üretken ve herkesi birleştiren biri olurum.",
        "Başkalarını memnun etmek için kendi isteğimden vazgeçebilirim.",
        "Çok fazla seçenek arasında kalmak beni yorar.",
        "Herkesle iyi geçinmeye çalışırım, düşmanım yoktur.",
        "Huzurlu ve sakin bir hayat hayalimdir."
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


# --- ENNEAGRAM PUANLAMA ---
def calculate_enneagram_report(all_answers):
    scores = {t: 0 for t in range(1, 10)}
    for q_id, val in all_answers.items():
        tip = int(q_id.split('_')[0])
        scores[tip] += val

    max_score = 20 * 5
    normalized = {t: round(s / max_score * 100, 1) for t, s in scores.items()}

    main_type = max(scores, key=scores.get)
    main_score = normalized[main_type]

    if main_type == 1:
        wings = [9, 2]
    elif main_type == 9:
        wings = [8, 1]
    else:
        wings = [main_type - 1, main_type + 1]

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


# ============================================================
# ANA APP FONKSİYONU
# ============================================================
def app():
    st.markdown("""
    <style>
        .test-card { background-color: #f8f9fa; border: 1px solid #ddd; border-radius: 10px; padding: 20px; margin-bottom: 15px; text-align: center; transition: 0.3s; cursor: pointer; }
        .test-card:hover { background-color: #e9ecef; border-color: #2E86C1; transform: translateY(-5px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .completed-badge { background-color: #d4edda; color: #155724; padding: 5px 10px; border-radius: 15px; font-size: 0.8em; font-weight: bold; }
        .main-header { color: #2E86C1; text-align: center; font-weight: bold; font-size: 2.5rem; margin-bottom: 10px; }
        .sub-header { color: #555; text-align: center; margin-bottom: 30px; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='main-header'>🏥 EĞİTİM KLİNİK MERKEZİ</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>Hoşgeldin, <b>{st.session_state.student_name}</b>. Kendini keşfetmeye hazır mısın?</div>", unsafe_allow_html=True)

    if "page" not in st.session_state:
        st.session_state.page = "home"

    ALL_TESTS = [
        "Enneagram Kişilik Testi",
        "Çalışma Davranışı Ölçeği (Baltaş)",
        "Sağ-Sol Beyin Dominansı Testi",
        "Sınav Kaygısı Ölçeği (DuSKÖ)",
        "VARK Öğrenme Stilleri Testi",
        "Çoklu Zeka Testi (Gardner)",
        "Holland Mesleki İlgi Envanteri (RIASEC)"
    ]

    # ============================================================
    # SAYFA 1: ANA MENÜ (HOME)
    # ============================================================
    if st.session_state.page == "home":
        st.markdown(f"## 👤 Merhaba, {st.session_state.student_name}")
        st.info("Aşağıdaki listeden dilediğin testi seçip çözebilirsin. Başarılar!")

        col1, col2 = st.columns(2)

        for idx, test in enumerate(ALL_TESTS):
            is_done = check_test_completed(st.session_state.student_id, test)
            target_col = col1 if idx % 2 == 0 else col2

            if is_done:
                target_col.button(f"✅ {test} (Tamamlandı)", disabled=True, key=test)
            else:
                if target_col.button(f"👉 {test}", type="primary", key=test):
                    st.session_state.selected_test = test
                    st.session_state.intro_passed = False

                    if "Enneagram" in test:
                        st.session_state.enneagram_type_idx = 1
                        st.session_state.enneagram_answers = {}
                        st.session_state.current_test_data = {"type": "enneagram_fixed"}

                    elif "Sağ-Sol Beyin" in test:
                        st.session_state.current_test_data = {"type": "ab_choice", "questions": SAG_SOL_BEYIN_QUESTIONS}
                        st.session_state.cevaplar = {}
                        st.session_state.sayfa = 0

                    elif "Çalışma Davranışı" in test:
                        st.session_state.current_test_data = {"type": "true_false", "questions": CALISMA_DAVRANISI_QUESTIONS}
                        st.session_state.cevaplar = {}
                        st.session_state.sayfa = 0

                    elif "Sınav Kaygısı" in test:
                        st.session_state.current_test_data = {"type": "true_false", "questions": SINAV_KAYGISI_QUESTIONS}
                        st.session_state.cevaplar = {}
                        st.session_state.sayfa = 0

                    elif "Çoklu Zeka" in test:
                        student_age = st.session_state.get('student_age', 15)
                        if student_age and student_age <= 13:
                            qs = []
                            for zk in ZEKA_SIRA:
                                qs.extend(COKLU_ZEKA_QUESTIONS_ILKOGRETIM[zk])
                            st.session_state.current_test_data = {"type": "coklu_zeka_ilk", "questions": qs}
                        else:
                            qs = []
                            for zk in ZEKA_SIRA:
                                qs.extend(COKLU_ZEKA_QUESTIONS_LISE[zk])
                            st.session_state.current_test_data = {"type": "coklu_zeka_lise", "questions": qs}
                        st.session_state.cevaplar = {}
                        st.session_state.sayfa = 0

                    elif "VARK" in test:
                        st.session_state.current_test_data = {"type": "vark_multi", "questions": VARK_QUESTIONS}
                        st.session_state.cevaplar = {}
                        st.session_state.sayfa = 0

                    elif "Holland" in test:
                        st.session_state.current_test_data = {"type": "holland_3", "questions": HOLLAND_QUESTIONS}
                        st.session_state.cevaplar = {}
                        st.session_state.sayfa = 0

                    st.session_state.page = "test"
                    st.rerun()

    # ============================================================
    # SAYFA 2: BAŞARI EKRANI
    # ============================================================
    elif st.session_state.page == "success_screen":
        st.markdown(
            "<div style='text-align:center; padding:40px;'>"
            "<h1>🎉 Harika İş Çıkardın!</h1>"
            "<p>Testi başarıyla tamamladın. Sonuçların öğretmenine iletildi.</p>"
            "</div>",
            unsafe_allow_html=True
        )

        if "last_report" in st.session_state and st.session_state.last_report:
            with st.expander("📋 Raporunu Görüntüle", expanded=True):
                st.markdown(st.session_state.last_report)

        st.markdown("---")
        c1, c2 = st.columns(2)
        if c1.button("🏠 Diğer Teste Geç"):
            st.session_state.page = "home"
            st.rerun()
        if c2.button("🚪 Çıkış Yap"):
            st.session_state.clear()
            st.rerun()

    # ============================================================
    # SAYFA 3: TEST ÇÖZME EKRANI
    # ============================================================
    elif st.session_state.page == "test":
        t_name = st.session_state.selected_test

        # --- GİRİŞ EKRANI ---
        if not st.session_state.intro_passed:
            st.title(f"📘 {t_name}")
            st.info("Lütfen tüm soruları içtenlikle cevapla. Doğru veya yanlış cevap yok, sadece SEN varsın.")
            if st.button("HAZIRIM, BAŞLA!", type="primary"):
                st.session_state.intro_passed = True
                st.rerun()

        # --- SORULAR ---
        else:
            data = st.session_state.current_test_data
            q_type = data.get("type")

            # ========================================
            # TİP: ENNEAGRAM
            # ========================================
            if q_type == "enneagram_fixed":
                curr_type = st.session_state.enneagram_type_idx
                questions = ENNEAGRAM_QUESTIONS[curr_type]

                st.progress(curr_type / 9)
                st.subheader(f"Bölüm {curr_type}: Tip {curr_type} Soruları")

                ennea_map = {
                    1: "Kesinlikle Katılmıyorum",
                    2: "Katılmıyorum",
                    3: "Kararsızım",
                    4: "Katılıyorum",
                    5: "Kesinlikle Katılıyorum"
                }
                opts = [1, 2, 3, 4, 5]

                all_answered = True
                for i, q_text in enumerate(questions):
                    q_key = f"{curr_type}_{i}"
                    st.write(f"**{i+1}. {q_text}**")
                    prev = st.session_state.enneagram_answers.get(q_key)
                    val = st.radio(
                        f"Soru {i+1}",
                        opts,
                        key=f"rad_{q_key}",
                        index=opts.index(prev) if prev else None,
                        horizontal=True,
                        format_func=lambda x: ennea_map[x],
                        label_visibility="collapsed"
                    )
                    if val:
                        st.session_state.enneagram_answers[q_key] = val
                    else:
                        all_answered = False
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
                                save_test_result_to_db(
                                    st.session_state.student_id,
                                    t_name,
                                    st.session_state.enneagram_answers,
                                    scores,
                                    rep
                                )
                                st.session_state.last_report = rep
                                st.session_state.page = "success_screen"
                                st.rerun()

            # ========================================
            # TİP: A/B SEÇİMLİ (Sağ-Sol Beyin)
            # DÜZELTME: q['option_a'] ve q['option_b'] yerine q['a'] ve q['b']
            # ========================================
            elif q_type == "ab_choice":
                qs = data["questions"]
                PER_PAGE = 10
                tot_p = (len(qs) + PER_PAGE - 1) // PER_PAGE
                start = st.session_state.sayfa * PER_PAGE
                curr_qs = qs[start:start + PER_PAGE]

                st.progress((st.session_state.sayfa + 1) / tot_p)
                page_q_ids = []

                for q in curr_qs:
                    qid = q["id"]
                    page_q_ids.append(qid)
                    st.write(f"**{qid}. {q['text']}**")

                    prev = st.session_state.cevaplar.get(qid)

                    # ✅ DÜZELTME: 'option_a'/'option_b' → 'a'/'b'
                    options = [f"a) {q['a']}", f"b) {q['b']}"]
                    idx = 0 if prev == "a" else (1 if prev == "b" else None)

                    val = st.radio(
                        f"Soru {qid}",
                        options,
                        key=f"q_{qid}",
                        index=idx,
                        horizontal=True,
                        label_visibility="collapsed"
                    )
                    if val:
                        st.session_state.cevaplar[qid] = "a" if val.startswith("a)") else "b"
                    st.divider()

                _navigate_pages(qs, page_q_ids, PER_PAGE, tot_p, t_name, q_type)

            # ========================================
            # TİP: DOĞRU/YANLIŞ (Çalışma Davranışı, Sınav Kaygısı)
            # ========================================
            elif q_type == "true_false":
                qs = data["questions"]
                PER_PAGE = 10
                tot_p = (len(qs) + PER_PAGE - 1) // PER_PAGE
                start = st.session_state.sayfa * PER_PAGE
                curr_qs = qs[start:start + PER_PAGE]

                st.progress((st.session_state.sayfa + 1) / tot_p)
                page_q_ids = []

                for q in curr_qs:
                    qid = q["id"]
                    page_q_ids.append(qid)
                    st.write(f"**{qid}. {q['text']}**")

                    prev = st.session_state.cevaplar.get(qid)
                    options = ["Doğru", "Yanlış"]
                    idx = 0 if prev == "D" else (1 if prev == "Y" else None)

                    val = st.radio(
                        f"Soru {qid}",
                        options,
                        key=f"q_{qid}",
                        index=idx,
                        horizontal=True,
                        label_visibility="collapsed"
                    )
                    if val:
                        st.session_state.cevaplar[qid] = "D" if val == "Doğru" else "Y"
                    st.divider()

                _navigate_pages(qs, page_q_ids, PER_PAGE, tot_p, t_name, q_type)

            # ========================================
            # TİP: ÇOKLU ZEKA LİSE (0-4 Likert)
            # ========================================
            elif q_type == "coklu_zeka_lise":
                qs = data["questions"]
                PER_PAGE = 10
                tot_p = (len(qs) + PER_PAGE - 1) // PER_PAGE
                start = st.session_state.sayfa * PER_PAGE
                curr_qs = qs[start:start + PER_PAGE]

                st.progress((st.session_state.sayfa + 1) / tot_p)
                page_q_ids = []

                likert_labels = {
                    0: "0 - Asla",
                    1: "1 - Çok Az",
                    2: "2 - Bazen",
                    3: "3 - Çoğu Kez",
                    4: "4 - Daima"
                }
                likert_opts = [0, 1, 2, 3, 4]

                for q in curr_qs:
                    qid = q["id"]
                    page_q_ids.append(qid)
                    st.write(f"**{qid}. {q['text']}**")

                    prev = st.session_state.cevaplar.get(qid)
                    idx = likert_opts.index(prev) if prev is not None else None

                    val = st.radio(
                        f"Soru {qid}",
                        likert_opts,
                        key=f"q_{qid}",
                        index=idx,
                        horizontal=True,
                        format_func=lambda x: likert_labels[x],
                        label_visibility="collapsed"
                    )
                    if val is not None:
                        st.session_state.cevaplar[qid] = val
                    st.divider()

                _navigate_pages(qs, page_q_ids, PER_PAGE, tot_p, t_name, q_type)

            # ========================================
            # TİP: ÇOKLU ZEKA İLKÖĞRETİM (Evet/Hayır)
            # ========================================
            elif q_type == "coklu_zeka_ilk":
                qs = data["questions"]
                PER_PAGE = 10
                tot_p = (len(qs) + PER_PAGE - 1) // PER_PAGE
                start = st.session_state.sayfa * PER_PAGE
                curr_qs = qs[start:start + PER_PAGE]

                st.progress((st.session_state.sayfa + 1) / tot_p)
                page_q_ids = []

                for q in curr_qs:
                    qid = q["id"]
                    page_q_ids.append(qid)
                    st.write(f"**{qid}. {q['text']}**")

                    prev = st.session_state.cevaplar.get(qid)
                    options = ["Evet", "Hayır"]
                    idx = 0 if prev == "E" else (1 if prev == "H" else None)

                    val = st.radio(
                        f"Soru {qid}",
                        options,
                        key=f"q_{qid}",
                        index=idx,
                        horizontal=True,
                        label_visibility="collapsed"
                    )
                    if val:
                        st.session_state.cevaplar[qid] = "E" if val == "Evet" else "H"
                    st.divider()

                _navigate_pages(qs, page_q_ids, PER_PAGE, tot_p, t_name, q_type)

            # ========================================
            # TİP: VARK (Çoklu Seçim)
            # ========================================
            elif q_type == "vark_multi":
                qs = data["questions"]
                PER_PAGE = 8
                tot_p = (len(qs) + PER_PAGE - 1) // PER_PAGE
                start = st.session_state.sayfa * PER_PAGE
                curr_qs = qs[start:start + PER_PAGE]

                st.progress((st.session_state.sayfa + 1) / tot_p)
                st.caption("💡 Her soruda birden fazla seçenek işaretleyebilirsin.")
                page_q_ids = []

                for q in curr_qs:
                    qid = q["id"]
                    page_q_ids.append(qid)
                    st.write(f"**{qid}. {q['text']}**")

                    prev = st.session_state.cevaplar.get(qid, [])
                    selected = []
                    for opt_key, opt_text in q["options"].items():
                        checked = opt_key in prev
                        if st.checkbox(f"{opt_key}) {opt_text}", value=checked, key=f"q_{qid}_{opt_key}"):
                            selected.append(opt_key)
                    st.session_state.cevaplar[qid] = selected
                    st.divider()

                _navigate_pages(qs, page_q_ids, PER_PAGE, tot_p, t_name, q_type)

            # ========================================
            # TİP: HOLLAND (Hoşlanırım/Fark etmez/Hoşlanmam)
            # ========================================
            elif q_type == "holland_3":
                qs = data["questions"]
                PER_PAGE = 10
                tot_p = (len(qs) + PER_PAGE - 1) // PER_PAGE
                start = st.session_state.sayfa * PER_PAGE
                curr_qs = qs[start:start + PER_PAGE]

                st.progress((st.session_state.sayfa + 1) / tot_p)
                page_q_ids = []

                holland_opts = ["😊 Hoşlanırım", "😐 Fark etmez", "😕 Hoşlanmam"]
                holland_score_map = {"😊 Hoşlanırım": 2, "😐 Fark etmez": 1, "😕 Hoşlanmam": 0}

                for q in curr_qs:
                    qid = q["id"]
                    page_q_ids.append(qid)
                    st.write(f"**{qid}. {q['text']}**")

                    prev = st.session_state.cevaplar.get(qid)
                    idx = {2: 0, 1: 1, 0: 2}.get(prev, None)

                    val = st.radio(
                        f"Soru {qid}",
                        holland_opts,
                        key=f"q_{qid}",
                        index=idx,
                        horizontal=True,
                        label_visibility="collapsed"
                    )
                    if val:
                        st.session_state.cevaplar[qid] = holland_score_map[val]
                    st.divider()

                _navigate_pages(qs, page_q_ids, PER_PAGE, tot_p, t_name, q_type)


# ============================================================
# SAYFA NAVİGASYONU + TEST BİTİRME (ORTAK FONKSİYON)
# ============================================================
def _navigate_pages(qs, page_q_ids, PER_PAGE, tot_p, t_name, q_type):
    """İleri/Geri navigasyon ve test bitirme mantığı."""
    c1, c2 = st.columns(2)

    if st.session_state.sayfa > 0:
        if c1.button("⬅️ Geri"):
            st.session_state.sayfa -= 1
            st.rerun()

    if st.session_state.sayfa < tot_p - 1:
        if c2.button("İleri ➡️"):
            missing = _check_missing(page_q_ids, q_type)
            if missing:
                st.error("⚠️ Bu sayfada boş bıraktığın sorular var. Onları doldurmadan geçemezsin. 😉")
            else:
                st.session_state.sayfa += 1
                st.rerun()
    else:
        if c2.button("Testi Bitir ✅", type="primary"):
            all_ids = [q["id"] for q in qs]
            missing = _check_missing(all_ids, q_type)
            if missing:
                st.error(f"⚠️ Eksik sorular var ({len(missing)} adet)! Lütfen kontrol et.")
            else:
                _finish_and_save(t_name, q_type)


def _check_missing(q_ids, q_type):
    """Cevaplanmamış soruları döndürür."""
    missing = []
    for qid in q_ids:
        ans = st.session_state.cevaplar.get(qid)
        if q_type == "vark_multi":
            if not ans:
                missing.append(qid)
        else:
            if ans is None:
                missing.append(qid)
    return missing


def _finish_and_save(t_name, q_type):
    """Testi puanla, raporu üret ve veritabanına kaydet."""
    answers = st.session_state.cevaplar
    scores = None
    report = ""

    with st.spinner("Sonuçların hesaplanıyor..."):

        if q_type == "ab_choice":
            result, report = calculate_sag_sol_beyin(answers)
            scores = {
                "sag_beyin":  result["sag_beyin"],
                "sol_beyin":  result["sol_beyin"],
                "sag_yuzde":  result["sag_yuzde"],
                "sol_yuzde":  result["sol_yuzde"],  # DÜZELTME: eksikti, öğretmen grafiği boş çıkıyordu
                "dominant":   result["dominant"],
                "level":      result["level"],
            }

        elif q_type == "true_false":
            if "Çalışma Davranışı" in t_name:
                result, report = calculate_calisma_davranisi(answers)
                scores = {
                    "total": result["total"],
                    "max_total": result["max_total"],
                    "categories": result["categories"]
                }
            elif "Sınav Kaygısı" in t_name:
                result, report = calculate_sinav_kaygisi(answers)
                scores = {
                    "total": result["total"],
                    "total_pct": result["total_pct"],
                    "level": result["overall_level"],
                    "categories": result["categories"]
                }

        elif q_type == "coklu_zeka_lise":
            result, report = calculate_coklu_zeka_lise(answers)
            scores = {zk: result["scores"][zk]["pct"] for zk in result["scores"]}

        elif q_type == "coklu_zeka_ilk":
            result, report = calculate_coklu_zeka_ilkogretim(answers)
            scores = {zk: result["scores"][zk]["pct"] for zk in result["scores"]}

        elif q_type == "vark_multi":
            result, report = calculate_vark(answers)
            scores = {
                "V": result["counts"]["V"],
                "A": result["counts"]["A"],
                "R": result["counts"]["R"],
                "K": result["counts"]["K"],
                "dominant": result["dominant"][0]
            }

        elif q_type == "holland_3":
            result, report = calculate_holland(answers)
            # DÜZELTME: result["percentages"] yoktur, doğrudan key'ler kullanılıyor
            scores = {
                "R": result["R"],
                "I": result["I"],
                "A": result["A"],
                "S": result["S"],
                "E": result["E"],
                "C": result["C"],
                "holland_code": result["holland_code"],
            }

        save_test_result_to_db(st.session_state.student_id, t_name, answers, scores, report)

        st.session_state.last_report = report
        st.session_state.page = "success_screen"
        st.rerun()
