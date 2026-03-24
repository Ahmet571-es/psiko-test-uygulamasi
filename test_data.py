# ============================================================
# test_data.py — Tüm Psikolojik Testlerin Sabit Verileri
# DÜZELTMELER:
#   1. Tüm calculate_* fonksiyonlarında key tipi normalize edildi
#      (DB json.loads → str key → int key dönüşümü)
#   2. calculate_calisma_davranisi: O(n²) → O(n) lookup dict
#   3. Sınav Kaygısı soru 3 ters madde olarak düzeltildi
#   4. VARK multimodal eşiği Fleming standardına (<=2) güncellendi
# ============================================================

# ============================================================
# BÖLÜM 1: SAĞ-SOL BEYİN TESTİ
# ============================================================

SAG_SOL_BEYIN_QUESTIONS = [
    {"id": 1,  "text": "Aşağıdakilerden hangisi sana daha çok uyuyor?", "a": "Risk almak eğlencelidir, heyecan verir.", "b": "Risk almadan da gayet iyi eğlenebilirim.", "right_brain": "a"},
    {"id": 2,  "text": "Bir işi yaparken nasıl davranırsın?", "a": "Eski işleri yapmak için sürekli yeni yollar ararım.", "b": "Bir yol iyi çalışıyorsa onu değiştirmem, aynen devam ederim.", "right_brain": "a"},
    {"id": 3,  "text": "İşlerini bitirme konusunda hangisi seni daha iyi tanımlar?", "a": "Birçok işe başlarım ama hepsini bitiremeyebilirim.", "b": "Bir işi bitirmeden kesinlikle yenisine başlamam.", "right_brain": "a"},
    {"id": 4,  "text": "Hayal gücünü kullanma konusunda nasılsın?", "a": "İşlerimde çok fazla hayal gücü kullanmam, gerçekçiyimdir.", "b": "Her işimde mutlaka hayal gücümü kullanırım.", "right_brain": "b"},
    {"id": 5,  "text": "Gelecekte ne olacağını tahmin ederken hangisini kullanırsın?", "a": "Olayları analiz ederek ne olacağını tahmin ederim.", "b": "İçimden gelen hisle ne olacağını hissederim.", "right_brain": "b"},
    {"id": 6,  "text": "Bir problemle karşılaştığında nasıl çözersin?", "a": "En iyi tek çözümü bulmaya çalışırım.", "b": "Birden fazla farklı çözüm yolu ararım.", "right_brain": "b"},
    {"id": 7,  "text": "Düşüncelerin kafanın içinde nasıl akar?", "a": "Düşüncelerim resimler ve görüntüler gibi akar.", "b": "Düşüncelerim kelimeler ve cümleler gibi akar.", "right_brain": "a"},
    {"id": 8,  "text": "Yeni fikirler karşısında nasıl tepki verirsin?", "a": "Yeni fikirleri başkalarından önce kabul ederim.", "b": "Yeni fikirleri başkalarından çok sorgularım.", "right_brain": "a"},
    {"id": 9,  "text": "Düzenin hakkında ne derler?", "a": "Başkaları benim düzenimi anlamaz ama bana göre düzenlidir.", "b": "Başkaları benim çok düzenli olduğumu söyler.", "right_brain": "a"},
    {"id": 10, "text": "Disiplin konusunda kendini nasıl tanımlarsın?", "a": "İyi bir öz disiplinim vardır, kendimi kontrol ederim.", "b": "Genellikle duygularıma ve içgüdülerime göre hareket ederim.", "right_brain": "b"},
    {"id": 11, "text": "İş yaparken zamanı nasıl kullanırsın?", "a": "Zamanımı önceden planlarım.", "b": "İş yaparken zamanı pek düşünmem, akar gider.", "right_brain": "b"},
    {"id": 12, "text": "Zor bir karar vermek gerektiğinde ne yaparsın?", "a": "Doğru bildiğimi, mantığıma uygun olanı seçerim.", "b": "Kalbimin ve hislerimin söylediğini seçerim.", "right_brain": "b"},
    {"id": 13, "text": "İşlerini hangi sırayla yaparsın?", "a": "Kolay işleri önce, önemli işleri sonra yaparım.", "b": "Önemli işleri önce, kolay işleri sonra yaparım.", "right_brain": "a"},
    {"id": 14, "text": "Yeni bir durumla karşılaştığında ne olur?", "a": "Kafamda çok fazla fikir uçuşur, hangisini seçeceğimi bilemem.", "b": "Bazen hiç fikrim olmaz, ne yapacağımı düşünmem gerekir.", "right_brain": "a"},
    {"id": 15, "text": "Yeni fikirler hakkında hangisi seni anlatır?", "a": "Yeni fikirleri çok sorgularım, kanıt isterim.", "b": "Yeni fikirlere açığımdır, hemen denerim.", "right_brain": "b"},
    {"id": 16, "text": "Hayatında değişiklik konusunda ne düşünürsün?", "a": "Hayatımda çok değişiklik ve çeşitlilik isterim.", "b": "Düzenli ve planlı bir hayat tercih ederim.", "right_brain": "a"},
    {"id": 17, "text": "Haklı olduğunu nasıl bilirsin?", "a": "Haklı olduğumu bilirim çünkü iyi nedenlerim ve kanıtlarım vardır.", "b": "Haklı olduğumu hissederim, bazen nedenim olmasa bile.", "right_brain": "b"},
    {"id": 18, "text": "İşlerini zamana nasıl yayarsın?", "a": "İşlerimi zamana eşit olarak yayarım.", "b": "İşlerimi son dakikada yapmayı tercih ederim.", "right_brain": "b"},
    {"id": 19, "text": "Eşyalarını nereye koyarsın?", "a": "Her şeyi belirli bir yere koyarım, hep aynı yer.", "b": "Eşyalarımın yeri o an ne yaptığıma göre değişir.", "right_brain": "b"},
    {"id": 20, "text": "Hangisi seni daha iyi tanımlar?", "a": "Tutarlıyımdır, ne yapacağım bellidir.", "b": "Spontaneyimdir, anlık kararlar verir sürprizleri severim.", "right_brain": "b"},
    {"id": 21, "text": "Çalışma ortamın nasıl olmalı?", "a": "Düzenli ve tertipli bir ortamda çalışmalıyım.", "b": "Rahat hissettiğim, esnek bir ortamda çalışırım.", "right_brain": "b"},
    {"id": 22, "text": "Okulda hangi tür dersleri daha çok seversin?", "a": "Türkçe, resim, müzik gibi sözel ve sanatsal dersler.", "b": "Matematik, fen bilgisi gibi sayısal dersler.", "right_brain": "a"},
    {"id": 23, "text": "Hangi tür sporları tercih edersin?", "a": "Tek başına yapılan sporlar (yüzme, koşu, bisiklet).", "b": "Takım sporları (basketbol, voleybol, futbol).", "right_brain": "a"},
    {"id": 24, "text": "Gördüğün rüyaları hatırlar mısın?", "a": "Evet, rüyalarımı çoğu zaman canlı ve detaylı hatırlarım.", "b": "Hayır, rüyalarımı nadiren hatırlarım.", "right_brain": "a"},
    {"id": 25, "text": "Konuşurken ellerini ve yüz ifadelerini nasıl kullanırsın?", "a": "Çok fazla el kol hareketi ve mimik kullanırım.", "b": "Çok az hareket yaparım, sakin konuşurum.", "right_brain": "a"},
    {"id": 26, "text": "Bir hikaye anlatırken nasıl anlatırsın?", "a": "Olayları sırasıyla, baştan sona düzgünce anlatırım.", "b": "Aklıma geldiği gibi, renkli detaylar ve duygular katarak anlatırım.", "right_brain": "b"},
    {"id": 27, "text": "İnsanları tanırken neyi daha çabuk hatırlarsın?", "a": "İnsanların yüzlerini ve görünüşlerini hatırlarım.", "b": "İnsanların isimlerini ve söylediklerini hatırlarım.", "right_brain": "a"},
    {"id": 28, "text": "Bir şey öğrenirken hangisini tercih edersin?", "a": "Resim, grafik, şema gibi görsellerle öğrenmek.", "b": "Yazılı metin okuyarak ve not alarak öğrenmek.", "right_brain": "a"},
    {"id": 29, "text": "Odanın düzeni hakkında ne düşünürsün?", "a": "Odamdaki eşyaların her zaman aynı yerde ve düzenli durmasını isterim.", "b": "Odamda yaratıcı bir dağınıklık vardır, ama ben nereye ne koyduğumu bilirim.", "right_brain": "b"},
    {"id": 30, "text": "Birinin yalan söylediğini nasıl anlarsın?", "a": "Söylediklerindeki çelişkileri ve mantık hatalarını yakalarım.", "b": "Yüz ifadesinden ve ses tonundan hissederim, sezgilerime güvenirim.", "right_brain": "b"},
]

SAG_SOL_BEYIN_DATA = {
    "sag": {
        "title": "Sağ Beyin Baskın", "icon": "🎨",
        "description": "Sen dünyaya daha çok duygularınla, sezgilerinle ve hayal gücünle bakan birisin. Yaratıcılık senin süper gücün!",
        "strengths": ["Güçlü hayal gücü ve yaratıcılık", "Sezgileri kuvvetli, insanları iyi okur", "Sanatsal ve görsel yetenekler", "Bütüncül düşünme (büyük resmi görme)", "Empati ve duygusal zeka", "Esnek ve spontane düşünme"],
        "development_areas": ["Zaman yönetimi ve planlama becerilerini geliştirebilirsin", "Detaylara daha fazla dikkat edebilirsin", "Başladığın işleri bitirme konusunda kendine hedefler koyabilirsin", "Düzenli çalışma alışkanlıkları edinebilirsin"],
        "study_tips": ["Ders çalışırken renkli kalemler, zihin haritaları (mind map) ve şemalar kullan.", "Konuları hikayeleştirerek veya görselleştirerek öğren.", "Müzik dinleyerek çalışmak sana iyi gelebilir (sözsüz müzik dene).", "Uzun çalışma seansları yerine kısa ama yaratıcı molalar ver.", "Grup çalışmalarında fikirlerini paylaşmaktan çekinme, farklı bakış açın değerli."],
        "career_areas": ["Sanat ve Tasarım", "Müzik", "Edebiyat ve Yazarlık", "Psikoloji", "Mimarlık", "Reklamcılık", "Fotoğrafçılık", "Oyun Tasarımı", "Film ve Sinema"],
    },
    "sol": {
        "title": "Sol Beyin Baskın", "icon": "🔬",
        "description": "Sen dünyaya daha çok mantığınla, analizlerinle ve sistemli düşünmenle bakan birisin. Analitik güç senin süper gücün!",
        "strengths": ["Güçlü analitik ve mantıksal düşünme", "Detaylara dikkat ve titizlik", "İyi planlama ve organizasyon", "Matematiksel ve sayısal beceriler", "Disiplinli ve tutarlı çalışma", "Dil ve sözel ifade becerileri"],
        "development_areas": ["Yaratıcı düşünme ve hayal gücünü geliştirebilirsin", "Duygularını ifade etme konusunda daha rahat olabilirsin", "Spontane ve esnek olmayı deneyebilirsin", "Büyük resmi görmek için adım geri atabilirsin"],
        "study_tips": ["Konuları sıralı ve adım adım çalış, listeler ve özetler çıkar.", "Formüller, kurallar ve kalıplar senin en iyi arkadaşın.", "Sessiz ve düzenli bir çalışma ortamı oluştur.", "Zaman planı yap ve ona sadık kal — bu seni güçlü kılar.", "Her konunun 'neden' ve 'nasıl' sorularını sor, derinlemesine anla."],
        "career_areas": ["Mühendislik", "Tıp", "Hukuk", "Bilgisayar Bilimi", "Muhasebe ve Finans", "Bilimsel Araştırma", "Matematik", "Programlama", "Bankacılık"],
    },
    "dengeli": {
        "title": "Dengeli Beyin", "icon": "⚖️",
        "description": "Sen hem yaratıcı hem de analitik tarafını dengeli kullanan birisin. Bu çok özel ve güçlü bir kombinasyon!",
        "strengths": ["Hem yaratıcı hem analitik düşünebilme", "Farklı durumlarına uyum sağlama esnekliği", "Hem detayları hem büyük resmi görebilme", "Dengeli karar verme yeteneği", "Farklı insanlarla iyi iletişim kurabilme", "Çok yönlü problem çözme becerisi"],
        "development_areas": ["Bazen hangi tarafını kullanacağına karar vermekte zorlanabilirsin", "Bir alanda uzmanlaşmak için bilinçli tercihler yapabilirsin", "Güçlü yönlerini keşfetmek için farklı alanları denemeye devam et"],
        "study_tips": ["Hem görsel hem yazılı materyalleri birlikte kullan.", "Bazen planlı, bazen serbest çalışmayı dene — ikisi de sana uyar.", "Hem bireysel hem grup çalışmalarından verim alabilirsin.", "Farklı ders çalışma tekniklerini dönüşümlü kullan.", "Güçlü olduğun tarafı keşfet ve onu bilinçli geliştir."],
        "career_areas": ["Girişimcilik", "Proje Yönetimi", "Eğitim ve Öğretmenlik", "Danışmanlık", "İletişim ve Medya", "Araştırma-Geliştirme", "Mühendislik Tasarımı", "Ürün Geliştirme"],
    },
}


def calculate_sag_sol_beyin(answers):
    """
    DÜZELTME: answers = {int(k): v} — DB'den str key gelirse int'e çevir.
    """
    answers = {int(k): v for k, v in answers.items()}

    sag_puan = 0
    sol_puan = 0
    for q in SAG_SOL_BEYIN_QUESTIONS:
        student_answer = answers.get(q["id"])
        if student_answer is None:
            continue
        if student_answer == q["right_brain"]:
            sag_puan += 1
        else:
            sol_puan += 1

    total = sag_puan + sol_puan or 1
    sag_yuzde = round(sag_puan / total * 100, 1)
    sol_yuzde = round(sol_puan / total * 100, 1)

    if sag_puan <= 8:
        dominant = "sol"
        level = "Güçlü Sol Beyin" if sag_puan <= 5 else "Orta Düzey Sol Beyin"
    elif sag_puan >= 22:
        dominant = "sag"
        level = "Güçlü Sağ Beyin" if sag_puan >= 25 else "Orta Düzey Sağ Beyin"
    else:
        dominant = "dengeli"
        level = "Dengeli Beyin"

    scores = {
        "sag_beyin": sag_puan,
        "sol_beyin": sol_puan,
        "sag_yuzde": sag_yuzde,
        "sol_yuzde": sol_yuzde,
        "dominant": dominant,
        "level": level,
    }
    report = generate_sag_sol_beyin_report(scores)
    return scores, report


def generate_sag_sol_beyin_report(scores):
    dominant = scores["dominant"]
    data = SAG_SOL_BEYIN_DATA[dominant]
    sag  = scores["sag_beyin"];  sol  = scores["sol_beyin"]
    sag_y = scores["sag_yuzde"]; sol_y = scores["sol_yuzde"]
    level = scores["level"]

    def bar(pct): n = round(pct/10); return "█"*n + "░"*(10-n)

    strengths_text = "\n".join(f"- ✅ {s}" for s in data["strengths"])
    dev_text       = "\n".join(f"- 🌱 {d}" for d in data["development_areas"])
    tips_text      = "\n".join(f"- 💡 {t}" for t in data["study_tips"])
    career_text    = ", ".join(data["career_areas"])

    return f"""# {data['icon']} SAĞ-SOL BEYİN ÜSTÜNLÜĞÜ RAPORU

**Sonucun:** {level}

---

## 📊 Puan Tablon

| Beyin Yarımküresi | Puan | Yüzde | Grafik |
|---|---|---|---|
| 🎨 Sağ Beyin | {sag}/30 | %{sag_y} | {bar(sag_y)} |
| 🔬 Sol Beyin | {sol}/30 | %{sol_y} | {bar(sol_y)} |

---

## 🌟 Sen Kimsin?
{data['description']}

---

## 💪 Senin Süper Güçlerin
{strengths_text}

---

## 🌱 Geliştirebileceğin Alanlar
{dev_text}

---

## 📚 Sana Özel Ders Çalışma İpuçları
{tips_text}

---

## 🚀 Sana Uygun Kariyer Alanları
{career_text}

---

## 💬 Son Söz
Unutma, sağ beyin veya sol beyin baskın olmak iyi ya da kötü değildir! Her ikisi de harika süper güçlerdir. Önemli olan kendi güçlü tarafını tanımak ve onu en iyi şekilde kullanmaktır. 🌟""".strip()


# ============================================================
# BÖLÜM 2: ÇALIŞMA DAVRANIŞI ÖLÇEĞİ (BALTAŞ)
# ============================================================

CALISMA_DAVRANISI_QUESTIONS = [
    {"id": 1,  "text": "Derslerle ilgili tekrarlarımın çoğunu sınavdan önceki gece yaparım.", "category": "G", "key": "Y"},
    {"id": 2,  "text": "Sınavlara hazırlanırken, sinirlilikten, gerginlikten, huzursuzluktan ötürü çalışmakta güçlük çekerim.", "category": "G", "key": "Y"},
    {"id": 3,  "text": "Ödevler ve kompozisyonlar bana angarya gelir, bir an önce kurtulmak isterim.", "category": "E", "key": "Y"},
    {"id": 4,  "text": "Anlayabilmek için çoğunlukla bir konuyu defalarca okurum.", "category": "D", "key": "Y"},
    {"id": 5,  "text": "Derse çalışırken önemli noktaları bulup çıkartmakta güçlük çekerim.", "category": "D", "key": "Y"},
    {"id": 6,  "text": "Bir dönem ödevini hazırlamaya başlamadan önce mutlaka müsveddesini yaparım.", "category": "G", "key": "D"},
    {"id": 7,  "text": "Bilmediğim veya anlamından emin olmadığım kelimeleri sözlükten bakarım.", "category": "D", "key": "D"},
    {"id": 8,  "text": "Not tutarken, öğretmenin veya yazarın kelimelerini değil kendi kelimelerimi kullanırım.", "category": "C", "key": "D"},
    {"id": 9,  "text": "Bir test sırasında sinirli olurum ve hak ettiğim kadar başarılı olamam.", "category": "G", "key": "Y"},
    {"id": 10, "text": "Derste notlarımı not defteri yerine elime geçen kağıtlara alırım.", "category": "C", "key": "Y"},
    {"id": 11, "text": "Zaman zaman okuduklarımı grafikler, şemalar ve özetler halinde ifade ederim.", "category": "D", "key": "D"},
    {"id": 12, "text": "Bir cümleyi meydana getiren ögeleri gerçekten bilmiyorum.", "category": "B", "key": "Y"},
    {"id": 13, "text": "Çalışmaya başlamak için çoğunlukla içimden gelmesini beklerim.", "category": "A", "key": "Y"},
    {"id": 14, "text": "Düzenli olarak tekrarlar yaparım.", "category": "B", "key": "D"},
    {"id": 15, "text": "Çalışmam sırasında telefonla arayanlar, gelen-giden ve başka sebepler çalışmaya ara vermemi gerektirir.", "category": "A", "key": "Y"},
    {"id": 16, "text": "Bir başka derse geçmeden önce, başladığım dersi bütünüyle tamamlarım.", "category": "B", "key": "Y"},
    {"id": 17, "text": "Çalışmam için harcamam gereken zamanı oyunda, televizyonun başında, telefonda, müzik dinleyerek, arkadaşlarla geçirdiğim olur.", "category": "A", "key": "Y"},
    {"id": 18, "text": "Zaman zaman, dersin amacının tam olarak ne olduğunu bilmeden, çalışmaya başladığımı fark ederim.", "category": "A", "key": "Y"},
    {"id": 19, "text": "Okulda öğrendiğim derslerle ilgili konuları dış dünyadaki olayları anlayabilmek için kullanırım.", "category": "B", "key": "D"},
    {"id": 20, "text": "Ders notlarının hepsini not defterimin içinde toplu olarak saklarım.", "category": "C", "key": "D"},
    {"id": 21, "text": "Kompozisyon ve dönem ödevlerinde sonuç bölümünü yazmakta zorlanıyorum.", "category": "G", "key": "Y"},
    {"id": 22, "text": "Öğretmenin her söylediğini not aldığım ve bunları elden geçirmediğim için bazen gereksiz malzemeyi çalışmak zorunda kalırım.", "category": "C", "key": "Y"},
    {"id": 23, "text": "Bir kompozisyon veya ödev hazırlarken, başlamadan önce bir plan yaparım.", "category": "E", "key": "D"},
    {"id": 24, "text": "Okuduğum her cümle veya paragraftan sonra not almak yerine, bölümü bitirdikten sonra not çıkartırım.", "category": "C", "key": "D"},
    {"id": 25, "text": "Kompozisyon veya ödevlerimi vermem gereken günden önce hazır ederim ve böylece birkaç kere okur ve gerekiyorsa yeniden yazarım.", "category": "E", "key": "D"},
    {"id": 26, "text": "Ödevleri bazen zamanında hazır edemem ve yetiştirmek zorunda kalırsam aceleyle hazırlarım.", "category": "E", "key": "Y"},
    {"id": 27, "text": "Bazı öğretmen ve derslerden hoşlanmamam okul başarımı etkiler.", "category": "F", "key": "Y"},
    {"id": 28, "text": "Sık sık ne okuduğumu bilmeden sayfalarca okumuş olduğumu fark ederim.", "category": "D", "key": "Y"},
    {"id": 29, "text": "Çoğunlukla okuduğum kitaptaki şekil ve tabloları atlarım.", "category": "D", "key": "Y"},
    {"id": 30, "text": "Bazı dersler için o kadar çok zaman harcıyorum ki, diğer derslere zamanım kalmıyor.", "category": "A", "key": "Y"},
    {"id": 31, "text": "Yeni (bilmediğim) kelimeleri ve anlamlarını yazmak için fihristli bir not defteri tutarım.", "category": "C", "key": "D"},
    {"id": 32, "text": "Çalışırken çoğunlukla kalkıp dolaşırım, gazete okurum veya bir şeyler araştırırım.", "category": "A", "key": "Y"},
    {"id": 33, "text": "Çalışmalarımla ilgili problemle karşılaşırsam, bunları öğretmenimle konuşmakta tereddüt etmem.", "category": "F", "key": "D"},
    {"id": 34, "text": "Bazen okurken önemli kelimeleri mırıldanarak veya fısıldayarak tekrar ederim.", "category": "D", "key": "D"},
    {"id": 35, "text": "Bazı öğretmenlerin beni antipatik bulduğunu hissediyorum.", "category": "F", "key": "Y"},
    {"id": 36, "text": "Doğru cevabı bilsem bile, çoğunlukla sınıfta sorulara cevap vermekten veya tekrarlara katılmaktan çekinirim.", "category": "F", "key": "Y"},
    {"id": 37, "text": "Çoğunlukla uykumu tam olarak alamıyorum ve sınıfta uyukladığımı hissediyorum.", "category": "A", "key": "Y"},
    {"id": 38, "text": "Yeni öğrendiğim kelimeleri uygun durumlarda kullanırım.", "category": "B", "key": "D"},
    {"id": 39, "text": "Zamana göre düzenlenmiş çalışma programım vardır.", "category": "A", "key": "D"},
    {"id": 40, "text": "Çalışırken kolayca hayallere dalabilirim.", "category": "A", "key": "Y"},
    {"id": 41, "text": "Bir yazılıda, yazmaya başlamadan önce o konuda fikir sahibi olmaya çalışmak bence zaman kaybıdır.", "category": "G", "key": "D"},
    {"id": 42, "text": "Yeni bir bölüme başlamadan önce o konuda fikir sahibi olmaya çalışmak bence zaman kaybıdır.", "category": "B", "key": "Y"},
    {"id": 43, "text": "Çalışma programıma sıkı sıkıya bağlı kalma düşüncesi bana sıkıntı verir, programda sık sık değişiklik yapmakta tereddüt etmem.", "category": "A", "key": "Y"},
    {"id": 44, "text": "Bazen televizyon seyrederken veya odada başkaları konuşurken ders çalıştığım olur.", "category": "A", "key": "Y"},
    {"id": 45, "text": "Kitaplarımda önemli veya zor bölümleri işaretlerim, böylece tekrarlarken bu noktalara özel dikkat harcamam mümkün olur.", "category": "D", "key": "D"},
    {"id": 46, "text": "Okurken dinlenme aralarımı bölüm sonlarında veririm ve kendi kendime o bölümün ana noktalarını tekrarlarım.", "category": "D", "key": "D"},
    {"id": 47, "text": "Öğrendiğim genel prensipleri ve kuralları ortaya koyan belirli örnekler düşünürüm.", "category": "B", "key": "D"},
    {"id": 48, "text": "Çalışmaya başlamakta güçlük çekerim.", "category": "A", "key": "Y"},
    {"id": 49, "text": "Bazen okula gittiğimde veya çalışmaya oturduğumda kitapları, kalemleri, notları veya diğer gerekli malzemeyi getirmediğimi fark ederim.", "category": "A", "key": "Y"},
    {"id": 50, "text": "Bir derste öğrendiklerimi, bir başka dersteki konuyu anlamak için kullanırım.", "category": "B", "key": "D"},
    {"id": 51, "text": "Bazen bir konuyu öğrendikten sonra gerekenden fazla tekrar yaparak, unutamayacağım şekilde hafızama yerleştiririm.", "category": "B", "key": "D"},
    {"id": 52, "text": "Bir ödevi nasıl yazmaya başlayacağımı gerçekten bilmiyorum.", "category": "E", "key": "Y"},
    {"id": 53, "text": "Ödevlerim daima içime bir sıkıntı verir.", "category": "E", "key": "Y"},
    {"id": 54, "text": "Bir sınava hazırlanırken, tam olarak kitaptaki kelimeleri hatırlamaya çalıştığım çok olur.", "category": "G", "key": "Y"},
    {"id": 55, "text": "Dersi doğrudan bir ışık altında değil, yansıyarak gelen bir ışık altında çalışırım.", "category": "A", "key": "Y"},
    {"id": 56, "text": "Bir konuyu ayrıntılı olarak çalışmaya başlamadan önce, genel bir fikir sahibi olabilmek için hızlı bir göz gezdiririm.", "category": "D", "key": "D"},
    {"id": 57, "text": "Öğretmenlerimin bana iyi duygular beslediğini hissediyorum.", "category": "F", "key": "D"},
    {"id": 58, "text": "Sınav başladığı zaman puan değerleri ve güçlük derecelerine bakmaksızın vakit kaybetmeden hemen yazmaya koyulurum.", "category": "G", "key": "Y"},
    {"id": 59, "text": "Birçok sınava, öğrendiklerimi sınav bitinceye kadar aklımda tutmak için çalışırım.", "category": "G", "key": "Y"},
    {"id": 60, "text": "Çabuk ancak bütünüyle anlayacak kadar hızlı okurum.", "category": "D", "key": "D"},
    {"id": 61, "text": "Not tutarken kendime ait özel işaretler ve kısaltmalar kullanırım.", "category": "C", "key": "D"},
    {"id": 62, "text": "Notlarımı derste tuttuğum gibi muhafaza eder bir karışıklık olmaması için onlara el sürmem.", "category": "C", "key": "Y"},
    {"id": 63, "text": "Bir ödeve başlamadan önce en az bir veya iki kaynağa bakar, güvendiğim kişilere danışırım.", "category": "E", "key": "D"},
    {"id": 64, "text": "Büyük çoğunlukla okul hayatını ilginç buluyorum.", "category": "F", "key": "D"},
    {"id": 65, "text": "Dersi dinlerken muhtemel sınav sorularına karşı dikkatli olurum ve bunları not alırım.", "category": "G", "key": "D"},
    {"id": 66, "text": "Sınava girmeden önce öğretmenin nelere önem verdiğiyle ilgilenmem ve sınav biçimiyle ilgili bilgi toplamak için vakit kaybetmem.", "category": "G", "key": "Y"},
    {"id": 67, "text": "Çalışma sürelerim oldukça kısadır ve bu yüzden zaman zaman dikkatimi toplamakta zorlanırım.", "category": "A", "key": "Y"},
    {"id": 68, "text": "Okula gitmek gerekmeseydi, pek çok şeyi daha kolay öğrenirdim.", "category": "F", "key": "Y"},
    {"id": 69, "text": "Okulda gençliğin en güzel günleri, hayatta kullanılıp kullanılmayacağı çok şüpheli birçok bilgiyi öğrenmek uğruna ziyan ediliyor.", "category": "F", "key": "Y"},
    {"id": 70, "text": "Ders çalışırken verdiğim dinlenme aralarından sonra tekrar derse dönmekte zorluk çekerim.", "category": "A", "key": "Y"},
    {"id": 71, "text": "Derse gelmeden önce işlenecek dersle ilgili okumayı zaman kaybı olarak görürüm.", "category": "C", "key": "Y"},
    {"id": 72, "text": "Öğretmenin anlattıkları kitapta varsa, onları anlamak için bol zamanım olacağı için fazla endişelenmem.", "category": "C", "key": "Y"},
    {"id": 73, "text": "Her kelimenin anlamına dikkat ederek çok yavaş okurum.", "category": "D", "key": "Y"},
]

CALISMA_DAVRANISI_CATEGORIES = {
    "A": {
        "name": "Çalışmaya Başlamak ve Sürdürmek",
        "question_ids": [13, 30, 40, 49, 15, 32, 43, 55, 17, 37, 44, 67, 18, 39, 48, 70],
        "max_score": 16,
        "interpretations": {
            "high": {"range": (10, 16), "text": "Ders çalışmaya başlamak ve zamanından etkin bir şekilde yararlanmak konusunda ciddi güçlüklerin olduğu görülüyor. Değerli zamanının önemli bir bölümünü ders çalışman gerektiğini düşünerek ya da ders başında ama çalışmadan geçirdiğin anlaşılıyor.", "tips": ["Her gün aynı saatte ders çalışmaya başla — bu bir alışkanlık yaratır.", "Pomodoro tekniğini dene: 25 dakika çalış, 5 dakika mola ver.", "Küçük hedefler koy: 'Bu akşam 2 sayfa çözeceğim' gibi somut planlar yap.", "Dikkat dağıtıcıları (telefon vb.) çalışma saatlerinde uzaklaştır."]},
            "mid": {"range": (5, 9), "text": "Ders çalışmaya başlamak ve sürdürmek konusunda bazı güçlüklerin olduğu anlaşılıyor. Kendi üzerinde denetim kuracak yöntemleri öğrenirsen hem sosyalleşmeye zaman ayırabilir, hem de başarını yükseltebilirsin.", "tips": ["Çalışma ve eğlence saatlerini önceden planla.", "Telefonu çalışma saatlerinde sessize al veya başka odaya koy.", "Çalışma arkadaşı bul — birlikte çalışmak motivasyonu artırır."]},
            "low": {"range": (0, 4), "text": "Ders çalışmaya başlamak ve sürdürmek konusunda önemli bir güçlüğün olmadığı anlaşılıyor. Hem ders çalışmaya ayırdığın zamandan en üst düzeyde yararlanman mümkün oluyor, hem de özel hayatına ve zevklerine zaman ayırabiliyorsun. Tebrikler! 🎉", "tips": []},
        },
    },
    "B": {
        "name": "Bilinçli Çalışmak ve Öğrendiğini Kullanmak",
        "question_ids": [12, 19, 47, 14, 38, 50, 16, 42, 51],
        "max_score": 9,
        "interpretations": {
            "high": {"range": (5, 9), "text": "Bilinçli çalışmak ve öğrendiğini kullanmak konusunda önemli eksiklerin olduğu görülüyor. Düzenli tekrar ve verimli ders çalışma yollarını öğrenmen başarın için büyük önem taşıyor.", "tips": ["Her dersten sonra 10 dakika kısa bir tekrar yap.", "Öğrendiğin bilgileri günlük hayattaki olaylarla ilişkilendir.", "Öğrendiğin konuları arkadaşlarına anlatmayı dene."]},
            "mid": {"range": (3, 4), "text": "Bilinçli çalışmak ve öğrendiğini kullanmak konusunda bazı eksiklerin olduğu görülüyor. Öğreneceğin malzemenin nerede kullanılacağını bilmek ve düzenli tekrar yapma tekniğini geliştirmek başarında köklü değişiklikler yapacaktır.", "tips": ["Haftalık tekrar planı oluştur.", "Öğrendiğin konuları arkadaşlarına anlatmayı dene."]},
            "low": {"range": (0, 2), "text": "Bilinçli çalışan ve öğrendiğini kullanan, bilgini geliştirerek unutmayı önleyen bir öğrenci olduğun görülüyor. Tebrikler! 🎉", "tips": []},
        },
    },
    "C": {
        "name": "Not Tutmak ve Dersi Dinlemek",
        "question_ids": [8, 22, 61, 72, 10, 24, 62, 20, 31, 71],
        "max_score": 10,
        "interpretations": {
            "high": {"range": (6, 10), "text": "Not tutmanın ve dersi dinlemenin başarı üzerindeki etkisini yeterince bilmediğin anlaşılıyor. Not tutmak konusunda tekniğini geliştirir ve bu konuda gayret harcarsan, bunun karşılığını en kısa zamanda göreceğinden emin olabilirsin.", "tips": ["Derste kendi cümlelerinle not al, öğretmenin her kelimesini yazmaya çalışma.", "Notlarını düzenli bir defterde tut, dağınık kağıtlar kullanma.", "Ders sonunda notlarını 5 dakika gözden geçir ve eksikleri tamamla."]},
            "mid": {"range": (3, 5), "text": "Not tutmak ve ders dinlemek konusunda bazı hataların olduğu anlaşılıyor.", "tips": ["Cornell not tutma yöntemini araştır ve dene.", "Kendi kısaltma ve sembollerini geliştir — daha hızlı not alırsın."]},
            "low": {"range": (0, 2), "text": "Not tutmak ve dersi dinlemek konusunda başarılı olduğun anlaşılıyor. Harika! 🎉", "tips": []},
        },
    },
    "D": {
        "name": "Okuma Alışkanlıkları ve Teknikleri",
        "question_ids": [4, 11, 34, 56, 5, 28, 45, 60, 7, 29, 46, 73],
        "max_score": 12,
        "interpretations": {
            "high": {"range": (8, 12), "text": "Okumaya çok fazla zaman ayırdığın, buna rağmen daha sonra oldukça az şey hatırlayabildiğin anlaşılıyor. Önemli olanla olmayanı ayırmakta güçlük çektiğin ve metin içinde sana gerekli olmayan yerlerde zaman kaybettiğin görülüyor.", "tips": ["Okumaya başlamadan önce başlıklara ve alt başlıklara göz gezdir.", "Önemli yerlerin altını çiz veya işaretle.", "Her bölümden sonra dur ve okuduğunu kendi kelimelerinle özetle."]},
            "mid": {"range": (4, 7), "text": "Okurken önemli olanla olmayanı ayırmakta zaman zaman güçlük çektiğin anlaşılıyor.", "tips": ["SQ3R tekniğini dene: Gözden Geçir, Soru Sor, Oku, Tekrarla, Gözden Geçir.", "Şekil ve tabloları atlama — bunlar konuyu anlamana yardımcı olur."]},
            "low": {"range": (0, 3), "text": "Okuduğun metin içinde gerekli olanları ayırabildiğin anlaşılıyor. Süper! 🎉", "tips": []},
        },
    },
    "E": {
        "name": "Ödev Hazırlamak",
        "question_ids": [3, 25, 52, 63, 23, 26, 53],
        "max_score": 7,
        "interpretations": {
            "high": {"range": (5, 7), "text": "Günlük veya dönem ödevi hazırlamanın, konunun özünü kavramak için ne kadar önemli olduğunun farkında olmadığın görülüyor. Ödevlerden bir an önce kurtulma eğilimin başarını tehdit eden önemli bir engel.", "tips": ["Ödevi küçük parçalara böl ve her gün biraz yap.", "Başlamadan önce kısa bir plan yap.", "Ödevini bitirdikten sonra bir gün bekle, sonra tekrar oku ve düzelt."]},
            "mid": {"range": (3, 4), "text": "Ödevlerini gereği gibi hazırlamak ve düzenlemekte zaman zaman güçlük çektiğin anlaşılıyor.", "tips": ["Ödev takvimi oluştur ve son teslim tarihlerini takip et.", "En az bir ek kaynak kullanmayı alışkanlık haline getir."]},
            "low": {"range": (0, 2), "text": "Ödevlerin eğitim hayatı içindeki önemini kavramış olduğun anlaşılıyor. Harika! 🎉", "tips": []},
        },
    },
    "F": {
        "name": "Okula Karşı Tutum",
        "question_ids": [27, 35, 57, 68, 33, 36, 64, 69],
        "max_score": 8,
        "interpretations": {
            "high": {"range": (5, 8), "text": "Okula karşı tutumunun çalışmayı, öğrenmeyi ve başarılı olmayı güçleştirdiği görülüyor. Okul, eğitim ve öğretmenlerle ilgili temel düşüncelerini gözden geçirmen önemli.", "tips": ["Sevmediğin derslerde bile ilgini çekecek bir nokta bulmaya çalış.", "Öğretmenlerinle iletişimi kesmemeye çalış — sorunlarını paylaş.", "Okuldaki sosyal etkinliklere katıl."]},
            "mid": {"range": (3, 4), "text": "Okula karşı bazı olumsuz duygu ve düşünceler içinde olduğun görülüyor.", "tips": ["Okulda seni mutlu eden şeylerin bir listesini yap.", "Güvendiğin bir öğretmenle düşüncelerini paylaş."]},
            "low": {"range": (0, 2), "text": "Okula karşı olumlu bir tavır içinde olduğun görülüyor. Süper! 🎉", "tips": []},
        },
    },
    "G": {
        "name": "Sınavlara Hazırlanmak ve Sınava Girmek",
        "question_ids": [1, 9, 54, 65, 2, 21, 58, 66, 6, 41, 59],
        "max_score": 11,
        "interpretations": {
            "high": {"range": (8, 11), "text": "Sınavlarda başarılı olmanın, sınav öncesinde başlayan ve sınavda da devam eden bir işlemler dizisi olduğunun farkında değilsin. Eğer zaman zaman çalıştığın ölçüde başarılı olmadığından yakınıyorsan, sınava hazırlanma tekniklerini öğrenmek önemli.", "tips": ["Sınavdan en az 3 gün önce çalışmaya başla.", "Sınavda önce tüm soruları oku, kolaylardan başla.", "Sınav öncesi öğretmenin nelere önem verdiğini öğrenmeye çalış.", "Sınav sırasında sakin ol — derin nefes al ve kendine güven."]},
            "mid": {"range": (4, 7), "text": "Sınavlara hazırlanmak ve sınava girmek konusunda bir hayli bilgi ve tecrübe sahibi olsan da bazı eksiklerin olduğu görülüyor.", "tips": ["Sınav stratejilerini gözden geçir — zaman yönetimi çok önemli.", "Geçmiş sınav sorularını çözerek pratik yap."]},
            "low": {"range": (0, 3), "text": "Sınavlara hazırlanmak ve sınava girmek konusundaki teknik ve taktikleri oldukça iyi bildiğin ve bunları uyguladığın görülüyor. Muhteşem! 🎉", "tips": []},
        },
    },
}


def calculate_calisma_davranisi(answers):
    """
    Çalışma Davranışı puanlama — POZİTİF PUAN SİSTEMİ.
    Yüksek puan = iyi çalışma davranışı (ters çevrildi).
    """
    answers = {int(k): v for k, v in answers.items()}
    q_lookup = {q["id"]: q for q in CALISMA_DAVRANISI_QUESTIONS}

    category_scores = {}
    category_positive = {}  # Pozitif puanlar (yüksek = iyi)
    for cat_key, cat_info in CALISMA_DAVRANISI_CATEGORIES.items():
        wrong = 0
        for qid in cat_info["question_ids"]:
            question = q_lookup.get(qid)
            if question is None:
                continue
            student_answer = answers.get(qid)
            if student_answer is not None and student_answer != question["key"]:
                wrong += 1
        category_scores[cat_key] = wrong
        # Pozitif puan: max - wrong = doğru davranış sayısı
        category_positive[cat_key] = cat_info["max_score"] - wrong

    total_wrong = sum(category_scores.values())
    max_total = sum(c["max_score"] for c in CALISMA_DAVRANISI_CATEGORIES.values())
    total_positive = max_total - total_wrong
    positive_pct = round(total_positive / max_total * 100, 1) if max_total else 0

    # 5 kademe seviye sistemi
    if positive_pct >= 80:
        level, level_emoji = "Çok İyi", "🟢"
    elif positive_pct >= 65:
        level, level_emoji = "İyi", "🔵"
    elif positive_pct >= 45:
        level, level_emoji = "Orta", "🟡"
    elif positive_pct >= 25:
        level, level_emoji = "Gelişime Açık", "🟠"
    else:
        level, level_emoji = "Acil Destek", "🔴"

    scores_named = {CALISMA_DAVRANISI_CATEGORIES[k]["name"]: category_positive[k] for k, v in category_positive.items()}

    # Kategori kombinasyon analizi
    combinations = _detect_calisma_combinations(category_positive, CALISMA_DAVRANISI_CATEGORIES)

    scores = {
        "categories": category_scores,           # Eski format (geriye uyumluluk)
        "categories_positive": category_positive, # YENİ: Pozitif puanlar
        "categories_named": scores_named,
        "total": total_wrong,                     # Eski (geriye uyumluluk)
        "total_positive": total_positive,         # YENİ
        "max_total": max_total,
        "positive_pct": positive_pct,             # YENİ
        "level": level,                           # YENİ: 5 kademe
        "level_emoji": level_emoji,               # YENİ
        "combinations": combinations,             # YENİ: Kombinasyon yorumları
    }
    report = generate_calisma_davranisi_report(scores)
    return scores, report


def _detect_calisma_combinations(positive, categories):
    """Kategori kombinasyonlarından anlamlı örüntüleri tespit eder."""
    combos = []

    def pct(cat_key):
        mx = categories[cat_key]["max_score"]
        return round(positive[cat_key] / mx * 100) if mx else 0

    # Motivasyon yüksek + Planlama düşük = İstekli ama plansız
    if pct("F") >= 60 and pct("A") < 40:
        combos.append({
            "type": "istekli_plansiz",
            "title": "🔥 İstekli ama Plansız",
            "detail": "Okula karşı olumlu tutumun var ama çalışmaya başlama ve sürdürme konusunda zorluk yaşıyorsun. İyi haber: Motivasyonun güçlü — sadece planlama tekniklerini öğrenmen gerekiyor!",
            "tip": "Her gün aynı saatte 25 dakikalık çalışma blokları planla (Pomodoro tekniği).",
        })

    # Planlama iyi + Not tutma zayıf = Disiplinli ama verimsiz
    if pct("A") >= 60 and pct("C") < 40:
        combos.append({
            "type": "disiplinli_verimsiz",
            "title": "⏰ Disiplinli ama Verimsiz",
            "detail": "Çalışmaya başlayıp sürdürebiliyorsun — harika! Ama not tutma ve dersi dinleme tekniklerin zayıf. Harcadığın zamanın verimini artırabilirsin.",
            "tip": "Not tutma tekniklerini öğren: Cornell yöntemi, mind map veya bullet journal.",
        })

    # Okuma iyi + Sınav hazırlık kötü = Bilen ama sınavda gösteremeyen
    if pct("D") >= 60 and pct("G") < 40:
        combos.append({
            "type": "bilen_gosteremeyen",
            "title": "📚 Bilgili ama Sınavda Zorlanıyor",
            "detail": "Okuma ve anlama becerilerin güçlü ama sınava hazırlanma ve sınav stratejilerin zayıf. Bildiklerini sınavda gösteremiyorsun.",
            "tip": "Sınav stratejileri: Önce tüm soruları oku, kolaylardan başla, zamanı böl.",
        })

    # Motivasyon düşük + her şey düşük = Genel motivasyon sorunu
    if pct("F") < 35 and pct("A") < 35:
        combos.append({
            "type": "motivasyon_krizi",
            "title": "⚠️ Genel Motivasyon Sorunu",
            "detail": "Hem okula karşı tutumun hem de çalışma alışkanlıkların düşük. Bu genellikle geçici bir durum — doğru destekle hızla düzelebilir.",
            "tip": "Bir rehber öğretmen veya danışmanla konuş. Küçük, ulaşılabilir hedeflerle başla.",
        })

    # Ödev iyi + Motivasyon iyi = Güçlü temel
    if pct("E") >= 60 and pct("F") >= 60:
        combos.append({
            "type": "guclu_temel",
            "title": "🌟 Güçlü Temel!",
            "detail": "Hem ödev yapma alışkanlığın hem de okula karşı tutumun çok iyi. Bu seni başarıya taşıyacak güçlü bir zemin.",
            "tip": "Bu gücünü koruyarak diğer alanları da geliştirmeye odaklan.",
        })

    # Her şey yüksek = Mükemmel
    all_high = all(pct(k) >= 65 for k in ["A", "B", "C", "D", "E", "F", "G"])
    if all_high:
        combos.append({
            "type": "mukemmel",
            "title": "🏆 Mükemmel Çalışma Profili!",
            "detail": "Tüm çalışma davranışı alanlarında güçlüsün. Tebrikler!",
            "tip": "Bu alışkanlıkları sürdür ve arkadaşlarına da ilham ver.",
        })

    return combos


def generate_calisma_davranisi_report(scores):
    category_scores = scores["categories"]
    positive = scores.get("categories_positive", {})
    max_total = scores["max_total"]
    total_positive = scores.get("total_positive", max_total - scores["total"])
    positive_pct = scores.get("positive_pct", round(total_positive / max_total * 100, 1) if max_total else 0)
    level = scores.get("level", "Orta")
    level_emoji = scores.get("level_emoji", "🟡")

    # Genel durum mesajı (5 kademe)
    level_messages = {
        "Çok İyi": "Çalışma alışkanlıkların mükemmel düzeyde! Sen bir rol model olabilirsin. 🌟",
        "İyi": "Çalışma alışkanlıkların genel olarak iyi. Küçük iyileştirmelerle mükemmele ulaşabilirsin!",
        "Orta": "Bazı alanlarda güçlüsün, bazılarında gelişime açıksın. Doğru tekniklerle çok daha başarılı olabilirsin!",
        "Gelişime Açık": "Çalışma davranışlarında önemli gelişim alanları var. Ama bunların hepsi öğrenilebilen beceriler!",
        "Acil Destek": "Çalışma alışkanlıklarında acil destek ihtiyacı var. Endişelenme — doğru rehberlikle hızla gelişebilirsin!",
    }
    msg = level_messages.get(level, "")

    report = f"# 📊 ÇALIŞMA DAVRANIŞI DEĞERLENDİRME RAPORU\n\n"
    report += f"**Genel Durum:** {level_emoji} **{level}** — Doğru Davranış Puanı: {total_positive}/{max_total} (%{positive_pct})\n\n"
    report += f"{msg}\n\n---\n\n"

    # Kategori Özet Tablosu
    report += "## 📋 Kategori Özet Tablosu\n\n"
    report += "| Kategori | Puan | Seviye | Grafik |\n"
    report += "|----------|------|--------|--------|\n"

    strong, weak, mid_areas = [], [], []
    for cat_key in ["A", "B", "C", "D", "E", "F", "G"]:
        cat = CALISMA_DAVRANISI_CATEGORIES[cat_key]
        pos = positive.get(cat_key, cat["max_score"] - category_scores.get(cat_key, 0))
        pct = round(pos / cat["max_score"] * 100, 1) if cat["max_score"] else 0
        n = round(pct / 10)
        bar = "█" * n + "░" * (10 - n)
        if pct >= 65:
            sev = "🟢"
            strong.append(cat["name"])
        elif pct >= 40:
            sev = "🟡"
            mid_areas.append(cat["name"])
        else:
            sev = "🔴"
            weak.append(cat["name"])
        report += f"| {cat_key}. {cat['name']} | {pos}/{cat['max_score']} | {sev} %{pct} | {bar} |\n"
    report += "\n---\n\n"

    # Detaylı Kategori Analizi
    report += "## 📝 Detaylı Kategori Analizi\n\n"
    for cat_key in ["A", "B", "C", "D", "E", "F", "G"]:
        cat = CALISMA_DAVRANISI_CATEGORIES[cat_key]
        score = category_scores.get(cat_key, 0)
        pos = positive.get(cat_key, cat["max_score"] - score)
        pct = round(pos / cat["max_score"] * 100, 1) if cat["max_score"] else 0

        report += f"### {cat_key}. {cat['name']}\n"
        report += f"**Doğru Davranış Puanın:** {pos}/{cat['max_score']} (%{pct})\n\n"

        for lk, ld in cat["interpretations"].items():
            lo, hi = ld["range"]
            if lo <= score <= hi:
                report += ld["text"] + "\n\n"
                if ld["tips"]:
                    report += "**Sana Özel İpuçları:**\n" + "\n".join(f"- 💡 {t}" for t in ld["tips"]) + "\n\n"
                break
        report += "---\n\n"

    # Kombinasyon Yorumları
    combinations = scores.get("combinations", [])
    if combinations:
        report += "## 🔗 Profil Analizi — Kategoriler Arası Bağlantılar\n\n"
        for combo in combinations:
            report += f"### {combo['title']}\n"
            report += f"{combo['detail']}\n\n"
            report += f"**💡 Öneri:** {combo['tip']}\n\n"
        report += "---\n\n"

    # Güçlü/Zayıf Özet
    report += "## 🌟 Özet Profil\n\n"
    if strong:
        report += f"**💪 Güçlü Yönlerin:** {', '.join(strong)}\n\n"
    if mid_areas:
        report += f"**🎯 Geliştirebileceğin Alanlar:** {', '.join(mid_areas)}\n\n"
    if weak:
        report += f"**⚠️ Öncelikli Destek Alanların:** {', '.join(weak)}\n\n"

    # Ebeveyn Rehberi
    report += "---\n\n## 👨‍👩‍👦 Ebeveyn Rehberi\n\n"
    if weak:
        report += "**Yapmanız Gerekenler:**\n"
        report += "- ✅ Çocuğunuzla birlikte haftalık bir çalışma planı oluşturun\n"
        report += "- ✅ Küçük başarıları bile takdir edin — motivasyon için çok önemli\n"
        report += "- ✅ Düzenli bir çalışma ortamı sağlayın (sessiz, düzenli, iyi aydınlatılmış)\n\n"
        report += "**Kaçınmanız Gerekenler:**\n"
        report += "- ❌ Başka çocuklarla kıyaslamaktan kaçının\n"
        report += "- ❌ Uzun süre kesintisiz çalışmaya zorlamayın (25 dk çalış + 5 dk mola ideal)\n"
        report += "- ❌ Cezalandırma yerine ödüllendirme sistemi kullanın\n\n"
    else:
        report += "Çocuğunuzun çalışma alışkanlıkları güçlü görünüyor. Bu başarıyı desteklemeye devam edin!\n\n"

    # Öğretmen Notu
    report += "## 👩‍🏫 Öğretmen Notu\n\n"
    if weak:
        report += f"Bu öğrencinin öncelikli gelişim alanları: **{', '.join(weak)}**.\n"
        report += "Sınıf içinde bu alanlara yönelik destekleyici geri bildirimler ve kısa görevler faydalı olacaktır.\n\n"
    else:
        report += "Bu öğrenci çalışma davranışları konusunda güçlü bir profile sahip. Akran desteği veya liderlik rolleri verilebilir.\n\n"

    report += "\n## 💬 Son Söz\nUnutma, çalışma davranışları doğuştan gelen değil, **öğrenilebilen** becerilerdir! Sen bunu yapabilirsin! 🚀"
    return report.strip()


# ============================================================
# BÖLÜM 3: SINAV KAYGISI ÖLÇEĞİ
# ============================================================

SINAV_KAYGISI_QUESTIONS = [
    {"id": 1,  "text": "Sınava girmeden de sınıf geçmenin ve başarılı olmanın bir yolu olmasını isterdim."},
    {"id": 2,  "text": "Bir sınavda başarılı olmak, diğer sınavlarda kendime güvenimin artmasına yardımcı olmaz."},
    {"id": 3,  "text": "Çevremizdekiler (ailem, arkadaşlarım) başaracağım konusunda bana güveniyorlar."},
    {"id": 4,  "text": "Bir sınav sırasında bazen zihnimin sınavla ilgili olmayan konulara kaydığını hissediyorum."},
    {"id": 5,  "text": "Önemli bir sınavdan önce veya sonra canım bir şey yemek istemez."},
    {"id": 6,  "text": "Öğretmenin sık sık küçük yazılı veya sözlü yoklamalar yaptığı derslerden nefret ederim."},
    {"id": 7,  "text": "Sınavların mutlaka resmi, ciddi ve gerginlik yaratan durumlar olması gerekmez."},
    {"id": 8,  "text": "Sınavlarda başarılı olanlar çoğunlukla hayatta da iyi pozisyonlara gelirler."},
    {"id": 9,  "text": "Önemli bir sınavdan önce veya sınav sırasında bazı arkadaşlarımın çalışırken daha az zorlandıklarını ve benden daha akıllı olduklarını düşünürüm."},
    {"id": 10, "text": "Eğer sınavlar olmasaydı dersleri daha iyi öğreneceğimden eminim."},
    {"id": 11, "text": "Ne kadar başarılı olacağım konusundaki endişeler, sınava hazırlığımı ve sınav başarımı etkiler."},
    {"id": 12, "text": "Önemli bir sınava girecek olmam uykularımı bozar."},
    {"id": 13, "text": "Sınav sırasında çevremdeki insanların gezinmesi ve bana bakmalarından endişe duyarım."},
    {"id": 14, "text": "Her zaman düşünmesem de başarısız olursam çevremdekilerinin bana hangi gözle bakacakları konusunda endişelenirim."},
    {"id": 15, "text": "Geleceğimin sınavlarda göstereceğim başarıya bağlı olması beni üzüyor."},
    {"id": 16, "text": "Kendimi bir toplayabilsem, birçok kişiden daha iyi not alacağımı biliyorum."},
    {"id": 17, "text": "Başarısız olursam, insanlar benim yeteneğimden şüpheye düşecekler."},
    {"id": 18, "text": "Hiçbir zaman sınavlara tam olarak hazırlandığım duygusunu yaşayamam."},
    {"id": 19, "text": "Bir sınavdan önce bir türlü gevşeyemem."},
    {"id": 20, "text": "Önemli sınavlardan önce zihnim adeta durur kalır."},
    {"id": 21, "text": "Bir sınav sırasında dışarıdan gelen gürültüler, çevremdekilerinin çıkardıkları sesler, ışık, oda sıcaklığı vb. beni rahatsız eder."},
    {"id": 22, "text": "Sınavdan önce daima huzursuz, gergin ve sıkıntılı olurum."},
    {"id": 23, "text": "Sınavların insanın gelecekteki amaçlarına ulaşması konusunda ölçü olmasına hayret ederim."},
    {"id": 24, "text": "Sınavlar insanın gerçekten ne kadar bildiğini göstermez."},
    {"id": 25, "text": "Düşük not aldığımda, hiç kimseye notumu söyleyemem."},
    {"id": 26, "text": "Bir sınavdan önce çoğunlukla içimden bağırmak gelir."},
    {"id": 27, "text": "Önemli sınavlardan önce midem bulanır."},
    {"id": 28, "text": "Önemli bir sınava çalışırken çok kere olumsuz düşüncelerle peşin bir yenilgiyi yaşarım."},
    {"id": 29, "text": "Sınav sonuçlarını almadan önce kendimi çok endişeli ve huzursuz hissederim."},
    {"id": 30, "text": "Sınava başlarken, bir sınav veya teste ihtiyaç duyulmayan bir işe girebilmeyi çok isterim."},
    {"id": 31, "text": "Bir sınavda başarılı olamazsam, zaman zaman zannettiğim kadar akıllı olmadığımı düşünürüm."},
    {"id": 32, "text": "Eğer kırık not alırsam, annem ve babam müthiş hayal kırıklığına uğrar."},
    {"id": 33, "text": "Sınavlarla ilgili endişelerim çoğunlukla tam olarak hazırlanmamı engeller ve bu durum beni daha çok endişelendirir."},
    {"id": 34, "text": "Sınav sırasında, bacağımı salladığımı, parmaklarımı sıraya vurduğumu fark ediyorum."},
    {"id": 35, "text": "Bir sınavdan sonra çoğunlukla yapmış olduğumdan daha iyi yapabileceğimi düşünürüm."},
    {"id": 36, "text": "Bir sınav sırasında duygularım dikkatimin dağılmasına sebep olur."},
    {"id": 37, "text": "Bir sınava ne kadar çok çalışırsam, o kadar çok karıştırıyorum."},
    {"id": 38, "text": "Başarısız olursam, kendimle ilgili görüşlerim değişir."},
    {"id": 39, "text": "Bir sınav sırasında bedenimin belirli yerlerindeki kaslar kasılır."},
    {"id": 40, "text": "Bir sınavdan önce ne kendime tam olarak güvenebilirim, ne de zihinsel olarak gevşeyebilirim."},
    {"id": 41, "text": "Başarısız olursam arkadaşlarımın gözünde değerimin düşeceğini biliyorum."},
    {"id": 42, "text": "Önemli problemlerimden biri, bir sınava tam olarak hazırlanıp hazırlanmadığımı bilmemektir."},
    {"id": 43, "text": "Gerçekten önemli bir sınava girerken çoğunlukla bedensel olarak panik içinde olurum."},
    {"id": 44, "text": "Testi değerlendirenlerin bazı öğrencilerin sınavda çok heyecanlandıklarını bilmelerini ve bunu testi değerlendirirken hesaba katmalarını isterdim."},
    {"id": 45, "text": "Sınıf geçmek için sınava girmektense ödev hazırlamayı tercih ederim."},
    {"id": 46, "text": "Kendi notumu söylemeden önce arkadaşlarımın kaç aldığını bilmek isterim."},
    {"id": 47, "text": "Kırık not aldığım zaman, tanıdığım bazı insanların benimle alay edeceğini biliyorum ve bu beni rahatsız ediyor."},
    {"id": 48, "text": "Eğer sınavlara yalnız başıma girsem ve zamanla sınırlanmamış olsam daha başarılı olacağımı düşünüyorum."},
    {"id": 49, "text": "Sınavdaki sonuçların hayat başarım ve güvenliğimle doğrudan ilgili olduğunu düşünürüm."},
    {"id": 50, "text": "Sınavlar sırasında bazen gerçekten bildiklerimi unutacak kadar heyecanlanıyorum."},
]

# DÜZELTME: Soru 3 ters madde.
# "Çevremizdekiler başaracağım konusunda bana güveniyorlar." — OLUMLU ifade.
# D = "Evet, güveniyorlar" = kaygı YOK → 0 puan.
# Y = "Hayır, güvenmiyorlar" = kaygı VAR → 1 puan.
SINAV_KAYGISI_TERS_MADDELER = {3}

SINAV_KAYGISI_CATEGORIES = {
    "baskalari_gorusu": {
        "name": "Başkalarının Sizi Nasıl Gördüğü ile İlgili Endişeler", "icon": "👥",
        "question_ids": [14, 17, 25, 32, 41, 46, 47],
        "max_score": 7,
        "interpretations": {
            "high": {"range": (5, 7), "text": "Başkalarının seni nasıl gördüğü senin için büyük önem taşıyor. Çevrendeki insanların değerlendirmeleri sınav durumunda zihinsel faaliyetini olumsuz etkiliyor.", "tips": ["Unutma: Sınavda ölçülen senin bilgin, kişiliğin veya değerin değil!", "Herkesin farklı güçlü yönleri var — kendini başkalarıyla kıyaslama.", "Güvendiğin birisiyle bu endişelerini paylaş."]},
            "mid": {"range": (3, 4), "text": "Başkalarının görüşleri seni bir miktar etkiliyor. Bu normal bir seviyede ama dikkat etmekte fayda var.", "tips": ["Kendi başarı ölçütlerini belirle — başkalarının standartları değil, seninkiler önemli.", "Küçük başarılarını fark et ve kutla."]},
            "low": {"range": (0, 2), "text": "Başkalarının seninle ilgili görüşleri seni fazla etkilemiyor. Gereksiz zaman ve enerji kaybetmiyorsun. Harika! 🎉", "tips": []},
        },
    },
    "kendi_gorusu": {
        "name": "Kendinizi Nasıl Gördüğünüzle İlgili Endişeler", "icon": "🪞",
        "question_ids": [2, 9, 16, 24, 31, 38, 40],
        "max_score": 7,
        "interpretations": {
            "high": {"range": (5, 7), "text": "Sınavlardaki başarınla kendinize olan saygını eşdeğer görüyorsun. Sınavlarda ölçülenin kişilik değerin değil, bilgi düzeyin olduğunu kabullenmek sana yardımcı olacaktır.", "tips": ["Sınav sonucu senin değerini belirlemez — bunu kendine sık sık hatırlat.", "Başarısızlık bir son değil, öğrenme fırsatıdır.", "Güçlü yönlerinin bir listesini yap ve zor anlarda oku."]},
            "mid": {"range": (3, 4), "text": "Sınav sonuçları öz güvenini kısmen etkiliyor. Sınavla kişisel değerini ayırt edebiliyorsun ama zaman zaman zorlanıyorsun.", "tips": ["Sınav dışı başarılarını da hatırla — spor, sanat, arkadaşlık gibi.", "Her sınavdan sonra 'ne öğrendim?' diye sor, 'kaç aldım?' yerine."]},
            "low": {"range": (0, 2), "text": "Sınavlardaki başarınla kendi kişiliğine verdiğin değeri birbirinden oldukça iyi ayırabildiğin anlaşılıyor. Süper! 🎉", "tips": []},
        },
    },
    "gelecek_endisesi": {
        "name": "Gelecekle İlgili Endişeler", "icon": "🔮",
        "question_ids": [1, 8, 15, 23, 30, 49],
        "max_score": 6,
        "interpretations": {
            "high": {"range": (4, 6), "text": "Sınavlardaki başarını gelecekteki mutluluğunun ve başarının tek ölçüsü olarak görüyorsun. Bu yaklaşım bilgini yeterince ortaya koymayı güçleştiriyor.", "tips": ["Hayatta başarılı olmanın birçok yolu var — sınav bunlardan sadece biri.", "Bugüne odaklan: 'Şimdi ne yapabilirim?' diye sor.", "Sınavları bir tehdit değil, geçilmesi gereken basamaklar olarak gör."]},
            "mid": {"range": (2, 3), "text": "Gelecekle ilgili bazı endişelerin var ama bunlar henüz kontrol dışına çıkmamış durumda.", "tips": ["Kısa vadeli hedefler koy — uzak gelecek yerine 'bu hafta ne yapabilirim?' diye düşün.", "Başarılı insanların hikayelerini oku — çoğunun yolu doğrusal değildi."]},
            "low": {"range": (0, 1), "text": "Gelecekteki mutluluğunun tek belirleyicisinin sınavlar olmadığının farkındasın. Harika! 🎉", "tips": []},
        },
    },
    "hazirlik_endisesi": {
        "name": "Yeterince Hazırlanamamakla İlgili Endişeler", "icon": "📖",
        "question_ids": [6, 11, 18, 26, 33, 42],
        "max_score": 6,
        "interpretations": {
            "high": {"range": (4, 6), "text": "Sınavları kişiliğin ve gelecekteki güvenliğinin bir ölçüsü olarak gördüğün için herhangi bir sınava hazırlık dönemi senin için bir kriz dönemi olabiliyor.", "tips": ["Sınava en az 3 gün öncesinden çalışmaya başla.", "Çalışma planı yap — neyi, ne zaman çalışacağını belirle.", "Çalıştıktan sonra kendini test et — hazır olduğunu görmek güven verir."]},
            "mid": {"range": (2, 3), "text": "Sınav hazırlığında bazen endişe yaşıyorsun ama genel olarak baş edebiliyorsun.", "tips": ["Çalışma planını yazıya dök — görünür bir plan güven verir.", "Sınav öncesi küçük testler çözerek hazırlık seviyeni ölç."]},
            "low": {"range": (0, 1), "text": "Sınavlara büyük bir gerginlik hissetmeden hazırlanıyorsun. Tebrikler! 🎉", "tips": []},
        },
    },
    "bedensel_tepkiler": {
        "name": "Bedensel Tepkiler", "icon": "💪",
        "question_ids": [5, 12, 19, 27, 34, 39, 43],
        "max_score": 7,
        "interpretations": {
            "high": {"range": (5, 7), "text": "Sınava hazırlanırken iştahsızlık, uykusuzluk, gerginlik gibi birçok bedensel rahatsızlıkla mücadele etmek zorunda kaldığın anlaşılıyor.", "tips": ["Derin nefes egzersizleri yap: 4 saniye nefes al, 4 saniye tut, 4 saniye ver.", "Sınavdan önce hafif egzersiz yap (yürüyüş, germe hareketleri).", "Düzenli uyku çok önemli — sınav gecesi erken yat."]},
            "mid": {"range": (3, 4), "text": "Bazı bedensel belirtiler yaşıyorsun ama bunlar henüz ciddi düzeyde değil.", "tips": ["Stresli dönemlerde fiziksel aktiviteyi artır.", "Düzenli beslenme ve uyku rutini oluştur."]},
            "low": {"range": (0, 2), "text": "Sınava hazırlık sırasında heyecanını kontrol edebildiğin anlaşılıyor. Çok iyi! 🎉", "tips": []},
        },
    },
    "zihinsel_tepkiler": {
        "name": "Zihinsel Tepkiler", "icon": "🧠",
        "question_ids": [4, 13, 20, 21, 28, 35, 36, 37, 48, 50],
        "max_score": 10,
        "interpretations": {
            "high": {"range": (7, 10), "text": "Sınava hazırlanırken veya sınav sırasında çevrende olan bitenden fazlasıyla etkilendiğin ve dikkatini toplamakta ciddi güçlük çektiğin görülüyor.", "tips": ["Dikkatini toplama egzersizleri yap (mindfulness, meditasyon).", "Sınav sırasında olumsuz düşünceler geldiğinde 'DUR' de ve nefes al.", "Pozitif iç konuşma yap: 'Ben bunu yapabilirim, hazırlandım.'"]},
            "mid": {"range": (4, 6), "text": "Bazen dikkat dağınıklığı ve olumsuz düşünceler yaşıyorsun ama tamamen kontrol dışı değil.", "tips": ["Sınav öncesi 5 dakika sessizce otur ve zihnini topla.", "Olumsuz düşünceleri yazıya dök — yazınca güçlerini kaybederler."]},
            "low": {"range": (0, 3), "text": "Zihinsel açıdan sınava hazırlanırken önemli bir rahatsızlık yaşamadığın görülüyor. Muhteşem! 🎉", "tips": []},
        },
    },
    "genel_kaygi": {
        "name": "Genel Sınav Kaygısı", "icon": "📋",
        "question_ids": [7, 10, 22, 29, 44, 45],
        "max_score": 6,
        "interpretations": {
            "high": {"range": (4, 6), "text": "Sınavlarda kendine güvenemediğin, sınavları varlığın ve geleceğin için bir tehdit olarak gördüğün anlaşılıyor. Sınav kaygını azaltacak teknikleri öğrenmen hem eğitim başarını yükseltecek hem de hayattan aldığın zevki artıracaktır.", "tips": ["Sınavı bir savaş değil, bir oyun gibi düşün — stratejini belirle ve oyna.", "Geçmiş başarılarını hatırla — daha önce de sınavları geçtin.", "Sınav sonrası kendini ödüllendir."]},
            "mid": {"range": (2, 3), "text": "Genel sınav kaygın orta düzeyde. Bazı sınavlarda daha çok gerginlik hissediyor olabilirsin.", "tips": ["Her sınav için kısa bir strateji planı yap.", "Sınavdan önce güzel bir aktivite yap — kendini iyi hissetmen performansı artırır."]},
            "low": {"range": (0, 1), "text": "Genel olarak sınavlara karşı sağlıklı bir tutum içinde olduğun anlaşılıyor. Süper! 🎉", "tips": []},
        },
    },
}


def calculate_sinav_kaygisi(answers):
    """
    Sınav Kaygısı puanlama — 5 kademe + baskın kaygı tipi.
    """
    answers = {int(k): v for k, v in answers.items()}

    category_scores = {}
    for cat_key, cat_info in SINAV_KAYGISI_CATEGORIES.items():
        score = 0
        for qid in cat_info["question_ids"]:
            ans = answers.get(qid)
            if ans is None:
                continue
            if qid in SINAV_KAYGISI_TERS_MADDELER:
                if ans == "Y":
                    score += 1
            else:
                if ans == "D":
                    score += 1
        category_scores[cat_key] = score

    total     = sum(category_scores.values())
    max_total = sum(c["max_score"] for c in SINAV_KAYGISI_CATEGORIES.values())
    total_pct = round(total / max_total * 100, 1) if max_total else 0

    # 5 kademe seviye sistemi
    if total_pct >= 75:
        overall, level_emoji = "Çok Yüksek", "🔴"
    elif total_pct >= 55:
        overall, level_emoji = "Yüksek", "🟠"
    elif total_pct >= 35:
        overall, level_emoji = "Orta", "🟡"
    elif total_pct >= 15:
        overall, level_emoji = "Düşük", "🔵"
    else:
        overall, level_emoji = "Çok Düşük", "🟢"

    # Baskın kaygı tipi profili
    anxiety_types = {
        "bedensel": {
            "categories": ["bedensel_tepkiler"],
            "name": "Bedensel Kaygı",
            "icon": "💪",
            "description": "Kaygın ağırlıklı olarak bedensel belirtilerle kendini gösteriyor: kas gerginliği, mide bulantısı, uykusuzluk.",
            "strategy": "Fiziksel rahatlama teknikleri (derin nefes, kas gevşetme, hafif egzersiz) en etkili yöntem.",
        },
        "bilissel": {
            "categories": ["zihinsel_tepkiler", "hazirlik_endisesi"],
            "name": "Bilişsel Kaygı",
            "icon": "🧠",
            "description": "Kaygın ağırlıklı olarak düşünce düzeyinde yaşanıyor: dikkat dağınıklığı, olumsuz düşünceler, konsantrasyon güçlüğü.",
            "strategy": "Bilişsel teknikler (pozitif iç konuşma, düşünce durdurma, görselleştirme) en etkili yöntem.",
        },
        "sosyal": {
            "categories": ["baskalari_gorusu", "kendi_gorusu"],
            "name": "Sosyal Kaygı",
            "icon": "👥",
            "description": "Kaygın ağırlıklı olarak başkalarının seni nasıl göreceği endişesinden kaynaklanıyor.",
            "strategy": "Öz-değer çalışması (başarıyı kişilikten ayırma, güçlü yönlere odaklanma) en etkili yöntem.",
        },
    }

    type_scores = {}
    for atype, info in anxiety_types.items():
        atype_total = sum(category_scores.get(c, 0) for c in info["categories"])
        atype_max = sum(SINAV_KAYGISI_CATEGORIES[c]["max_score"] for c in info["categories"])
        type_scores[atype] = round(atype_total / max(atype_max, 1) * 100, 1)

    dominant_type = max(type_scores, key=type_scores.get)
    dominant_info = anxiety_types[dominant_type]

    scores_named = {SINAV_KAYGISI_CATEGORIES[k]["name"]: v for k, v in category_scores.items()}

    scores = {
        "categories": category_scores,
        "categories_named": scores_named,
        "total": total, "max_total": max_total,
        "total_pct": total_pct, "overall_level": overall,
        "level_emoji": level_emoji,
        "dominant_type": dominant_type,
        "dominant_info": dominant_info,
        "type_scores": type_scores,
    }
    report = generate_sinav_kaygisi_report(scores)
    return scores, report


def generate_sinav_kaygisi_report(scores):
    category_scores = scores["categories"]
    total     = scores["total"]
    max_total = scores["max_total"]
    total_pct = scores["total_pct"]
    overall   = scores["overall_level"]
    level_emoji = scores.get("level_emoji", "🟡")

    # 5 kademe mesajlar
    level_messages = {
        "Çok Yüksek": "Sınav kaygın çok yüksek düzeyde. Bu kesinlikle üstesinden gelinebilir — doğru tekniklerle kısa sürede büyük fark yaratabilirsin!",
        "Yüksek": "Sınav kaygın yüksek görünüyor. Ama endişelenme — bu çok yaygın bir durum ve başa çıkmak tamamen mümkün!",
        "Orta": "Belirli düzeyde sınav kaygın var. Bu aslında performansını destekleyebilecek sağlıklı bir seviye — ama dikkat etmekte fayda var.",
        "Düşük": "Sınav kaygın düşük seviyede. Sınavlara karşı sağlıklı bir tutum içindesin!",
        "Çok Düşük": "Sınav kaygın çok düşük — sınavlara karşı son derece rahat bir tutumun var! 🎉",
    }
    msg = level_messages.get(overall, "")

    report = f"# 📝 SINAV KAYGISI DEĞERLENDİRME RAPORU\n\n"
    report += f"**Genel Kaygı Düzeyin:** {level_emoji} **{overall}** ({total}/{max_total} — %{total_pct})\n\n"
    report += f"{msg}\n\n"

    # Yerkes-Dodson notu
    if overall == "Orta":
        report += "> 💡 **Biliyor muydun?** Araştırmalar, orta düzeyde bir kaygının aslında performansı artırdığını gösteriyor (Yerkes-Dodson Yasası). Kaygın seni motive ediyor ama kontrol dışına çıkmasına izin vermemelisin.\n\n"

    report += "---\n\n"

    # Baskın Kaygı Tipi Profili
    dominant_info = scores.get("dominant_info", {})
    type_scores = scores.get("type_scores", {})
    if dominant_info and total_pct >= 20:
        report += f"## 🎯 Baskın Kaygı Tipin: {dominant_info.get('icon', '')} {dominant_info.get('name', '')}\n\n"
        report += f"{dominant_info.get('description', '')}\n\n"
        report += f"**En Etkili Başa Çıkma Yöntemi:** {dominant_info.get('strategy', '')}\n\n"

        report += "**Kaygı Tipi Dağılımın:**\n\n"
        report += "| Tip | Düzey |\n|-----|-------|\n"
        type_names = {"bedensel": "💪 Bedensel", "bilissel": "🧠 Bilişsel", "sosyal": "👥 Sosyal"}
        for tkey, tpct in sorted(type_scores.items(), key=lambda x: x[1], reverse=True):
            n = round(tpct / 10)
            bar = "█" * n + "░" * (10 - n)
            report += f"| {type_names.get(tkey, tkey)} | {bar} %{tpct} |\n"
        report += "\n---\n\n"

    # Alt Boyut Sonuçları (artık 3 kademeli)
    report += "## 📊 Alt Boyut Sonuçların\n\n"

    strong, weak, mid_areas = [], [], []
    order = ["baskalari_gorusu", "kendi_gorusu", "gelecek_endisesi",
             "hazirlik_endisesi", "bedensel_tepkiler", "zihinsel_tepkiler", "genel_kaygi"]
    for cat_key in order:
        cat   = SINAV_KAYGISI_CATEGORIES[cat_key]
        score = category_scores.get(cat_key, 0)
        pct   = round(score / cat["max_score"] * 100, 1) if cat["max_score"] else 0
        n = round(pct / 10)
        bar = "█" * n + "░" * (10 - n)
        report += f"### {cat['icon']} {cat['name']}\n**Puanın:** {score}/{cat['max_score']} ({bar} %{pct})\n\n"
        matched = False
        for lk in ["high", "mid", "low"]:
            ld = cat["interpretations"].get(lk)
            if ld is None:
                continue
            lo, hi = ld["range"]
            if lo <= score <= hi:
                report += ld["text"] + "\n\n"
                if ld["tips"]:
                    report += "**Sana Özel Öneriler:**\n" + "\n".join(f"- 💡 {t}" for t in ld["tips"]) + "\n\n"
                if lk == "low":
                    strong.append(cat["name"])
                elif lk == "high":
                    weak.append(cat["name"])
                else:
                    mid_areas.append(cat["name"])
                matched = True
                break
        if not matched:
            # Fallback for scores between ranges
            report += "Bu alanda orta düzeyde bir kaygı belirtisi görülüyor.\n\n"
            mid_areas.append(cat["name"])
        report += "---\n\n"

    # Özet
    report += "## 🌟 Özet Profil\n\n"
    if strong:
        report += f"**💪 Güçlü Yönlerin:** {', '.join(strong)}\n\n"
    if mid_areas:
        report += f"**🎯 Dikkat Edilmesi Gerekenler:** {', '.join(mid_areas)}\n\n"
    if weak:
        report += f"**⚠️ Üzerinde Çalışman Gereken Alanlar:** {', '.join(weak)}\n\n"

    # Pratik Baş Etme Teknikleri
    if total_pct >= 35:
        report += "---\n\n## 🛠️ Pratik Baş Etme Teknikleri\n\n"
        report += "### 🫁 Nefes Tekniği (4-7-8)\n"
        report += "4 saniye burundan nefes al → 7 saniye tut → 8 saniye ağızdan ver. Sınav öncesi 3 kez tekrarla.\n\n"
        report += "### 🧠 Düşünce Durdurma\n"
        report += "Olumsuz düşünce geldiğinde zihninde 'DUR!' de. Sonra yerine olumlu bir düşünce koy: 'Ben hazırlandım, yapabilirim.'\n\n"
        report += "### 🎬 Görselleştirme\n"
        report += "Sınavdan önce gözlerini kapat ve kendini sakin, güvenli bir şekilde soruları çözerken hayal et. 2 dakika yeterli.\n\n"
        report += "### 📝 Kaygı Günlüğü\n"
        report += "Her sınavdan önce endişelerini kağıda yaz. Araştırmalar, yazmanın kaygıyı %20'ye kadar azalttığını gösteriyor.\n\n"

    # Ebeveyn Rehberi
    report += "---\n\n## 👨‍👩‍👦 Ebeveyn Rehberi\n\n"
    if total_pct >= 55:
        report += "**Yapmanız Gerekenler:**\n"
        report += "- ✅ Çocuğunuzun kaygısını ciddiye alın — 'Boş ver, bir şey olmaz' demeyin\n"
        report += "- ✅ Sınav sonucuna değil, çabaya odaklanın: 'Ne kadar çalıştın?' sorusu 'Kaç aldın?' dan daha önemli\n"
        report += "- ✅ Fiziksel rahatlama tekniklerini birlikte pratik edin\n"
        report += "- ✅ Gerekirse okul rehberlik servisinden destek isteyin\n\n"
        report += "**Kaçınmanız Gerekenler:**\n"
        report += "- ❌ 'Ben senin yaşında çok daha çalışkandım' gibi kıyaslamalar\n"
        report += "- ❌ Sınav sonuçlarını ödül/ceza sistemiyle ilişkilendirme\n"
        report += "- ❌ Aşırı beklenti yükleme veya baskı\n\n"
    else:
        report += "Çocuğunuzun sınav kaygısı kontrol altında görünüyor. Mevcut destekleyici tutumunuzu sürdürün!\n\n"

    # Öğretmen Notu
    report += "## 👩‍🏫 Öğretmen Notu\n\n"
    if total_pct >= 55:
        report += f"Bu öğrenci yüksek sınav kaygısı yaşıyor. Baskın kaygı tipi: **{dominant_info.get('name', 'Belirtilmemiş')}**.\n"
        report += "Sınav ortamında ek süre, destekleyici geri bildirim ve başarı deneyimleri yaşatma önerilir.\n\n"
    elif total_pct >= 35:
        report += "Bu öğrencinin sınav kaygısı orta düzeyde. Sınav öncesi kısa motivasyon cümleleri faydalı olacaktır.\n\n"
    else:
        report += "Bu öğrenci sınavlara karşı sağlıklı bir tutum sergiliyor.\n\n"

    report += "\n## 💬 Son Söz\nSınav kaygısı çok yaygın bir durumdur ve başa çıkmak tamamen mümkündür! Sen bunu başarabilirsin! 💪"
    return report.strip()

# ============================================================
# BÖLÜM 4: ÇOKLU ZEKÂ TESTİ (GARDNER)
# ============================================================

COKLU_ZEKA_DATA = {
    "sozel":     {"name": "Sözel-Dilsel Zekâ",           "icon": "📝", "description": "Kelimelerle düşünme, dili etkili kullanma ve iletişim kurma yeteneğin çok güçlü!", "strengths": ["Güçlü okuma ve yazma becerileri", "Zengin kelime hazinesi", "İyi bir hikaye anlatıcısı", "Dillere yatkınlık", "İkna edici konuşma"], "study_tips": ["Konuları kendi kelimelerinle özetleyerek çalış.", "Sesli okuma ve anlatma yöntemini kullan.", "Günlük veya blog yazarak öğrendiklerini pekiştir.", "Kelime oyunları ve bulmacalar çöz."], "careers": ["Yazar", "Gazeteci", "Avukat", "Öğretmen", "Çevirmen", "Editör", "Diplomat"]},
    "mantiksal": {"name": "Mantıksal-Matematiksel Zekâ", "icon": "🔢", "description": "Sayılarla, mantıkla ve sistemli düşünmeyle arası çok iyi olan bir zihne sahipsin!", "strengths": ["Güçlü analitik düşünme", "Problem çözme becerisi", "Sayısal yetenekler", "Sebep-sonuç ilişkisi kurma", "Bilimsel merak"], "study_tips": ["Konuları mantıksal sıraya koyarak çalış.", "Formüller, grafikler ve tablolar oluştur.", "Neden-sonuç ilişkilerini sorgulayarak öğren.", "Matematik ve bilim problemleri çözerek pratik yap."], "careers": ["Mühendis", "Bilim İnsanı", "Programcı", "Doktor", "Ekonomist", "Muhasebeci", "Matematikçi"]},
    "gorsel":    {"name": "Görsel-Uzamsal Zekâ",          "icon": "🎨", "description": "Dünyayı görsellerle, renklerle ve şekillerle algılayan çok güçlü bir hayal gücün var!", "strengths": ["Güçlü görsel hafıza", "Zengin hayal gücü", "Renk ve tasarım duyarlılığı", "Mekânsal algılama", "Resim ve çizim yeteneği"], "study_tips": ["Zihin haritaları (mind map) çizerek çalış.", "Renkli kalemler ve görsel notlar kullan.", "Konuları şema ve diyagramlarla öğren.", "Video ve görsel materyallerden yararlan."], "careers": ["Mimar", "Grafik Tasarımcı", "Fotoğrafçı", "Ressam", "İç Mimar", "Pilot", "Cerrah"]},
    "muziksel":  {"name": "Müziksel-Ritmik Zekâ",         "icon": "🎵", "description": "Müziğe, ritimlere ve seslere karşı özel bir duyarlılığın var — bu harika bir yetenek!", "strengths": ["Ritim ve melodi duyarlılığı", "Müzikal hafıza", "Ses tonu ayrımı", "Müzik aletlerine yatkınlık", "Ritmik hareket becerisi"], "study_tips": ["Ders çalışırken fon müziği dinle (sözsüz).", "Öğrendiğin bilgileri şarkı veya kafiye haline getir.", "Ritmik tekrarlarla ezberle.", "Sesli çalışma yöntemini kullan."], "careers": ["Müzisyen", "Besteci", "Ses Mühendisi", "DJ", "Müzik Öğretmeni", "Şarkıcı", "Orkestra Şefi"]},
    "dogaci":    {"name": "Doğacı Zekâ",                   "icon": "🌿", "description": "Doğaya, hayvanlara ve çevreye karşı derin bir ilgi ve duyarlılığın var!", "strengths": ["Doğa sevgisi ve çevre bilinci", "Canlıları gözlemleme yeteneği", "Sınıflandırma becerisi", "Çevre duyarlılığı", "Mevsim ve iklim farkındalığı"], "study_tips": ["Mümkünse açık havada ders çalış.", "Doğa gözlemleri yaparak konuları somutlaştır.", "Sınıflandırma ve gruplama yöntemlerini kullan.", "Belgeseller izleyerek öğren."], "careers": ["Biyolog", "Veteriner", "Çevre Mühendisi", "Botanikçi", "Zoolog", "Ormancı", "Ekolog"]},
    "sosyal":    {"name": "Sosyal (Kişilerarası) Zekâ",    "icon": "🤝", "description": "İnsanlarla iletişim kurma, liderlik etme ve empati yapma konusunda çok yeteneklisin!", "strengths": ["Güçlü empati yeteneği", "Liderlik becerisi", "İletişim gücü", "İşbirliği yapabilme", "İnsanları anlama ve yönlendirme"], "study_tips": ["Grup çalışmaları ve tartışmalarla öğren.", "Öğrendiğin konuları arkadaşlarına anlat.", "Rol yapma ve canlandırma yöntemlerini dene.", "Çalışma grupları oluştur."], "careers": ["Psikolog", "Öğretmen", "İnsan Kaynakları Uzmanı", "Sosyal Hizmet Uzmanı", "Politikacı", "Satış Uzmanı"]},
    "bedensel":  {"name": "Bedensel-Kinestetik Zekâ",      "icon": "⚽", "description": "Bedenini çok iyi kullanıyorsun — hareket, spor ve el becerileri senin süper gücün!", "strengths": ["Güçlü beden koordinasyonu", "Sportif yetenek", "El becerileri", "Yaparak öğrenme", "Fiziksel ifade gücü"], "study_tips": ["Yaparak ve deneyerek öğren — laboratuvar, atölye çalışmaları.", "Ders çalışırken yürüyerek veya hareket ederek tekrar yap.", "Not alırken, çizerek ve yazarak çalış.", "Kısa aralarla aktif molalar ver."], "careers": ["Sporcu", "Cerrah", "Dansçı", "Fizyoterapist", "Teknisyen", "Heykeltıraş", "Aşçı"]},
    "icsel":     {"name": "İçsel (Özedönük) Zekâ",          "icon": "🧘", "description": "Kendini çok iyi tanıyorsun — güçlü ve zayıf yönlerinin farkındasın, bu çok değerli!", "strengths": ["Öz farkındalık", "Bağımsız çalışma becerisi", "Kendine güven", "Duygusal olgunluk", "Hedef belirleme ve motivasyon"], "study_tips": ["Bireysel çalışma sana daha uygun — sessiz ortamlar tercih et.", "Kendi kendine hedefler koy ve takip et.", "Günlük tut, öğrenme sürecini değerlendir.", "Meditasyon ve düşünce egzersizleri yap."], "careers": ["Psikolog", "Filozof", "Yazar", "Araştırmacı", "Girişimci", "Danışman", "Sanatçı"]},
}

ZEKA_SIRA = ["sozel", "mantiksal", "gorsel", "muziksel", "dogaci", "sosyal", "bedensel", "icsel"]

COKLU_ZEKA_QUESTIONS_LISE = {
    "sozel":     [{"id": 1,  "text": "Resimlerden çok yazılar dikkatimi çeker."}, {"id": 2,  "text": "İsimler, yerler, tarihler konusunda belleğim iyidir."}, {"id": 3,  "text": "Kitap okumayı severim."}, {"id": 4,  "text": "Kelimeleri doğru şekilde telaffuz ederim."}, {"id": 5,  "text": "Bilmecelerden, kelime oyunlarından hoşlanırım."}, {"id": 6,  "text": "Dinleyerek daha iyi öğrenirim."}, {"id": 7,  "text": "Yaşıma göre kelime hazinem iyidir."}, {"id": 8,  "text": "Yazı yazmaktan hoşlanırım."}, {"id": 9,  "text": "Öğrendiğim yeni kelimeleri kullanmayı severim."}, {"id": 10, "text": "Sözel tartışmalarda başarılıyımdır."}],
    "mantiksal": [{"id": 11, "text": "Makinelerin nasıl çalıştığına dair sorular sorarım."}, {"id": 12, "text": "Aritmetik problemleri kafadan hesaplarım."}, {"id": 13, "text": "Matematik ve fen derslerinden hoşlanırım."}, {"id": 14, "text": "Satranç ve benzeri strateji oyunları severim."}, {"id": 15, "text": "Mantık bulmacalarını, beyin jimnastiğini severim."}, {"id": 16, "text": "Bilgisayarda oyunlardan çok hoşlanırım."}, {"id": 17, "text": "Deneylerden, yeni denemeler yapmaktan hoşlanırım."}, {"id": 18, "text": "Arkadaşlarıma oranla daha soyut düşünebilirim."}, {"id": 19, "text": "Matematik oyunlarından hoşlanırım."}, {"id": 20, "text": "Sebep-sonuç ilişkilerini kurmaktan zevk alırım."}],
    "gorsel":    [{"id": 21, "text": "Renklere karşı çok duyarlıyımdır."}, {"id": 22, "text": "Harita, tablo türü materyalleri daha kolay algılarım."}, {"id": 23, "text": "Arkadaşlarıma oranla daha fazla hayal kurarım."}, {"id": 24, "text": "Resim yapmayı ve boyamayı çok severim."}, {"id": 25, "text": "Yap-boz, Lego gibi oyunlardan hoşlanırım."}, {"id": 26, "text": "Daha önce gittiğim yerleri kolayca hatırlarım."}, {"id": 27, "text": "Bulmaca çözmekten hoşlanırım."}, {"id": 28, "text": "Rüyalarımı çok net ve ayrıntılarıyla hatırlarım."}, {"id": 29, "text": "Resimli kitapları daha çok severim."}, {"id": 30, "text": "Kitaplarıma, defterlerime, diğer materyallere çizerim."}],
    "muziksel":  [{"id": 31, "text": "Şarkıların melodilerini rahatlıkla hatırlarım."}, {"id": 32, "text": "Güzel şarkı söylerim."}, {"id": 33, "text": "Müzik aleti çalar ya da çalmayı çok isterim."}, {"id": 34, "text": "Müzik dersini çok severim."}, {"id": 35, "text": "Ritmik konuşur ya da hareket ederim."}, {"id": 36, "text": "Farkında olmadan mırıldanırım."}, {"id": 37, "text": "Çalışırken elimle ya da ayağımla ritim tutarım."}, {"id": 38, "text": "Çevredeki sesler çok dikkatimi çeker."}, {"id": 39, "text": "Çalışırken müzik dinlemek çok hoşuma gider."}, {"id": 40, "text": "Öğrendiğim şarkıları paylaşmayı severim."}],
    "dogaci":    [{"id": 41, "text": "Hayvanlara karşı çok meraklıyımdır."}, {"id": 42, "text": "Doğaya karşı duyarsız olanlara kızarım."}, {"id": 43, "text": "Evde hayvan besler ya da beslemeyi çok severim."}, {"id": 44, "text": "Bahçede toprakla, bitkilerle oynamayı çok severim."}, {"id": 45, "text": "Bitki beslemeyi severim."}, {"id": 46, "text": "Çevre kirliliğine karşı çok duyarlıyımdır."}, {"id": 47, "text": "Bitki ya da hayvanlarla ilgili belgesellere ilgi duyarım."}, {"id": 48, "text": "Mevsimlerle ve iklim olaylarıyla çok ilgiliyimdir."}, {"id": 49, "text": "Değişik meyve ve sebzelere karşı ilgiliyimdir."}, {"id": 50, "text": "Doğa olaylarıyla çok ilgiliyimdir."}],
    "sosyal":    [{"id": 51, "text": "Arkadaşlarımla oyun oynamaktan hoşlanırım."}, {"id": 52, "text": "Çevremde bir lider olarak görülürüm."}, {"id": 53, "text": "Problemi olan arkadaşlarıma öğütler veririm."}, {"id": 54, "text": "Arkadaşlarım fikirlerime değer verir."}, {"id": 55, "text": "Organizasyonların vazgeçilmez elemanıyımdır."}, {"id": 56, "text": "Arkadaşlarıma bir şeyler anlatmaktan çok hoşlanırım."}, {"id": 57, "text": "Arkadaşlarımı sık sık ararım."}, {"id": 58, "text": "Arkadaşlarımın sorunlarına yardımcı olmaktan hoşlanırım."}, {"id": 59, "text": "Çevremdekiler benimle arkadaşlık kurmak ister."}, {"id": 60, "text": "İnsanlara selam verir, hatır sorarım."}],
    "bedensel":  [{"id": 61, "text": "Koşmayı, atlamayı ve güreşmeyi çok severim."}, {"id": 62, "text": "Oturduğum yerde duramam, kımıldanırım."}, {"id": 63, "text": "Düşüncelerimi mimik-davranışlarla rahat ifade ederim."}, {"id": 64, "text": "Bir şeyi okumak yerine yaparak öğrenmeyi severim."}, {"id": 65, "text": "Merak ettiğim şeyleri elime alarak incelemek isterim."}, {"id": 66, "text": "Boş vakitlerimi dışarıda geçirmek isterim."}, {"id": 67, "text": "Arkadaşlarımla fiziksel oyunlar oynamayı severim."}, {"id": 68, "text": "El becerilerim gelişmiştir."}, {"id": 69, "text": "Sorunlarımı anlatırken vücut hareketlerini kullanırım."}, {"id": 70, "text": "İnsanlara ve eşyalara dokunmaktan hoşlanırım."}],
    "icsel":     [{"id": 71, "text": "Bağımsız olmayı severim."}, {"id": 72, "text": "Güçlü ve zayıf yanlarımı bilirim."}, {"id": 73, "text": "Yalnız çalışmayı daha çok severim."}, {"id": 74, "text": "Yalnız oynamayı severim."}, {"id": 75, "text": "Yaptığım işleri arkadaşlarımla paylaşmayı severim."}, {"id": 76, "text": "Yaptığım işlerin bilincindeyimdir."}, {"id": 77, "text": "Pek kimseye akıl danışmam."}, {"id": 78, "text": "Kendime saygım yüksektir."}, {"id": 79, "text": "Yoğun olarak uğraştığım bir ilgi alanım, hobim vardır."}, {"id": 80, "text": "Yardım istemeden kendi başıma ürünleri ortaya koyarım."}],
}

COKLU_ZEKA_QUESTIONS_ILKOGRETIM = {
    "sozel":     [{"id": 1,  "text": "Kitaplara değer veririm."}, {"id": 10, "text": "Televizyon ya da film seyretmektense radyo dinlemeyi tercih ederim."}, {"id": 14, "text": "Kelime türetme ya da sözcük bulmacalarından hoşlanırım."}, {"id": 16, "text": "Tekerlemeler, komik şiirler ya da kelime oyunları ile kendimi ve başkalarını eğlendirmekten hoşlanırım."}, {"id": 26, "text": "Türkçe ve sosyal bilgiler dersleri matematik ve fen bilgisinden daha kolaydır."}],
    "gorsel":    [{"id": 3,  "text": "Kavramları okumadan ya da yazmadan önce gözümde canlandırabilirim."}, {"id": 5,  "text": "Resim yaparken çeşitli renkleri uyum içinde kullanırım."}, {"id": 15, "text": "Yap-boz, labirentler ve diğer görsel bulmacaları çözmekten hoşlanırım."}, {"id": 21, "text": "Hiç bilmediğim yerde bile yolumu bulabilirim."}, {"id": 34, "text": "Bir şeye yukarıdan kuşbakışı bakıldığında nasıl görünebileceğini rahatça gözümde canlandırabilirim."}],
    "muziksel":  [{"id": 7,  "text": "Bir şarkının yanlış söylendiğini hemen anlarım."}, {"id": 19, "text": "Müziksiz bir hayat benim için çok sıkıcıdır."}, {"id": 23, "text": "Yolda yürürken şarkılar mırıldanırım."}, {"id": 35, "text": "Bir, iki kez duyduğum şarkıyı doğru bir şekilde söyleyebilirim."}, {"id": 39, "text": "Ders çalışırken, iş yaparken ya da yeni bir şey öğrenirken sıkça şarkılar söyler ya da ayağımla yere vurarak tempo tutarım."}],
    "icsel":     [{"id": 20, "text": "Ulaşmak istediğim önemli hedeflerim var."}, {"id": 25, "text": "Yaptığım hatalardan ders alırım."}, {"id": 30, "text": "Arkadaşlarımla birlikte olmak yerine yalnız kalmayı isterim."}, {"id": 33, "text": "Kendimi güçlü ve bağımsız hissediyorum."}, {"id": 36, "text": "Günlük tutarım."}],
    "mantiksal": [{"id": 2,  "text": "Kâğıt, kalem kullanmadan hesap yapabilirim."}, {"id": 4,  "text": "Matematik çok sevdiğim derslerden biridir."}, {"id": 11, "text": "Zekâ bulmacalarını çözmekten hoşlanırım."}, {"id": 17, "text": "İşlerimi belli bir sıraya göre yaparım."}, {"id": 37, "text": "Bir şeyi, ölçüldüğü, gruplandırıldığı ya da miktarı hesaplandığında daha iyi anlarım."}],
    "bedensel":  [{"id": 6,  "text": "Uzun süre hareketsiz kalmaya dayanamam."}, {"id": 12, "text": "Dikiş, dokumacılık, oymacılık, doğramacılık ya da model yapmak gibi el becerisi gerektiren işlerle uğraşmayı severim."}, {"id": 22, "text": "Konuşurken çeşitli hareketler yaparım."}, {"id": 28, "text": "Yeni gördüğüm her şeye dokunmak isterim."}, {"id": 38, "text": "Öğrenmek için okumak ya da izlemek yerine o konuda uygulama yapmayı isterim."}],
    "sosyal":    [{"id": 8,  "text": "Tek başıma koşmak ve yüzmek yerine arkadaşlarımla basketbol, voleybol gibi sporları yapmayı tercih ederim."}, {"id": 13, "text": "Sorunlarımı kendi başıma çözmek yerine başka birinden yardım isterim."}, {"id": 24, "text": "Bildiğim bir konuyu başkalarına öğretme konusunda herkese meydan okurum."}, {"id": 29, "text": "Kendimi bir lider olarak görüyorum (ya da arkadaşlarım öyle olduğumu söylüyorlar)."}, {"id": 31, "text": "Kalabalık içinde kendimi rahat hissederim."}],
    "dogaci":    [{"id": 9,  "text": "Kırlarda ve ormanda olmaktan hoşlanırım."}, {"id": 18, "text": "Bazı insanların doğa konusundaki duyarsızlıkları beni çok üzer."}, {"id": 27, "text": "Etrafımda hayvanların olmasından çok hoşlanırım."}, {"id": 32, "text": "Çeşitli ağaç, kuş, bitki ve hayvan türleri arasındaki temel farklılıkları çok iyi bilirim."}, {"id": 40, "text": "Canlılar ve bitkilerle ilgili kitapları okumak, belgeselleri izlemekten çok hoşlanırım."}],
}


def calculate_coklu_zeka_lise(answers):
    """Çoklu Zekâ Lise — profil tipi + sinerji analizi."""
    answers = {int(k): v for k, v in answers.items()}
    scores = {}
    for zeka_key in ZEKA_SIRA:
        questions    = COKLU_ZEKA_QUESTIONS_LISE[zeka_key]
        total        = sum(answers.get(q["id"], 0) for q in questions)
        max_possible = len(questions) * 4
        scores[zeka_key] = {"raw": total, "max": max_possible,
                             "pct": round(total / max_possible * 100, 1)}

    sorted_scores = sorted(scores.items(), key=lambda x: x[1]["pct"], reverse=True)
    scores_named  = {COKLU_ZEKA_DATA[k]["name"]: v["pct"] for k, v in scores.items()}

    profile = _detect_zeka_profile(sorted_scores)
    synergies = _detect_zeka_synergies(sorted_scores[:3])

    result = {"version": "lise", "scores": scores, "scores_named": scores_named,
              "top3": sorted_scores[:3], "bottom2": sorted_scores[-2:],
              "profile": profile, "synergies": synergies}
    report = generate_coklu_zeka_report(result)
    return result, report


def calculate_coklu_zeka_ilkogretim(answers):
    """Çoklu Zekâ İlköğretim — profil tipi + sinerji analizi."""
    answers = {int(k): v for k, v in answers.items()}
    scores = {}
    for zeka_key in ZEKA_SIRA:
        questions    = COKLU_ZEKA_QUESTIONS_ILKOGRETIM[zeka_key]
        total        = sum(8 for q in questions if answers.get(q["id"]) == "E")
        max_possible = len(questions) * 8
        scores[zeka_key] = {"raw": total, "max": max_possible,
                             "pct": round(total / max_possible * 100, 1)}

    sorted_scores = sorted(scores.items(), key=lambda x: x[1]["pct"], reverse=True)
    scores_named  = {COKLU_ZEKA_DATA[k]["name"]: v["pct"] for k, v in scores.items()}

    profile = _detect_zeka_profile(sorted_scores)
    synergies = _detect_zeka_synergies(sorted_scores[:3])

    result = {"version": "ilkogretim", "scores": scores, "scores_named": scores_named,
              "top3": sorted_scores[:3], "bottom2": sorted_scores[-2:],
              "profile": profile, "synergies": synergies}
    report = generate_coklu_zeka_report(result)
    return result, report


def _detect_zeka_profile(sorted_scores):
    """Zekâ profil tipini belirler."""
    if not sorted_scores:
        return {"type": "belirsiz", "name": "Belirsiz", "description": ""}

    top_pct = sorted_scores[0][1]["pct"]
    second_pct = sorted_scores[1][1]["pct"] if len(sorted_scores) > 1 else 0
    bottom_pct = sorted_scores[-1][1]["pct"] if sorted_scores else 0
    pcts = [s[1]["pct"] for s in sorted_scores]
    spread = max(pcts) - min(pcts) if pcts else 0

    if spread <= 15:
        return {
            "type": "dengeli",
            "name": "🌈 Dengeli Profil",
            "description": "Tüm zekâ alanlarında birbirine yakın puanlar aldın. Çok yönlü bir yapın var — farklı alanlarda başarılı olabilirsin!",
        }
    elif top_pct - second_pct >= 15:
        top_name = COKLU_ZEKA_DATA[sorted_scores[0][0]]["name"]
        return {
            "type": "tek_baskin",
            "name": f"🎯 Tek Baskın: {top_name}",
            "description": f"Bir zekâ alanın ('{top_name}') diğerlerinden belirgin şekilde öne çıkıyor. Bu alanda uzmanlaşma potansiyelin yüksek!",
        }
    elif top_pct - sorted_scores[2][1]["pct"] <= 10 if len(sorted_scores) > 2 else False:
        names = [COKLU_ZEKA_DATA[s[0]]["name"] for s in sorted_scores[:3]]
        return {
            "type": "coklu_baskin",
            "name": f"⚡ Çoklu Baskın",
            "description": f"Birden fazla zekâ alanında ({', '.join(names)}) güçlüsün. Bu senin en büyük avantajın — bu alanları birleştirerek benzersiz yetenekler geliştirebilirsin!",
        }
    else:
        return {
            "type": "cift_baskin",
            "name": f"🔗 Çift Baskın",
            "description": f"İki zekâ alanın öne çıkıyor: {COKLU_ZEKA_DATA[sorted_scores[0][0]]['name']} ve {COKLU_ZEKA_DATA[sorted_scores[1][0]]['name']}. Bu ikili güçlü bir kombinasyon oluşturuyor!",
        }


def _detect_zeka_synergies(top3):
    """Top 3 zekâ arasındaki sinerjileri tespit eder."""
    SYNERGY_MAP = {
        frozenset(["mantiksal", "gorsel"]): {
            "name": "🏗️ Mühendislik Profili",
            "detail": "Mantıksal düşünme + görsel algı = mühendislik, mimarlık, bilgisayar bilimi alanlarında güçlü potansiyel.",
        },
        frozenset(["sozel", "sosyal"]): {
            "name": "🎤 İletişim Profili",
            "detail": "Dil yeteneği + sosyal zekâ = hukuk, eğitim, gazetecilik, halkla ilişkiler alanlarında güçlü potansiyel.",
        },
        frozenset(["muziksel", "bedensel"]): {
            "name": "🎭 Performans Profili",
            "detail": "Müzik + beden koordinasyonu = dans, tiyatro, spor, performans sanatları alanlarında güçlü potansiyel.",
        },
        frozenset(["icsel", "sozel"]): {
            "name": "✍️ Yaratıcı Yazar Profili",
            "detail": "İçsel farkındalık + dil yeteneği = yazarlık, psikoloji, felsefe, danışmanlık alanlarında güçlü potansiyel.",
        },
        frozenset(["dogaci", "bedensel"]): {
            "name": "🌿 Saha Bilimci Profili",
            "detail": "Doğa bilinci + fiziksel yetenek = biyoloji, veterinerlik, tarım, çevre bilimleri alanlarında güçlü potansiyel.",
        },
        frozenset(["mantiksal", "sozel"]): {
            "name": "⚖️ Akademik-Analitik Profil",
            "detail": "Mantık + dil = araştırma, hukuk, ekonomi, akademik kariyer alanlarında güçlü potansiyel.",
        },
        frozenset(["gorsel", "bedensel"]): {
            "name": "🎨 Tasarım Profili",
            "detail": "Görsel algı + el becerisi = endüstriyel tasarım, heykel, mimarlık, moda tasarımı alanlarında güçlü potansiyel.",
        },
        frozenset(["sosyal", "icsel"]): {
            "name": "🧑‍⚕️ İnsan Bilimci Profili",
            "detail": "Sosyal zekâ + iç görü = psikoloji, danışmanlık, koçluk, sosyal hizmet alanlarında güçlü potansiyel.",
        },
    }

    top_keys = [t[0] for t in top3]
    synergies = []
    for pair_set, info in SYNERGY_MAP.items():
        if pair_set.issubset(set(top_keys)):
            synergies.append(info)
    return synergies


def generate_coklu_zeka_report(result):
    scores  = result["scores"]
    top3    = result["top3"]
    bottom2 = result["bottom2"]
    ver     = "Lise/Yetişkin" if result["version"] == "lise" else "İlköğretim"
    profile = result.get("profile", {})
    synergies = result.get("synergies", [])

    report = f"# 🧠 ÇOKLU ZEKÂ DEĞERLENDİRME RAPORU\n**Versiyon:** {ver}\n\n---\n\n"

    # Profil Tipi
    if profile:
        report += f"## 🎯 Zekâ Profil Tipin: {profile.get('name', '')}\n\n"
        report += f"{profile.get('description', '')}\n\n---\n\n"

    # Zekâ Profil Tablosu
    report += "## 📊 Zekâ Profil Tablon\n\n| Zekâ Türü | Puan | Yüzde | Grafik |\n|---|---|---|---|\n"

    for zeka_key, sd in sorted(scores.items(), key=lambda x: x[1]["pct"], reverse=True):
        d = COKLU_ZEKA_DATA[zeka_key]
        n = round(sd["pct"] / 10)
        bar = "█" * n + "░" * (10 - n)
        report += f"| {d['icon']} {d['name']} | {sd['raw']}/{sd['max']} | %{sd['pct']} | {bar} |\n"

    report += "\n---\n\n## 🏆 En Güçlü 3 Zekâ Alanın\n\n"
    medals = ["🥇", "🥈", "🥉"]
    for rank, (zk, sd) in enumerate(top3, 1):
        d = COKLU_ZEKA_DATA[zk]
        report += f"### {medals[rank-1]} {rank}. {d['icon']} {d['name']} (%{sd['pct']})\n\n{d['description']}\n\n"
        report += "**Güçlü Yönlerin:**\n" + "\n".join(f"- ✅ {s}" for s in d["strengths"]) + "\n\n"
        report += "**Ders Çalışma İpuçları:**\n" + "\n".join(f"- 💡 {t}" for t in d["study_tips"]) + "\n\n"
        report += f"**Sana Uygun Kariyer Alanları:** {', '.join(d['careers'])}\n\n---\n\n"

    # Sinerji Bölümü
    if synergies:
        report += "## 🔗 Zekâ Sinerjilerin — Güçlü Kombinasyonlar\n\n"
        for syn in synergies:
            report += f"### {syn['name']}\n{syn['detail']}\n\n"
        report += "---\n\n"

    # Gelişime Açık Alanlar
    report += "## 🌱 Gelişime Açık Alanların\n\n"
    for zk, sd in bottom2:
        d = COKLU_ZEKA_DATA[zk]
        report += f"### {d['icon']} {d['name']} (%{sd['pct']})\n\nBu alanda henüz keşfetmediğin yeteneklerin olabilir. İşte geliştirmek için birkaç ipucu:\n\n"
        report += "\n".join(f"- 🌱 {t}" for t in d["study_tips"]) + "\n\n"

    # Ebeveyn Rehberi
    report += "---\n\n## 👨‍👩‍👦 Ebeveyn Rehberi\n\n"
    top_names = [COKLU_ZEKA_DATA[t[0]]["name"] for t in top3]
    report += f"Çocuğunuzun en güçlü zekâ alanları: **{', '.join(top_names)}**\n\n"
    report += "**Öneriler:**\n"
    report += "- ✅ Bu güçlü alanları destekleyecek etkinlikler ve kurslar araştırın\n"
    report += "- ✅ Zayıf alanları güçlü alanlar üzerinden geliştirin (ör: Görsel zekâsı güçlü bir çocuğa matematiği şemalarla öğretin)\n"
    report += "- ✅ Her zekâ türü eşit değerdedir — tek bir alana odaklanmak yerine çocuğunuzun doğal yeteneklerini keşfetmesine izin verin\n\n"

    # Öğretmen Notu
    report += "## 👩‍🏫 Öğretmen Notu\n\n"
    report += f"Bu öğrencinin güçlü zekâ alanları: **{', '.join(top_names)}**.\n"
    report += "Ders materyallerini bu zekâ alanlarına uygun çeşitlendirmek öğrenme verimliliğini artıracaktır.\n\n"

    report += "\n---\n\n## 💬 Son Söz\nUnutma, herkesin farklı zekâ alanlarında güçlü ve gelişime açık yönleri vardır. Hiçbir zekâ türü diğerinden daha iyi ya da kötü değildir! Sen benzersizsin! 🌟"
    return report.strip()


# ============================================================
# BÖLÜM 5: VARK ÖĞRENME STİLLERİ
# ============================================================

VARK_SCORING = {
    1:  {"a": "K", "b": "A", "c": "R", "d": "V"},
    2:  {"a": "V", "b": "A", "c": "R", "d": "K"},
    3:  {"a": "K", "b": "V", "c": "R", "d": "A"},
    4:  {"a": "K", "b": "A", "c": "V", "d": "R"},
    5:  {"a": "A", "b": "V", "c": "K", "d": "R"},
    6:  {"a": "K", "b": "R", "c": "V", "d": "A"},
    7:  {"a": "K", "b": "A", "c": "V", "d": "R"},
    8:  {"a": "R", "b": "K", "c": "A", "d": "V"},
    9:  {"a": "R", "b": "A", "c": "K", "d": "V"},
    10: {"a": "K", "b": "V", "c": "R", "d": "A"},
    11: {"a": "V", "b": "R", "c": "A", "d": "K"},
    12: {"a": "A", "b": "R", "c": "V", "d": "K"},
    13: {"a": "K", "b": "A", "c": "R", "d": "V"},
    14: {"a": "K", "b": "R", "c": "A", "d": "V"},
    15: {"a": "K", "b": "A", "c": "R", "d": "V"},
    16: {"a": "V", "b": "A", "c": "R", "d": "K"},
}

VARK_QUESTIONS = [
    {"id": 1,  "text": "Bir yere gitmek istiyorsun ama yolu bilmiyorsun. Ne yaparsın?", "options": {"a": "Doğru yönde yürümeye başlar, yolu bulmaya çalışırım.", "b": "Birinden yol tarifi isterim veya sesli navigasyon kullanırım.", "c": "Yol tarifini yazılı olarak okurum.", "d": "Harita veya navigasyondaki haritaya bakarım."}},
    {"id": 2,  "text": "Bir internet sitesinde grafik nasıl yapılır diye bir video var. En çok hangisinden öğrenirsin?", "options": {"a": "Şemaları ve diyagramları görerek.", "b": "Anlatanı dinleyerek.", "c": "Yazılı açıklamaları okuyarak.", "d": "Yapılan işlemleri izleyerek."}},
    {"id": 3,  "text": "Katılacağın bir gezi hakkında bilgi edinmek istiyorsun. Ne yaparsın?", "options": {"a": "Gezinin etkinlik ve öne çıkan yerlerinin detaylarına bakarım.", "b": "Haritaya bakıp gidilecek yerleri görürüm.", "c": "Gezi programını okuyarak bilgi edinirim.", "d": "Geziyi planlayan kişiyle ya da gidecek olan arkadaşlarımla konuşurum."}},
    {"id": 4,  "text": "Gelecekte ne yapmak istediğine karar verirken hangisi senin için önemlidir?", "options": {"a": "Bilgimi gerçek durumlarla uygulayabilmek.", "b": "Başkalarıyla tartışarak iletişim kurabilmek.", "c": "Tasarımlarla, haritalarla veya çizelgelerle çalışabilmek.", "d": "Yazarak kendimi iyi ifade edebilmek."}},
    {"id": 5,  "text": "Bir şey öğrenirken hangisini tercih edersin?", "options": {"a": "Konuyu biriyle konuşarak tartışmayı.", "b": "Kalıpları ve örüntüleri görmeyi.", "c": "Örnekler ve uygulamalar üzerinden denemeyi.", "d": "Kitap, makale ve ders notlarını okumayı."}},
    {"id": 6,  "text": "Birçok seçenek arasında karar vermen gerekiyor. Ne yaparsın?", "options": {"a": "Her seçeneği kendi bilgilerimle örnekleyerek değerlendiririm.", "b": "Seçenekleri anlatan yazılı bir belgeyi okurum.", "c": "Karşılaştırma grafikleri ve tabloları incelerim.", "d": "Konuyu bilen biriyle konuşurum."}},
    {"id": 7,  "text": "Yeni bir masa oyunu veya kart oyunu öğrenmek istiyorsun. Ne yaparsın?", "options": {"a": "Başkalarının oynamasını izler, sonra katılırım.", "b": "Birinin bana anlatmasını ve soru sormamı tercih ederim.", "c": "Oyunun şemalarını ve strateji diyagramlarını incelerim.", "d": "Oyunun kurallarını okurum."}},
    {"id": 8,  "text": "Sağlığınla ilgili bir konu hakkında bilgi edinmek istiyorsun. Ne yaparsın?", "options": {"a": "Konuyla ilgili bir makale veya yazı okurum.", "b": "Konuyu anlatan bir model veya görsel üzerinde incelerim.", "c": "Doktorla veya konuyu bilenle detaylı konuşurum.", "d": "Konuyu gösteren bir şema veya diyagrama bakarım."}},
    {"id": 9,  "text": "Bilgisayarda yeni bir şey öğrenmek istiyorsun. Ne yaparsın?", "options": {"a": "Yazılı kullanım kılavuzunu okurum.", "b": "Konuyu bilen birinden sözlü anlatım dinlerim.", "c": "Deneme-yanılma yöntemiyle kendim denerim.", "d": "Kitaptaki veya ekrandaki diyagramları takip ederim."}},
    {"id": 10, "text": "İnternetten bir şey öğrenirken hangisini tercih edersin?", "options": {"a": "Nasıl yapıldığını gösteren videoları.", "b": "İlginç tasarımları ve görsel özellikleri.", "c": "Detaylı yazılı makaleleri.", "d": "Uzmanların konuştuğu podcastleri ve videoları."}},
    {"id": 11, "text": "Yeni bir proje hakkında bilgi almak istiyorsun. Ne istersin?", "options": {"a": "Proje aşamalarını gösteren şemalar ve grafikler.", "b": "Projenin ana özelliklerini anlatan yazılı bir rapor.", "c": "Projeyi tartışma fırsatı.", "d": "Projenin başarıyla uygulandığı örnekler."}},
    {"id": 12, "text": "Daha iyi fotoğraf çekmeyi öğrenmek istiyorsun. Ne yaparsın?", "options": {"a": "Soru sorar, kamera ve özellikleri hakkında konuşurum.", "b": "Ne yapılması gerektiğini anlatan yazılı talimatları okurum.", "c": "Kameranın her parçasını gösteren şemaları incelerim.", "d": "İyi ve kötü fotoğraf örneklerini inceleyerek farkları anlarım."}},
    {"id": 13, "text": "Bir öğretmenin veya sunum yapan birinin hangisini kullanmasını tercih edersin?", "options": {"a": "Gösteriler, modeller veya uygulamalı çalışmalar.", "b": "Soru-cevap, tartışma veya konuk konuşmacılar.", "c": "Ders notları, kitaplar veya okuma materyalleri.", "d": "Şemalar, grafikler, haritalar veya çizelgeler."}},
    {"id": 14, "text": "Bir sınavdan veya yarışmadan sonra geri bildirim almak istiyorsun. Nasıl almayı tercih edersin?", "options": {"a": "Yaptıklarımdan örneklerle.", "b": "Sonuçlarımın yazılı açıklamasıyla.", "c": "Birinin benimle konuşarak açıklamasıyla.", "d": "Performansımı gösteren grafiklerle."}},
    {"id": 15, "text": "Bir evi veya daireyi ziyaret etmeden önce ne istersin?", "options": {"a": "Evin videosunu izlemeyi.", "b": "Ev sahibiyle konuşmayı.", "c": "Odaların ve özelliklerin yazılı açıklamasını okumayı.", "d": "Oda planını ve bölge haritasını görmeyi."}},
    {"id": 16, "text": "Parçalardan oluşan bir mobilyayı kurmakta zorlanıyorsun. Ne yaparsın?", "options": {"a": "Montaj aşamalarını gösteren şemaları incelerim.", "b": "Daha önce mobilya kurmuş birinden tavsiye isterim.", "c": "Birlikte gelen yazılı talimatları okurum.", "d": "Benzer bir mobilyayı kuran birinin videosunu izlerim."}},
]

VARK_STYLES = {
    "V": {"name": "Görsel (Visual)", "icon": "👁️", "description": "Sen görsel bir öğrenicisin! Şemalar, grafikler, haritalar ve diyagramlar senin en iyi öğrenme araçların.", "characteristics": ["Haritalar, grafikler ve şemalardan kolay öğrenir", "Bilgiyi görsel düzende organize etmeyi sever", "Renk kodlama ve vurgulama kullanır", "Mekânsal düzenleme ve tasarım becerileri güçlüdür"], "study_tips": ["📊 Zihin haritaları ve kavram haritaları çiz.", "🎨 Renkli kalemler ve fosforlu kalemler kullan.", "📐 Konuları şema, diyagram ve tablo halinde düzenle.", "🗺️ Akış şemaları ve süreç diyagramları oluştur.", "📋 Not alırken oklar, kutucuklar ve semboller kullan."], "avoid": "Uzun düz metinler ve sesli anlatımlar seni sıkabilir — görselleştir!"},
    "A": {"name": "İşitsel (Aural)", "icon": "👂", "description": "Sen işitsel bir öğrenicisin! Dinleyerek, tartışarak ve konuşarak en iyi şekilde öğreniyorsun.", "characteristics": ["Dersleri dinleyerek daha iyi anlar", "Tartışma ve soru-cevapla öğrenir", "Sesli tekrar yaparak ezberler", "Müzik ve ritimlerle bilgiyi hatırlar"], "study_tips": ["🎧 Ders sesli kayıtlarını dinle veya kendi kayıtlarını yap.", "🗣️ Öğrendiğin konuları birine sesli anlat.", "💬 Çalışma gruplarında tartışarak öğren.", "🎵 Önemli bilgileri kafiyeli veya ritmik cümlelerle ezberle.", "📱 Podcast ve sesli kitaplardan yararlan."], "avoid": "Sessiz ve uzun okuma seansları seni yorabilir — sesli çalış!"},
    "R": {"name": "Okuma/Yazma (Read/Write)", "icon": "📖", "description": "Sen okuyarak ve yazarak öğrenen birisin! Yazılı materyaller senin en güçlü öğrenme kaynağın.", "characteristics": ["Kitap, makale ve ders notlarını okuyarak öğrenir", "Not almayı ve yazarak tekrar yapmayı sever", "Listeler ve yazılı planlar oluşturur", "Sözlükler ve ansiklopedileri kullanır"], "study_tips": ["📝 Bol bol not al ve notlarını düzenle.", "📋 Öğrendiğin konuları kendi kelimelerinle yaz.", "📚 Ders kitapları ve ek okuma kaynakları kullan.", "🗒️ Listeler, özetler ve tanım kartları (flashcard) hazırla.", "✍️ Sınava hazırlanırken soruları yazarak çalış."], "avoid": "Sadece dinleme veya izleme yetersiz kalabilir — oku ve yaz!"},
    "K": {"name": "Kinestetik (Kinesthetic)", "icon": "🤸", "description": "Sen yaparak ve deneyerek öğrenen birisin! Uygulamalı etkinlikler senin en etkili öğrenme yolun.", "characteristics": ["Yaparak ve deneyerek öğrenir", "Uygulamalı çalışmaları tercih eder", "Gerçek hayat örnekleriyle konuları anlar", "Hareket ederken daha iyi düşünür"], "study_tips": ["🔬 Laboratuvar çalışmaları ve deneyler yap.", "🚶 Ders çalışırken yürüyerek tekrar et.", "🎭 Konuları canlandırarak veya rol yaparak öğren.", "✋ Model ve maketler yaparak somutlaştır.", "⏱️ Kısa süreli çalış, sık sık mola ver ve hareket et."], "avoid": "Uzun süre oturup okumak seni yorabilir — hareket et ve uygula!"},
}


def calculate_vark(answers):
    """
    DÜZELTME: is_multimodal eşiği <= 2 (Fleming standardı).
    Eskiden <= 1 idi, çok dar bir aralıktı.
    """
    vark_counts = {"V": 0, "A": 0, "R": 0, "K": 0}

    for qid, selected_options in answers.items():
        qid = int(qid)
        if qid not in VARK_SCORING:
            continue
        if isinstance(selected_options, str):
            selected_options = [selected_options]
        for opt in selected_options:
            opt = opt.lower()
            if opt in VARK_SCORING[qid]:
                vark_counts[VARK_SCORING[qid][opt]] += 1

    total = sum(vark_counts.values())
    percentages   = {k: round(v/total*100, 1) if total else 0 for k, v in vark_counts.items()}
    sorted_styles = sorted(vark_counts.items(), key=lambda x: x[1], reverse=True)
    dominant      = sorted_styles[0]
    second        = sorted_styles[1]

    # DÜZELTME: Fleming standardı — fark <= 2 ise multimodal
    is_multimodal = (dominant[1] - second[1]) <= 2 and dominant[1] > 0

    scores = {"counts": vark_counts, "percentages": percentages,
              "total_responses": total, "sorted": sorted_styles,
              "dominant": dominant, "is_multimodal": is_multimodal}
    report = generate_vark_report(scores)
    return scores, report


def generate_vark_report(scores):
    counts       = scores["counts"]
    percentages  = scores["percentages"]
    sorted_styles = scores["sorted"]
    dominant_key = scores["dominant"][0]
    is_multimodal = scores["is_multimodal"]

    report = "# 🎯 VARK ÖĞRENME STİLİ RAPORU\n\n---\n\n## 📊 Öğrenme Stili Profilin\n\n| Stil | Puan | Yüzde | Grafik |\n|---|---|---|---|\n"
    for sk, cnt in sorted_styles:
        s   = VARK_STYLES[sk]
        pct = percentages[sk]
        n   = round(pct / 10)
        bar = "█" * n + "░" * (10 - n)
        report += f"| {s['icon']} {s['name']} | {cnt} | %{pct} | {bar} |\n"

    report += "\n---\n\n"

    if is_multimodal:
        top_two = sorted_styles[:2]
        report += "## 🌟 Senin Öğrenme Stilin: Çok Modlu (Multimodal)\n\nBirden fazla öğrenme stilini eşit derecede kullanıyorsun!\n\n"
        report += f"En güçlü iki stilin: **{VARK_STYLES[top_two[0][0]]['name']}** ve **{VARK_STYLES[top_two[1][0]]['name']}**\n\n"
        for sk, _ in top_two:
            s = VARK_STYLES[sk]
            report += f"### {s['icon']} {s['name']}\n\n{s['description']}\n\n**Ders Çalışma İpuçları:**\n"
            report += "\n".join(f"- {t}" for t in s["study_tips"]) + "\n\n"
    else:
        s = VARK_STYLES[dominant_key]
        report += f"## 🌟 Senin Baskın Öğrenme Stilin: {s['icon']} {s['name']}\n\n{s['description']}\n\n"
        report += "**Seni Tanımlayan Özellikler:**\n" + "\n".join(f"- ✅ {c}" for c in s["characteristics"]) + "\n\n"
        report += "**Sana Özel Ders Çalışma İpuçları:**\n" + "\n".join(f"- {t}" for t in s["study_tips"]) + "\n\n"
        report += f"⚠️ **Dikkat:** {s['avoid']}\n\n"

    # DERSE ÖZEL ÖĞRENME STRATEJİLERİ
    active_style = dominant_key if not is_multimodal else sorted_styles[0][0]
    report += "---\n\n## 📚 Derse Özel Öğrenme Stratejilerin\n\n"

    DERS_STRATEJILERI = {
        "V": {
            "Matematik": "Formülleri renkli kartlara yaz. Grafik ve diyagramlarla çalış. Geometri konularında çizim yap.",
            "Türkçe/Edebiyat": "Zihin haritaları çiz. Dil bilgisi kurallarını şemalarla öğren. Kitap özetlerini görsel notlarla yap.",
            "Fen Bilimleri": "Deney süreçlerini şemalarla çiz. Hücre, atom gibi yapıları görselleştir. Renkli tablolar oluştur.",
            "Sosyal Bilimler": "Tarih çizelgeleri oluştur. Haritalar üzerinde çalış. Olayları görsel akış şemalarıyla ilişkilendir.",
        },
        "A": {
            "Matematik": "Formülleri sesli tekrarla. Çözüm adımlarını kendine anlat. Problem çözerken sesli düşün.",
            "Türkçe/Edebiyat": "Metinleri sesli oku. Şiirleri ve hikayeleri dinle. Tartışma gruplarına katıl.",
            "Fen Bilimleri": "Konuları birine anlatarak öğren. Podcast ve video dersleri dinle. Grup tartışması yap.",
            "Sosyal Bilimler": "Belgeseller ve podcast dinle. Tarihi olayları hikayeleştirerek anlat. Sözlü soru-cevap yap.",
        },
        "R": {
            "Matematik": "Formülleri yazarak tekrarla. Örnek soruları adım adım yaz. Not kartları (flashcard) hazırla.",
            "Türkçe/Edebiyat": "Kitap özetleri yaz. Kompozisyon pratiği yap. Kelime listeleri oluştur ve düzenli tekrarla.",
            "Fen Bilimleri": "Deney raporları yaz. Konuları kendi cümlelerinle özetle. Kitaptan önemli yerleri çıkar.",
            "Sosyal Bilimler": "Kronolojik notlar tut. Konu özetleri yaz. Kavramları kendi kelimelerinle tanımla.",
        },
        "K": {
            "Matematik": "Problem çözerken kağıt-kaleme sık başvur. Geometride modeller yap. Hesap makinesi ve araçlarla pratik yap.",
            "Türkçe/Edebiyat": "Rol yapma ve canlandırma yap. Hikayeleri sahnele. Kelime kartlarını fiziksel olarak sırala.",
            "Fen Bilimleri": "Laboratuvar deneyleri yap. Modeller ve maketler inşa et. Doğa gözlemleri yaparak öğren.",
            "Sosyal Bilimler": "Tarihsel olayları canlandır. Müze ve tarihi mekan ziyaretleri yap. Haritaları kendin çiz.",
        },
    }

    strategies = DERS_STRATEJILERI.get(active_style, {})
    if strategies:
        report += "| Ders | Strateji |\n|------|----------|\n"
        for ders, strateji in strategies.items():
            report += f"| **{ders}** | {strateji} |\n"
        report += "\n"

    # Zayıf Stilini Güçlendirme
    weakest_key = sorted_styles[-1][0]
    weakest_style = VARK_STYLES[weakest_key]
    report += f"---\n\n## 🌱 Zayıf Stilini Güçlendirme: {weakest_style['icon']} {weakest_style['name']}\n\n"
    report += f"En az kullandığın öğrenme stili **{weakest_style['name']}**. Bu stili de geliştirmek, öğrenme esnekliğini artırır:\n\n"
    report += "\n".join(f"- 🌱 {t}" for t in weakest_style["study_tips"][:3]) + "\n\n"

    # Ebeveyn Rehberi
    active_name = VARK_STYLES[active_style]["name"]
    report += "---\n\n## 👨‍👩‍👦 Ebeveyn Rehberi\n\n"
    report += f"Çocuğunuzun baskın öğrenme stili: **{active_name}**\n\n"
    parent_tips = {
        "V": "Çocuğunuza renkli kalemler, poster kağıtları ve görsel materyaller sağlayın. Çalışma odasında görsel düzen oluşturun.",
        "A": "Çocuğunuzla konuları tartışın. Sesli okuma ve dinleme materyalleri sağlayın. Sessiz bir çalışma ortamı çok önemli — diğer sesleri engelleyin.",
        "R": "Çocuğunuza kaliteli defterler ve not araçları sağlayın. Yazarak özetleme alışkanlığını destekleyin. Kitap okumasını teşvik edin.",
        "K": "Çocuğunuza yaparak öğrenme fırsatları sunun. Deney setleri, lego, maket malzemeleri sağlayın. Uzun süre oturmasını beklemeyin — kısa molalarla hareket etmesine izin verin.",
    }
    report += parent_tips.get(active_style, "") + "\n\n"

    # Öğretmen Notu
    report += "## 👩‍🏫 Öğretmen Notu\n\n"
    teacher_tips = {
        "V": "Bu öğrenci görsel materyallerden en çok verim alır. Tahta kullanımı, şemalar, renkli gösterimler etkili olacaktır.",
        "A": "Bu öğrenci işitsel öğrenir. Sınıf tartışmaları, sesli anlatım ve soru-cevap etkinlikleri etkili olacaktır.",
        "R": "Bu öğrenci okuyarak/yazarak öğrenir. Not tutma, özet çıkarma ve yazılı materyaller etkili olacaktır.",
        "K": "Bu öğrenci yaparak/deneyimleyerek öğrenir. Laboratuvar, atölye, rol yapma ve fiziksel etkinlikler etkili olacaktır.",
    }
    report += teacher_tips.get(active_style, "") + "\n\n"

    report += "---\n\n## 💬 Son Söz\nÖğrenme stilini bilmek, daha verimli çalışmanın anahtarıdır! Baskın stilini kullanarak başla, diğer stilleri de deneyerek öğrenme repertuarını genişlet. 🚀"
    return report.strip()


# ============================================================
# BÖLÜM 6: HOLLAND RIASEC MESLEKİ İLGİ ENVANTERİ
# ============================================================

HOLLAND_TYPES = {
    "R": {
        "name": "Gerçekçi (Realistic)", "icon": "🔧", "short": "Gerçekçi",
        "description": "Uygulamacı, somut ve pratik işleri seven bir yapın var! Elleriyle çalışmayı, fiziksel aktiviteleri ve somut sonuçlar üretmeyi tercih edersin.",
        "characteristics": ["Pratik ve uygulamacı", "El becerisi ve mekanik yeteneği güçlü", "Somut ve elle tutulur sonuçları sever", "Açık havada çalışmaktan hoşlanır", "Araç, makine ve aletlerle çalışmayı sever"],
        "careers": ["Makine/Elektrik/İnşaat Mühendisi", "Pilot", "Mimar (Uygulama)", "Ziraat Mühendisi", "Elektronikçi", "Ormancı", "Beden Eğitimi Öğretmeni", "Aşçı/Şef"],
        "study_environment": "Laboratuvar, atölye ve açık hava etkinlikleri sana en uygun öğrenme ortamı.",
    },
    "I": {
        "name": "Araştırmacı (Investigative)", "icon": "🔬", "short": "Araştırmacı",
        "description": "Meraklı, analitik ve bilimsel düşünmeyi seven bir yapın var! Problemleri araştırmayı, gözlem yapmayı ve çözüm üretmeyi seversin.",
        "characteristics": ["Meraklı ve analitik düşünür", "Bilimsel yöntemlere ilgi duyar", "Bağımsız çalışmayı tercih eder", "Matematiksel ve mantıksal düşünce güçlü", "Eleştirel ve sorgulayıcı"],
        "careers": ["Fizikçi/Kimyager/Biyolog", "Doktor", "Eczacı", "Yazılım Mühendisi", "Araştırmacı/Akademisyen", "Psikolog", "Matematikçi", "Veteriner"],
        "study_environment": "Kütüphane, laboratuvar ve bireysel araştırma ortamları sana en uygun.",
    },
    "A": {
        "name": "Sanatçı (Artistic)", "icon": "🎨", "short": "Sanatçı",
        "description": "Yaratıcı, özgür düşünceli ve estetik duyarlılığı yüksek bir yapın var! Kendini ifade etmeyi ve özgün eserler ortaya koymayı seversin.",
        "characteristics": ["Yaratıcı ve hayal gücü zengin", "Estetik duyarlılığı yüksek", "Özgün ve alışılmadık fikirleri sever", "Yapılandırılmamış ortamlarda daha iyi çalışır", "Duygusal ifade gücü kuvvetli"],
        "careers": ["Ressam/Heykeltıraş", "Müzisyen/Besteci", "Yazar/Şair", "Grafik Tasarımcı", "Fotoğrafçı", "Oyuncu", "Moda Tasarımcısı", "Reklamcı"],
        "study_environment": "Özgür ve yaratıcı ortamlar, bireysel projeler sana en uygun.",
    },
    "S": {
        "name": "Sosyal (Social)", "icon": "🤝", "short": "Sosyal",
        "description": "İnsanlarla çalışmayı, onlara yardım etmeyi ve öğretmeyi seven bir yapın var! Empati ve iletişim senin güçlü yönlerin.",
        "characteristics": ["İnsanlarla çalışmayı sever", "Empati yeteneği güçlü", "İyi bir dinleyici ve iletişimci", "Öğretmeyi ve yardım etmeyi sever", "Takım çalışmasına yatkın"],
        "careers": ["Öğretmen/Akademisyen", "Psikolog/Danışman", "Sosyal Hizmet Uzmanı", "Hemşire/Doktor", "İnsan Kaynakları", "Toplum Lideri", "Terapist"],
        "study_environment": "Grup çalışmaları, tartışmalar ve sosyal projeler sana en uygun.",
    },
    "E": {
        "name": "Girişimci (Enterprising)", "icon": "💼", "short": "Girişimci",
        "description": "Liderlik etmeyi, ikna etmeyi ve risk almayı seven bir yapın var! Hedeflerine ulaşmak için insanları organize edebilirsin.",
        "characteristics": ["Doğal liderlik özellikleri", "İkna ve etkileme becerisi güçlü", "Rekabetçi ve hırslı", "Risk almaktan çekinmez", "Organizasyon ve yönetim becerileri iyi"],
        "careers": ["İşletmeci/Girişimci", "Satış/Pazarlama Müdürü", "Avukat", "Politikacı", "Yönetici/CEO", "Broker", "Proje Müdürü"],
        "study_environment": "Liderlik rolleri, proje bazlı çalışmalar ve sunum ortamları sana en uygun.",
    },
    "C": {
        "name": "Geleneksel (Conventional)", "icon": "📊", "short": "Geleneksel",
        "description": "Düzenli, sistemli ve kurallara uygun çalışmayı seven bir yapın var! Detaylara dikkat etmek ve verileri organize etmek senin güçlü yönlerin.",
        "characteristics": ["Düzenli ve sistematik çalışır", "Detaylara çok dikkat eder", "Kurallara ve prosedürlere saygılı", "Veri ve sayılarla rahat çalışır", "Güvenilir ve tutarlı"],
        "careers": ["Muhasebeci/Mali Müşavir", "Banka Çalışanı", "Sekreter/İdari Asistan", "Veri Analisti", "Arşivci", "Vergi Uzmanı", "Aktüer"],
        "study_environment": "Yapılandırılmış, sessiz ve düzenli ortamlar sana en uygun.",
    },
}

HOLLAND_QUESTIONS = [
    # R (Gerçekçi) — 1-14
    {"id": 1,  "text": "Bir şeyi tamir etmekten hoşlanırım.", "type": "R"},
    {"id": 2,  "text": "Açık havada çalışmaktan hoşlanırım.", "type": "R"},
    {"id": 3,  "text": "Mekanik araçları ve makineleri kullanmaktan zevk alırım.", "type": "R"},
    {"id": 4,  "text": "Elleri ile çalışmayı severim.", "type": "R"},
    {"id": 5,  "text": "Fiziksel güç ve dayanıklılık gerektiren aktivitelerden hoşlanırım.", "type": "R"},
    {"id": 6,  "text": "Somut ve elle tutulur sonuçlar üretmekten zevk alırım.", "type": "R"},
    {"id": 7,  "text": "Spor yapmayı ve atletik aktivitelere katılmayı severim.", "type": "R"},
    {"id": 8,  "text": "Pratik problemleri çözmekten hoşlanırım.", "type": "R"},
    {"id": 9,  "text": "Yapım işleri ve inşaatla ilgili faaliyetleri severim.", "type": "R"},
    {"id": 10, "text": "Araç gereç ve ekipmanlarla çalışmaktan keyif alırım.", "type": "R"},
    {"id": 11, "text": "Ürün geliştirme ve prototip oluşturma gibi aktivitelerden hoşlanırım.", "type": "R"},
    {"id": 12, "text": "Yemek pişirmek veya el sanatlarıyla ilgilenmekten hoşlanırım.", "type": "R"},
    {"id": 13, "text": "Arabaları veya diğer motorlu araçları tamir etmek ilgimi çeker.", "type": "R"},
    {"id": 14, "text": "Elektronik cihazları sökmeyi ve onarmayı severim.", "type": "R"},
    # I (Araştırmacı) — 15-28
    {"id": 15, "text": "Bağımsız çalışmayı ve kendi başıma problem çözmeyi tercih ederim.", "type": "I"},
    {"id": 16, "text": "Bilimsel araştırmalara ilgi duyarım.", "type": "I"},
    {"id": 17, "text": "Karmaşık sorunları analiz etmekten zevk alırım.", "type": "I"},
    {"id": 18, "text": "Matematiksel problemleri çözmekten hoşlanırım.", "type": "I"},
    {"id": 19, "text": "Doğal dünya hakkında sorular sormaktan ve araştırma yapmaktan hoşlanırım.", "type": "I"},
    {"id": 20, "text": "Teorileri ve kavramları incelemeyi severim.", "type": "I"},
    {"id": 21, "text": "Bilgisayar programlama ve kodlamayı ilginç bulurum.", "type": "I"},
    {"id": 22, "text": "Yeni şeyler öğrenmek ve keşfetmek beni heyecanlandırır.", "type": "I"},
    {"id": 23, "text": "Sorunların kök nedenlerini bulmaya çalışırım.", "type": "I"},
    {"id": 24, "text": "Veri toplama ve analiz etmekten zevk alırım.", "type": "I"},
    {"id": 25, "text": "Deney yapmayı ve hipotezleri test etmeyi severim.", "type": "I"},
    {"id": 26, "text": "Gözlem yaparak sonuçlar çıkarmaktan hoşlanırım.", "type": "I"},
    {"id": 27, "text": "Teknik konular ve uzmanlık gerektiren alanlar ilgimi çeker.", "type": "I"},
    {"id": 28, "text": "Karmaşık sistemlerin nasıl çalıştığını anlamaktan zevk alırım.", "type": "I"},
    # A (Sanatçı) — 29-42
    {"id": 29, "text": "Resim yapmayı, çizmeyi veya el sanatlarıyla ilgilenmeyi severim.", "type": "A"},
    {"id": 30, "text": "Yazı yazmaktan (şiir, hikaye, deneme gibi) hoşlanırım.", "type": "A"},
    {"id": 31, "text": "Müzikle ilgilenmek (dinlemek, çalmak, söylemek) beni mutlu eder.", "type": "A"},
    {"id": 32, "text": "Yaratıcı projeler üzerinde çalışmaktan zevk alırım.", "type": "A"},
    {"id": 33, "text": "Kendimi sanatsal yollarla ifade etmeyi severim.", "type": "A"},
    {"id": 34, "text": "Estetik ve güzellik benim için önemlidir.", "type": "A"},
    {"id": 35, "text": "Hayal gücümü kullanarak yeni fikirler üretmekten hoşlanırım.", "type": "A"},
    {"id": 36, "text": "Fotoğrafçılık, film veya multimedya ile ilgilenmekten zevk alırım.", "type": "A"},
    {"id": 37, "text": "Dans, tiyatro veya performans sanatlarına ilgi duyarım.", "type": "A"},
    {"id": 38, "text": "Farklı kültürler ve sanat formlarını keşfetmekten hoşlanırım.", "type": "A"},
    {"id": 39, "text": "Doğaçlama yapmaktan ve ani kararlar almaktan zevk alırım.", "type": "A"},
    {"id": 40, "text": "Moda, tasarım veya dekorasyon ile ilgilenmekten hoşlanırım.", "type": "A"},
    {"id": 41, "text": "Sanatsal veya yaratıcı bir ortamda çalışmak isterim.", "type": "A"},
    {"id": 42, "text": "Yenilikçi ve orijinal fikirler geliştirmekten zevk alırım.", "type": "A"},
    # S (Sosyal) — 43-56
    {"id": 43, "text": "Başkalarına yardım etmekten ve onları desteklemekten hoşlanırım.", "type": "S"},
    {"id": 44, "text": "Öğretme veya eğitim verme konusunda tutkuluyum.", "type": "S"},
    {"id": 45, "text": "İnsanlarla çalışmayı ve onlarla etkileşimde bulunmayı severim.", "type": "S"},
    {"id": 46, "text": "Sosyal sorunlar ve toplumsal konular benim için önemlidir.", "type": "S"},
    {"id": 47, "text": "Danışmanlık ve rehberlik yapmaktan zevk alırım.", "type": "S"},
    {"id": 48, "text": "İyi bir dinleyiciyimdir ve insanlar sorunlarını benimle paylaşır.", "type": "S"},
    {"id": 49, "text": "Çocuklarla veya gençlerle çalışmaktan hoşlanırım.", "type": "S"},
    {"id": 50, "text": "Takım çalışması ve işbirliği benim için önemlidir.", "type": "S"},
    {"id": 51, "text": "İnsanları motive etmek ve teşvik etmek beni memnun eder.", "type": "S"},
    {"id": 52, "text": "Topluluk projeleri ve gönüllü faaliyetlere ilgi duyarım.", "type": "S"},
    {"id": 53, "text": "Başkalarının gelişimine katkı sağlamaktan mutluluk duyarım.", "type": "S"},
    {"id": 54, "text": "İnsanları anlayabilmek ve empati kurabilmek benim için kolaydır.", "type": "S"},
    {"id": 55, "text": "Sağlık hizmetleri veya sosyal hizmetler alanında çalışmak isterim.", "type": "S"},
    {"id": 56, "text": "Farklı kültürlerden ve geçmişlerden gelen insanlarla çalışmaktan hoşlanırım.", "type": "S"},
    # E (Girişimci) — 57-70
    {"id": 57, "text": "Başkalarını etkilemek ve ikna etmek benim için önemlidir.", "type": "E"},
    {"id": 58, "text": "Liderlik rolleri üstlenmekten ve sorumluluk almaktan hoşlanırım.", "type": "E"},
    {"id": 59, "text": "Girişimcilik ve iş kurmak benim için ilgi çekicidir.", "type": "E"},
    {"id": 60, "text": "Rekabetçi ortamlarda çalışmaktan zevk alırım.", "type": "E"},
    {"id": 61, "text": "Satış, pazarlama veya müzakere konularına ilgi duyarım.", "type": "E"},
    {"id": 62, "text": "Risk almak ve cesur kararlar vermek beni heyecanlandırır.", "type": "E"},
    {"id": 63, "text": "Proje yönetimi ve organizasyon konularında başarılıyımdır.", "type": "E"},
    {"id": 64, "text": "Sunum yapma ve kamuoyu önünde konuşma konusunda kendime güveniyorum.", "type": "E"},
    {"id": 65, "text": "Stratejik planlama ve uzun vadeli düşünmekten zevk alırım.", "type": "E"},
    {"id": 66, "text": "İş dünyasındaki gelişmeleri ve trendleri takip etmekten hoşlanırım.", "type": "E"},
    {"id": 67, "text": "Finansal konular ve yatırımlar ilgimi çeker.", "type": "E"},
    {"id": 68, "text": "Başkalarını harekete geçirmek ve motive etmek konusunda iyiyimdir.", "type": "E"},
    {"id": 69, "text": "Yeni iş fırsatları bulmak ve değerlendirmek beni heyecanlandırır.", "type": "E"},
    {"id": 70, "text": "Bir hedef belirleyip o hedefe ulaşmak için plan yapmaktan hoşlanırım.", "type": "E"},
    # C (Geleneksel) — 71-84
    {"id": 71, "text": "Verileri düzenlemek ve kayıt tutmaktan zevk alırım.", "type": "C"},
    {"id": 72, "text": "Belirli kurallara ve prosedürlere uymak benim için önemlidir.", "type": "C"},
    {"id": 73, "text": "Muhasebe ve finans konuları ilgimi çeker.", "type": "C"},
    {"id": 74, "text": "Düzenli ve sistematik bir çalışma ortamını tercih ederim.", "type": "C"},
    {"id": 75, "text": "Detaylara dikkat etmek ve hataları fark etmek konusunda iyiyimdir.", "type": "C"},
    {"id": 76, "text": "Hesap tabloları ve veritabanlarıyla çalışmaktan hoşlanırım.", "type": "C"},
    {"id": 77, "text": "Bürokrasi ve idari işler benim için anlamlıdır.", "type": "C"},
    {"id": 78, "text": "Kesin ve ölçülebilir sonuçlar üretmekten zevk alırım.", "type": "C"},
    {"id": 79, "text": "Rutinlere ve düzenli çalışma alışkanlıklarına sahip olmaktan hoşlanırım.", "type": "C"},
    {"id": 80, "text": "Ofis ortamında çalışmayı tercih ederim.", "type": "C"},
    {"id": 81, "text": "Bütçe planlaması ve maliyet analizi konularında başarılıyımdır.", "type": "C"},
    {"id": 82, "text": "Bilgileri doğru ve eksiksiz bir şekilde aktarmak benim için önemlidir.", "type": "C"},
    {"id": 83, "text": "Standartlara ve kalite kontrolüne önem veririm.", "type": "C"},
    {"id": 84, "text": "İdari ve destek hizmetleri alanında çalışmak isterim.", "type": "C"},
]


def calculate_holland(answers):
    """
    Holland RIASEC puanlama — 5'li Likert (0-4).
    Her tipten 14 soru, max puan: 14 × 4 = 56.
    """
    answers = {int(k): v for k, v in answers.items()}

    type_scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
    
    for q in HOLLAND_QUESTIONS:
        ans = answers.get(q["id"])
        if ans is not None:
            type_scores[q["type"]] += ans  # Gelen 0-4 puanını direkt ekle

    # Puana gore azalan, esitlikte RIASEC sirasini koruyan stabil siralama
    riasec_order = {"R": 0, "I": 1, "A": 2, "S": 3, "E": 4, "C": 5}
    sorted_types  = sorted(type_scores.items(), key=lambda x: (-x[1], riasec_order.get(x[0], 99)))
    top3          = sorted_types[:3]
    holland_code  = "".join(t[0] for t in top3)

    scores = {
        "R": type_scores["R"], "I": type_scores["I"],
        "A": type_scores["A"], "S": type_scores["S"],
        "E": type_scores["E"], "C": type_scores["C"],
        "holland_code": holland_code,
        "sorted_types": sorted_types,
        "top3": top3,
    }
    report = generate_holland_report(scores)
    return scores, report


def generate_holland_report(scores):
    top3         = scores["top3"]
    holland_code = scores["holland_code"]
    sorted_types = scores["sorted_types"]
    
    # Her tipten 14 soru var, max puan 4 olduğu için toplam 56 puan olur.
    max_per_type = 56 

    report = f"# 🧭 HOLLAND MESLEKİ İLGİ ENVANTERİ RAPORU\n\n**Senin Holland Kodun: {holland_code}**\n\n---\n\n## 📊 İlgi Profil Tablon\n\n| Tip | İsim | Puan | Yüzde | Grafik |\n|---|---|---|---|---|\n"

    for tkey, tscore in sorted_types:
        t   = HOLLAND_TYPES[tkey]
        pct = round(tscore / max_per_type * 100, 1) if max_per_type > 0 else 0
        n   = round(pct/10); bar = "█"*n + "░"*(10-n)
        report += f"| {t['icon']} {tkey} | {t['short']} | {tscore}/{max_per_type} | %{pct} | {bar} |\n"

    report += "\n---\n\n## 🌟 Holland Kodun Ne Anlama Geliyor?\n\n"
    report += f"**{holland_code}** kodu, seni en çok tanımlayan üç ilgi alanının birleşimidir.\n\n"

    medals = ["🥇","🥈","🥉"]
    for rank, (tkey, tscore) in enumerate(top3, 1):
        t   = HOLLAND_TYPES[tkey]
        pct = round(tscore / max_per_type * 100, 1) if max_per_type > 0 else 0
        report += f"### {medals[rank-1]} {rank}. Öncelik: {t['icon']} {t['name']} (%{pct})\n\n{t['description']}\n\n"
        report += "**Temel Özellikler:**\n" + "\n".join(f"- ✅ {c}" for c in t["characteristics"]) + "\n\n"
        report += f"**Öğrenme Ortamı:** {t['study_environment']}\n\n"
        report += "**Kariyer Önerileri:**\n" + "\n".join(f"- 🎯 {c}" for c in t["careers"]) + "\n\n---\n\n"

    report += """## 💡 Kariyer Seçiminde Holland Kodunu Kullanmak

Holland kodun, sana en uygun meslekleri belirlemende güçlü bir rehber!

**Unutma:**
- 🔍 En uygun meslekler, kodu tam olarak veya kısmen eşleşenlerdir.
- 🎯 Holland kodu bir kader değil, bir yol haritasıdır.
- 🌱 İlgi alanların zaman içinde değişebilir ve gelişebilir.
- 💪 Güçlü ilgi alanların, o alanda başarılı olma ihtimalini artırır.

---

## 💬 Son Söz
Holland teorisine göre insanlar iş ortamlarını, kendi kişilikleriyle en uyumlu çevreleri seçmeye çalışırlar. Kişilik-çevre uyumu ne kadar yüksek olursa, iş tatmini ve başarı da o kadar yüksek olur. Kendi koduna uygun bir kariyer yolu seçmek, hem mutlu hem başarılı olmanın anahtarıdır! 🚀"""
    return report.strip()


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
        "work_style": "Net kuralları, standartları ve beklentileri olan yapılandırılmış ortamlarda parlıyorsun. Kalite kontrol, hukuk, eğitim, tıp, muhasebe gibi titizlik ve etik gerektiren alanlarda doğal olarak güçlüsün. Kaotik veya kuralsız ortamlar seni strese sokar.",
        "relationship_style": "İlişkilerinde dürüstlük, sadakat ve tutarlılık ararsın. Söz verilip tutulmaması veya haksızlık seni derinden yaralar. Bazen yüksek beklentilerin partnerin veya arkadaşların üzerinde baskı oluşturabilir. Sevildiğini görmek için 'mükemmel' olmana gerek olmadığını hatırlatmak gerekiyor.",
        "stress_behavior": "Stres altında Tip 4'e (Bireyci) kayarsın: melankolik, kendini geri çeken, duygusal açıdan kapalı biri haline gelebilirsin. Eleştirini kendine yöneltirsin ve 'Hiçbir şeyi doğru yapamıyorum' hissine kapılabilirsin.",
        "growth_behavior": "Gelişim yolunda Tip 7'ye (Hevesli) yönelirsin: daha oyuncu, daha esnek ve daha neşeli biri olursun. Hayatın güzelliklerini fark edip, 'Yeterince iyi' diyebildiğinde gerçek huzuru bulursun.",
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
        "desc": "Sen dünyaya 'İnsanlara yardım etmeli ve onları sevmeliyim' gözlüğüyle bakıyorsun. Başkalarının ihtiyaçlarını kendi ihtiyaçlarından önce görme konusunda adeta bir antene sahipsin — odaya girer girmez kimin üzgün olduğunu, kimin desteğe ihtiyaç duyduğunu hissedebilirsin. Bu empatin ve cömertliğin seni insanların çok değer verdiği biri yapıyor. Ancak bazen kendi ihtiyaçlarını o kadar arka plana atıyorsun ki, zamanla tükenmişlik ve kırgınlık sinyalleri vermeye başlayabiliyor.",
        "strengths": ["Derin empati", "Koşulsuz destek", "Sosyal zeka", "Cömertlik", "Sıcaklık ve bağlanma"],
        "weaknesses": ["'Hayır' diyememek", "Kendi ihtiyaçlarını görmezden gelme", "Takdir görmek isteme", "Duygusal manipülasyon riski", "Başkalarına bağımlılık"],
        "work_style": "İnsan odaklı, ilişki kurma gerektiren işlerde parıldıyorsun.",
        "relationship_style": "İlişkilerinde derin bağ ve karşılıklı şefkat ararsın.",
        "stress_behavior": "Stres altında Tip 8'e kayarsın: kontrolcü ve talep edici hale gelebilirsin.",
        "growth_behavior": "Gelişim yolunda Tip 4'e yönelirsin: kendi duygularını keşfetmeye başlarsın.",
        "danger_signals": ["Sürekli başkalarının ihtiyaçlarını düşünmek", "'Beni kimse görmüyor' hissi", "Yardımını takdir etmeyeni cezalandırmak", "Tükenmişliği inkâr etmek"],
        "prescription": ["🌱 Kendin için bir şey yap", "🗣️ İhtiyacını dile getir", "⛔ Hayır pratiği", "🪞 İçe dön"],
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
        "desc": "Sen dünyaya 'Başarılı olmalı ve değer kanıtlamalıyım' gözlüğüyle bakıyorsun. Hedef koymak, strateji geliştirmek ve o hedefe doğru ilerlemek seni canlı tutuyor.",
        "strengths": ["Hedef odaklılık", "Enerji ve motivasyon", "Adaptasyon yeteneği", "Verimlilik", "Liderlik karizması"],
        "weaknesses": ["Kimlik-başarı karışıklığı", "Duyguları erteleme", "İmaj kaygısı", "Aşırı iş yükü", "İlişkileri proje gibi yönetme"],
        "work_style": "Rekabetçi, ölçülebilir başarı kriterleri olan ortamlarda parıldıyorsun.",
        "relationship_style": "İlişkilerinde hayranlık ve takdir önemlidir.",
        "stress_behavior": "Stres altında Tip 9'a kayarsın: hareketsizleşir ve içine kapanabilirsin.",
        "growth_behavior": "Gelişim yolunda Tip 6'ya yönelirsin: daha sadık ve dürüst olursun.",
        "danger_signals": ["Dinlenmenin boşa harcanan zaman gibi gelmesi", "Başarısızlık karşısında savunmacı olmak", "Gerçek hislerini 'verimli olmayan şey' görmek", "İlişkilerde statüyü ön plana koymak"],
        "prescription": ["🧘 Dur ve hisset", "🎭 Maske indir", "🏅 Başarısız olmayı dene", "❤️ Koşulsuz bağ"],
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
        "desc": "Sen dünyaya 'Ben farklıyım ve bu farkı anlamlı kılmalıyım' gözlüğüyle bakıyorsun. Duyguların yoğunluğu ve derinliği seni hem çok zengin hem de bazen çok ağır bir iç dünyaya sürüklüyor.",
        "strengths": ["Derin duygusal zeka", "Yaratıcılık ve estetik duyarlılık", "Otantiklik", "Empati derinliği", "Anlam arayışı"],
        "weaknesses": ["Melankoli ve hüzne gömülme", "Kendini eksik hissetme", "Dramatizasyon eğilimi", "Günlük rutine direnç", "İlişkilerde idealizm"],
        "work_style": "Yaratıcı özgürlük sunan, anlam ve estetik barındıran işlerde parıldıyorsun.",
        "relationship_style": "Derin, tutkulu ve anlam dolu bağlar ararsın.",
        "stress_behavior": "Stres altında Tip 2'ye kayarsın: başkalarına aşırı yönelirsin.",
        "growth_behavior": "Gelişim yolunda Tip 1'e yönelirsin: disiplin ve yapıya kavuşursun.",
        "danger_signals": ["Uzun süre hüzün içinde kalmak", "Başkalarını idealleştirip yıkılmak", "Sorumluluklardan kaçmak", "İzolasyona çekilmek"],
        "prescription": ["🌱 Rutini benimse", "🚶 Bedenle bağlan", "📓 Minnet listesi", "🛠️ Tamamla"],
        "famous_examples": "Frida Kahlo, Virginia Woolf, Bob Dylan",
        "careers": ["Sanatçı", "Yazar", "Terapist", "Tasarımcı", "Müzisyen", "Fotoğrafçı"],
    },
    5: {
        "title": "Tip 5: Araştırmacı",
        "role": "Gözlemci, Uzman",
        "icon": "🔬",
        "fear": "Yetersiz olmak, kaynaklarının tükenmesi.",
        "desire": "Yetkin, bilgili ve çevresini anlayan biri olmak.",
        "stress": 7, "growth": 8,
        "desc": "Sen dünyaya 'Önce anlamalıyım, sonra hareket ederim' gözlüğüyle bakıyorsun. Zihnin sürekli merakla dolu.",
        "strengths": ["Derin analitik düşünme", "Uzmanlık", "Bağımsızlık", "Gözlem gücü", "Sakinlik"],
        "weaknesses": ["İzolasyon", "Eylemden kaçınma", "Duygusal kopukluk", "Cimrilik (enerji/bilgi/zaman)", "Sosyal yorgunluk"],
        "work_style": "Bağımsız çalışma ve uzmanlık gerektiren ortamlarda güçlüsün.",
        "relationship_style": "Bağımsızlığına saygı duyan, entelektüel derinliği olan birini ararsın.",
        "stress_behavior": "Stres altında Tip 7'ye kayarsın: dağınık ve hiperaktif olabilirsin.",
        "growth_behavior": "Gelişim yolunda Tip 8'e yönelirsin: harekete geçer, liderlik edebilirsin.",
        "danger_signals": ["İnsanlardan uzak kalmak", "Bilgi toplamayı eyleme tercih etmek", "Hisleri analiz etmek", "Sosyal iletişimi gereksiz görmek"],
        "prescription": ["🤝 Bağlan", "⚡ Harekete geç", "💬 Hislerini söyle", "🌍 Dışarı çık"],
        "famous_examples": "Albert Einstein, Stephen Hawking, Bill Gates",
        "careers": ["Araştırmacı", "Yazılımcı", "Mühendis", "Analist", "Akademisyen", "Yazar"],
    },
    6: {
        "title": "Tip 6: Sadık",
        "role": "Sorgulayıcı, Güvenilir",
        "icon": "🛡️",
        "fear": "Güvensizlik, yalnız kalmak ve desteğini kaybetmek.",
        "desire": "Güvende olmak, güvenilir ilişkilere sahip olmak.",
        "stress": 3, "growth": 9,
        "desc": "Sen dünyaya 'Güvende miyim? Güvenebilir miyim?' gözlüğüyle bakıyorsun.",
        "strengths": ["Sadakat", "Sorumluluk", "Risk analizi", "Ekip ruhu", "Soru sorma cesareti"],
        "weaknesses": ["Aşırı kaygı", "Kararsızlık", "Güvensizlik", "Felaket senaryoları", "Otoriteyle çelişki"],
        "work_style": "Net roller ve güvenilir yapıların olduğu ortamlarda güçlüsün.",
        "relationship_style": "Sadakat ve güven senin için ilişkinin temeli.",
        "stress_behavior": "Stres altında Tip 3'e kayarsın: aşırı çalışır, performans odaklı olursun.",
        "growth_behavior": "Gelişim yolunda Tip 9'a yönelirsin: zihin sakinleşir, huzur bulursun.",
        "danger_signals": ["Kötü senaryo düşünerek karar verememek", "Güvendiğin insanları test etmek", "Fiziksel kaygı belirtileri", "Otoriteye hem muhtaç hem öfkeli hissetmek"],
        "prescription": ["🧘 Zihni durdur", "💪 İçgüdüne güven", "✅ Tamamlananları gör", "🤲 Destek iste"],
        "famous_examples": "Barack Obama, Ellen DeGeneres, Malala Yousafzai",
        "careers": ["Avukat", "Risk analisti", "Güvenlik uzmanı", "Muhasebeci", "Polis memuru", "Danışman"],
    },
    7: {
        "title": "Tip 7: Hevesli",
        "role": "Maceracı, Vizyoner",
        "icon": "🚀",
        "fear": "Acı çekmek, kısıtlanmak ve eğlencesiz hayat.",
        "desire": "Mutlu, özgür ve doyumsuz bir hayat sürmek.",
        "stress": 1, "growth": 5,
        "desc": "Sen dünyaya 'Hayat güzel olmalı ve ben her şeyi deneyimlemeliyim' gözlüğüyle bakıyorsun.",
        "strengths": ["Sınır tanımayan iyimserlik", "Hızlı öğrenme", "Yaratıcılık ve yenilikçilik", "Enerji ve coşku", "Esneklik"],
        "weaknesses": ["Odaklanma güçlüğü", "Acıdan kaçma", "Söz verip tutamamak", "Derinleşme güçlüğü", "Anlık tatmin"],
        "work_style": "Çeşitlilik, yaratıcılık ve hareket sunan ortamlarda parıldıyorsun.",
        "relationship_style": "Eğlenceli, spontane ve macera dolu ilişkiler ararsın.",
        "stress_behavior": "Stres altında Tip 1'e kayarsın: eleştirel ve mükemmeliyetçi olursun.",
        "growth_behavior": "Gelişim yolunda Tip 5'e yönelirsin: derinleşir ve odaklanırsın.",
        "danger_signals": ["Projeleri yarım bırakmak", "Sürekli meşguliyet arayışı", "Duygusal derinlikten kaçmak", "Bağlanmaktan kaçınmak"],
        "prescription": ["🎯 Bir şeyi bitir", "🌑 Karanlıkla otur", "📅 Derinleş", "🤝 Söz tut"],
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
        "desc": "Sen dünyaya 'Ben güçlü olmalıyım ve kontrol bendeyken herkes güvende' gözlüğüyle bakıyorsun.",
        "strengths": ["Liderlik gücü", "Karar alma hızı", "Adalet duygusu", "Güç ve dayanıklılık", "Dürüstlük"],
        "weaknesses": ["Kırılganlığı reddetme", "Baskıcılık", "Öfkenin ani çıkması", "Dinleme güçlüğü", "İktidar mücadelesi"],
        "work_style": "Liderlik ve bağımsızlık sunan ortamlarda güçlüsün.",
        "relationship_style": "Tutkulu, sadık ve koruyucu bir partner olursun.",
        "stress_behavior": "Stres altında Tip 5'e kayarsın: içine çekilir, izole olursun.",
        "growth_behavior": "Gelişim yolunda Tip 2'ye yönelirsin: şefkat açılır, kırılgan olabilirsin.",
        "danger_signals": ["Her şeyin kontrolde olması gerektiği hissi", "İnsanların senden korkması", "Duygusal kapıları kapatmak", "İlişkileri feda etmek"],
        "prescription": ["🤍 Kırılgan ol", "👂 Dinle", "🌿 Kontrol bırak", "❤️ Şefkat yönelt"],
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
        "desc": "Sen dünyaya 'Herkes iyi olsun, uyum bozulmasın' gözlüğüyle bakıyorsun.",
        "strengths": ["Doğal arabuluculuk", "Sabır ve anlayış", "Güven verme", "Empati", "İstikrar"],
        "weaknesses": ["Kendi sesini kaybetme", "Erteleme", "Pasif-agresif tepkiler", "Önceliklendirme güçlüğü", "Dışsal uyaranlara bağımlılık"],
        "work_style": "İşbirliği gerektiren, uyum içinde çalışılan ortamlarda güçlüsün.",
        "relationship_style": "Destekleyici, uyumlu ve sakin bir bağ ararsın.",
        "stress_behavior": "Stres altında Tip 6'ya kayarsın: kaygılanır ve güvensizleşirsin.",
        "growth_behavior": "Gelişim yolunda Tip 3'e yönelirsin: harekete geçer ve hedefler belirlersin.",
        "danger_signals": ["İsteklerini bastırmak", "Kararları ertelemek", "İçine atmak", "Kendininkinde pasif olmak"],
        "prescription": ["🗣️ Sesini çıkar", "⚡ Bir adım at", "📋 Önceliklendir", "🔍 Çatışmaya gir"],
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
