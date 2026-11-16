# Beijing Air Quality Analysis Dashboard 🌫️

Proyek akhir **Belajar Analisis Data dengan Python (Dicoding)** — analisis data dan dashboard interaktif menggunakan **Air Quality Dataset** dari 12 stasiun pemantauan kualitas udara di Beijing, Tiongkok.

- **Nama:** Bayu Adji Ramadhan
- **Dataset:** [Beijing Multi-Site Air Quality Data Set — UCI ML Repository #501](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data) (2013–2017)
- **Periode analisis dashboard:** Januari 2015 – Februari 2017

## 🔗 Dashboard Online

Dashboard sudah di-deploy di Streamlit Community Cloud:

🔗 **https://beijing-air-quality-bayu.streamlit.app**

Tautan yang sama juga tersimpan di berkas `url.txt`.

---

## 🎯 Pertanyaan Bisnis

1. **Stasiun manakah** di masing-masing kategori wilayah (*Urban*, *Suburban*, dan *Non-Urban*) yang mencatatkan rata-rata konsentrasi **PM2.5** tertinggi dan terendah selama periode tahun 2015 hingga 2017 untuk menentukan prioritas lokasi intervensi pengendalian emisi?
2. **Pada jam berapakah** puncak rata-rata konsentrasi **PM2.5** harian terjadi di wilayah *Urban*, *Suburban*, dan *Non-Urban* selama periode tahun 2015 hingga 2017, serta bagaimana pola fluktuasi musimannya pada rentang 2015 hingga 2017 guna mendukung penyusunan jadwal pembatasan operasional kendaraan berat dan peringatan dini kesehatan?

---

## 📁 Struktur Direktori

```
submission/
├── dashboard/
│   ├── dashboard.py        # Aplikasi Streamlit (main file)
│   └── main_data.csv       # Dataset bersih hasil wrangling (2015–2017)
├── data/
│   └── PRSA_Data_*.csv     # Dataset mentah 12 stasiun (2013–2017)
├── notebook.ipynb          # Data Wrangling → EDA → Visualisasi → Analisis Lanjutan
├── requirements.txt        # Dependensi Python
├── url.txt                 # Tautan dashboard yang sudah di-deploy
└── README.md
```

---

## 🚀 Menjalankan Dashboard di Lokal

### 1. Siapkan environment

```bash
# Masuk ke folder submission
cd submission

# Buat virtual environment
python -m venv env

# Aktifkan
source env/bin/activate        # Linux / macOS
# env\Scripts\activate         # Windows

# Install seluruh dependensi
pip install -r requirements.txt
```

### 2. Jalankan aplikasi

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka otomatis di `http://localhost:8501`. Jika browser tidak terbuka sendiri, buka manual tautan tersebut.

### 3. Hentikan server

```bash
Ctrl + C
```

---

## 📊 Fitur Dashboard

| Bagian | Isi |
| --- | --- |
| **Sidebar Filter** | Rentang tanggal (2015–2017) & pilihan zona wilayah (*Urban*, *Suburban*, *Non-Urban*) — semua visualisasi ikut menyesuaikan |
| **KPI Metrics** | Rata-rata PM2.5, stasiun terpolusi, stasiun terbersih, jam puncak polusi |
| **Visualisasi 1** | Peringkat stasiun berdasarkan rata-rata PM2.5 (stasiun terburuk di-highlight merah) + perbandingan antar zona wilayah |
| **Visualisasi 2** | Pola jam harian (*diurnal*), tren bulanan (*musiman*) dalam bentuk tab |
| **Analisis Lanjutan** | *Manual Grouping & Binning* kategori risiko kesehatan (5 kelas) + heatmap korelasi PM2.5 dengan parameter cuaca (TEMP, PRES, WSPM) |

> Catatan: notebook menganalisis 6 parameter cuaca (TEMP, PRES, DEWP, RAIN, WSPM). Dashboard memakai 4 parameter kunci saja karena `main_data.csv` sengaja diekspor ringkas (hanya kolom yang dipakai visualisasi) agar ukuran file tetap ~22 MB dan proses *load* di Streamlit Cloud cepat.

---

## 🔍 Temuan Utama

- **Perbandingan kategori wilayah & stasiun (2015–2017):** Rata-rata PM2.5 tertinggi berada di wilayah *Urban* (**76,51 µg/m³**; tertinggi **Dongsi 80,02 µg/m³**, terendah **Wanliu 73,50 µg/m³**) → diikuti *Suburban* (**68,46 µg/m³**; tertinggi **Shunyi 73,54 µg/m³**, terendah **Changping 63,39 µg/m³**) → dan *Non-Urban* (**61,45 µg/m³**; tertinggi **Huairou 62,95 µg/m³**, terendah sekaligus terbersih **Dingling 59,95 µg/m³**).
- **Pola diurnal (2015–2017):** Konsentrasi PM2.5 mencapai titik rendah pada pagi hari (06:00–07:00, *Non-Urban* **54,62 µg/m³**) dan sore hari (15:00–16:00, *Urban* **70,22 µg/m³**, *Suburban* **62,38 µg/m³**), lalu melonjak pada malam hari (20:00–23:00) dengan puncak di *Urban* (**84,32 µg/m³** pukul 23:00), *Suburban* (**76,62 µg/m³** pukul 23:00), dan *Non-Urban* (**67,65 µg/m³** pukul 20:00).
- **Siklus musiman kuat (2015–2017):** Puncak polusi selalu jatuh pada musim dingin November–Januari (rata-rata bulan **Desember 116,35 µg/m³**, **November 100,81 µg/m³**, dan **Januari 83,39 µg/m³**; rekor tertinggi pada **Desember 2015** hingga **128,56 µg/m³** di *Urban*), serta melandai pada akhir musim panas (**Agustus 45,06 µg/m³** dan **September 51,36 µg/m³**).
- **Meteorologi:** Kecepatan angin (`WSPM`, `r = -0,32`) berkorelasi negatif dengan PM2.5 (angin efektif mendispersi polutan), sedangkan suhu udara (`TEMP`, `r = -0,15`) berkorelasi negatif yang mengonfirmasi tingginya polusi saat musim dingin.

---

## 🛠️ Teknologi

- **Python** — pandas, NumPy
- **Visualisasi** — Matplotlib, Seaborn
- **Dashboard** — Streamlit
- **Analisis** — *Manual grouping & binning*, korelasi Pearson, analisis time series

---

## 📄 Lisensi Dataset

Dataset bersifat publik dan digunakan hanya untuk keperluan pembelajaran (proyek akhir Dicoding).
