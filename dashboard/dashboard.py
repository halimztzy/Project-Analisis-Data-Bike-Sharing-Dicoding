import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set style seaborn
sns.set(style='dark')

# --- HELPER FUNCTIONS ---
def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum"
    })
    daily_rentals_df = daily_rentals_df.reset_index()
    return daily_rentals_df

def create_season_rentals_df(df):
    season_rentals_df = df.groupby("season")[["casual", "registered"]].sum().reset_index()
    return season_rentals_df

def create_weather_rentals_df(df):
    weather_rentals_df = df.groupby("weathersit")["cnt"].mean().reset_index()
    return weather_rentals_df

# --- LOAD DATA ---
# Pastikan main_data.csv berada di folder yang sama atau sesuai path
all_df = pd.read_csv("dashboard/main_data.csv")

# Memastikan kolom dteday adalah datetime
all_df["dteday"] = pd.to_datetime(all_df["dteday"])
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(drop=True, inplace=True)

# --- SIDEBAR (LOGO SAJA) ---
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.markdown("### Bike Sharing Project")
    st.markdown("Analisis data penyewaan sepeda berdasarkan parameter waktu dan cuaca.")

# --- MAIN PAGE ---
st.header('Bike Sharing Dashboard 🚲')

# Menyiapkan variabel untuk filter
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

# --- FILTER RENTANG WAKTU (DI HALAMAN UTAMA AGAR TIDAK TERPOTONG) ---
st.subheader("Filter Data")
date_range = st.date_input(
    label='Pilih Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Cek apakah user sudah memilih kedua tanggal (start & end)
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    # Jika baru pilih satu tanggal, samakan start dan end agar tidak error
    start_date = date_range[0]
    end_date = date_range[0]

# Filter data berdasarkan tanggal yang dipilih
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                 (all_df["dteday"] <= str(end_date))]

# Menyiapkan berbagai dataframe hasil filter
daily_rentals_df = create_daily_rentals_df(main_df)
season_rentals_df = create_season_rentals_df(main_df)
weather_rentals_df = create_weather_rentals_df(main_df)

st.markdown("---")

# 1. Menampilkan Metric Total Penyewaan
st.subheader('Daily Rentals Overview')
col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = main_df.cnt.sum()
    st.metric("Total Penyewaan", value=f"{total_rentals:,}")

with col2:
    total_registered = main_df.registered.sum()
    st.metric("Total Registered", value=f"{total_registered:,}")

with col3:
    total_casual = main_df.casual.sum()
    st.metric("Total Casual", value=f"{total_casual:,}")

# 2. Visualisasi Pertanyaan 1: Pola Jam Sibuk
st.subheader("Pola Penyewaan: Hari Kerja vs Hari Libur")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=main_df, 
    x='hr', 
    y='cnt', 
    hue='workingday', 
    marker='o', 
    palette={0: 'blue', 1: 'orange'},
    ax=ax
)
ax.set_title(None)
ax.set_xlabel("Jam (0-23)")
ax.set_ylabel("Rata-rata Penyewaan")
ax.legend(title="Keterangan", labels=["Hari Libur/Weekend", "Hari Kerja"])
st.pyplot(fig)
st.write("**Insight:** Terlihat pola komuter (pagi & sore) pada hari kerja dan pola rekreasi pada siang hari di hari libur.")

# 3. Visualisasi Pertanyaan 2 & 3 (Dua Kolom)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Penyewaan per Musim")
    fig, ax = plt.subplots(figsize=(10, 6))
    season_melted = pd.melt(season_rentals_df, id_vars=['season'], value_vars=['casual', 'registered'])
    sns.barplot(data=season_melted, x='season', y='value', hue='variable', palette='viridis', ax=ax)
    ax.set_ylabel("Total Penyewaan")
    st.pyplot(fig)
    st.write("**Insight:** Musim Gugur (Fall) merupakan puncak penyewaan tertinggi.")

with col_right:
    st.subheader("Dampak Kondisi Cuaca")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=weather_rentals_df.sort_values(by='cnt', ascending=False), 
        x='weathersit', 
        y='cnt', 
        palette='magma', 
        ax=ax
    )
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)
    st.write("**Insight:** Cuaca cerah (Clear) mendominasi jumlah penyewaan dibandingkan cuaca hujan.")

st.caption('Copyright (c) Ansen Halim 2026')
