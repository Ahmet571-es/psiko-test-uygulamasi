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
    1: {
        "title": "Tip 1: Reformcu",
        "role": "Mükemmeliyetçi, Düzenleyici",
        "icon": "⚖️",
        "fear": "Hata yapmak, yozlaşmak ve kusurlu olmak.",
        "desire": "Doğruyu yapmak, iyi ve ahlaklı bir insan olmak.",
        "stress": 4, "growth": 7,
        "desc": (
            "Sen dünyaya 'Doğru olan şeyi yapmalıyız' gözlüğüyle bakıyorsun. "
            "İçinde adeta sürekli çalışan bir 'iç ses' var — bu ses sana nelerin "
            "daha iyi, daha doğru, daha adil olabileceğini fısıldıyor. "
            "Bu yüzden hem kendin hem de çevreni sürekli geliştirmeye çalışıyorsun. "
            "Titizliğin, dürüstlüğün ve etik değerlere bağlılığın seni gerçek anlamda "
            "güvenilir bir insan yapıyor. Ancak bu iç ses bazen çok gürültülü hale gelip "
            "seni kendinle ve başkalarıyla barışık olmaktan alıkoyabiliyor."
        ),
        "strengths": [
            "Güçlü etik değerleri ve ilkeleri — söz verdiğinde tutarsın",
            "Titizlik ve dikkat — işlerin ayrıntılarını başkalarının gözünden kaçmayacak şekilde görürsün",
            "Adalet duygusu — haksızlığa karşı durmaktan çekinmezsin",
            "Sorumluluk sahibi — üstlendiğin işi sonuna kadar götürürsün",
            "Öz disiplin — hedeflerine ulaşmak için kendini motive edebilirsin",
        ],
        "weaknesses": [
            "Mükemmeliyetçilik seni felç edebilir — 'ya tam olacak ya hiç' tuzağına düşebilirsin",
            "Eleştirel iç ses yorucu olabilir — hem kendinle hem başkalarıyla çok sert olabilirsin",
            "Sert ve esnek olmayan tutum — kurallara sıkı bağlılık bazen ilişkileri zorlar",
            "Öfkeyi bastırma — adaletsizlik karşısında duyduğun öfkeyi içe atarsın",
            "Gri alanlarla başa çıkmakta zorlanma — her şeyin siyah-beyaz olmadığını kabullenmek zor gelebilir",
        ],
        "work_style": (
            "Net kuralları, standartları ve beklentileri olan yapılandırılmış ortamlarda parlıyorsun. "
            "Kalite kontrol, hukuk, eğitim, tıp, muhasebe gibi titizlik ve etik gerektiren alanlarda "
            "doğal olarak güçlüsün. Kaotik veya kuralsız ortamlar seni strese sokar."
        ),
        "relationship_style": (
            "İlişkilerinde dürüstlük, sadakat ve tutarlılık ararsın. Söz verilip tutulmaması "
            "veya haksızlık seni derinden yaralar. Bazen yüksek beklentilerin "
            "partnerin veya arkadaşların üzerinde baskı oluşturabilir. "
            "Sevildiğini görmek için 'mükemmel' olmana gerek olmadığını hatırlatmak gerekiyor."
        ),
        "stress_behavior": (
            "Stres altında Tip 4'e (Bireyci) kayarsın: melankolik, kendini geri çeken, "
            "duygusal açıdan kapalı biri haline gelebilirsin. Eleştirini kendinee yöneltirsin "
            "ve 'Hiçbir şeyi doğru yapamıyorum' hissine kapılabilirsin."
        ),
        "growth_behavior": (
            "Gelişim yolunda Tip 7'ye (Hevesli) yönelirsin: daha oyuncu, daha esnek "
            "ve daha neşeli biri olursun. Hayatın güzelliklerini fark edip, "
            "'Yeterince iyi' diyebildiğinde gerçek huzuru bulursun."
        ),
        "danger_signals": [
            "Her şeyi ve herkesi sürekli düzeltme ihtiyacı hissetmek",
            "Dinginlik yerine sürekli gerginlik içinde olmak",
            "Öfkeni 'ince alınganlık' veya soğukluk olarak dışa vurmak",
            "'Ben daha iyi biliyorum' tavrıyla ilişkileri zorlamak",
        ],
        "prescription": [
            "🌿 Kendinle barış: Hata yapmak insani bir durum. Bugün bilerek küçük bir hata yap ve nasıl hissettiğini izle.",
            "🎭 Espri ve oyun: Haftada en az bir kez 'verimli' olmayan, sadece eğlenceli bir şey yap.",
            "🤍 Takdir et: Bugün hem kendin hem de çevrende üç şeyin 'yeterince iyi' olduğunu fark et.",
            "🗣️ Öfkeni ifade et: Öfkeni içine atmak yerine, güvendiğin birine sakin bir şekilde ilet.",
        ],
        "famous_examples": "Mahatma Gandhi, Nelson Mandela, Meryl Streep",
        "careers": ["Hukukçu", "Doktor", "Muhasebeci", "Eğitimci", "Etik danışmanı", "Kalite uzmanı"],
    },
    2: {
        "title": "Tip 2: Yardımcı",
        "role": "Şefkatli, İlgi Gösteren",
        "icon": "🤗",
        "fear": "İstenmemek, sevilmemek ve değersiz hissedilmek.",
        "desire": "Sevilmek, ihtiyaç duyulmak ve başkaları için önemli olmak.",
        "stress": 8, "growth": 4,
        "desc": (
            "Sen dünyaya 'İnsanlara yardım etmeli ve onları sevmeliyim' gözlüğüyle bakıyorsun. "
            "Başkalarının ihtiyaçlarını kendi ihtiyaçlarından önce görme konusunda adeta "
            "bir antene sahipsin — odaya girer girmez kimin üzgün olduğunu, kimin desteğe "
            "ihtiyaç duyduğunu hissedebilirsin. Bu empatin ve cömertliğin seni "
            "insanların çok değer verdiği biri yapıyor. Ancak bazen kendi ihtiyaçlarını "
            "o kadar arka plana atıyorsun ki, zamanla tükenmişlik ve kırgınlık sinyalleri "
            "vermeye başlayabiliyor."
        ),
        "strengths": [
            "Derin empati — başkalarının hislerini adeta kendi hislerin gibi anlarsın",
            "Koşulsuz destek — zor anlarda yanında olmak için elinden geleni yaparsın",
            "Sosyal zeka — insanları bir araya getirme ve ilişkileri güçlendirme konusunda üstünsün",
            "Cömertlik — sahip olduklarını başkalarıyla paylaşmaktan içtenlikle mutluluk duyarsın",
            "Sıcaklık ve bağlanma — insanların sana güven duymasını ve açılmasını sağlarsın",
        ],
        "weaknesses": [
            "'Hayır' diyememek — başkasını hayal kırıklığına uğratmamak için kendi sınırlarını aşarsın",
            "Kendi ihtiyaçlarını görmezden gelme — 'Ben iyiyim' demeye alışkın ama bazen değilsin",
            "Takdir görmek isteme — iyiliğin fark edilmediğinde kırılgan hissedebilirsin",
            "Duygusal manipülasyon riski — bilinçsizce suçluluk veya borçluluk hissi yaratabilirsin",
            "Başkalarına bağımlılık — ilişkilerdeki rolün kaybolursa kimlik krizi yaşayabilirsin",
        ],
        "work_style": (
            "İnsan odaklı, ilişki kurma gerektiren işlerde parıldıyorsun. "
            "Sağlık, eğitim, sosyal hizmet, danışmanlık ve insan kaynakları gibi alanlarda "
            "doğal olarak güçlüsün. Soğuk, bireysel ve rekabetçi ortamlar seni yorar."
        ),
        "relationship_style": (
            "İlişkilerinde derin bağ ve karşılıklı şefkat ararsın. Sevdiğin insanın "
            "ihtiyaçlarını sezmek sana doğal gelir. Ancak kendi ihtiyaçlarını dile getirmekte "
            "zorlanır ve birikmiş beklentilerin sıtem olarak çıkabilir. "
            "En sağlıklı ilişki: sevilmek için yardım etmediğin, "
            "sadece sevdiğin için yardım ettiğin ilişkidir."
        ),
        "stress_behavior": (
            "Stres altında Tip 8'e (Meydan Okuyan) kayarsın: kontrolcü, yüzleşmeci "
            "ve talep edici hale gelebilirsin. 'Senden bu kadar şey yaptım, neden fark etmiyorsun?' "
            "tepkileri verebilirsin."
        ),
        "growth_behavior": (
            "Gelişim yolunda Tip 4'e (Bireyci) yönelirsin: kendi duygularını ve ihtiyaçlarını "
            "keşfetmeye başlarsın. Başkalarına olan ilgin kadar kendine de ilgi gösterdiğinde "
            "hem daha mutlu hem daha otantik olursun."
        ),
        "danger_signals": [
            "Sürekli başkalarının ihtiyaçlarını düşünüp kendi ihtiyaçlarını bastırmak",
            "'Beni kimse görmüyor' hissiyle içten içe kırılmak",
            "Yardımını takdir etmeyeni pasif-agresif yollarla cezalandırmak",
            "Tükenmişliği inkâr ederek daha fazla vermeye çalışmak",
        ],
        "prescription": [
            "🌱 Kendin için bir şey yap: Bu hafta yalnızca senin için, kimseye faydası olmayan bir şey yap.",
            "🗣️ İhtiyacını dile getir: Bugün birine 'Benim de desteğe ihtiyacım var' de.",
            "⛔ Hayır pratiği: Bu hafta bir talebi reddet — ve suçluluk duymak yerine sınırını izle.",
            "🪞 İçe dön: 'Ben şu an ne hissediyorum? Benim ihtiyacım ne?' sorularını sık sor.",
        ],
        "famous_examples": "Desmond Tutu, Princess Diana, Dolly Parton",
        "careers": ["Hemşire", "Psikolog", "Öğretmen", "Sosyal hizmet uzmanı", "İK yöneticisi", "Terapist"],
    },
    3: {
        "title": "Tip 3: Başarılı",
        "role": "Odaklı, Performansçı",
        "icon": "🏆",
        "fear": "Başarısız olmak, değersiz ve sıradan görünmek.",
        "desire": "Başarılı, değerli ve hayranlık duyulan biri olmak.",
        "stress": 9, "growth": 6,
        "desc": (
            "Sen dünyaya 'Başarılı olmalı ve değer kanıtlamalıyım' gözlüğüyle bakıyorsun. "
            "Hedef koymak, strateji geliştirmek ve o hedefe doğru ilerlemek seni canlı tutuyor. "
            "Odaya girdiğinde enerjin hissedilir, insanları motive etme konusunda doğal bir yeteneğin var. "
            "İmajına ve nasıl göründüğüne dikkat ediyorsun — bu bazen avantaj, bazen kırılganlık. "
            "En büyük sorduğun soru şu: 'Başarmazsam hâlâ sevilir miyim?'"
        ),
        "strengths": [
            "Hedef odaklılık — belirlediğin hedefe kilitlenip ilerleyebilirsin",
            "Enerji ve motivasyon — çevreyi de sürüklediğin bir dinamizmin var",
            "Adaptasyon yeteneği — farklı ortamlara ve insanlara hızla uyum sağlarsın",
            "Verimlilik — en kısa yoldan sonuç üretme konusunda güçlüsün",
            "Liderlik karizması — insanlara ilham vermek sana doğal gelir",
        ],
        "weaknesses": [
            "Kimlik-başarı karışıklığı — başardıklarının ötesinde kim olduğunu sorgulamayabilirsin",
            "Duyguları erteleme — 'Bunu daha sonra hissederim, şimdi iş var' tuzağı",
            "İlişkileri proje gibi yönetme riski — empati yerine strateji ön plana çıkabilir",
            "İmaj kaygısı — gerçek kırılganlıklarını gizleme eğilimi",
            "Aşırı iş yükü — 'Daha fazlası' peşinde tükenmişliğe gidebilirsin",
        ],
        "work_style": (
            "Rekabetçi, ölçülebilir başarı kriterleri olan ve görünürlük sunan ortamlarda "
            "parıldıyorsun. Satış, girişimcilik, yöneticilik, halkla ilişkiler ve "
            "sahne sanatları gibi alanlarda doğal gücün ortaya çıkar. "
            "Takdir edilmediğin veya ilerleme göremediğin ortamlar seni söndürür."
        ),
        "relationship_style": (
            "İlişkilerinde hayranlık ve takdir önemlidir. Başarılarını paylaşmak istersin "
            "ama gerçek kırılganlıklarını göstermek zor gelir. "
            "En derin bağı, 'maskesini düşürebildiğin' insanlarla kurarsın. "
            "Partnerinin seni sadece başarıların için değil, gerçekten sevdiğini hissetmek istersin."
        ),
        "stress_behavior": (
            "Stres altında Tip 9'a (Barışçı) kayarsın: hareketsizleşir, "
            "erteleyebilir ve içine kapanabilirsin. 'Ne fark eder ki' hissiyle "
            "motivasyonunu kaybedebilirsin."
        ),
        "growth_behavior": (
            "Gelişim yolunda Tip 6'ya (Sadık) yönelirsin: daha sadık, dürüst ve "
            "gerçekten işbirlikçi olursun. Başarının ötesinde, anlam ve bağlılık arayışına girersin."
        ),
        "danger_signals": [
            "Dinlenmenin boşa harcanan zaman gibi gelmesi",
            "Başarısızlık ya da eleştiri karşısında aşırı savunmacı olmak",
            "Gerçek hislerini 'verimli olmayan bir şey' olarak görmek",
            "İlişkilerde derinlik yerine statüyü ön plana koymak",
        ],
        "prescription": [
            "🧘 Dur ve hisset: Her gün 5 dakika, gündemin dışında, sadece 'Ne hissediyorum?' diye sor.",
            "🎭 Maske indir: Güvendiğin birine 'Ben aslında şu an zor bir dönemdeyim' de.",
            "🏅 Başarısız olmayı dene: Küçük bir şeyde bilerek mükemmeliyetçiliği bırak.",
            "❤️ Koşulsuz bağ: Bu hafta hiçbir başarını paylaşmadan, sadece var olarak birisiyle zaman geçir.",
        ],
        "famous_examples": "Oprah Winfrey, Tom Cruise, Taylor Swift",
        "careers": ["Girişimci", "Satış müdürü", "Aktör/Sunucu", "Pazarlama uzmanı", "Yönetici", "Koç"],
    },
    4: {
        "title": "Tip 4: Bireyci",
        "role": "Romantik, Özgün",
        "icon": "🎨",
        "fear": "Kimliği olmamak, sıradan ve anlamsız biri olmak.",
        "desire": "Kendine özgü, anlamlı ve otantik bir kimliğe sahip olmak.",
        "stress": 2, "growth": 1,
        "desc": (
            "Sen dünyaya 'Ben farklıyım ve bu farkı anlamlı kılmalıyım' gözlüğüyle bakıyorsun. "
            "Duyguların yoğunluğu ve derinliği seni hem çok zengin hem de bazen çok ağır bir iç dünyaya sürüklüyor. "
            "Güzelliği, anlamı ve özgünlüğü sıradan insanların göremediği yerlerde görebilirsin. "
            "Sanat, müzik, edebiyat veya derin konuşmalar sana nefes aldırıyor. "
            "En büyük paradoks: hem çok özel hissetmek hem de gerçekten anlaşılmak istemek."
        ),
        "strengths": [
            "Derin duygusal zeka — başkalarının hissedemediği nüansları hissedersin",
            "Yaratıcılık ve estetik duyarlılık — güzelliği görme ve yaratma konusunda üstünsün",
            "Otantiklik — rol yapmayı reddeder, gerçek olan şeyi ararsin",
            "Empati derinliği — acı çeken birinin yanında gerçekten var olabilirsin",
            "Anlam arayışı — yüzeysel şeylerle yetinmez, derinliği ararsın",
        ],
        "weaknesses": [
            "Melankoli ve hüzne gömülme — duygular bazen seni tüketebilir",
            "Kendini eksik hissetme — başkalarının sahip olduklarına bakıp 'Ya ben?' diyebilirsin",
            "Dramatizasyon eğilimi — olayları olduğundan daha ağır yaşayabilirsin",
            "Günlük rutine direnç — sıradan görevler seni sıkıp boğabilir",
            "İlişkilerde idealizm — hayal kırıklığına karşı çok kırılgansın",
        ],
        "work_style": (
            "Yaratıcı özgürlük sunan, anlam ve estetik barındıran işlerde parıldıyorsun. "
            "Sanat, tasarım, yazarlık, terapistlik, müzik ve moda gibi alanlarda "
            "eşsiz bir katkı sunarsın. Monoton, kurumsal ve duygusuz ortamlar seni içten söndürür."
        ),
        "relationship_style": (
            "Derin, tutkulu ve anlam dolu bağlar ararsın. Yüzeysel ilişkiler seni tatmin etmez. "
            "Anlaşılma ve görülme ihtiyacın çok güçlüdür. Hayal kırıklığı yaşadığında "
            "mesafe koyabilir ya da dramatik tepkiler verebilirsin. "
            "En iyi ilişki: seni olduğun gibi görebilen biriyle kurduğun bağdır."
        ),
        "stress_behavior": (
            "Stres altında Tip 2'ye (Yardımcı) kayarsın: ihtiyaçlarını bastırıp "
            "başkalarına aşırı yönelir, sevilmeye çalışır ve duygusal bağımlılık geliştirebilirsin."
        ),
        "growth_behavior": (
            "Gelişim yolunda Tip 1'e (Reformcu) yönelirsin: disiplin ve yapıya kavuşur, "
            "yaratıcılığını somut eylemlere dönüştürebilirsin. Duygular seni tanımlamak yerine sana hizmet etmeye başlar."
        ),
        "danger_signals": [
            "Uzun süre hüzün veya boşluk içinde kalmak",
            "Başkalarını idealleştirip sonra yıkılmak",
            "Günlük hayattan ve sorumluluklardan kaçmak",
            "'Beni kimse gerçekten anlamıyor' düşüncesiyle izolasyona çekilmek",
        ],
        "prescription": [
            "🌱 Rutini benimse: Her gün küçük bir rutin oluştur — vücudun ve zihni çapalar.",
            "🚶 Bedenle bağlan: Duygu yoğunluğunda yürüyüş yap, nefes al, bedenine geri dön.",
            "📓 Minnet listesi: Her gün sahip olduğun üç şeyi yaz — eksikliğe değil, varlığa odaklan.",
            "🛠️ Tamamla: Yarım kalan yaratıcı bir projeyi bu hafta bitir.",
        ],
        "famous_examples": "Frida Kahlo, Virginia Woolf, Bob Dylan",
        "careers": ["Sanatçı", "Yazar", "Terapist", "Tasarımcı", "Müzisyen", "Fotoğrafçı"],
    },
    5: {
        "title": "Tip 5: Araştırmacı",
        "role": "Gözlemci, Uzman",
        "icon": "🔬",
        "fear": "Yetersiz olmak, kaynaklarının tükenmesi ve insanların istilasına uğramak.",
        "desire": "Yetkin, bilgili ve çevresini anlayan biri olmak.",
        "stress": 7, "growth": 8,
        "desc": (
            "Sen dünyaya 'Önce anlamalıyım, sonra hareket ederim' gözlüğüyle bakıyorsun. "
            "Zihnin sürekli merakla dolu — bir konuyu en ince detayına kadar araştırmak "
            "sana güvenlik ve zevk verir. Yalnızlık seni yıkmaz, aksine şarj eder. "
            "Enerjini, zamanını ve bilgini dikkatle paylaşırsın. "
            "Gözlemlemek ve analiz etmek eylemden daha rahat gelir. "
            "Zihnin muhteşem ama bazen seni hayattan uzaklaştırabilir."
        ),
        "strengths": [
            "Derin analitik düşünme — karmaşık konuları anlama ve açıklama konusunda üstünsün",
            "Uzmanlık — ilgi alanında derinlemesine bilgi biriktirir, gerçek bir uzman olursun",
            "Bağımsızlık — kendi başına çalışabilir ve kararlarını verebilirsin",
            "Gözlem gücü — diğerlerinin fark etmediği detayları ve örüntüleri görürsün",
            "Sakinlik — kriz anlarında soğukkanlılığını korursun",
        ],
        "weaknesses": [
            "İzolasyon — insanlardan ve sosyal bağlardan kendiğini geri çekebilirsin",
            "Eylemden kaçınma — 'Biraz daha araştırayım' derken harekete geçmeyi erteleyebilirsin",
            "Duygusal kopukluk — hisleri doğrudan yaşamak yerine analiz etmeyi tercih edersin",
            "Cimrilik (enerji/bilgi/zaman) — kaynaklarını paylaşmak güç gelebilir",
            "Sosyal yorgunluk — kalabalık ortamlar seni tüketir",
        ],
        "work_style": (
            "Bağımsız çalışma, derin düşünme ve uzmanlık gerektiren ortamlarda güçlüsün. "
            "Bilim, teknoloji, felsefe, araştırma, yazarlık ve mühendislik gibi alanlarda "
            "doğal avantajın var. Açık ofis, sürekli toplantı ve yoğun sosyal dinamikler seni yorar."
        ),
        "relationship_style": (
            "Bağımsızlığına saygı duyan, entelektüel derinliği olan birini ararsın. "
            "Hislerini doğrudan ifade etmek zor gelir, duygularını genellikle davranışlarla gösterirsin. "
            "Aşırı talep veya yakınlık baskısı seni kaçışa iter. "
            "En derin bağ: seni içine çekildiğinde yargılamayan biriyle kurduğun bağdır."
        ),
        "stress_behavior": (
            "Stres altında Tip 7'ye (Hevesli) kayarsın: dağınık, hiperaktif ve "
            "konsantre olamayan biri haline gelebilirsin. Düşünceler çok hızlı akar, "
            "hiçbiri derinleşemez."
        ),
        "growth_behavior": (
            "Gelişim yolunda Tip 8'e (Meydan Okuyan) yönelirsin: harekete geçer, "
            "güçlü kararlar alır ve liderlik edebilirsin. Zihin ile eylem birleştiğinde "
            "gerçek potansiyelini ortaya çıkarırsın."
        ),
        "danger_signals": [
            "Günlerce veya haftalarca insanlardan uzak kalmak",
            "Bilgi toplamayı eyleme tercih etmek",
            "Hisleri hissetmek yerine analiz etmek",
            "Sosyal iletişimi gereksiz enerji kaybı olarak görmek",
        ],
        "prescription": [
            "🤝 Bağlan: Bu hafta biriyle sıradan ama gerçek bir sohbet yap — amacı yok, sadece bağlantı.",
            "⚡ Harekete geç: 'Yeterince hazır hissettim' demeden küçük bir adım at.",
            "💬 Hislerini söyle: Güvendiğin birine bir duygundan bahset, analiz etmeden.",
            "🌍 Dışarı çık: Her gün en az 20 dakika dışarıda, insanların arasında ol.",
        ],
        "famous_examples": "Albert Einstein, Stephen Hawking, Bill Gates",
        "careers": ["Araştırmacı", "Yazılımcı", "Mühendis", "Analist", "Akademisyen", "Yazar"],
    },
    6: {
        "title": "Tip 6: Sadık",
        "role": "Sorgulayıcı, Güvenilir",
        "icon": "🛡️",
        "fear": "Güvensizlik, yalnız kalmak ve desteğini kaybetmek.",
        "desire": "Güvende olmak, güvenilir ilişkilere ve yapılara sahip olmak.",
        "stress": 3, "growth": 9,
        "desc": (
            "Sen dünyaya 'Güvende miyim? Güvenebilir miyim?' gözlüğüyle bakıyorsun. "
            "Tehditleri önceden görmek, olası riskleri hesaplamak ve en kötü senaryoya "
            "hazırlıklı olmak seni güvende tutmak için geliştirdiğin doğal bir refleks. "
            "Bu sayede inanılmaz derecede sadık, sorumluluk sahibi ve güvenilirsin. "
            "Bir kez güvenilirliğini kanıtladıysan yanından ayrılmazsın. "
            "Ancak zihnindeki 'ya olursa?' sesi bazen seni yorabilir."
        ),
        "strengths": [
            "Sadakat — bağlı olduğun insanlar ve değerler için sonuna kadar dururun",
            "Sorumluluk — üstlendiğin işi sonuna kadar götürür, sözünü tutarsın",
            "Risk analizi — tehlikeleri önceden görmek konusunda keskin bir sezgin var",
            "Ekip ruhu — grup içinde güven inşa etme ve herkesin iyiliğini düşünme konusunda güçlüsün",
            "Soru sorma cesareti — otoriteyi körü körüne kabul etmezsin, sorgularsın",
        ],
        "weaknesses": [
            "Aşırı kaygı — zihin sürekli olası tehlikeleri tarıyor olabilir",
            "Kararsızlık — 'Ya yanlış karar verirsem?' korkusuyla kilitlenebilirsin",
            "Güvensizlik — insanların niyetini test etme eğilimin ilişkileri zorlayabilir",
            "Felaket senaryoları — küçük sorunları kafanda büyütebilirsin",
            "Otoriteyle çelişki — hem otoriteye ihtiyaç duyar hem de ona şüpheyle bakarsın",
        ],
        "work_style": (
            "Net roller, güvenilir yapılar ve açık beklentilerin olduğu ortamlarda güçlüsün. "
            "Risk yönetimi, hukuk, güvenlik, finans, sağlık ve kriz yönetimi gibi alanlarda "
            "değerli katkı sunarsın. Kaotik, belirsiz ve güvensiz ortamlar seni tüketir."
        ),
        "relationship_style": (
            "Sadakat ve güven senin için ilişkinin temeli. Güvendiğin birinin seni hayal kırıklığına uğratması "
            "çok derinden etkiler. Test etme eğilimin — sordukların, yokladıkların — "
            "bazen fark edilmeden ilişkiye yük olabilir. "
            "En iyi ilişki: güvenilirliğini kanıtlamış, tutarlı ve seni yargılamayan biriyle."
        ),
        "stress_behavior": (
            "Stres altında Tip 3'e (Başarılı) kayarsın: aşırı çalışır, performans odaklı olur "
            "ve kontrolü ele geçirmeye çalışırsın. Kaygını başarı veya meşguliyet ile örtbas edersin."
        ),
        "growth_behavior": (
            "Gelişim yolunda Tip 9'a (Barışçı) yönelirsin: zihin sakinleşir, "
            "içgüdülerine güvenmeye başlarsın. Kaygı yerine huzur merkezinden hareket edersin."
        ),
        "danger_signals": [
            "Sürekli kötü senaryo düşünerek karar verememek",
            "Güvendiğin insanları bile sürekli test etmek",
            "Fiziksel belirtiler (mide ağrısı, baş ağrısı) olarak taşınan kaygı",
            "Otoriteye hem muhtaç hem de öfkeli hissetmek",
        ],
        "prescription": [
            "🧘 Zihni durdur: 'Bu düşünce gerçek mi yoksa senaryo mu?' diye sor.",
            "💪 İçgüdüne güven: Bir kararda aklını değil, ilk hissini rehber al.",
            "✅ Tamamlananları gör: Bugün neyin yolunda gittiğine odaklan, neyin bozulabileceğine değil.",
            "🤲 Destek iste: Kaygını birisiyle paylaş — yalnız taşımak onu büyütür.",
        ],
        "famous_examples": "Barack Obama, Ellen DeGeneres, Malala Yousafzai",
        "careers": ["Avukat", "Risk analisti", "Güvenlik uzmanı", "Muhasebeci", "Polis memuru", "Danışman"],
    },
    7: {
        "title": "Tip 7: Hevesli",
        "role": "Maceracı, Vizyoner",
        "icon": "🚀",
        "fear": "Acı çekmek, kısıtlanmak ve eğlencesiz bir hayata mahkûm olmak.",
        "desire": "Mutlu, özgür ve doyumsuz bir hayat sürmek.",
        "stress": 1, "growth": 5,
        "desc": (
            "Sen dünyaya 'Hayat güzel olmalı ve ben her şeyi deneyimlemeliyim' gözlüğüyle bakıyorsun. "
            "Enerji, iyimserlik ve merak senin doğal halin. "
            "Yeni fikirler, maceralar ve olasılıklar seni canlı tutuyor. "
            "Bir kapı kapanırken on yeni kapı görürsün ve içinden en az üçüne girmek istersin. "
            "Bu enerjin çevreni de aydınlatıyor — seninle olmak genellikle eğlenceli ve canlandırıcı. "
            "Ancak zorluklardan ve acıdan kaçma eğilimin bazen derinleşmeni engelleyebilir."
        ),
        "strengths": [
            "Sınır tanımayan iyimserlik — en zor durumlarda bile çıkış yolu görebilirsin",
            "Hızlı öğrenme — yeni konuları ve becerileri süratle kavrayabilirsin",
            "Yaratıcılık ve yenilikçilik — farklı alanları bağlayan yaratıcı çözümler üretirsin",
            "Enerji ve coşku — çevrendekileri harekete geçirir ve motive edersin",
            "Esneklik — planlar değiştiğinde hızla adapte olabilirsin",
        ],
        "weaknesses": [
            "Odaklanma güçlüğü — çok fazla şeye başlayıp bitiremeyebilirsin",
            "Acıdan kaçma — zor duyguları şenlik veya hareketle örtbas edebilirsin",
            "Söz vermek ama tutamamak — heyecanla verdiğin sözleri gerçekleştirmek zor gelebilir",
            "Derinleşme güçlüğü — yüzeyden yüzeye atlamak derinliği zorlaştırır",
            "Anlık tatmin — uzun vadeli sabır gerektiren işler seni zorlayabilir",
        ],
        "work_style": (
            "Çeşitlilik, yaratıcılık ve hareket sunan ortamlarda parıldıyorsun. "
            "Girişimcilik, medya, turizm, eğlence, yaratıcı sektörler ve eğitim gibi alanlarda "
            "doğal gücün ortaya çıkar. Monoton, tekrarlı ve kısıtlayıcı ortamlar seni boğar."
        ),
        "relationship_style": (
            "Eğlenceli, spontane ve macera dolu ilişkiler ararsın. "
            "Rutinleşen veya ağır bir hale gelen ilişkilerden uzaklaşma eğilimin var. "
            "Zorlu bir konuşmayı espriye vurmak veya ertelemek senin için kolay. "
            "En iyi ilişki: seni hem eğlenceli hem derin olmaya teşvik eden biriyle."
        ),
        "stress_behavior": (
            "Stres altında Tip 1'e (Reformcu) kayarsın: aşırı eleştirel, mükemmeliyetçi "
            "ve sabırsız hale gelebilirsin. Her şeyi yanlış bulan, sert biri gibi görünürsün."
        ),
        "growth_behavior": (
            "Gelişim yolunda Tip 5'e (Araştırmacı) yönelirsin: derinleşir, "
            "tek bir şeye uzun süre odaklanabilir ve gerçek uzmanlık geliştirebilirsin. "
            "Hızın yavaşlayınca hayatın zenginliğini daha derinden tadabilirsin."
        ),
        "danger_signals": [
            "Projeleri, ilişkileri veya sözleri yarım bırakmak",
            "Yalnız kaldığında huzursuzluk yerine sürekli meşguliyet arayışı",
            "Duygusal derinlikten kaçmak için hareket ve eğlenceye sığınmak",
            "Uzun vadeli bir şeye bağlanmaktan kaçınmak",
        ],
        "prescription": [
            "🎯 Bir şeyi bitir: Bu hafta yarım kalan bir şeyi tamamla — küçük olsun ama bütün olsun.",
            "🌑 Karanlıkla otur: Zor bir duygunun yanında 10 dakika kal — kaçmadan, çözmeye çalışmadan.",
            "📅 Derinleş: İlgi duyduğun bir konuya yüzeysel değil, gerçekten derinlemesine gir.",
            "🤝 Söz tut: Bu hafta verdiğin bir sözü eksiksiz yerine getir.",
        ],
        "famous_examples": "Robin Williams, Jim Carrey, Freddie Mercury",
        "careers": ["Girişimci", "Medya profesyoneli", "Rehber/Eğitimci", "Komedyen", "Turizm uzmanı"],
    },
    8: {
        "title": "Tip 8: Meydan Okuyan",
        "role": "Lider, Koruyucu",
        "icon": "⚡",
        "fear": "Kontrol edilmek, manipüle edilmek ve zayıf görünmek.",
        "desire": "Kendi hayatını kontrol etmek, güçlü ve bağımsız olmak.",
        "stress": 5, "growth": 2,
        "desc": (
            "Sen dünyaya 'Ben güçlü olmalıyım ve kontrol bendeyken herkes güvende' gözlüğüyle bakıyorsun. "
            "Doğrudan, güçlü ve kararlısın — etrafındakilere hissettirmeden liderlik edersin. "
            "Haksızlık ve zayıfların ezilmesi seni derin bir öfkeyle harekete geçirir. "
            "Zayıflık veya bağımlılık sana çok uzak hissettiriyor — kırılgan olmak tehlike gibi geliyor. "
            "Oysa bu güçlü kabuğun altında çok derin bir koruyuculuk ve sadakat yatıyor."
        ),
        "strengths": [
            "Liderlik gücü — doğal olarak öne çıkar, insanları yönlendirir ve korursun",
            "Karar alma hızı — belirsizlikte bile net ve kararlı olabilirsin",
            "Adalet duygusu — güçsüzlerin yanında olmak seni harekete geçirir",
            "Güç ve dayanıklılık — zorluklarla yüzleşmekten kaçınmazsın",
            "Dürüstlük — düşündüğünü açıkça söylersin, diplomasiyi bazen atlayabilirsin",
        ],
        "weaknesses": [
            "Kırılganlığı reddetme — duygusal açıklık sana tehlike gibi gelir",
            "Baskıcılık — kontrolü kaybetmemek için çevreyi baskı altına alabilirsin",
            "Öfkenin ani ve yoğun çıkması — sınır çiğnendiğinde sert tepkiler verebilirsin",
            "Dinleme güçlüğü — kendi görüşüne o kadar güvenirsin ki başkasını kapatabilirsin",
            "İktidar mücadelesi — boyun eğmek yerine çatışmayı seçebilirsin",
        ],
        "work_style": (
            "Liderlik, bağımsızlık ve gerçek etki imkânı sunan ortamlarda güçlüsün. "
            "Girişimcilik, yöneticilik, hukuk, politika ve kriz yönetimi gibi alanlarda "
            "doğal avantajın var. Ayrıntı odaklı, bürokratik ve seni kısıtlayan ortamlar seni boğar."
        ),
        "relationship_style": (
            "Tutkulu, sadık ve koruyucu bir partner veya arkadassın. "
            "Sevdiklerini zayıf düşürecek herkese karşı duracak cesareti taşırsın. "
            "Ancak kırılganlığını göstermek çok zor gelir — bu mesafe ve yalnızlık yaratabilir. "
            "En derin bağ: gücünü kullanan değil, içini gören biriyle kurduğun bağdır."
        ),
        "stress_behavior": (
            "Stres altında Tip 5'e (Araştırmacı) kayarsın: içine çekilir, "
            "izole olur ve pasif hale gelebilirsin. Dışarıya güçlü görünür, "
            "içeride ise yalnız ve tükenmişsindir."
        ),
        "growth_behavior": (
            "Gelişim yolunda Tip 2'ye (Yardımcı) yönelirsin: şefkat açılır, "
            "başkalarının ihtiyaçlarına gerçekten dokunur ve kırılgan olabilirsin. "
            "Güç, şefkati bastırmak yerine onu ifade etmek için kullanılır."
        ),
        "danger_signals": [
            "Her şeyin kontrolde olması gerektiği hissiyle sürekli gerginlik",
            "İnsanların senden gerçekten korkması",
            "Kırılganlığı zayıflık olarak görerek tüm duygusal kapıları kapatmak",
            "İktidar için ilişkileri ve değerleri feda etmek",
        ],
        "prescription": [
            "🤍 Kırılgan ol: Bu hafta güvendiğin birine gerçekten zor hissettiren bir şeyden bahset.",
            "👂 Dinle: Bir tartışmada karşındakinin bakış açısını sonuna kadar dinle, araya girme.",
            "🌿 Kontrol bırak: Bir konuda 'Ben bilmiyorum, sen karar ver' de — nasıl hissettirdiğini izle.",
            "❤️ Şefkat yönelt: Bugün güçsüz gördüğün birine, güç göstermeden, sadece insan olarak dokunmaya çalış.",
        ],
        "famous_examples": "Winston Churchill, Martin Luther King, Serena Williams",
        "careers": ["CEO", "Politikacı", "Avukat", "Girişimci", "Askeri lider", "Aktivist"],
    },
    9: {
        "title": "Tip 9: Barışçı",
        "role": "Uzlaştırıcı, Diplomat",
        "icon": "☮️",
        "fear": "Çatışma, kopukluk ve iç huzurun kaybı.",
        "desire": "İç ve dış huzura sahip olmak, herkesin uyum içinde olduğunu görmek.",
        "stress": 6, "growth": 3,
        "desc": (
            "Sen dünyaya 'Herkes iyi olsun, uyum bozulmasın' gözlüğüyle bakıyorsun. "
            "Sakinliğin, anlayışın ve kapsayıcılığın çevreye huzur verir. "
            "Çatışmayı önlemek için yüksek bir enerji harcarsın ve genellikle insanlara "
            "uzlaşmanın yolunu gösterebilirsin. Ancak bu barışı koruma çabası bazen "
            "kendi sesini bastırmanla sonuçlanabilir. 'Ben ne istiyorum?' sorusu "
            "zaman zaman en zorlu soru haline gelebilir."
        ),
        "strengths": [
            "Doğal arabuluculuk — çatışmaları görmek ve uzlaştırmak sana kolay gelir",
            "Sabır ve anlayış — farklı bakış açılarını kapsayıcı bir şekilde dinleyebilirsin",
            "Güven verme — insanlar yanında kendini güvende ve kabul görmüş hisseder",
            "Empati — başkasının dünyasına girmek ve onu anlamak konusunda üstünsün",
            "İstikrar — stresli ortamlarda sakin ve dengeli kalabilirsin",
        ],
        "weaknesses": [
            "Kendi sesini kaybetme — çatışmadan kaçmak için fikirlerini geri planda tutabilirsin",
            "Erteleme — harekete geçmek bazen çok ağır gelir, olduğu yerde kalırsın",
            "Pasif-agresif tepkiler — doğrudan söylemek yerine geri çekilir veya direnirsin",
            "Önceliklendirme güçlüğü — ne istediğini bilmemek enerjini dağıtır",
            "Dışsal uyaranlara bağımlılık — başkası harekete geçirmeden kendi kendine başlamak zor",
        ],
        "work_style": (
            "İşbirliği gerektiren, hiyerarşinin katı olmadığı ve uyum içinde çalışılan "
            "ortamlarda güçlüsün. Danışmanlık, arabuluculuk, sosyal hizmet, eğitim ve "
            "sağlık gibi alanlarda değerli katkı sunarsın. "
            "Aşırı rekabetçi, gürültülü ve çatışmacı ortamlar seni tüketir."
        ),
        "relationship_style": (
            "Destekleyici, uyumlu ve sakin bir bağ ararsın. "
            "Partnerinin mutluluğu için kendi isteklerini sık sık arka plana atarsın. "
            "Hayal kırıklıklarını doğrudan ifade etmek yerine mesafe koyar ya da pasif kalırsın. "
            "En iyi ilişki: fikirlerini ve isteklerini söylemeni güvenli hissettiren biriyle."
        ),
        "stress_behavior": (
            "Stres altında Tip 6'ya (Sadık) kayarsın: kaygılanır, "
            "güvensizleşir ve felaket senaryoları üretmeye başlarsın. "
            "Normalde sakin olan yapın, kaygı ve şüpheyle dolar."
        ),
        "growth_behavior": (
            "Gelişim yolunda Tip 3'e (Başarılı) yönelirsin: harekete geçer, "
            "hedefler belirler ve bunlara odaklanırsın. "
            "Pasiflik yerini enerjik ve amaçlı bir harekete bırakır."
        ),
        "danger_signals": [
            "Yıllarca kendi isteklerini ve duygularını bastırmak",
            "Önemli kararları sürekli ertelemek",
            "Söylemek istediklerini içine atıp geri çekilmek",
            "Başkalarının hayatında aktif, kendininkinde pasif olmak",
        ],
        "prescription": [
            "🗣️ Sesini çıkar: Bugün 'Ben şunu istiyorum' veya 'Ben şunu düşünüyorum' de — rahatsızlık normaldir.",
            "⚡ Bir adım at: Ertelediğin küçük bir şeyi bu gün yap, mükemmel olmak zorunda değil.",
            "📋 Önceliklendir: Sabah 'Bugün benim için en önemli üç şey nedir?' diye sor.",
            "🔍 Çatışmaya gir: Küçük bir anlaşmazlıkta görüşünü açıkla ve uzlaşmak yerine var ol.",
        ],
        "famous_examples": "Dalai Lama, Abraham Lincoln, Mister Rogers",
        "careers": ["Arabulucu", "Danışman", "Terapist", "Öğretmen", "Sosyal hizmet uzmanı", "Diplomat"],
    },
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

    main_type  = max(scores, key=scores.get)
    main_score = normalized[main_type]

    wings = [9, 2] if main_type == 1 else ([8, 1] if main_type == 9 else [main_type - 1, main_type + 1])
    wing_type = max(wings, key=lambda w: normalized[w])
    wing_score = normalized[wing_type]
    full_type_str = f"{main_type}w{wing_type}" if wing_score > main_score * 0.7 else f"{main_type} (Saf Tip)"

    data     = ENNEAGRAM_DATA[main_type]
    wing_txt = WING_DESCRIPTIONS.get(f"{main_type}w{wing_type}", "Dengeli kanat etkisi.")

    stress_data = ENNEAGRAM_DATA[data["stress"]]
    growth_data = ENNEAGRAM_DATA[data["growth"]]

    # Puan tablosu için sıralama
    sorted_scores = sorted(normalized.items(), key=lambda x: x[1], reverse=True)

    def bar(pct):
        n = round(pct / 10)
        return "█" * n + "░" * (10 - n)

    score_table = "\n".join(
        f"| {ENNEAGRAM_DATA[t]['icon']} Tip {t}: {ENNEAGRAM_DATA[t]['role'].split(',')[0]} "
        f"| %{p} | {bar(p)} |"
        for t, p in sorted_scores
    )

    strengths_txt  = "\n".join(f"- ✅ {s}" for s in data["strengths"])
    weaknesses_txt = "\n".join(f"- ⚠️ {w}" for w in data["weaknesses"])
    danger_txt     = "\n".join(f"- 🚨 {d}" for d in data["danger_signals"])
    prescription_txt = "\n".join(f"- {p}" for p in data["prescription"])
    careers_txt    = ", ".join(data.get("careers", []))

    report = f"""# {data['icon']} ENNEAGRAM KİŞİLİK RAPORU

**Senin Tipin:** {data['title']}
**Tam Profilin:** {full_type_str}
**Temel Rolün:** {data['role']}

---

## 📊 Tüm Tip Puanların

| Kişilik Tipi | Yüzde | Grafik |
|---|---|---|
{score_table}

---

## 🌟 Sen Kimsin?

{data['desc']}

---

## 🦅 Kanat Etkisi: {main_type}w{wing_type}

{wing_txt}

---

## 🔑 Temel Motivasyonun

| | |
|---|---|
| 😨 **Temel Korku** | {data['fear']} |
| 💛 **Temel Arzu** | {data['desire']} |

---

## 💪 Güçlü Yönlerin

{strengths_txt}

---

## 🌱 Gelişim Alanların

{weaknesses_txt}

---

## 💼 Çalışma Stilin

{data['work_style']}

**Sana Uygun Kariyer Alanları:** {careers_txt}

---

## 💑 İlişki Stilin

{data['relationship_style']}

---

## 🔴 Stres Altında Ne Olur?

{data['stress_behavior']}

> Stres tipine kayarsın: **{stress_data['title']}** ({stress_data['role']})

---

## 🟢 Gelişim Yolunda Ne Olur?

{data['growth_behavior']}

> Gelişim tipine doğru yol alırsın: **{growth_data['title']}** ({growth_data['role']})

---

## 🚨 Dikkat Sinyalleri

{danger_txt}

---

## 🛠️ Sana Özel Büyüme Taktikleri

{prescription_txt}

---

## 🌍 Aynı Tipdeki Tanınmış İsimler

{data.get('famous_examples', '—')}

---

## 💬 Son Söz

Enneagram bir kısıtlama değil, bir harita. Tipini bilmek seni kutucuğa hapsetmez —
aksine, neden böyle davrandığını, neyin seni harekete geçirdiğini ve nereye büyüyebileceğini
anlamana yardım eder. En sağlıklı versiyonuna ulaşmak için güçlü yönlerini kullan,
gelişim sinyallerini merak ve şefkatle karşıla. Değişim, kendini tanımakla başlar. 🌱
"""
    return scores, report.strip()


# ============================================================
# ANA APP FONKSİYONU
# ============================================================
def app():
    st.markdown("""
    <style>
        .test-card { background-color: #f8f9fa; border: 1px solid #ddd; border-radius: 10px; padding: 20px; margin-bottom: 15px; text-align: center; transition: 0.3s; cursor: pointer; }
        .test-card:hover { background-color: #e9ecef; border-color: #1b365d; transform: translateY(-5px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .completed-badge { background-color: #d4edda; color: #155724; padding: 5px 10px; border-radius: 15px; font-size: 0.8em; font-weight: bold; }
        
        /* BAŞLIK STİLLERİ (LOGUYA UYUMLU) */
        .main-header { 
            color: #1b365d; 
            text-align: center; 
            font-weight: 900; 
            font-size: 3.5rem; 
            margin-bottom: 0px; 
        }
        .sub-title {
            color: #cc0000;
            text-align: center;
            font-weight: bold;
            font-size: 1.5rem;
            margin-top: -10px;
            margin-bottom: 20px;
        }
        .welcome-text { color: #555; text-align: center; margin-bottom: 30px; font-style: italic; font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True)

    # --- KURUMSAL BAŞLIK ALANI (YENİ İSİM) ---
    st.markdown("<h1 class='main-header'>EĞİTİM CHECKUP</h1>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Kişisel Eğitim & Kariyer Analiz Merkezi</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='welcome-text'>Hoşgeldin, <b>{st.session_state.student_name}</b>. Kendini keşfetmeye hazır mısın?</div>", unsafe_allow_html=True)

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
                        import random
                        flat = []
                        for tip_no, qs in ENNEAGRAM_QUESTIONS.items():
                            for i, text in enumerate(qs):
                                flat.append({"type": tip_no, "idx": i, "text": text,
                                             "key": f"{tip_no}_{i}"})
                        random.shuffle(flat)
                        st.session_state.enneagram_shuffled  = flat
                        st.session_state.enneagram_page      = 0
                        st.session_state.enneagram_answers   = {}
                        st.session_state.current_test_data   = {"type": "enneagram_fixed"}

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
            
            c1, c2 = st.columns(2)
            
            if c1.button("⬅️ Vazgeç / Ana Menüye Dön"):
                st.session_state.page = "home"
                st.rerun()
                
            if c2.button("HAZIRIM, BAŞLA! 🚀", type="primary"):
                st.session_state.intro_passed = True
                st.rerun()

        # --- SORULAR ---
        else:
            data = st.session_state.current_test_data
            q_type = data.get("type")

            # ========================================
            # TİP: ENNEAGRAM — KARISIK SAYFALANMIŞ
            # ========================================
            if q_type == "enneagram_fixed":
                PER_PAGE  = 20
                all_qs    = st.session_state.enneagram_shuffled
                total_qs  = len(all_qs)          # 180
                curr_page = st.session_state.enneagram_page
                total_pages = (total_qs + PER_PAGE - 1) // PER_PAGE  # 9

                page_qs  = all_qs[curr_page * PER_PAGE : (curr_page + 1) * PER_PAGE]
                answered = sum(1 for q in all_qs
                               if st.session_state.enneagram_answers.get(q["key"]) is not None)

                # İlerleme — kaç soru cevaplandı, hangi bölüm
                st.progress(answered / total_qs)
                st.caption(f"Bölüm {curr_page + 1} / {total_pages}  •  "
                           f"{answered}/{total_qs} soru cevaplandı")
                st.divider()

                ennea_map = {
                    1: "Kesinlikle Katılmıyorum",
                    2: "Katılmıyorum",
                    3: "Kararsızım",
                    4: "Katılıyorum",
                    5: "Kesinlikle Katılıyorum",
                }
                opts = [1, 2, 3, 4, 5]

                all_answered = True
                for i, q in enumerate(page_qs):
                    global_num = curr_page * PER_PAGE + i + 1
                    st.write(f"**{global_num}. {q['text']}**")
                    prev = st.session_state.enneagram_answers.get(q["key"])
                    val  = st.radio(
                        f"Soru {global_num}",
                        opts,
                        key=f"rad_{q['key']}",
                        index=opts.index(prev) if prev is not None else None,
                        horizontal=True,
                        format_func=lambda x: ennea_map[x],
                        label_visibility="collapsed",
                    )
                    if val is not None:
                        st.session_state.enneagram_answers[q["key"]] = val
                    else:
                        all_answered = False
                    st.divider()

                c1, c2 = st.columns(2)
                if curr_page > 0:
                    if c1.button("⬅️ Önceki Bölüm"):
                        st.session_state.enneagram_page -= 1
                        st.rerun()

                is_last = curr_page == total_pages - 1
                if not is_last:
                    if c2.button("Sonraki Bölüm ➡️"):
                        if not all_answered:
                            st.error("⚠️ Lütfen bu bölümdeki tüm soruları cevapla.")
                        else:
                            st.session_state.enneagram_page += 1
                            st.rerun()
                else:
                    if c2.button("Bitir ve Gönder ✅", type="primary"):
                        total_answered = sum(
                            1 for q in all_qs
                            if st.session_state.enneagram_answers.get(q["key"]) is not None
                        )
                        if total_answered < total_qs:
                            st.error(f"⚠️ Henüz {total_qs - total_answered} soru cevaplanmadı. "
                                     "Önceki bölümlere dönerek eksikleri tamamla.")
                        else:
                            with st.spinner("Kişilik haritan çıkarılıyor..."):
                                scores, rep = calculate_enneagram_report(
                                    st.session_state.enneagram_answers
                                )
                                save_test_result_to_db(
                                    st.session_state.student_id,
                                    t_name,
                                    st.session_state.enneagram_answers,
                                    scores,
                                    rep,
                                )
                                st.session_state.last_report = rep
                                st.session_state.page = "success_screen"
                                st.rerun()

            # ========================================
            # TİP: A/B SEÇİMLİ (Sağ-Sol Beyin)
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
                "sol_yuzde":  result["sol_yuzde"],
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
