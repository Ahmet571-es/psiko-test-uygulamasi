"""
D2 Dikkat Testi — Dijital Motor
================================
Brickenkamp d2 dikkat testinin Streamlit uyumlu dijital adaptasyonu.

Semboller : "d" ve "p" harfleri, üst/altlarında 0-2 arası kısa çizgi
Hedef     : Toplam 2 çizgisi olan "d" harfleri
Yapı      : 14 satır × 20 sembol = 280 stimulus
Süre      : Satır başına 15 saniye (dijital uyarlama)

Skorlama (orijinal d2 formülleri):
  TN   – Toplam İşaretleme
  E1   – Atlama Hatası  (hedef atlandı)
  E2   – Yanlış İşaretleme (dikkat dağıtıcı işaretlendi)
  E    – Toplam Hata (E1 + E2)
  TN-E – Toplam Performans
  CP   – Konsantrasyon Performansı (doğru hedef − E2)
  FR   – Dalgalanma Oranı (max satır CP − min satır CP)
"""

import random

# ============================================================
# KONFİGÜRASYON
# ============================================================
D2_CONFIG = {
    "rows": 14,
    "symbols_per_row": 20,
    "time_per_row": 15,          # varsayılan saniye (yaşa göre değişir)
    "target_ratio": 0.40,        # her satırda ~%40 hedef
    "practice_symbols": 10,      # alıştırma satırı
}

# ============================================================
# YAŞA GÖRE SÜRE TABLOSU
# ============================================================
# Brickenkamp normlarına uygun dijital uyarlama:
#   7-9 yaş  : Motor beceri ve dikkat gelişimi erken → geniş süre
#   10-12 yaş: İlköğretim geçiş dönemi → orta süre
#   13-15 yaş: Ergenlik, ortalama dikkat kapasitesi → standart süre
#   16+ yaş  : Tam kapasite → kısa süre
# ============================================================

AGE_TIME_TABLE = [
    (9,  25),   # 7-9 yaş  → 25 saniye
    (12, 20),   # 10-12 yaş → 20 saniye
    (15, 15),   # 13-15 yaş → 15 saniye (standart)
    (999, 12),  # 16+ yaş   → 12 saniye
]


def get_time_per_row(age=None):
    """
    Öğrenci yaşına göre satır başına süreyi (saniye) döndürür.
    age=None ise varsayılan 15 saniye kullanılır.
    """
    if age is None:
        return D2_CONFIG["time_per_row"]
    for max_age, seconds in AGE_TIME_TABLE:
        if age <= max_age:
            return seconds
    return D2_CONFIG["time_per_row"]

# ============================================================
# SEMBOL TİPLERİ
# ============================================================
# (harf, üst_çizgi, alt_çizgi) → toplam 1-4 arası
ALL_SYMBOL_TYPES = []
for letter in ("d", "p"):
    for above in range(3):       # 0, 1, 2
        for below in range(3):
            total = above + below
            if 1 <= total <= 4:
                ALL_SYMBOL_TYPES.append({
                    "letter": letter,
                    "above": above,
                    "below": below,
                    "total": total,
                    "is_target": (letter == "d" and total == 2),
                })

TARGET_TYPES     = [s for s in ALL_SYMBOL_TYPES if s["is_target"]]
DISTRACTOR_TYPES = [s for s in ALL_SYMBOL_TYPES if not s["is_target"]]


# ============================================================
# SATIR / TEST ÜRETİCİ
# ============================================================
def generate_d2_row(n=20, target_ratio=0.40, rng=None):
    """Bir satır D2 sembolü üretir."""
    if rng is None:
        rng = random.Random()

    num_targets = round(n * target_ratio)
    num_dist    = n - num_targets

    row = []
    for _ in range(num_targets):
        row.append({**rng.choice(TARGET_TYPES)})
    for _ in range(num_dist):
        row.append({**rng.choice(DISTRACTOR_TYPES)})

    rng.shuffle(row)
    for i, sym in enumerate(row):
        sym["index"] = i
    return row


def generate_d2_test(seed=None):
    """14 satırlık tam D2 testi üretir."""
    rng = random.Random(seed)
    return [
        generate_d2_row(D2_CONFIG["symbols_per_row"],
                        D2_CONFIG["target_ratio"], rng)
        for _ in range(D2_CONFIG["rows"])
    ]


def generate_practice_row(seed=42):
    """Kısa alıştırma satırı (10 sembol)."""
    rng = random.Random(seed)
    return generate_d2_row(D2_CONFIG["practice_symbols"], 0.40, rng)


# ============================================================
# HTML RENDER
# ============================================================
def _marks_html(count):
    """Çizgileri dikey bar olarak render eder."""
    if count == 0:
        return '<div style="height:14px;">&nbsp;</div>'
    bars = "".join(
        '<span style="display:inline-block;width:3px;height:12px;'
        'background:#444;border-radius:1px;margin:0 2px;"></span>'
        for _ in range(count)
    )
    return (
        f'<div style="height:14px;display:flex;'
        f'justify-content:center;align-items:center;">{bars}</div>'
    )


def render_symbol_html(symbol, show_number=True):
    """Tek bir D2 sembolünü HTML olarak render eder."""
    idx_html = ""
    if show_number:
        idx_html = (
            f'<div style="font-size:9px;color:#bbb;margin-bottom:1px;">'
            f'{symbol["index"] + 1}</div>'
        )

    above = _marks_html(symbol["above"])
    below = _marks_html(symbol["below"])
    letter = symbol["letter"]

    return f"""<div style="text-align:center;padding:2px 0;min-width:44px;">
{idx_html}
{above}
<div style="font-size:26px;font-weight:800;color:#1B2A4A;line-height:30px;">{letter}</div>
{below}
</div>"""


def render_row_legend_html():
    """Hedef sembol açıklama kutusu."""
    examples = [s for s in TARGET_TYPES]
    ex_html = ""
    for s in examples:
        ex_html += render_symbol_html({**s, "index": 0}, show_number=False)

    return f"""
<div style="background:#f0f7ff;border:1px solid #b0d4f1;border-radius:10px;
            padding:12px 16px;margin-bottom:12px;">
  <div style="font-weight:700;color:#1B2A4A;margin-bottom:6px;">
    🎯 Hedef Semboller (sadece bunları işaretle):
  </div>
  <div style="display:flex;gap:16px;align-items:center;justify-content:center;">
    {ex_html}
  </div>
  <div style="font-size:0.82rem;color:#666;margin-top:6px;">
    <b>d</b> harfi + toplam <b>2 çizgi</b> (üstte ve/veya altta)
  </div>
</div>"""


def render_timer_js(seconds, row_num):
    """JavaScript geri sayım zamanlayıcısı."""
    return f"""
<div id="d2timer_{row_num}"
     style="text-align:center;font-size:2rem;font-weight:800;
            color:#1B2A4A;padding:6px 0;">
  ⏱️ {seconds}
</div>
<script>
(function() {{
  var timeLeft = {seconds};
  var el = document.getElementById('d2timer_{row_num}');
  if (!el) return;
  var iv = setInterval(function() {{
    timeLeft--;
    if (timeLeft <= 0) {{
      clearInterval(iv);
      el.textContent = '⏰ Süre doldu!';
      el.style.color = '#E74C3C';
    }} else {{
      el.textContent = '⏱️ ' + timeLeft;
      if (timeLeft <= 5) el.style.color = '#E74C3C';
      else if (timeLeft <= 10) el.style.color = '#F39C12';
    }}
  }}, 1000);
}})();
</script>"""


# ============================================================
# SKORLAMA
# ============================================================
def calculate_d2(row_results, time_per_row=None):
    """
    D2 test skorlarını hesaplar.

    Parametre
    ---------
    row_results : list[dict]
        Her eleman: {symbols, selected (list[bool]), elapsed_time}
    time_per_row : int | None
        Yaşa göre satır süresi (raporlama için)

    Döndürür
    --------
    dict : TN, E1, E2, E, TN_E, CP, FR ve yorumlar
    """
    total_tn = total_e1 = total_e2 = total_correct = total_targets = 0
    row_cps   = []     # satır bazlı CP
    row_tns   = []     # satır bazlı TN
    row_times = []

    for row in row_results:
        symbols  = row["symbols"]
        selected = row["selected"]
        elapsed  = row.get("elapsed_time", D2_CONFIG["time_per_row"])

        tn = sum(1 for s in selected if s)
        e1 = e2 = correct = targets = 0

        for sym, sel in zip(symbols, selected):
            if sym["is_target"]:
                targets += 1
                if sel:
                    correct += 1
                else:
                    e1 += 1
            else:
                if sel:
                    e2 += 1

        row_cps.append(correct - e2)
        row_tns.append(tn)
        row_times.append(elapsed)

        total_tn      += tn
        total_e1      += e1
        total_e2      += e2
        total_correct += correct
        total_targets += targets

    total_e = total_e1 + total_e2
    tn_e    = total_tn - total_e
    cp      = total_correct - total_e2
    fr      = (max(row_cps) - min(row_cps)) if row_cps else 0

    error_pct = round((total_e / max(total_tn, 1)) * 100, 1)
    hit_rate  = round((total_correct / max(total_targets, 1)) * 100, 1)
    cp_pct    = round((cp / max(total_targets, 1)) * 100, 1)

    # --- Dikkat seviyesi ---
    if cp_pct >= 80:
        level, level_desc = "Çok Yüksek", "Dikkat ve konsantrasyon kapasitesi mükemmel düzeyde."
    elif cp_pct >= 60:
        level, level_desc = "Yüksek", "Dikkat seviyesi ortalamanın üzerinde, güçlü konsantrasyon."
    elif cp_pct >= 40:
        level, level_desc = "Orta", "Dikkat seviyesi ortalama düzeyde."
    elif cp_pct >= 20:
        level, level_desc = "Düşük", "Dikkat seviyesi ortalamanın altında, gelişime açık."
    else:
        level, level_desc = "Çok Düşük", "Dikkat ve konsantrasyon alanında ciddi destek ihtiyacı."

    # --- Hız-doğruluk dengesi ---
    if hit_rate >= 80 and error_pct <= 10:
        balance = "Dengeli (Hızlı ve Doğru)"
        balance_desc = "Hem hız hem doğruluk yüksek — ideal performans profili."
    elif hit_rate >= 60 and error_pct > 15:
        balance = "Dürtüsel (Hızlı ama Hatalı)"
        balance_desc = "Hızlı çalışıyor ama dikkat dağılması nedeniyle hata oranı yüksek."
    elif hit_rate < 50 and error_pct <= 10:
        balance = "Temkinli (Yavaş ama Doğru)"
        balance_desc = "Az işaretleme yapıyor ama doğruluk yüksek — cesaretlendirme gerekli."
    else:
        balance = "Gelişime Açık"
        balance_desc = "Hem hız hem doğruluk alanında gelişim potansiyeli var."

    # --- Tutarlılık ---
    if fr <= 3:
        cons, cons_desc = "Çok Tutarlı", "Satırlar arası performans çok dengeli — sürdürülebilir dikkat."
    elif fr <= 5:
        cons, cons_desc = "Tutarlı", "Performans genel olarak dengeli, hafif dalgalanmalar normal."
    elif fr <= 8:
        cons, cons_desc = "Değişken", "Satırlar arası belirgin performans farkları — dikkat dalgalanması."
    else:
        cons, cons_desc = "Çok Değişken", "Ciddi performans dalgalanması — sürdürülebilir dikkat sorunu."

    return {
        "TN": total_tn, "E1": total_e1, "E2": total_e2, "E": total_e,
        "TN_E": tn_e, "CP": cp, "FR": fr,
        "hit_rate": hit_rate, "error_pct": error_pct, "cp_pct": cp_pct,
        "level": level, "level_desc": level_desc,
        "balance": balance, "balance_desc": balance_desc,
        "consistency": cons, "consistency_desc": cons_desc,
        "row_performances": row_cps, "row_speeds": row_tns,
        "row_times": row_times,
        "total_targets": total_targets, "total_correct": total_correct,
        "time_per_row": time_per_row,
    }


# ============================================================
# RAPOR ÜRETİCİ
# ============================================================
def generate_d2_report(scores):
    """Şablon tabanlı metin rapor üretir."""

    def bar(pct):
        n = max(0, min(10, round(pct / 10)))
        return "█" * n + "░" * (10 - n)

    row_table = "\n".join(
        f"| Satır {i+1:2d} | {cp:4d} | {spd:4d} |"
        for i, (cp, spd) in enumerate(
            zip(scores["row_performances"], scores["row_speeds"])
        )
    )

    report = f"""# 🎯 D2 DİKKAT TESTİ RAPORU

---

## 📊 Genel Performans Özeti

| Metrik | Değer | Açıklama |
|--------|-------|----------|
| 🎯 Konsantrasyon (CP) | **{scores['CP']}** | Doğru hedefler − Yanlış işaretlemeler |
| ⚡ Toplam Performans (TN-E) | **{scores['TN_E']}** | Toplam işaretleme − Toplam hata |
| 📊 Toplam İşaretleme (TN) | {scores['TN']} | Tüm satırlarda işaretlenen sembol sayısı |
| ❌ Toplam Hata (E) | {scores['E']} | Atlama ({scores['E1']}) + Yanlış ({scores['E2']}) |
| 📈 Dalgalanma (FR) | {scores['FR']} | En yüksek − en düşük satır performansı |"""

    if scores.get("time_per_row"):
        report += f"""
| ⏱️ Satır Süresi | {scores['time_per_row']} sn | Yaşa göre belirlenen süre |"""

    report += """---

## 🧠 Dikkat Seviyesi: **{scores['level']}**

{bar(scores['cp_pct'])} %{scores['cp_pct']}

{scores['level_desc']}

---

## ⚖️ Hız-Doğruluk Dengesi: **{scores['balance']}**

| Gösterge | Değer |
|----------|-------|
| Hedef Yakalama Oranı | %{scores['hit_rate']} |
| Hata Oranı | %{scores['error_pct']} |

{scores['balance_desc']}

---

## 📈 Tutarlılık: **{scores['consistency']}**

{scores['consistency_desc']}

---

## 📉 Satır Bazlı Performans

| Satır | CP | Hız |
|-------|-----|-----|
{row_table}

---

## 🔍 Hata Analizi

| Hata Türü | Sayı | Anlam |
|-----------|------|-------|
| Atlama Hatası (E1) | {scores['E1']} | Hedef sembollerin kaçırılması — dikkat dağılması |
| Yanlış İşaretleme (E2) | {scores['E2']} | Hedef olmayan sembollerin işaretlenmesi — dürtüsellik |

---

## 💡 Yorum ve Öneriler

"""

    # Seviyeye göre öneriler
    if scores["level"] in ("Çok Yüksek", "Yüksek"):
        report += (
            "Dikkat ve konsantrasyon kapasitesi güçlü bir profil sergileniyor.\n\n"
            "**Öneriler:**\n"
            "- 🎯 Karmaşık görevlerle dikkat kapasitesini daha da geliştir\n"
            "- 📚 Uzun süreli odaklanma gerektiren çalışmalarda bu güçlü yanını kullan\n"
            "- 🧘 Düzenli zihinsel egzersizlerle bu seviyeyi koru\n"
        )
    elif scores["level"] == "Orta":
        report += (
            "Dikkat seviyesi ortalama düzeyde. Gelişim potansiyeli var.\n\n"
            "**Öneriler:**\n"
            "- ⏱️ Pomodoro tekniği ile odaklanma sürelerini kademeli artır\n"
            "- 🎮 Dikkat geliştirici oyunlar ve bulmacalar ile pratik yap\n"
            "- 📵 Çalışma ortamından dikkat dağıtıcıları uzaklaştır\n"
            "- 💤 Düzenli uyku ve beslenme dikkat performansını doğrudan etkiler\n"
        )
    else:
        report += (
            "Dikkat ve konsantrasyon alanında gelişim ihtiyacı tespit edildi. "
            "Bu tamamen geliştirilebilir bir beceridir.\n\n"
            "**Öneriler:**\n"
            "- 🏃 Düzenli fiziksel aktivite dikkat kapasitesini artırır\n"
            "- ⏱️ Kısa odaklanma süreleriyle başla (5 dk) ve kademeli artır\n"
            "- 🎯 Tek seferde tek iş yap — çoklu görevden kaçın\n"
            "- 📝 Görevleri küçük parçalara böl\n"
            "- 🧘 Nefes egzersizleri ve mindfulness pratikleri faydalı olabilir\n"
        )

    if scores["balance"] == "Dürtüsel (Hızlı ama Hatalı)":
        report += (
            "\n**⚡ Dürtüsellik Notu:**\n"
            "Hızlı çalışma eğilimi hata oranını artırıyor. "
            "'Önce doğru, sonra hızlı' prensibini benimse.\n"
        )
    elif scores["balance"] == "Temkinli (Yavaş ama Doğru)":
        report += (
            "\n**🐢 Temkinlilik Notu:**\n"
            "Doğruluk oranı yüksek ama hız düşük. "
            "Zamanlı pratiklerle hızı kademeli olarak artır.\n"
        )

    report += f"""
---

## 📌 Özet Tablo

| Gösterge | Sonuç |
|----------|-------|
| Dikkat Seviyesi | **{scores['level']}** |
| Hız-Doğruluk | **{scores['balance']}** |
| Tutarlılık | **{scores['consistency']}** |
| Konsantrasyon Puanı | **{scores['CP']}/{scores['total_targets']}** |
| Genel Hata | **{scores['E']}** (Atlama: {scores['E1']}, Yanlış: {scores['E2']}) |
"""
    return report.strip()


# ============================================================
# D2 KART STİLİ CSS (Checkbox → Tıklanabilir Kart)
# ============================================================

D2_CARD_CSS = """
<style>
/* ── D2 Grid Layout ── */
div[data-testid="stForm"] .d2-grid-row {
    display: grid;
    grid-template-columns: repeat(10, 1fr);
    gap: 6px;
    margin-bottom: 8px;
}
@media (max-width: 700px) {
    div[data-testid="stForm"] .d2-grid-row {
        grid-template-columns: repeat(5, 1fr);
    }
}

/* ── Sembol kartlarını stillendir ── */
div[data-testid="stForm"] div[data-testid="stCheckbox"] {
    background: #f8f9fc;
    border: 2px solid #dde1e8;
    border-radius: 10px;
    padding: 6px 2px 8px;
    text-align: center;
    transition: all 0.12s ease;
    cursor: pointer;
}
div[data-testid="stForm"] div[data-testid="stCheckbox"]:hover {
    border-color: #64b5f6;
    background: #e8f0fe;
    transform: translateY(-1px);
    box-shadow: 0 3px 8px rgba(0,0,0,0.10);
}

/* ── Seçili kart stili ── */
div[data-testid="stForm"] div[data-testid="stCheckbox"]:has(input:checked) {
    border-color: #4CAF50 !important;
    background: #e8f5e9 !important;
    box-shadow: 0 0 0 2px #4CAF50, 0 2px 8px rgba(76,175,80,0.25);
}

/* ── Checkbox native görünümünü gizle ── */
div[data-testid="stForm"] div[data-testid="stCheckbox"] > label > div[data-testid="stMarkdownContainer"] {
    display: block !important;
}
div[data-testid="stForm"] div[data-testid="stCheckbox"] > label > div:first-child {
    position: absolute;
    opacity: 0;
    width: 0;
    height: 0;
    overflow: hidden;
}

/* ── Seçim sayacı ── */
.d2-counter {
    text-align:center; margin: 4px 0;
    font-size:0.85rem; color:#555;
}
.d2-counter b { color:#1B2A4A; }

/* ── Legend ── */
.d2-legend {
    background:#f0f7ff; border:1px solid #b0d4f1; border-radius:10px;
    padding:8px 12px; margin-bottom:10px; text-align:center;
    font-size:0.85rem; color:#1B2A4A;
}
.d2-legend b { color:#0d47a1; }
</style>
"""


def render_symbol_label(symbol):
    """
    Bir D2 sembolünü checkbox label'ı olarak render eder.
    Tıklanabilir kart içeriği.
    """
    above = symbol["above"]
    below = symbol["below"]
    letter = symbol["letter"]
    idx = symbol.get("index", 0) + 1

    def marks(count):
        if count == 0:
            return '<div style="height:14px;">&nbsp;</div>'
        bars = "".join(
            '<span style="display:inline-block;width:3px;height:12px;'
            'background:#444;border-radius:1px;margin:0 2px;"></span>'
            for _ in range(count)
        )
        return (
            f'<div style="height:14px;display:flex;'
            f'justify-content:center;align-items:center;">{bars}</div>'
        )

    return (
        f'<div style="text-align:center;min-width:36px;padding:2px 0;">'
        f'<div style="font-size:9px;color:#aaa;margin-bottom:1px;">{idx}</div>'
        f'{marks(above)}'
        f'<div style="font-size:24px;font-weight:800;color:#1B2A4A;line-height:28px;">{letter}</div>'
        f'{marks(below)}'
        f'</div>'
    )
