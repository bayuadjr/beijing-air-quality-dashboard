# -*- coding: utf-8 -*-
"""
Beijing Air Quality Analysis Dashboard (2015-2017)

Aplikasi Streamlit untuk mengeksplorasi kualitas udara di 12 stasiun pemantauan Beijing.
Alur kerja lengkap (Data Wrangling -> EDA -> Visualisasi -> Analisis Lanjutan)
ada di notebook.ipynb pada root repository.

Jalankan lokal:  streamlit run dashboard/dashboard.py

Author : Bayu Adji Ramadhan
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi Halaman
st.set_page_config(
    page_title="Beijing Air Quality Dashboard",
    page_icon="🌫️",
    layout="wide"
)

# Fungsi Load Data dengan Caching agar cepat
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "main_data.csv")
    df = pd.read_csv(file_path)
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

df = load_data()

# ================= SIDEBAR FILTER =================
with st.sidebar:
    st.title("🌫️ Air Quality Explorer")
    st.markdown("Filter data pemantauan kualitas udara di 12 stasiun Beijing.")

    # Filter Rentang Tanggal
    min_date = df['datetime'].min().date()
    max_date = df['datetime'].max().date()

    start_date, end_date = st.date_input(
        label="📅 Pilih Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    # Filter Tipe Wilayah
    station_types = st.multiselect(
        label="🏙️ Pilih Zona Wilayah",
        options=df['station_type'].unique(),
        default=df['station_type'].unique()
    )

    st.caption("Proyek Akhir Analisis Data — Bayu Adji Ramadhan")

# Menyaring Data Berdasarkan Input Sidebar
filtered_df = df[
    (df['datetime'].dt.date >= start_date) &
    (df['datetime'].dt.date <= end_date) &
    (df['station_type'].isin(station_types))
]

# ================= MAIN PAGE =================
st.title("📊 Beijing Air Quality Analysis Dashboard (2015–2017)")
st.markdown(
    "Dashboard interaktif untuk memantau tingkat polutan **PM2.5** berdasarkan klasifikasi tata ruang "
    "(*Urban*, *Suburban*, *Non-Urban*), pola waktu harian/musiman, serta kategori risiko kesehatan."
)

if filtered_df.empty:
    st.warning("Data kosong untuk filter yang dipilih. Silakan sesuaikan kembali filter di sidebar.")
    st.stop()

# --- KPI Metrics ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    avg_pm25 = filtered_df['PM2.5'].mean()
    st.metric("Rata-rata PM2.5", f"{avg_pm25:.2f} µg/m³")
with col2:
    worst_station = filtered_df.groupby('station')['PM2.5'].mean().idxmax()
    st.metric("Stasiun Polusi Tertinggi", worst_station)
with col3:
    best_station = filtered_df.groupby('station')['PM2.5'].mean().idxmin()
    st.metric("Stasiun Udara Terbersih", best_station)
with col4:
    peak_hour = filtered_df.groupby('hour')['PM2.5'].mean().idxmax()
    st.metric("Jam Puncak Polusi", f"Pukul {peak_hour:02d}:00")

st.divider()

# --- Visualisasi Pertanyaan 1 ---
st.subheader("1. Perbandingan Rata-rata Konsentrasi PM2.5 per Stasiun & Zona Wilayah")

col_left, col_right = st.columns([3, 2])

with col_left:
    station_avg = filtered_df.groupby(['station', 'station_type'])['PM2.5'].mean().reset_index()
    station_avg = station_avg.sort_values(by='PM2.5', ascending=False)

    # Prinsip Desain Visual: Highlight stasiun terburuk dengan warna merah terang
    colors = ['#e74c3c' if i == 0 else '#95a5a6' for i in range(len(station_avg))]

    fig1, ax1 = plt.subplots(figsize=(8, 5))
    # hue='station' + legend=False: cara baru meneruskan warna custom tanpa
    # memunculkan legend ganda. Menghindari FutureWarning seaborn >=0.13.
    sns.barplot(data=station_avg, x='PM2.5', y='station', palette=colors,
                hue='station', legend=False, ax=ax1)
    ax1.set_title("Peringkat Stasiun Berdasarkan Rata-rata PM2.5 (Highlight: Tertinggi)", fontsize=11)
    ax1.set_xlabel("Rata-rata PM2.5 (µg/m³)")
    ax1.set_ylabel("Stasiun")
    ax1.grid(axis='x', linestyle='--', alpha=0.5)
    st.pyplot(fig1)

with col_right:
    type_avg = filtered_df.groupby('station_type')['PM2.5'].mean().reset_index()
    type_avg = type_avg.sort_values(by='PM2.5', ascending=False)
    palette_zone = {'Urban': '#e74c3c', 'Suburban': '#f39c12', 'Non-Urban': '#2ecc71'}

    fig2, ax2 = plt.subplots(figsize=(6, 5))
    # Sama seperti fig1: hue dipakai agar palette diterima tanpa warning,
    # legend dimatikan karena sumbu X sudah menjelaskan kategorinya.
    sns.barplot(data=type_avg, x='station_type', y='PM2.5', palette=palette_zone,
                hue='station_type', legend=False, ax=ax2)
    ax2.set_title("Rata-rata PM2.5 Berdasarkan Zona Wilayah", fontsize=11)
    ax2.set_xlabel("Zona Wilayah")
    ax2.set_ylabel("Rata-rata PM2.5 (µg/m³)")
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    st.pyplot(fig2)

st.divider()

# --- Visualisasi Pertanyaan 2 ---
st.subheader("2. Pola Jam Harian (Diurnal) & Tren Bulanan Konsentrasi PM2.5")

tab1, tab2 = st.tabs(["🕒 Pola Jam Harian (00:00 - 23:00)", "📅 Tren Bulanan (Musiman)"])

with tab1:
    hourly_df = filtered_df.groupby(['station_type', 'hour'])['PM2.5'].mean().reset_index()
    fig3, ax3 = plt.subplots(figsize=(11, 4.5))
    sns.lineplot(
        data=hourly_df, x='hour', y='PM2.5', hue='station_type',
        palette={'Urban': '#e74c3c', 'Suburban': '#f39c12', 'Non-Urban': '#2ecc71'},
        marker='o', linewidth=2.2, ax=ax3
    )
    ax3.set_title("Fluktuasi Rata-rata PM2.5 per Jam Berdasarkan Zona Wilayah (2015–2017)", fontsize=12)
    ax3.set_xlabel("Jam (0 - 23)")
    ax3.set_ylabel("Rata-rata PM2.5 (µg/m³)")
    ax3.set_xticks(range(0, 24))
    ax3.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig3)
    st.info(
        "💡 **Insight:** Sepanjang periode 2015–2017, konsentrasi PM2.5 mencapai titik rendah pada pagi hari "
        "(pukul 06:00–07:00, Non-Urban 54,62 µg/m³) serta sore hari (pukul 15:00–16:00), dan melonjak tajam pada malam hari "
        "(pukul 20:00–23:00, dengan puncak di wilayah Urban 84,32 µg/m³ dan Suburban 76,62 µg/m³ pada pukul 23:00, "
        "serta Non-Urban 67,65 µg/m³ pada pukul 20:00) akibat penyusutan lapisan atmosfer malam dan aktivitas logistik kendaraan berat."
    )

with tab2:
    monthly_df = filtered_df.groupby(['station_type', pd.Grouper(key='datetime', freq='ME')])['PM2.5'].mean().reset_index()
    fig4, ax4 = plt.subplots(figsize=(11, 4.5))
    sns.lineplot(
        data=monthly_df, x='datetime', y='PM2.5', hue='station_type',
        palette={'Urban': '#e74c3c', 'Suburban': '#f39c12', 'Non-Urban': '#2ecc71'},
        marker='o', linewidth=2, ax=ax4
    )
    ax4.set_title("Tren Rata-rata Bulanan PM2.5 Berdasarkan Zona Wilayah (2015–2017)", fontsize=12)
    ax4.set_xlabel("Waktu")
    ax4.set_ylabel("Rata-rata PM2.5 (µg/m³)")
    ax4.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig4)
    st.info(
        "💡 **Insight:** Terlihat siklus musiman yang sangat kuat sepanjang 2015–2017 di mana polusi udara selalu memuncak pada "
        "musim dingin (November–Januari, khususnya Desember rata-rata 116,35 µg/m³ dengan rekor Desember 2015 mencapai 128,56 µg/m³ "
        "di zona Urban) dan melandai pada akhir musim panas (Agustus rata-rata 45,06 µg/m³ dan September 51,36 µg/m³)."
    )

st.divider()

# --- Visualisasi Analisis Lanjutan (Clustering & Meteorologi) ---
st.subheader("3. Analisis Lanjutan: Clustering Risiko Kesehatan (Binning) & Korelasi Cuaca")

col_adv1, col_adv2 = st.columns([3, 2])

with col_adv1:
    cat_order = ['Good (0-35)', 'Moderate (35-75)', 'Unhealthy for Sensitive (75-115)', 'Unhealthy (115-150)', 'Very Unhealthy (>150)']
    category_dist = pd.crosstab(filtered_df['station_type'], filtered_df['pm25_category'], normalize='index') * 100
    category_dist = category_dist.reindex(columns=[c for c in cat_order if c in category_dist.columns])

    fig5, ax5 = plt.subplots(figsize=(8, 4.5))
    category_dist.plot(kind='barh', stacked=True, colormap='RdYlGn_r', ax=ax5)
    ax5.set_title("Proporsi Kategori Risiko Kesehatan Udara per Zona Wilayah", fontsize=11)
    ax5.set_xlabel("Persentase Waktu (%)")
    ax5.set_ylabel("Zona Wilayah")
    ax5.legend(title="Kategori PM2.5", bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
    ax5.grid(axis='x', linestyle='--', alpha=0.5)
    st.pyplot(fig5)

with col_adv2:
    weather_cols = ['PM2.5', 'TEMP', 'PRES', 'WSPM']
    corr = filtered_df[weather_cols].corr()
    fig6, ax6 = plt.subplots(figsize=(5, 4.5))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1, ax=ax6)
    ax6.set_title("Korelasi PM2.5 dengan Parameter Cuaca", fontsize=11)
    st.pyplot(fig6)