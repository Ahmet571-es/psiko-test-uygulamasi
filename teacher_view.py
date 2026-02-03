import streamlit as st
import pandas as pd
import time
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from db_utils import get_all_results, reset_database

# --- API AYARLARI ---
load_dotenv()
if "GROK_API_KEY" in st.secrets:
    GROK_API_KEY = st.secrets["GROK_API_KEY"]
else:
    GROK_API_KEY = os.getenv("GROK_API_KEY")

client = OpenAI(api_key=GROK_API_KEY, base_url="https://api.x.ai/v1")

# --- HARMANLANMIŞ RAPOR PROMPTU ---
HARMAN_RAPOR_PROMPT = """
Sen dünyanın en iyi psikometrik test sentez ve bütüncül profil analizi uzmanısın.

GÖREV: Aşağıda bir öğrenciye ait farklı zamanlarda yapılmış BİRDEN FAZLA testin sonuçları verilmiştir.
Bu sonuçları tek tek yorumlamak yerine, hepsini birleştirerek (sentezleyerek) öğrenci hakkında "Bütüncül Bir Profil Raporu" oluştur.

Öğrencinin Tüm Test Verileri:
{tum_cevaplar_json}

Lütfen raporu şu başlıklar altında, sade ve akıcı bir Türkçe ile yaz:

1. **Öğrenci Profil Özeti:** Tüm testlerin ortak paydası nedir? (Örn: Hem dikkatli hem mükemmeliyetçi vb.)
2. **Güçlü Yönlerin Sentezi:** Farklı testlerden gelen güçlü yönler birbirini nasıl destekliyor?
3. **Gelişim Alanları:** Hangi zayıf yönler veya riskler birden fazla testte göze çarpıyor?
4. **Öğrenme ve Çalışma Stratejisi:** Bu öğrenci en iyi nasıl öğrenir? (VARK, Zeka ve Kişilik testlerine dayanarak).
5. **Kariyer ve İlgi Eğilimleri:** Hangi meslek grupları bu profile (İlgi, Yetenek, Kişilik) en uygundur?
6. **Öğretmene Tavsiyeler:** Bu öğrenciye yaklaşırken nelere dikkat edilmeli?

Not: Asla genel geçer şeyler yazma, tamamen verilen verilere odaklan.
"""

def get_ai_response(prompt):
    if not GROK_API_KEY:
        return "Hata: API Key bulunamadı."
    try:
        response = client.chat.completions.create(
            model="grok-4-1-fast-reasoning",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Hata: {e}"

def app():
    st.title("👨‍🏫 Öğretmen Yönetim Paneli")
    
    # --- SIDEBAR: YÖNETİCİ AYARLARI ---
    with st.sidebar:
        st.markdown("---")
        st.header("⚙️ İşlemler")
        
        # Veri Silme Bölümü
        with st.expander("🗑️ Sistemi Sıfırla"):
            st.warning("DİKKAT: Tüm veriler silinir!")
            if st.checkbox("Onaylıyorum"):
                if st.button("VERİTABANINI TEMİZLE", type="primary"):
                    if reset_database():
                        st.success("Sistem sıfırlandı.")
                        time.sleep(1)
                        st.rerun()
    
    # --- VERİLERİ ÇEK ---
    results = get_all_results()
    
    if not results:
        st.info("📭 Henüz tamamlanmış bir test bulunmamaktadır.")
        return

    df = pd.DataFrame(results)
    
    # Tarih formatını güzelleştir
    # df['Tarih'] veritabanından date objesi olarak gelir, stringe çevirelim
    df['Tarih'] = pd.to_datetime(df['Tarih']).dt.strftime('%d.%m.%Y')

    # --- 1. SON AKTİVİTELER (BİLDİRİM EKRANI) ---
    st.subheader("🔔 Son Aktiviteler (Canlı Akış)")
    
    # En son yapılanı en üstte göster (Ters sıralama)
    # Not: Gerçek saat verisi için db_utils'de timestamp olması lazım ama şu an tarih bazlı sıralıyoruz.
    # Son eklenenler listenin sonundadır, ters çeviriyoruz.
    latest_df = df.iloc[::-1] 
    
    st.dataframe(
        latest_df[["Öğrenci", "Test", "Tarih"]], 
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    # --- 2. ÖĞRENCİ DETAY VE HARMANLANMIŞ RAPOR ---
    st.subheader("👤 Öğrenci İnceleme ve Analiz")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        ogrenci_listesi = df["Öğrenci"].unique()
        secilen_ogrenci = st.selectbox("İncelenecek Öğrenciyi Seç:", ogrenci_listesi)
    
    # Seçilen öğrencinin verilerini süz
    ogrenci_verisi = df[df["Öğrenci"] == secilen_ogrenci]
    toplam_test = len(ogrenci_verisi)
    
    with col2:
        st.info(f"**{secilen_ogrenci}** toplam **{toplam_test}** adet test tamamlamış.")

    # --- HARMANLANMIŞ RAPOR BUTONU ---
    if toplam_test > 1:
        st.markdown("### 🧩 Bütüncül Analiz")
        st.write("Bu öğrenci birden fazla test çözmüş. Tüm sonuçları birleştirerek yapay zeka destekli **Harmanlanmış Rapor** alabilirsiniz.")
        
        if st.button(f"🧠 {secilen_ogrenci} için HARMANLANMIŞ RAPOR OLUŞTUR", type="primary"):
            with st.spinner("Öğrencinin tüm test geçmişi (Enneagram, Dikkat, Zeka vb.) birleştirilip analiz ediliyor..."):
                # Veriyi hazırla
                tum_veriler = []
                for _, row in ogrenci_verisi.iterrows():
                    tum_veriler.append({
                        "Test Adı": row['Test'],
                        "Tarih": row['Tarih'],
                        "Sonuçlar (Puanlar/Cevaplar)": row['Ham Cevaplar'], # veya Puanlar
                        "Mevcut Rapor Özeti": row['Rapor'][:200] + "..." # Raporun başından biraz al
                    })
                
                # Promptu hazırla
                final_prompt = HARMAN_RAPOR_PROMPT.format(tum_cevaplar_json=json.dumps(tum_veriler, ensure_ascii=False))
                
                # API Çağrısı
                harman_rapor = get_ai_response(final_prompt)
                
                # Ekrana Bas
                st.markdown("---")
                st.success("✅ Harmanlanmış Rapor Hazır!")
                st.markdown(harman_rapor)
                st.download_button("📥 Harmanlanmış Raporu İndir", harman_rapor, file_name=f"{secilen_ogrenci}_Bütüncül_Analiz.txt")
                st.markdown("---")

    # --- 3. TEKİL TEST RAPORLARI ---
    st.markdown(f"### 📄 {secilen_ogrenci} - Tekil Test Geçmişi")
    
    for index, row in ogrenci_verisi.iterrows():
        # Expander başlığına Tarih ve Test adını yaz
        baslik = f"📌 {row['Test']} (Tamamlanma: {row['Tarih']})"
        
        with st.expander(baslik):
            tab1, tab2, tab3 = st.tabs(["📝 Analiz Raporu", "🔢 Cevaplar", "📊 Puanlar"])
            
            with tab1:
                st.markdown(row['Rapor'])
                st.download_button(
                    label="Raporu İndir",
                    data=str(row['Rapor']),
                    file_name=f"{secilen_ogrenci}_{row['Test']}.txt",
                    key=f"btn_{index}"
                )
            
            with tab2:
                st.json(row['Ham Cevaplar'])
                
            with tab3:
                if row['Puanlar']:
                    st.json(row['Puanlar'])
                else:
                    st.info("Bu test için sayısal puan kaydı yok (Örn: Sadece metin bazlı analiz).")
