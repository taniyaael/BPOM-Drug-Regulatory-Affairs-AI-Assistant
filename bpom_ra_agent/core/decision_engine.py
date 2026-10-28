"""Pathway Decision Engine for BPOM Drug Registration.
Determines exact Registration Category (Kategori 1-7), Evaluation Pathway (Jalur 40/100/120/150/300 HK),
PNBP Fees (PP 32/2017), and technical requirements in English and Bahasa Indonesia.
"""

from typing import Dict, Any, List, Optional
from bpom_ra_agent.core.regulatory_database import (
    STATUTES, FEES_PNBP_PP32_2017, TIMELINES_HK, RECOGNIZED_SRAS, CLIMATIC_ZONE_IVB
)

class RegistrationAssessment:
    """Stores the complete evaluation results from the Decision Engine."""
    def __init__(self, data: Dict[str, Any]):
        self.raw_data = data
        self.category_code = data["category_code"]
        self.category_name_id = data["category_name_id"]
        self.category_name_en = data["category_name_en"]
        self.category_basis = data["category_basis"]
        
        self.track_code = data["track_code"]
        self.track_name_id = data["track_name_id"]
        self.track_name_en = data["track_name_en"]
        self.timeline_days_hk = data["timeline_days_hk"]
        self.prereg_days_hk = data["prereg_days_hk"]
        self.total_working_days = data["total_working_days"]
        self.estimated_calendar_months = data["estimated_calendar_months"]
        self.track_basis = data["track_basis"]
        
        self.fees = data["fees"]
        self.total_fee_idr = data["total_fee_idr"]
        
        self.reliance_applicable = data["reliance_applicable"]
        self.reliance_details = data["reliance_details"]
        
        self.key_requirements_id = data["key_requirements_id"]
        self.key_requirements_en = data["key_requirements_en"]
        self.risk_factors = data["risk_factors"]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category_code": self.category_code,
            "category_name_id": self.category_name_id,
            "category_name_en": self.category_name_en,
            "category_basis": self.category_basis,
            "track_code": self.track_code,
            "track_name_id": self.track_name_id,
            "track_name_en": self.track_name_en,
            "timeline_days_hk": self.timeline_days_hk,
            "prereg_days_hk": self.prereg_days_hk,
            "total_working_days": self.total_working_days,
            "estimated_calendar_months": self.estimated_calendar_months,
            "track_basis": self.track_basis,
            "fees": self.fees,
            "total_fee_idr": self.total_fee_idr,
            "reliance_applicable": self.reliance_applicable,
            "reliance_details": self.reliance_details,
            "key_requirements_id": self.key_requirements_id,
            "key_requirements_en": self.key_requirements_en,
            "risk_factors": self.risk_factors
        }


class PathwayDecisionEngine:
    """Rule-based decision logic matching Indonesian BPOM registration guidelines."""

    @staticmethod
    def evaluate(product: Dict[str, Any]) -> RegistrationAssessment:
        """Evaluate product dossier profile and return regulatory determination."""
        product_type = product.get("product_type", "GENERIC").upper()
        origin = product.get("origin", "LOCAL").upper()
        is_sra_approved = product.get("is_sra_approved", False)
        sra_countries = product.get("sra_countries", [])
        is_public_health_emergency = product.get("is_public_health_emergency", False)
        be_study_available = product.get("be_study_available", False)
        bcs_class = product.get("bcs_class", None)
        foreign_gmp_status = product.get("foreign_gmp_status", "LOCAL_CPOB").upper()
        variation_type = product.get("variation_type", None)
        
        # 1. Determine Category (Kategori 1 - 7)
        fees: List[Dict[str, Any]] = []
        
        # Always includes Pre-Registration fee
        fees.append({
            "component": "Pre-Registration (Pra-Registrasi)",
            "code": FEES_PNBP_PP32_2017["PRE_REGISTRATION"]["code"],
            "amount_idr": FEES_PNBP_PP32_2017["PRE_REGISTRATION"]["amount_idr"],
            "basis": FEES_PNBP_PP32_2017["PRE_REGISTRATION"]["basis"]
        })

        if variation_type:
            category_code = "KATEGORI_7"
            category_name_id = "Kategori 7: Registrasi Variasi"
            category_name_en = "Category 7: Variation Registration"
            category_basis = "PerBPOM No. 24 Tahun 2017 Pasal 15"
            if variation_type == "MAJOR":
                fee_item = FEES_PNBP_PP32_2017["VARIATION_MAJOR"]
            elif variation_type == "MINOR_APPROVAL":
                fee_item = FEES_PNBP_PP32_2017["VARIATION_MINOR_APPROVAL"]
            else:
                fee_item = FEES_PNBP_PP32_2017["VARIATION_MINOR_NOTIFICATION"]
            fees.append({
                "component": fee_item["name_en"],
                "code": fee_item["code"],
                "amount_idr": fee_item["amount_idr"],
                "basis": fee_item["basis"]
            })
        elif product_type in ["NCE", "BIOLOGIC_NOVEL", "BIOSIMILAR"]:
            category_code = "KATEGORI_1"
            category_name_id = "Kategori 1: Registrasi Baru (Zat Aktif Baru / Produk Biologi / Biosimilar)"
            category_name_en = "Category 1: New Registration (New Chemical Entity / Novel Biologic / Biosimilar)"
            category_basis = "PerBPOM No. 24/2017 Pasal 9 ayat (1) jo. PerBPOM 15/2019"
            fees.append({
                "component": FEES_PNBP_PP32_2017["CATEGORY_1"]["name_en"],
                "code": FEES_PNBP_PP32_2017["CATEGORY_1"]["code"],
                "amount_idr": FEES_PNBP_PP32_2017["CATEGORY_1"]["amount_idr"],
                "basis": FEES_PNBP_PP32_2017["CATEGORY_1"]["basis"]
            })
        elif product_type == "NEW_INDICATION":
            category_code = "KATEGORI_2"
            category_name_id = "Kategori 2: Registrasi Baru (Indikasi Baru / Posologi Baru)"
            category_name_en = "Category 2: New Registration (New Indication / New Posology)"
            category_basis = "PerBPOM No. 24/2017 Pasal 10"
            fees.append({
                "component": FEES_PNBP_PP32_2017["CATEGORY_2"]["name_en"],
                "code": FEES_PNBP_PP32_2017["CATEGORY_2"]["code"],
                "amount_idr": FEES_PNBP_PP32_2017["CATEGORY_2"]["amount_idr"],
                "basis": FEES_PNBP_PP32_2017["CATEGORY_2"]["basis"]
            })
        elif product_type == "NEW_FORM_STRENGTH":
            category_code = "KATEGORI_3"
            category_name_id = "Kategori 3: Registrasi Baru (Bentuk Sediaan Baru / Rute Baru / Kekuatan Baru)"
            category_name_en = "Category 3: New Registration (New Dosage Form / Route / Strength)"
            category_basis = "PerBPOM No. 24/2017 Pasal 11"
            fees.append({
                "component": FEES_PNBP_PP32_2017["CATEGORY_3"]["name_en"],
                "code": FEES_PNBP_PP32_2017["CATEGORY_3"]["code"],
                "amount_idr": FEES_PNBP_PP32_2017["CATEGORY_3"]["amount_idr"],
                "basis": FEES_PNBP_PP32_2017["CATEGORY_3"]["basis"]
            })
        elif product_type == "GENERIC":
            if be_study_available or (bcs_class in [1, 3]):
                category_code = "KATEGORI_4"
                category_name_id = "Kategori 4: Registrasi Obat Copy (dengan Uji Bioekivalensi / Biowaiver BCS)"
                category_name_en = "Category 4: Copy/Generic Registration (with Bioequivalence Study / BCS Biowaiver)"
                category_basis = "PerBPOM No. 24/2017 Pasal 12 jo. PerBPOM 11/2022"
                fees.append({
                    "component": FEES_PNBP_PP32_2017["CATEGORY_4"]["name_en"],
                    "code": FEES_PNBP_PP32_2017["CATEGORY_4"]["code"],
                    "amount_idr": FEES_PNBP_PP32_2017["CATEGORY_4"]["amount_idr"],
                    "basis": FEES_PNBP_PP32_2017["CATEGORY_4"]["basis"]
                })
            else:
                category_code = "KATEGORI_5"
                category_name_id = "Kategori 5: Registrasi Obat Copy (tanpa Uji BE in vivo / Uji Disolusi Terbanding)"
                category_name_en = "Category 5: Copy Drug Registration (Standard / In Vitro Dissolution Equivalence)"
                category_basis = "PerBPOM No. 24/2017 Pasal 13"
                fees.append({
                    "component": FEES_PNBP_PP32_2017["CATEGORY_5"]["name_en"],
                    "code": FEES_PNBP_PP32_2017["CATEGORY_5"]["code"],
                    "amount_idr": FEES_PNBP_PP32_2017["CATEGORY_5"]["amount_idr"],
                    "basis": FEES_PNBP_PP32_2017["CATEGORY_5"]["basis"]
                })
        else:
            category_code = "KATEGORI_1"
            category_name_id = "Kategori 1: Registrasi Baru"
            category_name_en = "Category 1: New Registration"
            category_basis = "PerBPOM No. 24/2017"
            fees.append({
                "component": FEES_PNBP_PP32_2017["CATEGORY_1"]["name_en"],
                "code": FEES_PNBP_PP32_2017["CATEGORY_1"]["code"],
                "amount_idr": FEES_PNBP_PP32_2017["CATEGORY_1"]["amount_idr"],
                "basis": FEES_PNBP_PP32_2017["CATEGORY_1"]["basis"]
            })

        # Check Foreign GMP fees for imported drugs
        if origin == "IMPORTED":
            if foreign_gmp_status == "DESK_EVALUATION_NEEDED":
                fees.append({
                    "component": FEES_PNBP_PP32_2017["FOREIGN_GMP_DESKTOP"]["name_en"],
                    "code": FEES_PNBP_PP32_2017["FOREIGN_GMP_DESKTOP"]["code"],
                    "amount_idr": FEES_PNBP_PP32_2017["FOREIGN_GMP_DESKTOP"]["amount_idr"],
                    "basis": FEES_PNBP_PP32_2017["FOREIGN_GMP_DESKTOP"]["basis"]
                })
            elif foreign_gmp_status == "ONSITE_INSPECTION_NEEDED":
                fees.append({
                    "component": FEES_PNBP_PP32_2017["FOREIGN_GMP_ONSITE"]["name_en"],
                    "code": FEES_PNBP_PP32_2017["FOREIGN_GMP_ONSITE"]["code"],
                    "amount_idr": FEES_PNBP_PP32_2017["FOREIGN_GMP_ONSITE"]["amount_idr"],
                    "basis": FEES_PNBP_PP32_2017["FOREIGN_GMP_ONSITE"]["basis"]
                })

        total_fee_idr = sum(item["amount_idr"] for item in fees)

        # 2. Determine Timeline Track (Jalur Evaluasi)
        reliance_applicable = False
        reliance_details = ""
        prereg_days_hk = TIMELINES_HK["PRE_REGISTRATION"]["days"]

        if is_public_health_emergency:
            track_code = "JALUR_40_HK"
            track_name_id = "Jalur Khusus 40 Hari Kerja (Program Prioritas / Kedaruratan Kesehatan)"
            track_name_en = "Priority 40 Working Days Track (Public Health Emergency / Priority Program)"
            timeline_days_hk = 40
            track_basis = "PerBPOM No. 24/2017 Pasal 27 ayat (1)"
        elif product_type in ["NCE", "BIOLOGIC_NOVEL", "BIOSIMILAR"] and is_sra_approved:
            reliance_applicable = True
            reliance_details = f"Approved by SRA: {', '.join(sra_countries) if sra_countries else 'Stringent Regulatory Authority'}. Qualified for Reliance Evaluation under PerBPOM 24/2023."
            if product_type == "BIOSIMILAR":
                track_code = "JALUR_120_HK"
                track_name_id = "Jalur 120 Hari Kerja (Biosimilar Terdaftar SRA dengan Reliance Parsial)"
                track_name_en = "120 Working Days Track (Biosimilar Approved by SRA via Partial Reliance)"
                timeline_days_hk = 120
                track_basis = "PerBPOM No. 24/2023 Pasal 28 jo. PerBPOM 15/2019"
            else:
                track_code = "JALUR_100_HK"
                track_name_id = "Jalur 100 Hari Kerja (Obat Baru Terdaftar SRA via Mekanisme Reliance)"
                track_name_en = "100 Working Days Track (New Drug Approved by SRA via Reliance Pathway)"
                timeline_days_hk = 100
                track_basis = "PerBPOM No. 24/2017 Pasal 27 ayat (2) huruf b jo. PerBPOM 24/2023"
        elif product_type in ["NCE", "BIOLOGIC_NOVEL"] and not is_sra_approved:
            track_code = "JALUR_300_HK"
            track_name_id = "Jalur 300 Hari Kerja: Evaluasi Lengkap Komnas Penilai Obat"
            track_name_en = "300 Working Days Track: Full National Evaluation by Komnas Penilai Obat"
            timeline_days_hk = 300
            track_basis = "PerBPOM No. 24/2017 Pasal 27 ayat (4)"
        elif product_type in ["NEW_INDICATION", "NEW_FORM_STRENGTH"]:
            track_code = "JALUR_150_HK"
            track_name_id = "Jalur 150 Hari Kerja (Kategori 2 & 3 / Modifikasi)"
            track_name_en = "150 Working Days Track (Category 2 & 3 Modifications)"
            timeline_days_hk = 150
            track_basis = "PerBPOM No. 24/2017 Pasal 27 ayat (3)"
        elif product_type == "GENERIC":
            track_code = "JALUR_100_HK"
            track_name_id = "Jalur 100 Hari Kerja (Obat Copy dengan Uji BE / Disolusi Terbanding Standar)"
            track_name_en = "100 Working Days Track (Generic Copy with standard BE / Dissolution)"
            timeline_days_hk = 100
            track_basis = "PerBPOM No. 24/2017 Pasal 27 ayat (2) huruf a"
        else:
            track_code = "JALUR_150_HK"
            track_name_id = "Jalur 150 Hari Kerja Standar"
            track_name_en = "150 Working Days Standard Track"
            timeline_days_hk = 150
            track_basis = "PerBPOM No. 24/2017"

        total_working_days = prereg_days_hk + timeline_days_hk
        # Converting Working Days to estimated calendar duration:
        # 1 month ≈ 20-22 working days. Assuming 1-2 cycles of Tambahan Data (clock stops):
        estimated_calendar_months = round((total_working_days / 21) * 1.35, 1)

        # 3. Compile Key Regulatory Requirements and Risk Factors
        key_requirements_id: List[str] = [
            f"Pengajuan Pra-Registrasi melalui sistem elektronik BPOM (ASROT/New AeS) dengan waktu evaluasi {prereg_days_hk} HK.",
            f"Pembayaran tagihan PNBP (Billing SIMPONI) sebelum batas waktu kedaluwarsa (7 hari kalender).",
            f"Penyusunan dokumen registrasi format ACTD (Part I Administratif s/d Part IV Klinis).",
            f"Stabilitas Produk Jadi wajib memenuhi Kondisi Iklim Zona IVb (30°C ± 2°C / 75% ± 5% RH) minimal 6 bulan real-time & accelerated pada saat registrasi."
        ]
        key_requirements_en: List[str] = [
            f"Pre-registration submission via BPOM electronic portal (ASROT/New AeS) with {prereg_days_hk} Working Days review timeline.",
            f"Payment of official PNBP e-billing (SIMPONI) within payment validity window (7 calendar days).",
            f"Submission of dossier in ASEAN Common Technical Dossier (ACTD) format (Parts I to IV).",
            f"Finished product stability must strictly conform to Climatic Zone IVb (30°C ± 2°C / 75% ± 5% RH) with min. 6 months real-time & accelerated data at submission."
        ]
        risk_factors: List[str] = []

        if origin == "IMPORTED":
            key_requirements_id.append(
                "Wajib melampirkan Certificate of Pharmaceutical Product (CPP) format WHO dari otoritas negara pengekspor (harus masih berlaku)."
            )
            key_requirements_id.append(
                "Sertifikat CPOB pabrik luar negeri wajib telah memperoleh Surat Pengakuan CPOB Luar Negeri dari BPOM RI."
            )
            key_requirements_en.append(
                "Must provide a valid WHO-format Certificate of Pharmaceutical Product (CPP) from the competent exporting authority."
            )
            key_requirements_en.append(
                "Foreign manufacturing site must possess an active BPOM Foreign GMP Recognition Certificate."
            )
            if foreign_gmp_status != "VALID_BPOM_CERT":
                risk_factors.append(
                    "CRITICAL RISK: Foreign GMP recognition is pending or absent. Desktop/on-site inspection can add 3-6 months to the timeline."
                )

        if product_type in ["BIOLOGIC_NOVEL", "BIOSIMILAR"]:
            key_requirements_id.append(
                "Produk Biologi wajib menyertakan Rencana Manajemen Risiko (Risk Management Plan / RMP) dan Dokumen Karakterisasi Mutu / Biosimilarity komparatif."
            )
            key_requirements_en.append(
                "Biological product must include a comprehensive Risk Management Plan (RMP) and head-to-head Biosimilarity Comparability Exercise."
            )
            if not is_sra_approved:
                risk_factors.append(
                    "HIGH RISK: Submitting a biologic without prior SRA approval triggers 300 HK full review by Komnas Penilai Obat with ad-hoc expert hearings."
                )

        if product_type == "GENERIC":
            if not be_study_available and (bcs_class not in [1, 3]):
                risk_factors.append(
                    "MAJOR RISK: In vivo bioequivalence study is missing for non-BCS class I/III molecule, which will cause pre-registration rejection."
                )

        return RegistrationAssessment({
            "category_code": category_code,
            "category_name_id": category_name_id,
            "category_name_en": category_name_en,
            "category_basis": category_basis,
            "track_code": track_code,
            "track_name_id": track_name_id,
            "track_name_en": track_name_en,
            "timeline_days_hk": timeline_days_hk,
            "prereg_days_hk": prereg_days_hk,
            "total_working_days": total_working_days,
            "estimated_calendar_months": estimated_calendar_months,
            "track_basis": track_basis,
            "fees": fees,
            "total_fee_idr": total_fee_idr,
            "reliance_applicable": reliance_applicable,
            "reliance_details": reliance_details,
            "key_requirements_id": key_requirements_id,
            "key_requirements_en": key_requirements_en,
            "risk_factors": risk_factors
        })
