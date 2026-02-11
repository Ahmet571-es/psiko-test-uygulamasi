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

# --- API VE BAĞLANTI AYARLARI ---
load_dotenv()
if "GROK_API_KEY" in st.secrets:
    GROK_API_KEY = st.secrets["GROK_API_KEY"]
else:
    GROK_API_KEY = os.getenv("GROK_API_KEY")

# xAI (Grok) İstemcisi
client = OpenAI(api_key=GROK_API_KEY, base_url="https://api.x.ai/v1")

# --- YARDIMCI FONKSİYONLAR ---

def get_ai_analysis(prompt):
    """
    Yapay Zekaya analiz isteği gönderir.
    Hata durumunda kullanıcıya bilgi döner.
    """
    if not GROK_API_KEY:
        return "Hata: API Key bulunamadı. Lütfen sistem yöneticisiyle görüşün."
    try:
        response = client.chat.completions.create(
            model="grok-4-1-fast-reasoning", # Akıl yürütme yeteneği en yüksek model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1 # Daha tutarlı ve analitik sonuçlar için düşük sıcaklık
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Analiz sırasında bir hata oluştu: {str(e)}"

def plot_scores(data_dict, title):
    """
    Test sonuçlarını görselleştirmek için Bar Grafiği oluşturur.
    """
    if not data_dict or not isinstance(data_dict, dict):
        return None
    
    # Veriyi hazırla
    labels = [str(k) for k in data_dict.keys()]
    try:
        values = [float(v) for v in data_dict.values()]
    except:
        return None 

    # Grafik Ayarları (Seaborn & Matplotlib)
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Renk paleti ve çizim
    sns.barplot(x=values, y=labels, ax=ax, palette="viridis", orient='h')
    
    ax.set_title(f"{title} - Puan Dağılımı", fontsize=14, fontweight='bold')
    ax.set_xlabel("Puan / Yüzde")
    ax.set_ylabel("Kategoriler / Tipler")
    
    plt.tight_layout()
    return fig

# --- ANA ÖĞRETMEN UYGULAMASI ---

def app():
    # --- CSS: MOUSE İŞARETÇİSİ VE ARAYÜZ İYİLEŞTİRMELERİ ---
    st.markdown("""
    <style>
        /* Tüm Seçim Kutuları (Selectbox, Multiselect) üzerine gelince el işareti çıksın */
        .stSelectbox div, .stMultiSelect div {
            cursor: pointer !important;
        }
        div[data-baseweb="select"] {
            cursor: pointer !important;
        }
        /* Açılır liste elemanları */
        div[role="listbox"] li {
            cursor: pointer !important;
        }
        /* Radyo Butonları */
        .stRadio > label {
            font-weight: bold;
            font-size: 16px;
            color: #2E86C1;
            cursor: pointer !important;
        }
        .stRadio div[role="radiogroup"] > label {
            cursor: pointer !important;
        }
        /* Rapor Arşiv Kutusu */
        .archive-box {
            background-color: #f8f9fa;
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        /* Rapor Başlıkları */
        .report-header {
            color: #155724;
            background-color: #d4edda;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
            border: 1px solid #c3e6cb;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("👨‍🏫 Öğretmen Yönetim Paneli")
    st.markdown("---")

    # Veritabanından verileri çek
    data = get_all_students_with_results()
    
    # Öğrenci İsim Listesini Oluştur
    student_names_all = [d["info"].name for d in data] if data else []

    # --- SIDEBAR: YÖNETİM VE SİLME ARAÇLARI ---
    with st.sidebar:
        st.header("⚙️ Yönetim Araçları")
        
        # 1. ÖĞRENCİ SİLME
        with st.expander("🗑️ Öğrenci Dosyası Sil"):
            if not student_names_all:
                st.info("Sistemde kayıtlı öğrenci yok.")
            else:
                st.warning("Seçilen öğrencilerin tüm verileri (testler, raporlar) silinecektir.")
                selected_to_delete = st.multiselect("Silinecekleri Seç:", options=student_names_all)
                
                if selected_to_delete:
                    if st.button("SEÇİLENLERİ KALICI OLARAK SİL", type="primary"):
                        if delete_specific_students(selected_to_delete):
                            st.success("Kayıtlar başarıyla silindi.")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Silme işlemi başarısız oldu.")

        st.markdown("---")
        
        # 2. TAM SIFIRLAMA
        with st.expander("⚠️ Fabrika Ayarlarına Dön"):
            st.error("DİKKAT: Bu işlem tüm veritabanını temizler.")
            if st.button("TÜM SİSTEMİ SIFIRLA"):
                if reset_database():
                    st.success("Sistem tamamen sıfırlandı.")
                    time.sleep(1)
                    st.rerun()

    # --- ANA EKRAN AKIŞI ---
    
    if not data:
        st.info("📂 Henüz kayıtlı öğrenci verisi bulunmamaktadır.")
        return

    # 1. ÖĞRENCİ SEÇİMİ (VARSAYILAN BOŞ)
    st.subheader("📂 Öğrenci Dosyası Görüntüle")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        # index=None ile varsayılan boş gelir, placeholder görünür
        selected_name = st.selectbox(
            "İncelemek İstediğiniz Öğrenciyi Seçiniz:", 
            student_names_all, 
            index=None, 
            placeholder="Listeden bir öğrenci seçin..."
        )
    
    # EĞER SEÇİM YAPILMADIYSA BURADA DUR
    if not selected_name:
        st.info("👆 Lütfen analizlerini görmek istediğiniz öğrenciyi yukarıdaki listeden seçiniz.")
        return

    # SEÇİLEN ÖĞRENCİNİN VERİLERİNİ AL
    student_data = next(d for d in data if d["info"].name == selected_name)
    info = student_data["info"]
    tests = student_data["tests"]

    # 2. ÖĞRENCİ KİMLİK KARTI
    with st.container():
        st.markdown(f"### 🆔 {info.name}")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Yaş / Cinsiyet", f"{info.age} / {info.gender}")
        c1.caption("Demografik Bilgi")
        
        c2.metric("Kullanıcı Adı", info.username)
        c2.caption("Sistem Girişi")
        
        c3.write(f"**Şifre:** {info.password}")
        c3.caption("Güvenlik")
        
        c4.metric("Toplam Giriş", info.login_count)
        c4.caption("Aktiflik Durumu")
    
    st.divider()

    # ============================================================
    # 3. KAYITLI RAPOR ARŞİVİ (VERİTABANINDAN ÇEKİLENLER)
    # ============================================================
    st.subheader("📂 Kayıtlı Rapor Arşivi")
    
    # Bu öğrencinin geçmiş raporlarını veritabanından getir
    history = get_student_analysis_history(info.id)
    
    if not history:
        st.info("Bu öğrenci için henüz oluşturulmuş bütüncül veya detaylı bir analiz raporu bulunmamaktadır.")
    else:
        st.markdown(f"Bu öğrenci için **{len(history)} adet** kayıtlı rapor bulundu. Görüntülemek için aşağıdan seçim yapabilirsiniz:")
        
        for idx, record in enumerate(history):
            # Buton etiketi: Kombinasyon + Tarih
            btn_label = f"📄 Rapor {idx+1}: {record['combination']} ({record['date']})"
            
            with st.expander(btn_label):
                st.markdown(f"<div class='report-header'><b>ANALİZ EDİLEN TESTLER:</b> {record['combination']}</div>", unsafe_allow_html=True)
                st.markdown(record['report'])
                
                # İndirme Butonu
                st.download_button(
                    label=f"📥 Raporu İndir ({idx+1})",
                    data=record['report'],
                    file_name=f"{info.name}_Rapor_{idx+1}.txt",
                    mime="text/plain",
                    key=f"dl_{idx}"
                )

    st.divider()

    # ============================================================
    # 4. YENİ ANALİZ OLUŞTURMA MERKEZİ (SEÇENEKLİ)
    # ============================================================
    st.subheader("⚡ Yeni Analiz Oluştur")
    
    if not tests:
        st.warning("⚠️ Bu öğrenci henüz hiç test çözmemiş. Analiz yapılamaz.")
    else:
        # Öğrencinin çözdüğü tüm testleri listele
        all_completed_tests = [t["test_name"] for t in tests]
        
        st.write("Analiz raporu oluşturmak istediğiniz testleri seçiniz:")
        
        # Çoklu Seçim Kutusu
        selected_tests = st.multiselect(
            "Test Listesi:", 
            options=all_completed_tests, 
            default=all_completed_tests # Kolaylık olsun diye hepsi seçili gelsin
        )
        
        if selected_tests:
            st.markdown("---")
            st.write("📊 **Analiz Yöntemini Seçiniz:**")
            
            # --- YÖNTEM SEÇİMİ (RADIO BUTTON) ---
            analysis_mode = st.radio(
                "Nasıl bir rapor istiyorsunuz?",
                options=["BÜTÜNCÜL (Harmanlanmış) Rapor", "AYRI AYRI (Tekil) Raporlar"],
                index=0,
                help="Bütüncül: Seçilen tüm testleri birleştirip tek bir sentez rapor yazar.\nAyrı Ayrı: Seçilen her test için sırayla ayrı ayrı raporlar oluşturur ve kaydeder."
            )
            
            st.markdown("<br>", unsafe_allow_html=True) # Boşluk
            
            if st.button("🚀 ANALİZİ BAŞLAT", type="primary"):
                # Seçilen testlerin verilerini filtrele
                analyzed_data = [t for t in tests if t["test_name"] in selected_tests]
                
                # --- ORTAK ADIM: PUAN GRAFİKLERİNİ GÖSTER ---
                st.markdown("### 📊 Puan Grafikleri")
                gc = st.columns(2)
                for i, t in enumerate(analyzed_data):
                    if t["scores"]:
                        fig = plot_scores(t["scores"], t["test_name"])
                        if fig:
                            gc[i % 2].pyplot(fig)
                        else:
                            gc[i % 2].info(f"{t['test_name']} için grafik verisi yok.")

                # ====================================================
                # MOD 1: BÜTÜNCÜL (HARMANLANMIŞ) ANALİZ
                # ====================================================
                if analysis_mode == "BÜTÜNCÜL (Harmanlanmış) Rapor":
                    
                    st.info(f"⏳ Yapay Zeka, seçilen **{len(selected_tests)} testi** birbiriyle ilişkilendirerek bütüncül bir rapor yazıyor. Lütfen bekleyin...")
                    
                    with st.spinner("Analiz sentezleniyor..."):
                        # Yapay Zekaya gidecek veriyi hazırla
                        ai_input = []
                        for t in analyzed_data:
                            ai_input.append({
                                "TEST ADI": t["test_name"], 
                                "TARİH": str(t["date"]),
                                "SONUÇLAR": t["scores"] if t["scores"] else t["raw_answers"]
                            })
                        
                        # --- DÜNYA STANDARTLARINDA SÜPER PROMPT ---
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
                        
                        # Bütüncül raporu veritabanına kaydet
                        save_holistic_analysis(info.id, selected_tests, final_report)
                        
                        st.success("✅ Bütüncül analiz başarıyla tamamlandı ve Arşiv'e kaydedildi.")
                        time.sleep(1.5)
                        st.rerun()

                # ====================================================
                # MOD 2: AYRI AYRI (TEKİL) ANALİZLER
                # ====================================================
                else:
                    progress_text = "Testler sırayla analiz ediliyor. Lütfen bekleyin..."
                    my_bar = st.progress(0, text=progress_text)
                    total_ops = len(analyzed_data)
                    
                    for idx, t in enumerate(analyzed_data):
                        test_name = t["test_name"]
                        my_bar.progress((idx + 1) / total_ops, text=f"**{test_name}** analiz ediliyor... ({idx+1}/{total_ops})")
                        
                        ai_input = [{
                            "TEST ADI": test_name, 
                            "TARİH": str(t["date"]),
                            "SONUÇLAR": t["scores"] if t["scores"] else t["raw_answers"]
                        }]
                        
                        # Tekil Analiz Promptu
                        prompt = f"""
                        Sen uzman bir psikologsun. Aşağıdaki TEST SONUCUNA göre öğrenciyi detaylı analiz et.
                        
                        ÖĞRENCİ: {info.name}, {info.age}, {info.gender}
                        TEST: {test_name}
                        VERİLER: {json.dumps(ai_input, ensure_ascii=False)}

                        GÖREV: Sadece bu teste odaklanarak derinlemesine bir yorum yap.
                        RAPOR FORMATI:
                        1. Test Sonucunun Anlamı
                        2. Güçlü Yönler
                        3. Gelişim Alanları
                        4. Bu Teste Özel Tavsiyeler
                        
                        Dil: Türkçe.
                        """
                        
                        single_report = get_ai_analysis(prompt)
                        
                        # Tek başına (Liste içinde tek eleman olarak) kaydet
                        save_holistic_analysis(info.id, [test_name], single_report)
                    
                    my_bar.empty()
                    st.success(f"✅ Seçilen {total_ops} test başarıyla AYRI AYRI analiz edildi ve Arşiv'e eklendi.")
                    time.sleep(2)
                    st.rerun()

    # 5. TEST GEÇMİŞİ LİSTESİ (ALT KISIM)
    st.divider()
    with st.expander("🗂️ Test Geçmişi ve Ham Veriler (Liste)"):
        if tests:
            df_tests = pd.DataFrame(tests)
            df_tests['date'] = pd.to_datetime(df_tests['date']).dt.strftime('%d.%m.%Y')
            st.dataframe(df_tests[["test_name", "date"]], use_container_width=True)
