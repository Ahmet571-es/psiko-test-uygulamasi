"""
Akademik Analiz Testi — Performans Motoru
==========================================
Özel tasarım çok boyutlu akademik yetkinlik testi.

4 Alt Boyut:
  1. Okuma Anlama   — Metin kavrama, çıkarım, ana fikir
  2. Matematiksel Muhakeme — Problem çözme, sayısal düşünme
  3. Mantıksal Düşünme — Örüntü, analoji, seri tamamlama
  4. Akademik Öz-Değerlendirme — Çalışma stratejisi, özgüven (Likert)

2 Versiyon:
  - İlköğretim (8-13 yaş): ~40 soru
  - Lise (14-18 yaş): ~50 soru
"""

# ============================================================
# İLKÖĞRETİM — OKUMA ANLAMA (3 metin × 4 soru = 12)
# ============================================================
OKUMA_ILKOGRETIM = [
    {
        "passage": (
            "Arılar, doğadaki en çalışkan canlılardan biridir. Bir bal arısı, "
            "yaşamı boyunca sadece bir çay kaşığının on ikide biri kadar bal üretir. "
            "Bir kavanoz bal üretmek için arıların yaklaşık 3,5 milyon çiçeği ziyaret "
            "etmesi gerekir. Arılar balı üretirken aynı zamanda bitkilerin tozlaşmasını "
            "da sağlar. Bilim insanları, arıların yok olması durumunda birçok meyve "
            "ve sebzenin de yok olacağını söylemektedir."
        ),
        "questions": [
            {"id": "oi_1", "text": "Bir bal arısı yaşamı boyunca ne kadar bal üretir?",
             "options": {"a": "Bir çay kaşığı", "b": "Bir çay kaşığının on ikide biri",
                         "c": "Bir kavanoz", "d": "Hiç üretmez"},
             "answer": "b"},
            {"id": "oi_2", "text": "Bir kavanoz bal için yaklaşık kaç çiçek ziyaret edilir?",
             "options": {"a": "350 bin", "b": "35 bin", "c": "3,5 milyon", "d": "35 milyon"},
             "answer": "c"},
            {"id": "oi_3", "text": "Arıların tozlaşma yapmasının önemi nedir?",
             "options": {"a": "Balın tadını güzelleştirir", "b": "Bitkilerin üremesini sağlar",
                         "c": "Arıların daha hızlı uçmasını sağlar", "d": "Çiçeklerin rengini değiştirir"},
             "answer": "b"},
            {"id": "oi_4", "text": "Metnin ana fikri nedir?",
             "options": {"a": "Arılar çok hızlı uçar", "b": "Bal çok lezzetlidir",
                         "c": "Arılar doğa için çok önemli ve çalışkan canlılardır",
                         "d": "Arılar tehlikeli böceklerdir"},
             "answer": "c"},
        ]
    },
    {
        "passage": (
            "Su, yeryüzünün yaklaşık yüzde yetmişini kaplar. Ancak bu suyun büyük "
            "çoğunluğu tuzlu su olan okyanuslardadır. İçilebilir tatlı su, toplam "
            "suyun sadece yüzde üçünü oluşturur. Üstelik bu tatlı suyun da büyük "
            "bölümü kutuplardaki buzullarda donmuş hâldedir. İnsanların kolayca "
            "kullanabileceği tatlı su kaynakları — nehirler, göller ve yeraltı suları — "
            "dünyadaki toplam suyun yüzde birinden bile azdır. Bu nedenle suyu "
            "tasarruflu kullanmak herkesin sorumluluğudur."
        ),
        "questions": [
            {"id": "oi_5", "text": "Yeryüzünün yüzde kaçı suyla kaplıdır?",
             "options": {"a": "%30", "b": "%50", "c": "%70", "d": "%90"},
             "answer": "c"},
            {"id": "oi_6", "text": "Tatlı su toplam suyun yüzde kaçını oluşturur?",
             "options": {"a": "%1", "b": "%3", "c": "%10", "d": "%30"},
             "answer": "b"},
            {"id": "oi_7",
             "text": "Metne göre, tatlı suyun büyük bölümü nerededir?",
             "options": {"a": "Nehirlerde", "b": "Göllerde",
                         "c": "Kutuplardaki buzullarda", "d": "Okyanuslarda"},
             "answer": "c"},
            {"id": "oi_8",
             "text": "Metinden çıkarılabilecek en önemli sonuç nedir?",
             "options": {"a": "Okyanuslar çok büyüktür",
                         "b": "Kullanılabilir su kaynağı çok kısıtlıdır",
                         "c": "Buzullar erimelidir",
                         "d": "Tuzlu su içilebilir hâle getirilebilir"},
             "answer": "b"},
        ]
    },
    {
        "passage": (
            "Eski Mısırlılar, papirüs bitkisinden kâğıt benzeri bir malzeme "
            "üretmeyi başaran ilk uygarlıklardan biridir. Papirüs, Nil Nehri "
            "kıyılarında yetişen uzun bir saz bitkisidir. Mısırlılar bu bitkinin "
            "gövdesini ince şeritler hâlinde kesiyor, şeritleri yan yana ve üst "
            "üste diziyordu. Sonra ağır taşlarla presleyerek düzleştiriyorlardı. "
            "Kuruyan yaprak, yazı yazmaya uygun pürüzsüz bir yüzey oluyordu. "
            "Papirüs sayesinde Mısırlılar tarih, tıp ve matematik bilgilerini "
            "gelecek nesillere aktarabildi."
        ),
        "questions": [
            {"id": "oi_9", "text": "Papirüs bitkisi nerede yetişir?",
             "options": {"a": "Çöllerde", "b": "Dağlarda",
                         "c": "Nil Nehri kıyılarında", "d": "Deniz altında"},
             "answer": "c"},
            {"id": "oi_10",
             "text": "Mısırlılar papirüsü nasıl düzleştiriyordu?",
             "options": {"a": "Ateşle ısıtarak", "b": "Ağır taşlarla presleyerek",
                         "c": "Suya batırarak", "d": "Rüzgârda kurulayarak"},
             "answer": "b"},
            {"id": "oi_11",
             "text": "'Gelecek nesillere aktarabildi' ifadesinden ne anlıyoruz?",
             "options": {"a": "Bilgi sonraki kuşaklara ulaştı",
                         "b": "Papirüs çok pahalıydı",
                         "c": "Mısırlılar yazı yazmayı sevmezdi",
                         "d": "Bilgi sadece Mısır'da kaldı"},
             "answer": "a"},
            {"id": "oi_12",
             "text": "Bu metne en uygun başlık hangisidir?",
             "options": {"a": "Nil Nehri'nin Önemi", "b": "Kâğıdın Tarihi: Papirüs",
                         "c": "Eski Mısır Piramitleri", "d": "Bitkilerden Yapılan Eşyalar"},
             "answer": "b"},
        ]
    },
]

# ============================================================
# İLKÖĞRETİM — MATEMATİKSEL MUHAKEME (12 soru)
# ============================================================
MATEMATIK_ILKOGRETIM = [
    {"id": "mi_1",
     "text": "Bir çiftlikte 24 tavuk ve 18 koyun vardır. Hayvanların toplam ayak sayısı kaçtır?",
     "options": {"a": "84", "b": "120", "c": "96", "d": "108"},
     "answer": "b"},  # 24×2 + 18×4 = 48+72=120
    {"id": "mi_2",
     "text": "Ali'nin 120 TL'si vardı. Parasının üçte birini kitaba, kalanın yarısını kaleme harcadı. Elinde kaç TL kaldı?",
     "options": {"a": "40 TL", "b": "60 TL", "c": "30 TL", "d": "80 TL"},
     "answer": "a"},  # 120/3=40 kitap, kalan 80, 80/2=40 kalem, kalan 40
    {"id": "mi_3",
     "text": "Bir sınıfta 30 öğrenci var. Öğrencilerin %60'ı kız ise kaç erkek öğrenci vardır?",
     "options": {"a": "18", "b": "15", "c": "12", "d": "20"},
     "answer": "c"},  # 30×0.6=18 kız, 30-18=12 erkek
    {"id": "mi_4",
     "text": "Bir dikdörtgenin uzun kenarı 12 cm, kısa kenarı 8 cm. Çevresi kaç cm'dir?",
     "options": {"a": "96 cm", "b": "40 cm", "c": "20 cm", "d": "36 cm"},
     "answer": "b"},  # 2×(12+8)=40
    {"id": "mi_5",
     "text": "5, 10, 20, 40, … serisinde sonraki sayı kaçtır?",
     "options": {"a": "60", "b": "50", "c": "80", "d": "100"},
     "answer": "c"},  # ×2 serisi
    {"id": "mi_6",
     "text": "Bir markette elmalar 3'lü paketlerde satılmaktadır. 5 paket alan kişi kaç elma almış olur?",
     "options": {"a": "12", "b": "8", "c": "15", "d": "18"},
     "answer": "c"},
    {"id": "mi_7",
     "text": "Ayşe saatte 4 km yürüyor. 2 saat 30 dakikada kaç km yol alır?",
     "options": {"a": "8 km", "b": "10 km", "c": "12 km", "d": "6 km"},
     "answer": "b"},  # 4×2.5=10
    {"id": "mi_8",
     "text": "Bir pizzanın 3/8'i yendikten sonra kalan kısmın tamamı kaçta kaçtır?",
     "options": {"a": "5/8", "b": "3/5", "c": "1/2", "d": "4/8"},
     "answer": "a"},
    {"id": "mi_9",
     "text": "Bir kutuya her gün 7 bilye atılıyor. 4 gün sonra kutudan 10 bilye alınırsa kutuda kaç bilye kalır?",
     "options": {"a": "18", "b": "28", "c": "38", "d": "17"},
     "answer": "a"},  # 7×4=28, 28-10=18
    {"id": "mi_10",
     "text": "Bir saat 09:45'i gösteriyor. 2 saat 30 dakika sonra saat kaçı gösterir?",
     "options": {"a": "11:45", "b": "12:15", "c": "12:45", "d": "11:15"},
     "answer": "b"},
    {"id": "mi_11",
     "text": "6 işçi bir duvarı 10 günde örüyor. Aynı duvarı 3 işçi kaç günde örer?",
     "options": {"a": "15 gün", "b": "20 gün", "c": "5 gün", "d": "30 gün"},
     "answer": "b"},  # 6×10=60 iş günü, 60/3=20
    {"id": "mi_12",
     "text": "Bir arabanın deposunda 45 litre benzin var. Her 100 km'de 8 litre benzin harcıyorsa, yaklaşık kaç km yol gidebilir?",
     "options": {"a": "450 km", "b": "360 km", "c": "562 km", "d": "400 km"},
     "answer": "c"},  # 45/8×100=562.5
]

# ============================================================
# İLKÖĞRETİM — MANTIKSAL DÜŞÜNME (10 soru)
# ============================================================
MANTIK_ILKOGRETIM = [
    {"id": "li_1",
     "text": "Elma → Meyve, Köpek → Hayvan, Gül → ?",
     "options": {"a": "Ağaç", "b": "Bahçe", "c": "Çiçek", "d": "Yaprak"},
     "answer": "c"},
    {"id": "li_2",
     "text": "2, 6, 12, 20, 30, … serisinde sonraki sayı kaçtır?",
     "options": {"a": "36", "b": "40", "c": "42", "d": "44"},
     "answer": "c"},  # farklar: 4,6,8,10,12
    {"id": "li_3",
     "text": "Tüm kediler hayvandır. Bazı hayvanlar uçar. Buna göre hangisi kesinlikle doğrudur?",
     "options": {"a": "Bazı kediler uçar", "b": "Hiçbir kedi uçamaz",
                 "c": "Tüm kediler hayvandır", "d": "Tüm hayvanlar kedidir"},
     "answer": "c"},
    {"id": "li_4",
     "text": "Bir gruptaki harf sırası: A, C, F, J, … Sonraki harf hangisidir? (A=1, B=2, ...)",
     "options": {"a": "M", "b": "N", "c": "O", "d": "P"},
     "answer": "c"},  # +2,+3,+4,+5 → J(10)+5=O(15)
    {"id": "li_5",
     "text": "Kitap → Okumak, Bıçak → Kesmek, Kalem → ?",
     "options": {"a": "Silmek", "b": "Çizmek", "c": "Yazmak", "d": "Boyamak"},
     "answer": "c"},
    {"id": "li_6",
     "text": "Ayşe, Mehmet'ten uzundur. Mehmet, Ali'den uzundur. Buna göre hangisi kesinlikle doğrudur?",
     "options": {"a": "Ali en uzundur", "b": "Mehmet en kısadır",
                 "c": "Ayşe, Ali'den uzundur", "d": "Ali, Ayşe'den uzundur"},
     "answer": "c"},
    {"id": "li_7",
     "text": "81, 27, 9, 3, … serisinde sonraki sayı kaçtır?",
     "options": {"a": "0", "b": "1", "c": "2", "d": "-3"},
     "answer": "b"},  # ÷3 serisi
    {"id": "li_8",
     "text": "Bir kutu kırmızı, bir kutu mavi, bir kutu karışık top içeriyor. Kutular YANLIŞ etiketlenmiş. 'Karışık' yazan kutudan 1 top çektin ve kırmızı geldi. 'Karışık' yazan kutuda gerçekte ne var?",
     "options": {"a": "Karışık", "b": "Mavi", "c": "Kırmızı", "d": "Bilinemez"},
     "answer": "c"},
    {"id": "li_9",
     "text": "Pazartesi bugün ise 100 gün sonra hangi gündür?",
     "options": {"a": "Çarşamba", "b": "Perşembe", "c": "Cuma", "d": "Cumartesi"},
     "answer": "a"},  # 100÷7=14 hafta 2 gün → Çarşamba
    {"id": "li_10",
     "text": "Dört arkadaş bir sırada oturuyor. Ahmet, Zeynep'in solunda. Burak, en sağda. Elif, Ahmet ile Burak arasında. Soldan sağa sıralama nedir?",
     "options": {"a": "Zeynep-Ahmet-Elif-Burak", "b": "Ahmet-Zeynep-Elif-Burak",
                 "c": "Zeynep-Elif-Ahmet-Burak", "d": "Ahmet-Elif-Zeynep-Burak"},
     "answer": "a"},
]

# ============================================================
# İLKÖĞRETİM — AKADEMİK ÖZ-DEĞERLENDİRME (10 soru, Likert 1-5)
# ============================================================
OZ_DEGER_ILKOGRETIM = [
    {"id": "odi_1", "text": "Ders çalışırken konuya kolayca odaklanabilirim."},
    {"id": "odi_2", "text": "Bir konuyu anlamazsam tekrar tekrar çalışırım."},
    {"id": "odi_3", "text": "Sınavlarda kendime güvenirim."},
    {"id": "odi_4", "text": "Okuduğum metinleri anlayıp özetleyebilirim."},
    {"id": "odi_5", "text": "Matematik problemlerini çözmekten keyif alırım."},
    {"id": "odi_6", "text": "Ödevlerimi zamanında tamamlarım."},
    {"id": "odi_7", "text": "Yeni konuları öğrenmek beni heyecanlandırır."},
    {"id": "odi_8", "text": "Arkadaşlarıma bir konuyu açıklayabilecek kadar iyi anlıyorum."},
    {"id": "odi_9", "text": "Zor bir soruyla karşılaşınca pes etmem, çözmeye çalışırım."},
    {"id": "odi_10", "text": "Ders çalışma planı yapıp ona uyarım."},
]


# ============================================================
# LİSE — OKUMA ANLAMA (3 metin × 5 soru = 15)
# ============================================================
OKUMA_LISE = [
    {
        "passage": (
            "Yapay zekâ teknolojilerinin hızla gelişmesi, toplumda hem heyecan hem de "
            "endişe yaratmaktadır. Bir yandan tıpta erken tanı, eğitimde kişiselleştirilmiş "
            "öğrenme ve endüstride verimlilik artışı gibi somut faydalar sağlanırken; "
            "öte yandan iş gücü piyasasında köklü dönüşümler beklenmektedir. Dünya "
            "Ekonomik Forumu'nun raporuna göre, 2030 yılına kadar mevcut mesleklerin "
            "yaklaşık üçte biri otomasyona bağlı olarak dönüşecektir. Ancak uzmanlar, "
            "yok olacak her mesleğin yerine daha önce var olmayan yeni mesleklerin "
            "doğacağını da vurgulamaktadır. Kritik olan, bireylerin yaşam boyu öğrenme "
            "becerisini kazanması ve değişime uyum sağlayabilmesidir."
        ),
        "questions": [
            {"id": "ol_1", "text": "Metne göre yapay zekânın sağladığı faydalardan biri hangisidir?",
             "options": {"a": "İşsizliğin artması", "b": "Eğitimde kişiselleştirilmiş öğrenme",
                         "c": "Mesleklerin tamamen yok olması", "d": "Teknolojinin yavaşlaması"},
             "answer": "b"},
            {"id": "ol_2", "text": "Dünya Ekonomik Forumu'na göre 2030'a kadar mesleklerin ne kadarı dönüşecek?",
             "options": {"a": "Tamamı", "b": "Yarısı", "c": "Yaklaşık üçte biri", "d": "Onda biri"},
             "answer": "c"},
            {"id": "ol_3", "text": "Uzmanlar yok olan meslekler hakkında ne söylemektedir?",
             "options": {"a": "Yerine yeni meslekler doğacak", "b": "Hiçbir şey yapılamaz",
                         "c": "Herkes işsiz kalacak", "d": "Sadece mühendisler çalışacak"},
             "answer": "a"},
            {"id": "ol_4", "text": "Metne göre bireyler için kritik olan beceri hangisidir?",
             "options": {"a": "Sadece tek bir meslekte uzmanlaşmak", "b": "Teknolojiden uzak durmak",
                         "c": "Yaşam boyu öğrenme ve değişime uyum", "d": "Mümkün olduğunca erken emekli olmak"},
             "answer": "c"},
            {"id": "ol_5", "text": "Metnin yazarı yapay zekâya karşı nasıl bir tutum sergilemektedir?",
             "options": {"a": "Tamamen olumsuz", "b": "Tamamen olumlu",
                         "c": "Dengeli — hem fırsatları hem riskleri ele alan", "d": "Kayıtsız ve ilgisiz"},
             "answer": "c"},
        ]
    },
    {
        "passage": (
            "Fotosentez, canlı yaşamın temelini oluşturan en önemli biyokimyasal süreçtir. "
            "Bitkiler, güneş enerjisini kullanarak karbondioksit ve suyu glikoz ve oksijene "
            "dönüştürür. Bu süreç, atmosferdeki oksijen miktarını dengede tutarken aynı "
            "zamanda besin zincirinin ilk halkasını oluşturur. Yapılan araştırmalar, "
            "yağmur ormanlarının yılda yaklaşık 28 milyar ton karbondioksiti absorbe "
            "ettiğini ortaya koymuştur. Ancak ormansızlaşma nedeniyle bu kapasite hızla "
            "azalmaktadır. Bilim insanları, yapay fotosentez teknolojileri geliştirerek "
            "bu açığı kapatmaya çalışmaktadır; fakat doğal sürecin verimliliğine ulaşmak "
            "henüz mümkün olamamıştır."
        ),
        "questions": [
            {"id": "ol_6", "text": "Fotosentezin girdileri (hammaddeleri) nelerdir?",
             "options": {"a": "Oksijen ve glikoz", "b": "Karbondioksit ve su",
                         "c": "Güneş ve oksijen", "d": "Glikoz ve su"},
             "answer": "b"},
            {"id": "ol_7", "text": "Yağmur ormanları yılda ne kadar karbondioksit absorbe eder?",
             "options": {"a": "28 milyon ton", "b": "2,8 milyar ton",
                         "c": "28 milyar ton", "d": "280 milyar ton"},
             "answer": "c"},
            {"id": "ol_8", "text": "Fotosentez besin zincirindeki hangi rolü üstlenir?",
             "options": {"a": "Son halka — artıkları temizler", "b": "Orta halka — enerjiyi aktarır",
                         "c": "İlk halka — besin üretir", "d": "Besin zinciriyle ilgisi yoktur"},
             "answer": "c"},
            {"id": "ol_9", "text": "Yapay fotosentez teknolojisiyle ilgili metnin söylediği nedir?",
             "options": {"a": "Doğal süreçten daha verimli", "b": "Henüz doğal sürecin verimliliğine ulaşamadı",
                         "c": "Tamamen başarısız oldu", "d": "Ormansızlaşmayı durdurdu"},
             "answer": "b"},
            {"id": "ol_10", "text": "Metnin ana argümanı nedir?",
             "options": {"a": "Yapay fotosentez doğal olanın yerini alacak",
                         "b": "Fotosentez yaşam için hayati ama ormansızlaşma bu sistemi tehdit ediyor",
                         "c": "Bitkiler gereksiz canlılardır",
                         "d": "Karbondioksit zararsız bir gazdır"},
             "answer": "b"},
        ]
    },
    {
        "passage": (
            "Osmanlı İmparatorluğu döneminde vakıf sistemi, toplumsal dayanışmanın "
            "temel kurumlarından biriydi. Varlıklı kişiler; camiler, medreseler, "
            "kervansaraylar, çeşmeler ve hastaneler inşa ettirerek bunları vakıf "
            "yoluyla toplumun hizmetine sunardı. Vakıf gelirleri genellikle dükkân, "
            "han veya tarım arazisi kiralarından elde edilirdi. Bu gelirlerle "
            "kurumların bakımı yapılır, çalışanlarının maaşları ödenir ve "
            "yoksullara yardım edilirdi. Vakıf sistemi, devlet bütçesine yük "
            "olmadan sosyal hizmetlerin sürdürülmesini sağlayan, zamanının çok "
            "ötesinde bir sivil toplum modeliydi."
        ),
        "questions": [
            {"id": "ol_11", "text": "Vakıfların gelirleri nereden elde edilirdi?",
             "options": {"a": "Devlet bütçesinden", "b": "Savaş ganimetlerinden",
                         "c": "Dükkân, han ve tarım arazisi kiralarından", "d": "Vergi toplamaktan"},
             "answer": "c"},
            {"id": "ol_12", "text": "Vakıf gelirlerinin kullanım alanı hangisi DEĞİLDİR?",
             "options": {"a": "Kurumların bakımı", "b": "Çalışan maaşları",
                         "c": "Yoksullara yardım", "d": "Padişahın saray masrafları"},
             "answer": "d"},
            {"id": "ol_13", "text": "Metne göre vakıf sisteminin en önemli özelliği nedir?",
             "options": {"a": "Devletten bağımsız sosyal hizmet sunması",
                         "b": "Sadece zenginlere hizmet vermesi",
                         "c": "Askeri amaçlarla kurulması",
                         "d": "Sadece eğitim alanında faaliyet göstermesi"},
             "answer": "a"},
            {"id": "ol_14", "text": "'Zamanının çok ötesinde' ifadesiyle yazar ne demek istiyor?",
             "options": {"a": "Sistem çok eskiydi", "b": "Sistem kendi dönemine göre çok ileriydi",
                         "c": "Sistem işe yaramıyordu", "d": "Sistem çok karmaşıktı"},
             "answer": "b"},
            {"id": "ol_15", "text": "Günümüzde vakıf sisteminin benzeri olarak ne gösterilebilir?",
             "options": {"a": "Vergi sistemi", "b": "Askerlik hizmeti",
                         "c": "Sivil toplum kuruluşları ve hayır kurumları", "d": "Siyasi partiler"},
             "answer": "c"},
        ]
    },
]

# ============================================================
# LİSE — MATEMATİKSEL MUHAKEME (15 soru)
# ============================================================
MATEMATIK_LISE = [
    {"id": "ml_1",
     "text": "Bir ürünün fiyatı önce %20 artırıldı, sonra %20 indirildi. Son fiyat, başlangıç fiyatına göre nasıldır?",
     "options": {"a": "Aynı kaldı", "b": "%4 düştü", "c": "%4 arttı", "d": "%2 düştü"},
     "answer": "b"},  # 100→120→96, %4 düşüş
    {"id": "ml_2",
     "text": "x + y = 10 ve x − y = 4 ise x × y kaçtır?",
     "options": {"a": "21", "b": "24", "c": "14", "d": "16"},
     "answer": "a"},  # x=7, y=3, 7×3=21
    {"id": "ml_3",
     "text": "Bir havuz A musluğuyla 6 saatte, B musluğuyla 3 saatte doluyor. İkisi birlikte açılırsa kaç saatte dolar?",
     "options": {"a": "1 saat", "b": "2 saat", "c": "4,5 saat", "d": "3 saat"},
     "answer": "b"},  # 1/6+1/3=1/6+2/6=3/6=1/2 → 2 saat
    {"id": "ml_4",
     "text": "Bir sınıfta matematik sınavının ortalaması 65 puan. 5 öğrenci eklenseydi ve her biri 85 alsaydı, ortalama 70 olurdu. Sınıfta kaç öğrenci vardı?",
     "options": {"a": "15", "b": "20", "c": "10", "d": "25"},
     "answer": "a"},  # 65n + 5×85 = 70(n+5) → 65n+425=70n+350 → 75=5n → n=15
    {"id": "ml_5",
     "text": "Bir üçgenin iç açıları oranı 2:3:4'tür. En büyük açı kaç derecedir?",
     "options": {"a": "60°", "b": "80°", "c": "90°", "d": "100°"},
     "answer": "b"},  # 2x+3x+4x=180, 9x=180, x=20, büyük=80
    {"id": "ml_6",
     "text": "500 TL'yi yıllık %12 basit faizle 2 yıl yatırırsanız toplam ne kadar olur?",
     "options": {"a": "560 TL", "b": "620 TL", "c": "600 TL", "d": "624 TL"},
     "answer": "b"},  # 500 + 500×0.12×2 = 500+120 = 620
    {"id": "ml_7",
     "text": "Bir zarla arka arkaya 2 kez atıldığında, toplamın 7 gelme olasılığı kaçtır?",
     "options": {"a": "1/6", "b": "1/9", "c": "5/36", "d": "7/36"},
     "answer": "a"},  # 6 uygun çift / 36 toplam = 1/6
    {"id": "ml_8",
     "text": "2^10 kaçtır?",
     "options": {"a": "512", "b": "1024", "c": "2048", "d": "256"},
     "answer": "b"},
    {"id": "ml_9",
     "text": "Bir araç ilk 2 saatte 80 km/sa, sonraki 3 saatte 60 km/sa hızla gitti. Ortalama hızı kaç km/sa'dir?",
     "options": {"a": "68", "b": "70", "c": "72", "d": "66"},
     "answer": "a"},  # (160+180)/5=340/5=68
    {"id": "ml_10",
     "text": "log₁₀(1000) kaçtır?",
     "options": {"a": "2", "b": "3", "c": "4", "d": "10"},
     "answer": "b"},
    {"id": "ml_11",
     "text": "Bir kutuda 5 kırmızı, 3 mavi top var. Art arda 2 top çekilirse (yerine konmadan), ikisinin de kırmızı olma olasılığı kaçtır?",
     "options": {"a": "5/14", "b": "25/64", "c": "5/8", "d": "10/28"},
     "answer": "a"},  # (5/8)×(4/7)=20/56=5/14
    {"id": "ml_12",
     "text": "f(x) = 3x − 7 ise f(5) kaçtır?",
     "options": {"a": "8", "b": "22", "c": "15", "d": "2"},
     "answer": "a"},
    {"id": "ml_13",
     "text": "Bir eşkenar üçgenin bir kenarı 10 cm ise alanı yaklaşık kaç cm²'dir? (√3 ≈ 1,73)",
     "options": {"a": "43,3", "b": "50", "c": "25", "d": "86,6"},
     "answer": "a"},  # (√3/4)×100 ≈ 43.3
    {"id": "ml_14",
     "text": "Bir sayının %150'si 75'tir. O sayı kaçtır?",
     "options": {"a": "45", "b": "50", "c": "60", "d": "112,5"},
     "answer": "b"},  # x×1.5=75 → x=50
    {"id": "ml_15",
     "text": "3, 7, 15, 31, 63, … serisinde sonraki sayı kaçtır?",
     "options": {"a": "95", "b": "127", "c": "125", "d": "126"},
     "answer": "b"},  # ×2+1: 3→7→15→31→63→127
]

# ============================================================
# LİSE — MANTIKSAL DÜŞÜNME (12 soru)
# ============================================================
MANTIK_LISE = [
    {"id": "ll_1",
     "text": "Demokrasi → Seçim, Diktatörlük → ?",
     "options": {"a": "Özgürlük", "b": "Baskı", "c": "Parlamento", "d": "Anayasa"},
     "answer": "b"},
    {"id": "ll_2",
     "text": "1, 1, 2, 3, 5, 8, 13, … serisinde sonraki sayı kaçtır?",
     "options": {"a": "18", "b": "20", "c": "21", "d": "26"},
     "answer": "c"},  # Fibonacci
    {"id": "ll_3",
     "text": "Tüm bilim insanları meraklıdır. Bazı öğretmenler bilim insanıdır. Buna göre hangisi kesinlikle doğrudur?",
     "options": {"a": "Tüm öğretmenler meraklıdır", "b": "Bazı öğretmenler meraklıdır",
                 "c": "Hiçbir öğretmen meraklı değildir", "d": "Meraklı olan herkes bilim insanıdır"},
     "answer": "b"},
    {"id": "ll_4",
     "text": "A, B'den zengindir. C, D'den fakirdir. B, D'den zengindir. Kim en fakirdir?",
     "options": {"a": "A", "b": "B", "c": "C", "d": "D"},
     "answer": "c"},  # A>B>D>C
    {"id": "ll_5",
     "text": "Doktor → Stetoskop, Ressam → Fırça, Cerrah → ?",
     "options": {"a": "İlaç", "b": "Neşter", "c": "Röntgen", "d": "Mikroskop"},
     "answer": "b"},
    {"id": "ll_6",
     "text": "64, 32, 16, 8, 4, … Bu serideki sayıların toplamı (sonsuz devam etse) neye yaklaşır?",
     "options": {"a": "124", "b": "128", "c": "130", "d": "Sonsuza gider"},
     "answer": "b"},  # Geometrik seri: 64/(1-0.5)=128
    {"id": "ll_7",
     "text": "Beş kişilik bir yarışta Ahmet, Elif'ten önce bitirdi. Burak sonuncu olmadı. Cemre, Deniz'den sonra ama Burak'tan önce bitirdi. Elif, Deniz'den sonra bitirdi. Deniz kaçıncı oldu?",
     "options": {"a": "1.", "b": "2.", "c": "3.", "d": "4."},
     "answer": "b"},  # Ahmet>Elif, Deniz>Cemre>Burak, Deniz>Elif → Ahmet,Deniz,Elif/Cemre,Burak
    {"id": "ll_8",
     "text": "'Yağmur yağarsa yer ıslak olur.' Bu önermenin karşıt anlamlısı (ters kontrapozitif) hangisidir?",
     "options": {"a": "Yağmur yağmazsa yer ıslak olmaz",
                 "b": "Yer ıslak değilse yağmur yağmamıştır",
                 "c": "Yer ıslaksa yağmur yağmıştır",
                 "d": "Yağmur yağarsa yer kuru kalır"},
     "answer": "b"},
    {"id": "ll_9",
     "text": "Bir şifre 4 haneli ve her hane 0-9 arası farklı rakamlardan oluşuyor. İlk hane 0 olamaz. Kaç farklı şifre oluşturulabilir?",
     "options": {"a": "4536", "b": "5040", "c": "3024", "d": "10000"},
     "answer": "a"},  # 9×9×8×7=4536
    {"id": "ll_10",
     "text": "Bir yalancı her zaman yalan söyler, bir dürüst her zaman doğru söyler. Biri diyor ki: 'İkimiz de yalancıyız.' Bu kişi kim olabilir?",
     "options": {"a": "Dürüst", "b": "Yalancı", "c": "İkisi de olabilir", "d": "Hiçbiri olamaz"},
     "answer": "b"},
    {"id": "ll_11",
     "text": "X, Y ve Z üç farklı meslek yapıyor: Doktor, Avukat, Mühendis. X, mühendis değil. Y, doktor değil. Z, ne doktor ne avukat. X'in mesleği nedir?",
     "options": {"a": "Doktor", "b": "Avukat", "c": "Mühendis", "d": "Bilinemez"},
     "answer": "a"},  # Z=Mühendis, Y=Avukat(doktor değil), X=Doktor
    {"id": "ll_12",
     "text": "Bir satranç tahtasında (8×8) iki köşegen üzerinde toplam kaç kare vardır?",
     "options": {"a": "14", "b": "15", "c": "16", "d": "8"},
     "answer": "b"},  # 8+8-1(ortak merkez)=15
]

# ============================================================
# LİSE — AKADEMİK ÖZ-DEĞERLENDİRME (12 soru, Likert 1-5)
# ============================================================
OZ_DEGER_LISE = [
    {"id": "odl_1", "text": "Karmaşık bir konuyu anlayıncaya kadar farklı kaynaklardan araştırırım."},
    {"id": "odl_2", "text": "Sınav öncesi etkili bir çalışma planı yapabilirim."},
    {"id": "odl_3", "text": "Bir metni okuduktan sonra ana fikrini ve alt temalarını belirleyebilirim."},
    {"id": "odl_4", "text": "Matematiksel problemlerde birden fazla çözüm yolu düşünebilirim."},
    {"id": "odl_5", "text": "Eleştirel düşünerek bilgiyi sorgulayabilirim."},
    {"id": "odl_6", "text": "Grup çalışmalarında fikirlerimi etkili bir şekilde ifade edebilirim."},
    {"id": "odl_7", "text": "Uzun vadeli akademik hedeflerim var ve bunlar için çalışıyorum."},
    {"id": "odl_8", "text": "Başarısız olduğumda nedenlerini analiz eder, stratejimi değiştiririm."},
    {"id": "odl_9", "text": "Farklı disiplinler arasında bağlantı kurabilirim."},
    {"id": "odl_10", "text": "Not alarak ve özetleyerek çalışma verimliliğimi artırırım."},
    {"id": "odl_11", "text": "Akademik konularda kendime güveniyorum."},
    {"id": "odl_12", "text": "Öğrendiğim bilgiyi gerçek hayat durumlarına uygulayabilirim."},
]


# ============================================================
# BÖLÜM VE VERSİYON PAKETLERİ
# ============================================================
def get_akademik_sections(version="lise"):
    """Versiyon bazlı bölümleri döndürür."""
    if version == "ilkogretim":
        return [
            {
                "name": "📖 Okuma Anlama",
                "type": "passage_mc",
                "data": OKUMA_ILKOGRETIM,
                "icon": "📖",
            },
            {
                "name": "🔢 Matematiksel Muhakeme",
                "type": "mc",
                "data": MATEMATIK_ILKOGRETIM,
                "icon": "🔢",
            },
            {
                "name": "🧩 Mantıksal Düşünme",
                "type": "mc",
                "data": MANTIK_ILKOGRETIM,
                "icon": "🧩",
            },
            {
                "name": "📝 Akademik Öz-Değerlendirme",
                "type": "likert",
                "data": OZ_DEGER_ILKOGRETIM,
                "icon": "📝",
            },
        ]
    else:
        return [
            {
                "name": "📖 Okuma Anlama",
                "type": "passage_mc",
                "data": OKUMA_LISE,
                "icon": "📖",
            },
            {
                "name": "🔢 Matematiksel Muhakeme",
                "type": "mc",
                "data": MATEMATIK_LISE,
                "icon": "🔢",
            },
            {
                "name": "🧩 Mantıksal Düşünme",
                "type": "mc",
                "data": MANTIK_LISE,
                "icon": "🧩",
            },
            {
                "name": "📝 Akademik Öz-Değerlendirme",
                "type": "likert",
                "data": OZ_DEGER_LISE,
                "icon": "📝",
            },
        ]


def get_total_questions(version="lise"):
    """Toplam soru sayısını döndürür."""
    sections = get_akademik_sections(version)
    total = 0
    for sec in sections:
        if sec["type"] == "passage_mc":
            for passage in sec["data"]:
                total += len(passage["questions"])
        else:
            total += len(sec["data"])
    return total


# ============================================================
# SKORLAMA
# ============================================================
def calculate_akademik(answers, version="lise"):
    """
    Akademik analiz skorlarını hesaplar.

    Parametre
    ---------
    answers : dict  → {question_id: selected_option_key_or_int}
    version : str   → 'lise' veya 'ilkogretim'

    Döndürür
    --------
    dict : Bölüm skorları + genel profil
    """
    sections = get_akademik_sections(version)
    results = {}

    for sec in sections:
        sec_name = sec["name"]
        sec_type = sec["type"]

        if sec_type == "passage_mc":
            correct = total = 0
            for passage in sec["data"]:
                for q in passage["questions"]:
                    total += 1
                    if answers.get(q["id"]) == q["answer"]:
                        correct += 1
            pct = round(correct / max(total, 1) * 100, 1)
            results[sec_name] = {
                "correct": correct, "total": total, "pct": pct,
            }

        elif sec_type == "mc":
            correct = total = 0
            for q in sec["data"]:
                total += 1
                if answers.get(q["id"]) == q["answer"]:
                    correct += 1
            pct = round(correct / max(total, 1) * 100, 1)
            results[sec_name] = {
                "correct": correct, "total": total, "pct": pct,
            }

        elif sec_type == "likert":
            total_score = 0
            count = len(sec["data"])
            for q in sec["data"]:
                val = answers.get(q["id"], 3)
                if isinstance(val, str):
                    try:
                        val = int(val)
                    except ValueError:
                        val = 3
                total_score += val
            max_score = count * 5
            pct = round(total_score / max(max_score, 1) * 100, 1)
            results[sec_name] = {
                "score": total_score, "max": max_score,
                "pct": pct, "count": count,
            }

    # Genel ortalama (performans bölümleri ağırlıklı)
    perf_keys = [k for k in results if "Öz-Değerlendirme" not in k]
    oz_key = [k for k in results if "Öz-Değerlendirme" in k]

    perf_avg = (
        sum(results[k]["pct"] for k in perf_keys) / max(len(perf_keys), 1)
    )
    oz_avg = results[oz_key[0]]["pct"] if oz_key else 0

    # Ağırlıklı ortalama: %75 performans, %25 öz-değerlendirme
    overall = round(perf_avg * 0.75 + oz_avg * 0.25, 1)

    # Seviye belirleme
    if overall >= 80:
        level, level_desc = "Çok Yüksek", "Akademik yetkinlik mükemmel düzeyde."
    elif overall >= 65:
        level, level_desc = "Yüksek", "Akademik yetkinlik ortalamanın üzerinde."
    elif overall >= 50:
        level, level_desc = "Orta", "Akademik yetkinlik ortalama düzeyde."
    elif overall >= 35:
        level, level_desc = "Düşük", "Akademik yetkinlik gelişime açık."
    else:
        level, level_desc = "Çok Düşük", "Akademik destek ihtiyacı tespit edildi."

    # Güçlü ve zayıf alanlar
    perf_sorted = sorted(
        [(k, results[k]["pct"]) for k in perf_keys],
        key=lambda x: x[1], reverse=True,
    )
    strongest = perf_sorted[0] if perf_sorted else ("", 0)
    weakest = perf_sorted[-1] if perf_sorted else ("", 0)

    return {
        "version": version,
        "sections": results,
        "performance_avg": round(perf_avg, 1),
        "self_assessment": oz_avg,
        "overall": overall,
        "level": level,
        "level_desc": level_desc,
        "strongest": {"name": strongest[0], "pct": strongest[1]},
        "weakest": {"name": weakest[0], "pct": weakest[1]},
    }


# ============================================================
# RAPOR ÜRETİCİ
# ============================================================
def generate_akademik_report(scores):
    """Şablon tabanlı metin rapor üretir."""

    ver_label = "İlköğretim" if scores["version"] == "ilkogretim" else "Lise"

    def bar(pct):
        n = max(0, min(10, round(pct / 10)))
        return "█" * n + "░" * (10 - n)

    def level_emoji(pct):
        if pct >= 80:
            return "🟢"
        elif pct >= 50:
            return "🟡"
        return "🔴"

    # Bölüm tablosu
    sec_rows = ""
    for name, data in scores["sections"].items():
        pct = data["pct"]
        if "correct" in data:
            detail = f"{data['correct']}/{data['total']}"
        else:
            detail = f"{data['score']}/{data['max']}"
        sec_rows += f"| {level_emoji(pct)} {name} | {detail} | %{pct} | {bar(pct)} |\n"

    report = f"""# 📚 AKADEMİK ANALİZ RAPORU ({ver_label})

---

## 📊 Genel Akademik Profil

| Gösterge | Değer |
|----------|-------|
| 📈 Genel Akademik Skor | **%{scores['overall']}** |
| 🎯 Performans Ortalaması | %{scores['performance_avg']} |
| 📝 Öz-Değerlendirme | %{scores['self_assessment']} |
| 🏆 Akademik Seviye | **{scores['level']}** |

{bar(scores['overall'])} %{scores['overall']}

{scores['level_desc']}

---

## 📋 Bölüm Bazlı Sonuçlar

| Bölüm | Doğru/Toplam | Yüzde | Grafik |
|-------|-------------|-------|--------|
{sec_rows}

---

## 💪 En Güçlü Alan: {scores['strongest']['name']}

%{scores['strongest']['pct']} başarı oranıyla en güçlü performans bu alanda gösterildi.

## 🌱 Gelişim Alanı: {scores['weakest']['name']}

%{scores['weakest']['pct']} başarı oranıyla bu alan gelişim potansiyeli taşıyor.

---

## 🔍 Detaylı Yorum

"""

    sections = scores["sections"]

    # Okuma anlama yorumu
    for key in sections:
        if "Okuma" in key:
            pct = sections[key]["pct"]
            if pct >= 75:
                report += (
                    "**📖 Okuma Anlama:** Metin kavrama becerisi güçlü. Ana fikir, çıkarım ve "
                    "detay sorularında yüksek başarı gösterildi. Bu beceri tüm derslerin "
                    "temelidir ve güçlü bir avantaj sağlar.\n\n"
                )
            elif pct >= 50:
                report += (
                    "**📖 Okuma Anlama:** Orta düzeyde metin kavrama becerisi. Ana fikir "
                    "genellikle doğru tespit ediliyor, ancak çıkarım ve derinlemesine analiz "
                    "sorularında gelişim potansiyeli var. Düzenli kitap okuma alışkanlığı "
                    "bu alanı güçlendirecektir.\n\n"
                )
            else:
                report += (
                    "**📖 Okuma Anlama:** Metin kavrama becerisinde gelişim ihtiyacı var. "
                    "Okuduğunu anlama stratejileri (altını çizme, not alma, özetleme) "
                    "öğretilmeli. Yaşa uygun kitaplarla düzenli okuma programı önerilir.\n\n"
                )

    # Matematik yorumu
    for key in sections:
        if "Matematik" in key:
            pct = sections[key]["pct"]
            if pct >= 75:
                report += (
                    "**🔢 Matematiksel Muhakeme:** Sayısal düşünme ve problem çözme becerisi "
                    "güçlü. Soyut düşünme kapasitesi yüksek.\n\n"
                )
            elif pct >= 50:
                report += (
                    "**🔢 Matematiksel Muhakeme:** Temel matematiksel işlemlerde yetkin, "
                    "ancak çok adımlı problem çözmede gelişim alanı var. Günlük hayattan "
                    "problem çözme pratikleri faydalı olacaktır.\n\n"
                )
            else:
                report += (
                    "**🔢 Matematiksel Muhakeme:** Sayısal düşünme becerisinde destek "
                    "ihtiyacı tespit edildi. Temel kavramların pekiştirilmesi ve adım adım "
                    "problem çözme stratejilerinin öğretilmesi önerilir.\n\n"
                )

    # Mantık yorumu
    for key in sections:
        if "Mantık" in key:
            pct = sections[key]["pct"]
            if pct >= 75:
                report += (
                    "**🧩 Mantıksal Düşünme:** Analitik düşünme, örüntü tanıma ve "
                    "çıkarım yapma becerileri güçlü. Bu yetenek akademik başarının "
                    "temel taşlarından biridir.\n\n"
                )
            elif pct >= 50:
                report += (
                    "**🧩 Mantıksal Düşünme:** Temel mantık becerileri mevcut, "
                    "karmaşık çıkarım sorularında gelişim potansiyeli var. Bulmaca, "
                    "strateji oyunları ve mantık soruları pratik için idealdir.\n\n"
                )
            else:
                report += (
                    "**🧩 Mantıksal Düşünme:** Mantıksal düşünme becerisinde destek "
                    "ihtiyacı var. Sıralama, gruplama ve basit çıkarım alıştırmaları "
                    "ile kademeli gelişim sağlanabilir.\n\n"
                )

    # Öz-değerlendirme yorumu
    for key in sections:
        if "Öz-Değerlendirme" in key:
            pct = sections[key]["pct"]
            perf = scores["performance_avg"]
            gap = pct - perf

            if abs(gap) <= 10:
                report += (
                    "**📝 Öz-Değerlendirme:** Öğrencinin kendini değerlendirmesi "
                    "gerçek performansıyla tutarlı. Bu, sağlıklı bir akademik "
                    "farkındalık göstergesidir.\n\n"
                )
            elif gap > 10:
                report += (
                    "**📝 Öz-Değerlendirme:** Öğrenci kendini gerçek performansından "
                    f"daha yüksek değerlendiriyor (öz: %{pct}, performans: %{perf}). "
                    "Bu, motivasyon için olumlu olsa da gerçekçi hedef belirleme "
                    "konusunda rehberlik gerekebilir.\n\n"
                )
            else:
                report += (
                    "**📝 Öz-Değerlendirme:** Öğrenci kendini gerçek performansının "
                    f"altında değerlendiriyor (öz: %{pct}, performans: %{perf}). "
                    "Akademik özgüven geliştirilmeli. Başarılarını fark etmesini "
                    "sağlayacak pozitif geri bildirim önemlidir.\n\n"
                )

    report += f"""---

## 💡 Genel Öneriler

"""

    if scores["overall"] >= 65:
        report += (
            "- 🏆 Akademik performans güçlü — zenginleştirme programları ve ileri düzey "
            "materyallerle meydan okuma oluşturulmalı\n"
            "- 📚 Güçlü alanlar üzerinden zayıf alanları destekleme stratejisi uygulanabilir\n"
            "- 🎯 Yarışma ve proje bazlı çalışmalarla motivasyon artırılabilir\n"
        )
    elif scores["overall"] >= 50:
        report += (
            "- 📋 Bireysel çalışma planı oluşturulmalı — zayıf alanlara haftada ekstra 2 saat\n"
            "- 🧩 Öğrenme stiline uygun materyaller kullanılmalı (VARK testi ile birlikte değerlendir)\n"
            "- ⏰ Düzenli tekrar programı (spaced repetition) uygulanmalı\n"
            "- 💪 Başarı deneyimleri yaşatarak akademik özgüven geliştirilmeli\n"
        )
    else:
        report += (
            "- 🆘 Acil akademik destek programı başlatılmalı\n"
            "- 📖 Temel okuma anlama becerileri öncelikli olarak güçlendirilmeli\n"
            "- 🔢 Matematik temelleri (sayı kavramı, dört işlem) pekiştirilmeli\n"
            "- 👨‍🏫 Birebir öğretmen desteği veya özel ders önerilir\n"
            "- 🏥 Öğrenme güçlüğü açısından uzman değerlendirmesi düşünülebilir\n"
        )

    report += f"""
---

## 📌 Özet Tablo

| Gösterge | Sonuç |
|----------|-------|
| Versiyon | {ver_label} |
| Genel Skor | **%{scores['overall']}** ({scores['level']}) |
| En Güçlü Alan | {scores['strongest']['name']} (%{scores['strongest']['pct']}) |
| Gelişim Alanı | {scores['weakest']['name']} (%{scores['weakest']['pct']}) |
| Performans / Öz-Değerlendirme | %{scores['performance_avg']} / %{scores['self_assessment']} |
"""
    return report.strip()
