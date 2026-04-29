# Bike Sharing Analysis Dashboard ✨

## Deskripsi
Proyek ini merupakan tugas akhir dari modul "Analisis Data dengan Python" di Dicoding. Proyek ini bertujuan untuk menganalisis dataset Bike Sharing dan menyajikannya dalam bentuk dashboard interaktif. Analisis berfokus pada pola penggunaan sepeda berdasarkan jam sibuk, pengaruh musim, dan dampak kondisi cuaca terhadap jumlah penyewaan.

## Struktur Folder
- `dashboard`: Berisi file `dashboard.py` dan data yang sudah dibersihkan `main_data.csv`.
- `data`: Berisi dataset asli (day.csv & hour.csv).
- `notebook.ipynb`: File analisis data lengkap mulai dari Gathering hingga Visualisasi.
- `requirements.txt`: Daftar library yang dibutuhkan.

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir bike_sharing_analysis
cd bike_sharing_analysis
pip install -r requirements.txt
```

## Run Streamlit App
```
streamlit run dashboard/dashboard.py
```
