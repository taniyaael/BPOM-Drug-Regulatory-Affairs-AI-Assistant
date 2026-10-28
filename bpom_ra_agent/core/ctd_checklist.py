"""ACTD / ICH CTD Checklist Engine for BPOM Drug Registration.
Generates comprehensive, module-by-module compliance checklists (Part I to IV)
with dynamic applicability triggers based on drug classification and origin.
"""

from typing import Dict, Any, List

class CTDModuleItem:
    def __init__(self, section_id: str, title_id: str, title_en: str,
                 mandatory_for: List[str], waived_for: List[str],
                 bpom_specific_notes_id: str, bpom_specific_notes_en: str):
        self.section_id = section_id
        self.title_id = title_id
        self.title_en = title_en
        self.mandatory_for = mandatory_for
        self.waived_for = waived_for
        self.bpom_specific_notes_id = bpom_specific_notes_id
        self.bpom_specific_notes_en = bpom_specific_notes_en

    def is_applicable(self, product_type: str) -> bool:
        if "ALL" in self.mandatory_for:
            if product_type in self.waived_for:
                return False
            return True
        return product_type in self.mandatory_for

def get_bpom_actd_checklist(product_type: str, origin: str) -> Dict[str, Any]:
    """Builds a contextualized ACTD checklist customized for BPOM submission."""
    
    # Define complete ACTD inventory
    items_part_1 = [
        {
            "code": "1.1",
            "title_id": "Surat Pengantar Permohonan Registrasi",
            "title_en": "Registration Application Cover Letter",
            "required": True,
            "notes_id": "Ditandatangani oleh Apoteker Penanggung Jawab (PJT) / Direktur Industri Farmasi pendaftar.",
            "notes_en": "Signed by Pharmacist-in-Charge (PJT) / Regulatory Director of the applicant company."
        },
        {
            "code": "1.2",
            "title_id": "Formulir Registrasi Obat & Bukti Pengajuan Elektronik",
            "title_en": "Drug Registration Application Form & E-Submission Receipt",
            "required": True,
            "notes_id": "Diisi lengkap melalui portal ASROT / New AeS BPOM RI beserta dokumen pra-registrasi.",
            "notes_en": "Completed via BPOM ASROT / New AeS portal including pre-registration dossiers."
        },
        {
            "code": "1.3",
            "title_id": "Surat Pernyataan Pendaftar (Komitmen Dokumen & Paten)",
            "title_en": "Applicant Commitment Letter (Authenticity & Patent Declaration)",
            "required": True,
            "notes_id": "Format baku BPOM bermaterai cukup; pernyataan keabsahan dokumen dan tidak melanggar paten.",
            "notes_en": "BPOM standard format with duty stamp; affirming dossier authenticity and non-infringement of patents."
        },
        {
            "code": "1.4",
            "title_id": "Sertifikat Izin Industri Farmasi Pendaftar",
            "title_en": "Applicant Pharmaceutical Industry License",
            "required": True,
            "notes_id": "Izin Industri Farmasi aktif yang diterbitkan oleh Kementerian Kesehatan RI / OSS-RBA.",
            "notes_en": "Active Pharma License issued by Ministry of Health RI / OSS-RBA system."
        },
        {
            "code": "1.5",
            "title_id": "Dokumen Sertifikasi CPOB (GMP) Fasilitas Produksi",
            "title_en": "GMP Certification Documents of Manufacturing Site",
            "required": True,
            "notes_id": "Untuk lokal: Sertifikat CPOB aktif BPOM untuk lini sediaan terkait. Untuk impor: Sertifikat CPOB negara asal + Surat Pengakuan Pemenuhan Standar CPOB dari BPOM RI.",
            "notes_en": "Local: Active BPOM GMP cert for relevant dosage line. Imported: Origin GMP cert + BPOM Foreign GMP Recognition Letter."
        },
        {
            "code": "1.6",
            "title_id": "Certificate of Pharmaceutical Product (CPP) Format WHO",
            "title_en": "Certificate of Pharmaceutical Product (CPP) - WHO Format",
            "required": (origin == "IMPORTED"),
            "notes_id": "Wajib untuk obat impor. Diterbitkan oleh Badan Otoritas Regulasi Negara Pengekspor sesuai standar WHO.",
            "notes_en": "Mandatory for imported drugs. Issued by National Regulatory Authority of exporting country under WHO format."
        },
        {
            "code": "1.7",
            "title_id": "Surat Kuasa / Letter of Authorization (LoA) & Kontrak Lisensi",
            "title_en": "Letter of Authorization (LoA) & License Agreement",
            "required": (origin == "IMPORTED"),
            "notes_id": "Surat penunjukan resmi dari pemilik produk/prinsipal di luar negeri kepada pendaftar di Indonesia.",
            "notes_en": "Official authorization letter from foreign principal to local applicant in Indonesia (notarized & apostilled/legalized)."
        },
        {
            "code": "1.8",
            "title_id": "Ringkasan Karakteristik Produk (SmPC / Leaflet Informasi Obat)",
            "title_en": "Summary of Product Characteristics (SmPC / Prescribing Information)",
            "required": True,
            "notes_id": "Mengacu pada format BPOM RI; mencantumkan indikasi, posologi, kontraindikasi, efek samping, dan peringatan.",
            "notes_en": "BPOM compliant format; detailing indications, posology, contraindications, adverse reactions, and warnings."
        },
        {
            "code": "1.9",
            "title_id": "Informasi Produk untuk Pasien (Brosur / PIL) Bahasa Indonesia",
            "title_en": "Patient Information Leaflet (PIL) in Bahasa Indonesia",
            "required": True,
            "notes_id": "Wajib dalam Bahasa Indonesia dengan bahasa yang mudah dipahami oleh pasien/konsumen.",
            "notes_en": "Mandatory in Bahasa Indonesia, structured for lay clarity per BPOM labeling guidelines."
        },
        {
            "code": "1.10",
            "title_id": "Rancangan Kemasan (Label, Etiket, Blister, Dus / Carton Mockup)",
            "title_en": "Packaging Design (Label, Foil/Blister, Outer Carton Mockups)",
            "required": True,
            "notes_id": "Memenuhi regulasi penandaan BPOM: logo lingkaran obat keras/bebas, peringatan DOT, NIE mockup, QR code placeholder.",
            "notes_en": "Strict BPOM labeling compliance: Rx red circle symbol, black warning boxes, registration number placeholder, 2D barcode."
        },
        {
            "code": "1.11",
            "title_id": "Pernyataan Jaminan Produk Halal & Asal Bahan Baku",
            "title_en": "Halal Product Assurance & Raw Material Origin Declaration",
            "required": True,
            "notes_id": "Surat pernyataan asal bahan baku (porcine/non-porcine statement) dan sertifikat halal jika mencantumkan logo Halal.",
            "notes_en": "Official declaration regarding animal origin (porcine-free/porcine trace) and Halal certificate if Halal claim is made."
        },
        {
            "code": "1.12",
            "title_id": "Bukti Setor Penerimaan Negara Bukan Pajak (PNBP SIMPONI)",
            "title_en": "Non-Tax State Revenue (PNBP SIMPONI) Payment Receipt",
            "required": True,
            "notes_id": "Surat Setoran Bukan Pajak (SSBP) / bukti bayar billing SIMPONI pra-registrasi dan registrasi.",
            "notes_en": "Official e-receipt from SIMPONI / Ministry of Finance portal for pre-reg and registration fees."
        }
    ]

    items_part_2 = [
        {
            "code": "2.1",
            "title_id": "Ringkasan Dokumen Mutu (Quality Overall Summary - QOS)",
            "title_en": "Quality Overall Summary (QOS - ACTD Part II Section A)",
            "required": True,
            "notes_id": "Rangkuman komprehensif data mutu zat aktif (S) dan produk jadi (P).",
            "notes_en": "Comprehensive narrative summary of Drug Substance (S) and Drug Product (P)."
        },
        {
            "code": "2.2",
            "title_id": "Zat Aktif (Drug Substance / Active Pharmaceutical Ingredient - S)",
            "title_en": "Drug Substance / Active Pharmaceutical Ingredient (S.1 - S.7)",
            "required": True,
            "notes_id": "S.1 Nomenklatur, S.2 Proses Sintesis & Kontrol Bahan, S.3 Karakterisasi & Impuritas (Nitrosamin & Logam Berat), S.4 Spesifikasi & Validasi Metode Analisis, S.5 Baku Pembanding, S.6 Kemasan Wadah, S.7 Stabilitas Zat Aktif.",
            "notes_en": "S.1 Nomenclature, S.2 Synthesis & In-process Controls, S.3 Impurity Profile (Nitrosamines & Elemental Impurities), S.4 Specs & Analytical Validation, S.5 Reference Standards, S.6 Container, S.7 Stability."
        },
        {
            "code": "2.3",
            "title_id": "Produk Jadi (Drug Product - P.1 s/d P.7)",
            "title_en": "Drug Product (P.1 - P.7: Formulation & Manufacturing Process)",
            "required": True,
            "notes_id": "P.1 Pemerian & Formula, P.2 Pengembangan Farmasetika, P.3 Prosedur Pembuatan & Laporan Validasi Proses 3 Batch Komersial, P.4 Kontrol Eksipien, P.5 Spesifikasi Rilis/Kedaluwarsa & Hasil Analisis 3 Batch, P.6 Baku Pembanding, P.7 Kemasan Primer/Sekunder.",
            "notes_en": "P.1 Description & Formula, P.2 Pharmaceutical Development, P.3 Manufacturing Process & 3-Commercial-Batch Process Validation Report, P.4 Excipient Controls, P.5 Release/Shelf-Life Specs & CoA of 3 Batches, P.6 Ref Standard, P.7 Container System."
        },
        {
            "code": "2.4",
            "title_id": "Stabilitas Produk Jadi Kondisi Zona Iklim IVb (P.8)",
            "title_en": "Drug Product Stability Data - Climatic Zone IVb (P.8)",
            "required": True,
            "notes_id": "Wajib data stabilitas kondisi Zona IVb (30°C ± 2°C / 75% ± 5% RH) minimal 6 bulan real-time & 6 bulan accelerated (40°C/75% RH) saat pengajuan, disertai surat komitmen uji stabilitas hingga batas kedaluwarsa.",
            "notes_en": "Mandatory Zone IVb data (30°C ± 2°C / 75% ± 5% RH) min. 6 months real-time & accelerated data at submission, with formal commitment letter for ongoing real-time studies."
        }
    ]

    # Part III: Non-Clinical
    is_non_clinical_waived = (product_type == "GENERIC")
    items_part_3 = [
        {
            "code": "3.1",
            "title_id": "Ringkasan Non-Klinis (Nonclinical Overview & Written Summaries)",
            "title_en": "Nonclinical Overview & Written Summaries (ACTD Part III Section A)",
            "required": not is_non_clinical_waived,
            "notes_id": "Dikecualikan (Waived) untuk Obat Generik/Copy. Wajib untuk Obat Baru (NCE) dan Produk Biologi.",
            "notes_en": "Waived for Generic/Copy drugs. Mandatory for NCE and Biological Products."
        },
        {
            "code": "3.2",
            "title_id": "Laporan Studi Farmakodinamika & Farmakokinetika Non-Klinis",
            "title_en": "Non-Clinical Pharmacodynamics & Pharmacokinetics Reports",
            "required": not is_non_clinical_waived,
            "notes_id": "Dikecualikan untuk Obat Copy. Untuk biosimilar: studi komparatif in vitro / in vivo binding & mechanism of action.",
            "notes_en": "Waived for Generics. For biosimilars: comparative in vitro / in vivo binding and functional assays."
        },
        {
            "code": "3.3",
            "title_id": "Laporan Toksikologi (Single/Repeat Dose, Genotoxicity, Carcinogenicity)",
            "title_en": "Toxicology Reports (Single/Repeat Dose, Genotoxicity, Carcinogenicity)",
            "required": not is_non_clinical_waived,
            "notes_id": "Dikecualikan untuk Obat Generik. Wajib GLP-compliant untuk NCE / Produk Biologi.",
            "notes_en": "Waived for Generics. Must be GLP-compliant for NCE / Novel Biologics."
        }
    ]

    # Part IV: Clinical
    items_part_4 = [
        {
            "code": "4.1",
            "title_id": "Ringkasan Klinis (Clinical Overview & Clinical Summary)",
            "title_en": "Clinical Overview & Clinical Summary (ACTD Part IV Section A)",
            "required": True,
            "notes_id": "Rangkuman efikasi dan keamanan klinis. Untuk generik: tinjauan bioekivalensi.",
            "notes_en": "Synthesis of clinical efficacy and safety. For generics: overview of bioequivalence evidence."
        },
        {
            "code": "4.2",
            "title_id": "Laporan Uji Bioekivalensi (BE) ATAU Justifikasi Biowaiver BCS",
            "title_en": "Bioequivalence (BE) Study Report OR BCS Biowaiver Justification",
            "required": (product_type == "GENERIC"),
            "notes_id": "Untuk Obat Copy: Wajib laporan uji BE in vivo terhadap obat komparator resmi BPOM, atau justifikasi permohonan biowaiver BCS (Kelas 1 atau 3) sesuai PerBPOM 11/2022.",
            "notes_en": "For Generic Copy: In vivo BE report against BPOM designated Indonesian comparator product, or formal BCS Biowaiver Dossier (Class 1 or 3) per PerBPOM 11/2022."
        },
        {
            "code": "4.3",
            "title_id": "Laporan Uji Disolusi Terbanding (UDT / In Vitro Equivalence)",
            "title_en": "Comparative Dissolution Profile (In Vitro Equivalence Report)",
            "required": (product_type == "GENERIC"),
            "notes_id": "Uji disolusi komparatif pada 3 pH media (pH 1.2, pH 4.5, pH 6.8) dengan nilai f2 similarity factor >= 50.",
            "notes_en": "Comparative dissolution across 3 buffer media (pH 1.2, pH 4.5, pH 6.8) showing f2 similarity score >= 50."
        },
        {
            "code": "4.4",
            "title_id": "Laporan Uji Klinis Efikasi & Keamanan (Fase I - III)",
            "title_en": "Clinical Efficacy & Safety Trial Reports (Phase I - III)",
            "required": (product_type in ["NCE", "BIOLOGIC_NOVEL", "BIOSIMILAR", "NEW_INDICATION"]),
            "notes_id": "Untuk Produk Biologi / Biosimilar: uji klinis komparatif PK/PD dan studi kemanjuran klinis fase 3 komparatif.",
            "notes_en": "For Biologics / Biosimilars: Head-to-head clinical PK/PD comparability and Phase 3 clinical equivalence/non-inferiority trials."
        },
        {
            "code": "4.5",
            "title_id": "Rencana Manajemen Risiko (Risk Management Plan - RMP) & Farmakovigilans",
            "title_en": "Risk Management Plan (RMP) & Pharmacovigilance System",
            "required": (product_type in ["NCE", "BIOLOGIC_NOVEL", "BIOSIMILAR"]),
            "notes_id": "Wajib untuk semua Produk Biologi dan NCE; mencakup sistem pelaporan MESO / ESO dan identifikasi risiko keamanan di Indonesia.",
            "notes_en": "Mandatory for all Biologics and NCEs; detailing pharmacovigilance mechanisms, adverse reaction monitoring, and local safety surveillance."
        },
        {
            "code": "4.6",
            "title_id": "Periodic Safety Update Report (PSUR / PBRER) Terkini",
            "title_en": "Periodic Safety Update Report (PSUR / PBRER) - Latest Periodic Report",
            "required": (product_type in ["NCE", "BIOLOGIC_NOVEL", "BIOSIMILAR"] and origin == "IMPORTED"),
            "notes_id": "Laporan pemantauan keamanan pasca-pemasaran berkala dari negara-negara tempat produk telah dipasarkan.",
            "notes_en": "Worldwide post-marketing cumulative safety experience from all countries where the product is currently licensed."
        }
    ]

    return {
        "Part_I_Administrative": items_part_1,
        "Part_II_Quality": items_part_2,
        "Part_III_NonClinical": items_part_3,
        "Part_IV_Clinical": items_part_4,
        "is_non_clinical_waived": is_non_clinical_waived
    }
