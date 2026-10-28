"""Dossier Evaluation Suite for BPOM Drug Registration.
Performs rigorous, module-by-module assessment of submitted dossier evidence (Parts I to IV),
calculates regulatory compliance scores, assigns BPOM verdicts (MS / TD / TMS),
and drafts formal BPOM Query Letters (Surat Permintaan Tambahan Data).
"""

from typing import Dict, Any, List

class ModuleEvaluationItem:
    def __init__(self, code: str, module: str, title_id: str, title_en: str,
                 status: str,  # "MS" (Compliant), "TD" (Query Needed), "TMS" (Non-Compliant), "WAIVED"
                 score: float, max_score: float,
                 evaluator_notes_id: str, evaluator_notes_en: str,
                 query_text_id: str = "", query_text_en: str = ""):
        self.code = code
        self.module = module
        self.title_id = title_id
        self.title_en = title_en
        self.status = status
        self.score = score
        self.max_score = max_score
        self.evaluator_notes_id = evaluator_notes_id
        self.evaluator_notes_en = evaluator_notes_en
        self.query_text_id = query_text_id
        self.query_text_en = query_text_en

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "module": self.module,
            "title_id": self.title_id,
            "title_en": self.title_en,
            "status": self.status,
            "score": self.score,
            "max_score": self.max_score,
            "evaluator_notes_id": self.evaluator_notes_id,
            "evaluator_notes_en": self.evaluator_notes_en,
            "query_text_id": self.query_text_id,
            "query_text_en": self.query_text_en
        }


class DossierEvaluationResult:
    def __init__(self, data: Dict[str, Any]):
        self.raw_data = data
        self.product_name = data["product_name"]
        self.verdict_code = data["verdict_code"]  # "MS", "TD", "TMS"
        self.verdict_title_id = data["verdict_title_id"]
        self.verdict_title_en = data["verdict_title_en"]
        self.compliance_score = data["compliance_score"]
        self.module_results = data["module_results"]
        self.queries_id = data["queries_id"]
        self.queries_en = data["queries_en"]
        self.draft_letter_id = data["draft_letter_id"]
        self.draft_letter_en = data["draft_letter_en"]
        self.summary_remarks_id = data["summary_remarks_id"]
        self.summary_remarks_en = data["summary_remarks_en"]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "product_name": self.product_name,
            "verdict_code": self.verdict_code,
            "verdict_title_id": self.verdict_title_id,
            "verdict_title_en": self.verdict_title_en,
            "compliance_score": self.compliance_score,
            "module_results": self.module_results,
            "queries_id": self.queries_id,
            "queries_en": self.queries_en,
            "draft_letter_id": self.draft_letter_id,
            "draft_letter_en": self.draft_letter_en,
            "summary_remarks_id": self.summary_remarks_id,
            "summary_remarks_en": self.summary_remarks_en
        }


class DossierEvaluator:
    """Evaluates comprehensive drug dossier submissions against BPOM benchmarks."""

    @staticmethod
    def evaluate_dossier(dossier: Dict[str, Any]) -> DossierEvaluationResult:
        product_name = dossier.get("product_name", "Target Medicinal Product")
        product_type = dossier.get("product_type", "GENERIC").upper()
        origin = dossier.get("origin", "LOCAL").upper()

        items: List[ModuleEvaluationItem] = []
        queries_id: List[str] = []
        queries_en: List[str] = []

        total_earned_score = 0.0
        total_max_score = 0.0

        # =====================================================================
        # PART I: ADMINISTRATIVE & LEGAL EVALUATION
        # =====================================================================
        # 1. GMP Status
        gmp_status = dossier.get("gmp_status", "VALID_LOCAL")
        if gmp_status in ["VALID_LOCAL", "VALID_BPOM_RECOGNITION"]:
            items.append(ModuleEvaluationItem(
                code="EVAL-ADM-01", module="Part I: Administratif",
                title_id="Sertifikasi CPOB / Pengakuan CPOB Luar Negeri",
                title_en="GMP Certification / BPOM Foreign GMP Recognition",
                status="MS", score=10.0, max_score=10.0,
                evaluator_notes_id="Pemenuhan CPOB telah diverifikasi dan masih berlaku untuk bentuk sediaan yang diajukan.",
                evaluator_notes_en="GMP compliance verified and currently valid for the proposed dosage form."
            ))
            total_earned_score += 10.0
        elif gmp_status == "DESK_PENDING":
            items.append(ModuleEvaluationItem(
                code="EVAL-ADM-01", module="Part I: Administratif",
                title_id="Sertifikasi CPOB / Pengakuan CPOB Luar Negeri",
                title_en="GMP Certification / BPOM Foreign GMP Recognition",
                status="TD", score=5.0, max_score=10.0,
                evaluator_notes_id="Surat Pengakuan CPOB Luar Negeri masih dalam proses evaluasi desk BPOM RI.",
                evaluator_notes_en="Foreign GMP Recognition application is currently under desktop review by BPOM.",
                query_text_id="Mohon segera menyampaikan salinan Surat Persetujuan/Pengakuan Pemenuhan Standar CPOB Fasilitas Manufaktur Luar Negeri yang diterbitkan oleh Badan POM RI.",
                query_text_en="Please provide a copy of the official Foreign GMP Recognition Letter issued by Badan POM RI for the manufacturing site."
            ))
            queries_id.append(items[-1].query_text_id)
            queries_en.append(items[-1].query_text_en)
            total_earned_score += 5.0
        else: # NONE or INVALID
            items.append(ModuleEvaluationItem(
                code="EVAL-ADM-01", module="Part I: Administratif",
                title_id="Sertifikasi CPOB / Pengakuan CPOB Luar Negeri",
                title_en="GMP Certification / BPOM Foreign GMP Recognition",
                status="TMS", score=0.0, max_score=10.0,
                evaluator_notes_id="Pabrik pembuat belum terdaftar atau tidak memiliki sertifikasi CPOB aktif yang diakui BPOM.",
                evaluator_notes_en="Manufacturing site lacks active, valid GMP compliance recognized by BPOM.",
                query_text_id="Pabrik pembuat belum memiliki status pengakuan CPOB BPOM. Registrasi tidak dapat disetujui tanpa sertifikat pemenuhan CPOB yang sah.",
                query_text_en="Site has no valid BPOM GMP recognition. Approval cannot be granted without active GMP certification."
            ))
            queries_id.append(items[-1].query_text_id)
            queries_en.append(items[-1].query_text_en)
        total_max_score += 10.0

        # 2. CPP Status for Imported Drugs
        if origin == "IMPORTED":
            cpp_status = dossier.get("cpp_status", "WHO_VALID")
            if cpp_status == "WHO_VALID":
                items.append(ModuleEvaluationItem(
                    code="EVAL-ADM-02", module="Part I: Administratif",
                    title_id="Certificate of Pharmaceutical Product (CPP) Format WHO",
                    title_en="WHO-Scheme Certificate of Pharmaceutical Product (CPP)",
                    status="MS", score=10.0, max_score=10.0,
                    evaluator_notes_id="CPP format WHO resmi dari otoritas negara pengekspor telah dilampirkan dengan masa berlaku aktif.",
                    evaluator_notes_en="Official WHO-scheme CPP from exporting NRA submitted with active validity."
                ))
                total_earned_score += 10.0
            else:
                items.append(ModuleEvaluationItem(
                    code="EVAL-ADM-02", module="Part I: Administratif",
                    title_id="Certificate of Pharmaceutical Product (CPP) Format WHO",
                    title_en="WHO-Scheme Certificate of Pharmaceutical Product (CPP)",
                    status="TMS", score=0.0, max_score=10.0,
                    evaluator_notes_id="CPP tidak sesuai format WHO Certification Scheme atau telah habis masa berlakunya.",
                    evaluator_notes_en="CPP does not comply with WHO scheme or has expired.",
                    query_text_id="Agar menyampaikan Certificate of Pharmaceutical Product (CPP) format WHO terkini yang diterbitkan oleh Badan Otoritas Negara Asal dengan masa berlaku minimal 2 (dua) tahun.",
                    query_text_en="Please provide an updated WHO-format CPP issued by the competent health authority of origin with min. 2 years validity."
                ))
                queries_id.append(items[-1].query_text_id)
                queries_en.append(items[-1].query_text_en)
            total_max_score += 10.0

        # 3. Labeling & Patient Information Leaflet (PIL) in Bahasa Indonesia
        has_id_pil = dossier.get("has_indonesian_pil", True)
        if has_id_pil:
            items.append(ModuleEvaluationItem(
                code="EVAL-ADM-03", module="Part I: Administratif",
                title_id="Informasi Produk (SmPC) & Brosur Pasien (PIL) Bahasa Indonesia",
                title_en="Product Information (SmPC) & Patient Leaflet (PIL) in Indonesian",
                status="MS", score=10.0, max_score=10.0,
                evaluator_notes_id="Naskah brosur pasien dalam Bahasa Indonesia telah memenuhi ketentuan penandaan BPOM.",
                evaluator_notes_en="Indonesian PIL draft complies with BPOM labeling standards."
            ))
            total_earned_score += 10.0
        else:
            items.append(ModuleEvaluationItem(
                code="EVAL-ADM-03", module="Part I: Administratif",
                title_id="Informasi Produk (SmPC) & Brosur Pasien (PIL) Bahasa Indonesia",
                title_en="Product Information (SmPC) & Patient Leaflet (PIL) in Indonesian",
                status="TD", score=4.0, max_score=10.0,
                evaluator_notes_id="Brosur pasien hanya tersedia dalam bahasa asing tanpa terjemahan resmi Bahasa Indonesia.",
                evaluator_notes_en="Patient package insert provided only in foreign language without Indonesian text.",
                query_text_id="Wajib menyampaikan rancangan naskah Informasi Produk untuk Pasien (PIL / Brosur) dalam Bahasa Indonesia yang lugas dan sesuai dengan SmPC.",
                query_text_en="Mandatory submission of draft Patient Information Leaflet (PIL) in clear Bahasa Indonesia aligned with SmPC."
            ))
            queries_id.append(items[-1].query_text_id)
            queries_en.append(items[-1].query_text_en)
            total_earned_score += 4.0
        total_max_score += 10.0

        # 4. Halal & Raw Material Origin Declaration
        has_halal_declaration = dossier.get("has_halal_declaration", True)
        if has_halal_declaration:
            items.append(ModuleEvaluationItem(
                code="EVAL-ADM-04", module="Part I: Administratif",
                title_id="Pernyataan Asal Bahan Baku & Jaminan Produk Halal (UU JPH)",
                title_en="Raw Material Origin Declaration & Halal Compliance (Law No. 33/2014)",
                status="MS", score=5.0, max_score=5.0,
                evaluator_notes_id="Surat pernyataan asal bahan baku (porcine/non-porcine statement) telah dilampirkan lengkap.",
                evaluator_notes_en="Raw material origin statement (porcine-free/porcine status) submitted."
            ))
            total_earned_score += 5.0
        else:
            items.append(ModuleEvaluationItem(
                code="EVAL-ADM-04", module="Part I: Administratif",
                title_id="Pernyataan Asal Bahan Baku & Jaminan Produk Halal (UU JPH)",
                title_en="Raw Material Origin Declaration & Halal Compliance (Law No. 33/2014)",
                status="TD", score=2.0, max_score=5.0,
                evaluator_notes_id="Surat pernyataan asal bahan baku porcine/non-porcine belum disertakan.",
                evaluator_notes_en="Declaration regarding porcine origin of raw materials is missing.",
                query_text_id="Agar melengkapi surat pernyataan resmi terkait asal-usul bahan baku aktif dan eksipien (mengandung babi / bebas babi) sesuai UU JPH.",
                query_text_en="Please provide a formal declaration regarding the animal/porcine origin of drug substance and excipients per Indonesian Halal regulations."
            ))
            queries_id.append(items[-1].query_text_id)
            queries_en.append(items[-1].query_text_en)
            total_earned_score += 2.0
        total_max_score += 5.0

        # =====================================================================
        # PART II: QUALITY / CMC EVALUATION
        # =====================================================================
        # 5. Process Validation (3 commercial batches)
        pv_batches = int(dossier.get("process_validation_batches", 3))
        if pv_batches >= 3:
            items.append(ModuleEvaluationItem(
                code="EVAL-Q-01", module="Part II: Mutu (P.3)",
                title_id="Validasi Proses Pembuatan 3 Bets Skala Komersial",
                title_en="Process Validation for 3 Consecutive Commercial Batches",
                status="MS", score=15.0, max_score=15.0,
                evaluator_notes_id="Laporan validasi proses lengkap pada 3 bets komersial berturut-turut telah memenuhi syarat.",
                evaluator_notes_en="Completed process validation reports across 3 consecutive commercial batches accepted."
            ))
            total_earned_score += 15.0
        elif pv_batches > 0:
            items.append(ModuleEvaluationItem(
                code="EVAL-Q-01", module="Part II: Mutu (P.3)",
                title_id="Validasi Proses Pembuatan 3 Bets Skala Komersial",
                title_en="Process Validation for 3 Consecutive Commercial Batches",
                status="TD", score=7.0, max_score=15.0,
                evaluator_notes_id=f"Data validasi proses baru mencakup {pv_batches} bets. Belum memenuhi syarat 3 bets komersial.",
                evaluator_notes_en=f"Process validation only submitted for {pv_batches} batch(es); 3 batches required.",
                query_text_id="Mohon melengkapi laporan validasi proses lengkap beserta Certificate of Analysis (CoA) untuk minimal 3 (tiga) bets produksi skala komersial berturut-turut.",
                query_text_en="Please submit complete process validation reports and CoAs for at least 3 consecutive commercial production batches."
            ))
            queries_id.append(items[-1].query_text_id)
            queries_en.append(items[-1].query_text_en)
            total_earned_score += 7.0
        else:
            items.append(ModuleEvaluationItem(
                code="EVAL-Q-01", module="Part II: Mutu (P.3)",
                title_id="Validasi Proses Pembuatan 3 Bets Skala Komersial",
                title_en="Process Validation for 3 Consecutive Commercial Batches",
                status="TMS", score=0.0, max_score=15.0,
                evaluator_notes_id="Hanya menyertakan protokol validasi tanpa ada laporan pelaksanaan validasi proses.",
                evaluator_notes_en="Only validation protocol provided without executed validation batch data.",
                query_text_id="Laporan validasi proses komersial belum tersedia. Wajib menyerahkan laporan validasi 3 bets komersial sebelum izin edar dapat dipertimbangkan.",
                query_text_en="Executed commercial validation missing. Mandatory submission of 3-batch validation reports prior to approval."
            ))
            queries_id.append(items[-1].query_text_id)
            queries_en.append(items[-1].query_text_en)
        total_max_score += 15.0

        # 6. Stability Climatic Zone IVb Testing (30°C ± 2°C / 75% ± 5% RH)
        stability_zone = dossier.get("stability_zone", "ZONE_4B").upper()
        stability_months = int(dossier.get("stability_months", 12))
        has_stability_commitment = dossier.get("has_stability_commitment", True)

        if "4B" in stability_zone or "IVB" in stability_zone:
            if stability_months >= 6:
                items.append(ModuleEvaluationItem(
                    code="EVAL-Q-02", module="Part II: Mutu (P.8)",
                    title_id="Data Stabilitas Produk Jadi Kondisi Zona Iklim IVb (30°C/75% RH)",
                    title_en="Finished Product Stability Testing under Climatic Zone IVb (30°C/75% RH)",
                    status="MS", score=20.0, max_score=20.0,
                    evaluator_notes_id=f"Tersedia data stabilitas real-time Zona IVb selama {stability_months} bulan dan dipercepat 40°C/75% RH selama 6 bulan.",
                    evaluator_notes_en=f"Zone IVb real-time data for {stability_months} months and accelerated 40°C/75% RH for 6 months accepted."
                ))
                total_earned_score += 20.0
            else:
                items.append(ModuleEvaluationItem(
                    code="EVAL-Q-02", module="Part II: Mutu (P.8)",
                    title_id="Data Stabilitas Produk Jadi Kondisi Zona Iklim IVb (30°C/75% RH)",
                    title_en="Finished Product Stability Testing under Climatic Zone IVb (30°C/75% RH)",
                    status="TD", score=8.0, max_score=20.0,
                    evaluator_notes_id=f"Data stabilitas real-time Zona IVb baru mencakup {stability_months} bulan (minimal disyaratkan 6 bulan saat registrasi).",
                    evaluator_notes_en=f"Zone IVb stability only covers {stability_months} months (min. 6 months required at submission).",
                    query_text_id="Agar melengkapi laporan stabilitas real-time kondisi Zona Iklim IVb (30°C ± 2°C / 75% ± 5% RH) minimal bulan ke-6 beserta CoA stabilitas terkait.",
                    query_text_en="Please provide the 6-month timepoint real-time stability study report under Climatic Zone IVb (30°C ± 2°C / 75% ± 5% RH)."
                ))
                queries_id.append(items[-1].query_text_id)
                queries_en.append(items[-1].query_text_en)
                total_earned_score += 8.0
        else: # Missing Zone IVb (only Zone II)
            items.append(ModuleEvaluationItem(
                code="EVAL-Q-02", module="Part II: Mutu (P.8)",
                title_id="Data Stabilitas Produk Jadi Kondisi Zona Iklim IVb (30°C/75% RH)",
                title_en="Finished Product Stability Testing under Climatic Zone IVb (30°C/75% RH)",
                status="TMS", score=0.0, max_score=20.0,
                evaluator_notes_id="FATAL: Data stabilitas tidak diuji pada kondisi Zona Iklim IVb (hanya Zona II). Pelanggaran kriteria registrasi BPOM.",
                evaluator_notes_en="FATAL: Stability testing was conducted only under Zone II (25°C/60% RH). Non-compliant with BPOM Zone IVb criteria.",
                query_text_id="Data stabilitas pada kondisi Zona Iklim IVb (30°C ± 2°C / 75% ± 5% RH) belum diserahkan. BPOM tidak dapat menyetujui masa kedaluwarsa tanpa pengujian kondisi tropis IVb.",
                query_text_en="Finished product stability data under ASEAN Climatic Zone IVb (30°C ± 2°C / 75% ± 5% RH) is missing. Shelf-life cannot be approved."
            ))
            queries_id.append(items[-1].query_text_id)
            queries_en.append(items[-1].query_text_en)
        total_max_score += 20.0

        # 7. Ongoing Stability Commitment Letter
        if has_stability_commitment:
            items.append(ModuleEvaluationItem(
                code="EVAL-Q-03", module="Part II: Mutu (P.8)",
                title_id="Surat Komitmen Uji Stabilitas Lanjutan Zona IVb",
                title_en="Ongoing Stability Commitment Letter for Climatic Zone IVb",
                status="MS", score=5.0, max_score=5.0,
                evaluator_notes_id="Surat komitmen uji stabilitas lanjutan hingga akhir masa simpan telah dilampirkan.",
                evaluator_notes_en="Signed stability commitment letter for full shelf-life submitted."
            ))
            total_earned_score += 5.0
        else:
            items.append(ModuleEvaluationItem(
                code="EVAL-Q-03", module="Part II: Mutu (P.8)",
                title_id="Surat Komitmen Uji Stabilitas Lanjutan Zona IVb",
                title_en="Ongoing Stability Commitment Letter for Climatic Zone IVb",
                status="TD", score=2.0, max_score=5.0,
                evaluator_notes_id="Surat komitmen uji stabilitas lanjutan belum dilampirkan.",
                evaluator_notes_en="Ongoing stability commitment letter is missing.",
                query_text_id="Agar menyampaikan Surat Pernyataan Komitmen bermaterai untuk melanjutkan uji stabilitas jangka panjang kondisi Zona IVb hingga batas kedaluwarsa yang diajukan.",
                query_text_en="Please provide a formal signed and stamped Stability Commitment Letter to continue Zone IVb real-time stability to the full shelf-life."
            ))
            queries_id.append(items[-1].query_text_id)
            queries_en.append(items[-1].query_text_en)
            total_earned_score += 2.0
        total_max_score += 5.0

        # =====================================================================
        # PART III: NON-CLINICAL EVALUATION
        # =====================================================================
        if product_type == "GENERIC":
            items.append(ModuleEvaluationItem(
                code="EVAL-NC-01", module="Part III: Non-Klinis",
                title_id="Kajian Farmakologi & Toksikologi Non-Klinis",
                title_en="Non-Clinical Pharmacology & Toxicology Studies",
                status="WAIVED", score=5.0, max_score=5.0,
                evaluator_notes_id="Dikecualikan (Waived) untuk Obat Generik / Copy sesuai ketentuan PerBPOM No. 24/2017.",
                evaluator_notes_en="Waived for Generic / Copy medicinal products per BPOM Regulation No. 24 of 2017."
            ))
            total_earned_score += 5.0
        else: # NCE / Biologic
            has_nonclinical = dossier.get("has_nonclinical_studies", True)
            if has_nonclinical:
                items.append(ModuleEvaluationItem(
                    code="EVAL-NC-01", module="Part III: Non-Klinis",
                    title_id="Kajian Farmakodinamika & Toksikologi GLP Komparatif",
                    title_en="Comparative GLP Pharmacology & Toxicology Studies",
                    status="MS", score=10.0, max_score=10.0,
                    evaluator_notes_id="Kajian non-klinis komparatif (in vitro binding, bioassay, toksikologi) telah memenuhi pedoman produk biologi/NCE.",
                    evaluator_notes_en="Comparative non-clinical data (in vitro bioassays, binding, toxicology) accepted."
                ))
                total_earned_score += 10.0
            else:
                items.append(ModuleEvaluationItem(
                    code="EVAL-NC-01", module="Part III: Non-Klinis",
                    title_id="Kajian Farmakodinamika & Toksikologi GLP Komparatif",
                    title_en="Comparative GLP Pharmacology & Toxicology Studies",
                    status="TD", score=3.0, max_score=10.0,
                    evaluator_notes_id="Kajian non-klinis belum lengkap untuk kategori produk biologi / zat aktif baru.",
                    evaluator_notes_en="Non-clinical module is incomplete for biologic / new active substance.",
                    query_text_id="Mohon melengkapi ringkasan studi non-klinis dan laporan studi farmakodinamika komparatif in vitro/in vivo sesuai PerBPOM 15/2019.",
                    query_text_en="Please provide non-clinical overview and comparative in vitro/in vivo binding/pharmacodynamic study reports per BPOM Reg 15/2019."
                ))
                queries_id.append(items[-1].query_text_id)
                queries_en.append(items[-1].query_text_en)
                total_earned_score += 3.0
            total_max_score += 10.0

        # =====================================================================
        # PART IV: CLINICAL & EQUIVALENCE EVALUATION
        # =====================================================================
        if product_type == "GENERIC":
            has_be_study = dossier.get("has_be_study", True)
            be_ci_passed = dossier.get("be_ci_passed", True)
            comparator_ok = dossier.get("comparator_ok", True)
            has_udt_3_media = dossier.get("has_udt_3_media", True)

            # BE Study Report
            if has_be_study and be_ci_passed and comparator_ok:
                items.append(ModuleEvaluationItem(
                    code="EVAL-CLIN-01", module="Part IV: Klinis (4.2)",
                    title_id="Laporan Uji Bioekivalensi (BE) In Vivo vs Inovator Resmi BPOM",
                    title_en="In Vivo Bioequivalence (BE) Study Report vs Official Reference Drug",
                    status="MS", score=15.0, max_score=15.0,
                    evaluator_notes_id="Uji BE memenuhi kriteria bioekivalen: 90% Confidence Interval AUC0-t dan Cmax berada dalam rentang 80.00% - 125.00% terhadap inovator terdaftar.",
                    evaluator_notes_en="BE study demonstrates bioequivalence: 90% CI for AUC0-t and Cmax fall within 80.00% - 125.00% vs approved innovator."
                ))
                total_earned_score += 15.0
            elif not comparator_ok:
                items.append(ModuleEvaluationItem(
                    code="EVAL-CLIN-01", module="Part IV: Klinis (4.2)",
                    title_id="Laporan Uji Bioekivalensi (BE) In Vivo vs Inovator Resmi BPOM",
                    title_en="In Vivo Bioequivalence (BE) Study Report vs Official Reference Drug",
                    status="TMS", score=0.0, max_score=15.0,
                    evaluator_notes_id="FATAL: Komparator yang digunakan bukan komparator resmi terdaftar di BPOM RI tanpa adanya studi penyetaraan (bridging study).",
                    evaluator_notes_en="FATAL: Reference product used in BE study is not an approved Indonesian comparator product.",
                    query_text_id="Obat komparator uji BE yang digunakan adalah produk luar negeri yang belum diakui BPOM. Harap serahkan kajian kesetaraan farmasetik komparator atau protokol uji BE ulang.",
                    query_text_en="Comparator product in BE study is an unverified foreign drug. Submit bridging equivalence characterization or re-trial."
                ))
                queries_id.append(items[-1].query_text_id)
                queries_en.append(items[-1].query_text_en)
            else:
                items.append(ModuleEvaluationItem(
                    code="EVAL-CLIN-01", module="Part IV: Klinis (4.2)",
                    title_id="Laporan Uji Bioekivalensi (BE) In Vivo vs Inovator Resmi BPOM",
                    title_en="In Vivo Bioequivalence (BE) Study Report vs Official Reference Drug",
                    status="TMS", score=0.0, max_score=15.0,
                    evaluator_notes_id="Laporan uji bioekivalensi in vivo belum tersedia atau interval kepercayaan gagal memenuhi batas 80-125%.",
                    evaluator_notes_en="In vivo BE study report is missing or 90% CI failed the 80.00-125.00% bioequivalence acceptance criteria.",
                    query_text_id="Laporan uji BE in vivo belum memenuhi syarat bioekivalen sesuai Peraturan BPOM No. 11 Tahun 2022.",
                    query_text_en="In vivo BE study report fails to prove bioequivalence under BPOM Regulation No. 11 of 2022."
                ))
                queries_id.append(items[-1].query_text_id)
                queries_en.append(items[-1].query_text_en)
            total_max_score += 15.0

            # UDT (In Vitro Dissolution in 3 Media)
            if has_udt_3_media:
                items.append(ModuleEvaluationItem(
                    code="EVAL-CLIN-02", module="Part IV: Klinis (4.3)",
                    title_id="Uji Disolusi Terbanding (UDT) pada 3 Media pH (1.2, 4.5, 6.8)",
                    title_en="Comparative In Vitro Dissolution (UDT) across 3 pH Media",
                    status="MS", score=10.0, max_score=10.0,
                    evaluator_notes_id="Profil disolusi terbanding identik dengan produk komparator pada media pH 1.2, 4.5, dan 6.8 dengan faktor kemiripan f2 >= 50.",
                    evaluator_notes_en="In vitro dissolution profile demonstrates similarity to reference product with f2 score >= 50 across 3 pH buffer media."
                ))
                total_earned_score += 10.0
            else:
                items.append(ModuleEvaluationItem(
                    code="EVAL-CLIN-02", module="Part IV: Klinis (4.3)",
                    title_id="Uji Disolusi Terbanding (UDT) pada 3 Media pH (1.2, 4.5, 6.8)",
                    title_en="Comparative In Vitro Dissolution (UDT) across 3 pH Media",
                    status="TD", score=3.0, max_score=10.0,
                    evaluator_notes_id="Laporan UDT pada 3 pH media (pH 1.2, 4.5, 6.8) belum lengkap atau perhitungan nilai f2 belum disertakan.",
                    evaluator_notes_en="Comparative dissolution test across 3 pH media (pH 1.2, 4.5, 6.8) or f2 calculation is incomplete.",
                    query_text_id="Agar melengkapi laporan Uji Disolusi Terbanding (UDT) pada 3 media disolusi (pH 1.2, 4.5, dan 6.8) dengan perhitungan nilai f2 terhadap bets uji BE.",
                    query_text_en="Please provide comparative dissolution test reports in 3 pH media (pH 1.2, 4.5, 6.8) with f2 similarity calculation."
                ))
                queries_id.append(items[-1].query_text_id)
                queries_en.append(items[-1].query_text_en)
                total_earned_score += 3.0
            total_max_score += 10.0

        else: # Biologic / NCE Clinical Studies
            has_clinical_trials = dossier.get("has_clinical_trials", True)
            has_rmp = dossier.get("has_rmp", True)

            if has_clinical_trials:
                items.append(ModuleEvaluationItem(
                    code="EVAL-CLIN-03", module="Part IV: Klinis (4.4)",
                    title_id="Uji Klinis Komparatif Fase 1 & 3 / Efikasi dan Keamanan",
                    title_en="Comparative Phase 1 & 3 Clinical Trials / Efficacy and Safety",
                    status="MS", score=15.0, max_score=15.0,
                    evaluator_notes_id="Uji klinis fase 1 (PK/PD) dan fase 3 komparatif membuktikan kesetaraan kemanjuran terapeutik dan profil keamanan.",
                    evaluator_notes_en="Phase 1 PK/PD and Phase 3 comparative clinical trials demonstrate equivalent efficacy and comparable safety profile."
                ))
                total_earned_score += 15.0
            else:
                items.append(ModuleEvaluationItem(
                    code="EVAL-CLIN-03", module="Part IV: Klinis (4.4)",
                    title_id="Uji Klinis Komparatif Fase 1 & 3 / Efikasi dan Keamanan",
                    title_en="Comparative Phase 1 & 3 Clinical Trials / Efficacy and Safety",
                    status="TMS", score=0.0, max_score=15.0,
                    evaluator_notes_id="Data uji klinis komparatif fase 3 tidak lengkap atau belum membuktikan kesetaraan biosimilar.",
                    evaluator_notes_en="Phase 3 comparative clinical trial data is missing or fails to prove therapeutic equivalence.",
                    query_text_id="Data uji klinis komparatif belum lengkap. Harap serahkan laporan studi klinis fase 3 komparatif lengkap (CSR) beserta analisis imunogenisitas.",
                    query_text_en="Comparative clinical trial data is incomplete. Please submit full Phase 3 Clinical Study Report (CSR) and immunogenicity profile."
                ))
                queries_id.append(items[-1].query_text_id)
                queries_en.append(items[-1].query_text_en)
            total_max_score += 15.0

            if has_rmp:
                items.append(ModuleEvaluationItem(
                    code="EVAL-CLIN-04", module="Part IV: Klinis (4.5)",
                    title_id="Rencana Manajemen Risiko (RMP) & Sistem Farmakovigilans",
                    title_en="Risk Management Plan (RMP) & Pharmacovigilance System",
                    status="MS", score=10.0, max_score=10.0,
                    evaluator_notes_id="RMP dan sistem pemantauan farmakovigilans di Indonesia telah memenuhi syarat PerBPOM No. 15/2019.",
                    evaluator_notes_en="RMP and local pharmacovigilance surveillance protocol comply with BPOM requirements."
                ))
                total_earned_score += 10.0
            else:
                items.append(ModuleEvaluationItem(
                    code="EVAL-CLIN-04", module="Part IV: Klinis (4.5)",
                    title_id="Rencana Manajemen Risiko (RMP) & Sistem Farmakovigilans",
                    title_en="Risk Management Plan (RMP) & Pharmacovigilance System",
                    status="TD", score=3.0, max_score=10.0,
                    evaluator_notes_id="Rencana Manajemen Risiko (RMP) spesifik untuk wilayah Indonesia belum dilampirkan.",
                    evaluator_notes_en="Indonesia-specific Risk Management Plan (RMP) is missing.",
                    query_text_id="Wajib menyampaikan dokumen Rencana Manajemen Risiko (RMP) dan prosedur pelaporan farmakovigilans (MESO) yang berlaku di Indonesia.",
                    query_text_en="Mandatory submission of Risk Management Plan (RMP) and local pharmacovigilance (MESO) monitoring SOP for Indonesia."
                ))
                queries_id.append(items[-1].query_text_id)
                queries_en.append(items[-1].query_text_en)
                total_earned_score += 3.0
            total_max_score += 10.0

        # Calculate Overall Compliance Score
        compliance_score = round((total_earned_score / total_max_score) * 100.0, 1) if total_max_score > 0 else 0.0

        # Determine BPOM Verdict
        has_tms = any(item.status == "TMS" for item in items)
        has_td = any(item.status == "TD" for item in items)

        if has_tms or compliance_score < 60.0:
            verdict_code = "TMS"
            verdict_title_id = "TIDAK MEMENUHI SYARAT (TMS) - Berpotensi Ditolak"
            verdict_title_en = "DOES NOT MEET REQUIREMENTS (TMS) - Non-Viable / Rejection Trigger"
            summary_remarks_id = "Dossier memiliki defisiensi fatal yang melanggar kriteria pokok registrasi obat BPOM. Permohonan izin edar tidak dapat disetujui tanpa pengujian/dokumen ulang menyeluruh."
            summary_remarks_en = "Dossier contains fatal deficiencies non-compliant with fundamental BPOM drug criteria. Application cannot be approved without comprehensive re-testing or missing key documentation."
        elif has_td or compliance_score < 90.0:
            verdict_code = "TD"
            verdict_title_id = "PERMINTAAN TAMBAHAN DATA (TD) - Evaluasi Tertunda (Clock-Stop)"
            verdict_title_en = "REQUEST FOR ADDITIONAL DATA (TD) - Evaluation Clock-Stop"
            summary_remarks_id = f"Dossier dapat dilanjutkan ke tahap evaluasi berikutnya setelah pendaftar memenuhi {len(queries_id)} butir Permintaan Tambahan Data dalam batas waktu 20 Hari Kerja."
            summary_remarks_en = f"Dossier is viable subject to applicant satisfactorily resolving {len(queries_en)} query items within the statutory 20 Working Days timeline."
        else:
            verdict_code = "MS"
            verdict_title_id = "MEMENUHI SYARAT (MS) - Siap Disetujui (Recommended for NIE)"
            verdict_title_en = "MEETS ALL REQUIREMENTS (MS) - Recommended for Marketing Authorization (NIE)"
            summary_remarks_id = "Seluruh dokumen administratif, mutu, non-klinis, dan klinis telah memenuhi standar regulasi BPOM RI secara komprehensif. Direkomendasikan untuk penerbitan Izin Edar (NIE)."
            summary_remarks_en = "All administrative, quality, non-clinical, and clinical modules comprehensively meet BPOM regulatory criteria. Recommended for issuance of Marketing Authorization (NIE)."

        # Draft Official BPOM Query Letter (Surat Tambahan Data)
        draft_letter_id = DossierEvaluator._format_draft_td_letter_id(product_name, queries_id)
        draft_letter_en = DossierEvaluator._format_draft_td_letter_en(product_name, queries_en)

        return DossierEvaluationResult({
            "product_name": product_name,
            "verdict_code": verdict_code,
            "verdict_title_id": verdict_title_id,
            "verdict_title_en": verdict_title_en,
            "compliance_score": compliance_score,
            "module_results": [it.to_dict() for it in items],
            "queries_id": queries_id,
            "queries_en": queries_en,
            "draft_letter_id": draft_letter_id,
            "draft_letter_en": draft_letter_en,
            "summary_remarks_id": summary_remarks_id,
            "summary_remarks_en": summary_remarks_en
        })

    @staticmethod
    def _format_draft_td_letter_id(product_name: str, queries: List[str]) -> str:
        if not queries:
            return "Tidak ada permintaan tambahan data. Seluruh parameter dossier telah Memenuhi Syarat (MS)."
        
        items_text = "\n".join([f"{idx+1}. {q}" for idx, q in enumerate(queries)])
        return f"""BADAN PENGAWAS OBAT DAN MAKANAN REPUBLIK INDONESIA
DIREKTORAT REGISTRASI OBAT
Jl. Percetakan Negara No. 23, Jakarta Pusat 10560 | Telp: (021) 4244407
____________________________________________________________________________________

Nomor    : RG.01.03.3.33.2026/TD/{product_name.replace(' ', '_').upper()[:15]}
Lampiran : -
Perihal  : Permintaan Tambahan Data Registrasi Obat - {product_name}

Kepada Yth.
Pimpinan Industri Farmasi Pendaftar
Di Tempat

Sehubungan dengan evaluasi teknis dan administratif terhadap berkas registrasi obat yang Saudara ajukan:
Nama Obat      : {product_name}
Tanggal Evaluasi : 2026

Berdasarkan hasil evaluasi Tim Penilai Registrasi Obat Badan POM RI mengacu pada Peraturan BPOM No. 24 Tahun 2017 jo. PerBPOM No. 13 Tahun 2021, bersama ini diberitahukan bahwa berkas registrasi tersebut masih memerlukan kelengkapan dan klarifikasi data tambahan sebagai berikut:

{items_text}

Sesuai ketentuan Pasal 29 Peraturan BPOM No. 24 Tahun 2017, Saudara diberikan kesempatan untuk menyampaikan data tambahan tersebut melalui portal elektronik ASROT / New AeS selambat-lambatnya 20 (dua puluh) Hari Kerja terhitung sejak tanggal surat ini diterbitkan.

Apabila sampai dengan batas waktu yang telah ditentukan Saudara belum menyampaikan kelengkapan data yang diminta tanpa pemberitahuan tertulis yang dapat dipertanggungjawabkan, maka permohonan registrasi obat dinyatakan DITOLAK (Batal Demi Hukum).

Demikian agar menjadi maklum dan perhatian Saudara.


Direktur Registrasi Obat
Badan Pengawas Obat dan Makanan RI

[Tanda Tangan & Cap Elektronik BPOM]
"""

    @staticmethod
    def _format_draft_td_letter_en(product_name: str, queries: List[str]) -> str:
        if not queries:
            return "No regulatory queries required. All dossier modules fully comply with BPOM standards (MS)."
        
        items_text = "\n".join([f"{idx+1}. {q}" for idx, q in enumerate(queries)])
        return f"""INDONESIAN FOOD AND DRUG AUTHORITY (BADAN POM RI)
DIRECTORATE OF DRUG REGISTRATION
Jl. Percetakan Negara No. 23, Central Jakarta 10560, Indonesia
____________________________________________________________________________________

Ref No.   : RG.01.03.3.33.2026/TD/{product_name.replace(' ', '_').upper()[:15]}
Subject   : Official Request for Additional Regulatory Data (Query Notice) - {product_name}

To:
Head of Regulatory Affairs / Applicant Pharmaceutical Industry
Registered Office, Indonesia

Following the technical, administrative, and clinical assessment of the marketing authorization dossier submitted for:
Medicinal Product : {product_name}
Review Cycle      : Stage 1 Evaluation

In accordance with BPOM Regulation No. 24 of 2017 jo. Reg No. 13 of 2021, the BPOM Drug Evaluation Committee has identified the following technical queries and deficiencies requiring resolution:

{items_text}

Pursuant to Article 29 of BPOM Regulation No. 24 of 2017, the applicant is granted 20 (twenty) Working Days from the date of this notice to furnish the complete response package via the BPOM electronic submission portal.

Failure to address all queries within the statutory deadline without justified notice will result in the immediate closure and formal REJECTION of the application.


Yours sincerely,
Director of Drug Registration
Indonesian Food and Drug Authority (Badan POM RI)

[Official Seal & Electronic Signature]
"""
