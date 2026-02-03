# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 21:04:35 2026

@author: YYYNÇİGGGİİÜÜÜÜĞĞĞ
"""

import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import random
import time
from db_utils import check_daily_limit, check_test_completed, save_test_result_to_db

# --- API VE AYARLAR ---
load_dotenv()
if "GROK_API_KEY" in st.secrets:
    GROK_API_KEY = st.secrets["GROK_API_KEY"]
else:
    GROK_API_KEY = os.getenv("GROK_API_KEY")

client = OpenAI(api_key=GROK_API_KEY, base_url="https://api.x.ai/v1")

# --- SABİT VERİLER ---
BURDON_SURELERI = {
    "7-8 Yaş (10 Dakika)": 600, "9-10 Yaş (8 Dakika)": 480,
    "11-12 Yaş (6 Dakika)": 360, "13-14 Yaş (4 Dakika)": 240,
    "15-16 Yaş (3 Dakika)": 180, "17+ / Yetişkin (2.5 Dakika)": 150
}

TEST_BILGILERI = {
    "Enneagram Kişilik Testi": {"amac": "Temel kişilik tipinizi belirler.", "nasil": "İfadelerin size ne kadar uyduğunu işaretleyin.", "ipucu": "Dürüst olun."},
    "d2 Dikkat Testi": {
        "amac": "Seçici dikkatinizi ölçer.", 
        "nasil": 'Toplam 14 satır vardır. Her satır için 20 saniyeniz var. Üzerinde toplam 2 çizgi olan d " harflerini bulun.', 
        "ipucu": 'Hızlanın! Süre dolunca otomatik diğer satıra geçilir. Geri dönülemez. p " harflerini atlayın.'
    },
    "Burdon Dikkat Testi": {"amac": "Uzun süreli dikkatinizi ölçer.", "nasil": "a, b, c, d, g harflerini işaretleyin.", "ipucu": "Süre bitmeden tamamlayın."},
    "Genel": {"amac": "Kişisel analiz.", "nasil": "Size en uygun seçeneği işaretleyin.", "ipucu": "Dürüst olun."}
}

TESTLER = [
    "Enneagram Kişilik Testi", "d2 Dikkat Testi", "Burdon Dikkat Testi",
    "Çoklu Zeka Testi (Gardner)", "Holland Mesleki İlgi Envanteri (RIASEC)",
    "VARK Öğrenme Stilleri Testi", "Sağ-Sol Beyin Dominansı Testi",
    "Çalışma Davranışı Ölçeği (Baltaş)", "Sınav Kaygısı Ölçeği (DuSKÖ)"
]

# --- PROMPTLAR ---
SORU_URETIM_PROMPT = """
Sen dünyanın en iyi Türk psikometrik test tasarımcısı ve çocuk/ergen psikolojisi uzmanısın.
GÖREV: Sadece belirtilen test için, orijinal testin soru sayısına ve yapısına TAM SADIK kalarak, tamamen yeni ve benzersiz sorular üret.
- Tüm sorular doğal, akıcı ve düzgün Türkçe olsun. ASLA devrik cümle kullanma.
- Her soru tek bir kısa, net ve sade cümle olsun.
- Sorular ortaokul ve lise öğrencisinin rahatça anlayabileceği kadar açık ve basit olsun.
- Hiçbir şekilde yönlendirme, manipülasyon, yargı, parantez içi açıklama, örnek veya ek bilgi ekleme.
- Sorular tamamen tarafsız ve objektif olsun, hiçbir duygu veya değer yargısı yükleme.
- Sorular psikolojik olarak derin ve kaliteli olsun; üst seviye analizlere olanak tanısın ama anlaşılırlığı asla feda etme.
- Tüm sorular 5'li Likert ölçeğine (Kesinlikle Katılmıyorum - Katılmıyorum - Kararsızım - Katılıyorum - Kesinlikle Katılıyorum) mükemmel uyumlu olsun.
- Aynı veya çok benzer ifadeler ASLA tekrarlanmasın.
- Çıktı SADECE ve SADECE geçerli JSON formatında olsun. Başka hiçbir metin, açıklama veya markdown yazma.

Testlere özgü zorunlu kurallar:
- Enneagram Kişilik Testi: Tam 144 soru üret. 9 tip için eşit dağılım (her tip tam 16 soru). RHETI tarzı kişisel ifadeler kullan ("Ben ...", "Benim için ... önemlidir" vb.).
- Çoklu Zeka Testi (Gardner): Tam 80 soru üret. 8 zeka alanı için tam 10'ar soru: Sözel, Mantıksal, Görsel, Müziksel, Bedensel, Sosyal, İçsel, Doğacı.
- Holland Mesleki İlgi Envanteri (RIASEC): Tam 90 soru üret. 6 tip için tam 15'er soru: Gerçekçi, Araştırmacı, Yaratıcı, Sosyal, Girişimci, Düzenli. Aktivite ve ilgi odaklı olsun.
- VARK Öğrenme Stilleri Testi: Tam 16 soru üret. Orijinal VARK senaryo tarzında günlük hayat durumları üzerinden tercih soruları.
- Sağ-Sol Beyin Dominansı Testi: Tam 30 soru üret. 15 sol beyin + 15 sağ beyin özelliği.
- Çalışma Davranışı Ölçeği (Baltaş): Tam 73 soru üret. Çalışma alışkanlıkları, motivasyon ve disiplin odaklı.
- Sınav Kaygısı Ölçeği (DuSKÖ): Tam 50 soru üret. Sınav kaygısı belirtileri odaklı.

JSON formatı kesin olarak şöyle olsun:
{{
  "type": "likert",
  "questions": [
    {{"id": 1, "text": "Soru metni burada"}},
    ...
  ]
}}
Enneagram için ekstra: {{"id": 1, "text": "...", "type": 1}} (type 1-9 integer)
Gardner için ekstra: {{"id": 1, "text": "...", "area": "Sözel"}}
Holland için ekstra: {{"id": 1, "text": "...", "area": "Gerçekçi"}}

Sadece istenen test için soru üret. Çıktıya kesinlikle başka hiçbir şey yazma.
Test adı: {test_adi}
"""

TEK_RAPOR_PROMPT = """
Sen dünyanın en iyi psikometrik test analizi uzmanısın.
GÖREV: Sadece verilen JSON verilerine dayanarak, test sonuçlarını nesnel ve veri odaklı şekilde analiz et.
Asla genel geçer bilgi verme, sadece kullanıcının puanları ve cevapları üzerinden yorum yap.
Rapor tamamen tarafsız olsun.

Test: {test_adi}
Veriler: {cevaplar_json}

Rapor Formatı (Tam olarak bu başlıkları kullan):
1. **Genel Değerlendirme:** Test sonuçlarının genel özeti.
2. **Puan Analizi:** Her alan/tip için alınan puanlar ve bu puanların anlamı (sayısal verilere dayanarak).
3. **Güçlü Yönler:** Yüksek puan alınan alanlardaki özellikler ve sonuçları.
4. **Gelişim Alanları:** Düşük puan alınan alanlardaki özellikler ve sonuçları.
5. **Öneriler:** Veri odaklı, uygulanabilir 4-5 somut tavsiye.

Dil: Sade, yalın ve profesyonel Türkçe. Tarafsız ve nesnel bir üslup kullan.
"""

# --- YARDIMCI FONKSİYONLAR ---
def get_data_from_ai(prompt):
    if not GROK_API_KEY:
        return "Hata: API Key bulunamadı."
    try:
        response = client.chat.completions.create(
            model="grok-beta",
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

def score_enneagram(answers, questions):
    scores = {i: 0 for i in range(1, 10)}
    for q in questions:
        q_id = q["id"]
        score = answers.get(q_id)
        if score and "type" in q:
            scores[q["type"]] += score
    return scores

# --- CALLBACK FONKSİYONLARI ---
def toggle_burdon_selection(item_id, current_chunk):
    if current_chunk not in st.session_state.burdon_isaretlenen:
        st.session_state.burdon_isaretlenen[current_chunk] = set()
    if item_id in st.session_state.burdon_isaretlenen[current_chunk]:
        st.session_state.burdon_isaretlenen[current_chunk].remove(item_id)
    else:
        st.session_state.burdon_isaretlenen[current_chunk].add(item_id)

def toggle_d2_selection(item_id):
    if item_id in st.session_state.d2_isaretlenen:
        st.session_state.d2_isaretlenen.remove(item_id)
    else:
        st.session_state.d2_isaretlenen.add(item_id)

# --- ANA ÖĞRENCİ UYGULAMASI (APP) ---
def app():
    # CSS
    st.markdown("""
    <style>
        .stButton > button { width: 100%; border-radius: 10px; height: 50px; font-weight: 600; }
        [data-testid="column"] div.stButton > button { height: 60px; font-size: 22px; margin: 1px; }
    </style>
    """, unsafe_allow_html=True)

    # Session State
    if "page" not in st.session_state: st.session_state.page = "home"
    if "intro_passed" not in st.session_state: st.session_state.intro_passed = False

    # 1. LIMIT KONTROLÜ
    if not check_daily_limit(st.session_state.student_id):
        st.error("⚠️ Günlük test çözme limitinize ulaştınız. Yarın tekrar bekleriz.")
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
                
                with st.spinner("Test hazırlanıyor..."):
                    if "d2" in selected_test.lower():
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
                        prompt = SORU_URETIM_PROMPT.format(test_adi=selected_test)
                        raw = get_data_from_ai(prompt)
                        try:
                            test_data = json.loads(raw)
                            test_data["type"] = "enneagram" if "Enneagram" in selected_test else "likert"
                            st.session_state.current_test_data = test_data
                            st.session_state.cevaplar = {}
                            st.session_state.sayfa = 0
                        except:
                            st.error("Test üretilirken hata oluştu. Lütfen tekrar deneyin.")
                            return
                
                st.session_state.page = "test"
                st.rerun()

    # 3. SAYFA: TEST EKRANI
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
            questions = data.get("questions", [])

            # --- TİP 1: LIKERT / ENNEAGRAM ---
            if q_type in ["enneagram", "likert"]:
                PER_PAGE = 10
                total = (len(questions) // PER_PAGE) + (1 if len(questions) % PER_PAGE else 0)
                start = st.session_state.sayfa * PER_PAGE
                current_qs = questions[start:start + PER_PAGE]
                
                st.progress((st.session_state.sayfa + 1) / total)
                
                options_map = {"Kesinlikle Katılmıyorum": 1, "Katılmıyorum": 2, "Kararsızım": 3, "Katılıyorum": 4, "Kesinlikle Katılıyorum": 5}
                opts = list(options_map.keys())
                options_reverse = {v: k for k, v in options_map.items()}

                for q in current_qs:
                    st.write(f"**{q['text']}**")
                    saved = st.session_state.cevaplar.get(q['id'])
                    def_idx = opts.index(options_reverse[saved]) if saved in options_reverse else None
                    val = st.radio("Seçim:", opts, key=f"q_{q['id']}", index=def_idx, horizontal=True, label_visibility="collapsed")
                    if val: st.session_state.cevaplar[q['id']] = options_map[val]
                    st.divider()

                c1, c2 = st.columns(2)
                if st.session_state.sayfa > 0:
                    if c1.button("⬅️ Geri"):
                        st.session_state.sayfa -= 1
                        st.rerun()
                
                if st.session_state.sayfa < total - 1:
                    if c2.button("İleri ➡️"):
                        st.session_state.sayfa += 1
                        st.rerun()
                else:
                    if c2.button("TESTİ BİTİR VE GÖNDER ✅", type="primary"):
                        if len(st.session_state.cevaplar) < len(questions):
                            st.warning("Lütfen tüm soruları cevaplayınız!")
                        else:
                            with st.spinner("Sonuçlar hesaplanıyor ve öğretmene iletiliyor..."):
                                scores = None
                                if q_type == "enneagram":
                                    scores = score_enneagram(st.session_state.cevaplar, questions)
                                    stats = {"Puanlar": scores}
                                else:
                                    stats = {"Cevaplar": st.session_state.cevaplar}
                                
                                prompt = TEK_RAPOR_PROMPT.format(test_adi=test_name, cevaplar_json=json.dumps(stats, ensure_ascii=False))
                                report = get_data_from_ai(prompt)

                                success = save_test_result_to_db(
                                    st.session_state.student_id,
                                    test_name,
                                    st.session_state.cevaplar,
                                    scores,
                                    report
                                )

                                if success:
                                    st.success("Test başarıyla tamamlandı. Sonuçlarınız öğretmeninize iletildi.")
                                    st.session_state.page = "home"
                                    time.sleep(3)
                                    st.rerun()
                                else:
                                    st.error("Kayıt sırasında hata oluştu.")

            # --- TİP 2: d2 DİKKAT TESTİ ---
            elif q_type == "d2":
                ROW_TIME_LIMIT = 20
                TOTAL_ROWS = 14
                
                @st.fragment(run_every=1)
                def d2_row_timer():
                    if st.session_state.get("d2_basla", False) and not st.session_state.get("d2_bitti", False):
                        elapsed = time.time() - st.session_state.d2_row_start_time
                        remaining = ROW_TIME_LIMIT - elapsed
                        if remaining <= 0:
                            st.session_state.d2_current_row += 1
                            if st.session_state.d2_current_row >= TOTAL_ROWS:
                                st.session_state.d2_bitti = True
                            else:
                                st.session_state.d2_row_start_time = time.time()
                            st.rerun()
                        st.progress(max(0.0, remaining / ROW_TIME_LIMIT))
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
                        st.success("Test Tamamlandı.")
                        st.session_state.page = "home"
                        time.sleep(3)
                        st.rerun()
                else:
                    d2_row_timer()
                    curr_r = st.session_state.d2_current_row
                    start_idx = curr_r * 47
                    current_items = questions[start_idx:start_idx + 47]
                    d2_grid_view(current_items)

            # --- TİP 3: BURDON TESTİ ---
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

                @st.fragment
                def burdon_grid(seg):
                    if st.session_state.get("test_bitti", False): return
                    st.info(f"HEDEFLER: {', '.join(st.session_state.burdon_targets)}")
                    rows = [seg[i:i+10] for i in range(0, len(seg), 10)]
                    curr = st.session_state.current_chunk
                    sel = st.session_state.burdon_isaretlenen.get(curr, set())
                    for row in rows:
                        cols = st.columns(len(row))
                        for c, item in enumerate(row):
                            is_sel = item['id'] in sel
                            cols[c].button(item['char'], key=f"b_{item['id']}", type="primary" if is_sel else "secondary", on_click=toggle_burdon_selection, args=(item['id'], curr))

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
                        st.success("Test Tamamlandı.")
                        st.session_state.page = "home"
                        time.sleep(3)
                        st.rerun()
                else:
                    start = st.session_state.current_chunk * CHUNK_SIZE
                    burdon_grid(questions[start:start + CHUNK_SIZE])
                    
                    c1, c2 = st.columns([1, 4])
                    if st.session_state.current_chunk < total - 1:
                        if c2.button("SONRAKİ ➡️"):
                            st.session_state.current_chunk += 1
                            st.rerun()
                    else:
                        if c2.button("BİTİR 🏁", type="primary"):
                            st.session_state.test_bitti = True
                            st.rerun()