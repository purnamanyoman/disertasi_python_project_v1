# Proyek Python Disertasi

Proyek ini adalah prototipe awal untuk penelitian tentang Bloom Filter, Cuckoo Filter,
workload dinamis, evaluasi performa, dan model adaptif.

## Fitur utama
- preprocessing dataset CSV
- pembentukan query positif dan negatif
- generator workload uniform dan Zipf
- implementasi sederhana Bloom Filter
- implementasi sederhana Cuckoo Filter
- evaluasi FPR, latency, throughput, dan memory
- eksperimen parameter
- model adaptif sederhana berbasis Random Forest

## Struktur project
```text
disertasi_python_project_v1/
├── data/
│   ├── raw/          # dataset sumber
│   ├── processed/    # dataset hasil preprocessing
│   └── workload/     # output workload eksperimen
├── results/          # output hasil eksperimen
├── src/              # kode utama pipeline
├── requirements.txt  # daftar dependency Python
└── README.md         # dokumentasi singkat project
```

## Cara menjalankan
```bash
pip install -r requirements.txt
python src/main.py --input data/raw/dataset_sample.csv --key title
```
