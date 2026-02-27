import streamlit as st
import streamlit.components.v1 as components
import json
import time
import random
from db_utils import check_test_completed, save_test_result_to_db
from d2_engine import (
    D2_CONFIG, generate_d2_test, generate_practice_row,
    render_symbol_html, render_row_legend_html, render_timer_js,
    calculate_d2, generate_d2_report,
    get_time_per_row, D2_CARD_CSS, render_symbol_label,
)
from akademik_engine import (
    get_akademik_sections, get_total_questions,
    calculate_akademik, generate_akademik_report,
)

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
    # Enneagram
    ENNEAGRAM_QUESTIONS, ENNEAGRAM_DATA, WING_DESCRIPTIONS,
    calculate_enneagram_report,
)



# ============================================================
# TEST META BİLGİLERİ (YENİ — Süre + Açıklama + İkon)
# ============================================================
TEST_META = {
    "Enneagram Kişilik Testi": {
        "icon": "🧬",
        "color": "#8E44AD",
        "duration": "~25 dk",
        "questions": 180,
        "desc": "9 kişilik tipinden hangisine en yakınsın? Güçlü yönlerini, korkularını ve büyüme yolunu keşfet.",
    },
    "Çalışma Davranışı Ölçeği": {
        "icon": "📚",
        "color": "#2E86C1",
        "duration": "~15 dk",
        "questions": 73,
        "desc": "Ders çalışma alışkanlıklarını ve akademik davranış kalıplarını analiz et.",
    },
    "Sağ-Sol Beyin Dominansı Testi": {
        "icon": "🧠",
        "color": "#E74C3C",
        "duration": "~7 dk",
        "questions": 30,
        "desc": "Beyinin hangi yarısı daha baskın? Yaratıcı mı, analitik mi, yoksa dengeli misin?",
    },
    "Sınav Kaygısı Ölçeği": {
        "icon": "😰",
        "color": "#F39C12",
        "duration": "~10 dk",
        "questions": 50,
        "desc": "Sınav kaygın hangi boyutlarda seni etkiliyor? Fiziksel, zihinsel, duygusal...",
    },
    "VARK Öğrenme Stilleri Testi": {
        "icon": "👁️",
        "color": "#27AE60",
        "duration": "~8 dk",
        "questions": 16,
        "desc": "En iyi nasıl öğreniyorsun? Görsel, İşitsel, Okuma/Yazma, Kinestetik...",
    },
    "Çoklu Zeka Testi": {
        "icon": "💡",
        "color": "#3498DB",
        "duration": "~12 dk",
        "questions": 80,
        "desc": "Howard Gardner'ın 8 zeka alanından hangilerinde güçlüsün?",
    },
    "Holland Mesleki İlgi Envanteri": {
        "icon": "🧭",
        "color": "#1ABC9C",
        "duration": "~15 dk",
        "questions": 84,
        "desc": "Hangi meslek alanları sana en uygun? RIASEC koduyla kariyer haritanı çıkar.",
    },
    "D2 Dikkat Testi": {
        "icon": "🎯",
        "color": "#E74C3C",
        "duration": "~5 dk",
        "questions": 280,
        "desc": "Dikkat ve konsantrasyon kapasiteni ölç. Zamanlı performans testi.",
    },
    "Akademik Analiz Testi": {
        "icon": "📚",
        "color": "#9B59B6",
        "duration": "~25 dk",
        "questions": 67,
        "desc": "Okuma anlama, matematik, mantık ve akademik öz-değerlendirme ile akademik profilini çıkar.",
    },
}


# ============================================================
# 🏠 ANA APP FONKSİYONU
# ============================================================
def app():
    # --- GENEL CSS ---
    st.markdown("""
    <style>
        /* ===== ÖĞRENCİ GÖRÜNÜM CSS ===== */
        .main-header {
            text-align: center;
            font-weight: 900;
            font-size: 2.2rem;
            margin-bottom: 5px;
            color: #1B2A4A;
            letter-spacing: 1px;
        }
        .sub-header {
            text-align: center;
            margin-bottom: 25px;
            font-size: 1rem;
            color: #555;
        }
        
        /* ===== TEST KART TASARIMI ===== */
        .test-card {
            background: #ffffff;
            border: 1px solid #E0E4EA;
            border-radius: 16px;
            padding: 24px 20px;
            margin-bottom: 16px;
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .test-card::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: var(--card-color, #2E86C1);
        }
        .test-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            border-color: var(--card-color, #2E86C1);
        }
        .test-card-icon {
            font-size: 2.5rem;
            margin-bottom: 8px;
        }
        .test-card-title {
            font-weight: 700;
            font-size: 1rem;
            color: #1B2A4A;
            margin-bottom: 6px;
        }
        .test-card-desc {
            font-size: 0.82rem;
            color: #777;
            margin-bottom: 10px;
            line-height: 1.4;
        }
        .test-card-meta {
            display: flex;
            justify-content: center;
            gap: 15px;
            font-size: 0.75rem;
            color: #999;
        }
        
        /* ===== DURUM BADGELERİ ===== */
        .badge-done {
            background: linear-gradient(135deg, #d4edda, #c3e6cb);
            color: #155724;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            display: inline-block;
            margin-top: 8px;
        }
        .badge-ready {
            background: linear-gradient(135deg, #d1ecf1, #bee5eb);
            color: #0c5460;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            display: inline-block;
            margin-top: 8px;
        }
        
        /* ===== İSTATİSTİK KUTUSU ===== */
        .stat-box {
            background: #ffffff;
            border: 1px solid #E0E4EA;
            border-radius: 14px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }
        .stat-number {
            font-size: 2rem;
            font-weight: 800;
            color: #1B2A4A;
        }
        .stat-label {
            font-size: 0.8rem;
            color: #999;
            margin-top: 4px;
        }
        
        /* ===== İLERLEME ÇUBUĞU ===== */
        .progress-container {
            background: #E8EDF3;
            border-radius: 10px;
            height: 10px;
            overflow: hidden;
            margin: 10px 0;
        }
        .progress-bar {
            height: 100%;
            border-radius: 10px;
            background: linear-gradient(90deg, #1B2A4A, #2E86C1);
            transition: width 0.5s ease;
        }
        
        /* ===== MOTİVASYON MESAJLARI ===== */
        .motivation-box {
            background: linear-gradient(135deg, #1B2A4A 0%, #2C3E6B 100%);
            color: white;
            border-radius: 16px;
            padding: 25px;
            text-align: center;
            margin: 20px 0;
        }
        .motivation-box h3 {
            color: #FFFFFF;
            margin-bottom: 8px;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- BAŞLIK ---
    st.markdown("<h1 class='main-header'>🎓 EĞİTİM CHECK UP</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>Hoşgeldin <b>{st.session_state.student_name}</b> — Kendini keşfetmeye hazır mısın?</div>", unsafe_allow_html=True)

    # --- SAYFA GEÇİŞİNDE OTOMATİK SCROLL TO TOP ---
    if st.session_state.get("_scroll_top"):
        components.html(
            """<script>
                window.parent.document.querySelector('section.main').scrollTo({top: 0, behavior: 'instant'});
            </script>""",
            height=0
        )
        st.session_state._scroll_top = False

    if "page" not in st.session_state:
        st.session_state.page = "home"

    ALL_TESTS = [
        "Enneagram Kişilik Testi",
        "Çalışma Davranışı Ölçeği",
        "Sağ-Sol Beyin Dominansı Testi",
        "Sınav Kaygısı Ölçeği",
        "VARK Öğrenme Stilleri Testi",
        "Çoklu Zeka Testi",
        "Holland Mesleki İlgi Envanteri",
        "D2 Dikkat Testi",
        "Akademik Analiz Testi",
    ]

    # ============================================================
    # SAYFA 1: ANA MENÜ (HOME)
    # ============================================================
    if st.session_state.page == "home":
        
        # --- İSTATİSTİK KUTUSU ---
        completed_count = sum(1 for t in ALL_TESTS if check_test_completed(st.session_state.student_id, t))
        total_count = len(ALL_TESTS)
        pct = round(completed_count / total_count * 100)
        
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-number">{completed_count}/{total_count}</div>
                    <div class="stat-label">Tamamlanan Test</div>
                </div>
            """, unsafe_allow_html=True)
        with sc2:
            st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-number">%{pct}</div>
                    <div class="stat-label">İlerleme Oranı</div>
                </div>
            """, unsafe_allow_html=True)
        with sc3:
            remaining = total_count - completed_count
            st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-number">{remaining}</div>
                    <div class="stat-label">Kalan Test</div>
                </div>
            """, unsafe_allow_html=True)
        
        # İlerleme Çubuğu
        st.markdown(f"""
            <div class="progress-container">
                <div class="progress-bar" style="width: {pct}%;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        # Tüm testler tamamlandıysa kutlama mesajı
        if completed_count == total_count:
            st.markdown("""
                <div class="motivation-box">
                    <h3>🎉 Tebrikler! Tüm Testleri Tamamladın!</h3>
                    <p>Harika bir iş çıkardın. Öğretmenin artık sana özel bir analiz raporu hazırlayabilir.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Motivasyon mesajları
            motivations = [
                "Her test, kendini daha iyi tanımana bir adım daha yaklaştırıyor. 🌟",
                "Doğru veya yanlış cevap yok — sadece SEN varsın! 💪",
                "Kendini keşfetmek, geleceğine yatırım yapmaktır. 🚀",
                "Her cevabın, sana özel bir yol haritası çiziyor. 🗺️",
            ]
            st.info(f"💡 {random.choice(motivations)}")
        
        st.markdown("---")
        
        # --- TEST KARTLARI ---
        col1, col2 = st.columns(2)
        
        for idx, test in enumerate(ALL_TESTS):
            is_done = check_test_completed(st.session_state.student_id, test)
            target_col = col1 if idx % 2 == 0 else col2
            meta = TEST_META.get(test, {})
            
            with target_col:
                if is_done:
                    st.markdown(f"""
                        <div class="test-card" style="--card-color: #27AE60; opacity: 0.85;">
                            <div class="test-card-icon">{meta.get('icon', '📝')}</div>
                            <div class="test-card-title">{test}</div>
                            <div class="test-card-desc">{meta.get('desc', '')}</div>
                            <span class="badge-done">✅ Tamamlandı</span>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="test-card" style="--card-color: {meta.get('color', '#2E86C1')};">
                            <div class="test-card-icon">{meta.get('icon', '📝')}</div>
                            <div class="test-card-title">{test}</div>
                            <div class="test-card-desc">{meta.get('desc', '')}</div>
                            <div class="test-card-meta">
                                <span>⏱️ {meta.get('duration', '~10 dk')}</span>
                                <span>📝 {meta.get('questions', '?')} soru</span>
                            </div>
                            <span class="badge-ready">🎯 Hazır</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"▶️ {test} Başla", key=test, type="primary"):
                        st.session_state.selected_test = test
                        st.session_state.intro_passed = False

                        if "Enneagram" in test:
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
                            student_grade = st.session_state.get('student_grade')
                            student_age = st.session_state.get('student_age', 15)
                            is_ilkogretim = (student_grade and student_grade <= 8) or (not student_grade and student_age and student_age <= 13)
                            if is_ilkogretim:
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
                            st.session_state.current_test_data = {"type": "holland_5", "questions": HOLLAND_QUESTIONS}
                            st.session_state.cevaplar = {}
                            st.session_state.sayfa = 0

                        elif "D2 Dikkat" in test:
                            seed = hash(str(st.session_state.student_id) + str(time.time()))
                            student_age = st.session_state.get("student_age", 15)
                            st.session_state.current_test_data = {"type": "d2_timed"}
                            st.session_state.d2_rows = generate_d2_test(seed=seed)
                            st.session_state.d2_current_row = -1   # -1 = alıştırma
                            st.session_state.d2_row_results = []
                            st.session_state.d2_practice_done = False
                            st.session_state.d2_row_start = None
                            st.session_state.d2_time_per_row = get_time_per_row(student_age)

                        elif "Akademik Analiz" in test:
                            student_grade = st.session_state.get("student_grade")
                            if student_grade:
                                # Grade bilgisi var — doğrudan 4 kademe sistemi
                                st.session_state.current_test_data = {
                                    "type": "akademik_perf",
                                    "grade": student_grade,
                                }
                                st.session_state.akd_version = None
                                st.session_state.akd_grade = student_grade
                            else:
                                # Grade bilgisi yok (eski kayıt) — yaşa göre fallback
                                student_age = st.session_state.get("student_age", 15)
                                version = "ilkogretim" if student_age and student_age <= 13 else "lise"
                                st.session_state.current_test_data = {
                                    "type": "akademik_perf",
                                    "version": version,
                                }
                                st.session_state.akd_version = version
                                st.session_state.akd_grade = None
                            st.session_state.akd_section_idx = 0
                            st.session_state.akd_answers = {}

                        st.session_state.page = "test"
                        st.session_state._scroll_top = True
                        st.rerun()

    # ============================================================
    # SAYFA 2: BAŞARI EKRANI
    # ============================================================
    elif st.session_state.page == "success_screen":
        st.markdown("""
            <div class="motivation-box">
                <h3>🎉 Harika İş Çıkardın!</h3>
                <p>Testi başarıyla tamamladın. Sonuçların öğretmenine iletildi.</p>
            </div>
        """, unsafe_allow_html=True)

        if "last_report" in st.session_state and st.session_state.last_report:
            with st.expander("📋 Raporunu Görüntüle", expanded=True):
                st.markdown(st.session_state.last_report)

        st.markdown("---")
        c1, c2 = st.columns(2)
        if c1.button("🏠 Diğer Teste Geç", type="primary"):
            st.session_state.page = "home"
            st.session_state._scroll_top = True
            st.rerun()
        if c2.button("🚪 Çıkış Yap"):
            st.session_state.clear()
            st.session_state._scroll_top = True
            st.rerun()

    # ============================================================
    # SAYFA 3: TEST ÇÖZME EKRANI
    # ============================================================
    elif st.session_state.page == "test":
        t_name = st.session_state.selected_test
        meta = TEST_META.get(t_name, {})

        # --- GİRİŞ EKRANI ---
        if not st.session_state.intro_passed:
            st.markdown(f"### {meta.get('icon', '📝')} {t_name}")
            
            # Test bilgi kartı
            st.markdown(f"""
                <div style="background: #ffffff; border: 1px solid #E0E4EA; border-radius: 16px; padding: 25px; margin: 15px 0;
                            border-top: 4px solid {meta.get('color', '#2E86C1')};">
                    <p style="color: #555; font-size: 1rem; margin-bottom: 15px;">{meta.get('desc', '')}</p>
                    <div style="display: flex; gap: 20px; color: #777; font-size: 0.9rem;">
                        <span>⏱️ Tahmini süre: <b>{meta.get('duration', '~10 dk')}</b></span>
                        <span>📝 <b>{meta.get('questions', '?')}</b> soru</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.info("💡 Doğru veya yanlış cevap yoktur. İçinden geldiği gibi, samimiyetle cevapla.")
            
            c1, c2 = st.columns(2)
            
            if c1.button("⬅️ Vazgeç / Ana Menü"):
                st.session_state.page = "home"
                st.session_state._scroll_top = True
                st.rerun()
                
            if c2.button("HAZIRIM, BAŞLA! 🚀", type="primary"):
                st.session_state.intro_passed = True
                st.session_state._scroll_top = True
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
                total_qs  = len(all_qs)
                curr_page = st.session_state.enneagram_page
                total_pages = (total_qs + PER_PAGE - 1) // PER_PAGE

                page_qs  = all_qs[curr_page * PER_PAGE : (curr_page + 1) * PER_PAGE]
                answered = sum(1 for q in all_qs
                               if st.session_state.enneagram_answers.get(q["key"]) is not None)

                st.progress(answered / total_qs)
                st.caption(f"📖 Bölüm {curr_page + 1} / {total_pages}  •  "
                           f"✍️ {answered}/{total_qs} soru cevaplandı")
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
                        st.session_state._scroll_top = True
                        st.rerun()

                is_last = curr_page == total_pages - 1
                if not is_last:
                    if c2.button("Sonraki Bölüm ➡️"):
                        if not all_answered:
                            st.error("⚠️ Lütfen bu bölümdeki tüm soruları cevapla.")
                        else:
                            st.session_state.enneagram_page += 1
                            st.session_state._scroll_top = True
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
                            with st.spinner("🧬 Kişilik haritan çıkarılıyor..."):
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
                                st.session_state._scroll_top = True
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
                st.caption(f"📖 Sayfa {st.session_state.sayfa + 1} / {tot_p}")
                page_q_ids = []

                for q in curr_qs:
                    qid = q["id"]
                    page_q_ids.append(qid)
                    st.write(f"**{qid}. {q['text']}**")
                    prev = st.session_state.cevaplar.get(qid)
                    options = [f"a) {q['a']}", f"b) {q['b']}"]
                    idx = 0 if prev == "a" else (1 if prev == "b" else None)
                    val = st.radio(f"Soru {qid}", options, key=f"q_{qid}", index=idx, horizontal=True, label_visibility="collapsed")
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
                st.caption(f"📖 Sayfa {st.session_state.sayfa + 1} / {tot_p}")
                page_q_ids = []

                for q in curr_qs:
                    qid = q["id"]
                    page_q_ids.append(qid)
                    st.write(f"**{qid}. {q['text']}**")
                    prev = st.session_state.cevaplar.get(qid)
                    options = ["Doğru", "Yanlış"]
                    idx = 0 if prev == "D" else (1 if prev == "Y" else None)
                    val = st.radio(f"Soru {qid}", options, key=f"q_{qid}", index=idx, horizontal=True, label_visibility="collapsed")
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
                st.caption(f"📖 Sayfa {st.session_state.sayfa + 1} / {tot_p}")
                page_q_ids = []

                likert_labels = {0: "0 - Asla", 1: "1 - Çok Az", 2: "2 - Bazen", 3: "3 - Çoğu Kez", 4: "4 - Daima"}
                likert_opts = [0, 1, 2, 3, 4]

                for q in curr_qs:
                    qid = q["id"]
                    page_q_ids.append(qid)
                    st.write(f"**{qid}. {q['text']}**")
                    prev = st.session_state.cevaplar.get(qid)
                    idx = likert_opts.index(prev) if prev is not None else None
                    val = st.radio(f"Soru {qid}", likert_opts, key=f"q_{qid}", index=idx, horizontal=True, format_func=lambda x: likert_labels[x], label_visibility="collapsed")
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
                st.caption(f"📖 Sayfa {st.session_state.sayfa + 1} / {tot_p}")
                page_q_ids = []

                for q in curr_qs:
                    qid = q["id"]
                    page_q_ids.append(qid)
                    st.write(f"**{qid}. {q['text']}**")
                    prev = st.session_state.cevaplar.get(qid)
                    options = ["Evet", "Hayır"]
                    idx = 0 if prev == "E" else (1 if prev == "H" else None)
                    val = st.radio(f"Soru {qid}", options, key=f"q_{qid}", index=idx, horizontal=True, label_visibility="collapsed")
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
                st.caption(f"📖 Sayfa {st.session_state.sayfa + 1} / {tot_p}  •  💡 Her soruda birden fazla seçenek işaretleyebilirsin.")
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
            # TİP: HOLLAND (5'li Likert)
            # ========================================
            elif q_type == "holland_5":
                qs = data["questions"]
                PER_PAGE = 10
                tot_p = (len(qs) + PER_PAGE - 1) // PER_PAGE
                start = st.session_state.sayfa * PER_PAGE
                curr_qs = qs[start:start + PER_PAGE]

                st.progress((st.session_state.sayfa + 1) / tot_p)
                st.caption(f"📖 Sayfa {st.session_state.sayfa + 1} / {tot_p}")
                page_q_ids = []

                holland_opts = [0, 1, 2, 3, 4]
                holland_labels = {
                    0: "😣 Hiç Hoşlanmam",
                    1: "😕 Hoşlanmam",
                    2: "😐 Kararsızım",
                    3: "😊 Hoşlanırım",
                    4: "😍 Çok Hoşlanırım"
                }

                for q in curr_qs:
                    qid = q["id"]
                    page_q_ids.append(qid)
                    st.write(f"**{qid}. {q['text']}**")
                    prev = st.session_state.cevaplar.get(qid)
                    idx = holland_opts.index(prev) if prev is not None else None
                    val = st.radio(
                        f"Soru {qid}", holland_opts, key=f"q_{qid}",
                        index=idx, horizontal=True,
                        format_func=lambda x: holland_labels[x],
                        label_visibility="collapsed"
                    )
                    if val is not None:
                        st.session_state.cevaplar[qid] = val
                    st.divider()

                _navigate_pages(qs, page_q_ids, PER_PAGE, tot_p, t_name, q_type)

            # ========================================
            # TİP: D2 DİKKAT TESTİ (Tıklanabilir Kart)
            # ========================================
            elif q_type == "d2_timed":
                current_row = st.session_state.d2_current_row
                time_per_row = st.session_state.get("d2_time_per_row", D2_CONFIG["time_per_row"])

                # Kart CSS'ini enjekte et
                st.markdown(D2_CARD_CSS, unsafe_allow_html=True)

                # ---- ALIŞTIRMA TURU ----
                if current_row == -1 and not st.session_state.d2_practice_done:
                    st.markdown("### 🎯 Alıştırma Turu")
                    st.info(
                        f"Aşağıdaki sembollere **tıklayarak** hedefleri işaretle. "
                        f"Ana testte her satır için **{time_per_row} saniye** süren olacak. "
                        f"Bu tur puanlanmaz."
                    )
                    st.markdown(
                        '<div class="d2-legend">🎯 Hedef: <b>d</b> harfi + toplam <b>2 çizgi</b> '
                        '(üstte ve/veya altta) → tıkla!</div>',
                        unsafe_allow_html=True,
                    )

                    practice = generate_practice_row()

                    with st.form("d2_practice"):
                        D2_COLS = 5
                        for sub_r in range((len(practice) + D2_COLS - 1) // D2_COLS):
                            cols = st.columns(D2_COLS)
                            for c in range(D2_COLS):
                                idx = sub_r * D2_COLS + c
                                if idx < len(practice):
                                    with cols[c]:
                                        st.markdown(
                                            render_symbol_html(practice[idx]),
                                            unsafe_allow_html=True,
                                        )
                                        st.checkbox(
                                            "✓ Seç", key=f"d2p_{idx}",
                                        )

                        if st.form_submit_button("Alıştırmayı Tamamla ✅", type="primary"):
                            st.session_state.d2_practice_done = True
                            st.session_state.d2_current_row = 0
                            st.session_state.d2_row_start = time.time()
                            st.session_state._scroll_top = True
                            st.rerun()

                # ---- ANA TEST SATIRLARI ----
                elif 0 <= current_row < D2_CONFIG["rows"]:
                    row_symbols = st.session_state.d2_rows[current_row]

                    st.markdown(
                        f"### 🎯 Satır {current_row + 1} / {D2_CONFIG['rows']}"
                    )
                    st.progress((current_row + 1) / D2_CONFIG["rows"])

                    if st.session_state.d2_row_start is None:
                        st.session_state.d2_row_start = time.time()

                    components.html(
                        render_timer_js(time_per_row, current_row),
                        height=55,
                    )

                    st.markdown(
                        '<div class="d2-legend">🎯 Hedef: <b>d</b> harfi + toplam <b>2 çizgi</b> '
                        '(üstte ve/veya altta) → tıkla!</div>',
                        unsafe_allow_html=True,
                    )

                    with st.form(f"d2_row_{current_row}"):
                        D2_COLS = 5
                        for sub_r in range(
                            (len(row_symbols) + D2_COLS - 1) // D2_COLS
                        ):
                            cols = st.columns(D2_COLS)
                            for c in range(D2_COLS):
                                idx = sub_r * D2_COLS + c
                                if idx < len(row_symbols):
                                    with cols[c]:
                                        st.markdown(
                                            render_symbol_html(row_symbols[idx]),
                                            unsafe_allow_html=True,
                                        )
                                        st.checkbox(
                                            "✓ Seç",
                                            key=f"d2r{current_row}_s{idx}",
                                        )

                        submitted = st.form_submit_button(
                            "Satırı Gönder ➡️", type="primary"
                        )

                    if submitted:
                        elapsed = time.time() - (
                            st.session_state.d2_row_start or time.time()
                        )
                        selected = [
                            st.session_state.get(
                                f"d2r{current_row}_s{i}", False
                            )
                            for i in range(len(row_symbols))
                        ]

                        st.session_state.d2_row_results.append(
                            {
                                "symbols": row_symbols,
                                "selected": selected,
                                "elapsed_time": elapsed,
                            }
                        )

                        next_row = current_row + 1
                        if next_row >= D2_CONFIG["rows"]:
                            _finish_d2_test(t_name)
                        else:
                            st.session_state.d2_current_row = next_row
                            st.session_state.d2_row_start = time.time()
                            st.session_state._scroll_top = True
                            st.rerun()

                    if st.session_state.d2_row_start:
                        if time.time() - st.session_state.d2_row_start > time_per_row:
                            st.warning("⏰ Süre doldu! Lütfen satırı gönderin.")

            # ========================================
            # TİP: AKADEMİK ANALİZ (Bölümlü Performans)
            # ========================================
            elif q_type == "akademik_perf":
                akd_grade = st.session_state.get("akd_grade")
                akd_version = st.session_state.get("akd_version")
                sections = get_akademik_sections(grade=akd_grade, version=akd_version)
                sec_idx = st.session_state.akd_section_idx
                total_secs = len(sections)

                if sec_idx < total_secs:
                    sec = sections[sec_idx]
                    # Kademe etiketi
                    KADEME_LABELS = {5: "5-6. Sınıf", 6: "5-6. Sınıf", 7: "7-8. Sınıf", 8: "7-8. Sınıf",
                                     9: "9-10. Sınıf", 10: "9-10. Sınıf", 11: "11-12. Sınıf", 12: "11-12. Sınıf"}
                    if akd_grade:
                        ver_label = KADEME_LABELS.get(akd_grade, f"{akd_grade}. Sınıf")
                    else:
                        ver_label = "İlköğretim" if akd_version == "ilkogretim" else "Lise"

                    st.markdown(
                        f"### {sec['icon']} Bölüm {sec_idx + 1}/{total_secs}: "
                        f"{sec['name']}"
                    )
                    st.progress((sec_idx + 1) / total_secs)
                    st.caption(f"📎 Versiyon: {ver_label}")

                    with st.form(f"akd_sec_{sec_idx}"):

                        # ---- Okuma Anlama (metin + sorular) ----
                        if sec["type"] == "passage_mc":
                            for p_idx, passage in enumerate(sec["data"]):
                                st.markdown(
                                    f"<div style='background:#f8f9fa;border-left:4px solid "
                                    f"#9B59B6;padding:15px;border-radius:8px;margin:10px 0;'>"
                                    f"<b>📄 Metin {p_idx + 1}</b><br><br>"
                                    f"{passage['passage']}</div>",
                                    unsafe_allow_html=True,
                                )
                                for q in passage["questions"]:
                                    prev = st.session_state.akd_answers.get(q["id"])
                                    opts = list(q["options"].values())
                                    keys = list(q["options"].keys())
                                    idx_prev = (
                                        keys.index(prev) if prev in keys else None
                                    )
                                    val = st.radio(
                                        f"**{q['text']}**",
                                        keys,
                                        index=idx_prev,
                                        format_func=lambda k, o=q["options"]: f"{k}) {o[k]}",
                                        key=f"akd_{q['id']}",
                                    )
                                    if val:
                                        st.session_state.akd_answers[q["id"]] = val
                                    st.divider()

                        # ---- Çoktan Seçmeli (matematik, mantık) ----
                        elif sec["type"] == "mc":
                            for q in sec["data"]:
                                prev = st.session_state.akd_answers.get(q["id"])
                                keys = list(q["options"].keys())
                                idx_prev = (
                                    keys.index(prev) if prev in keys else None
                                )
                                val = st.radio(
                                    f"**{q['text']}**",
                                    keys,
                                    index=idx_prev,
                                    format_func=lambda k, o=q["options"]: f"{k}) {o[k]}",
                                    key=f"akd_{q['id']}",
                                )
                                if val:
                                    st.session_state.akd_answers[q["id"]] = val
                                st.divider()

                        # ---- Likert (öz-değerlendirme) ----
                        elif sec["type"] == "likert":
                            likert_labels = {
                                1: "Hiç Katılmıyorum",
                                2: "Katılmıyorum",
                                3: "Kararsızım",
                                4: "Katılıyorum",
                                5: "Tamamen Katılıyorum",
                            }
                            for q in sec["data"]:
                                prev = st.session_state.akd_answers.get(q["id"])
                                idx_prev = (
                                    prev - 1 if isinstance(prev, int) and 1 <= prev <= 5
                                    else None
                                )
                                val = st.radio(
                                    f"**{q['text']}**",
                                    [1, 2, 3, 4, 5],
                                    index=idx_prev,
                                    format_func=lambda x: f"{x} — {likert_labels[x]}",
                                    key=f"akd_{q['id']}",
                                    horizontal=True,
                                )
                                if val:
                                    st.session_state.akd_answers[q["id"]] = val
                                st.divider()

                        # ---- Navigasyon butonları ----
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if sec_idx > 0:
                                back = st.form_submit_button("⬅️ Önceki Bölüm")
                            else:
                                back = False
                        with col_b:
                            if sec_idx < total_secs - 1:
                                nxt = st.form_submit_button(
                                    "Sonraki Bölüm ➡️", type="primary"
                                )
                            else:
                                nxt = st.form_submit_button(
                                    "Testi Bitir ✅", type="primary"
                                )

                    if back:
                        st.session_state.akd_section_idx = max(0, sec_idx - 1)
                        st.session_state._scroll_top = True
                        st.rerun()
                    if nxt:
                        if sec_idx < total_secs - 1:
                            st.session_state.akd_section_idx = sec_idx + 1
                            st.session_state._scroll_top = True
                            st.rerun()
                        else:
                            _finish_akademik_test(t_name)


# ============================================================
# D2 TEST BİTİRME FONKSİYONU
# ============================================================
def _finish_d2_test(t_name):
    """D2 testini puanla, rapor üret ve veritabanına kaydet."""
    row_results = st.session_state.d2_row_results

    with st.spinner("📊 D2 sonuçların hesaplanıyor..."):
        scores = calculate_d2(row_results)
        report = generate_d2_report(scores)

        scores_for_db = {
            "TN": scores["TN"], "E1": scores["E1"],
            "E2": scores["E2"], "E": scores["E"],
            "TN_E": scores["TN_E"], "CP": scores["CP"],
            "FR": scores["FR"],
            "hit_rate": scores["hit_rate"],
            "error_pct": scores["error_pct"],
            "cp_pct": scores["cp_pct"],
            "level": scores["level"],
            "balance": scores["balance"],
            "consistency": scores["consistency"],
            "row_performances": scores["row_performances"],
            "student_age": st.session_state.get("student_age"),
            "time_per_row": st.session_state.get("d2_time_per_row", D2_CONFIG["time_per_row"]),
        }

        raw_answers = {
            f"row_{i}": {
                "selected": r["selected"],
                "elapsed_time": round(r["elapsed_time"], 2),
            }
            for i, r in enumerate(row_results)
        }

        save_test_result_to_db(
            st.session_state.student_id, t_name,
            raw_answers, scores_for_db, report,
        )

        st.session_state.last_report = report
        st.session_state.page = "success_screen"
        st.session_state._scroll_top = True
        st.rerun()


# ============================================================
# AKADEMİK ANALİZ TEST BİTİRME FONKSİYONU
# ============================================================
def _finish_akademik_test(t_name):
    """Akademik analiz testini puanla, rapor üret ve veritabanına kaydet."""
    answers = st.session_state.akd_answers
    akd_grade = st.session_state.get("akd_grade")
    akd_version = st.session_state.get("akd_version")

    with st.spinner("📊 Akademik analiz sonuçların hesaplanıyor..."):
        scores = calculate_akademik(answers, grade=akd_grade, version=akd_version)
        report = generate_akademik_report(scores)

        scores_for_db = {
            "version": akd_version,
            "grade": akd_grade,
            "overall": scores["overall"],
            "level": scores["level"],
            "performance_avg": scores["performance_avg"],
            "self_assessment": scores["self_assessment"],
            "strongest": scores["strongest"]["name"],
            "weakest": scores["weakest"]["name"],
        }
        for sec_name, sec_data in scores["sections"].items():
            key = sec_name.split(" ")[-1] if " " in sec_name else sec_name
            scores_for_db[key] = sec_data["pct"]

        save_test_result_to_db(
            st.session_state.student_id, t_name,
            answers, scores_for_db, report,
        )

        st.session_state.last_report = report
        st.session_state.page = "success_screen"
        st.session_state._scroll_top = True
        st.rerun()


# ============================================================
# SAYFA NAVİGASYONU + TEST BİTİRME (ORTAK FONKSİYON)
# ============================================================
def _navigate_pages(qs, page_q_ids, PER_PAGE, tot_p, t_name, q_type):
    """İleri/Geri navigasyon ve test bitirme mantığı."""
    c1, c2 = st.columns(2)

    if st.session_state.sayfa > 0:
        if c1.button("⬅️ Geri"):
            st.session_state.sayfa -= 1
            st.session_state._scroll_top = True
            st.rerun()

    if st.session_state.sayfa < tot_p - 1:
        if c2.button("İleri ➡️"):
            missing = _check_missing(page_q_ids, q_type)
            if missing:
                st.error("⚠️ Bu sayfada boş bıraktığın sorular var. Onları doldurmadan geçemezsin.")
            else:
                st.session_state.sayfa += 1
                st.session_state._scroll_top = True
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

    with st.spinner("📊 Sonuçların hesaplanıyor..."):

        if q_type == "ab_choice":
            result, report = calculate_sag_sol_beyin(answers)
            scores = {
                "sag_beyin": result["sag_beyin"], "sol_beyin": result["sol_beyin"],
                "sag_yuzde": result["sag_yuzde"], "sol_yuzde": result["sol_yuzde"],
                "dominant": result["dominant"], "level": result["level"],
            }

        elif q_type == "true_false":
            if "Çalışma Davranışı" in t_name:
                result, report = calculate_calisma_davranisi(answers)
                scores = {"total": result["total"], "max_total": result["max_total"], "categories": result["categories"]}
            elif "Sınav Kaygısı" in t_name:
                result, report = calculate_sinav_kaygisi(answers)
                scores = {"total": result["total"], "total_pct": result["total_pct"], "level": result["overall_level"], "categories": result["categories"]}

        elif q_type == "coklu_zeka_lise":
            result, report = calculate_coklu_zeka_lise(answers)
            scores = {zk: result["scores"][zk]["pct"] for zk in result["scores"]}

        elif q_type == "coklu_zeka_ilk":
            result, report = calculate_coklu_zeka_ilkogretim(answers)
            scores = {zk: result["scores"][zk]["pct"] for zk in result["scores"]}

        elif q_type == "vark_multi":
            result, report = calculate_vark(answers)
            scores = {
                "V": result["counts"]["V"], "A": result["counts"]["A"],
                "R": result["counts"]["R"], "K": result["counts"]["K"],
                "dominant": result["dominant"][0]
            }

        elif q_type == "holland_5":
            result, report = calculate_holland(answers)
            scores = {
                "R": result["R"], "I": result["I"], "A": result["A"],
                "S": result["S"], "E": result["E"], "C": result["C"],
                "holland_code": result["holland_code"],
            }

        save_test_result_to_db(st.session_state.student_id, t_name, answers, scores, report)

        st.session_state.last_report = report
        st.session_state.page = "success_screen"
        st.session_state._scroll_top = True
        st.rerun()
