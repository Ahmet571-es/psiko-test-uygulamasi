import streamlit as st
import pandas as pd
import time
from db_utils import get_all_results, reset_database

def app():
    st.title("👨‍🏫 Öğretmen Yönetim Paneli")
    
    # --- SIDEBAR: SIFIRLAMA BUTONU ---
    with st.sidebar:
        st.markdown("---")
        st.header("⚠️ Yönetici Ayarları")
        
        with st.expander("🗑️ Sistemi Sıfırla"):
            st.error("Bu işlem tüm öğrenci kayıtlarını ve test sonuçlarını kalıcı olarak silecektir!")
            
            # Yanlışlıkla basılmasın diye onay kutusu
            onay = st.checkbox("Evet, tüm verileri silmek istiyorum.")
            
            if onay:
                if st.button("VERİLERİ SİL", type="primary"):
                    if reset_database():
                        st.success("Veritabanı temizlendi!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Bir hata oluştu.")

    # --- ANA EKRAN ---
    results = get_all_results()
    
    if not results:
        st.info("Sistemde henüz tamamlanmış bir test kaydı bulunmamaktadır.")
        return

    # Verileri Tabloya Dönüştür
    df = pd.DataFrame(results)
    
    # 1. Genel Liste
    st.subheader("📋 Tüm Tamamlanan Testler")
    st.dataframe(df[["Öğrenci", "Test", "Tarih"]], use_container_width=True)
    
    st.markdown("---")
    
    # 2. Detaylı İnceleme
    st.subheader("🔍 Detaylı Rapor Görüntüleme")
    
    col1, col2 = st.columns(2)
    with col1:
        ogrenci_listesi = df["Öğrenci"].unique()
        secilen_ogrenci = st.selectbox("Öğrenci Seçiniz:", ogrenci_listesi)
    
    # Seçilen öğrencinin verilerini süz
    ogrenci_verisi = df[df["Öğrenci"] == secilen_ogrenci]
    
    st.success(f"**{secilen_ogrenci}** adlı öğrencinin test sonuçları:")
    
    for index, row in ogrenci_verisi.iterrows():
        with st.expander(f"📄 {row['Test']} - {row['Tarih']} (Raporu Aç)"):
            
            tab1, tab2, tab3 = st.tabs(["Yapay Zeka Analizi", "Öğrenci Cevapları", "Sayısal Skorlar"])
            
            with tab1:
                st.markdown("### 📝 Analiz Raporu")
                st.markdown(row['Rapor'])
                st.download_button(
                    label="📥 Bu Raporu İndir",
                    data=row['Rapor'],
                    file_name=f"{secilen_ogrenci}_{row['Test']}_Analiz.txt",
                    mime="text/plain"
                )
            
            with tab2:
                st.markdown("### 🔢 Ham Cevaplar")
                st.json(row['Ham Cevaplar'])
                
            with tab3:
                st.markdown("### 📊 Puan Tablosu")
                st.json(row['Puanlar'])
