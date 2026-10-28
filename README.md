# BPOM Drug Regulatory Affairs AI Agent
### Sistem Cerdas Asisten Regulasi Obat BPOM RI (Bilingual: Bahasa Indonesia & English)
Link publikasi aplikasi: https://gratis-components-emotions-macintosh.trycloudflare.com/

AI Agent spesialis regulasi obat (Regulatory Affairs) yang dirancang khusus untuk memandu proses registrasi obat ke **Badan Pengawas Obat dan Makanan Republik Indonesia (BPOM RI)**. Dilengkapi dengan logika penentuan jalur (pathway decision logic), daftar periksa modul ACTD/ICH CTD, verifikasi tarif resmi PNBP dan timeline evaluasi, audit kesenjangan dossier (gap-check), serta ekspor laporan resmi Microsoft Word (`.docx`).

---

## 🏛️ Landasan Regulasi & Rujukan Resmi BPOM

Agent ini memverifikasi data dan persyaratan teknis terhadap regulasi resmi BPOM RI terkini:
1. **Peraturan BPOM No. 24 Tahun 2017** tentang Kriteria dan Tata Laksana Registrasi Obat.
2. **Peraturan BPOM No. 13 Tahun 2021** (Perubahan PerBPOM 24/2017 - tata laksana jalur elektronik AAS/ASROT).
3. **Peraturan BPOM No. 24 Tahun 2023** (Perubahan Kedua - Jalur Evaluasi Reliance untuk obat yang telah disetujui SRA/WHO Listed Authority).
4. **Peraturan Pemerintah (PP) No. 32 Tahun 2017** tentang Jenis dan Tarif atas Jenis Penerimaan Negara Bukan Pajak (PNBP) yang Berlaku pada Badan POM.
5. **Peraturan BPOM No. 15 Tahun 2019 jo. No. 28 Tahun 2022** tentang Registrasi Produk Biologi & Biosimilar.
6. **Peraturan BPOM No. 27 Tahun 2020** tentang Penerapan CPOB & Penilaian/Pengakuan CPOB Luar Negeri (Desk Evaluation & On-site).
7. **Peraturan BPOM No. 11 Tahun 2022** tentang Tata Laksana Uji Bioekivalensi (BE) & Kriteria Biowaiver BCS.
8. **ASEAN Stability Guideline (Zone IVb)**: Kondisi penyimpanan iklim tropis panas dan sangat lembap (30°C ± 2°C / 75% ± 5% RH).

---

## 📁 Struktur Direktori

```
Tugas AI/
├── bpom_ra_agent/
│   ├── __init__.py
│   ├── cli.py                     # Antarmuka CLI bilingual (EN/ID)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── regulatory_database.py  # Basis data regulasi, tarif PNBP (PP 32/2017), & timeline evaluasi HK
│   │   ├── decision_engine.py      # Pathway Decision Logic (Kategori 1-7, Jalur 40/100/120/150/300 HK)
│   │   ├── ctd_checklist.py       # Generator checklist ACTD Modul 1 s/d 4 (dengan trigger kekhususan BPOM)
│   │   ├── gap_analyzer.py        # Mesin audit gap-check (identifikasi temuan Critical, Major, Minor)
│   │   └── template_engine.py     # Template Cover Letter BPOM, Komitmen Stabilitas Zona IVb, Biowaiver
│   └── docx_generator/
│       ├── __init__.py
│       └── docx_builder.py        # Generator dokumen Word (.docx) eksekutif dengan tabel dan styling
├── agent_skill/
│   └── SKILL.md                   # Definisi skill Antigravity untuk aktivasi percakapan otomatis
├── test_scenarios/
│   ├── scenarios_data.py          # Data 3 skenario realistis (Biologi Impor, Generik Lokal, Gap-Check)
│   └── test_runner.py             # Script pengujian otomatis bilingual yang menghasilkan dokumen .docx
├── outputs/                       # Berkas Word (.docx) hasil evaluasi & audit
│   ├── Scenario_1_Imported_Biologic_Evaluation_EN.docx
│   ├── Scenario_1_Evaluasi_Produk_Biologi_Impor_ID.docx
│   ├── Scenario_2_Local_Generic_Evaluation_EN.docx
│   ├── Scenario_2_Evaluasi_Obat_Generik_Lokal_ID.docx
│   ├── Scenario_3_Dossier_Gap_Check_Audit_Report_EN.docx
│   └── Scenario_3_Laporan_Audit_Gap_Check_Dossier_ID.docx
└── README.md
```

---

## 🚀 Cara Menjalankan

### 1. Menjalankan Seluruh Skenario Uji (Test Scenarios)
Untuk mengeksekusi 3 skenario realistis sekaligus dan memperbarui dokumen Word (`.docx`):
```powershell
& "C:\Users\taniya.elizabeth\AppData\Local\Programs\Python\Python312\python.exe" test_scenarios\test_runner.py
```

### 2. Menggunakan CLI untuk Evaluasi Skenario Tertentu
```powershell
# Jalankan Skenario 1 (Produk Biologi Impor)
& "C:\Users\taniya.elizabeth\AppData\Local\Programs\Python\Python312\python.exe" bpom_ra_agent\cli.py --scenario 1

# Jalankan Skenario 2 (Obat Generik Lokal)
& "C:\Users\taniya.elizabeth\AppData\Local\Programs\Python\Python312\python.exe" bpom_ra_agent\cli.py --scenario 2

# Jalankan Skenario 3 (Audit Gap-Check Dossier Onkologi)
& "C:\Users\taniya.elizabeth\AppData\Local\Programs\Python\Python312\python.exe" bpom_ra_agent\cli.py --scenario 3
```

---

## 📊 Hasil Uji 3 Skenario Realistis

### Skenario 1: Produk Biologi Impor (Trastuzumab Biosimilar mAb)
- **Nama Produk**: Herclonix 440 mg Serbuk Liofilisasi untuk Infus
- **Klasifikasi**: Biosimilar (Produk Biologi) - Impor dari Uni Eropa (Belanda)
- **Status Persetujuan SRA**: Telah disetujui oleh EMA (Eropa) & Health Canada
- **Hasil Keputusan Jalur BPOM**:
  - **Kategori**: Kategori 1 (Zat Aktif Baru / Produk Biologi / Biosimilar)
  - **Jalur Evaluasi**: Jalur 120 Hari Kerja (Biosimilar Terdaftar SRA via Mekanisme Reliance Parsial - PerBPOM 24/2023)
  - **Total Waktu Evaluasi**: 20 HK Pra-registrasi + 120 HK Registrasi = **140 Hari Kerja** (~9 Bulan Kalender)
  - **Rincian Biaya PNBP (PP 32/2017)**:
    - Pra-Registrasi: Rp 1.000.000
    - Registrasi Kategori 1: Rp 100.000.000
    - Penilaian CPOB Luar Negeri (Desk Evaluation): Rp 10.000.000
    - **Total Tarif PNBP**: **Rp 111.000.000**
- **Dokumen Word Dihasilkan**:
  - [Scenario_1_Evaluasi_Produk_Biologi_Impor_ID.docx](outputs/Scenario_1_Evaluasi_Produk_Biologi_Impor_ID.docx)
  - [Scenario_1_Imported_Biologic_Evaluation_EN.docx](outputs/Scenario_1_Imported_Biologic_Evaluation_EN.docx)

---

### Skenario 2: Obat Generik Lokal (Metformin HCl 500mg Tablet)
- **Nama Produk**: Metforin 500 Tablet Salut Selaput
- **Klasifikasi**: Obat Copy / Generik - Produksi Lokal (Cikarang, Jawa Barat)
- **Status Ekivalensi**: Laporan Uji BE in vivo lengkap vs Inovator Glucophage (Merck), validasi proses 3 bets, data stabilitas Zona IVb
- **Hasil Keputusan Jalur BPOM**:
  - **Kategori**: Kategori 4 (Registrasi Obat Copy dengan Uji Bioekivalensi)
  - **Jalur Evaluasi**: Jalur 100 Hari Kerja (Obat Copy dengan Uji BE Terstandar - PerBPOM 24/2017)
  - **Total Waktu Evaluasi**: 20 HK Pra-registrasi + 100 HK Registrasi = **120 Hari Kerja** (~7.7 Bulan Kalender)
  - **Rincian Biaya PNBP (PP 32/2017)**:
    - Pra-Registrasi: Rp 1.000.000
    - Registrasi Kategori 4: Rp 30.000.000
    - **Total Tarif PNBP**: **Rp 31.000.000**
  - **Checklist ACTD**: Bagian III (Non-Klinis) otomatis berstatus **[WAIVED]** sesuai ketentuan obat copy.
- **Dokumen Word Dihasilkan**:
  - [Scenario_2_Evaluasi_Obat_Generik_Lokal_ID.docx](outputs/Scenario_2_Evaluasi_Obat_Generik_Lokal_ID.docx)
  - [Scenario_2_Local_Generic_Evaluation_EN.docx](outputs/Scenario_2_Local_Generic_Evaluation_EN.docx)

---

### Skenario 3: Audit Kesenjangan Dossier (Dossier Gap-Check)
- **Produk Target**: Pemetrexed Disodium 500mg (Dossier Onkologi Impor)
- **Hasil Audit Kepatuhan Regulasi BPOM**:
  - **Status Kesiapan**: **HIGH RISK: Subject to Outright Rejection at Pre-Reg / Evaluation**
  - **Total Temuan**: 8 Temuan Kesenjangan (4 Critical, 3 Major, 1 Minor)
  - **Temuan Kritis (Critical Gaps)**:
    1. `[CRITICAL] GAP-MUTU-01`: Stabilitas hanya diuji pada Zona II (25°C/60% RH); tidak ada data Zona IVb (30°C/75% RH). *Remediasi: Wajib uji Zona IVb min. 6 bulan sebelum submit.*
    2. `[CRITICAL] GAP-ADM-01`: CPP bukan format resmi WHO scheme dan masa berlaku telah kedaluwarsa. *Remediasi: Ajukan CPP WHO scheme terkini.*
    3. `[CRITICAL] GAP-ADM-02`: Pabrik luar negeri belum memiliki Surat Pengakuan CPOB Luar Negeri dari BPOM. *Remediasi: Ajukan penilaian CPOB LN via portal e-CPOB.*
    4. `[CRITICAL] GAP-KLIN-02`: Komparator uji BE yang digunakan adalah komparator luar negeri yang belum diakui BPOM. *Remediasi: Uji kesetaraan komparator atau bridging study.*
  - **Temuan Mayor (Major Gaps)**:
    1. `[MAJOR] GAP-MUTU-04`: Validasi proses komersial 3 bets belum selesai (hanya protokol/skala lab).
    2. `[MAJOR] GAP-KLIN-03`: Laporan Uji Disolusi Terbanding (UDT) 3 pH media belum lengkap.
    3. `[MAJOR] GAP-ADM-03`: Leaflet Pasien (PIL) belum tersedia dalam Bahasa Indonesia.
  - **Temuan Minor (Minor Gap)**:
    1. `[MINOR] GAP-MUTU-03`: Surat komitmen uji stabilitas lanjutan belum dilampirkan.
- **Dokumen Word Dihasilkan**:
  - [Scenario_3_Laporan_Audit_Gap_Check_Dossier_ID.docx](outputs/Scenario_3_Laporan_Audit_Gap_Check_Dossier_ID.docx)
  - [Scenario_3_Dossier_Gap_Check_Audit_Report_EN.docx](outputs/Scenario_3_Dossier_Gap_Check_Audit_Report_EN.docx)
