import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import time
from db_utils import get_all_students_with_results, reset_database, delete_specific_students, save_holistic_analysis, get_student_analysis_history
from openai import OpenAI
import os
from dotenv import load_dotenv

# --- API AYARLARI ---
load_dotenv()
if "GROK_API_KEY" in st.secrets:
    GROK_API_KEY = st.secrets["GROK_API_KEY"]
else:
    GROK_API_KEY = os.getenv("GROK_API_KEY")

client = OpenAI(api_key=GROK_API_KEY, base_url="https://api.x.ai/v1")

# --- YARDIMCI FONKSİYONLAR ---
def get_ai_analysis(prompt):
    if not GROK_API_KEY: return "Hata: API Key bulunamadı."
    try:
        response = client.chat.completions.create(
            model="grok-4-1-fast-reasoning", # En güçlü akıl yürütme modeli
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1 # Yaratıcılık düşük, tutarlılık yüksek
        )
        return response.choices[0].message.content.strip()
    except Exception as e: return f"Analiz Hatası: {e}"

def plot_scores(data_dict, title):
    if not data_dict or not isinstance(data_dict, dict): return None
    labels = [str(k) for k in data_dict.keys()]
    try: values = [float(v) for v in data_dict.values()]
    except: return None 
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=values, y=labels, ax=ax, palette="viridis", orient='h')
    ax.set_title(f"{title} - Puan Dağılımı", fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig

# --- ANA UYGULAMA ---
def app():
    st.markdown("""
    <style>
        .stSelectbox div, .stMultiSelect div, div[data-baseweb="select"] { cursor: pointer !important; }
        .archive-box { background-color: #f8f9fa; border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
        .report-header { color: #155724; background-color: #d4edda; padding: 10px; border-radius: 5px; margin-bottom: 10px; border: 1px solid #c3e6cb; }
        div[role="listbox"] li { cursor: pointer !important; }
    </style>
    """, unsafe_allow_html=True)

    st.title("👨‍🏫 Öğretmen Yönetim Paneli")
    st.markdown("---")

    data = get_all_students_with_results()
    student_names_all = [d["info"].name for d in data] if data else []

    # --- SIDEBAR ---
    with st.sidebar:
        st.header("⚙️ Yönetim")
        with st.expander("🗑️ Öğrenci Sil"):
            if not student_names_all: st.info("Öğrenci yok.")
            else:
                to_del = st.multiselect("Seç:", student_names_all)
                if to_del and st.button("SİL"):
                    delete_specific_students(to_del)
                    st.success("Silindi."); time.sleep(1); st.rerun()
        with st.expander("⚠️ Sıfırla"):
            if st.button("TÜMÜNÜ SIFIRLA"):
                reset_database(); st.success("Sıfırlandı."); time.sleep(1); st.rerun()

    if not data:
        st.info("📂 Henüz kayıtlı veri yok.")
        return

    # 1. ÖĞRENCİ SEÇİMİ
    st.subheader("📂 Öğrenci Dosyası")
    selected_name = st.selectbox("Öğrenci Seçiniz:", student_names_all, index=None, placeholder="Listeden seçin...")
    
    if not selected_name:
        st.info("👆 Analiz için bir öğrenci seçiniz.")
        return

    student_data = next(d for d in data if d["info"].name == selected_name)
    info = student_data["info"]
    tests = student_data["tests"]

    # 2. KİMLİK KARTI
    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Öğrenci", info.name)
        c2.metric("Yaş/Cinsiyet", f"{info.age} / {info.gender}")
        c3.metric("Kullanıcı Adı", info.username)
        c4.metric("Giriş Sayısı", info.login_count)
    st.divider()

    # ============================================================
    # 3. KAYITLI RAPOR ARŞİVİ
    # ============================================================
    st.subheader("📂 Kayıtlı Rapor Arşivi")
    history = get_student_analysis_history(info.id)
    analyzed_combinations = [] 
    
    if not history:
        st.info("Bu öğrenci için henüz oluşturulmuş bütüncül bir analiz raporu yok.")
    else:
        st.markdown(f"Bu öğrenci için **{len(history)} adet** kayıtlı rapor bulundu.")
        for idx, record in enumerate(history):
            analyzed_combinations.append(record['combination'])
            btn_label = f"📄 Rapor {idx+1}: {record['combination']} ({record['date']})"
            with st.expander(btn_label):
                st.markdown(f"<div class='report-header'><b>ANALİZ EDİLEN TESTLER:</b> {record['combination']}</div>", unsafe_allow_html=True)
                st.markdown(record['report'])
                st.download_button(label=f"📥 İndir ({idx+1})", data=record['report'], file_name=f"{info.name}_Rapor_{idx+1}.txt", mime="text/plain", key=f"dl_{idx}")

    st.divider()

    # ============================================================
    # 4. YENİ ANALİZ OLUŞTURMA (SÜPER PROMPT İLE GÜÇLENDİRİLDİ)
    # ============================================================
    st.subheader("⚡ Yeni Analiz Oluştur")
    
    if not tests:
        st.warning("⚠️ Bu öğrenci henüz hiç test çözmemiş.")
    else:
        all_completed_tests = [t["test_name"] for t in tests]
        already_analyzed_singles = [ac for ac in analyzed_combinations if " + " not in ac]
        available_tests = [t for t in all_completed_tests if t not in already_analyzed_singles]
        
        if not available_tests:
            st.success("✅ Tüm testlerin tekil analizleri tamamlanmış.")
            st.info("💡 İpucu: Çoklu analiz (Kombinasyon) yapmak istiyorsanız ama testler burada görünmüyorsa, yukarıdaki arşivden mevcut raporları inceleyebilirsiniz.")
        else:
            st.write("Henüz analiz edilmemiş testler:")
            selected_tests = st.multiselect("Testleri Seç:", options=available_tests, default=available_tests)
            
            if st.button("🧠 YENİ ANALİZ OLUŞTUR VE KAYDET", type="primary"):
                if not selected_tests:
                    st.error("En az bir test seçmelisiniz.")
                else:
                    analyzed_data = [t for t in tests if t["test_name"] in selected_tests]
                    st.info(f"⏳ Şu testler analiz ediliyor: **{', '.join(selected_tests)}**")
                    
                    st.markdown("### 📊 Puan Grafikleri")
                    gc = st.columns(2)
                    for i, t in enumerate(analyzed_data):
                        if t["scores"]:
                            fig = plot_scores(t["scores"], t["test_name"])
                            if fig: gc[i%2].pyplot(fig)

                    with st.spinner("Yapay zeka verileri sentezliyor (Bu işlem 30-40 saniye sürebilir)..."):
                        ai_input = []
                        for t in analyzed_data:
                            ai_input.append({
                                "TEST ADI": t["test_name"], 
                                "TARİH": str(t["date"]),
                                "SONUÇLAR": t["scores"] if t["scores"] else t["raw_answers"]
                            })
                        
                        # --- DÜNYA STANDARTLARINDA ANALİZ PROMPTU ---
                        prompt = f"""
                        Sen dünyanın en prestijli eğitim kurumlarında (Harvard, MIT, Cambridge) kullanılan analiz tekniklerine hakim, uzman bir baş psikolog ve veri bilimcisisin.

                        GÖREVİN:
                        Aşağıda verileri sunulan öğrenci için "Kişiye Özel Bütüncül (Holistik) Gelişim Raporu" hazırlamak.
                        
                        ÖĞRENCİ KİMLİĞİ:
                        Ad: {info.name}, Yaş: {info.age}, Cinsiyet: {info.gender}
                        
                        ANALİZ EDİLECEK VERİLER (JSON):
                        {json.dumps(ai_input, ensure_ascii=False)}

                        ----------------------------------------------------------
                        ⚠️ KRİTİK ANALİZ KURALLARI (BUNLARA KESİNLİKLE UY):
                        
                        1. **HARMANLAMA (SENTEZ) ZORUNLULUĞU:**
                           - Asla "Enneagram sonucun bu, Çoklu Zeka sonucun şu" diye alt alta sıralama yapma.
                           - Testler arasındaki **GİZLİ BAĞLANTILARI** bul.
                           - Örn: "Matematiksel zekan yüksek (Çoklu Zeka) ama Mükemmeliyetçi yapın (Enneagram Tip 1) yüzünden işlem hatası yapmaktan korkuyorsun."
                        
                        2. **DERİNLİK VE İÇGÖRÜ:**
                           - Yüzeysel cümleler kurma. "Ders çalışmalısın" deme; "Görsel hafızan (VARK) güçlü olduğu için, formülleri renkli post-it'lere yazıp duvara asmalısın" de.
                        
                        3. **TON VE ÜSLUP:**
                           - Samimi, motive edici ama son derece profesyonel ol. Koçluk dili kullan.

                        ----------------------------------------------------------
                        ### 🌟 ANALİZ İÇİN FEW-SHOT (ÖRNEK VAKA) KÜTÜPHANESİ 🌟
                        (Analiz yaparken aşağıdaki 20 mükemmel örneğin mantığını kopyala)

                        **Vaka 1: (Enneagram Tip 5 + Görsel Öğrenme)**
                        ❌ Kötü: "Tip 5 olduğun için araştırmayı seversin. Görsel öğrenirsin."
                        ✅ İyi: "Tip 5 Araştırmacı kimliğin sayesinde konuların derinliğine inmeye bayılıyorsun. Ancak zihnin kelimelerden çok resimlerle çalışıyor (Görsel). Bu yüzden, uzun makaleler okumak yerine belgesel izleyerek veya infografik inceleyerek 3 kat daha hızlı öğrenebilirsin."

                        **Vaka 2: (Sınav Kaygısı Yüksek + Mükemmeliyetçi Tip 1)**
                        ❌ Kötü: "Sınavda heyecanlanma."
                        ✅ İyi: "Sınavlarda yaşadığın o yoğun çarpıntı (Fiziksel Kaygı), aslında başarısızlık korkusu değil; Tip 1'den gelen 'Hata yapma lüksüm yok' inancından kaynaklanıyor. Hata yapmanın, öğrenmenin bir parçası olduğunu kabul ettiğin an o el titremelerin geçecek."

                        **Vaka 3: (Sosyal Zeka Düşük + İçsel Zeka Yüksek)**
                        ❌ Kötü: "Arkadaş edinmelisin."
                        ✅ İyi: "Kalabalık gruplar seni yoruyor olabilir çünkü İçsel Zekan çok baskın; sen kendi iç dünyanda şarj oluyorsun. Sosyalleşmek için zorlama partiler yerine, birebir derin sohbet edebileceğin sakin ortamları tercih etmelisin."

                        **Vaka 4: (Bedensel Zeka Yüksek + Dikkat Dağınıklığı)**
                        ❌ Kötü: "Yerinde duramıyorsun."
                        ✅ İyi: "Ders çalışırken sürekli kalem çevirmen veya ayağını sallaman bir yaramazlık değil; Bedensel Zekan (Kinestetik) böyle çalışıyor. Hatta ders çalışırken elinde bir stres topu olması odağını artıracaktır."

                        **Vaka 5: (Müziksel Zeka + Sözel Zeka)**
                        ✅ İyi: "Kelimelerle aran çok iyi ama onları bir ritimle duyduğunda hafızana kazıyorsun. Tarih derslerini ezberlemek yerine, olayları rap şarkısı gibi ritmik bir şekilde mırıldanmayı dene."

                        **Vaka 6: (Doğacı Zeka + Tip 9 Barışçı)**
                        ✅ İyi: "Kaos ve gürültü senin en büyük düşmanın (Tip 9). Doğacı zekan da eklenince, senin için en verimli çalışma ortamı kütüphane değil; penceresi ağaca bakan sessiz bir oda veya parktaki bir banktır."

                        **Vaka 7: (Tip 3 Başarılı + Mantıksal Zeka)**
                        ✅ İyi: "Rekabet senin yakıtın (Tip 3). Mantıksal zekanla birleşince, hedeflerini bir video oyunu gibi 'Level 1, Level 2' şeklinde basamaklara bölmelisin. Her tamamladığın konu sana bir zafer hissi vermeli."

                        **Vaka 8: (Tip 2 Yardımcı + Sosyal Zeka)**
                        ✅ İyi: "Başkalarına ders anlatırken, kendin tek başına çalışmaktan çok daha iyi anlıyorsun. Çünkü Tip 2 yanın 'yardım etmeyi', Sosyal zekan ise 'etkileşimi' seviyor. Çalışma grubunun öğretmeni sen olmalısın."

                        **Vaka 9: (Tip 7 Hevesli + Düşük Çalışma Disiplini)**
                        ✅ İyi: "Zihnin bir lunapark gibi (Tip 7), sürekli eğlence arıyor. Masaya oturduğun an sıkılman çok normal. Pomodoro tekniği senin için değil; sen '15 dakika çalış, 5 dakika dans et' taktiğiyle enerjini atmalısın."

                        **Vaka 10: (Tip 6 Sadık + Yüksek Kaygı)**
                        ✅ İyi: "Sürekli 'Ya sınav kötü geçerse?' senaryoları kurman, Tip 6'nın güvenlik arayışından geliyor. Senin ilacın belirsizliği yok etmektir. Konuları bitirdikçe bir listeye tik atmak sana 'Güvendeyim, her şey kontrol altında' hissi verecektir."

                        **Vaka 11: (Görsel Zeka + Tip 4 Bireyci)**
                        ✅ İyi: "Sıradan notlar seni boğar. Tip 4 estetik arayışınla birleşen görsel zekan için defterin rengarenk, çizimlerle dolu ve sana özel olmalı. Kendi özgün not alma stilini yarat."

                        **Vaka 12: (Tip 8 Meydan Okuyan + Bedensel Zeka)**
                        ✅ İyi: "Sana 'Şunu yap' denmesinden nefret ediyorsun (Tip 8). Ders çalışmayı bir zorunluluk değil, kazanılacak bir güç savaşı olarak gör. Yürüyüş yaparken sesli notlar dinleyerek o enerjini bilgiye dönüştür."

                        **Vaka 13: (Sözel Zeka + Tip 1 Mükemmeliyetçi)**
                        ✅ İyi: "Kelimeleri seçerken o kadar titizsin ki (Tip 1), bazen kompozisyon yazarken takılıp kalıyorsun. Sözel zekan akmak istiyor. İlk taslakta hata yapmaya izin ver, düzeltmeyi sonraya bırak."

                        **Vaka 14: (İçsel Zeka + Tip 5 Gözlemci)**
                        ✅ İyi: "Sen tam bir stratejistsin. Kimseyle konuşmadan saatlerce odanda vakit geçirebilirsin. Bu izolasyon, derinlemesine öğrenme (Deep Work) için harika bir süper güç. Bunu bozma, sadece dozunu ayarla."

                        **Vaka 15: (Kinestetik Öğrenme + Tip 7)**
                        ✅ İyi: "Sadece okumak sana yetmez, yapman lazım! Deney setleri, maketler veya simülasyonlar tam sana göre. Tip 7 merakınla birleşince, dokunarak öğrendiğin hiçbir şeyi unutmazsın."

                        **Vaka 16: (Tip 2 + Düşük Sınav Kaygısı)**
                        ✅ İyi: "Sınavdan korkmuyorsun ama 'Ailemi hayal kırıklığına uğratır mıyım?' korkusu (Tip 2) seni yiyip bitiriyor. Unutma, sen notlarından ibaret değilsin ve sevilmek için başarılı olmak zorunda değilsin."

                        **Vaka 17: (Mantıksal Zeka + Tip 6)**
                        ✅ İyi: "Her bilginin mantıklı bir kanıtını istiyorsun. Ezber yapmak sana işkence gibi geliyor. Neden-sonuç ilişkisi kuramadığın hiçbir konuyu öğrenemezsin. Öğretmenine 'Neden?' diye sormaktan çekinme."

                        **Vaka 18: (Müziksel + Tip 4)**
                        ✅ İyi: "Duygusal iniş çıkışların (Tip 4) çalışma düzenini bozabilir. Ancak müziksel zekan burada devreye giriyor: Moduna uygun (Sakinleşmek için klasik, enerji için rock) müzik listeleriyle beynini hackleyebilirsin."

                        **Vaka 19: (Tip 9 + Düşük Motivasyon)**
                        ✅ İyi: "Harekete geçmek (Eylemsizlik) senin en büyük sınavın. Tip 9 konfor alanını sever. Masanın başına oturana kadar zorlanırsın ama oturduktan sonra nehir gibi akarsın. Sadece başla, gerisi gelecek."

                        **Vaka 20: (Tip 8 + Sosyal Zeka)**
                        ✅ İyi: "Liderlik vasfın (Tip 8) ve sosyal zekan seni okul kulüplerinin doğal başkanı yapıyor. Bu enerjiyi proje ödevlerini yönetirken kullanırsan hem eğlenir hem de yüksek not alırsın."

                        ----------------------------------------------------------
                        
                        İSTENEN RAPOR FORMATI:
                        1. **BÜTÜNCÜL PROFİL HARİTASI:** (Öğrencinin tüm özelliklerinin kesişim kümesi)
                        2. **SÜPER GÜÇLERİN SENTEZİ:** (Farklı testlerden gelen güçlü yanların birbirini nasıl beslediği)
                        3. **GİZLİ ENGELLER VE KİLİT ÇÖZÜMLER:** (Zayıf yönlerin analizi ve nokta atışı çözümler)
                        4. **KİŞİYE ÖZEL ÖĞRENME STRATEJİSİ:** (VARK ve Zeka türüne göre reçete)
                        5. **GELECEK VİZYONU VE KARİYER:** (Kişilik ve yeteneğe uygun meslekler)
                        6. **AİLE VE ÖĞRETMENE NOT:** (Bu öğrenciye nasıl yaklaşılmalı?)

                        Dil: Türkçe. Üslup: Profesyonel, Akıcı, İlham Verici ve Analitik.
                        """
                        
                        final_report = get_ai_analysis(prompt)
                        save_holistic_analysis(info.id, selected_tests, final_report)
                        
                        st.success("✅ Analiz tamamlandı ve kaydedildi.")
                        time.sleep(1)
                        st.rerun()

    # 5. LİSTE
    st.divider()
    with st.expander("🗂️ Test Geçmişi (Liste)"):
        if tests:
            df = pd.DataFrame(tests)
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%d.%m.%Y')
            st.dataframe(df[["test_name", "date"]], use_container_width=True)
