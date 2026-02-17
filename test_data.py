# ============================================================
# TEST_DATA.PY — Tüm Psikolojik Testlerin Sabit Verileri
# 
# Bu dosya student_view.py ve teacher_view.py tarafından import edilir.
# İçerik:
#   1. Sağ-Sol Beyin Testi (30 soru)
#   2. Çalışma Davranışı Ölçeği (73 soru)
#   3. Sınav Kaygısı Ölçeği (50 soru)
#   4. Çoklu Zeka Testi (Lise 80 + İlköğretim 40 soru)
#   5. VARK Öğrenme Stilleri (16 soru)
#   6. Holland RIASEC (84 soru)
#
# Enneagram verileri student_view.py'de mevcut kalacak.
# ============================================================

# ============================================================
# PARÇA 1: SAĞ-SOL BEYİN ÜSTÜNLÜĞÜ TESTİ
# Kaynak: Dr. Loren D. Crane, "Alert Scale of Cognitive Style"
# Western Michigan University, 1989
# + Firma sahibinin belgesi + ek davranışsal sorular
# ============================================================

# --- SABİT SORULAR (30 ADET) ---
# Her soru: id, text (soru metni), a (sağ beyin seçeneği), b (sol beyin seçeneği)
# Puanlama: Bazı sorularda A = sağ beyin, bazılarında B = sağ beyin
# "right_answer" alanı: "a" ise A seçeneği sağ beyin puanı verir, "b" ise B seçeneği

SAG_SOL_BEYIN_QUESTIONS = [
    # --- Orijinal Alert Scale (Crane, 1989) — Türkçe Uyarlama (21 soru) ---
    {
        "id": 1,
        "text": "Aşağıdakilerden hangisi sana daha çok uyuyor?",
        "a": "Risk almak eğlencelidir, heyecan verir.",
        "b": "Risk almadan da gayet iyi eğlenebilirim.",
        "right_brain": "a"
    },
    {
        "id": 2,
        "text": "Bir işi yaparken nasıl davranırsın?",
        "a": "Eski işleri yapmak için sürekli yeni yollar ararım.",
        "b": "Bir yol iyi çalışıyorsa onu değiştirmem, aynen devam ederim.",
        "right_brain": "a"
    },
    {
        "id": 3,
        "text": "İşlerini bitirme konusunda hangisi seni daha iyi tanımlar?",
        "a": "Birçok işe başlarım ama hepsini bitiremeyebilirim.",
        "b": "Bir işi bitirmeden kesinlikle yenisine başlamam.",
        "right_brain": "a"
    },
    {
        "id": 4,
        "text": "Hayal gücünü kullanma konusunda nasılsın?",
        "a": "İşlerimde çok fazla hayal gücü kullanmam, gerçekçiyimdir.",
        "b": "Her işimde mutlaka hayal gücümü kullanırım.",
        "right_brain": "b"
    },
    {
        "id": 5,
        "text": "Gelecekte ne olacağını tahmin ederken hangisini kullanırsın?",
        "a": "Olayları analiz ederek ne olacağını tahmin ederim.",
        "b": "İçimden gelen hisle ne olacağını hissederim.",
        "right_brain": "b"
    },
    {
        "id": 6,
        "text": "Bir problemle karşılaştığında nasıl çözersin?",
        "a": "En iyi tek çözümü bulmaya çalışırım.",
        "b": "Birden fazla farklı çözüm yolu ararım.",
        "right_brain": "b"
    },
    {
        "id": 7,
        "text": "Düşüncelerin kafanın içinde nasıl akar?",
        "a": "Düşüncelerim resimler ve görüntüler gibi akar.",
        "b": "Düşüncelerim kelimeler ve cümleler gibi akar.",
        "right_brain": "a"
    },
    {
        "id": 8,
        "text": "Yeni fikirler karşısında nasıl tepki verirsin?",
        "a": "Yeni fikirleri başkalarından önce kabul ederim.",
        "b": "Yeni fikirleri başkalarından çok sorgularım.",
        "right_brain": "a"
    },
    {
        "id": 9,
        "text": "Düzenin hakkında ne derler?",
        "a": "Başkaları benim düzenimi anlamaz ama bana göre düzenlidir.",
        "b": "Başkaları benim çok düzenli olduğumu söyler.",
        "right_brain": "a"
    },
    {
        "id": 10,
        "text": "Disiplin konusunda kendini nasıl tanımlarsın?",
        "a": "İyi bir öz disiplinim vardır, kendimi kontrol ederim.",
        "b": "Genellikle duygularıma ve içgüdülerime göre hareket ederim.",
        "right_brain": "b"
    },
    {
        "id": 11,
        "text": "İş yaparken zamanı nasıl kullanırsın?",
        "a": "Zamanımı önceden planlarım.",
        "b": "İş yaparken zamanı pek düşünmem, akar gider.",
        "right_brain": "b"
    },
    {
        "id": 12,
        "text": "Zor bir karar vermek gerektiğinde ne yaparsın?",
        "a": "Doğru bildiğimi, mantığıma uygun olanı seçerim.",
        "b": "Kalbimin ve hislerimin söylediğini seçerim.",
        "right_brain": "b"
    },
    {
        "id": 13,
        "text": "İşlerini hangi sırayla yaparsın?",
        "a": "Kolay işleri önce, önemli işleri sonra yaparım.",
        "b": "Önemli işleri önce, kolay işleri sonra yaparım.",
        "right_brain": "a"
    },
    {
        "id": 14,
        "text": "Yeni bir durumla karşılaştığında ne olur?",
        "a": "Kafamda çok fazla fikir uçuşur, hangisini seçeceğimi bilemem.",
        "b": "Bazen hiç fikrim olmaz, ne yapacağımı düşünmem gerekir.",
        "right_brain": "a"
    },
    {
        "id": 15,
        "text": "Yeni fikirler hakkında hangisi seni anlatır?",
        "a": "Yeni fikirleri çok sorgularım, kanıt isterim.",
        "b": "Yeni fikirlere açığımdır, hemen denerim.",
        "right_brain": "b"  
    },
    {
        "id": 16,
        "text": "Hayatında değişiklik konusunda ne düşünürsün?",
        "a": "Hayatımda çok değişiklik ve çeşitlilik isterim.",
        "b": "Düzenli ve planlı bir hayat tercih ederim.",
        "right_brain": "a"
    },
    {
        "id": 17,
        "text": "Haklı olduğunu nasıl bilirsin?",
        "a": "Haklı olduğumu bilirim çünkü iyi nedenlerim ve kanıtlarım vardır.",
        "b": "Haklı olduğumu hissederim, bazen nedenim olmasa bile.",
        "right_brain": "b"
    },
    {
        "id": 18,
        "text": "İşlerini zamana nasıl yayarsın?",
        "a": "İşlerimi zamana eşit olarak yayarım.",
        "b": "İşlerimi son dakikada yapmayı tercih ederim.",
        "right_brain": "b"
    },
    {
        "id": 19,
        "text": "Eşyalarını nereye koyarsın?",
        "a": "Her şeyi belirli bir yere koyarım, hep aynı yer.",
        "b": "Eşyalarımın yeri o an ne yaptığıma göre değişir.",
        "right_brain": "b"
    },
    {
        "id": 20,
        "text": "Hangisi seni daha iyi tanımlar?",
        "a": "Tutarlıyımdır, ne yapacağım bellidir.",
        "b": "Spontaneyimdir, anlık kararlar verir sürprizleri severim.",
        "right_brain": "b"
    },
    {
        "id": 21,
        "text": "Çalışma ortamın nasıl olmalı?",
        "a": "Düzenli ve tertipli bir ortamda çalışmalıyım.",
        "b": "Rahat hissettiğim, esnek bir ortamda çalışırım.",
        "right_brain": "b"
    },
    # --- Firma Belgesinden Uyarlanan Sorular (4 soru) ---
    {
        "id": 22,
        "text": "Okulda hangi tür dersleri daha çok seversin?",
        "a": "Türkçe, resim, müzik gibi sözel ve sanatsal dersler.",
        "b": "Matematik, fen bilgisi gibi sayısal dersler.",
        "right_brain": "a"
    },
    {
        "id": 23,
        "text": "Hangi tür sporları tercih edersin?",
        "a": "Tek başına yapılan sporlar (yüzme, koşu, bisiklet).",
        "b": "Takım sporları (basketbol, voleybol, futbol).",
        "right_brain": "a"
    },
    {
        "id": 24,
        "text": "Gördüğün rüyaları hatırlar mısın?",
        "a": "Evet, rüyalarımı çoğu zaman canlı ve detaylı hatırlarım.",
        "b": "Hayır, rüyalarımı nadiren hatırlarım.",
        "right_brain": "a"
    },
    {
        "id": 25,
        "text": "Konuşurken ellerini ve yüz ifadelerini nasıl kullanırsın?",
        "a": "Çok fazla el kol hareketi ve mimik kullanırım.",
        "b": "Çok az hareket yaparım, sakin konuşurum.",
        "right_brain": "a"
    },
    # --- Ek Davranışsal Sorular (5 soru) ---
    {
        "id": 26,
        "text": "Bir hikaye anlatırken nasıl anlatırsın?",
        "a": "Olayları sırasıyla, baştan sona düzgünce anlatırım.",
        "b": "Aklıma geldiği gibi, renkli detaylar ve duygular katarak anlatırım.",
        "right_brain": "b"
    },
    {
        "id": 27,
        "text": "İnsanları tanırken neyi daha çabuk hatırlarsın?",
        "a": "İnsanların yüzlerini ve görünüşlerini hatırlarım.",
        "b": "İnsanların isimlerini ve söylediklerini hatırlarım.",
        "right_brain": "a"
    },
    {
        "id": 28,
        "text": "Bir şey öğrenirken hangisini tercih edersin?",
        "a": "Resim, grafik, şema gibi görsellerle öğrenmek.",
        "b": "Yazılı metin okuyarak ve not alarak öğrenmek.",
        "right_brain": "a"
    },
    {
        "id": 29,
        "text": "Odanın düzeni hakkında ne düşünürsün?",
        "a": "Odamdaki eşyaların her zaman aynı yerde ve düzenli durmasını isterim.",
        "b": "Odamda yaratıcı bir dağınıklık vardır, ama ben nereye ne koyduğumu bilirim.",
        "right_brain": "b"
    },
    {
        "id": 30,
        "text": "Birinin yalan söylediğini nasıl anlarsın?",
        "a": "Söylediklerindeki çelişkileri ve mantık hatalarını yakalarım.",
        "b": "Yüz ifadesinden ve ses tonundan hissederim, sezgilerime güvenirim.",
        "right_brain": "b"
    },
]

# --- SAĞ VE SOL BEYİN ÖZELLİK VERİLERİ ---
SAG_SOL_BEYIN_DATA = {
    "sag": {
        "title": "Sağ Beyin Baskın",
        "icon": "🎨",
        "description": "Sen dünyaya daha çok duygularınla, sezgilerinle ve hayal gücünle bakan birisin. Yaratıcılık senin süper gücün!",
        "strengths": [
            "Güçlü hayal gücü ve yaratıcılık",
            "Sezgileri kuvvetli, insanları iyi okur",
            "Sanatsal ve görsel yetenekler",
            "Bütüncül düşünme (büyük resmi görme)",
            "Empati ve duygusal zeka",
            "Esnek ve spontane düşünme"
        ],
        "development_areas": [
            "Zaman yönetimi ve planlama becerilerini geliştirebilirsin",
            "Detaylara daha fazla dikkat edebilirsin",
            "Başladığın işleri bitirme konusunda kendine hedefler koyabilirsin",
            "Düzenli çalışma alışkanlıkları edinebilirsin"
        ],
        "study_tips": [
            "Ders çalışırken renkli kalemler, zihin haritaları (mind map) ve şemalar kullan.",
            "Konuları hikayeleştirerek veya görselleştirerek öğren.",
            "Müzik dinleyerek çalışmak sana iyi gelebilir (sözsüz müzik dene).",
            "Uzun çalışma seansları yerine kısa ama yaratıcı molalar ver.",
            "Grup çalışmalarında fikirlerini paylaşmaktan çekinme, farklı bakış açın değerli."
        ],
        "career_areas": [
            "Sanat ve Tasarım", "Müzik", "Edebiyat ve Yazarlık",
            "Psikoloji", "Mimarlık", "Reklamcılık", "Fotoğrafçılık",
            "Oyun Tasarımı", "Film ve Sinema"
        ]
    },
    "sol": {
        "title": "Sol Beyin Baskın",
        "icon": "🔬",
        "description": "Sen dünyaya daha çok mantığınla, analizlerinle ve sistemli düşünmenle bakan birisin. Analitik güç senin süper gücün!",
        "strengths": [
            "Güçlü analitik ve mantıksal düşünme",
            "Detaylara dikkat ve titizlik",
            "İyi planlama ve organizasyon",
            "Matematiksel ve sayısal beceriler",
            "Disiplinli ve tutarlı çalışma",
            "Dil ve sözel ifade becerileri"
        ],
        "development_areas": [
            "Yaratıcı düşünme ve hayal gücünü geliştirebilirsin",
            "Duygularını ifade etme konusunda daha rahat olabilirsin",
            "Spontane ve esnek olmayı deneyebilirsin",
            "Büyük resmi görmek için adım geri atabilirsin"
        ],
        "study_tips": [
            "Konuları sıralı ve adım adım çalış, listeler ve özetler çıkar.",
            "Formüller, kurallar ve kalıplar senin en iyi arkadaşın.",
            "Sessiz ve düzenli bir çalışma ortamı oluştur.",
            "Zaman planı yap ve ona sadık kal — bu seni güçlü kılar.",
            "Her konunun 'neden' ve 'nasıl' sorularını sor, derinlemesine anla."
        ],
        "career_areas": [
            "Mühendislik", "Tıp", "Hukuk", "Bilgisayar Bilimi",
            "Muhasebe ve Finans", "Bilimsel Araştırma", "Matematik",
            "Programlama", "Bankacılık"
        ]
    },
    "dengeli": {
        "title": "Dengeli Beyin",
        "icon": "⚖️",
        "description": "Sen hem yaratıcı hem de analitik tarafını dengeli kullanan birisin. Bu çok özel ve güçlü bir kombinasyon!",
        "strengths": [
            "Hem yaratıcı hem analitik düşünebilme",
            "Farklı durumlarına uyum sağlama esnekliği",
            "Hem detayları hem büyük resmi görebilme",
            "Dengeli karar verme yeteneği",
            "Farklı insanlarla iyi iletişim kurabilme",
            "Çok yönlü problem çözme becerisi"
        ],
        "development_areas": [
            "Bazen hangi tarafını kullanacağına karar vermekte zorlanabilirsin",
            "Bir alanda uzmanlaşmak için bilinçli tercihler yapabilirsin",
            "Güçlü yönlerini keşfetmek için farklı alanları denemeye devam et"
        ],
        "study_tips": [
            "Hem görsel hem yazılı materyalleri birlikte kullan.",
            "Bazen planlı, bazen serbest çalışmayı dene — ikisi de sana uyar.",
            "Hem bireysel hem grup çalışmalarından verim alabilirsin.",
            "Farklı ders çalışma tekniklerini dönüşümlü kullan.",
            "Güçlü olduğun tarafı keşfet ve onu bilinçli geliştir."
        ],
        "career_areas": [
            "Girişimcilik", "Proje Yönetimi", "Eğitim ve Öğretmenlik",
            "Danışmanlık", "İletişim ve Medya", "Araştırma-Geliştirme",
            "Mühendislik Tasarımı", "Ürün Geliştirme"
        ]
    }
}

# --- PUANLAMA FONKSİYONU ---
def calculate_sag_sol_beyin(answers):
    """
    Sağ-Sol Beyin testini puanlar.
    
    Args:
        answers: dict — {soru_id: "a" veya "b"}
        Örnek: {1: "a", 2: "b", 3: "a", ...}
    
    Returns:
        (scores_dict, report_text)
        scores_dict: {"sag_beyin": int, "sol_beyin": int, "dominant": str}
    """
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
    
    total = sag_puan + sol_puan
    if total == 0:
        total = 1  # Sıfıra bölme koruması
    
    sag_yuzde = round(sag_puan / total * 100, 1)
    sol_yuzde = round(sol_puan / total * 100, 1)
    
    # Baskınlık belirleme (5 kademe — Crane ölçeği uyarlaması)
    # 30 soru için orantılı aralıklar:
    # Güçlü Sol: 0-5 sağ puan | Orta Sol: 6-11 | Dengeli: 12-18 | Orta Sağ: 19-24 | Güçlü Sağ: 25-30
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
        "level": level
    }
    
    report = generate_sag_sol_beyin_report(scores)
    
    return scores, report


def generate_sag_sol_beyin_report(scores):
    """
    Sağ-Sol Beyin testi için şablon tabanlı rapor üretir.
    Dil: Türkçe, çocuk/ergen dostu, sıcak ve cesaretlendirici.
    """
    dominant = scores["dominant"]
    data = SAG_SOL_BEYIN_DATA[dominant]
    
    sag = scores["sag_beyin"]
    sol = scores["sol_beyin"]
    sag_y = scores["sag_yuzde"]
    sol_y = scores["sol_yuzde"]
    level = scores["level"]
    
    # Progress bar karakterleri
    sag_bar_len = round(sag_y / 10)
    sol_bar_len = round(sol_y / 10)
    sag_bar = "█" * sag_bar_len + "░" * (10 - sag_bar_len)
    sol_bar = "█" * sol_bar_len + "░" * (10 - sol_bar_len)
    
    # Güçlü yönler listesi
    strengths_text = "\n".join([f"- ✅ {s}" for s in data["strengths"]])
    
    # Gelişim alanları
    dev_text = "\n".join([f"- 🌱 {d}" for d in data["development_areas"]])
    
    # Çalışma ipuçları
    tips_text = "\n".join([f"- 💡 {t}" for t in data["study_tips"]])
    
    # Kariyer alanları
    career_text = ", ".join(data["career_areas"])
    
    report = f"""
# {data['icon']} SAĞ-SOL BEYİN ÜSTÜNLÜĞÜ RAPORU

**Sonucun:** {level}

---

## 📊 Puan Tablon

| Beyin Yarımküresi | Puan | Yüzde | Grafik |
|---|---|---|---|
| 🎨 Sağ Beyin | {sag}/30 | %{sag_y} | {sag_bar} |
| 🔬 Sol Beyin | {sol}/30 | %{sol_y} | {sol_bar} |

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

Unutma, sağ beyin veya sol beyin baskın olmak iyi ya da kötü değildir! Her ikisi de harika süper güçlerdir. Önemli olan kendi güçlü tarafını tanımak ve onu en iyi şekilde kullanmaktır. Aynı zamanda diğer tarafını da geliştirerek daha da güçlenebilirsin! 🌟
"""
    return report.strip()


# ============================================================
# TEST: Örnek kullanım ve doğrulama
# ============================================================


# ============================================================
# PARÇA 2: ÇALIŞMA DAVRANIŞI DEĞERLENDİRME ÖLÇEĞİ (BALTAŞ)
# Kaynak: Firma sahibinin standart belgesi
# 73 soru, 7 kategori, Doğru/Yanlış formatı
# Puanlama: Cevap anahtarına UYMAYAN cevap sayısı = puan
# ============================================================

# --- SABİT SORULAR (73 ADET) ---
# Her soru: id, text, category (A-G), key ("D" veya "Y")
# key = doğru cevap anahtarı
# Puanlama: Öğrencinin cevabı anahtara UYMUYORSA → 1 puan (o kategoride)

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

# --- KATEGORİ TANIMLARI VE CEVAP ANAHTARI ---
CALISMA_DAVRANISI_CATEGORIES = {
    "A": {
        "name": "Çalışmaya Başlamak ve Sürdürmek",
        "question_ids": [13, 30, 40, 49, 15, 32, 43, 55, 17, 37, 44, 67, 18, 39, 48, 70],
        "max_score": 16,
        "interpretations": {
            "high": {
                "range": (10, 16),
                "text": "Ders çalışmaya başlamak ve zamanından etkin bir şekilde yararlanmak konusunda ciddi güçlüklerin olduğu görülüyor. Değerli zamanının önemli bir bölümünü ders çalışman gerektiğini düşünerek ya da ders başında ama çalışmadan geçirdiğin anlaşılıyor. Başarını yükseltebilmek için mutlaka ders çalışmaya başlamak ve sürdürmek konusundaki teknikleri ve iç disiplinini kurmayı öğrenmen gerekiyor.",
                "tips": [
                    "Her gün aynı saatte ders çalışmaya başla — bu bir alışkanlık yaratır.",
                    "Çalışmaya başlamadan önce masanı hazırla ve dikkat dağıtıcıları kaldır.",
                    "Pomodoro tekniğini dene: 25 dakika çalış, 5 dakika mola ver.",
                    "Küçük hedefler koy: 'Bu akşam 2 sayfa çözeceğim' gibi somut planlar yap."
                ]
            },
            "mid": {
                "range": (5, 9),
                "text": "Ders çalışmaya başlamak ve sürdürmek konusunda bazı güçlüklerin olduğu anlaşılıyor. Eğlenmeye ve dinlenmeye de vakit ayırabilmek için derse ayırdığın zamandan en etkin şekilde yararlanman gerekiyor. Kendi üzerinde denetim kuracak yöntemleri öğrenirsen hem sosyalleşmeye zaman ayırabilir, hem de başarını yükseltebilirsin.",
                "tips": [
                    "Çalışma ve eğlence saatlerini önceden planla.",
                    "Telefonu çalışma saatlerinde sessize al veya başka odaya koy.",
                    "Çalışma arkadaşı bul — birlikte çalışmak motivasyonu artırır."
                ]
            },
            "low": {
                "range": (0, 4),
                "text": "Ders çalışmaya başlamak ve sürdürmek konusunda önemli bir güçlüğün olmadığı anlaşılıyor. Hem ders çalışmaya ayırdığın zamandan en üst düzeyde yararlanman mümkün oluyor, hem de özel hayatına ve zevklerine zaman ayırabiliyorsun. Kendini iyi denetleyebilen bir insan olduğun için seni kutlarız! 🎉",
                "tips": []
            }
        }
    },
    "B": {
        "name": "Bilinçli Çalışmak ve Öğrendiğini Kullanmak",
        "question_ids": [12, 19, 47, 14, 38, 50, 16, 42, 51],
        "max_score": 9,
        "interpretations": {
            "high": {
                "range": (5, 9),
                "text": "Bilinçli çalışmak ve öğrendiğini kullanmak konusunda önemli eksiklerin olduğu görülüyor. Neyi, niçin öğrendiğini bilmediğin ve düzenli tekrarlar yapmadığın için okul hayatı sana oldukça güç geliyor olabilir. Düzenli tekrar ve verimli ders çalışma yollarını öğrenmen başarın için büyük önem taşıyor.",
                "tips": [
                    "Her dersten sonra 10 dakika kısa bir tekrar yap.",
                    "Öğrendiğin bilgileri günlük hayattaki olaylarla ilişkilendir.",
                    "Kendi kendine 'Bu konuyu neden öğreniyorum?' diye sor."
                ]
            },
            "mid": {
                "range": (3, 4),
                "text": "Bilinçli çalışmak ve öğrendiğini kullanmak konusunda bazı eksiklerin olduğu görülüyor. Öğreneceğin malzemenin nerede kullanılacağını bilmek ve düzenli tekrar yapma tekniğini geliştirmek başarında köklü değişiklikler yapacaktır.",
                "tips": [
                    "Haftalık tekrar planı oluştur.",
                    "Öğrendiğin konuları arkadaşlarına anlatmayı dene — anlatarak öğrenmek çok etkilidir."
                ]
            },
            "low": {
                "range": (0, 2),
                "text": "Bilinçli çalışan ve öğrendiğini kullanan, bilgini geliştirerek unutmayı önleyen bir öğrenci olduğun görülüyor. Yaptığın düzenli tekrarların başarındaki payı büyüktür. Tebrikler! 🎉",
                "tips": []
            }
        }
    },
    "C": {
        "name": "Not Tutmak ve Dersi Dinlemek",
        "question_ids": [8, 22, 61, 72, 10, 24, 62, 20, 31, 71],
        "max_score": 10,
        "interpretations": {
            "high": {
                "range": (6, 10),
                "text": "Not tutmanın ve dersi dinlemenin başarı üzerindeki etkisini yeterince bilmediğin anlaşılıyor. Not tutmak konusunda tekniğini geliştirir ve bu konuda gayret harcarsan, bunun karşılığını en kısa zamanda göreceğinden emin olabilirsin.",
                "tips": [
                    "Derste kendi cümlelerinle not al, öğretmenin her kelimesini yazmaya çalışma.",
                    "Notlarını düzenli bir defterde tut, dağınık kağıtlar kullanma.",
                    "Ders sonunda notlarını 5 dakika gözden geçir ve eksikleri tamamla."
                ]
            },
            "mid": {
                "range": (3, 5),
                "text": "Not tutmak ve ders dinlemek konusunda bazı hataların olduğu anlaşılıyor. Not tutma becerisini geliştirir ve bu konudaki teknikleri öğrenirsen verdiğin emeğin karşılığını fazlasıyla alırsın.",
                "tips": [
                    "Cornell not tutma yöntemini araştır ve dene.",
                    "Kendi kısaltma ve sembollerini geliştir — daha hızlı not alırsın."
                ]
            },
            "low": {
                "range": (0, 2),
                "text": "Not tutmak ve dersi dinlemek konusunda başarılı olduğun anlaşılıyor. Öğretmenin söylediklerini iyi dinlediğin, önemli ve önemsiz noktaları birbirinden ayırdığın, notlarını yeniden gözden geçirip düzenlediğin için başarın yükseliyor. Harika! 🎉",
                "tips": []
            }
        }
    },
    "D": {
        "name": "Okuma Alışkanlıkları ve Teknikleri",
        "question_ids": [4, 11, 34, 56, 5, 28, 45, 60, 7, 29, 46, 73],
        "max_score": 12,
        "interpretations": {
            "high": {
                "range": (8, 12),
                "text": "Okumaya çok fazla zaman ayırdığın, buna rağmen daha sonra oldukça az şey hatırlayabildiğin anlaşılıyor. Önemli olanla olmayanı ayırmakta güçlük çektiğin ve metin içinde sana gerekli olmayan yerlerde zaman kaybettiğin görülüyor. Başarını yükseltebilmek için okuma becerini geliştirmeye özel önem vermen gerekiyor.",
                "tips": [
                    "Okumaya başlamadan önce başlıklara ve alt başlıklara göz gezdir.",
                    "Önemli yerlerin altını çiz veya işaretle.",
                    "Her bölümden sonra dur ve okuduğunu kendi kelimelerinle özetle.",
                    "Hız okuma tekniklerini araştır ve pratik yap."
                ]
            },
            "mid": {
                "range": (4, 7),
                "text": "Okurken önemli olanla olmayanı ayırmakta zaman zaman güçlük çektiğin ve değerli vaktinden yeterince yararlanamadığın anlaşılıyor. Okuma hızını yükseltip seçiciliğini artırabilirsen başarında önemli gelişmeler olacaktır.",
                "tips": [
                    "SQ3R tekniğini dene: Gözden Geçir, Soru Sor, Oku, Tekrarla, Gözden Geçir.",
                    "Şekil ve tabloları atlama — bunlar konuyu anlamana yardımcı olur."
                ]
            },
            "low": {
                "range": (0, 3),
                "text": "Okuduğun metin içinde gerekli olanları ayırabildiğin ve gereksiz okumalarla zaman kaybetmediğin anlaşılıyor. Bu başarını olumlu yönde etkiliyor. Süper! 🎉",
                "tips": []
            }
        }
    },
    "E": {
        "name": "Ödev Hazırlamak",
        "question_ids": [3, 25, 52, 63, 23, 26, 53],
        "max_score": 7,
        "interpretations": {
            "high": {
                "range": (5, 7),
                "text": "Günlük veya dönem ödevi hazırlamanın, konunun özünü kavramak için ne kadar önemli olduğunun farkında olmadığın görülüyor. Ödevlerden bir an önce kurtulma eğilimin başarını tehdit eden önemli bir engel. Ödevlerin gelişimin için bir adım olduğunu kabullenir ve öğrenirsen başarın yükselecektir.",
                "tips": [
                    "Ödevi küçük parçalara böl ve her gün biraz yap.",
                    "Başlamadan önce kısa bir plan yap: Ne yapacaksın? Hangi kaynakları kullanacaksın?",
                    "Ödevini bitirdikten sonra bir gün bekle, sonra tekrar oku ve düzelt."
                ]
            },
            "mid": {
                "range": (3, 4),
                "text": "Ödevlerini gereği gibi hazırlamak ve düzenlemekte zaman zaman güçlük çektiğin anlaşılıyor. Ödevlerini zamanında ve yeterli çalışmayla yapman başarını artıracaktır.",
                "tips": [
                    "Ödev takvimi oluştur ve son teslim tarihlerini takip et.",
                    "En az bir ek kaynak kullanmayı alışkanlık haline getir."
                ]
            },
            "low": {
                "range": (0, 2),
                "text": "Ödevlerin eğitim hayatı içindeki önemini kavramış olduğun anlaşılıyor. Çeşitli kişi ve kaynaklardan yararlanarak, zamanında hazırladığın ödevler başarının önemli sebeplerinden biri olmaya devam edecek. Harika! 🎉",
                "tips": []
            }
        }
    },
    "F": {
        "name": "Okula Karşı Tutum",
        "question_ids": [27, 35, 57, 68, 33, 36, 64, 69],
        "max_score": 8,
        "interpretations": {
            "high": {
                "range": (5, 8),
                "text": "Okula karşı tutumunun çalışmayı, öğrenmeyi ve başarılı olmayı güçleştirdiği görülüyor. Sadece okulda değil, hiçbir konuda olumsuz bir tutumla olumlu bir sonuç elde etmek mümkün değildir. Okul, eğitim ve öğretmenlerle ilgili temel düşüncelerini gözden geçirmen, eğitime verdiğin yılların karşılığını alabilmen açısından çok önemli.",
                "tips": [
                    "Sevmediğin derslerde bile ilgini çekecek bir nokta bulmaya çalış.",
                    "Öğretmenlerinle iletişimi kesmemeye çalış — sorunlarını paylaş.",
                    "Okuldaki sosyal etkinliklere katıl — okulu sadece dersle sınırlama."
                ]
            },
            "mid": {
                "range": (3, 4),
                "text": "Okula karşı bazı olumsuz duygu ve düşünceler içinde olduğun görülüyor. Okula karşı zaman zaman gelişen bu olumsuz tavrının başarını etkilememesi için bunları yeniden ele alman ve gözden geçirmen faydalı olacaktır.",
                "tips": [
                    "Okulda seni mutlu eden şeylerin bir listesini yap.",
                    "Güvendiğin bir öğretmenle düşüncelerini paylaş."
                ]
            },
            "low": {
                "range": (0, 2),
                "text": "Okula karşı olumlu bir tavır içinde olduğun görülüyor. Okul hayatının ilginç yönlerini bulup ondan keyif aldığın ve bunun da başarını yükselttiği, öğretmenlerin ve arkadaşlarınla ilişkini geliştirdiği muhakkak. Süper! 🎉",
                "tips": []
            }
        }
    },
    "G": {
        "name": "Sınavlara Hazırlanmak ve Sınava Girmek",
        "question_ids": [1, 9, 54, 65, 2, 21, 58, 66, 6, 41, 59],
        "max_score": 11,
        "interpretations": {
            "high": {
                "range": (8, 11),
                "text": "Sınavlarda başarılı olmanın, sınav öncesinde başlayan ve sınavda da devam eden bir işlemler dizisi olduğunun farkında değilsin. Eğer zaman zaman çalıştığın ölçüde başarılı olmadığından yakınıyorsan, muhtemelen başarısızlığının arkasındaki sebeplerin başında sınava hazırlanma teknikleri ve sınav taktiklerini yeterince bilmemek veya uygulamamak yatıyor.",
                "tips": [
                    "Sınavdan en az 3 gün önce çalışmaya başla — son geceye bırakma.",
                    "Sınavda önce tüm soruları oku, kolaylardan başla.",
                    "Sınav öncesi öğretmenin nelere önem verdiğini öğrenmeye çalış.",
                    "Sınav sırasında sakin ol — derin nefes al ve kendine güven."
                ]
            },
            "mid": {
                "range": (4, 7),
                "text": "Sınavlara hazırlanmak ve sınava girmek konusunda bir hayli bilgi ve tecrübe sahibi olsan da bazı eksiklerin olduğu görülüyor. Bu eksiklerini giderirsen başarın daha da yükselecektir.",
                "tips": [
                    "Sınav stratejilerini gözden geçir — zaman yönetimi çok önemli.",
                    "Geçmiş sınav sorularını çözerek pratik yap."
                ]
            },
            "low": {
                "range": (0, 3),
                "text": "Sınavlara hazırlanmak ve sınava girmek konusundaki teknik ve taktikleri oldukça iyi bildiğin ve bunları uyguladığın görülüyor. Yüksek başarının arkasındaki en önemli sebeplerden biri de hiç şüphesiz budur. Muhteşem! 🎉",
                "tips": []
            }
        }
    }
}


# --- PUANLAMA FONKSİYONU ---
def calculate_calisma_davranisi(answers):
    """
    Çalışma Davranışı Ölçeğini puanlar.
    
    Puanlama mantığı (Baltaş ölçeğine göre):
    Her kategoride, cevap anahtarına UYMAYAN cevap sayısı = o kategorinin puanı.
    Yüksek puan = o alanda sorun var demektir.
    
    Args:
        answers: dict — {soru_id: "D" veya "Y"}
        Örnek: {1: "Y", 2: "D", 3: "Y", ...}
    
    Returns:
        (scores_dict, report_text)
    """
    category_scores = {}
    
    for cat_key, cat_info in CALISMA_DAVRANISI_CATEGORIES.items():
        wrong_count = 0
        for qid in cat_info["question_ids"]:
            # Bu sorunun doğru cevabını bul
            question = next((q for q in CALISMA_DAVRANISI_QUESTIONS if q["id"] == qid), None)
            if question is None:
                continue
            
            student_answer = answers.get(qid)
            if student_answer is None:
                continue
            
            # Cevap anahtarına UYMAYAN cevap = 1 puan
            if student_answer != question["key"]:
                wrong_count += 1
        
        category_scores[cat_key] = wrong_count
    
    # Toplam puan
    total = sum(category_scores.values())
    max_total = sum(c["max_score"] for c in CALISMA_DAVRANISI_CATEGORIES.values())
    
    # Genel değerlendirme için yüzdeler
    scores_with_names = {}
    for cat_key, score in category_scores.items():
        cat_name = CALISMA_DAVRANISI_CATEGORIES[cat_key]["name"]
        scores_with_names[cat_name] = score
    
    scores = {
        "categories": category_scores,
        "categories_named": scores_with_names,
        "total": total,
        "max_total": max_total
    }
    
    report = generate_calisma_davranisi_report(scores)
    
    return scores, report


def generate_calisma_davranisi_report(scores):
    """
    Çalışma Davranışı testi için şablon tabanlı rapor üretir.
    """
    category_scores = scores["categories"]
    total = scores["total"]
    max_total = scores["max_total"]
    genel_yuzde = round(total / max_total * 100, 1) if max_total > 0 else 0
    
    # Genel durum değerlendirmesi
    if genel_yuzde >= 60:
        genel_durum = "🔴 Çalışma davranışlarında önemli güçlükler var. Ama endişelenme, bunların hepsi geliştirilebilir!"
    elif genel_yuzde >= 35:
        genel_durum = "🟡 Çalışma davranışlarında bazı alanlar gelişime açık. Doğru tekniklerle çok daha başarılı olabilirsin!"
    else:
        genel_durum = "🟢 Çalışma davranışların genel olarak iyi durumda. Tebrikler, böyle devam et!"
    
    report = f"""
# 📊 ÇALIŞMA DAVRANIŞI DEĞERLENDİRME RAPORU

**Genel Durum:** {genel_durum}
**Toplam Puan:** {total}/{max_total} (%{genel_yuzde})

---

## 📋 Kategori Bazında Sonuçlar

"""
    
    # Güçlü ve zayıf alanları ayır
    strong_areas = []
    weak_areas = []
    
    for cat_key in ["A", "B", "C", "D", "E", "F", "G"]:
        cat_info = CALISMA_DAVRANISI_CATEGORIES[cat_key]
        score = category_scores.get(cat_key, 0)
        max_s = cat_info["max_score"]
        cat_name = cat_info["name"]
        pct = round(score / max_s * 100, 1) if max_s > 0 else 0
        
        # Progress bar
        bar_len = round(pct / 10)
        bar = "█" * bar_len + "░" * (10 - bar_len)
        
        report += f"### {cat_key}. {cat_name}\n"
        report += f"**Puanın:** {score}/{max_s} ({bar} %{pct})\n\n"
        
        # Doğru yorum aralığını bul
        for level_key, level_data in cat_info["interpretations"].items():
            low, high = level_data["range"]
            if low <= score <= high:
                report += f"{level_data['text']}\n\n"
                
                if level_data["tips"]:
                    report += "**Sana Özel İpuçları:**\n"
                    for tip in level_data["tips"]:
                        report += f"- 💡 {tip}\n"
                    report += "\n"
                
                if level_key == "low":
                    strong_areas.append(cat_name)
                elif level_key == "high":
                    weak_areas.append(cat_name)
                break
        
        report += "---\n\n"
    
    # Özet bölümü
    report += "## 🌟 Özet\n\n"
    
    if strong_areas:
        report += f"**Güçlü Yönlerin:** {', '.join(strong_areas)}\n\n"
    
    if weak_areas:
        report += f"**Öncelikli Gelişim Alanların:** {', '.join(weak_areas)}\n\n"
    
    report += """
## 💬 Son Söz

Unutma, çalışma davranışları doğuştan gelen değil, **öğrenilebilen** becerilerdir! Bugünkü sonuçların yarınki başarını belirlemez. Önemli olan farkında olmak ve adım adım geliştirmektir. Sen bunu yapabilirsin! 🚀
"""
    return report.strip()


# ============================================================
# TEST: Örnek kullanım ve doğrulama
# ============================================================


# ============================================================
# PARÇA 3: SINAV KAYGISI ÖLÇEĞİ
# Kaynak: MEB Rehberlik ve Araştırma Merkezi Standart Ölçeği
# 50 soru, 7 alt boyut, Doğru/Yanlış formatı
# Puanlama: "Doğru" işaretleyen = 1 puan (o alt boyutta)
# ============================================================

# --- SABİT SORULAR (50 ADET) ---
# Tüm sorularda "Doğru" cevabı = kaygı göstergesi = 1 puan
# Soru 3, 7, 8 → ters maddeler DEĞİL (bu ölçekte tüm D cevapları puan alır)

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
    {"id": 14, "text": "Her zaman düşünmesem de başarısız olursam çevremdekilerin bana hangi gözle bakacakları konusunda endişelenirim."},
    {"id": 15, "text": "Geleceğimin sınavlarda göstereceğim başarıya bağlı olması beni üzüyor."},
    {"id": 16, "text": "Kendimi bir toplayabilsem, birçok kişiden daha iyi not alacağımı biliyorum."},
    {"id": 17, "text": "Başarısız olursam, insanlar benim yeteneğimden şüpheye düşecekler."},
    {"id": 18, "text": "Hiçbir zaman sınavlara tam olarak hazırlandığım duygusunu yaşayamam."},
    {"id": 19, "text": "Bir sınavdan önce bir türlü gevşeyemem."},
    {"id": 20, "text": "Önemli sınavlardan önce zihnim adeta durur kalır."},
    {"id": 21, "text": "Bir sınav sırasında dışarıdan gelen gürültüler, çevremdekilerin çıkardıkları sesler, ışık, oda sıcaklığı vb. beni rahatsız eder."},
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

# --- 7 ALT BOYUT VE CEVAP ANAHTARI ---
# Kaynak: MEB Rehberlik ve Araştırma Merkezi resmi belgesi
# D = 1 puan, Y = 0 puan

SINAV_KAYGISI_CATEGORIES = {
    "baskalari_gorusu": {
        "name": "Başkalarının Sizi Nasıl Gördüğü ile İlgili Endişeler",
        "icon": "👥",
        "question_ids": [3, 14, 17, 25, 32, 41, 46, 47],
        "max_score": 8,
        "interpretations": {
            "high": {
                "range": (4, 8),
                "text": "Başkalarının seni nasıl gördüğü senin için büyük önem taşıyor. Çevrendeki insanların değerlendirmeleri sınav durumunda zihinsel faaliyetini olumsuz etkiliyor ve sınav başarını tehlikeye atabiliyor.",
                "tips": [
                    "Unutma: Sınavda ölçülen senin bilgin, kişiliğin veya değerin değil!",
                    "Herkesin farklı güçlü yönleri var — kendini başkalarıyla kıyaslama.",
                    "Not: Sadece bir sayıdır, seni tanımlamaz.",
                    "Güvendiğin birisiyle (ailen, öğretmenin) bu endişelerini paylaş."
                ]
            },
            "low": {
                "range": (0, 3),
                "text": "Başkalarının seninle ilgili görüşleri seni fazla etkilemiyor. Bu sebeple sınavlara hazırlanırken çevrendeki insanların ne düşündükleri konusunda gereksiz zaman ve enerji kaybetmiyorsun. Bu harika bir durum! 🎉",
                "tips": []
            }
        }
    },
    "kendi_gorusu": {
        "name": "Kendinizi Nasıl Gördüğünüzle İlgili Endişeler",
        "icon": "🪞",
        "question_ids": [2, 9, 16, 24, 31, 38, 40],
        "max_score": 7,
        "interpretations": {
            "high": {
                "range": (4, 7),
                "text": "Sınavlardaki başarınla kendinize olan saygını eşdeğer görüyorsun. Sınavlarda ölçülenin kişilik değerin değil, bilgi düzeyin olduğunu kabullenmek sana yardımcı olacaktır. Bu düşünce biçimi problemleri çözmende sana yardımcı olmadığı gibi, endişelerini artırıyor.",
                "tips": [
                    "Sınav sonucu senin değerini belirlemez — bunu kendine sık sık hatırlat.",
                    "Başarısızlık bir son değil, öğrenme fırsatıdır.",
                    "Güçlü yönlerinin bir listesini yap ve zor anlarda oku.",
                    "Kendine karşı nazik ol — herkes hata yapabilir."
                ]
            },
            "low": {
                "range": (0, 3),
                "text": "Sınavlardaki başarınla kendi kişiliğine verdiğin değeri birbirinden oldukça iyi ayırabildiğin anlaşılıyor. Bu tutumun problemleri daha etkili bir biçimde çözmene imkân veriyor ve okul başarını olumlu yönde etkiliyor. Süper! 🎉",
                "tips": []
            }
        }
    },
    "gelecek_endisesi": {
        "name": "Gelecekle İlgili Endişeler",
        "icon": "🔮",
        "question_ids": [1, 8, 15, 23, 30, 49],
        "max_score": 6,
        "interpretations": {
            "high": {
                "range": (3, 6),
                "text": "Sınavlardaki başarını gelecekteki mutluluğunun ve başarının tek ölçüsü olarak görüyorsun. Bu yaklaşım sınavların güvenliğin ve amaçlarına ulaşman konusunda engel olduğunu düşündürüyor. Bu düşünceler bilgini yeterince ortaya koymayı güçleştiriyor.",
                "tips": [
                    "Hayatta başarılı olmanın birçok yolu var — sınav bunlardan sadece biri.",
                    "Bugüne odaklan: 'Şimdi ne yapabilirim?' diye sor.",
                    "Sınavları bir tehdit değil, geçilmesi gereken basamaklar olarak gör.",
                    "İlham veren insanların hikayelerini oku — birçoğu sınavlarda zorlanmıştır."
                ]
            },
            "low": {
                "range": (0, 2),
                "text": "Gelecekteki mutluluğunun ve başarının tek belirleyicisinin sınavlar olmadığının farkındasın. Sınavlara geçilmesi gereken aşamalar olarak bakman, bilgini yeterince ortaya koymana imkân veriyor. Harika! 🎉",
                "tips": []
            }
        }
    },
    "hazirlik_endisesi": {
        "name": "Yeterince Hazırlanamamakla İlgili Endişeler",
        "icon": "📖",
        "question_ids": [6, 11, 18, 26, 33, 42],
        "max_score": 6,
        "interpretations": {
            "high": {
                "range": (3, 6),
                "text": "Sınavları kişiliğin ve gelecekteki güvenliğinin bir ölçüsü olarak gördüğün için herhangi bir sınava hazırlık dönemi senin için bir kriz dönemi olabiliyor. Sınavda başarılı olmanı sağlayacak hazırlanma tekniklerini öğrenirsen, kendine güvenin artacak ve endişelerini kontrol etmen kolaylaşacak.",
                "tips": [
                    "Sınava en az 3 gün öncesinden çalışmaya başla.",
                    "Çalışma planı yap — neyi, ne zaman çalışacağını belirle.",
                    "Çalıştıktan sonra kendini test et — hazır olduğunu görmek güven verir.",
                    "Eksik konuları listele ve tek tek üzerinden geç."
                ]
            },
            "low": {
                "range": (0, 2),
                "text": "Sınavlara büyük bir gerginlik hissetmeden hazırlanıyorsun. Sınava hazırlanmanın sistemini bilmen, gereksiz gerginlikleri yaşamandan ve huzurlu bir şekilde çalışmandan kaynaklanan başarını yükseltiyor. Tebrikler! 🎉",
                "tips": []
            }
        }
    },
    "bedensel_tepkiler": {
        "name": "Bedensel Tepkiler",
        "icon": "💪",
        "question_ids": [5, 12, 19, 27, 34, 39, 43],
        "max_score": 7,
        "interpretations": {
            "high": {
                "range": (4, 7),
                "text": "Sınava hazırlanırken iştahsızlık, uykusuzluk, gerginlik gibi birçok bedensel rahatsızlıkla mücadele etmek zorunda kaldığın anlaşılıyor. Bu rahatsızlıklar sınav hazırlığını güçleştiriyor. Bedensel tepkilerini kontrol etmeyi öğrenmen hem hazırlığını hem de sınavda bildiklerini ortaya koymanı kolaylaştıracaktır.",
                "tips": [
                    "Derin nefes egzersizleri yap: 4 saniye nefes al, 4 saniye tut, 4 saniye ver.",
                    "Sınavdan önce hafif egzersiz yap (yürüyüş, germe hareketleri).",
                    "Düzenli uyku çok önemli — sınav gecesi erken yat.",
                    "Sınav günü hafif bir kahvaltı yap, aç karnına girme."
                ]
            },
            "low": {
                "range": (0, 3),
                "text": "Sınava hazırlık sırasında heyecanını kontrol edebildiğin ve bedensel olarak çalışmanı zorlaştıracak bir rahatsızlık hissetmediğin anlaşılıyor. Bu çok iyi! 🎉",
                "tips": []
            }
        }
    },
    "zihinsel_tepkiler": {
        "name": "Zihinsel Tepkiler",
        "icon": "🧠",
        "question_ids": [4, 13, 20, 21, 28, 35, 36, 37, 48, 50],
        "max_score": 10,
        "interpretations": {
            "high": {
                "range": (4, 10),
                "text": "Sınava hazırlanırken veya sınav sırasında çevrende olan bitenden fazlasıyla etkilendiğin ve dikkatini toplamakta güçlük çektiğin görülüyor. Bu durum düşünce akışını yavaşlatır ve başarıyı engeller. Zihinsel tepkilerini kontrol altına almayı öğrenmen çok faydalı olacaktır.",
                "tips": [
                    "Dikkatini toplama egzersizleri yap (mindfulness, meditasyon).",
                    "Sınav sırasında olumsuz düşünceler geldiğinde 'DUR' de ve nefes al.",
                    "Çalışırken dikkat dağıtıcıları (telefon, TV) uzaklaştır.",
                    "Pozitif iç konuşma yap: 'Ben bunu yapabilirim, hazırlandım.'"
                ]
            },
            "low": {
                "range": (0, 3),
                "text": "Zihinsel açıdan sınava hazırlanırken veya sınav sırasında önemli bir rahatsızlık yaşamadığın görülüyor. Heyecanını kontrol etmen, zihinsel ve duygusal olarak hazırlığını kolaylaştırıyor ve başarını artırıyor. Muhteşem! 🎉",
                "tips": []
            }
        }
    },
    "genel_kaygi": {
        "name": "Genel Sınav Kaygısı",
        "icon": "📋",
        "question_ids": [7, 10, 22, 29, 44, 45],
        "max_score": 6,
        "interpretations": {
            "high": {
                "range": (3, 6),
                "text": "Sınavlarda kendine güvenemediğin, sınavları varlığın ve geleceğin için bir tehdit olarak gördüğün anlaşılıyor. Sınavlara sahip oldukları önemin çok üzerinde değer vermekte ve belki de bu sebeple çok fazla heyecanlanıyorsun. Sınav kaygını azaltacak teknikleri öğrenmen hem eğitim başarını yükseltecek hem de hayattan aldığın zevki artıracaktır.",
                "tips": [
                    "Sınavı bir savaş değil, bir oyun gibi düşün — stratejini belirle ve oyna.",
                    "Geçmiş başarılarını hatırla — daha önce de sınavları geçtin.",
                    "Kaygı tamamen normal bir duygudur — biraz kaygı performansı artırır.",
                    "Sınav sonrası kendini ödüllendir — bir film izle, sevdiğin bir şey yap."
                ]
            },
            "low": {
                "range": (0, 2),
                "text": "Genel olarak sınavlara karşı sağlıklı bir tutum içinde olduğun anlaşılıyor. Sınavları bir tehdit olarak görmemen ve uygun düzeyde bir heyecan yaşaman başarını olumlu etkiliyor. Süper! 🎉",
                "tips": []
            }
        }
    }
}


# --- PUANLAMA FONKSİYONU ---
def calculate_sinav_kaygisi(answers):
    """
    Sınav Kaygısı Ölçeğini puanlar.
    
    Puanlama: "D" (Doğru) = 1 puan, "Y" (Yanlış) = 0 puan
    Her alt boyut ayrı ayrı puanlanır.
    
    Args:
        answers: dict — {soru_id: "D" veya "Y"}
    
    Returns:
        (scores_dict, report_text)
    """
    category_scores = {}
    
    for cat_key, cat_info in SINAV_KAYGISI_CATEGORIES.items():
        score = 0
        for qid in cat_info["question_ids"]:
            student_answer = answers.get(qid)
            if student_answer == "D":
                score += 1
        category_scores[cat_key] = score
    
    # Toplam puan
    total = sum(category_scores.values())
    max_total = sum(c["max_score"] for c in SINAV_KAYGISI_CATEGORIES.values())
    
    # Genel kaygı seviyesi
    total_pct = round(total / max_total * 100, 1) if max_total > 0 else 0
    
    if total_pct >= 60:
        overall_level = "Yüksek"
        overall_color = "🔴"
    elif total_pct >= 35:
        overall_level = "Orta"
        overall_color = "🟡"
    else:
        overall_level = "Düşük"
        overall_color = "🟢"
    
    # İsimli skorlar (grafik için)
    scores_with_names = {}
    for cat_key, score in category_scores.items():
        cat_name = SINAV_KAYGISI_CATEGORIES[cat_key]["name"]
        scores_with_names[cat_name] = score
    
    scores = {
        "categories": category_scores,
        "categories_named": scores_with_names,
        "total": total,
        "max_total": max_total,
        "total_pct": total_pct,
        "overall_level": overall_level
    }
    
    report = generate_sinav_kaygisi_report(scores)
    
    return scores, report


def generate_sinav_kaygisi_report(scores):
    """
    Sınav Kaygısı testi için şablon tabanlı rapor üretir.
    """
    category_scores = scores["categories"]
    total = scores["total"]
    max_total = scores["max_total"]
    total_pct = scores["total_pct"]
    overall_level = scores["overall_level"]
    
    # Genel durum mesajı
    if overall_level == "Yüksek":
        genel_mesaj = "Sınav kaygın yüksek görünüyor. Ama endişelenme — bu çok yaygın bir durum ve üstesinden gelmek tamamen mümkün! Aşağıdaki ipuçları sana yardımcı olacak."
        genel_renk = "🔴"
    elif overall_level == "Orta":
        genel_mesaj = "Belirli düzeyde sınav kaygın olduğu görülüyor. Bu aslında normal — biraz kaygı seni motive bile edebilir. Ama bazı alanlarda kendini rahatlatmayı öğrenmen faydalı olacak."
        genel_renk = "🟡"
    else:
        genel_mesaj = "Sınav kaygın düşük seviyede. Sınavlara karşı sağlıklı bir tutum içindesin. Bu harika bir durum!"
        genel_renk = "🟢"
    
    report = f"""
# 📝 SINAV KAYGISI DEĞERLENDİRME RAPORU

**Genel Kaygı Düzeyin:** {genel_renk} {overall_level} ({total}/{max_total} — %{total_pct})

{genel_mesaj}

---

## 📊 Alt Boyut Sonuçların

"""
    
    # Sorunlu ve iyi alanları ayır
    problem_areas = []
    good_areas = []
    
    for cat_key in ["baskalari_gorusu", "kendi_gorusu", "gelecek_endisesi", 
                     "hazirlik_endisesi", "bedensel_tepkiler", "zihinsel_tepkiler", "genel_kaygi"]:
        cat_info = SINAV_KAYGISI_CATEGORIES[cat_key]
        score = category_scores.get(cat_key, 0)
        max_s = cat_info["max_score"]
        cat_name = cat_info["name"]
        icon = cat_info["icon"]
        pct = round(score / max_s * 100, 1) if max_s > 0 else 0
        
        # Progress bar
        bar_len = round(pct / 10)
        bar = "█" * bar_len + "░" * (10 - bar_len)
        
        report += f"### {icon} {cat_name}\n"
        report += f"**Puanın:** {score}/{max_s} ({bar} %{pct})\n\n"
        
        # Doğru yorum aralığını bul
        for level_key, level_data in cat_info["interpretations"].items():
            low, high = level_data["range"]
            if low <= score <= high:
                report += f"{level_data['text']}\n\n"
                
                if level_data["tips"]:
                    report += "**Sana Özel Öneriler:**\n"
                    for tip in level_data["tips"]:
                        report += f"- 💡 {tip}\n"
                    report += "\n"
                
                if level_key == "low":
                    good_areas.append(cat_name)
                elif level_key == "high":
                    problem_areas.append(cat_name)
                break
        
        report += "---\n\n"
    
    # Özet
    report += "## 🌟 Özet\n\n"
    
    if good_areas:
        report += f"**Güçlü Yönlerin:** {', '.join(good_areas)}\n\n"
    
    if problem_areas:
        report += f"**Üzerinde Çalışman Gereken Alanlar:** {', '.join(problem_areas)}\n\n"
    
    # Genel tavsiyeler
    report += """
## 🛠️ Genel Kaygı Azaltma Teknikleri

- 🫁 **Nefes Egzersizi:** 4-4-4 tekniği (4 sn nefes al, 4 sn tut, 4 sn ver)
- 🧘 **Kas Gevşetme:** Sınavdan önce omuz ve boyun kaslarını gevşet
- 📝 **Pozitif İç Konuşma:** "Ben hazırlandım, yapabilirim" cümlelerini tekrarla
- 📅 **Planlı Hazırlık:** Son dakikaya bırakmak kaygıyı artırır — erken başla
- 🏃 **Fiziksel Aktivite:** Düzenli egzersiz kaygıyı azaltır

---

## 💬 Son Söz

Sınav kaygısı çok yaygın bir durumdur ve başa çıkmak tamamen mümkündür! Kaygı hissetmek normal ve insani bir duygudur. Önemli olan bu duyguyu kontrol edebilmeyi öğrenmektir. Yukarıdaki önerileri uygulamaya başladığında, zamanla kendini daha rahat ve güvenli hissettiğini göreceksin. Sen bunu başarabilirsin! 💪
"""
    return report.strip()


# ============================================================
# TEST: Örnek kullanım ve doğrulama
# ============================================================


# ============================================================
# PARÇA 4: ÇOKLU ZEKÂ KURAMI DEĞERLENDİRME ÖLÇEĞİ (GARDNER)
# Kaynak: Firma belgesi (MEB EARGED modeli)
# Lise/Yetişkin: 80 soru (8 zeka × 10 soru), Likert 0-4
# İlköğretim: 40 soru (8 zeka × 5 soru), Evet/Hayır
# ============================================================

# --- 8 ZEKÂ TÜRÜ VERİLERİ (Ortak) ---
COKLU_ZEKA_DATA = {
    "sozel": {
        "name": "Sözel-Dilsel Zekâ",
        "icon": "📝",
        "description": "Kelimelerle düşünme, dili etkili kullanma ve iletişim kurma yeteneğin çok güçlü!",
        "strengths": [
            "Güçlü okuma ve yazma becerileri",
            "Zengin kelime hazinesi",
            "İyi bir hikaye anlatıcısı",
            "Dillere yatkınlık",
            "İkna edici konuşma"
        ],
        "study_tips": [
            "Konuları kendi kelimelerinle özetleyerek çalış.",
            "Sesli okuma ve anlatma yöntemini kullan.",
            "Günlük veya blog yazarak öğrendiklerini pekiştir.",
            "Kelime oyunları ve bulmacalar çöz."
        ],
        "careers": ["Yazar", "Gazeteci", "Avukat", "Öğretmen", "Çevirmen", "Editör", "Diplomat"]
    },
    "mantiksal": {
        "name": "Mantıksal-Matematiksel Zekâ",
        "icon": "🔢",
        "description": "Sayılarla, mantıkla ve sistemli düşünmeyle arası çok iyi olan bir zihne sahipsin!",
        "strengths": [
            "Güçlü analitik düşünme",
            "Problem çözme becerisi",
            "Sayısal yetenekler",
            "Sebep-sonuç ilişkisi kurma",
            "Bilimsel merak"
        ],
        "study_tips": [
            "Konuları mantıksal sıraya koyarak çalış.",
            "Formüller, grafikler ve tablolar oluştur.",
            "Neden-sonuç ilişkilerini sorgulayarak öğren.",
            "Matematik ve bilim problemleri çözerek pratik yap."
        ],
        "careers": ["Mühendis", "Bilim İnsanı", "Programcı", "Doktor", "Ekonomist", "Muhasebeci", "Matematikçi"]
    },
    "gorsel": {
        "name": "Görsel-Uzamsal Zekâ",
        "icon": "🎨",
        "description": "Dünyayı görsellerle, renklerle ve şekillerle algılayan çok güçlü bir hayal gücün var!",
        "strengths": [
            "Güçlü görsel hafıza",
            "Zengin hayal gücü",
            "Renk ve tasarım duyarlılığı",
            "Mekânsal algılama",
            "Resim ve çizim yeteneği"
        ],
        "study_tips": [
            "Zihin haritaları (mind map) çizerek çalış.",
            "Renkli kalemler ve görsel notlar kullan.",
            "Konuları şema ve diyagramlarla öğren.",
            "Video ve görsel materyallerden yararlan."
        ],
        "careers": ["Mimar", "Grafik Tasarımcı", "Fotoğrafçı", "Ressam", "İç Mimar", "Pilot", "Cerrah"]
    },
    "muziksel": {
        "name": "Müziksel-Ritmik Zekâ",
        "icon": "🎵",
        "description": "Müziğe, ritimlere ve seslere karşı özel bir duyarlılığın var — bu harika bir yetenek!",
        "strengths": [
            "Ritim ve melodi duyarlılığı",
            "Müzikal hafıza",
            "Ses tonu ayrımı",
            "Müzik aletlerine yatkınlık",
            "Ritmik hareket becerisi"
        ],
        "study_tips": [
            "Ders çalışırken fon müziği dinle (sözsüz).",
            "Öğrendiğin bilgileri şarkı veya kafiye haline getir.",
            "Ritmik tekrarlarla ezberle.",
            "Sesli çalışma yöntemini kullan."
        ],
        "careers": ["Müzisyen", "Besteci", "Ses Mühendisi", "DJ", "Müzik Öğretmeni", "Şarkıcı", "Orkestra Şefi"]
    },
    "dogaci": {
        "name": "Doğacı Zekâ",
        "icon": "🌿",
        "description": "Doğaya, hayvanlara ve çevreye karşı derin bir ilgi ve duyarlılığın var!",
        "strengths": [
            "Doğa sevgisi ve çevre bilinci",
            "Canlıları gözlemleme yeteneği",
            "Sınıflandırma becerisi",
            "Çevre duyarlılığı",
            "Mevsim ve iklim farkındalığı"
        ],
        "study_tips": [
            "Mümkünse açık havada ders çalış.",
            "Doğa gözlemleri yaparak konuları somutlaştır.",
            "Sınıflandırma ve gruplama yöntemlerini kullan.",
            "Belgeseller izleyerek öğren."
        ],
        "careers": ["Biyolog", "Veteriner", "Çevre Mühendisi", "Botanikçi", "Zoolog", "Ormancı", "Ekolog"]
    },
    "sosyal": {
        "name": "Sosyal (Kişilerarası) Zekâ",
        "icon": "🤝",
        "description": "İnsanlarla iletişim kurma, liderlik etme ve empati yapma konusunda çok yeteneklisin!",
        "strengths": [
            "Güçlü empati yeteneği",
            "Liderlik becerisi",
            "İletişim gücü",
            "İşbirliği yapabilme",
            "İnsanları anlama ve yönlendirme"
        ],
        "study_tips": [
            "Grup çalışmaları ve tartışmalarla öğren.",
            "Öğrendiğin konuları arkadaşlarına anlat.",
            "Rol yapma ve canlandırma yöntemlerini dene.",
            "Çalışma grupları oluştur."
        ],
        "careers": ["Psikolog", "Öğretmen", "İnsan Kaynakları Uzmanı", "Sosyal Hizmet Uzmanı", "Politikacı", "Satış Uzmanı"]
    },
    "bedensel": {
        "name": "Bedensel-Kinestetik Zekâ",
        "icon": "⚽",
        "description": "Bedenini çok iyi kullanıyorsun — hareket, spor ve el becerileri senin süper gücün!",
        "strengths": [
            "Güçlü beden koordinasyonu",
            "Sportif yetenek",
            "El becerileri",
            "Yaparak öğrenme",
            "Fiziksel ifade gücü"
        ],
        "study_tips": [
            "Yaparak ve deneyerek öğren — laboratuvar, atölye çalışmaları.",
            "Ders çalışırken yürüyerek veya hareket ederek tekrar yap.",
            "Not alırken, çizerek ve yazarak çalış.",
            "Kısa aralarla aktif molalar ver."
        ],
        "careers": ["Sporcu", "Cerrah", "Dansçı", "Fizyoterapist", "Teknisyen", "Heykeltıraş", "Aşçı"]
    },
    "icsel": {
        "name": "İçsel (Özedönük) Zekâ",
        "icon": "🧘",
        "description": "Kendini çok iyi tanıyorsun — güçlü ve zayıf yönlerinin farkındasın, bu çok değerli!",
        "strengths": [
            "Öz farkındalık",
            "Bağımsız çalışma becerisi",
            "Kendine güven",
            "Duygusal olgunluk",
            "Hedef belirleme ve motivasyon"
        ],
        "study_tips": [
            "Bireysel çalışma sana daha uygun — sessiz ortamlar tercih et.",
            "Kendi kendine hedefler koy ve takip et.",
            "Günlük tut, öğrenme sürecini değerlendir.",
            "Meditasyon ve düşünce egzersizleri yap."
        ],
        "careers": ["Psikolog", "Filozof", "Yazar", "Araştırmacı", "Girişimci", "Danışman", "Sanatçı"]
    }
}

# Zeka türü sıralaması (belgeden)
ZEKA_SIRA = ["sozel", "mantiksal", "gorsel", "muziksel", "dogaci", "sosyal", "bedensel", "icsel"]

# --- LİSE / YETİŞKİN VERSİYONU (80 SORU, Likert 0-4) ---
# Sıralama: Her 10 soru bir zeka türüne ait
# 1-10: Sözel, 11-20: Mantıksal, 21-30: Görsel, 31-40: Müziksel
# 41-50: Doğacı, 51-60: Sosyal, 61-70: Bedensel, 71-80: İçsel

COKLU_ZEKA_QUESTIONS_LISE = {
    "sozel": [
        {"id": 1,  "text": "Resimlerden çok yazılar dikkatimi çeker."},
        {"id": 2,  "text": "İsimler, yerler, tarihler konusunda belleğim iyidir."},
        {"id": 3,  "text": "Kitap okumayı severim."},
        {"id": 4,  "text": "Kelimeleri doğru şekilde telaffuz ederim."},
        {"id": 5,  "text": "Bilmecelerden, kelime oyunlarından hoşlanırım."},
        {"id": 6,  "text": "Dinleyerek daha iyi öğrenirim."},
        {"id": 7,  "text": "Yaşıma göre kelime hazinem iyidir."},
        {"id": 8,  "text": "Yazı yazmaktan hoşlanırım."},
        {"id": 9,  "text": "Öğrendiğim yeni kelimeleri kullanmayı severim."},
        {"id": 10, "text": "Sözel tartışmalarda başarılıyımdır."},
    ],
    "mantiksal": [
        {"id": 11, "text": "Makinelerin nasıl çalıştığına dair sorular sorarım."},
        {"id": 12, "text": "Aritmetik problemleri kafadan hesaplarım."},
        {"id": 13, "text": "Matematik ve fen derslerinden hoşlanırım."},
        {"id": 14, "text": "Satranç ve benzeri strateji oyunları severim."},
        {"id": 15, "text": "Mantık bulmacalarını, beyin jimnastiğini severim."},
        {"id": 16, "text": "Bilgisayarda oyunlardan çok hoşlanırım."},
        {"id": 17, "text": "Deneylerden, yeni denemeler yapmaktan hoşlanırım."},
        {"id": 18, "text": "Arkadaşlarıma oranla daha soyut düşünebilirim."},
        {"id": 19, "text": "Matematik oyunlarından hoşlanırım."},
        {"id": 20, "text": "Sebep-sonuç ilişkilerini kurmaktan zevk alırım."},
    ],
    "gorsel": [
        {"id": 21, "text": "Renklere karşı çok duyarlıyımdır."},
        {"id": 22, "text": "Harita, tablo türü materyalleri daha kolay algılarım."},
        {"id": 23, "text": "Arkadaşlarıma oranla daha fazla hayal kurarım."},
        {"id": 24, "text": "Resim yapmayı ve boyamayı çok severim."},
        {"id": 25, "text": "Yap-boz, Lego gibi oyunlardan hoşlanırım."},
        {"id": 26, "text": "Daha önce gittiğim yerleri kolayca hatırlarım."},
        {"id": 27, "text": "Bulmaca çözmekten hoşlanırım."},
        {"id": 28, "text": "Rüyalarımı çok net ve ayrıntılarıyla hatırlarım."},
        {"id": 29, "text": "Resimli kitapları daha çok severim."},
        {"id": 30, "text": "Kitaplarıma, defterlerime, diğer materyallere çizerim."},
    ],
    "muziksel": [
        {"id": 31, "text": "Şarkıların melodilerini rahatlıkla hatırlarım."},
        {"id": 32, "text": "Güzel şarkı söylerim."},
        {"id": 33, "text": "Müzik aleti çalar ya da çalmayı çok isterim."},
        {"id": 34, "text": "Müzik dersini çok severim."},
        {"id": 35, "text": "Ritmik konuşur ya da hareket ederim."},
        {"id": 36, "text": "Farkında olmadan mırıldanırım."},
        {"id": 37, "text": "Çalışırken elimle ya da ayağımla ritim tutarım."},
        {"id": 38, "text": "Çevredeki sesler çok dikkatimi çeker."},
        {"id": 39, "text": "Çalışırken müzik dinlemek çok hoşuma gider."},
        {"id": 40, "text": "Öğrendiğim şarkıları paylaşmayı severim."},
    ],
    "dogaci": [
        {"id": 41, "text": "Hayvanlara karşı çok meraklıyımdır."},
        {"id": 42, "text": "Doğaya karşı duyarsız olanlara kızarım."},
        {"id": 43, "text": "Evde hayvan besler ya da beslemeyi çok severim."},
        {"id": 44, "text": "Bahçede toprakla, bitkilerle oynamayı çok severim."},
        {"id": 45, "text": "Bitki beslemeyi severim."},
        {"id": 46, "text": "Çevre kirliliğine karşı çok duyarlıyımdır."},
        {"id": 47, "text": "Bitki ya da hayvanlarla ilgili belgesellere ilgi duyarım."},
        {"id": 48, "text": "Mevsimlerle ve iklim olaylarıyla çok ilgiliyimdir."},
        {"id": 49, "text": "Değişik meyve ve sebzelere karşı ilgiliyimdir."},
        {"id": 50, "text": "Doğa olaylarıyla çok ilgiliyimdir."},
    ],
    "sosyal": [
        {"id": 51, "text": "Arkadaşlarımla oyun oynamaktan hoşlanırım."},
        {"id": 52, "text": "Çevremde bir lider olarak görülürüm."},
        {"id": 53, "text": "Problemi olan arkadaşlarıma öğütler veririm."},
        {"id": 54, "text": "Arkadaşlarım fikirlerime değer verir."},
        {"id": 55, "text": "Organizasyonların vazgeçilmez elemanıyımdır."},
        {"id": 56, "text": "Arkadaşlarıma bir şeyler anlatmaktan çok hoşlanırım."},
        {"id": 57, "text": "Arkadaşlarımı sık sık ararım."},
        {"id": 58, "text": "Arkadaşlarımın sorunlarına yardımcı olmaktan hoşlanırım."},
        {"id": 59, "text": "Çevremdekiler benimle arkadaşlık kurmak ister."},
        {"id": 60, "text": "İnsanlara selam verir, hatır sorarım."},
    ],
    "bedensel": [
        {"id": 61, "text": "Koşmayı, atlamayı ve güreşmeyi çok severim."},
        {"id": 62, "text": "Oturduğum yerde duramam, kımıldanırım."},
        {"id": 63, "text": "Düşüncelerimi mimik-davranışlarla rahat ifade ederim."},
        {"id": 64, "text": "Bir şeyi okumak yerine yaparak öğrenmeyi severim."},
        {"id": 65, "text": "Merak ettiğim şeyleri elime alarak incelemek isterim."},
        {"id": 66, "text": "Boş vakitlerimi dışarıda geçirmek isterim."},
        {"id": 67, "text": "Arkadaşlarımla fiziksel oyunlar oynamayı severim."},
        {"id": 68, "text": "El becerilerim gelişmiştir."},
        {"id": 69, "text": "Sorunlarımı anlatırken vücut hareketlerini kullanırım."},
        {"id": 70, "text": "İnsanlara ve eşyalara dokunmaktan hoşlanırım."},
    ],
    "icsel": [
        {"id": 71, "text": "Bağımsız olmayı severim."},
        {"id": 72, "text": "Güçlü ve zayıf yanlarımı bilirim."},
        {"id": 73, "text": "Yalnız çalışmayı daha çok severim."},
        {"id": 74, "text": "Yalnız oynamayı severim."},
        {"id": 75, "text": "Yaptığım işleri arkadaşlarımla paylaşmayı severim."},
        {"id": 76, "text": "Yaptığım işlerin bilincindeyimdir."},
        {"id": 77, "text": "Pek kimseye akıl danışmam."},
        {"id": 78, "text": "Kendime saygım yüksektir."},
        {"id": 79, "text": "Yoğun olarak uğraştığım bir ilgi alanım, hobim vardır."},
        {"id": 80, "text": "Yardım istemeden kendi başıma ürünleri ortaya koyarım."},
    ]
}

# --- İLKÖĞRETİM VERSİYONU (40 SORU, Evet/Hayır) ---
# MEB EARGED kaynağından, her doğru cevap 8 puan

COKLU_ZEKA_QUESTIONS_ILKOGRETIM = {
    "sozel": [
        {"id": 1,  "text": "Kitaplara değer veririm."},
        {"id": 10, "text": "Televizyon ya da film seyretmektense radyo dinlemeyi tercih ederim."},
        {"id": 14, "text": "Kelime türetme ya da sözcük bulmacalarından hoşlanırım."},
        {"id": 16, "text": "Tekerlemeler, komik şiirler ya da kelime oyunları ile kendimi ve başkalarını eğlendirmekten hoşlanırım."},
        {"id": 26, "text": "Türkçe ve sosyal bilgiler dersleri matematik ve fen bilgisinden daha kolaydır."},
    ],
    "gorsel": [
        {"id": 3,  "text": "Kavramları okumadan ya da yazmadan önce gözümde canlandırabilirim."},
        {"id": 5,  "text": "Resim yaparken çeşitli renkleri uyum içinde kullanırım."},
        {"id": 15, "text": "Yap-boz, labirentler ve diğer görsel bulmacaları çözmekten hoşlanırım."},
        {"id": 21, "text": "Hiç bilmediğim yerde bile yolumu bulabilirim."},
        {"id": 34, "text": "Bir şeye yukarıdan kuşbakışı bakıldığında nasıl görünebileceğini rahatça gözümde canlandırabilirim."},
    ],
    "muziksel": [
        {"id": 7,  "text": "Bir şarkının yanlış söylendiğini hemen anlarım."},
        {"id": 19, "text": "Müziksiz bir hayat benim için çok sıkıcıdır."},
        {"id": 23, "text": "Yolda yürürken şarkılar mırıldanırım."},
        {"id": 35, "text": "Bir, iki kez duyduğum şarkıyı doğru bir şekilde söyleyebilirim."},
        {"id": 39, "text": "Ders çalışırken, iş yaparken ya da yeni bir şey öğrenirken sıkça şarkılar söyler ya da ayağımla yere vurarak tempo tutarım."},
    ],
    "icsel": [
        {"id": 20, "text": "Ulaşmak istediğim önemli hedeflerim var."},
        {"id": 25, "text": "Yaptığım hatalardan ders alırım."},
        {"id": 30, "text": "Arkadaşlarımla birlikte olmak yerine yalnız kalmayı isterim."},
        {"id": 33, "text": "Kendimi güçlü ve bağımsız hissediyorum."},
        {"id": 36, "text": "Günlük tutarım."},
    ],
    "mantiksal": [
        {"id": 2,  "text": "Kâğıt, kalem kullanmadan hesap yapabilirim."},
        {"id": 4,  "text": "Matematik çok sevdiğim derslerden biridir."},
        {"id": 11, "text": "Zekâ bulmacalarını çözmekten hoşlanırım."},
        {"id": 17, "text": "İşlerimi belli bir sıraya göre yaparım."},
        {"id": 37, "text": "Bir şeyi, ölçüldüğü, gruplandırıldığı ya da miktarı hesaplandığında daha iyi anlarım."},
    ],
    "bedensel": [
        {"id": 6,  "text": "Uzun süre hareketsiz kalmaya dayanamam."},
        {"id": 12, "text": "Dikiş, dokumacılık, oymacılık, doğramacılık ya da model yapmak gibi el becerisi gerektiren işlerle uğraşmayı severim."},
        {"id": 22, "text": "Konuşurken çeşitli hareketler yaparım."},
        {"id": 28, "text": "Yeni gördüğüm her şeye dokunmak isterim."},
        {"id": 38, "text": "Öğrenmek için okumak ya da izlemek yerine o konuda uygulama yapmayı isterim."},
    ],
    "sosyal": [
        {"id": 8,  "text": "Tek başıma koşmak ve yüzmek yerine arkadaşlarımla basketbol, voleybol gibi sporları yapmayı tercih ederim."},
        {"id": 13, "text": "Sorunlarımı kendi başıma çözmek yerine başka birinden yardım isterim."},
        {"id": 24, "text": "Bildiğim bir konuyu başkalarına öğretme konusunda herkese meydan okurum."},
        {"id": 29, "text": "Kendimi bir lider olarak görüyorum (ya da arkadaşlarım öyle olduğumu söylüyorlar)."},
        {"id": 31, "text": "Kalabalık içinde kendimi rahat hissederim."},
    ],
    "dogaci": [
        {"id": 9,  "text": "Kırlarda ve ormanda olmaktan hoşlanırım."},
        {"id": 18, "text": "Bazı insanların doğa konusundaki duyarsızlıkları beni çok üzer."},
        {"id": 27, "text": "Etrafımda hayvanların olmasından çok hoşlanırım."},
        {"id": 32, "text": "Çeşitli ağaç, kuş, bitki ve hayvan türleri arasındaki temel farklılıkları çok iyi bilirim."},
        {"id": 40, "text": "Canlılar ve bitkilerle ilgili kitapları okumak, belgeselleri izlemekten çok hoşlanırım."},
    ]
}


# --- PUANLAMA FONKSİYONU (LİSE) ---
def calculate_coklu_zeka_lise(answers):
    """
    Lise/Yetişkin versiyonu puanlama.
    answers: dict — {soru_id: 0-4 (Likert)}
    Maks per zeka: 10 soru × 4 = 40 puan
    """
    scores = {}
    for zeka_key in ZEKA_SIRA:
        questions = COKLU_ZEKA_QUESTIONS_LISE[zeka_key]
        total = sum(answers.get(q["id"], 0) for q in questions)
        max_possible = len(questions) * 4  # 10 × 4 = 40
        percentage = round(total / max_possible * 100, 1)
        scores[zeka_key] = {
            "raw": total,
            "max": max_possible,
            "pct": percentage
        }
    
    # Sıralama
    sorted_scores = sorted(scores.items(), key=lambda x: x[1]["pct"], reverse=True)
    top3 = sorted_scores[:3]
    bottom2 = sorted_scores[-2:]
    
    # İsimli skorlar (grafik uyumluluğu için)
    scores_named = {}
    for k, v in scores.items():
        scores_named[COKLU_ZEKA_DATA[k]["name"]] = v["pct"]
    
    result = {
        "version": "lise",
        "scores": scores,
        "scores_named": scores_named,
        "top3": top3,
        "bottom2": bottom2
    }
    
    report = generate_coklu_zeka_report(result)
    return result, report


# --- PUANLAMA FONKSİYONU (İLKÖĞRETİM) ---
def calculate_coklu_zeka_ilkogretim(answers):
    """
    İlköğretim versiyonu puanlama.
    answers: dict — {soru_id: "E" (Evet) veya "H" (Hayır)}
    Maks per zeka: 5 soru × 8 = 40 puan (her doğru 8 puan)
    """
    scores = {}
    for zeka_key in ZEKA_SIRA:
        questions = COKLU_ZEKA_QUESTIONS_ILKOGRETIM[zeka_key]
        total = sum(8 for q in questions if answers.get(q["id"]) == "E")
        max_possible = len(questions) * 8  # 5 × 8 = 40
        percentage = round(total / max_possible * 100, 1)
        scores[zeka_key] = {
            "raw": total,
            "max": max_possible,
            "pct": percentage
        }
    
    sorted_scores = sorted(scores.items(), key=lambda x: x[1]["pct"], reverse=True)
    top3 = sorted_scores[:3]
    bottom2 = sorted_scores[-2:]
    
    scores_named = {}
    for k, v in scores.items():
        scores_named[COKLU_ZEKA_DATA[k]["name"]] = v["pct"]
    
    result = {
        "version": "ilkogretim",
        "scores": scores,
        "scores_named": scores_named,
        "top3": top3,
        "bottom2": bottom2
    }
    
    report = generate_coklu_zeka_report(result)
    return result, report


# --- RAPOR ÜRETME (Ortak) ---
def generate_coklu_zeka_report(result):
    """
    Çoklu Zekâ raporu üretir. Her iki versiyon için ortak.
    """
    scores = result["scores"]
    top3 = result["top3"]
    bottom2 = result["bottom2"]
    version_text = "Lise/Yetişkin" if result["version"] == "lise" else "İlköğretim"
    
    report = f"""
# 🧠 ÇOKLU ZEKÂ DEĞERLENDİRME RAPORU
**Versiyon:** {version_text}

---

## 📊 Zekâ Profil Tablon

| Zekâ Türü | Puan | Yüzde | Grafik |
|---|---|---|---|
"""
    
    # Tüm zeka türlerini yüzdeye göre sırala
    sorted_all = sorted(scores.items(), key=lambda x: x[1]["pct"], reverse=True)
    
    for zeka_key, score_data in sorted_all:
        data = COKLU_ZEKA_DATA[zeka_key]
        pct = score_data["pct"]
        raw = score_data["raw"]
        max_s = score_data["max"]
        bar_len = round(pct / 10)
        bar = "█" * bar_len + "░" * (10 - bar_len)
        report += f"| {data['icon']} {data['name']} | {raw}/{max_s} | %{pct} | {bar} |\n"
    
    report += "\n---\n\n"
    
    # En güçlü 3 zeka
    report += "## 🏆 En Güçlü 3 Zekâ Alanın\n\n"
    
    for rank, (zeka_key, score_data) in enumerate(top3, 1):
        data = COKLU_ZEKA_DATA[zeka_key]
        medals = ["🥇", "🥈", "🥉"]
        
        report += f"### {medals[rank-1]} {rank}. {data['icon']} {data['name']} (%{score_data['pct']})\n\n"
        report += f"{data['description']}\n\n"
        
        report += "**Güçlü Yönlerin:**\n"
        for s in data["strengths"]:
            report += f"- ✅ {s}\n"
        report += "\n"
        
        report += "**Ders Çalışma İpuçları:**\n"
        for t in data["study_tips"]:
            report += f"- 💡 {t}\n"
        report += "\n"
        
        report += f"**Sana Uygun Kariyer Alanları:** {', '.join(data['careers'])}\n\n"
        report += "---\n\n"
    
    # Gelişime açık alanlar
    report += "## 🌱 Gelişime Açık Alanların\n\n"
    
    for zeka_key, score_data in bottom2:
        data = COKLU_ZEKA_DATA[zeka_key]
        report += f"### {data['icon']} {data['name']} (%{score_data['pct']})\n\n"
        report += f"Bu alanda henüz keşfetmediğin yeteneklerin olabilir. İşte geliştirmek için birkaç ipucu:\n\n"
        for t in data["study_tips"]:
            report += f"- 🌱 {t}\n"
        report += "\n"
    
    report += """
---

## 💬 Son Söz

Unutma, herkesin farklı zekâ alanlarında güçlü ve gelişime açık yönleri vardır. Hiçbir zekâ türü diğerinden daha iyi ya da kötü değildir! Howard Gardner'ın dediği gibi: "Her insan benzersiz bir zekâ kombinasyonuna sahiptir." Senin kombinasyonun da sana özel ve değerli! 🌟

Güçlü yönlerini kullanarak öğrenmeye devam et ve gelişime açık alanlarını da yavaş yavaş keşfet. Başarı, kendini tanımakla başlar! 🚀
"""
    return report.strip()


# ============================================================
# PARÇA 5: VARK ÖĞRENME STİLLERİ TESTİ
# Kaynak: Fleming VARK Questionnaire v8.02 (Türkçe uyarlama)
# 16 soru, her soru 4 seçenekli (a-d)
# 4 Öğrenme Stili: Visual, Aural, Read/Write, Kinesthetic
# Puanlama: Her seçenek V/A/R/K kategorisine ait
# ============================================================

# --- PUANLAMA TABLOSU (Resmi VARK Scoring Chart) ---
# Her soru için a/b/c/d hangi VARK kategorisine karşılık geliyor
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

# --- SABİT SORULAR (16 ADET, Türkçe uyarlama) ---
VARK_QUESTIONS = [
    {
        "id": 1,
        "text": "Bir yere gitmek istiyorsun ama yolu bilmiyorsun. Ne yaparsın?",
        "options": {
            "a": "Doğru yönde yürümeye başlar, yolu bulmaya çalışırım.",
            "b": "Birinden yol tarifi isterim veya sesli navigasyon kullanırım.",
            "c": "Yol tarifini yazılı olarak okurum.",
            "d": "Harita veya navigasyondaki haritaya bakarım."
        }
    },
    {
        "id": 2,
        "text": "Bir internet sitesinde grafik nasıl yapılır diye bir video var. Videoda konuşan biri, yazılı açıklamalar ve şemalar var. En çok hangisinden öğrenirsin?",
        "options": {
            "a": "Şemaları ve diyagramları görerek.",
            "b": "Anlatanı dinleyerek.",
            "c": "Yazılı açıklamaları okuyarak.",
            "d": "Yapılan işlemleri izleyerek."
        }
    },
    {
        "id": 3,
        "text": "Katılacağın bir gezi hakkında bilgi edinmek istiyorsun. Ne yaparsın?",
        "options": {
            "a": "Gezinin etkinlik ve öne çıkan yerlerinin detaylarına bakarım.",
            "b": "Haritaya bakıp gidilecek yerleri görürüm.",
            "c": "Gezi programını okuyarak bilgi edinirim.",
            "d": "Geziyi planlayan kişiyle ya da gidecek olan arkadaşlarımla konuşurum."
        }
    },
    {
        "id": 4,
        "text": "Gelecekte ne yapmak istediğine karar verirken hangisi senin için önemlidir?",
        "options": {
            "a": "Bilgimi gerçek durumlarla uygulayabilmek.",
            "b": "Başkalarıyla tartışarak iletişim kurabilmek.",
            "c": "Tasarımlarla, haritalarla veya çizelgelerle çalışabilmek.",
            "d": "Yazarak kendimi iyi ifade edebilmek."
        }
    },
    {
        "id": 5,
        "text": "Bir şey öğrenirken hangisini tercih edersin?",
        "options": {
            "a": "Konuyu biriyle konuşarak tartışmayı.",
            "b": "Kalıpları ve örüntüleri görmeyi.",
            "c": "Örnekler ve uygulamalar üzerinden denemeyi.",
            "d": "Kitap, makale ve ders notlarını okumayı."
        }
    },
    {
        "id": 6,
        "text": "Birçok seçenek arasında karar vermen gerekiyor. Ne yaparsın?",
        "options": {
            "a": "Her seçeneği kendi bilgilerimle örnekleyerek değerlendiririm.",
            "b": "Seçenekleri anlatan yazılı bir belgeyi okurum.",
            "c": "Karşılaştırma grafikleri ve tabloları incelerim.",
            "d": "Konuyu bilen biriyle konuşurum."
        }
    },
    {
        "id": 7,
        "text": "Yeni bir masa oyunu veya kart oyunu öğrenmek istiyorsun. Ne yaparsın?",
        "options": {
            "a": "Başkalarının oynamasını izler, sonra katılırım.",
            "b": "Birinin bana anlatmasını ve soru sormamı tercih ederim.",
            "c": "Oyunun şemalarını ve strateji diyagramlarını incelerim.",
            "d": "Oyunun kurallarını okurum."
        }
    },
    {
        "id": 8,
        "text": "Sağlığınla ilgili bir konu hakkında bilgi edinmek istiyorsun. Ne yaparsın?",
        "options": {
            "a": "Konuyla ilgili bir makale veya yazı okurum.",
            "b": "Konuyu anlatan bir model veya görsel üzerinde incelerim.",
            "c": "Doktorla veya konuyu bilenle detaylı konuşurum.",
            "d": "Konuyu gösteren bir şema veya diyagrama bakarım."
        }
    },
    {
        "id": 9,
        "text": "Bilgisayarda yeni bir şey öğrenmek istiyorsun. Ne yaparsın?",
        "options": {
            "a": "Yazılı kullanım kılavuzunu okurum.",
            "b": "Konuyu bilen birinden sözlü anlatım dinlerim.",
            "c": "Deneme-yanılma yöntemiyle kendim denerim.",
            "d": "Kitaptaki veya ekrandaki diyagramları takip ederim."
        }
    },
    {
        "id": 10,
        "text": "İnternetten bir şey öğrenirken hangisini tercih edersin?",
        "options": {
            "a": "Nasıl yapıldığını gösteren videoları.",
            "b": "İlginç tasarımları ve görsel özellikleri.",
            "c": "Detaylı yazılı makaleleri.",
            "d": "Uzmanların konuştuğu podcastleri ve videoları."
        }
    },
    {
        "id": 11,
        "text": "Yeni bir proje hakkında bilgi almak istiyorsun. Ne istersin?",
        "options": {
            "a": "Proje aşamalarını gösteren şemalar ve grafikler.",
            "b": "Projenin ana özelliklerini anlatan yazılı bir rapor.",
            "c": "Projeyi tartışma fırsatı.",
            "d": "Projenin başarıyla uygulandığı örnekler."
        }
    },
    {
        "id": 12,
        "text": "Daha iyi fotoğraf çekmeyi öğrenmek istiyorsun. Ne yaparsın?",
        "options": {
            "a": "Soru sorar, kamera ve özellikleri hakkında konuşurum.",
            "b": "Ne yapılması gerektiğini anlatan yazılı talimatları okurum.",
            "c": "Kameranın her parçasını gösteren şemaları incelerim.",
            "d": "İyi ve kötü fotoğraf örneklerini inceleyerek farkları anlarım."
        }
    },
    {
        "id": 13,
        "text": "Bir öğretmenin veya sunum yapan birinin hangisini kullanmasını tercih edersin?",
        "options": {
            "a": "Gösteriler, modeller veya uygulamalı çalışmalar.",
            "b": "Soru-cevap, tartışma veya konuk konuşmacılar.",
            "c": "Ders notları, kitaplar veya okuma materyalleri.",
            "d": "Şemalar, grafikler, haritalar veya çizelgeler."
        }
    },
    {
        "id": 14,
        "text": "Bir sınavdan veya yarışmadan sonra geri bildirim almak istiyorsun. Nasıl almayı tercih edersin?",
        "options": {
            "a": "Yaptıklarımdan örneklerle.",
            "b": "Sonuçlarımın yazılı açıklamasıyla.",
            "c": "Birinin benimle konuşarak açıklamasıyla.",
            "d": "Performansımı gösteren grafiklerle."
        }
    },
    {
        "id": 15,
        "text": "Bir evi veya daireyi ziyaret etmeden önce ne istersin?",
        "options": {
            "a": "Evin videosunu izlemeyi.",
            "b": "Ev sahibiyle konuşmayı.",
            "c": "Odaların ve özelliklerin yazılı açıklamasını okumayı.",
            "d": "Oda planını ve bölge haritasını görmeyi."
        }
    },
    {
        "id": 16,
        "text": "Parçalardan oluşan bir mobilyayı kurmakta zorlanıyorsun. Ne yaparsın?",
        "options": {
            "a": "Montaj aşamalarını gösteren şemaları incelerim.",
            "b": "Daha önce mobilya kurmuş birinden tavsiye isterim.",
            "c": "Birlikte gelen yazılı talimatları okurum.",
            "d": "Benzer bir mobilyayı kuran birinin videosunu izlerim."
        }
    },
]


# --- 4 ÖĞRENME STİLİ VERİLERİ ---
VARK_STYLES = {
    "V": {
        "name": "Görsel (Visual)",
        "icon": "👁️",
        "description": "Sen görsel bir öğrenicisin! Şemalar, grafikler, haritalar ve diyagramlar senin en iyi öğrenme araçların.",
        "characteristics": [
            "Haritalar, grafikler ve şemalardan kolay öğrenir",
            "Bilgiyi görsel düzende organize etmeyi sever",
            "Renk kodlama ve vurgulama kullanır",
            "Mekânsal düzenleme ve tasarım becerileri güçlüdür",
            "Yazılı metinden çok görsel materyalleri tercih eder"
        ],
        "study_tips": [
            "📊 Zihin haritaları ve kavram haritaları çiz.",
            "🎨 Renkli kalemler ve fosforlu kalemler kullan.",
            "📐 Konuları şema, diyagram ve tablo halinde düzenle.",
            "🗺️ Akış şemaları ve süreç diyagramları oluştur.",
            "📋 Not alırken oklar, kutucuklar ve semboller kullan."
        ],
        "avoid": "Uzun düz metinler ve sesli anlatımlar seni sıkabilir — görselleştir!"
    },
    "A": {
        "name": "İşitsel (Aural)",
        "icon": "👂",
        "description": "Sen işitsel bir öğrenicisin! Dinleyerek, tartışarak ve konuşarak en iyi şekilde öğreniyorsun.",
        "characteristics": [
            "Dersleri dinleyerek daha iyi anlar",
            "Tartışma ve soru-cevapla öğrenir",
            "Sesli tekrar yaparak ezberler",
            "Müzik ve ritimlerle bilgiyi hatırlar",
            "Sözlü talimatları kolayca takip eder"
        ],
        "study_tips": [
            "🎧 Ders sesli kayıtlarını dinle veya kendi kayıtlarını yap.",
            "🗣️ Öğrendiğin konuları birine sesli anlat.",
            "💬 Çalışma gruplarında tartışarak öğren.",
            "🎵 Önemli bilgileri kafiyeli veya ritmik cümlelerle ezberle.",
            "📱 Podcast ve sesli kitaplardan yararlan."
        ],
        "avoid": "Sessiz ve uzun okuma seansları seni yorabilir — sesli çalış!"
    },
    "R": {
        "name": "Okuma/Yazma (Read/Write)",
        "icon": "📖",
        "description": "Sen okuyarak ve yazarak öğrenen birisin! Yazılı materyaller senin en güçlü öğrenme kaynağın.",
        "characteristics": [
            "Kitap, makale ve ders notlarını okuyarak öğrenir",
            "Not almayı ve yazarak tekrar yapmayı sever",
            "Listeler ve yazılı planlar oluşturur",
            "Sözlükler ve ansiklopedileri kullanır",
            "Yazılı talimatları kolayca takip eder"
        ],
        "study_tips": [
            "📝 Bol bol not al ve notlarını düzenle.",
            "📋 Öğrendiğin konuları kendi kelimelerinle yaz.",
            "📚 Ders kitapları ve ek okuma kaynakları kullan.",
            "🗒️ Listeler, özetler ve tanım kartları (flashcard) hazırla.",
            "✍️ Sınava hazırlanırken soruları yazarak çalış."
        ],
        "avoid": "Sadece dinleme veya izleme yetersiz kalabilir — oku ve yaz!"
    },
    "K": {
        "name": "Kinestetik (Kinesthetic)",
        "icon": "🤸",
        "description": "Sen yaparak ve deneyerek öğrenen birisin! Uygulamalı etkinlikler senin en etkili öğrenme yolun.",
        "characteristics": [
            "Yaparak ve deneyerek öğrenir",
            "Uygulamalı çalışmaları tercih eder",
            "Gerçek hayat örnekleriyle konuları anlar",
            "Hareket ederken daha iyi düşünür",
            "Somut deneyimler ve simülasyonlarla öğrenir"
        ],
        "study_tips": [
            "🔬 Laboratuvar çalışmaları ve deneyler yap.",
            "🚶 Ders çalışırken yürüyerek tekrar et.",
            "🎭 Konuları canlandırarak veya rol yaparak öğren.",
            "✋ Model ve maketler yaparak somutlaştır.",
            "⏱️ Kısa süreli çalış, sık sık mola ver ve hareket et."
        ],
        "avoid": "Uzun süre oturup okumak seni yorabilir — hareket et ve uygula!"
    }
}


# --- PUANLAMA FONKSİYONU ---
def calculate_vark(answers):
    """
    VARK testini puanlar.
    
    VARK'ta öğrenci birden fazla şık seçebilir!
    answers: dict — {soru_id: ["a"] veya ["a", "c"] (liste)}
    
    Returns:
        (scores_dict, report_text)
    """
    vark_counts = {"V": 0, "A": 0, "R": 0, "K": 0}
    
    for qid, selected_options in answers.items():
        qid = int(qid)
        if qid not in VARK_SCORING:
            continue
        
        # Birden fazla seçenek seçilebilir
        if isinstance(selected_options, str):
            selected_options = [selected_options]
        
        for opt in selected_options:
            opt = opt.lower()
            if opt in VARK_SCORING[qid]:
                category = VARK_SCORING[qid][opt]
                vark_counts[category] += 1
    
    total = sum(vark_counts.values())
    
    # Yüzde hesapla
    percentages = {}
    for k, v in vark_counts.items():
        percentages[k] = round(v / total * 100, 1) if total > 0 else 0
    
    # Baskın stili bul
    sorted_styles = sorted(vark_counts.items(), key=lambda x: x[1], reverse=True)
    dominant = sorted_styles[0]
    second = sorted_styles[1]
    
    # Multimodal kontrol (üst iki arasında fark az mı?)
    is_multimodal = (dominant[1] - second[1]) <= 1 and dominant[1] > 0
    
    scores = {
        "counts": vark_counts,
        "percentages": percentages,
        "total_responses": total,
        "sorted": sorted_styles,
        "dominant": dominant,
        "is_multimodal": is_multimodal
    }
    
    report = generate_vark_report(scores)
    return scores, report


def generate_vark_report(scores):
    """
    VARK testi için şablon tabanlı rapor üretir.
    """
    counts = scores["counts"]
    percentages = scores["percentages"]
    sorted_styles = scores["sorted"]
    dominant_key = scores["dominant"][0]
    is_multimodal = scores["is_multimodal"]
    
    report = """
# 🎯 VARK ÖĞRENME STİLİ RAPORU

---

## 📊 Öğrenme Stili Profilin

| Stil | Puan | Yüzde | Grafik |
|---|---|---|---|
"""
    
    for style_key, count in sorted_styles:
        style = VARK_STYLES[style_key]
        pct = percentages[style_key]
        bar_len = round(pct / 10)
        bar = "█" * bar_len + "░" * (10 - bar_len)
        report += f"| {style['icon']} {style['name']} | {count} | %{pct} | {bar} |\n"
    
    report += "\n---\n\n"
    
    # Baskın stil
    if is_multimodal:
        top_two = sorted_styles[:2]
        report += "## 🌟 Senin Öğrenme Stilin: Çok Modlu (Multimodal)\n\n"
        report += "Birden fazla öğrenme stilini eşit derecede kullanıyorsun! Bu çok esnek bir öğrenme yeteneğine sahip olduğunu gösteriyor.\n\n"
        report += f"En güçlü iki stilin: **{VARK_STYLES[top_two[0][0]]['name']}** ve **{VARK_STYLES[top_two[1][0]]['name']}**\n\n"
        
        for style_key, _ in top_two:
            style = VARK_STYLES[style_key]
            report += f"### {style['icon']} {style['name']}\n\n"
            report += f"{style['description']}\n\n"
            report += "**Ders Çalışma İpuçları:**\n"
            for tip in style["study_tips"]:
                report += f"- {tip}\n"
            report += "\n"
    else:
        style = VARK_STYLES[dominant_key]
        report += f"## 🌟 Senin Baskın Öğrenme Stilin: {style['icon']} {style['name']}\n\n"
        report += f"{style['description']}\n\n"
        
        report += "**Seni Tanımlayan Özellikler:**\n"
        for c in style["characteristics"]:
            report += f"- ✅ {c}\n"
        report += "\n"
        
        report += "**Sana Özel Ders Çalışma İpuçları:**\n"
        for tip in style["study_tips"]:
            report += f"- {tip}\n"
        report += "\n"
        
        report += f"⚠️ **Dikkat:** {style['avoid']}\n\n"
    
    # Diğer stiller
    report += "---\n\n## 📚 Diğer Öğrenme Stillerin\n\n"
    
    start_idx = 2 if is_multimodal else 1
    for style_key, count in sorted_styles[start_idx:]:
        style = VARK_STYLES[style_key]
        pct = percentages[style_key]
        if pct > 0:
            report += f"### {style['icon']} {style['name']} (%{pct})\n"
            report += f"Bu stili de kullanıyorsun. İşte bu stilden faydalanmak için ipuçları:\n"
            for tip in style["study_tips"][:2]:
                report += f"- {tip}\n"
            report += "\n"
    
    report += """
---

## 💬 Son Söz

Öğrenme stilini bilmek, daha verimli çalışmanın anahtarıdır! Ama unutma, en iyi öğrenme genellikle birden fazla stilin birlikte kullanılmasıyla olur. Baskın stilini kullanarak başla, diğer stilleri de deneyerek öğrenme repertuarını genişlet. Herkesin öğrenme yolu farklıdır ve senin yolun sana özel! 🚀
"""
    return report.strip()


# ============================================================
# PARÇA 6: HOLLAND RIASEC MESLEKİ İLGİ ENVANTERİ
# Kaynak: Holland Tipoloji Kuramı, MEB RAM kaynakları
# 84 soru (6 tip × 14 etkinlik) — dengeli dağılım
# Puanlama: Hoşlanırım=2, Fark etmez=1, Hoşlanmam=0
# ============================================================

# --- 6 HOLLAND TİPİ VERİLERİ ---
HOLLAND_TYPES = {
    "R": {
        "name": "Gerçekçi (Realistic)",
        "icon": "🔧",
        "short": "Gerçekçi",
        "description": "Uygulamacı, somut ve pratik işleri seven bir yapın var! Elleriyle çalışmayı, fiziksel aktiviteleri ve somut sonuçlar üretmeyi tercih edersin.",
        "characteristics": [
            "Pratik ve uygulamacı",
            "El becerisi ve mekanik yeteneği güçlü",
            "Somut ve elle tutulur sonuçları sever",
            "Açık havada çalışmaktan hoşlanır",
            "Araç, makine ve aletlerle çalışmayı sever",
            "Sabırlı ve sebatkâr"
        ],
        "careers": [
            "Mühendis (Makine, Elektrik, İnşaat)",
            "Tekniker / Teknisyen",
            "Pilot",
            "Mimar (Uygulama)",
            "Ziraat Mühendisi",
            "Elektrikçi / Elektronikçi",
            "Ormancı",
            "Beden Eğitimi Öğretmeni",
            "Aşçı / Şef",
            "Denizci / Kaptan"
        ],
        "study_environment": "Laboratuvar, atölye ve açık hava etkinlikleri sana en uygun öğrenme ortamı."
    },
    "I": {
        "name": "Araştırmacı (Investigative)",
        "icon": "🔬",
        "short": "Araştırmacı",
        "description": "Meraklı, analitik ve bilimsel düşünmeyi seven bir yapın var! Problemleri araştırmayı, gözlem yapmayı ve çözüm üretmeyi seversin.",
        "characteristics": [
            "Meraklı ve analitik düşünür",
            "Bilimsel yöntemlere ilgi duyar",
            "Bağımsız çalışmayı tercih eder",
            "Matematiksel ve mantıksal düşünce güçlü",
            "Gözlem yapmayı ve araştırmayı sever",
            "Eleştirel ve sorgulayıcı"
        ],
        "careers": [
            "Bilim İnsanı (Fizikçi, Kimyager, Biyolog)",
            "Doktor / Tıp Uzmanı",
            "Eczacı",
            "Yazılım Mühendisi",
            "Araştırmacı / Akademisyen",
            "Psikolog",
            "Matematikçi",
            "Veteriner",
            "Biyomedikal Mühendisi",
            "Arkeolog"
        ],
        "study_environment": "Kütüphane, laboratuvar ve bireysel araştırma ortamları sana en uygun."
    },
    "A": {
        "name": "Sanatçı (Artistic)",
        "icon": "🎨",
        "short": "Sanatçı",
        "description": "Yaratıcı, özgür düşünceli ve estetik duyarlılığı yüksek bir yapın var! Kendini ifade etmeyi, hayal gücünü kullanmayı ve özgün eserler ortaya koymayı seversin.",
        "characteristics": [
            "Yaratıcı ve hayal gücü güçlü",
            "Estetik duyarlılığı yüksek",
            "Özgürlüğe ve bağımsızlığa değer verir",
            "Duygusal ve sezgisel",
            "Kurallara bağlı kalmaktan hoşlanmaz",
            "Kendini ifade etmeyi sever"
        ],
        "careers": [
            "Ressam / Heykeltıraş",
            "Grafik Tasarımcı",
            "Müzisyen / Besteci",
            "Yazar / Şair",
            "Oyuncu / Tiyatrocu",
            "Moda Tasarımcısı",
            "Fotoğrafçı",
            "İç Mimar / Dekoratör",
            "Film Yönetmeni",
            "Animatör / Çizgi Film Yapımcısı"
        ],
        "study_environment": "Sanat atölyeleri, stüdyolar ve yaratıcı projeler sana en uygun öğrenme ortamı."
    },
    "S": {
        "name": "Sosyal (Social)",
        "icon": "🤝",
        "short": "Sosyal",
        "description": "İnsanlarla çalışmayı, yardım etmeyi ve iletişim kurmayı seven bir yapın var! Başkalarına öğretmeyi, rehberlik etmeyi ve desteklemeyi seversin.",
        "characteristics": [
            "Yardımsever ve empatik",
            "İletişim becerileri güçlü",
            "İşbirliğine yatkın",
            "Sabırlı ve anlayışlı",
            "Toplumsal sorunlara duyarlı",
            "Öğretmeyi ve paylaşmayı sever"
        ],
        "careers": [
            "Öğretmen",
            "Psikolojik Danışman / Rehber",
            "Sosyal Hizmet Uzmanı",
            "Hemşire / Sağlık Personeli",
            "İnsan Kaynakları Uzmanı",
            "Fizyoterapist",
            "Diyetisyen",
            "Çocuk Gelişim Uzmanı",
            "Halkla İlişkiler Uzmanı",
            "Din Görevlisi"
        ],
        "study_environment": "Grup çalışmaları, tartışma ortamları ve toplum hizmeti projeleri sana çok uygun."
    },
    "E": {
        "name": "Girişimci (Enterprising)",
        "icon": "💼",
        "short": "Girişimci",
        "description": "Liderlik etmeyi, ikna etmeyi ve yönetmeyi seven bir yapın var! Risk almaktan çekinmez, insanları organize etmeyi ve hedeflere ulaşmayı seversin.",
        "characteristics": [
            "Liderlik yeteneği güçlü",
            "İkna edici ve etkili konuşur",
            "Risk almaktan çekinmez",
            "Enerjik ve hırslı",
            "Rekabetçi yapıda",
            "Organizasyon becerisi yüksek"
        ],
        "careers": [
            "İş İnsanı / Girişimci",
            "Avukat",
            "Pazarlama Müdürü",
            "Politikacı",
            "Satış Yöneticisi",
            "Emlakçı",
            "Spor Menajeri",
            "Gazeteci / Sunucu",
            "Proje Yöneticisi",
            "İthalat-İhracat Uzmanı"
        ],
        "study_environment": "Yarışmalar, münazaralar, liderlik projeleri ve iş simülasyonları sana çok uygun."
    },
    "C": {
        "name": "Gelenekçi (Conventional)",
        "icon": "📊",
        "short": "Gelenekçi",
        "description": "Düzenli, sistematik ve detaycı bir yapın var! Verileri organize etmeyi, kurallara uymayı ve işleri planlı bir şekilde yürütmeyi seversin.",
        "characteristics": [
            "Düzenli ve organize",
            "Detaycı ve titiz",
            "Kurallara uyar ve sorumluluk sahibi",
            "Sayısal verilere ilgili",
            "Planlı ve metodik çalışır",
            "Güvenilir ve tutarlı"
        ],
        "careers": [
            "Muhasebeci / Mali Müşavir",
            "Bankacı",
            "Memur / Bürokrat",
            "Vergi Müfettişi",
            "Sekreter / Ofis Yöneticisi",
            "Kütüphaneci",
            "Arşivci",
            "Hakim / Savcı",
            "İstatistikçi",
            "Bilgi Teknolojileri Uzmanı"
        ],
        "study_environment": "Düzenli programlar, listeler, planlı çalışma ve detaylı notlar sana en uygun öğrenme yöntemi."
    }
}

# Holland tip sırası
HOLLAND_ORDER = ["R", "I", "A", "S", "E", "C"]

# --- SABİT SORULAR (84 ADET: 6 × 14) ---
# Her soru: id, text, type (R/I/A/S/E/C)
# Puanlama: Hoşlanırım=2, Fark etmez=1, Hoşlanmam=0

HOLLAND_QUESTIONS = [
    # === R - Gerçekçi (14 soru) ===
    {"id": 1,  "text": "Bir makineyi söküp tekrar birleştirmek", "type": "R"},
    {"id": 2,  "text": "Ahşap, metal veya plastikten bir şeyler yapmak", "type": "R"},
    {"id": 3,  "text": "Araba veya bisiklet tamiri yapmak", "type": "R"},
    {"id": 4,  "text": "Bahçe işleriyle uğraşmak, toprakla çalışmak", "type": "R"},
    {"id": 5,  "text": "Spor yapmak veya fiziksel aktivitelerle uğraşmak", "type": "R"},
    {"id": 6,  "text": "Elektrik tesisatı veya elektronik devreler kurmak", "type": "R"},
    {"id": 7,  "text": "Açık havada, doğada çalışmak", "type": "R"},
    {"id": 8,  "text": "Hayvanlara bakmak veya onlarla çalışmak", "type": "R"},
    {"id": 9,  "text": "Bir binayı veya yapıyı inşa etmek veya onarmak", "type": "R"},
    {"id": 10, "text": "Aletler ve el aletleri kullanarak bir şeyler üretmek", "type": "R"},
    {"id": 11, "text": "Bilgisayar donanımını kurmak veya tamir etmek", "type": "R"},
    {"id": 12, "text": "Yemek pişirmek veya yiyecek hazırlamak", "type": "R"},
    {"id": 13, "text": "Bir arazi üzerinde ölçüm ve planlama yapmak", "type": "R"},
    {"id": 14, "text": "Maket veya model yapmak (uçak, gemi, araba vb.)", "type": "R"},

    # === I - Araştırmacı (14 soru) ===
    {"id": 15, "text": "Bilimsel bir deney yapmak", "type": "I"},
    {"id": 16, "text": "Matematik veya fen problemleri çözmek", "type": "I"},
    {"id": 17, "text": "Bir konuyu derinlemesine araştırmak", "type": "I"},
    {"id": 18, "text": "Bir olayın nedenlerini araştırıp analiz etmek", "type": "I"},
    {"id": 19, "text": "Laboratuvarda çalışmak", "type": "I"},
    {"id": 20, "text": "Bilimsel bir makale veya rapor okumak", "type": "I"},
    {"id": 21, "text": "Yıldızları ve gezegenleri gözlemlemek", "type": "I"},
    {"id": 22, "text": "İnsan vücudunun nasıl çalıştığını öğrenmek", "type": "I"},
    {"id": 23, "text": "Bir hipotez oluşturup test etmek", "type": "I"},
    {"id": 24, "text": "Doğadaki bitki ve hayvanları sınıflandırmak", "type": "I"},
    {"id": 25, "text": "Bilgisayar programlama veya kodlama yapmak", "type": "I"},
    {"id": 26, "text": "Karmaşık bir bulmacayı veya mantık sorusunu çözmek", "type": "I"},
    {"id": 27, "text": "Bir hastalığın tedavi yöntemlerini araştırmak", "type": "I"},
    {"id": 28, "text": "Yeni teknolojilerin nasıl çalıştığını incelemek", "type": "I"},

    # === A - Sanatçı (14 soru) ===
    {"id": 29, "text": "Resim yapmak veya boyamak", "type": "A"},
    {"id": 30, "text": "Müzik aleti çalmak veya şarkı söylemek", "type": "A"},
    {"id": 31, "text": "Hikaye, şiir veya roman yazmak", "type": "A"},
    {"id": 32, "text": "Bir tiyatro oyununda rol almak", "type": "A"},
    {"id": 33, "text": "Fotoğraf çekmek ve düzenlemek", "type": "A"},
    {"id": 34, "text": "Moda tasarımı yapmak, kıyafet tasarlamak", "type": "A"},
    {"id": 35, "text": "Bir odayı veya mekânı dekore etmek", "type": "A"},
    {"id": 36, "text": "Film veya video çekmek ve kurgulamak", "type": "A"},
    {"id": 37, "text": "Kendi bestelerimi veya şarkı sözlerimi yazmak", "type": "A"},
    {"id": 38, "text": "El sanatları (seramik, takı, ebru vb.) ile uğraşmak", "type": "A"},
    {"id": 39, "text": "Dans etmek veya koreografi oluşturmak", "type": "A"},
    {"id": 40, "text": "Dijital tasarım veya grafik tasarım yapmak", "type": "A"},
    {"id": 41, "text": "Bir sergiye, konsere veya tiyatroya gitmek", "type": "A"},
    {"id": 42, "text": "Kendi hayal dünyamda özgün fikirler geliştirmek", "type": "A"},

    # === S - Sosyal (14 soru) ===
    {"id": 43, "text": "Bir arkadaşıma derslerinde yardım etmek", "type": "S"},
    {"id": 44, "text": "Hasta veya yaşlı birine bakım yapmak", "type": "S"},
    {"id": 45, "text": "Bir gruba veya takıma liderlik etmek", "type": "S"},
    {"id": 46, "text": "Gönüllü olarak toplum hizmeti yapmak", "type": "S"},
    {"id": 47, "text": "İnsanların sorunlarını dinlemek ve çözüm önermek", "type": "S"},
    {"id": 48, "text": "Küçük çocuklara bir şeyler öğretmek", "type": "S"},
    {"id": 49, "text": "Bir hayır kurumunda çalışmak", "type": "S"},
    {"id": 50, "text": "İnsanlar arasındaki anlaşmazlıklarda arabuluculuk yapmak", "type": "S"},
    {"id": 51, "text": "Sınıf arkadaşlarıma ders anlatmak", "type": "S"},
    {"id": 52, "text": "Engelli bireylere destek olmak", "type": "S"},
    {"id": 53, "text": "Bir kampanya veya sosyal proje organize etmek", "type": "S"},
    {"id": 54, "text": "İnsanlara sağlıklı yaşam hakkında bilgi vermek", "type": "S"},
    {"id": 55, "text": "Bir spor takımını antrenman konusunda yönlendirmek", "type": "S"},
    {"id": 56, "text": "Yeni bir öğrencinin okula uyum sağlamasına yardım etmek", "type": "S"},

    # === E - Girişimci (14 soru) ===
    {"id": 57, "text": "Bir ürün veya fikri başkalarına satmak", "type": "E"},
    {"id": 58, "text": "Bir iş kurmak ve yönetmek", "type": "E"},
    {"id": 59, "text": "İnsanları ikna etmek ve etkilemek", "type": "E"},
    {"id": 60, "text": "Bir etkinlik veya organizasyon planlamak", "type": "E"},
    {"id": 61, "text": "Bir tartışmada veya münazarada yarışmak", "type": "E"},
    {"id": 62, "text": "Para yönetimi ve bütçe planlaması yapmak", "type": "E"},
    {"id": 63, "text": "Bir proje ekibini yönetmek ve yönlendirmek", "type": "E"},
    {"id": 64, "text": "Hızlı karar vermek ve risk almak", "type": "E"},
    {"id": 65, "text": "Yeni iş fikirleri geliştirmek", "type": "E"},
    {"id": 66, "text": "Bir ürünün reklamını veya tanıtımını yapmak", "type": "E"},
    {"id": 67, "text": "Topluluk önünde sunum yapmak veya konuşmak", "type": "E"},
    {"id": 68, "text": "Bir seçim kampanyasında çalışmak", "type": "E"},
    {"id": 69, "text": "İnsanlarla pazarlık yapmak ve anlaşma sağlamak", "type": "E"},
    {"id": 70, "text": "Sosyal medyada bir hesap veya sayfa yönetmek", "type": "E"},

    # === C - Gelenekçi (14 soru) ===
    {"id": 71, "text": "Dosyaları ve belgeleri düzenli bir şekilde arşivlemek", "type": "C"},
    {"id": 72, "text": "Bir tabloya veya listeye veri girmek", "type": "C"},
    {"id": 73, "text": "Hesap yapmak, gelir-gider tablosu hazırlamak", "type": "C"},
    {"id": 74, "text": "Yazışmaları ve raporları düzenli tutmak", "type": "C"},
    {"id": 75, "text": "Bir programı veya çizelgeyi takip etmek", "type": "C"},
    {"id": 76, "text": "Hatasız ve dikkatli bir şekilde form doldurmak", "type": "C"},
    {"id": 77, "text": "Bir kütüphane veya arşivde çalışmak", "type": "C"},
    {"id": 78, "text": "Envanter veya stok sayımı yapmak", "type": "C"},
    {"id": 79, "text": "Bilgileri sınıflandırmak ve kategorilere ayırmak", "type": "C"},
    {"id": 80, "text": "Kurallara ve prosedürlere uygun çalışmak", "type": "C"},
    {"id": 81, "text": "Bir bütçeyi veya hesabı kontrol etmek", "type": "C"},
    {"id": 82, "text": "Ofis programlarında (Excel, Word) çalışmak", "type": "C"},
    {"id": 83, "text": "Posta, kargo veya teslimat işlerini organize etmek", "type": "C"},
    {"id": 84, "text": "Bir işin her adımını planlayıp kontrol listesi hazırlamak", "type": "C"},
]


# --- PUANLAMA FONKSİYONU ---
def calculate_holland(answers):
    """
    Holland RIASEC testini puanlar.
    
    Args:
        answers: dict — {soru_id: 2 (Hoşlanırım), 1 (Fark etmez), 0 (Hoşlanmam)}
    
    Returns:
        (scores_dict, report_text)
    """
    type_scores = {t: 0 for t in HOLLAND_ORDER}
    type_max = {t: 0 for t in HOLLAND_ORDER}
    
    for q in HOLLAND_QUESTIONS:
        q_type = q["type"]
        type_max[q_type] += 2  # max 2 per question
        
        ans = answers.get(q["id"], 0)
        type_scores[q_type] += ans
    
    # Yüzdeler
    percentages = {}
    for t in HOLLAND_ORDER:
        pct = round(type_scores[t] / type_max[t] * 100, 1) if type_max[t] > 0 else 0
        percentages[t] = pct
    
    # Sıralama
    sorted_types = sorted(type_scores.items(), key=lambda x: x[1], reverse=True)
    top3 = sorted_types[:3]
    
    # Holland kodu (en yüksek 3 harfin birleşimi)
    holland_code = "".join([t[0] for t in top3])
    
    scores = {
        "raw_scores": type_scores,
        "max_scores": type_max,
        "percentages": percentages,
        "sorted": sorted_types,
        "top3": top3,
        "holland_code": holland_code
    }
    
    report = generate_holland_report(scores)
    return scores, report


def generate_holland_report(scores):
    """
    Holland RIASEC raporu üretir.
    """
    raw = scores["raw_scores"]
    max_s = scores["max_scores"]
    pcts = scores["percentages"]
    sorted_types = scores["sorted"]
    top3 = scores["top3"]
    holland_code = scores["holland_code"]
    
    report = f"""
# 🧭 HOLLAND RIASEC MESLEKİ İLGİ RAPORU

**Senin Holland Kodun:** 🏷️ **{holland_code}**

---

## 📊 Mesleki İlgi Profilin

| Tip | Puan | Yüzde | Grafik |
|---|---|---|---|
"""
    
    for t_key, t_score in sorted_types:
        t_data = HOLLAND_TYPES[t_key]
        pct = pcts[t_key]
        mx = max_s[t_key]
        bar_len = round(pct / 10)
        bar = "█" * bar_len + "░" * (10 - bar_len)
        report += f"| {t_data['icon']} {t_data['short']} | {t_score}/{mx} | %{pct} | {bar} |\n"
    
    report += "\n---\n\n"
    
    # En güçlü 3 tip
    report += "## 🏆 En Güçlü 3 Mesleki İlgi Alanın\n\n"
    
    medals = ["🥇", "🥈", "🥉"]
    for rank, (t_key, t_score) in enumerate(top3):
        t_data = HOLLAND_TYPES[t_key]
        pct = pcts[t_key]
        
        report += f"### {medals[rank]} {rank+1}. {t_data['icon']} {t_data['name']} (%{pct})\n\n"
        report += f"{t_data['description']}\n\n"
        
        report += "**Seni Tanımlayan Özellikler:**\n"
        for c in t_data["characteristics"]:
            report += f"- ✅ {c}\n"
        report += "\n"
        
        report += f"**Sana Uygun Meslekler:**\n"
        for career in t_data["careers"]:
            report += f"- 💼 {career}\n"
        report += "\n"
        
        report += f"**Öğrenme Ortamı:** {t_data['study_environment']}\n\n"
        report += "---\n\n"
    
    # Holland Kodu Açıklaması
    code_names = [HOLLAND_TYPES[c]["short"] for c in holland_code]
    report += f"## 🏷️ Holland Kodun: {holland_code}\n\n"
    report += f"Bu kod, senin en güçlü üç ilgi alanının birleşimidir: **{code_names[0]}** + **{code_names[1]}** + **{code_names[2]}**\n\n"
    report += "Bu üç alanın kesiştiği meslekler senin için en uygun olanlardır. Meslek seçimi yaparken bu üç alanı birlikte değerlendirmeni öneriyoruz.\n\n"
    
    # Altıgen Açıklaması
    report += """
---

## 🔷 Holland Altıgen Modeli

Holland'ın kuramına göre, altıgendeki birbirine yakın tipler (örn. R-I veya S-E) daha uyumludur. Senin kodundaki harfler ne kadar yakınsa, ilgi alanların o kadar tutarlıdır.

```
        R (Gerçekçi)
       / \\
      I   C (Gelenekçi)
      |   |
      A   E (Girişimci)
       \\ /
        S (Sosyal)
```

---

## 💬 Son Söz

Bu test, senin mesleki ilgi alanlarını gösteriyor — ama unutma, ilgi alanları zamanla değişebilir ve gelişebilir! Önemli olan kendin hakkında daha fazla şey öğrenmek ve farklı alanlara da şans vermektir. Meslek seçimi bir süreçtir ve bu süreçte rehber öğretmenin ve ailen sana yol gösterebilir. Sen ne olmak istiyorsan, onun için çalışabilirsin! 🚀
"""
    return report.strip()
