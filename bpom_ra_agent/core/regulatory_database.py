"""Regulatory Database for BPOM (Badan Pengawas Obat dan Makanan Republik Indonesia).
Contains statutory citations, official PNBP fees (PP No. 32/2017), evaluation timelines,
reliance frameworks (PerBPOM 24/2023), and technical standards (Zone IVb, BE, GMP).
"""

from typing import Dict, Any, List

# Official Citations & Statutes
STATUTES = {
    "REG_REGISTRATION_MAIN": {
        "title": "Peraturan BPOM No. 24 Tahun 2017 tentang Kriteria dan Tata Laksana Registrasi Obat",
        "english_title": "BPOM Regulation No. 24 of 2017 on Criteria and Procedures for Drug Registration",
        "abbreviation": "PerBPOM 24/2017",
        "description": "Foundational regulation governing drug classification, categories, registration pathways, and dossier submission in Indonesia."
    },
    "REG_REGISTRATION_AMENDMENT_1": {
        "title": "Peraturan BPOM No. 13 Tahun 2021 tentang Perubahan atas Peraturan BPOM No. 24 Tahun 2017",
        "english_title": "BPOM Regulation No. 13 of 2021 on Amendment to BPOM Reg 24/2017",
        "abbreviation": "PerBPOM 13/2021",
        "description": "Updated evaluation pathways, electronic registration protocols (AAS/ASROT), and timeline adjustments."
    },
    "REG_REGISTRATION_AMENDMENT_2": {
        "title": "Peraturan BPOM No. 24 Tahun 2023 tentang Perubahan Kedua atas Peraturan BPOM No. 24 Tahun 2017",
        "english_title": "BPOM Regulation No. 24 of 2023 on Second Amendment to BPOM Reg 24/2017",
        "abbreviation": "PerBPOM 24/2023",
        "description": "Introduces reliance evaluation pathways for drugs approved by Stringent Regulatory Authorities (SRA / WHO Listed Authorities)."
    },
    "PNBP_FEES": {
        "title": "Peraturan Pemerintah (PP) No. 32 Tahun 2017 tentang Jenis dan Tarif atas Jenis Penerimaan Negara Bukan Pajak yang Berlaku pada Badan Pengawas Obat dan Makanan",
        "english_title": "Government Regulation No. 32 of 2017 on Types and Tariffs of Non-Tax State Revenue (PNBP) Applicable to BPOM",
        "abbreviation": "PP 32/2017",
        "description": "Official legal tariff for pre-registration, new drug registration, copy/generic registration, variations, and GMP inspections."
    },
    "BIOLOGICS_REGULATION": {
        "title": "Peraturan BPOM No. 15 Tahun 2019 jo. Peraturan BPOM No. 28 Tahun 2022 tentang Registrasi Produk Biologi",
        "english_title": "BPOM Regulation No. 15 of 2019 jo. BPOM Regulation No. 28 of 2022 on Biological Products Registration",
        "abbreviation": "PerBPOM 15/2019 & 28/2022",
        "description": "Requirements for biological originators and biosimilars (similarity exercise, quality characterization, clinical comparability, and pharmacovigilance/RMP)."
    },
    "GMP_REGULATION": {
        "title": "Peraturan BPOM No. 27 Tahun 2020 tentang Penerapan Cara Pembuatan Obat yang Baik (CPOB)",
        "english_title": "BPOM Regulation No. 27 of 2020 on Implementation of Good Manufacturing Practice (GMP)",
        "abbreviation": "PerBPOM 27/2020",
        "description": "Mandates local CPOB compliance and rules for Foreign GMP Desktop Evaluation and On-Site Inspection Recognition."
    },
    "BIOEQUIVALENCE_REGULATION": {
        "title": "Peraturan BPOM No. 11 Tahun 2022 tentang Tata Laksana Uji Bioekivalensi",
        "english_title": "BPOM Regulation No. 11 of 2022 on Procedures for Bioequivalence Studies",
        "abbreviation": "PerBPOM 11/2022",
        "description": "Governs in vivo bioequivalence (BE) trial protocols and criteria for Biopharmaceutics Classification System (BCS) Biowaivers."
    },
    "HALAL_REQUIREMENT": {
        "title": "Undang-Undang No. 33 Tahun 2014 tentang Jaminan Produk Halal jo. UU Cipta Kerja & PP 39/2021",
        "english_title": "Law No. 33 of 2014 on Halal Product Assurance jo. Job Creation Law & PP 39/2021",
        "abbreviation": "UU JPH / PP 39/2021",
        "description": "Mandates disclosure of product origin, animal-derived raw materials, and Halal certification or non-halal warning information."
    }
}

# Official PNBP Fees under PP No. 32 Tahun 2017 (in IDR)
FEES_PNBP_PP32_2017 = {
    # Pre-registration (Pra-registrasi)
    "PRE_REGISTRATION": {
        "amount_idr": 1000000,
        "code": "PP32-PR01",
        "name_id": "Pra-Registrasi (Semua Kategori Obat Baru, Biologi, dan Copy)",
        "name_en": "Pre-Registration (All Categories: New Drug, Biologic, and Generic Copy)",
        "basis": "PP 32/2017 Lampiran I.A"
    },
    # Category 1: New Chemical Entity (NCE) / Novel Active / Novel Biologic / Biosimilar
    "CATEGORY_1": {
        "amount_idr": 100000000,
        "code": "PP32-REG01",
        "name_id": "Registrasi Baru Kategori 1 (Zat Aktif Baru / Produk Biologi Baru / Biosimilar)",
        "name_en": "New Registration Category 1 (New Active Substance / Novel Biologic / Biosimilar)",
        "basis": "PP 32/2017 Lampiran I.B.1.a"
    },
    # Category 2: New Indication / Posology
    "CATEGORY_2": {
        "amount_idr": 75000000,
        "code": "PP32-REG02",
        "name_id": "Registrasi Baru Kategori 2 (Indikasi Baru / Posologi Baru)",
        "name_en": "New Registration Category 2 (New Indication / New Posology)",
        "basis": "PP 32/2017 Lampiran I.B.1.b"
    },
    # Category 3: New Dosage Form / Route of Admin / Strength
    "CATEGORY_3": {
        "amount_idr": 50000000,
        "code": "PP32-REG03",
        "name_id": "Registrasi Baru Kategori 3 (Bentuk Sediaan Baru / Rute Pemberian Baru / Kekuatan Baru)",
        "name_en": "New Registration Category 3 (New Dosage Form / Route of Administration / New Strength)",
        "basis": "PP 32/2017 Lampiran I.B.1.c"
    },
    # Category 4: Generic Copy Drug (with Bioequivalence Study / In Vitro Equivalence)
    "CATEGORY_4": {
        "amount_idr": 30000000,
        "code": "PP32-REG04",
        "name_id": "Registrasi Kategori 4 (Obat Copy dengan Uji Ekivalensi / Uji BE)",
        "name_en": "Registration Category 4 (Copy/Generic Drug with Bioequivalence Study / Equivalence)",
        "basis": "PP 32/2017 Lampiran I.B.2.a"
    },
    # Category 5: Generic Copy Drug (Standard without in vivo BE requirement / BCS waiver)
    "CATEGORY_5": {
        "amount_idr": 20000000,
        "code": "PP32-REG05",
        "name_id": "Registrasi Kategori 5 (Obat Copy tanpa Uji Bioekivalensi In Vivo / Perubahan Tertentu)",
        "name_en": "Registration Category 5 (Copy/Generic Drug without in vivo BE / Standard Formulations)",
        "basis": "PP 32/2017 Lampiran I.B.2.b"
    },
    # Category 6: Copy Drug with other changes / presentations
    "CATEGORY_6": {
        "amount_idr": 15000000,
        "code": "PP32-REG06",
        "name_id": "Registrasi Kategori 6 (Obat Copy dengan Perubahan Kemasan/Presentasi Tertentu)",
        "name_en": "Registration Category 6 (Copy Drug with specific packaging/presentation variants)",
        "basis": "PP 32/2017 Lampiran I.B.2.c"
    },
    # Variations
    "VARIATION_MAJOR": {
        "amount_idr": 10000000,
        "code": "PP32-VAR01",
        "name_id": "Registrasi Variasi Mayor (VaMa)",
        "name_en": "Major Variation Registration (VaMa)",
        "basis": "PP 32/2017 Lampiran I.C.1"
    },
    "VARIATION_MINOR_APPROVAL": {
        "amount_idr": 5000000,
        "code": "PP32-VAR02",
        "name_id": "Registrasi Variasi Minor dengan Persetujuan (VaMi-B)",
        "name_en": "Minor Variation Requiring Approval (VaMi-B)",
        "basis": "PP 32/2017 Lampiran I.C.2"
    },
    "VARIATION_MINOR_NOTIFICATION": {
        "amount_idr": 1000000,
        "code": "PP32-VAR03",
        "name_id": "Registrasi Variasi Minor dengan Notifikasi (VaMi-A)",
        "name_en": "Minor Variation by Notification (VaMi-A)",
        "basis": "PP 32/2017 Lampiran I.C.3"
    },
    # Foreign GMP Assessment Fees
    "FOREIGN_GMP_DESKTOP": {
        "amount_idr": 10000000,
        "code": "PP32-GMP01",
        "name_id": "Penilaian Dokumen Pemenuhan CPOB Fasilitas Luar Negeri (Desk Evaluation)",
        "name_en": "Document Assessment of Foreign GMP Compliance (Desk Evaluation)",
        "basis": "PP 32/2017 Lampiran II.A"
    },
    "FOREIGN_GMP_ONSITE": {
        "amount_idr": 50000000,
        "code": "PP32-GMP02",
        "name_id": "Inspeksi Fasilitas CPOB Luar Negeri (Di Luar Biaya Transportasi & Akomodasi)",
        "name_en": "On-Site Inspection of Foreign GMP Facility (Excludes travel & lodging costs)",
        "basis": "PP 32/2017 Lampiran II.B"
    }
}

# Evaluation Timelines (in Working Days / Hari Kerja - HK)
TIMELINES_HK = {
    "PRE_REGISTRATION": {
        "days": 20,
        "description_id": "Evaluasi Dokumen Pra-Registrasi dan penerbitan Surat Hasil Pra-Registrasi (SHPR)",
        "description_en": "Pre-Registration Document Evaluation & issuance of Pre-Registration Result Letter (SHPR)",
        "basis": "PerBPOM 24/2017 Pasal 21"
    },
    "JALUR_40_HK": {
        "days": 40,
        "description_id": "Jalur Khusus 40 Hari Kerja: Obat program kesehatan nasional, obat penanganan wabah/darurat, atau obat khusus ekspor.",
        "description_en": "Special 40-Working-Day Track: National public health priority, epidemic/emergency countermeasures, or dedicated export products.",
        "basis": "PerBPOM 24/2017 Pasal 27 ayat (1)"
    },
    "JALUR_100_HK": {
        "days": 100,
        "description_id": "Jalur 100 Hari Kerja: Obat Baru / Produk Biologi melalui mekanisme Reliance (telah disetujui di minimal 1 SRA terpercaya), atau Obat Copy dengan Uji BE terstandar / BCS biowaiver.",
        "description_en": "100-Working-Day Track: New Drugs / Biologics via Reliance (approved by >= 1 trusted SRA/WHO Listed Authority), or Standard Generic Copies with validated BE/BCS biowaiver.",
        "basis": "PerBPOM 24/2017 Pasal 27 ayat (2) jo. PerBPOM 24/2023"
    },
    "JALUR_120_HK": {
        "days": 120,
        "description_id": "Jalur 120 Hari Kerja: Produk Biologi Biosimilar yang telah disetujui oleh SRA dengan data komparabilitas lengkap melalui jalur reliance parsial.",
        "description_en": "120-Working-Day Track: Biosimilar biologics approved by an SRA with complete comparability data under partial reliance.",
        "basis": "PerBPOM 24/2023 Pasal 28"
    },
    "JALUR_150_HK": {
        "days": 150,
        "description_id": "Jalur 150 Hari Kerja: Obat Baru / Produk Biologi Kategori 2 dan 3, atau Obat Copy formulasi khusus yang memerlukan evaluasi data mutu dan klinik komparatif.",
        "description_en": "150-Working-Day Track: Category 2 & 3 New Drugs/Biologics, or Complex Generics requiring specialized quality and comparative clinical assessment.",
        "basis": "PerBPOM 24/2017 Pasal 27 ayat (3)"
    },
    "JALUR_300_HK": {
        "days": 300,
        "description_id": "Jalur 300 Hari Kerja: Evaluasi Lengkap (Full Evaluation) untuk Zat Aktif Baru (NCE) atau Produk Biologi Baru yang belum pernah disetujui oleh SRA, dinilai melalui sidang Komite Nasional (KOMNAS) Penilai Obat.",
        "description_en": "300-Working-Day Track: Full Evaluation for New Chemical Entities (NCE) or Novel Biologics without prior SRA authorization, requiring full Komnas Penilai Obat review.",
        "basis": "PerBPOM 24/2017 Pasal 27 ayat (4)"
    }
}

# Recognized Stringent Regulatory Authorities (SRA / WHO Listed Authorities for Reliance)
RECOGNIZED_SRAS = [
    {"country": "United States", "agency": "US FDA (Food and Drug Administration)"},
    {"country": "European Union", "agency": "EMA (European Medicines Agency)"},
    {"country": "Japan", "agency": "PMDA / MHLW (Pharmaceuticals and Medical Devices Agency)"},
    {"country": "Switzerland", "agency": "Swissmedic"},
    {"country": "United Kingdom", "agency": "MHRA (Medicines and Healthcare products Regulatory Agency)"},
    {"country": "Australia", "agency": "TGA (Therapeutic Goods Administration)"},
    {"country": "Canada", "agency": "Health Canada"},
    {"country": "Singapore", "agency": "HSA (Health Sciences Authority) - under ASEAN / WHO maturity Level 4"}
]

# Climatic Zone IVb Technical Specifications
CLIMATIC_ZONE_IVB = {
    "zone": "Zone IVb (Hot & Very Humid)",
    "target_territory": "ASEAN / Indonesia",
    "real_time_condition": "30°C ± 2°C / 75% ± 5% RH",
    "accelerated_condition": "40°C ± 2°C / 75% ± 5% RH",
    "minimum_submission_data": "Minimum 6 months real-time and 6 months accelerated at time of dossier submission (12 months real-time preferred/mandatory for biologicals)",
    "commitment": "Mandatory written commitment to continue real-time stability to the full claimed shelf-life (e.g. 24, 36, or 60 months) under Zone IVb."
}
