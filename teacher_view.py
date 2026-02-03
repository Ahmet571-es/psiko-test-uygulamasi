# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 21:03:04 2026

@author: YYYNÇİGGGİİÜÜÜÜĞĞĞ
"""

import streamlit as st
import pandas as pd
from db_utils import get_all_results

def app():
    st.title("👨‍🏫 Öğretmen Yönetim Paneli")
    
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