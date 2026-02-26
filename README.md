# 🎓 Eğitim Check-Up — Psikometrik Test Uygulaması

Öğrencilere yönelik **9 farklı psikometrik test** sunan, Streamlit tabanlı eğitim psikolojisi uygulaması.
Öğretmen paneli ile AI destekli (Claude) bireysel ve bütüncül analiz raporları üretilebilir.

## 🧪 Testler

| Test | Soru | Açıklama |
|------|------|----------|
| Enneagram Kişilik | 180 | 9 kişilik tipi, kanat analizi |
| Çalışma Davranışı | 73 | Ders çalışma alışkanlıkları |
| Sağ-Sol Beyin | 30 | Beyin dominansı |
| Sınav Kaygısı | 50 | 7 alt boyut, 3 kademe |
| VARK Öğrenme Stili | 16 | Görsel/İşitsel/Okuma/Kinestetik |
| Çoklu Zeka | 80 | Gardner 8 zeka alanı (İlköğretim + Lise) |
| Holland RIASEC | 84 | Mesleki ilgi, 3 harfli kod |
| D2 Dikkat | 280 | Zamanlı dikkat/konsantrasyon |
| Akademik Analiz | 67 | 4 kademe, zorluk ağırlıklı puanlama |

## 🚀 Kurulum

```bash
# 1. Repo'yu klonla
git clone https://github.com/Ahmet571-es/psiko-test-uygulamasi.git
cd psiko-test-uygulamasi

# 2. Bağımlılıkları yükle
pip install -r requirements.txt

# 3. Ortam değişkenlerini ayarla
cp .env.example .env
# .env dosyasını düzenle (API key, DB URL, şifre)

# 4. Uygulamayı başlat
streamlit run app.py
```

## ⚙️ Ortam Değişkenleri

| Değişken | Zorunlu | Açıklama |
|----------|---------|----------|
| `SUPABASE_DB_URL` | Evet* | PostgreSQL bağlantı URL'si |
| `ANTHROPIC_API_KEY` | Evet | Claude API anahtarı |
| `TEACHER_PASSWORD` | Evet | Öğretmen paneli şifresi |
| `CLAUDE_MODEL` | Hayır | Claude model adı (varsayılan: claude-sonnet-4-20250514) |

\* URL yoksa SQLite kullanılır (lokal geliştirme).

## 📁 Dosya Yapısı

```
app.py              — Ana uygulama (giriş/kayıt)
student_view.py     — Öğrenci test arayüzü
teacher_view.py     — Öğretmen analiz paneli
db_utils.py         — Veritabanı işlemleri (PostgreSQL + SQLite)
test_data.py        — Test soruları ve puanlama fonksiyonları
akademik_engine.py  — Akademik Analiz v2 (4 kademe, zorluk ağırlıklı)
d2_engine.py        — D2 Dikkat Testi motoru
requirements.txt    — Python bağımlılıkları
```

## 🛠️ Teknolojiler

- **Frontend:** Streamlit
- **Backend:** Python 3.10+
- **Veritabanı:** PostgreSQL (Supabase) / SQLite fallback
- **AI:** Anthropic Claude API
- **Görselleştirme:** Matplotlib, Seaborn
