# ============================================================
# akademik_engine.py — v2.0
# Sınıf Bazlı + Zorluk Kademeli + Alt Beceri Etiketli
# 4 Kademe: 5-6 / 7-8 / 9-10 / 11-12
# Her kademe: Okuma(20) + Mat(20) + Mantık(15) + ÖzDeğ(12) = 67
# ============================================================

KADEME_MAP = {5: "kademe_1", 6: "kademe_1", 7: "kademe_2", 8: "kademe_2",
              9: "kademe_3", 10: "kademe_3", 11: "kademe_4", 12: "kademe_4"}

KADEME_LABELS = {"kademe_1": "5-6. Sınıf (Temel)", "kademe_2": "7-8. Sınıf (Orta)",
                 "kademe_3": "9-10. Sınıf (İleri)", "kademe_4": "11-12. Sınıf (Üst)"}

DIFFICULTY_WEIGHTS = {"kolay": 1, "orta": 2, "zor": 3}

SKILL_LABELS = {
    "detay_bulma": "Detay Bulma", "ana_fikir": "Ana Fikir", "cikarim": "Çıkarım Yapma",
    "soz_varligi": "Söz Varlığı", "yazar_tutumu": "Yazarın Tutumu", "karsilastirma": "Karşılaştırma",
    "hesaplama": "Temel Hesaplama", "problem_cozme": "Problem Çözme", "geometri": "Geometri",
    "veri_yorumlama": "Veri Yorumlama", "cebir": "Cebirsel Düşünme", "olasilik": "Olasılık",
    "oran_orant": "Oran-Orantı / Yüzde",
    "analoji": "Analoji", "seri": "Seri Tamamlama", "kiyas": "Kıyas / Tasım",
    "siralama": "Sıralama", "mantiksal_cikarim": "Mantıksal Çıkarım",
}

def grade_to_kademe(grade):
    return KADEME_MAP.get(grade, "kademe_2")

# ============================================================
# KADEME 1 — 5-6. SINIF
# ============================================================
K1_OKUMA = [
    {"passage": "Arılar, doğadaki en çalışkan canlılardan biridir. Bir bal arısı, yaşamı boyunca sadece bir çay kaşığının on ikide biri kadar bal üretir. Bir kavanoz bal üretmek için arıların yaklaşık 3,5 milyon çiçeği ziyaret etmesi gerekir. Arılar balı üretirken aynı zamanda bitkilerin tozlaşmasını da sağlar. Bilim insanları, arıların yok olması durumunda birçok meyve ve sebzenin de yok olacağını söylemektedir.",
     "questions": [
        {"id":"k1_oa_1","text":"Bir bal arısı yaşamı boyunca ne kadar bal üretir?","options":{"a":"Bir çay kaşığı","b":"Bir çay kaşığının on ikide biri","c":"Bir kavanoz","d":"Hiç üretmez"},"answer":"b","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k1_oa_2","text":"Bir kavanoz bal için yaklaşık kaç çiçek ziyaret edilir?","options":{"a":"350 bin","b":"35 bin","c":"3,5 milyon","d":"35 milyon"},"answer":"c","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k1_oa_3","text":"Arıların tozlaşma yapmasının doğaya faydası nedir?","options":{"a":"Balın tadını güzelleştirir","b":"Bitkilerin üremesini sağlar","c":"Arıların daha hızlı uçmasını sağlar","d":"Çiçeklerin rengini değiştirir"},"answer":"b","difficulty":"orta","skill":"cikarim"},
        {"id":"k1_oa_4","text":"Metnin ana fikri nedir?","options":{"a":"Arılar çok hızlı uçar","b":"Bal çok lezzetlidir","c":"Arılar doğa için çok önemli ve çalışkan canlılardır","d":"Arılar tehlikeli böceklerdir"},"answer":"c","difficulty":"orta","skill":"ana_fikir"},
        {"id":"k1_oa_5","text":"Arılar yok olursa ne gibi bir sonuç beklenir?","options":{"a":"Balın fiyatı düşer","b":"Meyve ve sebze üretimi ciddi şekilde azalır","c":"Çiçekler daha güzel açar","d":"Başka böcekler bal üretmeye başlar"},"answer":"b","difficulty":"zor","skill":"cikarim"},
    ]},
    {"passage": "Su, yeryüzünün yaklaşık yüzde yetmişini kaplar. Ancak bu suyun büyük çoğunluğu tuzlu su olan okyanuslardadır. İçilebilir tatlı su, toplam suyun sadece yüzde üçünü oluşturur. Üstelik bu tatlı suyun da büyük bölümü kutuplardaki buzullarda donmuş hâldedir. İnsanların kolayca kullanabileceği tatlı su kaynakları — nehirler, göller ve yeraltı suları — dünyadaki toplam suyun yüzde birinden bile azdır.",
     "questions": [
        {"id":"k1_oa_6","text":"Yeryüzünün yüzde kaçı suyla kaplıdır?","options":{"a":"%30","b":"%50","c":"%70","d":"%90"},"answer":"c","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k1_oa_7","text":"Tatlı su toplam suyun yüzde kaçını oluşturur?","options":{"a":"%1","b":"%3","c":"%10","d":"%30"},"answer":"b","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k1_oa_8","text":"Tatlı suyun büyük bölümü nerededir?","options":{"a":"Nehirlerde","b":"Göllerde","c":"Kutuplardaki buzullarda","d":"Okyanuslarda"},"answer":"c","difficulty":"orta","skill":"detay_bulma"},
        {"id":"k1_oa_9","text":"Metinden çıkarılabilecek en önemli sonuç nedir?","options":{"a":"Okyanuslar çok büyüktür","b":"Kullanılabilir tatlı su çok kısıtlıdır","c":"Buzullar erimelidir","d":"Tuzlu su içilebilir yapılabilir"},"answer":"b","difficulty":"orta","skill":"cikarim"},
        {"id":"k1_oa_10","text":"'İnsanların kolayca kullanabileceği' ifadesiyle ne kastedilmektedir?","options":{"a":"Her türlü su","b":"Sadece şişe suyu","c":"Arıtma gerektirmeden ulaşılabilen nehir, göl ve yeraltı suları","d":"Okyanus suyu"},"answer":"c","difficulty":"zor","skill":"soz_varligi"},
    ]},
    {"passage": "Eski Mısırlılar, papirüs bitkisinden kâğıt benzeri bir malzeme üretmeyi başaran ilk uygarlıklardan biridir. Papirüs, Nil Nehri kıyılarında yetişen uzun bir saz bitkisidir. Mısırlılar bu bitkinin gövdesini ince şeritler hâlinde kesiyor, şeritleri yan yana ve üst üste diziyordu. Sonra ağır taşlarla presleyerek düzleştiriyorlardı. Kuruyan yaprak, yazı yazmaya uygun pürüzsüz bir yüzey oluyordu.",
     "questions": [
        {"id":"k1_oa_11","text":"Papirüs bitkisi nerede yetişir?","options":{"a":"Çöllerde","b":"Dağlarda","c":"Nil Nehri kıyılarında","d":"Deniz altında"},"answer":"c","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k1_oa_12","text":"Mısırlılar papirüsü nasıl düzleştiriyordu?","options":{"a":"Ateşle ısıtarak","b":"Ağır taşlarla presleyerek","c":"Suya batırarak","d":"Rüzgârda kurulayarak"},"answer":"b","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k1_oa_13","text":"Papirüs üretiminin doğru sıralaması hangisidir?","options":{"a":"Kes → Diz → Presle → Kurut","b":"Presle → Diz → Kurut → Kes","c":"Kurut → Kes → Presle → Diz","d":"Diz → Kes → Kurut → Presle"},"answer":"a","difficulty":"orta","skill":"cikarim"},
        {"id":"k1_oa_14","text":"Bu metne en uygun başlık hangisidir?","options":{"a":"Nil Nehri","b":"Kâğıdın Tarihi: Papirüs","c":"Eski Mısır Piramitleri","d":"Bitkilerden Yapılan Eşyalar"},"answer":"b","difficulty":"orta","skill":"ana_fikir"},
        {"id":"k1_oa_15","text":"Papirüs üretimi Mısırlılar için neden önemli olmuş olabilir?","options":{"a":"Ticaret için kullandılar","b":"Bilgilerini yazarak gelecek kuşaklara aktardılar","c":"Ev yapımında kullandılar","d":"Yemek pişirmek için kullandılar"},"answer":"b","difficulty":"zor","skill":"cikarim"},
    ]},
    {"passage": "Her yıl milyonlarca kuş, mevsim değişimiyle birlikte uzun yolculuklara çıkar. Buna göç denir. Kuşlar genellikle soğuk mevsimde sıcak bölgelere, sıcak mevsimde ise tekrar yaşadıkları yere dönerler. Leylekler, kırlangıçlar ve flamingolar göç eden kuşlara örnektir. Bilim insanları, kuşların yollarını güneşin konumuna, yıldızlara ve dünyanın manyetik alanına bakarak bulduklarını keşfetmiştir.",
     "questions": [
        {"id":"k1_oa_16","text":"Göç nedir?","options":{"a":"Kuşların yuva yapması","b":"Kuşların mevsime göre uzun yolculuklara çıkması","c":"Kuşların yavrulaması","d":"Kuşların uyuması"},"answer":"b","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k1_oa_17","text":"Aşağıdakilerden hangisi göç eden bir kuştur?","options":{"a":"Serçe","b":"Kartal","c":"Leylek","d":"Papağan"},"answer":"c","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k1_oa_18","text":"Kuşlar göç sırasında yollarını nasıl bulur?","options":{"a":"İnsanlardan sorar","b":"Güneş, yıldızlar ve manyetik alan sayesinde","c":"Harita kullanır","d":"Sadece hafızasını kullanır"},"answer":"b","difficulty":"orta","skill":"detay_bulma"},
        {"id":"k1_oa_19","text":"Kuşlar neden sıcak bölgelere göç eder?","options":{"a":"Güzel manzara için","b":"Soğukta yiyecek bulmak zorlaştığı için","c":"İnsanlardan kaçmak için","d":"Yarış yapmak için"},"answer":"b","difficulty":"orta","skill":"cikarim"},
        {"id":"k1_oa_20","text":"Manyetik alan kuşlar için neden önemlidir?","options":{"a":"Uçmalarını kolaylaştırır","b":"Yön bulmalarına yardımcı olur","c":"Daha hızlı uçmalarını sağlar","d":"Avlanmalarını kolaylaştırır"},"answer":"b","difficulty":"zor","skill":"cikarim"},
    ]},
]

K1_MATEMATIK = [
    {"id":"k1_m_1","text":"Bir markette elmalar 3'lü paketlerde satılıyor. 5 paket alan kişi kaç elma almış olur?","options":{"a":"12","b":"8","c":"15","d":"18"},"answer":"c","difficulty":"kolay","skill":"hesaplama"},
    {"id":"k1_m_2","text":"425 + 378 = ?","options":{"a":"793","b":"803","c":"813","d":"703"},"answer":"b","difficulty":"kolay","skill":"hesaplama"},
    {"id":"k1_m_3","text":"Bir dikdörtgenin uzun kenarı 12 cm, kısa kenarı 8 cm. Çevresi kaç cm'dir?","options":{"a":"96","b":"40","c":"20","d":"36"},"answer":"b","difficulty":"kolay","skill":"geometri"},
    {"id":"k1_m_4","text":"5, 10, 20, 40, … serisinde sonraki sayı kaçtır?","options":{"a":"60","b":"50","c":"80","d":"100"},"answer":"c","difficulty":"kolay","skill":"hesaplama"},
    {"id":"k1_m_5","text":"Bir pizzanın 3/8'i yendikten sonra kalan kısmı kaçta kaçtır?","options":{"a":"5/8","b":"3/5","c":"1/2","d":"4/8"},"answer":"a","difficulty":"kolay","skill":"hesaplama"},
    {"id":"k1_m_6","text":"Bir sınıfta 30 öğrenci var. Yarısı erkekse kaç kız öğrenci vardır?","options":{"a":"10","b":"20","c":"15","d":"25"},"answer":"c","difficulty":"kolay","skill":"hesaplama"},
    {"id":"k1_m_7","text":"Bir karenin bir kenarı 9 cm ise alanı kaç cm²'dir?","options":{"a":"36","b":"81","c":"72","d":"18"},"answer":"b","difficulty":"kolay","skill":"geometri"},
    {"id":"k1_m_8","text":"Saat 08:45'te yola çıktın, 1 saat 30 dakika sonra vardın. Kaçta vardın?","options":{"a":"09:45","b":"10:15","c":"10:45","d":"09:15"},"answer":"b","difficulty":"kolay","skill":"hesaplama"},
    {"id":"k1_m_9","text":"Bir çiftlikte 24 tavuk ve 18 koyun var. Hayvanların toplam ayak sayısı kaçtır?","options":{"a":"84","b":"120","c":"96","d":"108"},"answer":"b","difficulty":"orta","skill":"problem_cozme"},
    {"id":"k1_m_10","text":"Ali'nin 120 TL'si vardı. Üçte birini kitaba harcadı. Elinde kaç TL kaldı?","options":{"a":"40","b":"60","c":"80","d":"90"},"answer":"c","difficulty":"orta","skill":"problem_cozme"},
    {"id":"k1_m_11","text":"Bir sınıfta 30 öğrenci var. %60'ı kız ise kaç erkek öğrenci vardır?","options":{"a":"18","b":"15","c":"12","d":"20"},"answer":"c","difficulty":"orta","skill":"oran_orant"},
    {"id":"k1_m_12","text":"3 kg elma 45 TL ise 7 kg elma kaç TL'dir?","options":{"a":"90","b":"105","c":"95","d":"115"},"answer":"b","difficulty":"orta","skill":"oran_orant"},
    {"id":"k1_m_13","text":"Ayşe saatte 4 km yürüyor. 2 saat 30 dakikada kaç km yol alır?","options":{"a":"8","b":"10","c":"12","d":"6"},"answer":"b","difficulty":"orta","skill":"problem_cozme"},
    {"id":"k1_m_14","text":"Bir kutuya her gün 7 bilye atılıyor. 4 gün sonra kutudan 10 bilye alınırsa kutuda kaç bilye kalır?","options":{"a":"18","b":"28","c":"38","d":"17"},"answer":"a","difficulty":"orta","skill":"problem_cozme"},
    {"id":"k1_m_15","text":"Bir üçgenin iki açısı 55° ve 75° ise üçüncü açısı kaç derecedir?","options":{"a":"40","b":"50","c":"60","d":"130"},"answer":"b","difficulty":"orta","skill":"geometri"},
    {"id":"k1_m_16","text":"Bir otopark saati 5 TL. Ahmet 3 saat, Zeynep 5 saat park etti. Toplam ne kadar ödediler?","options":{"a":"30","b":"35","c":"40","d":"25"},"answer":"c","difficulty":"orta","skill":"problem_cozme"},
    {"id":"k1_m_17","text":"Ali parasının 1/3'ünü kitaba, kalanın yarısını kaleme harcadı. Başta 120 TL varsa elinde kaç TL kaldı?","options":{"a":"40","b":"60","c":"30","d":"80"},"answer":"a","difficulty":"zor","skill":"problem_cozme"},
    {"id":"k1_m_18","text":"Bir bahçenin uzunluğu genişliğinin 2 katı. Çevresi 36 m ise alanı kaç m²?","options":{"a":"54","b":"72","c":"48","d":"36"},"answer":"b","difficulty":"zor","skill":"geometri"},
    {"id":"k1_m_19","text":"Her öğrenciye 4 kalem verilirse 3 artar, 5 kalem verilirse 7 eksik kalır. Kaç öğrenci var?","options":{"a":"8","b":"10","c":"12","d":"15"},"answer":"b","difficulty":"zor","skill":"cebir"},
    {"id":"k1_m_20","text":"Saat 09:45 gösteriyor. 2 saat 30 dakika önce saat kaçtı?","options":{"a":"7:15","b":"7:45","c":"6:15","d":"8:15"},"answer":"a","difficulty":"zor","skill":"problem_cozme"},
]

K1_MANTIK = [
    {"id":"k1_l_1","text":"Elma → Meyve, Köpek → Hayvan, Gül → ?","options":{"a":"Ağaç","b":"Bahçe","c":"Çiçek","d":"Yaprak"},"answer":"c","difficulty":"kolay","skill":"analoji"},
    {"id":"k1_l_2","text":"Kitap → Okumak, Bıçak → Kesmek, Kalem → ?","options":{"a":"Silmek","b":"Çizmek","c":"Yazmak","d":"Boyamak"},"answer":"c","difficulty":"kolay","skill":"analoji"},
    {"id":"k1_l_3","text":"2, 4, 6, 8, … serisinde sonraki sayı kaçtır?","options":{"a":"9","b":"10","c":"11","d":"12"},"answer":"b","difficulty":"kolay","skill":"seri"},
    {"id":"k1_l_4","text":"Hangisi diğerlerinden farklıdır? Masa, Sandalye, Elma, Dolap","options":{"a":"Masa","b":"Sandalye","c":"Elma","d":"Dolap"},"answer":"c","difficulty":"kolay","skill":"analoji"},
    {"id":"k1_l_5","text":"Göz → Görmek, Kulak → ?","options":{"a":"Yemek","b":"Duymak","c":"Koklamak","d":"Dokunmak"},"answer":"b","difficulty":"kolay","skill":"analoji"},
    {"id":"k1_l_6","text":"1, 3, 5, 7, 9, … serisinde 10. sayı kaçtır?","options":{"a":"17","b":"19","c":"21","d":"15"},"answer":"b","difficulty":"kolay","skill":"seri"},
    {"id":"k1_l_7","text":"2, 6, 12, 20, 30, … serisinde sonraki sayı kaçtır?","options":{"a":"36","b":"40","c":"42","d":"44"},"answer":"c","difficulty":"orta","skill":"seri"},
    {"id":"k1_l_8","text":"Ayşe, Mehmet'ten uzun. Mehmet, Ali'den uzun. En kısa kim?","options":{"a":"Ayşe","b":"Mehmet","c":"Ali","d":"Bilinemez"},"answer":"c","difficulty":"orta","skill":"siralama"},
    {"id":"k1_l_9","text":"Tüm kediler hayvandır. Bazı hayvanlar uçar. Hangisi kesinlikle doğrudur?","options":{"a":"Bazı kediler uçar","b":"Hiçbir kedi uçamaz","c":"Tüm kediler hayvandır","d":"Tüm hayvanlar kedidir"},"answer":"c","difficulty":"orta","skill":"kiyas"},
    {"id":"k1_l_10","text":"A, C, F, J, … sonraki harf? (A=1,B=2,...)","options":{"a":"M","b":"N","c":"O","d":"P"},"answer":"c","difficulty":"orta","skill":"seri"},
    {"id":"k1_l_11","text":"Cem, Deniz'den yaşlı. Deniz, Elif'ten yaşlı. Elif, Cem'den yaşlı olabilir mi?","options":{"a":"Evet","b":"Hayır","c":"Belki","d":"Bilgi yetersiz"},"answer":"b","difficulty":"orta","skill":"siralama"},
    {"id":"k1_l_12","text":"81, 27, 9, 3, … serisinde sonraki sayı kaçtır?","options":{"a":"0","b":"1","c":"2","d":"-3"},"answer":"b","difficulty":"orta","skill":"seri"},
    {"id":"k1_l_13","text":"4 arkadaş sırada. Ahmet Zeynep'in solunda. Burak en sağda. Elif Ahmet-Burak arasında. Soldan sıra?","options":{"a":"Zeynep-Ahmet-Elif-Burak","b":"Ahmet-Zeynep-Elif-Burak","c":"Zeynep-Elif-Ahmet-Burak","d":"Ahmet-Elif-Zeynep-Burak"},"answer":"a","difficulty":"zor","skill":"siralama"},
    {"id":"k1_l_14","text":"Pazartesi bugünse 100 gün sonra hangi gündür?","options":{"a":"Çarşamba","b":"Perşembe","c":"Cuma","d":"Cumartesi"},"answer":"a","difficulty":"zor","skill":"mantiksal_cikarim"},
    {"id":"k1_l_15","text":"3 kutu var: biri kırmızı, biri mavi, biri karışık toplu. Kutular YANLIŞ etiketli. 'Karışık' kutusundan 1 top çektin, kırmızı geldi. Bu kutuda gerçekte ne var?","options":{"a":"Karışık","b":"Mavi","c":"Kırmızı","d":"Bilinemez"},"answer":"c","difficulty":"zor","skill":"mantiksal_cikarim"},
]

K1_OZ_DEGER = [
    {"id":"k1_od_1","text":"Ders çalışırken konuya kolayca odaklanabilirim."},
    {"id":"k1_od_2","text":"Bir konuyu anlamazsam tekrar tekrar çalışırım."},
    {"id":"k1_od_3","text":"Sınavlarda kendime güvenirim."},
    {"id":"k1_od_4","text":"Okuduğum metinleri anlayıp özetleyebilirim."},
    {"id":"k1_od_5","text":"Matematik problemlerini çözmekten keyif alırım."},
    {"id":"k1_od_6","text":"Ödevlerimi zamanında tamamlarım."},
    {"id":"k1_od_7","text":"Yeni konuları öğrenmek beni heyecanlandırır."},
    {"id":"k1_od_8","text":"Arkadaşlarıma bir konuyu açıklayabilirim."},
    {"id":"k1_od_9","text":"Zor bir soruyla karşılaşınca pes etmem."},
    {"id":"k1_od_10","text":"Ders çalışma planı yapıp ona uyarım."},
    {"id":"k1_od_11","text":"Derslerde söz alıp fikrimi söyleyebilirim."},
    {"id":"k1_od_12","text":"Öğrendiklerimi günlük hayatta kullanabilirim."},
]


# ============================================================
# KADEME 2 — 7-8. SINIF (ORTA / LGS)
# ============================================================
K2_OKUMA = [
    {"passage": "Yapay zekâ teknolojilerinin hızla gelişmesi toplumda hem heyecan hem de endişe yaratmaktadır. Bir yandan tıpta erken tanı, eğitimde kişiselleştirilmiş öğrenme ve endüstride verimlilik artışı gibi somut faydalar sağlanırken; öte yandan iş gücü piyasasında köklü dönüşümler beklenmektedir. Uzmanlar, 2030 yılına kadar mevcut mesleklerin yaklaşık üçte birinin otomasyona bağlı olarak dönüşeceğini öngörmektedir. Kritik olan, bireylerin yaşam boyu öğrenme becerisini kazanmasıdır.",
     "questions": [
        {"id":"k2_oa_1","text":"Yapay zekânın sağladığı faydalardan biri hangisidir?","options":{"a":"İşsizliğin artması","b":"Eğitimde kişiselleştirilmiş öğrenme","c":"Mesleklerin tamamen yok olması","d":"Teknolojinin yavaşlaması"},"answer":"b","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k2_oa_2","text":"2030'a kadar mesleklerin ne kadarı dönüşecek?","options":{"a":"Tamamı","b":"Yarısı","c":"Yaklaşık üçte biri","d":"Onda biri"},"answer":"c","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k2_oa_3","text":"Metne göre bireyler için kritik olan beceri nedir?","options":{"a":"Tek meslekte uzmanlaşmak","b":"Teknolojiden uzak durmak","c":"Yaşam boyu öğrenme","d":"Erken emekli olmak"},"answer":"c","difficulty":"orta","skill":"ana_fikir"},
        {"id":"k2_oa_4","text":"Yazarın yapay zekâya karşı tutumu nasıldır?","options":{"a":"Tamamen olumsuz","b":"Tamamen olumlu","c":"Dengeli — hem fırsatları hem riskleri ele alan","d":"Kayıtsız"},"answer":"c","difficulty":"orta","skill":"yazar_tutumu"},
        {"id":"k2_oa_5","text":"Metinden çıkarılacak en güçlü sonuç nedir?","options":{"a":"Teknoloji kötüdür","b":"Değişime uyum sağlayanlar avantajlı olacak","c":"Tüm meslekler yok olacak","d":"Eğitimin önemi azalacak"},"answer":"b","difficulty":"zor","skill":"cikarim"},
    ]},
    {"passage": "Fotosentez, canlı yaşamın temelini oluşturan biyokimyasal süreçtir. Bitkiler, güneş enerjisini kullanarak karbondioksit ve suyu glikoz ve oksijene dönüştürür. Bu süreç atmosferdeki oksijen miktarını dengede tutarken besin zincirinin ilk halkasını oluşturur. Yağmur ormanları yılda yaklaşık 28 milyar ton karbondioksiti absorbe eder. Ancak ormansızlaşma bu kapasiteyi hızla azaltmaktadır. Yapay fotosentez teknolojileri henüz doğal sürecin verimliliğine ulaşamamıştır.",
     "questions": [
        {"id":"k2_oa_6","text":"Fotosentezin girdileri nelerdir?","options":{"a":"Oksijen ve glikoz","b":"Karbondioksit ve su","c":"Güneş ve oksijen","d":"Glikoz ve su"},"answer":"b","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k2_oa_7","text":"Yağmur ormanları yılda ne kadar CO₂ absorbe eder?","options":{"a":"28 milyon ton","b":"2,8 milyar ton","c":"28 milyar ton","d":"280 milyar ton"},"answer":"c","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k2_oa_8","text":"Fotosentez besin zincirindeki rolü nedir?","options":{"a":"Son halka","b":"Orta halka","c":"İlk halka — besin üretir","d":"İlgisi yoktur"},"answer":"c","difficulty":"orta","skill":"cikarim"},
        {"id":"k2_oa_9","text":"Yapay fotosentezle ilgili metnin söylediği nedir?","options":{"a":"Doğaldan daha verimli","b":"Henüz doğal sürecin verimliliğine ulaşamadı","c":"Tamamen başarısız","d":"Ormansızlaşmayı durdurdu"},"answer":"b","difficulty":"orta","skill":"detay_bulma"},
        {"id":"k2_oa_10","text":"Metnin ana argümanı nedir?","options":{"a":"Yapay fotosentez doğal olanın yerini alacak","b":"Fotosentez hayati ama ormansızlaşma bu sistemi tehdit ediyor","c":"Bitkiler gereksizdir","d":"CO₂ zararsızdır"},"answer":"b","difficulty":"zor","skill":"ana_fikir"},
    ]},
    {"passage": "Osmanlı döneminde vakıf sistemi toplumsal dayanışmanın temel kurumlarından biriydi. Varlıklı kişiler camiler, medreseler, kervansaraylar, çeşmeler ve hastaneler inşa ettirerek bunları vakıf yoluyla toplumun hizmetine sunardı. Vakıf gelirleri dükkân, han veya tarım arazisi kiralarından elde edilirdi. Bu gelirlerle kurumların bakımı yapılır, çalışanların maaşları ödenir ve yoksullara yardım edilirdi. Vakıf sistemi devlet bütçesine yük olmadan sosyal hizmetlerin sürdürülmesini sağlayan ileri bir modeldi.",
     "questions": [
        {"id":"k2_oa_11","text":"Vakıf gelirleri nereden elde edilirdi?","options":{"a":"Devlet bütçesinden","b":"Savaş ganimetlerinden","c":"Dükkân, han ve arazi kiralarından","d":"Vergi toplamaktan"},"answer":"c","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k2_oa_12","text":"Hangisi vakıf gelirlerinin kullanım alanı DEĞİLDİR?","options":{"a":"Kurumların bakımı","b":"Çalışan maaşları","c":"Yoksullara yardım","d":"Padişahın saray masrafları"},"answer":"d","difficulty":"orta","skill":"cikarim"},
        {"id":"k2_oa_13","text":"Vakıf sisteminin en önemli özelliği nedir?","options":{"a":"Devletten bağımsız sosyal hizmet sunması","b":"Sadece zenginlere hizmet vermesi","c":"Askeri amaçlarla kurulması","d":"Sadece eğitim alanında çalışması"},"answer":"a","difficulty":"orta","skill":"ana_fikir"},
        {"id":"k2_oa_14","text":"'Zamanının çok ötesinde' ifadesiyle yazar ne demek istiyor?","options":{"a":"Sistem çok eskiydi","b":"Sistem kendi dönemine göre çok ileriydi","c":"Sistem işe yaramıyordu","d":"Sistem karmaşıktı"},"answer":"b","difficulty":"orta","skill":"soz_varligi"},
        {"id":"k2_oa_15","text":"Günümüzde vakıf sisteminin benzeri ne olabilir?","options":{"a":"Vergi sistemi","b":"Askerlik hizmeti","c":"Sivil toplum kuruluşları ve hayır kurumları","d":"Siyasi partiler"},"answer":"c","difficulty":"zor","skill":"karsilastirma"},
    ]},
    {"passage": "İnsan beyni yaklaşık 86 milyar nörondan oluşur. Her nöron binlerce başka nöronla bağlantı kurabilir; bu bağlantılara sinaps denir. Öğrenme süreci aslında nöronlar arası yeni sinapsların oluşması ve mevcut bağlantıların güçlenmesidir. Araştırmalar, düzenli olarak yeni şeyler öğrenen insanların beyninde daha yoğun sinaptik ağlar oluştuğunu göstermektedir. Beyin bir kas gibi çalıştıkça güçlenir. Bu nedenle bilim insanları 'beyin plastiği' kavramını kullanarak beynin yaşam boyu değişebileceğini vurgular.",
     "questions": [
        {"id":"k2_oa_16","text":"İnsan beyninde yaklaşık kaç nöron vardır?","options":{"a":"86 milyon","b":"86 milyar","c":"860 milyar","d":"8,6 milyar"},"answer":"b","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k2_oa_17","text":"Sinaps nedir?","options":{"a":"Bir beyin hastalığı","b":"Nöronlar arası bağlantı","c":"Bir beyin bölgesi","d":"Bir hormon"},"answer":"b","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k2_oa_18","text":"Öğrenme sürecinde beyinde ne olur?","options":{"a":"Nöronlar ölür","b":"Yeni sinapslar oluşur ve mevcut bağlantılar güçlenir","c":"Beyin küçülür","d":"Nöron sayısı ikiye katlanır"},"answer":"b","difficulty":"orta","skill":"cikarim"},
        {"id":"k2_oa_19","text":"'Beyin plastiği' kavramı ne anlama gelir?","options":{"a":"Beyin plastikten yapılmıştır","b":"Beyin yaşam boyu değişebilir ve gelişebilir","c":"Beyin kırılgandır","d":"Beyin sabit ve değişmezdir"},"answer":"b","difficulty":"orta","skill":"soz_varligi"},
        {"id":"k2_oa_20","text":"Bu metinden öğrenciler için çıkarılacak en önemli ders nedir?","options":{"a":"Beyni kullanmamak gerekir","b":"Öğrenmeye devam etmek beyni güçlendirir","c":"86 milyar nöron yeterlidir","d":"Beyin yaşlandıkça zayıflar"},"answer":"b","difficulty":"zor","skill":"cikarim"},
    ]},
]

K2_MATEMATIK = [
    {"id":"k2_m_1","text":"Bir ürünün fiyatı önce %20 artırıldı, sonra %20 indirildi. Son fiyat başlangıca göre nasıl?","options":{"a":"Aynı kaldı","b":"%4 düştü","c":"%4 arttı","d":"%2 düştü"},"answer":"b","difficulty":"kolay","skill":"oran_orant"},
    {"id":"k2_m_2","text":"x + y = 10 ve x − y = 4 ise x kaçtır?","options":{"a":"5","b":"6","c":"7","d":"8"},"answer":"c","difficulty":"kolay","skill":"cebir"},
    {"id":"k2_m_3","text":"Bir sınıfın matematik ortalaması 72. 25 öğrenci varsa toplam puan kaçtır?","options":{"a":"1800","b":"1750","c":"1900","d":"1700"},"answer":"a","difficulty":"kolay","skill":"veri_yorumlama"},
    {"id":"k2_m_4","text":"Bir üçgenin iç açıları oranı 2:3:4. En büyük açı kaç derecedir?","options":{"a":"60°","b":"80°","c":"90°","d":"100°"},"answer":"b","difficulty":"kolay","skill":"geometri"},
    {"id":"k2_m_5","text":"3, 7, 15, 31, 63, … serisinde sonraki sayı?","options":{"a":"95","b":"127","c":"125","d":"126"},"answer":"b","difficulty":"kolay","skill":"hesaplama"},
    {"id":"k2_m_6","text":"Bir karenin köşegen uzunluğu 10√2 cm ise kenar uzunluğu kaç cm?","options":{"a":"5","b":"10","c":"15","d":"20"},"answer":"b","difficulty":"kolay","skill":"geometri"},
    {"id":"k2_m_7","text":"Bir sayının %150'si 75'tir. O sayı kaçtır?","options":{"a":"45","b":"50","c":"60","d":"112,5"},"answer":"b","difficulty":"kolay","skill":"oran_orant"},
    {"id":"k2_m_8","text":"2⁸ kaçtır?","options":{"a":"128","b":"256","c":"512","d":"64"},"answer":"b","difficulty":"kolay","skill":"hesaplama"},
    {"id":"k2_m_9","text":"Bir havuz A musluğuyla 6 saatte, B ile 3 saatte doluyor. İkisi birlikte kaç saatte doldurur?","options":{"a":"1","b":"2","c":"4,5","d":"3"},"answer":"b","difficulty":"orta","skill":"problem_cozme"},
    {"id":"k2_m_10","text":"Sınıf ortalaması 65. 5 öğrenci eklense ve her biri 85 alsa ortalama 70 olur. Sınıfta kaç öğrenci vardı?","options":{"a":"15","b":"20","c":"10","d":"25"},"answer":"a","difficulty":"orta","skill":"problem_cozme"},
    {"id":"k2_m_11","text":"500 TL yıllık %12 basit faizle 2 yıl yatırılırsa toplam kaç TL olur?","options":{"a":"560","b":"620","c":"600","d":"624"},"answer":"b","difficulty":"orta","skill":"oran_orant"},
    {"id":"k2_m_12","text":"Bir araç ilk 2 saatte 80 km/sa, sonraki 3 saatte 60 km/sa hızla gitti. Ortalama hızı?","options":{"a":"68","b":"70","c":"72","d":"66"},"answer":"a","difficulty":"orta","skill":"problem_cozme"},
    {"id":"k2_m_13","text":"Bir zarla 2 kez atıldığında toplamın 7 gelme olasılığı?","options":{"a":"1/6","b":"1/9","c":"5/36","d":"7/36"},"answer":"a","difficulty":"orta","skill":"olasilik"},
    {"id":"k2_m_14","text":"6 işçi bir duvarı 10 günde örüyor. 3 işçi kaç günde örer?","options":{"a":"15","b":"20","c":"5","d":"30"},"answer":"b","difficulty":"orta","skill":"oran_orant"},
    {"id":"k2_m_15","text":"Bir dairenin yarıçapı 7 cm ise çevresi yaklaşık kaç cm? (π≈22/7)","options":{"a":"44","b":"38","c":"22","d":"154"},"answer":"a","difficulty":"orta","skill":"geometri"},
    {"id":"k2_m_16","text":"Bir dikdörtgenler prizmasının boyutları 3×4×5 cm. Hacmi kaç cm³?","options":{"a":"12","b":"60","c":"47","d":"120"},"answer":"b","difficulty":"orta","skill":"geometri"},
    {"id":"k2_m_17","text":"Arabanın deposunda 45 litre benzin var. 100 km'de 8 litre harcıyorsa yaklaşık kaç km gidebilir?","options":{"a":"450","b":"360","c":"562","d":"400"},"answer":"c","difficulty":"zor","skill":"problem_cozme"},
    {"id":"k2_m_18","text":"Bir kutuda 5 kırmızı, 3 mavi top var. Art arda 2 top çekilirse (yerine konmadan) ikisinin de kırmızı olma olasılığı?","options":{"a":"5/14","b":"25/64","c":"5/8","d":"10/28"},"answer":"a","difficulty":"zor","skill":"olasilik"},
    {"id":"k2_m_19","text":"A ve B şehirleri arası 240 km. Bir araç A'dan 60 km/sa, diğeri B'den 80 km/sa ile aynı anda hareket ediyor. Kaç saat sonra buluşurlar?","options":{"a":"1,5 sa","b":"약 1,7 sa","c":"2 sa","d":"약 2,5 sa"},"answer":"b","difficulty":"zor","skill":"problem_cozme"},
    {"id":"k2_m_20","text":"f(x)=2x+3 ise f(f(2))=?","options":{"a":"17","b":"15","c":"13","d":"11"},"answer":"b","difficulty":"zor","skill":"cebir"},
]

K2_MANTIK = [
    {"id":"k2_l_1","text":"Demokrasi → Seçim, Diktatörlük → ?","options":{"a":"Özgürlük","b":"Baskı","c":"Parlamento","d":"Anayasa"},"answer":"b","difficulty":"kolay","skill":"analoji"},
    {"id":"k2_l_2","text":"Doktor → Stetoskop, Ressam → Fırça, Cerrah → ?","options":{"a":"İlaç","b":"Neşter","c":"Röntgen","d":"Mikroskop"},"answer":"b","difficulty":"kolay","skill":"analoji"},
    {"id":"k2_l_3","text":"1, 1, 2, 3, 5, 8, 13, … sonraki sayı?","options":{"a":"18","b":"20","c":"21","d":"26"},"answer":"c","difficulty":"kolay","skill":"seri"},
    {"id":"k2_l_4","text":"Tüm bilim insanları meraklıdır. Bazı öğretmenler bilim insanıdır. Hangisi kesinlikle doğru?","options":{"a":"Tüm öğretmenler meraklıdır","b":"Bazı öğretmenler meraklıdır","c":"Hiçbir öğretmen meraklı değildir","d":"Meraklı olan herkes bilim insanıdır"},"answer":"b","difficulty":"kolay","skill":"kiyas"},
    {"id":"k2_l_5","text":"64, 32, 16, 8, 4, … serideki tüm sayıların toplamı (sonsuz) neye yaklaşır?","options":{"a":"124","b":"128","c":"130","d":"Sonsuza gider"},"answer":"b","difficulty":"kolay","skill":"seri"},
    {"id":"k2_l_6","text":"Hangisi diğerlerinden farklıdır? Atom, Molekül, Hücre, Gezegen","options":{"a":"Atom","b":"Molekül","c":"Hücre","d":"Gezegen"},"answer":"d","difficulty":"kolay","skill":"analoji"},
    {"id":"k2_l_7","text":"A, B'den zengin. C, D'den fakir. B, D'den zengin. Kim en fakir?","options":{"a":"A","b":"B","c":"C","d":"D"},"answer":"c","difficulty":"orta","skill":"siralama"},
    {"id":"k2_l_8","text":"'Yağmur yağarsa yer ıslak olur.' Kontrapozitifi nedir?","options":{"a":"Yağmur yağmazsa yer ıslak olmaz","b":"Yer ıslak değilse yağmur yağmamıştır","c":"Yer ıslaksa yağmur yağmıştır","d":"Yağmur yağarsa yer kuru kalır"},"answer":"b","difficulty":"orta","skill":"mantiksal_cikarim"},
    {"id":"k2_l_9","text":"5 kişilik yarışta Ahmet Elif'ten önce. Burak sonuncu değil. Cemre Deniz'den sonra ama Burak'tan önce. Elif Deniz'den sonra. Deniz kaçıncı?","options":{"a":"1.","b":"2.","c":"3.","d":"4."},"answer":"b","difficulty":"orta","skill":"siralama"},
    {"id":"k2_l_10","text":"X, Y, Z üç farklı meslek yapıyor: Doktor, Avukat, Mühendis. X mühendis değil. Y doktor değil. Z ne doktor ne avukat. X'in mesleği?","options":{"a":"Doktor","b":"Avukat","c":"Mühendis","d":"Bilinemez"},"answer":"a","difficulty":"orta","skill":"mantiksal_cikarim"},
    {"id":"k2_l_11","text":"Bir yalancı her zaman yalan söyler, dürüst her zaman doğru söyler. Biri diyor: 'İkimiz de yalancıyız.' Bu kişi kim?","options":{"a":"Dürüst","b":"Yalancı","c":"İkisi de olabilir","d":"Hiçbiri olamaz"},"answer":"b","difficulty":"orta","skill":"mantiksal_cikarim"},
    {"id":"k2_l_12","text":"2, 5, 11, 23, 47, … sonraki sayı?","options":{"a":"91","b":"93","c":"94","d":"95"},"answer":"d","difficulty":"orta","skill":"seri"},
    {"id":"k2_l_13","text":"4 haneli şifre, her hane 0-9 farklı rakam, ilk hane 0 olamaz. Kaç farklı şifre oluşturulabilir?","options":{"a":"4536","b":"5040","c":"3024","d":"10000"},"answer":"a","difficulty":"zor","skill":"mantiksal_cikarim"},
    {"id":"k2_l_14","text":"Satranç tahtasında (8×8) iki köşegen üzerinde toplam kaç kare var?","options":{"a":"14","b":"15","c":"16","d":"8"},"answer":"b","difficulty":"zor","skill":"mantiksal_cikarim"},
    {"id":"k2_l_15","text":"Ada'da herkes ya şövalye (hep doğru söyler) ya haydut (hep yalan söyler). A: 'B şövalye.' B: 'A ve ben farklı türdeniz.' A ve B'nin türleri?","options":{"a":"İkisi de şövalye","b":"İkisi de haydut","c":"A şövalye, B haydut","d":"A haydut, B şövalye"},"answer":"b","difficulty":"zor","skill":"mantiksal_cikarim"},
]

K2_OZ_DEGER = [
    {"id":"k2_od_1","text":"Karmaşık bir konuyu anlayıncaya kadar farklı kaynaklardan araştırırım."},
    {"id":"k2_od_2","text":"Sınav öncesi etkili bir çalışma planı yapabilirim."},
    {"id":"k2_od_3","text":"Bir metni okuduktan sonra ana fikrini belirleyebilirim."},
    {"id":"k2_od_4","text":"Matematiksel problemlerde birden fazla çözüm yolu düşünebilirim."},
    {"id":"k2_od_5","text":"Eleştirel düşünerek bilgiyi sorgulayabilirim."},
    {"id":"k2_od_6","text":"Grup çalışmalarında fikirlerimi etkili şekilde ifade edebilirim."},
    {"id":"k2_od_7","text":"Uzun vadeli akademik hedeflerim var ve bunlar için çalışıyorum."},
    {"id":"k2_od_8","text":"Başarısız olduğumda nedenlerini analiz eder stratejimi değiştiririm."},
    {"id":"k2_od_9","text":"Farklı dersler arasında bağlantı kurabilirim."},
    {"id":"k2_od_10","text":"Not alarak ve özetleyerek çalışma verimliliğimi artırırım."},
    {"id":"k2_od_11","text":"Akademik konularda kendime güveniyorum."},
    {"id":"k2_od_12","text":"Öğrendiğim bilgiyi gerçek hayata uygulayabilirim."},
]


# ============================================================
# KADEME 3 — 9-10. SINIF (İLERİ)
# ============================================================
K3_OKUMA = [
    {"passage": "Bilişsel psikolojide 'çapa etkisi' olarak bilinen fenomen, karar verme süreçlerimizi şaşırtıcı biçimde etkiler. İlk karşılaştığımız bilgi — ne kadar alakasız olursa olsun — sonraki yargılarımız için bir referans noktası oluşturur. Örneğin bir deneyde katılımcılara rastgele bir sayı gösterilmiş, ardından BM'ye üye ülke sayısını tahmin etmeleri istenmiştir. Yüksek sayı görenlerin tahminleri, düşük sayı görenlerden sistematik olarak yüksek çıkmıştır. Bu etki pazarlamada, müzakerelerde ve hukuki kararlarda bile gözlemlenmektedir.",
     "questions": [
        {"id":"k3_oa_1","text":"Çapa etkisi nedir?","options":{"a":"İlk bilginin sonraki yargıları etkilemesi","b":"Gemilerin çapa atması","c":"Hafıza kaybı","d":"Motivasyon artışı"},"answer":"a","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k3_oa_2","text":"Deneyde katılımcılara ne gösterilmiş?","options":{"a":"Resimler","b":"Rastgele bir sayı","c":"Ülke bayrakları","d":"Bir harita"},"answer":"b","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k3_oa_3","text":"Çapa etkisi hangi alanlarda gözlemlenir?","options":{"a":"Sadece laboratuvarda","b":"Pazarlama, müzakere ve hukuk","c":"Sadece eğitimde","d":"Sadece psikoloji kliniğinde"},"answer":"b","difficulty":"orta","skill":"detay_bulma"},
        {"id":"k3_oa_4","text":"Yazarın amacı nedir?","options":{"a":"Okuyucuyu korkutmak","b":"Bilişsel bir önyargıyı bilimsel kanıtlarla açıklamak","c":"BM'yi tanıtmak","d":"Pazarlama teknikleri öğretmek"},"answer":"b","difficulty":"orta","skill":"yazar_tutumu"},
        {"id":"k3_oa_5","text":"Bu bilgi günlük hayatta nasıl kullanılabilir?","options":{"a":"Hiçbir işe yaramaz","b":"Müzakerelerde ilk teklifinizi stratejik belirleyerek karşı tarafı etkileyebilirsiniz","c":"Gemicilik yapılabilir","d":"Hafıza güçlendirilebilir"},"answer":"b","difficulty":"zor","skill":"cikarim"},
    ]},
    {"passage": "Antik Yunan'da demokrasinin doğuşu, tarihte bir dönüm noktasıdır. Atina'da MÖ 508'de Kleisthenes'in reformlarıyla vatandaşlara doğrudan yönetimde söz hakkı tanınmıştır. Ancak bu demokrasi bugünkü anlayıştan çok farklıydı: kadınlar, köleler ve yabancılar oy kullanamazdı. Nüfusun yalnızca yaklaşık %15'i 'vatandaş' sayılırdı. Yine de bu sistem, iktidarın halkla paylaşılması fikrinin ilk somut örneğiydi ve bugünkü demokratik sistemlerin temelini oluşturmuştur.",
     "questions": [
        {"id":"k3_oa_6","text":"Atina demokrasisi hangi tarihte başlamıştır?","options":{"a":"MÖ 508","b":"MÖ 350","c":"MS 508","d":"MÖ 1000"},"answer":"a","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k3_oa_7","text":"Atina'da kimler oy kullanamazdı?","options":{"a":"Erkekler","b":"Kadınlar, köleler ve yabancılar","c":"Tüm yetişkinler","d":"Sadece askerler"},"answer":"b","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k3_oa_8","text":"Nüfusun yüzde kaçı vatandaş sayılırdı?","options":{"a":"%50","b":"%30","c":"%15","d":"%75"},"answer":"c","difficulty":"orta","skill":"detay_bulma"},
        {"id":"k3_oa_9","text":"Yazar Atina demokrasisini nasıl değerlendiriyor?","options":{"a":"Tamamen olumsuz","b":"Eksik ama tarihi açıdan önemli","c":"Mükemmel bir sistem","d":"Günümüz için geçersiz"},"answer":"b","difficulty":"orta","skill":"yazar_tutumu"},
        {"id":"k3_oa_10","text":"'İktidarın halkla paylaşılması' ifadesinden ne anlaşılır?","options":{"a":"Herkesin eşit para alması","b":"Yönetim kararlarında halkın söz sahibi olması","c":"Kralın halkla yemek yemesi","d":"Ordunun sivil yönetime geçmesi"},"answer":"b","difficulty":"zor","skill":"soz_varligi"},
    ]},
    {"passage": "Kuantum mekaniğinin en şaşırtıcı ilkelerinden biri 'süperpozisyon'dur. Bir kuantum parçacığı, gözlemlenmediği sürece aynı anda birden fazla durumda bulunabilir. Schrödinger'in ünlü düşünce deneyinde bir kutu içindeki kedi, kutunun kapağı açılana kadar hem canlı hem ölü kabul edilir. Bu sezgiye aykırı ilke, kuantum bilgisayarların temelini oluşturur: klasik bilgisayarların 0 veya 1 kullandığı yerde, kuantum bilgisayarlar aynı anda hem 0 hem 1 olabilen 'kübit'leri kullanır.",
     "questions": [
        {"id":"k3_oa_11","text":"Süperpozisyon ne demektir?","options":{"a":"Bir nesnenin yok olması","b":"Bir parçacığın aynı anda birden fazla durumda olabilmesi","c":"Işığın kırılması","d":"Atomun bölünmesi"},"answer":"b","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k3_oa_12","text":"Schrödinger deneyinde kedi ne zaman 'canlı veya ölü' belirlenir?","options":{"a":"Kutu kapatıldığında","b":"Kutu açıldığında (gözlemlendiğinde)","c":"Hiçbir zaman","d":"Deney başladığında"},"answer":"b","difficulty":"orta","skill":"cikarim"},
        {"id":"k3_oa_13","text":"Klasik bilgisayar ile kuantum bilgisayarın farkı nedir?","options":{"a":"Klasik daha hızlıdır","b":"Kuantum aynı anda 0 ve 1 olabilen kübitleri kullanır","c":"İkisi aynıdır","d":"Klasik kübit kullanır"},"answer":"b","difficulty":"orta","skill":"karsilastirma"},
        {"id":"k3_oa_14","text":"'Sezgiye aykırı' ifadesi neden kullanılmıştır?","options":{"a":"Çünkü günlük deneyimimizle çelişen bir durumdur","b":"Çünkü kolaydır","c":"Çünkü herkes anlayabilir","d":"Çünkü yanlıştır"},"answer":"a","difficulty":"orta","skill":"soz_varligi"},
        {"id":"k3_oa_15","text":"Bu metin hangi varsayımı sorgular?","options":{"a":"Bir nesne aynı anda sadece bir durumda olabilir","b":"Kediler ölümsüzdür","c":"Bilgisayarlar düşünebilir","d":"Fizik kuralları değişmezdir"},"answer":"a","difficulty":"zor","skill":"cikarim"},
    ]},
    {"passage": "Dünya genelinde antibiyotik direnci, 21. yüzyılın en ciddi sağlık tehditleri arasında gösterilmektedir. Bakterilerin antibiyotiklere karşı direnç geliştirmesi doğal bir evrimsel süreçtir; ancak gereksiz ve yanlış antibiyotik kullanımı bu süreci dramatik biçimde hızlandırmaktadır. Dünya Sağlık Örgütü, her yıl yaklaşık 700 bin kişinin dirençli enfeksiyonlardan hayatını kaybettiğini ve 2050'ye kadar bu sayının 10 milyona ulaşabileceğini tahmin etmektedir. Çözüm; yeni antibiyotik geliştirmenin yanı sıra mevcut antibiyotiklerin akılcı kullanımını sağlamaktır.",
     "questions": [
        {"id":"k3_oa_16","text":"Her yıl dirençli enfeksiyonlardan kaç kişi hayatını kaybediyor?","options":{"a":"70 bin","b":"700 bin","c":"7 milyon","d":"70 milyon"},"answer":"b","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k3_oa_17","text":"Antibiyotik direncini ne hızlandırır?","options":{"a":"Temiz su kullanımı","b":"Gereksiz ve yanlış antibiyotik kullanımı","c":"Egzersiz","d":"Aşılama"},"answer":"b","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k3_oa_18","text":"2050 tahmini ne?","options":{"a":"Antibiyotik direnci bitecek","b":"Yılda 10 milyon ölüm","c":"Yeni hastalıklar çıkacak","d":"Tüm bakteriler yok olacak"},"answer":"b","difficulty":"orta","skill":"detay_bulma"},
        {"id":"k3_oa_19","text":"Metne göre çözüm nedir?","options":{"a":"Antibiyotik kullanmayı bırakmak","b":"Yeni antibiyotik geliştirme + akılcı kullanım","c":"Sadece yeni ilaçlar","d":"Hiçbir şey yapılamaz"},"answer":"b","difficulty":"orta","skill":"ana_fikir"},
        {"id":"k3_oa_20","text":"'Doğal bir evrimsel süreç' ifadesi niçin önemlidir?","options":{"a":"Direncin tamamen engellenemeyeceğini ama yavaşlatılabileceğini ima eder","b":"Direncin iyi bir şey olduğunu söyler","c":"İnsanların suçsuz olduğunu söyler","d":"Evrimin yanlış olduğunu söyler"},"answer":"a","difficulty":"zor","skill":"cikarim"},
    ]},
]

K3_MATEMATIK = [
    {"id":"k3_m_1","text":"f(x) = 3x − 7 ise f(5) kaçtır?","options":{"a":"8","b":"22","c":"15","d":"2"},"answer":"a","difficulty":"kolay","skill":"cebir"},
    {"id":"k3_m_2","text":"log₁₀(1000) kaçtır?","options":{"a":"2","b":"3","c":"4","d":"10"},"answer":"b","difficulty":"kolay","skill":"cebir"},
    {"id":"k3_m_3","text":"2¹⁰ kaçtır?","options":{"a":"512","b":"1024","c":"2048","d":"256"},"answer":"b","difficulty":"kolay","skill":"hesaplama"},
    {"id":"k3_m_4","text":"x² − 9 = 0 denkleminin kökleri?","options":{"a":"±3","b":"±9","c":"3","d":"9"},"answer":"a","difficulty":"kolay","skill":"cebir"},
    {"id":"k3_m_5","text":"Bir eşkenar üçgenin kenarı 10 cm, alanı yaklaşık kaç cm²? (√3≈1,73)","options":{"a":"43,3","b":"50","c":"25","d":"86,6"},"answer":"a","difficulty":"kolay","skill":"geometri"},
    {"id":"k3_m_6","text":"sin(30°) kaçtır?","options":{"a":"1/2","b":"√2/2","c":"√3/2","d":"1"},"answer":"a","difficulty":"kolay","skill":"geometri"},
    {"id":"k3_m_7","text":"Bir veri setinde medyan nedir? Veri: 3, 7, 8, 12, 15","options":{"a":"7","b":"8","c":"9","d":"12"},"answer":"b","difficulty":"kolay","skill":"veri_yorumlama"},
    {"id":"k3_m_8","text":"5! (5 faktöriyel) kaçtır?","options":{"a":"25","b":"120","c":"60","d":"20"},"answer":"b","difficulty":"kolay","skill":"hesaplama"},
    {"id":"k3_m_9","text":"f(x) = x² − 4x + 3 fonksiyonunun kökleri?","options":{"a":"1 ve 3","b":"2 ve 3","c":"-1 ve -3","d":"0 ve 4"},"answer":"a","difficulty":"orta","skill":"cebir"},
    {"id":"k3_m_10","text":"Bir silindirin yarıçapı 3 cm, yüksekliği 10 cm. Hacmi? (π≈3,14)","options":{"a":"282,6","b":"94,2","c":"188,4","d":"314"},"answer":"a","difficulty":"orta","skill":"geometri"},
    {"id":"k3_m_11","text":"10.000 TL yıllık %8 bileşik faizle 2 yıl yatırılırsa toplam?","options":{"a":"11.600","b":"11.664","c":"11.800","d":"12.000"},"answer":"b","difficulty":"orta","skill":"oran_orant"},
    {"id":"k3_m_12","text":"Bir sınıftan rastgele seçilen öğrencinin erkek VEYA gözlüklü olma olasılığı: 20 erkek (5 gözlüklü), 10 kız (3 gözlüklü). Toplam 30.","options":{"a":"23/30","b":"25/30","c":"20/30","d":"28/30"},"answer":"a","difficulty":"orta","skill":"olasilik"},
    {"id":"k3_m_13","text":"3x + 2y = 12 ve x − y = 1 denklem sisteminin çözümü?","options":{"a":"x=2, y=3","b":"x=2, y=1","c":"x=14/5, y=9/5","d":"x=3, y=2"},"answer":"c","difficulty":"orta","skill":"cebir"},
    {"id":"k3_m_14","text":"Bir fonksiyonun grafiği x=2'de y eksenini kesiyor. f(x) = ax + b, f(0)=4, f(2)=0 ise a=?","options":{"a":"-2","b":"2","c":"-1","d":"1"},"answer":"a","difficulty":"orta","skill":"cebir"},
    {"id":"k3_m_15","text":"8 kişilik bir gruptan 3 kişilik bir komite kaç farklı şekilde oluşturulabilir?","options":{"a":"24","b":"56","c":"336","d":"40320"},"answer":"b","difficulty":"orta","skill":"olasilik"},
    {"id":"k3_m_16","text":"İki zar atıldığında toplamın 8 veya üzeri olma olasılığı?","options":{"a":"5/12","b":"15/36","c":"5/36","d":"21/36"},"answer":"b","difficulty":"orta","skill":"olasilik"},
    {"id":"k3_m_17","text":"f(x) = x³ − 3x² + 2 fonksiyonunun x=1'deki türevi?","options":{"a":"-3","b":"0","c":"-1","d":"3"},"answer":"a","difficulty":"zor","skill":"cebir"},
    {"id":"k3_m_18","text":"Bir üçgenin köşeleri A(0,0), B(6,0), C(3,4). Alanı?","options":{"a":"12","b":"24","c":"8","d":"16"},"answer":"a","difficulty":"zor","skill":"geometri"},
    {"id":"k3_m_19","text":"lim(x→0) sin(x)/x = ?","options":{"a":"0","b":"1","c":"∞","d":"Tanımsız"},"answer":"b","difficulty":"zor","skill":"cebir"},
    {"id":"k3_m_20","text":"Bir havuzun hacmi 12.000 litre. A borusu saatte 500 litre dolduruyor, B borusu saatte 200 litre boşaltıyor. İkisi birlikte açıkken havuz kaç saatte dolar?","options":{"a":"24","b":"40","c":"30","d":"60"},"answer":"b","difficulty":"zor","skill":"problem_cozme"},
]

K3_MANTIK = [
    {"id":"k3_l_1","text":"Sebep → Sonuç, Hipotez → ?","options":{"a":"Deney","b":"Teori","c":"Kanıt","d":"Test"},"answer":"d","difficulty":"kolay","skill":"analoji"},
    {"id":"k3_l_2","text":"1, 4, 9, 16, 25, … sonraki sayı?","options":{"a":"30","b":"35","c":"36","d":"49"},"answer":"c","difficulty":"kolay","skill":"seri"},
    {"id":"k3_l_3","text":"'Tüm metaller iletkendir' ve 'Bakır bir metaldir' önermelerinden ne çıkar?","options":{"a":"Bakır iletken değildir","b":"Bakır iletkendir","c":"Bazı metaller iletken değildir","d":"Bilinemez"},"answer":"b","difficulty":"kolay","skill":"kiyas"},
    {"id":"k3_l_4","text":"Evrim → Darwin, Görelilik → ?","options":{"a":"Newton","b":"Einstein","c":"Hawking","d":"Curie"},"answer":"b","difficulty":"kolay","skill":"analoji"},
    {"id":"k3_l_5","text":"Hangi sayı diğerlerinden farklı mantıkla oluşmuştur? 2, 3, 5, 7, 9, 11","options":{"a":"3","b":"7","c":"9","d":"11"},"answer":"c","difficulty":"kolay","skill":"seri"},
    {"id":"k3_l_6","text":"p: 'Hava yağmurlu' q: 'Yere ıslak' ise p→q'nun değili?","options":{"a":"Hava yağmurlu VE yer ıslak değil","b":"Hava yağmurlu değil VE yer ıslak","c":"Hava yağmurlu değil VEYA yer ıslak","d":"Hava yağmurlu VEYA yer ıslak değil"},"answer":"a","difficulty":"kolay","skill":"mantiksal_cikarim"},
    {"id":"k3_l_7","text":"A, B, C, D, E beş arkadaş. A, C'den uzun. B, E'den kısa. D en uzun. C, B'den uzun. En kısa kim?","options":{"a":"A","b":"B","c":"C","d":"E"},"answer":"d","difficulty":"orta","skill":"siralama"},
    {"id":"k3_l_8","text":"'Bazı öğrenciler sporcu. Tüm sporcular sağlıklı.' Hangisi kesin doğru?","options":{"a":"Tüm öğrenciler sağlıklı","b":"Bazı öğrenciler sağlıklı","c":"Hiçbir öğrenci sağlıklı değil","d":"Tüm sağlıklılar sporcu"},"answer":"b","difficulty":"orta","skill":"kiyas"},
    {"id":"k3_l_9","text":"3, 6, 11, 18, 27, … sonraki?","options":{"a":"36","b":"38","c":"40","d":"35"},"answer":"b","difficulty":"orta","skill":"seri"},
    {"id":"k3_l_10","text":"Bir algoritma: x ile başla, 2 ile çarp, 3 çıkar. x=4 için 3 kez uygulanırsa sonuç?","options":{"a":"25","b":"29","c":"31","d":"35"},"answer":"c","difficulty":"orta","skill":"mantiksal_cikarim"},
    {"id":"k3_l_11","text":"5 farklı renk bayrak var. 3 tanesi bir direğe sırayla asılacak. Kaç farklı düzenleme mümkün?","options":{"a":"60","b":"10","c":"15","d":"125"},"answer":"a","difficulty":"orta","skill":"mantiksal_cikarim"},
    {"id":"k3_l_12","text":"'p VE q' doğruysa, 'p VEYA q' doğru mudur?","options":{"a":"Evet, her zaman","b":"Hayır, hiçbir zaman","c":"Bazen","d":"Bilgi yetersiz"},"answer":"a","difficulty":"orta","skill":"mantiksal_cikarim"},
    {"id":"k3_l_13","text":"Bir adada 3 kabile var: hep doğru söyleyen, hep yalan söyleyen ve rastgele söyleyen. A: 'Ben rastgele değilim.' B: 'A doğru söylüyor.' B'nin kabilesi ne olamaz?","options":{"a":"Doğrucu","b":"Yalancı","c":"Rastgele","d":"Hiçbiri"},"answer":"c","difficulty":"zor","skill":"mantiksal_cikarim"},
    {"id":"k3_l_14","text":"n² + n her zaman çift midir? (n doğal sayı)","options":{"a":"Evet — çünkü n(n+1) ardışık iki sayının çarpımıdır","b":"Hayır — n=3 için tek","c":"Sadece çift n'ler için","d":"Bilinemez"},"answer":"a","difficulty":"zor","skill":"mantiksal_cikarim"},
    {"id":"k3_l_15","text":"100 kapı var, hepsi kapalı. 1. turda tüm kapılar açılıyor. 2. turda her 2. kapı değiştiriliyor. 3. turda her 3. kapı... 100. tura kadar devam. Son durumda kaç kapı açık?","options":{"a":"10","b":"50","c":"25","d":"12"},"answer":"a","difficulty":"zor","skill":"mantiksal_cikarim"},
]

K3_OZ_DEGER = [
    {"id":"k3_od_1","text":"Bir konuyu derinlemesine araştırıp farklı bakış açılarını değerlendirebilirim."},
    {"id":"k3_od_2","text":"Sınav ve proje takvimimi etkin biçimde yönetebilirim."},
    {"id":"k3_od_3","text":"Okuduğum akademik metinleri eleştirel olarak değerlendirebilirim."},
    {"id":"k3_od_4","text":"Soyut matematiksel kavramları anlayıp uygulayabilirim."},
    {"id":"k3_od_5","text":"Bir argümanın güçlü ve zayıf yönlerini tespit edebilirim."},
    {"id":"k3_od_6","text":"Sunum yaparak fikirlerimi etkili biçimde aktarabilirim."},
    {"id":"k3_od_7","text":"Kariyer hedeflerim doğrultusunda bilinçli akademik tercihler yapıyorum."},
    {"id":"k3_od_8","text":"Hatalarımdan sistematik olarak ders çıkarırım."},
    {"id":"k3_od_9","text":"Farklı disiplinlerin kesişim noktalarını görebilirim."},
    {"id":"k3_od_10","text":"Kendi öğrenme stratejilerimi değerlendirip geliştirebilirim."},
    {"id":"k3_od_11","text":"Zorlu akademik görevlerin üstesinden gelebileceğime inanırım."},
    {"id":"k3_od_12","text":"Teorik bilgiyi pratiğe dönüştürebilirim."},
]


# ============================================================
# KADEME 4 — 11-12. SINIF (ÜST / YKS)
# ============================================================
K4_OKUMA = [
    {"passage": "Postmodern felsefede 'büyük anlatılar'ın sonu tezini ileri süren Jean-François Lyotard, Aydınlanma'nın evrensel ilerleme vaadinin artık geçerliliğini yitirdiğini savunmuştur. Lyotard'a göre bilginin meşrulaştırılması artık tek bir üst-anlatıya değil, yerel ve bağlamsal 'küçük anlatılar'a dayanmaktadır. Bu görüş, bilimin nesnel hakikat iddialarını da sorgulamış ve bilginin toplumsal iktidar yapılarıyla iç içe olduğunu vurgulamıştır. Eleştirmenler ise bu yaklaşımın nihilizme ve göreciliğe kapı araladığını öne sürmüştür.",
     "questions": [
        {"id":"k4_oa_1","text":"Lyotard'ın temel tezi nedir?","options":{"a":"Bilim her zaman doğrudur","b":"Büyük anlatılar artık geçerli değildir","c":"Aydınlanma mükemmeldir","d":"Bilgi iktidardan bağımsızdır"},"answer":"b","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k4_oa_2","text":"'Küçük anlatılar' ne anlama gelir?","options":{"a":"Kısa hikâyeler","b":"Yerel ve bağlamsal bilgi meşrulaştırma biçimleri","c":"Çocuk masalları","d":"Bilimsel makaleler"},"answer":"b","difficulty":"orta","skill":"soz_varligi"},
        {"id":"k4_oa_3","text":"Eleştirmenler ne söylüyor?","options":{"a":"Lyotard haklı","b":"Bu yaklaşım nihilizme kapı aralar","c":"Büyük anlatılar doğrudur","d":"Bilgi iktidarla ilgisizdir"},"answer":"b","difficulty":"orta","skill":"detay_bulma"},
        {"id":"k4_oa_4","text":"Metin hangi varsayımı sorgular?","options":{"a":"Evrensel ve nesnel hakikatin varlığı","b":"Yerçekiminin varlığı","c":"Dünyanın yuvarlak olması","d":"Suyun akışkanlığı"},"answer":"a","difficulty":"orta","skill":"cikarim"},
        {"id":"k4_oa_5","text":"Bu tartışmanın bilim etiği açısından sonucu ne olabilir?","options":{"a":"Bilime güvenmemek gerekir","b":"Bilimsel iddiaların sosyal bağlamını da değerlendirmek gerekir","c":"Bilim tamamen nesnel kabul edilmelidir","d":"Felsefe bilimden daha önemlidir"},"answer":"b","difficulty":"zor","skill":"cikarim"},
    ]},
    {"passage": "Epigenetik, DNA dizisinde değişiklik olmaksızın gen ifadesinin değişmesini inceleyen bilim dalıdır. Çevresel faktörler — beslenme, stres, toksinler — genlerin 'açılıp kapanmasını' etkileyebilir. Daha da çarpıcı olanı, bazı epigenetik değişikliklerin nesilden nesile aktarılabilmesidir. Hollanda'daki 1944 kıtlığını yaşayan annelerin çocuklarında ve hatta torunlarında metabolik hastalık riskinin artmış olması bu durumun en bilinen örneğidir. Bu alan, 'doğa mı yetiştirme mi' tartışmasını temelden dönüştürmektedir.",
     "questions": [
        {"id":"k4_oa_6","text":"Epigenetik neyi inceler?","options":{"a":"DNA dizisindeki mutasyonları","b":"DNA değişmeden gen ifadesinin değişmesini","c":"Proteinlerin yapısını","d":"Hücre bölünmesini"},"answer":"b","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k4_oa_7","text":"Hollanda kıtlığı örneği neyi kanıtlar?","options":{"a":"Kıtlığın acı olduğunu","b":"Epigenetik değişikliklerin nesiller arası aktarılabildiğini","c":"DNA'nın değişmez olduğunu","d":"Beslenmenin önemsiz olduğunu"},"answer":"b","difficulty":"orta","skill":"cikarim"},
        {"id":"k4_oa_8","text":"'Doğa mı yetiştirme mi' tartışması nasıl dönüşüyor?","options":{"a":"Doğa kesin kazandı","b":"Yetiştirme kesin kazandı","c":"İkisi birbirini etkiliyor — çevre genleri açıp kapatabiliyor","d":"Tartışma sona erdi"},"answer":"c","difficulty":"orta","skill":"cikarim"},
        {"id":"k4_oa_9","text":"Metinde hangi bilimsel paradigma değişikliği ima ediliyor?","options":{"a":"Genetik determinizmin zayıflaması","b":"Evrimin reddi","c":"DNA'nın keşfi","d":"Mendel genetiğinin doğrulanması"},"answer":"a","difficulty":"zor","skill":"cikarim"},
        {"id":"k4_oa_10","text":"Bu bilginin halk sağlığı politikası açısından sonucu ne olabilir?","options":{"a":"Genetik testler yasaklanmalı","b":"Toplum sağlığı müdahaleleri gelecek nesilleri de etkileyebilir","c":"Beslenmenin önemi yoktur","d":"Sadece bireysel tedaviye odaklanılmalı"},"answer":"b","difficulty":"zor","skill":"cikarim"},
    ]},
    {"passage": "Yapay genel zekâ (AGI), insan düzeyinde veya üzerinde bilişsel yeteneklere sahip yapay bir sistemdir. Günümüzdeki 'dar yapay zekâ' sistemleri tek bir göreve odaklanırken, AGI teorik olarak herhangi bir entelektüel görevi insanlar kadar iyi yapabilecektir. Bazı araştırmacılar AGI'nin 2040'lara kadar mümkün olabileceğini öngörürken, diğerleri bunun yüzyıllar sürebileceğini ya da hiç gerçekleşmeyebileceğini savunmaktadır. Tartışmanın merkezinde bilinç, niyetlilik ve 'anlama'nın ne olduğu soruları yer almaktadır.",
     "questions": [
        {"id":"k4_oa_11","text":"AGI ile dar yapay zekâ arasındaki fark nedir?","options":{"a":"AGI daha yavaştır","b":"Dar YZ tek görev, AGI herhangi bir entelektüel görev","c":"Fark yoktur","d":"AGI yazılım değildir"},"answer":"b","difficulty":"kolay","skill":"karsilastirma"},
        {"id":"k4_oa_12","text":"AGI'nin zamanlaması konusunda uzmanlar ne düşünüyor?","options":{"a":"Hepsi 2040 diyor","b":"Hepsi imkânsız diyor","c":"Görüşler çok farklı — 2040'lardan asla'ya kadar","d":"Hepsi 2025 diyor"},"answer":"c","difficulty":"orta","skill":"detay_bulma"},
        {"id":"k4_oa_13","text":"Tartışmanın merkezinde hangi felsefi sorular var?","options":{"a":"Maliyet ve verimlilik","b":"Bilinç, niyetlilik ve anlama","c":"Programlama dili","d":"Donanım kapasitesi"},"answer":"b","difficulty":"orta","skill":"detay_bulma"},
        {"id":"k4_oa_14","text":"Bu metinden çıkarılacak epistemolojik soru nedir?","options":{"a":"Bilgisayar ne kadar hızlı olabilir","b":"'Anlama' ve 'hesaplama' aynı şey midir","c":"Yapay zekâ ucuz mudur","d":"İnternet hızı yeterli midir"},"answer":"b","difficulty":"zor","skill":"cikarim"},
        {"id":"k4_oa_15","text":"Metinde ima edilen en derin paradoks nedir?","options":{"a":"AGI'yi tanımlamak için kullandığımız kavramları (bilinç, anlama) kendimiz bile tam tanımlayamıyoruz","b":"Bilgisayarlar pahalıdır","c":"Yapay zekâ tehlikelidir","d":"İnsanlar zekidir"},"answer":"a","difficulty":"zor","skill":"cikarim"},
    ]},
    {"passage": "Oyun teorisinin en ünlü modeli 'Mahkûmun İkilemi'dir. İki şüpheli ayrı ayrı sorgulanır; her biri diğerini suçlayabilir (ihanet) veya sessiz kalabilir (işbirliği). Eğer ikisi de sessiz kalırsa hafif ceza alır. Biri suçlar diğeri kalırsa suçlayan serbest, diğeri ağır ceza alır. İkisi de suçlarsa ikisi de orta ceza alır. Bireysel rasyonalite ihaneti, kolektif rasyonalite işbirliğini tercih ettirir. Bu model, silahlanma yarışından iklim değişikliğine kadar pek çok gerçek dünya durumunu açıklar.",
     "questions": [
        {"id":"k4_oa_16","text":"Mahkûmun İkileminde en iyi kolektif sonuç nedir?","options":{"a":"İkisi de suçlar","b":"İkisi de sessiz kalır (işbirliği)","c":"Biri suçlar","d":"Hiçbiri sorgulanmaz"},"answer":"b","difficulty":"kolay","skill":"detay_bulma"},
        {"id":"k4_oa_17","text":"Bireysel rasyonalite neden ihaneti tercih ettirir?","options":{"a":"İhanet her durumda daha az ceza getirir","b":"İhanet daha ahlâklıdır","c":"Diğerinin ne yapacağından emin olamama","d":"Sessiz kalmak yasadışıdır"},"answer":"c","difficulty":"orta","skill":"cikarim"},
        {"id":"k4_oa_18","text":"Bu model iklim değişikliğini nasıl açıklar?","options":{"a":"Her ülke emisyon azaltmalı ama bireysel olarak azaltmama teşviki var","b":"İklim değişikliği yoktur","c":"Sadece büyük ülkeleri ilgilendirir","d":"Doğal bir süreçtir"},"answer":"a","difficulty":"orta","skill":"cikarim"},
        {"id":"k4_oa_19","text":"'Bireysel rasyonalite ile kolektif rasyonalite çatışır' ifadesi ne anlama gelir?","options":{"a":"Herkes kendi çıkarını düşünürse toplum zarar görür","b":"Toplum bireylerin düşmanıdır","c":"Bireyler düşünemez","d":"Kolektif karar her zaman yanlıştır"},"answer":"a","difficulty":"zor","skill":"soz_varligi"},
        {"id":"k4_oa_20","text":"Mahkûmun İkileminden çıkmanın yolu ne olabilir?","options":{"a":"Daha sert cezalar","b":"Tekrarlanan etkileşimler, güven ve itibar mekanizmaları","c":"Sorgulamayı yasaklamak","d":"Oyun teorisini bilmemek"},"answer":"b","difficulty":"zor","skill":"cikarim"},
    ]},
]

K4_MATEMATIK = [
    {"id":"k4_m_1","text":"∫(2x)dx = ?","options":{"a":"x² + C","b":"2x² + C","c":"x + C","d":"2 + C"},"answer":"a","difficulty":"kolay","skill":"cebir"},
    {"id":"k4_m_2","text":"f(x) = x³ fonksiyonunun türevi f'(x) = ?","options":{"a":"x²","b":"3x²","c":"3x","d":"x³"},"answer":"b","difficulty":"kolay","skill":"cebir"},
    {"id":"k4_m_3","text":"Matris A = [[1,2],[3,4]]. det(A) = ?","options":{"a":"2","b":"-2","c":"10","d":"-10"},"answer":"b","difficulty":"kolay","skill":"cebir"},
    {"id":"k4_m_4","text":"lim(x→∞) (3x²+1)/(x²+5) = ?","options":{"a":"3","b":"1","c":"0","d":"∞"},"answer":"a","difficulty":"kolay","skill":"cebir"},
    {"id":"k4_m_5","text":"10.000 TL %10 bileşik faizle 3 yıl: toplam?","options":{"a":"13.000","b":"13.310","c":"13.100","d":"13.331"},"answer":"d","difficulty":"kolay","skill":"hesaplama"},
    {"id":"k4_m_6","text":"C(10,3) = ?","options":{"a":"120","b":"720","c":"30","d":"1000"},"answer":"a","difficulty":"kolay","skill":"olasilik"},
    {"id":"k4_m_7","text":"cos(60°) = ?","options":{"a":"1/2","b":"√2/2","c":"√3/2","d":"0"},"answer":"a","difficulty":"kolay","skill":"geometri"},
    {"id":"k4_m_8","text":"log₂(32) = ?","options":{"a":"4","b":"5","c":"6","d":"3"},"answer":"b","difficulty":"kolay","skill":"cebir"},
    {"id":"k4_m_9","text":"f(x) = e²ˣ fonksiyonunun türevi?","options":{"a":"e²ˣ","b":"2e²ˣ","c":"2xe²ˣ","d":"e²"},"answer":"b","difficulty":"orta","skill":"cebir"},
    {"id":"k4_m_10","text":"∫₀² (3x²)dx = ?","options":{"a":"8","b":"12","c":"6","d":"24"},"answer":"a","difficulty":"orta","skill":"cebir"},
    {"id":"k4_m_11","text":"Normal dağılımda ortalamanın 1 standart sapma içinde kalan oran yaklaşık?","options":{"a":"%50","b":"%68","c":"%95","d":"%99"},"answer":"b","difficulty":"orta","skill":"veri_yorumlama"},
    {"id":"k4_m_12","text":"3×3 birim matrisin determinantı?","options":{"a":"0","b":"1","c":"3","d":"9"},"answer":"b","difficulty":"orta","skill":"cebir"},
    {"id":"k4_m_13","text":"Bir para 5 kez atılıyor. En az 4 tura gelme olasılığı?","options":{"a":"6/32","b":"5/32","c":"1/32","d":"10/32"},"answer":"a","difficulty":"orta","skill":"olasilik"},
    {"id":"k4_m_14","text":"y = x² + 2x − 3 parabolünün tepe noktası?","options":{"a":"(-1, -4)","b":"(1, 0)","c":"(-1, 4)","d":"(2, 5)"},"answer":"a","difficulty":"orta","skill":"cebir"},
    {"id":"k4_m_15","text":"Bir kürenin yarıçapı 6 cm. Hacmi? (π≈3,14)","options":{"a":"904,3","b":"452,2","c":"226,1","d":"1808,6"},"answer":"a","difficulty":"orta","skill":"geometri"},
    {"id":"k4_m_16","text":"Σ(k=1→n) k = n(n+1)/2. Σ(k=1→100) k = ?","options":{"a":"5000","b":"5050","c":"10000","d":"10100"},"answer":"b","difficulty":"orta","skill":"hesaplama"},
    {"id":"k4_m_17","text":"f(x,y) = x²y + xy². ∂f/∂x = ?","options":{"a":"2xy + y²","b":"x² + 2xy","c":"2x + y","d":"x + 2y"},"answer":"a","difficulty":"zor","skill":"cebir"},
    {"id":"k4_m_18","text":"∫₀¹ eˣ dx = ?","options":{"a":"e","b":"e-1","c":"1","d":"e+1"},"answer":"b","difficulty":"zor","skill":"cebir"},
    {"id":"k4_m_19","text":"Bayes teoremi: P(A)=0.01, P(B|A)=0.9, P(B|¬A)=0.05. P(A|B)≈?","options":{"a":"0.15","b":"0.08","c":"0.90","d":"0.50"},"answer":"a","difficulty":"zor","skill":"olasilik"},
    {"id":"k4_m_20","text":"n elemanlı bir kümenin alt küme sayısı 2ⁿ. 5 elemanlı kümenin boş olmayan alt küme sayısı?","options":{"a":"31","b":"32","c":"16","d":"63"},"answer":"a","difficulty":"zor","skill":"olasilik"},
]

K4_MANTIK = [
    {"id":"k4_l_1","text":"Korelasyon → İlişki, Nedensellik → ?","options":{"a":"Gözlem","b":"Sebep-sonuç","c":"İstatistik","d":"Rastlantı"},"answer":"b","difficulty":"kolay","skill":"analoji"},
    {"id":"k4_l_2","text":"p → q doğru. q → r doğru. Hangisi kesinlikle doğru?","options":{"a":"r → p","b":"p → r","c":"¬p → ¬r","d":"¬r → q"},"answer":"b","difficulty":"kolay","skill":"mantiksal_cikarim"},
    {"id":"k4_l_3","text":"1, 2, 6, 24, 120, … sonraki sayı?","options":{"a":"240","b":"600","c":"720","d":"480"},"answer":"c","difficulty":"kolay","skill":"seri"},
    {"id":"k4_l_4","text":"Tümevarım → Özelden genele, Tümdengelim → ?","options":{"a":"Genelden özele","b":"Özelden özele","c":"Genelden genele","d":"Sezgiden bilgiye"},"answer":"a","difficulty":"kolay","skill":"analoji"},
    {"id":"k4_l_5","text":"'p VEYA q' doğru ve 'p' yanlış ise?","options":{"a":"q doğru","b":"q yanlış","c":"Bilinemez","d":"İkisi de yanlış"},"answer":"a","difficulty":"kolay","skill":"mantiksal_cikarim"},
    {"id":"k4_l_6","text":"0, 1, 1, 2, 3, 5, 8, 13, 21, 34, … Bu dizide 12. terim?","options":{"a":"89","b":"144","c":"55","d":"233"},"answer":"a","difficulty":"kolay","skill":"seri"},
    {"id":"k4_l_7","text":"Bir argümanda 'Ad hominem' hatası nedir?","options":{"a":"Argümanı değil kişiyi hedef almak","b":"Yanlış genelleme","c":"Döngüsel akıl yürütme","d":"Kaygan zemin"},"answer":"a","difficulty":"orta","skill":"mantiksal_cikarim"},
    {"id":"k4_l_8","text":"Russell Paradoksu: 'Kendini içermeyen tüm kümelerin kümesi kendini içerir mi?'","options":{"a":"Evet","b":"Hayır","c":"Hem evet hem hayır — paradoks","d":"Soru anlamsız"},"answer":"c","difficulty":"orta","skill":"mantiksal_cikarim"},
    {"id":"k4_l_9","text":"A, B, C, D, E beş kişi yuvarlak masada oturuyor. A, B'nin yanında değil. C, D ile E arasında. B, E'nin solunda. Kaç farklı oturma düzeni mümkün?","options":{"a":"2","b":"4","c":"6","d":"8"},"answer":"a","difficulty":"orta","skill":"siralama"},
    {"id":"k4_l_10","text":"'Korelasyon nedensellik değildir' ilkesi ne anlama gelir?","options":{"a":"İki şey birlikte değişebilir ama biri diğerine neden olmayabilir","b":"İstatistik yanlıştır","c":"Bilim güvenilmezdir","d":"Her korelasyon rastlantıdır"},"answer":"a","difficulty":"orta","skill":"mantiksal_cikarim"},
    {"id":"k4_l_11","text":"Gödel'in eksiklik teoremi neyi söyler?","options":{"a":"Matematik tutarsızdır","b":"Yeterince güçlü her formel sistemde kanıtlanamayan doğru önermeler vardır","c":"Her önerme kanıtlanabilir","d":"Mantık gereksizdir"},"answer":"b","difficulty":"orta","skill":"mantiksal_cikarim"},
    {"id":"k4_l_12","text":"Bir otomat kuralı: girdi 0 ise sola git, 1 ise sağa git, başlangıç ortada. Girdi: 0,1,1,0,0,1. Son konum başlangıca göre nerede?","options":{"a":"1 sola","b":"Başlangıçta","c":"1 sağa","d":"2 sola"},"answer":"a","difficulty":"orta","skill":"mantiksal_cikarim"},
    {"id":"k4_l_13","text":"Theseus'un Gemisi: Bir geminin tüm parçaları yavaşça değiştirilirse aynı gemi midir? Bu hangi felsefi problemi ortaya koyar?","options":{"a":"Kimlik ve süreklilik problemi","b":"Özgür irade problemi","c":"Kötülük problemi","d":"Bilgi problemi"},"answer":"a","difficulty":"zor","skill":"mantiksal_cikarim"},
    {"id":"k4_l_14","text":"Hankel, Cantor'un çaprazlama argümanı neyi kanıtlar?","options":{"a":"Doğal sayılar sonludur","b":"Gerçek sayılar doğal sayılardan 'daha büyük' bir sonsuzluktur","c":"Sonsuzluk yoktur","d":"Her küme sayılabilir"},"answer":"b","difficulty":"zor","skill":"mantiksal_cikarim"},
    {"id":"k4_l_15","text":"NP-tam problem ne demektir?","options":{"a":"Çözümü kolay, doğrulaması zor","b":"Çözümü zor ama doğrulaması kolay, ve tüm NP problemleri buna indirgenebilir","c":"Çözümsüz","d":"Sadece kuantum bilgisayarla çözülür"},"answer":"b","difficulty":"zor","skill":"mantiksal_cikarim"},
]

K4_OZ_DEGER = [
    {"id":"k4_od_1","text":"Akademik literatürü takip edip sentezleyebilirim."},
    {"id":"k4_od_2","text":"YKS/sınav hazırlık sürecimi stratejik olarak planlayabilirim."},
    {"id":"k4_od_3","text":"Farklı kaynakları karşılaştırarak bilgiyi eleştirel değerlendirebilirim."},
    {"id":"k4_od_4","text":"İleri matematik kavramlarını (türev, integral, olasılık) anlıyorum."},
    {"id":"k4_od_5","text":"Bir konudaki varsayımları tespit edip sorgulayabilirim."},
    {"id":"k4_od_6","text":"Akademik yazım kurallarına uygun metin üretebilirim."},
    {"id":"k4_od_7","text":"Üniversite ve kariyer hedeflerim net ve bu hedeflere yönelik çalışıyorum."},
    {"id":"k4_od_8","text":"Karmaşık problemleri parçalara ayırarak sistematik çözebilirim."},
    {"id":"k4_od_9","text":"Disiplinlerarası düşünce ile yenilikçi çözümler üretebilirim."},
    {"id":"k4_od_10","text":"Kendi bilişsel güçlü ve zayıf yönlerimin farkındayım."},
    {"id":"k4_od_11","text":"Akademik baskı altında bile performansımı koruyabilirim."},
    {"id":"k4_od_12","text":"Öğrendiklerimi toplumsal sorunlara uygulayabilirim."},
]


# ============================================================
# BÖLÜM VE VERSİYON PAKETLERİ
# ============================================================
ALL_KADEMELER = {
    "kademe_1": {"okuma": K1_OKUMA, "matematik": K1_MATEMATIK, "mantik": K1_MANTIK, "oz_deger": K1_OZ_DEGER},
    "kademe_2": {"okuma": K2_OKUMA, "matematik": K2_MATEMATIK, "mantik": K2_MANTIK, "oz_deger": K2_OZ_DEGER},
    "kademe_3": {"okuma": K3_OKUMA, "matematik": K3_MATEMATIK, "mantik": K3_MANTIK, "oz_deger": K3_OZ_DEGER},
    "kademe_4": {"okuma": K4_OKUMA, "matematik": K4_MATEMATIK, "mantik": K4_MANTIK, "oz_deger": K4_OZ_DEGER},
}

def get_akademik_sections(grade=None, version=None):
    """Sınıf veya versiyon bazlı bölümleri döndürür. Geriye uyumlu."""
    if grade is not None:
        kademe = grade_to_kademe(grade)
    elif version == "ilkogretim":
        kademe = "kademe_1"
    elif version == "lise":
        kademe = "kademe_3"
    else:
        kademe = "kademe_2"

    data = ALL_KADEMELER[kademe]
    return [
        {"name": "📖 Okuma Anlama", "type": "passage_mc", "data": data["okuma"], "icon": "📖"},
        {"name": "🔢 Matematiksel Muhakeme", "type": "mc", "data": data["matematik"], "icon": "🔢"},
        {"name": "🧩 Mantıksal Düşünme", "type": "mc", "data": data["mantik"], "icon": "🧩"},
        {"name": "📝 Akademik Öz-Değerlendirme", "type": "likert", "data": data["oz_deger"], "icon": "📝"},
    ]

def get_total_questions(grade=None, version=None):
    sections = get_akademik_sections(grade=grade, version=version)
    total = 0
    for sec in sections:
        if sec["type"] == "passage_mc":
            for p in sec["data"]:
                total += len(p["questions"])
        else:
            total += len(sec["data"])
    return total


# ============================================================
# SKORLAMA — ZORLUK AĞIRLIKLI + ALT BECERİ
# ============================================================
def calculate_akademik(answers, grade=None, version=None):
    sections = get_akademik_sections(grade=grade, version=version)
    kademe = grade_to_kademe(grade) if grade else ("kademe_1" if version == "ilkogretim" else "kademe_3" if version == "lise" else "kademe_2")
    results = {}

    for sec in sections:
        sec_name = sec["name"]
        sec_type = sec["type"]

        if sec_type == "passage_mc":
            correct = total = weighted = weighted_max = 0
            diff_breakdown = {"kolay": [0, 0], "orta": [0, 0], "zor": [0, 0]}
            skill_breakdown = {}
            for passage in sec["data"]:
                for q in passage["questions"]:
                    total += 1
                    diff = q.get("difficulty", "orta")
                    w = DIFFICULTY_WEIGHTS.get(diff, 1)
                    weighted_max += w
                    diff_breakdown[diff][1] += 1
                    sk = q.get("skill", "detay_bulma")
                    if sk not in skill_breakdown:
                        skill_breakdown[sk] = [0, 0]
                    skill_breakdown[sk][1] += 1
                    if answers.get(q["id"]) == q["answer"]:
                        correct += 1
                        weighted += w
                        diff_breakdown[diff][0] += 1
                        skill_breakdown[sk][0] += 1
            pct = round(weighted / max(weighted_max, 1) * 100, 1)
            results[sec_name] = {
                "correct": correct, "total": total, "pct": pct,
                "weighted_score": weighted, "weighted_max": weighted_max,
                "difficulty_breakdown": {k: {"correct": v[0], "total": v[1], "pct": round(v[0]/max(v[1],1)*100,1)} for k, v in diff_breakdown.items()},
                "skill_breakdown": {k: {"correct": v[0], "total": v[1], "pct": round(v[0]/max(v[1],1)*100,1)} for k, v in skill_breakdown.items()},
            }

        elif sec_type == "mc":
            correct = total = weighted = weighted_max = 0
            diff_breakdown = {"kolay": [0, 0], "orta": [0, 0], "zor": [0, 0]}
            skill_breakdown = {}
            for q in sec["data"]:
                total += 1
                diff = q.get("difficulty", "orta")
                w = DIFFICULTY_WEIGHTS.get(diff, 1)
                weighted_max += w
                diff_breakdown[diff][1] += 1
                sk = q.get("skill", "hesaplama")
                if sk not in skill_breakdown:
                    skill_breakdown[sk] = [0, 0]
                skill_breakdown[sk][1] += 1
                if answers.get(q["id"]) == q["answer"]:
                    correct += 1
                    weighted += w
                    diff_breakdown[diff][0] += 1
                    skill_breakdown[sk][0] += 1
            pct = round(weighted / max(weighted_max, 1) * 100, 1)
            results[sec_name] = {
                "correct": correct, "total": total, "pct": pct,
                "weighted_score": weighted, "weighted_max": weighted_max,
                "difficulty_breakdown": {k: {"correct": v[0], "total": v[1], "pct": round(v[0]/max(v[1],1)*100,1)} for k, v in diff_breakdown.items()},
                "skill_breakdown": {k: {"correct": v[0], "total": v[1], "pct": round(v[0]/max(v[1],1)*100,1)} for k, v in skill_breakdown.items()},
            }

        elif sec_type == "likert":
            total_score = 0
            count = len(sec["data"])
            for q in sec["data"]:
                val = answers.get(q["id"], 3)
                if isinstance(val, str):
                    try: val = int(val)
                    except ValueError: val = 3
                total_score += val
            max_score = count * 5
            pct = round(total_score / max(max_score, 1) * 100, 1)
            results[sec_name] = {"score": total_score, "max": max_score, "pct": pct, "count": count}

    # Genel hesaplama
    perf_keys = [k for k in results if "Öz-Değerlendirme" not in k]
    oz_key = [k for k in results if "Öz-Değerlendirme" in k]
    perf_avg = sum(results[k]["pct"] for k in perf_keys) / max(len(perf_keys), 1)
    oz_avg = results[oz_key[0]]["pct"] if oz_key else 0
    overall = round(perf_avg * 0.75 + oz_avg * 0.25, 1)

    if overall >= 80: level, level_emoji, level_desc = "Çok Yüksek", "🟢", "Akademik yetkinlik mükemmel düzeyde."
    elif overall >= 65: level, level_emoji, level_desc = "Yüksek", "🔵", "Akademik yetkinlik ortalamanın üzerinde."
    elif overall >= 50: level, level_emoji, level_desc = "Orta", "🟡", "Akademik yetkinlik ortalama düzeyde."
    elif overall >= 35: level, level_emoji, level_desc = "Gelişime Açık", "🟠", "Akademik yetkinlik gelişime açık."
    else: level, level_emoji, level_desc = "Acil Destek", "🔴", "Akademik destek ihtiyacı tespit edildi."

    gap = round(oz_avg - perf_avg, 1)
    if abs(gap) <= 10: gap_type, gap_desc = "tutarli", "Öz değerlendirme performansla tutarlı."
    elif gap > 20: gap_type, gap_desc = "asiri_ozguvenli", f"Kendini %{abs(gap)} yüksek değerlendiriyor."
    elif gap > 10: gap_type, gap_desc = "hafif_ozguvenli", f"Kendini biraz yüksek değerlendiriyor (fark: %{abs(gap)})."
    elif gap < -20: gap_type, gap_desc = "dusuk_ozguven", f"Kendini %{abs(gap)} düşük değerlendiriyor — özgüven desteği gerekli."
    else: gap_type, gap_desc = "hafif_dusuk", f"Kendini biraz düşük değerlendiriyor (fark: %{abs(gap)})."

    perf_sorted = sorted([(k, results[k]["pct"]) for k in perf_keys], key=lambda x: x[1], reverse=True)
    strongest = perf_sorted[0] if perf_sorted else ("", 0)
    weakest = perf_sorted[-1] if perf_sorted else ("", 0)

    return {
        "version": version or kademe, "kademe": kademe, "kademe_label": KADEME_LABELS.get(kademe, ""),
        "grade": grade, "sections": results,
        "performance_avg": round(perf_avg, 1), "self_assessment": oz_avg,
        "overall": overall, "level": level, "level_emoji": level_emoji, "level_desc": level_desc,
        "strongest": {"name": strongest[0], "pct": strongest[1]},
        "weakest": {"name": weakest[0], "pct": weakest[1]},
        "gap": gap, "gap_type": gap_type, "gap_desc": gap_desc,
    }


# ============================================================
# RAPOR ÜRETİCİ
# ============================================================
def generate_akademik_report(scores):
    kademe_label = scores.get("kademe_label", "")
    level_emoji = scores.get("level_emoji", "🟡")
    grade = scores.get("grade", "")
    grade_str = f" ({grade}. Sınıf)" if grade else ""

    def bar(pct):
        n = max(0, min(10, round(pct / 10)))
        return "█" * n + "░" * (10 - n)

    def level_icon(pct):
        if pct >= 80: return "🟢"
        elif pct >= 65: return "🔵"
        elif pct >= 50: return "🟡"
        elif pct >= 35: return "🟠"
        return "🔴"

    sec_rows = ""
    for name, data in scores["sections"].items():
        pct = data["pct"]
        if "correct" in data:
            detail = f"{data['correct']}/{data['total']}"
        else:
            detail = f"{data['score']}/{data['max']}"
        sec_rows += f"| {level_icon(pct)} {name} | {detail} | %{pct} | {bar(pct)} |\n"

    report = f"""# 📚 AKADEMİK ANALİZ RAPORU — {kademe_label}{grade_str}

---

## 📊 Genel Akademik Profil

| Gösterge | Değer |
|----------|-------|
| 📈 Genel Akademik Skor | {level_emoji} **%{scores['overall']}** |
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

## 📊 Zorluk Kademesi Analizi

"""

    for name, data in scores["sections"].items():
        if "difficulty_breakdown" in data:
            report += f"### {name}\n\n| Zorluk | Doğru/Toplam | Başarı |\n|--------|-------------|--------|\n"
            for diff in ["kolay", "orta", "zor"]:
                db = data["difficulty_breakdown"].get(diff, {"correct": 0, "total": 0, "pct": 0})
                emoji = {"kolay": "🟢", "orta": "🟡", "zor": "🔴"}[diff]
                report += f"| {emoji} {diff.capitalize()} | {db['correct']}/{db['total']} | %{db['pct']} |\n"
            report += "\n"

    report += "---\n\n## 🎯 Alt Beceri Profili\n\n"
    for name, data in scores["sections"].items():
        if "skill_breakdown" in data and data["skill_breakdown"]:
            report += f"### {name}\n\n| Beceri | Doğru/Toplam | Başarı |\n|--------|-------------|--------|\n"
            for sk, sb in sorted(data["skill_breakdown"].items(), key=lambda x: x[1]["pct"], reverse=True):
                label = SKILL_LABELS.get(sk, sk)
                report += f"| {label} | {sb['correct']}/{sb['total']} | {bar(sb['pct'])} %{sb['pct']} |\n"
            report += "\n"

    # Güçlü/Zayıf
    report += f"""---

## 💪 En Güçlü Alan: {scores['strongest']['name']}
%{scores['strongest']['pct']} başarı oranıyla en güçlü performans.

## 🌱 Gelişim Alanı: {scores['weakest']['name']}
%{scores['weakest']['pct']} başarı oranıyla gelişim potansiyeli taşıyor.

---

## 🔍 Öz-Değerlendirme Analizi

{scores['gap_desc']}

"""

    # Zorluk bazlı yorum
    for name, data in scores["sections"].items():
        if "difficulty_breakdown" in data:
            db = data["difficulty_breakdown"]
            kolay_pct = db.get("kolay", {}).get("pct", 0)
            zor_pct = db.get("zor", {}).get("pct", 0)
            if kolay_pct >= 80 and zor_pct < 30:
                report += f"**{name}:** Temel kavramlar güçlü ama zor sorularda zorlanılıyor → Derinleştirme ve uygulama çalışması önerilir.\n\n"
            elif kolay_pct < 50:
                report += f"**{name}:** Temel kavramlarda bile güçlük var → Temelden başlayarak adım adım ilerleme önerilir.\n\n"
            elif zor_pct >= 60:
                report += f"**{name}:** Zor sorularda bile yüksek başarı → Meydan okuyucu problemlerle zenginleştirme önerilir.\n\n"

    # Ebeveyn + Öğretmen
    report += """---

## 👨‍👩‍👦 Ebeveyn Rehberi

"""
    if scores["overall"] >= 65:
        report += "Çocuğunuzun akademik performansı güçlü! Zenginleştirme etkinlikleri ve ileri düzey materyaller sunun.\n\n"
    elif scores["overall"] >= 50:
        report += "Çocuğunuz ortalama düzeyde. Zayıf alanlara haftada 2-3 saat ekstra çalışma ve öğrenme stiline uygun materyaller önerilir.\n\n"
    else:
        report += "Çocuğunuzun akademik desteğe ihtiyacı var. Okul rehberlik servisi, bireysel destek ve temel becerilere odaklanma önerilir.\n\n"

    report += f"""## 👩‍🏫 Öğretmen Notu

**Kademe:** {kademe_label}
**Seviye:** {scores['level']} (%{scores['overall']})
**Güçlü:** {scores['strongest']['name']} (%{scores['strongest']['pct']})
**Gelişim:** {scores['weakest']['name']} (%{scores['weakest']['pct']})

"""

    report += f"""---

## 📌 Özet Tablo

| Gösterge | Sonuç |
|----------|-------|
| Kademe | {kademe_label} |
| Genel Skor | **%{scores['overall']}** ({scores['level']}) |
| En Güçlü Alan | {scores['strongest']['name']} (%{scores['strongest']['pct']}) |
| Gelişim Alanı | {scores['weakest']['name']} (%{scores['weakest']['pct']}) |
| Performans / Öz-Değerlendirme | %{scores['performance_avg']} / %{scores['self_assessment']} |
"""
    return report.strip()
