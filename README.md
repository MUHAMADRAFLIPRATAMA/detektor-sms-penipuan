# Detektor Pesan Penipuan

Aplikasi machine learning untuk mendeteksi apakah sebuah pesan SMS atau WhatsApp termasuk **normal** atau **penipuan**. Sistem ini menggunakan kombinasi **TF-IDF** dan **Logistic Regression**, serta menyediakan antarmuka command line dan web sederhana.

## Fitur

- Membersihkan teks sebelum diproses model.
- Mengubah teks menjadi fitur numerik menggunakan TF-IDF.
- Melatih model Logistic Regression dengan data pesan normal dan penipuan.
- Menghasilkan label `NORMAL` atau `PENIPUAN`.
- Menampilkan tingkat keyakinan prediksi.
- Menyimpan model terlatih dalam format Joblib.
- Menyimpan hasil evaluasi ke file JSON.
- Membuat grafik distribusi data, confusion matrix, dan metrik model.
- Menyediakan web interface sederhana tanpa framework tambahan.

## Struktur Folder

```text
.
├── app.py                         # Entry point command line utama
├── web_app.py                     # Server web lokal
├── predict.bat                    # Shortcut prediksi di Windows
├── data/
│   ├── dataset.csv                # Dataset tambahan
│   ├── dataset_raw/               # Dataset mentah
│   │   ├── dataset1/
│   │   ├── dataset2/
│   │   └── dataset3/
│   └── dataset_processed/
│       └── messages.csv           # Dataset hasil preprocessing
├── models/
│   ├── fraud_detector.joblib      # Model yang sudah dilatih
│   ├── evaluation.json            # Hasil evaluasi model
│   └── hasil_grafik.png           # Grafik evaluasi
├── src/
│   ├── detector.py                # Implementasi preprocessing, training, prediksi
│   ├── generate_graphs.py         # Pembuat grafik evaluasi
│   └── __init__.py
└── result/
    ├── result.html                # Halaman hasil evaluasi
    ├── demo.html                  # Halaman demo
    └── hasil_grafik.png           # Salinan grafik evaluasi
```

## Persyaratan

- Python 3.10 atau lebih baru
- pip
- Windows, Linux, atau macOS

Pustaka Python yang diperlukan:

```text
joblib
scikit-learn
matplotlib
```

Install dependensi dengan perintah berikut:

```bash
python -m pip install joblib scikit-learn matplotlib
```

Jika menggunakan beberapa instalasi Python di Windows, gunakan:

```bash
py -m pip install joblib scikit-learn matplotlib
```

## Menjalankan Training

Training membaca dataset dari folder `data/dataset_raw/`, membersihkan data, membagi data menjadi data training dan testing, lalu menyimpan model hasil training.

```bash
python app.py train
```

Atau jalankan implementasi langsung:

```bash
python src/detector.py train
```

Setelah berhasil, file berikut akan dibuat atau diperbarui:

- `data/dataset_processed/messages.csv`
- `models/fraud_detector.joblib`
- `models/evaluation.json`

Pembagian data menggunakan 80% data training dan 20% data testing. Nilai `random_state` adalah `42`, sehingga hasil pembagian dapat direproduksi.

## Melakukan Prediksi dari Command Line

Gunakan perintah berikut:

```bash
python app.py predict "Selamat Anda mendapatkan hadiah, klik link ini sekarang"
```

Contoh output:

```json
{
  "label": "PENIPUAN",
  "confidence": 0.9987,
  "message": "Selamat Anda mendapatkan hadiah, klik link ini sekarang"
}
```

Alternatif di Windows:

```bat
predict.bat "Selamat Anda mendapatkan hadiah"
```

File `predict.bat` memiliki lokasi Python yang spesifik. Jika Python terpasang di lokasi lain, jalankan perintah Python secara langsung atau ubah path Python pada file tersebut.

## Menjalankan Web Interface

Pastikan model sudah tersedia, kemudian jalankan:

```bash
python web_app.py
```

Buka alamat berikut pada browser:

```text
http://127.0.0.1:8000
```

Masukkan pesan pada kotak teks, lalu tekan tombol **Periksa Pesan**. Server menyediakan endpoint berikut:

| Method | Endpoint | Keterangan |
|---|---|---|
| GET | `/` | Menampilkan halaman aplikasi |
| POST | `/predict` | Menganalisis pesan dalam format JSON |

Contoh request ke endpoint prediksi:

```json
{
  "message": "Anda memenangkan hadiah, segera klaim sekarang"
}
```

Contoh menggunakan `curl`:

```bash
curl -X POST http://127.0.0.1:8000/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"Anda memenangkan hadiah\"}"
```

Pada Linux atau macOS, gunakan `\` sebagai pemisah baris:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"message":"Anda memenangkan hadiah"}'
```

## Alur Pemrosesan

1. Dataset dibaca dari beberapa file CSV dan format SMS tab-separated.
2. Kolom pesan dan label dicari dari beberapa nama kolom yang didukung.
3. Pesan diubah menjadi huruf kecil.
4. URL diganti menjadi token `URL`.
5. Nomor telepon diganti menjadi token `PHONE`.
6. Spasi berlebih dihapus.
7. Data duplikat dihapus.
8. Teks diubah menjadi fitur TF-IDF dengan unigram dan bigram.
9. Logistic Regression melakukan klasifikasi.
10. Model menghasilkan label dan confidence berdasarkan probabilitas prediksi.

## Format Label Dataset

Sistem mengubah label berikut menjadi kelas normal:

- `ham`
- `normal`
- `legitimate`

Label berikut diubah menjadi kelas penipuan:

- `spam`
- `scam`
- `fraud`
- `penipuan`
- `phishing`

Nilai internal yang digunakan model:

- `0` = normal
- `1` = penipuan

Dataset CSV harus memiliki kolom teks dan label. Nama kolom teks yang didukung adalah `text` atau `Pesan`. Nama kolom label yang didukung adalah `spam_ham_label`, `Kategori`, atau `label`.

## Evaluasi Model

Setelah training, hasil evaluasi disimpan dalam `models/evaluation.json`. Metrik yang digunakan adalah:

- **Accuracy**: persentase seluruh prediksi yang benar.
- **Precision**: ketepatan prediksi pada suatu kelas.
- **Recall**: kemampuan menemukan seluruh data dari suatu kelas.
- **F1-score**: keseimbangan antara precision dan recall.
- **Support**: jumlah data pada setiap kelas.

Untuk membuat grafik evaluasi:

```bash
python src/generate_graphs.py
```

Grafik akan disimpan di:

```text
models/hasil_grafik.png
```

Grafik berisi:

- Distribusi jumlah pesan normal dan penipuan.
- Confusion matrix.
- Perbandingan accuracy, F1 normal, dan F1 penipuan.

Halaman hasil evaluasi dapat dibuka dengan membuka file berikut pada browser:

```text
result/result.html
```

## Catatan Penggunaan

- Hasil model bukan jaminan mutlak bahwa sebuah pesan benar-benar penipuan.
- Confidence adalah probabilitas dari model, bukan bukti keamanan pesan.
- Pesan dengan pola baru atau bahasa yang berbeda dari dataset dapat menghasilkan prediksi yang kurang akurat.
- Jangan memasukkan data pribadi, password, PIN, atau informasi rahasia ke aplikasi saat pengujian.
- Untuk hasil yang lebih baik, gunakan dataset yang cukup besar, beragam, dan memiliki label yang benar.

## Troubleshooting

### Model belum ada

Jika muncul pesan `Model belum ada`, jalankan training terlebih dahulu:

```bash
python app.py train
```

### Dataset tidak ditemukan

Pastikan struktur folder dataset sesuai dengan struktur proyek, terutama:

```text
data/dataset_raw/dataset1/
data/dataset_raw/dataset2/
data/dataset_raw/dataset3/
```

### Dependensi belum terpasang

Install ulang dependensi:

```bash
python -m pip install joblib scikit-learn matplotlib
```

### Port 8000 sedang digunakan

Ubah port pada bagian akhir `web_app.py`, misalnya dari `8000` menjadi `8080`, lalu buka:

```text
http://127.0.0.1:8080
```

## Lisensi dan Dataset

Proyek ini menggunakan dataset publik untuk kebutuhan pengembangan dan evaluasi. Periksa lisensi masing-masing dataset sebelum menggunakan proyek ini untuk kebutuhan komersial atau mendistribusikan ulang datanya.
