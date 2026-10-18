# Beijing Air Quality Analysis Dashboard 🌫️

Proyek akhir **Belajar Analisis Data dengan Python (Dicoding)** — analisis data dan dashboard interaktif menggunakan **Air Quality Dataset** dari 12 stasiun pemantauan kualitas udara di Beijing, Tiongkok.

- **Nama:** Bayu Adji Ramadhan
- **Dataset:** [Beijing Multi-Site Air Quality Data Set — UCI ML Repository #501](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data) (2013–2017)
- **Periode analisis dashboard:** Januari 2015 – Februari 2017

## 🔗 Dashboard Online

Dashboard sudah di-deploy di Streamlit Community Cloud:
**Lihat `url.txt`** untuk tautan publiknya.

---

## 🎯 Pertanyaan Bisnis

1. **Stasiun manakah** di masing-masing kategori wilayah (*Urban*, *Suburban*, *Non-Urban*) yang mencatatkan rata-rata konsentrasi **PM2.5** tertinggi dan terendah selama 2015–2017, untuk menentukan prioritas lokasi intervensi pengendalian emisi?
2. **Pada jam berapakah** puncak rata-rata konsentrasi PM2.5 harian terjadi di tiap kategori wilayah, dan bagaimana pola fluktuasi musimannya — untuk mendukung penyusunan jadwal pembatasan operasional kendaraan berat dan peringatan dini kesehatan?

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

---

## 🔍 Temuan Utama

- **Hierarki wilayah konsisten sepanjang 24 jam:** *Urban* tertinggi (73–88 µg/m³) → *Suburban* (65–80 µg/m³) → *Non-Urban* (58–71 µg/m³).
- **Pola diurnal:** titik terendah pada 06:00–07:00, lalu melonjak pada 20:00–23:00 akibat penyusutan lapisan atmosfer malam dan aktivitas logistik kendaraan berat.
- **Siklus musiman kuat:** puncak polusi selalu jatuh pada Desember–Januari (musim dingin, inversi suhu), melandai pada Agustus–September.
- **Meteorologi:** kecepatan angin (`WSPM`) berkorelasi negatif dengan PM2.5 (angin mendispersi polutan), sedangkan tekanan udara (`PRES`) berkorelasi positif — memperkuat temuan pola musim dingin.

---

## 🛠️ Teknologi

- **Python** — pandas, NumPy
- **Visualisasi** — Matplotlib, Seaborn
- **Dashboard** — Streamlit
- **Analisis** — *Manual grouping & binning*, korelasi Pearson, analisis time series

---

## 📄 Lisensi Dataset

Dataset bersifat publik dan digunakan hanya untuk keperluan pembelajaran (proyek akhir Dicoding).
