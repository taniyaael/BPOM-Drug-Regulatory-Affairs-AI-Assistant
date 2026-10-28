"""Dossier Gap-Check & Risk Analyzer Engine for BPOM Drug Registration.
Performs rigorous audit of incoming dossier items against BPOM regulatory benchmarks,
categorizing gaps by severity (Critical / Major / Minor) with statutory citations and remediation paths.
"""

from typing import Dict, Any, List

class GapFinding:
    def __init__(self, item_code: str, module: str, title_id: str, title_en: str,
                 severity: str, observation_id: str, observation_en: str,
                 impact_id: str, impact_en: str,
                 bpom_basis: str,
                 remediation_id: str, remediation_en: str):
        self.item_code = item_code
        self.module = module
        self.title_id = title_id
        self.title_en = title_en
        self.severity = severity  # "CRITICAL", "MAJOR", "MINOR"
        self.observation_id = observation_id
        self.observation_en = observation_en
        self.impact_id = impact_id
        self.impact_en = impact_en
        self.bpom_basis = bpom_basis
        self.remediation_id = remediation_id
        self.remediation_en = remediation_en

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_code": self.item_code,
            "module": self.module,
            "title_id": self.title_id,
            "title_en": self.title_en,
            "severity": self.severity,
            "observation_id": self.observation_id,
            "observation_en": self.observation_en,
            "impact_id": self.impact_id,
            "impact_en": self.impact_en,
            "bpom_basis": self.bpom_basis,
            "remediation_id": self.remediation_id,
            "remediation_en": self.remediation_en
        }


class DossierGapAnalyzer:
    """Audits submitted dossier elements and identifies BPOM regulatory discrepancies."""

    @staticmethod
    def audit_dossier(dossier_data: Dict[str, Any], product_type: str, origin: str) -> Dict[str, Any]:
        findings: List[GapFinding] = []

        # 1. Audit Stability Climatic Zone IVb (Part II / P.8)
        stability_info = dossier_data.get("stability", {})
        climatic_zone = stability_info.get("climatic_zone", "").upper()
        real_time_months = stability_info.get("real_time_months", 0)
        has_zone_ivb = ("IVB" in climatic_zone) or ("ZONE 4B" in climatic_zone) or (
            stability_info.get("temp_rh") == "30C/75%RH"
        )
        has_commitment_letter = stability_info.get("has_commitment_letter", False)

        if not has_zone_ivb:
            findings.append(GapFinding(
                item_code="GAP-MUTU-01",
                module="Part II Quality (P.8)",
                title_id="Data Stabilitas Belum Memenuhi Kondisi Zona Iklim IVb",
                title_en="Stability Data Lacks Climatic Zone IVb Testing",
                severity="CRITICAL",
                observation_id=(
                    f"Dossier hanya mencantumkan data stabilitas pada {climatic_zone or 'Zona II (25°C/60% RH)'}. "
                    "Belum ada data pengujian pada kondisi Zona IVb (30°C ± 2°C / 75% ± 5% RH)."
                ),
                observation_en=(
                    f"Dossier only provides stability studies conducted under {climatic_zone or 'Zone II (25°C/60% RH)'}. "
                    "Testing under ASEAN Climatic Zone IVb (30°C ± 2°C / 75% ± 5% RH) is absent."
                ),
                impact_id="Pemberian status penolakan pra-registrasi atau Surat Permintaan Tambahan Data (TD) dengan clock-stop.",
                impact_en="Immediate rejection during pre-registration or full evaluation clock-stop (Permintaan Tambahan Data).",
                bpom_basis="PerBPOM No. 24/2017 Lampiran III & Pedoman Stabilitas ASEAN (Zone IVb)",
                remediation_id=(
                    "Segera mulai uji stabilitas real-time pada kondisi 30°C ± 2°C / 75% ± 5% RH dan uji dipercepat pada 40°C/75% RH. "
                    "Kumpulkan minimal 6 bulan data real-time Zona IVb sebelum mengajukan registrasi, serta sertakan Surat Komitmen Stabilitas."
                ),
                remediation_en=(
                    "Immediately initiate real-time stability under 30°C ± 2°C / 75% ± 5% RH and accelerated testing at 40°C/75% RH. "
                    "Generate at least 6 months of Zone IVb data prior to submission, accompanied by a signed Stability Commitment Letter."
                )
            ))
        elif real_time_months < 6:
            findings.append(GapFinding(
                item_code="GAP-MUTU-02",
                module="Part II Quality (P.8)",
                title_id="Durasi Data Stabilitas Real-Time Zona IVb Kurang dari 6 Bulan",
                title_en="Zone IVb Real-Time Stability Duration < 6 Months",
                severity="MAJOR",
                observation_id=f"Data stabilitas real-time Zona IVb yang tersedia baru mencakup {real_time_months} bulan (minimal disyaratkan 6 bulan).",
                observation_en=f"Real-time Zone IVb stability only covers {real_time_months} months (minimum mandatory duration is 6 months).",
                impact_id="Permintaan Tambahan Data (TD) berkala atau penolakan permohonan masa simpan yang diajukan.",
                impact_en="Regulatory query (TD) requiring submission of 6-month timepoint before evaluation proceeds.",
                bpom_basis="PerBPOM No. 24/2017 & ASEAN Stability Guideline",
                remediation_id="Tunggu hingga data pengujian stabilitas bulan ke-6 lengkap dan CoA stabilitas diterbitkan sebelum submit ke BPOM.",
                remediation_en="Hold dossier submission until the 6-month testing timepoint completes and formal stability report is signed."
            ))

        if not has_commitment_letter:
            findings.append(GapFinding(
                item_code="GAP-MUTU-03",
                module="Part II Quality (P.8)",
                title_id="Surat Komitmen Uji Stabilitas Lanjutan Belum Dilampirkan",
                title_en="Ongoing Stability Commitment Letter Missing",
                severity="MINOR",
                observation_id="Belum ada surat pernyataan komitmen resmi untuk melanjutkan uji stabilitas hingga shelf-life penuh.",
                observation_en="Formal written commitment letter to continue stability testing throughout proposed shelf-life is missing.",
                impact_id="Catatan minor pada tahap evaluasi mutu yang harus dipenuhi sebelum persetujuan NIE.",
                impact_en="Minor quality deficiency note requiring submission prior to marketing authorization issuance.",
                bpom_basis="PerBPOM No. 24/2017 Bab IV",
                remediation_id="Siapkan surat komitmen bermaterai dari Penanggung Jawab Mutu / Regulatory Affairs pendaftar.",
                remediation_en="Draft and execute a formal Stability Commitment Letter signed by QA/Regulatory Director."
            ))

        # 2. Audit Foreign GMP & CPP for Imported Drugs
        if origin == "IMPORTED":
            cpp_status = dossier_data.get("cpp", {})
            has_who_cpp = cpp_status.get("is_who_format", False)
            cpp_valid = cpp_status.get("is_valid", False)
            if not has_who_cpp or not cpp_valid:
                findings.append(GapFinding(
                    item_code="GAP-ADM-01",
                    module="Part I Administrative (1.6)",
                    title_id="Certificate of Pharmaceutical Product (CPP) Tidak Sesuai Format WHO atau Kedaluwarsa",
                    title_en="CPP Non-Compliant with WHO Scheme or Expired",
                    severity="CRITICAL",
                    observation_id="CPP yang dilampirkan bukan format resmi WHO Certification Scheme atau masa berlakunya telah habis.",
                    observation_en="Submitted CPP does not comply with the official WHO Certification Scheme format or has expired.",
                    impact_id="Penolakan mutlak pada tahap Pra-Registrasi (SHPR Ditolak). Dokumen registrasi tidak dapat diproses.",
                    impact_en="Outright rejection during Pre-Registration stage (SHPR Rejected). Dossier cannot proceed to main evaluation.",
                    bpom_basis="PerBPOM No. 24/2017 Pasal 18 & Rekomendasi WHO TRS 823",
                    remediation_id="Ajukan permohonan CPP format WHO terkini ke otoritas negara pengekspor (misalnya EMA, US FDA, PMDA) dengan masa berlaku minimal 2 tahun.",
                    remediation_en="Request an updated WHO-format CPP from the issuing health authority in the country of origin with >= 2 years validity."
                ))

            foreign_gmp = dossier_data.get("foreign_gmp", {})
            has_bpom_gmp_rec = foreign_gmp.get("has_bpom_recognition", False)
            if not has_bpom_gmp_rec:
                findings.append(GapFinding(
                    item_code="GAP-ADM-02",
                    module="Part I Administrative (1.5)",
                    title_id="Pabrik Luar Negeri Belum Memiliki Surat Pengakuan CPOB BPOM RI",
                    title_en="Foreign Site Lacks BPOM Foreign GMP Recognition Letter",
                    severity="CRITICAL",
                    observation_id="Fasilitas manufaktur luar negeri belum terdaftar atau belum memperoleh Surat Persetujuan/Pengakuan Pemenuhan Standar CPOB dari BPOM RI.",
                    observation_en="Foreign manufacturing site has not obtained BPOM Foreign GMP Recognition / Compliance Certificate.",
                    impact_id="Dossier tidak dapat diterbitkan Surat Persetujuan Izin Edar (NIE). Proses inspeksi luar negeri membutuhkan waktu 3-6 bulan.",
                    impact_en="Marketing Authorization (NIE) cannot be granted. GMP inspection / desk evaluation adds 3 to 6 months to lead time.",
                    bpom_basis="PerBPOM No. 27 Tahun 2020 tentang Pengakuan CPOB Luar Negeri",
                    remediation_id=(
                        "Segera ajukan permohonan Penilaian Pemenuhan Standar CPOB Fasilitas Luar Negeri melalui portal e-CPOB BPOM "
                        "(jalur desk evaluation jika memiliki sertifikat PIC/S dari otoritas anggota PIC/S, atau inspeksi on-site)."
                    ),
                    remediation_en=(
                        "Immediately file an application for Foreign GMP Recognition via BPOM e-CPOB portal "
                        "(desktop review route if site holds a valid PIC/S authority GMP certificate, or on-site audit)."
                    )
                ))

        # 3. Audit Process Validation (Part II / P.3)
        pv_status = dossier_data.get("process_validation", {})
        commercial_batches_validated = pv_status.get("commercial_batches_validated", 0)
        has_protocol_only = pv_status.get("protocol_only", False)
        if has_protocol_only or commercial_batches_validated < 3:
            findings.append(GapFinding(
                item_code="GAP-MUTU-04",
                module="Part II Quality (P.3)",
                title_id="Laporan Validasi Proses 3 Batch Komersial Belum Lengkap",
                title_en="Process Validation for 3 Consecutive Commercial Batches Incomplete",
                severity="MAJOR",
                observation_id=(
                    f"Hanya menyerahkan {commercial_batches_validated} batch data validasi atau hanya protokol validasi. "
                    "BPOM mempersyaratkan laporan validasi proses lengkap untuk minimal 3 bets skala produksi/komersial berturut-turut."
                ),
                observation_en=(
                    f"Only {commercial_batches_validated} validation batch reports or validation protocol provided. "
                    "BPOM strictly requires completed process validation reports from 3 consecutive commercial/production-scale batches."
                ),
                impact_id="Permintaan Tambahan Data (TD) Tahap 1 pada sesi evaluasi mutu. Berpotensi menunda persetujuan hingga 60 HK.",
                impact_en="Stage 1 Quality Query (Tambahan Data), creating evaluation hold of up to 60 working days.",
                bpom_basis="PerBPOM No. 24/2017 & Petunjuk Operasional Penerapan CPOB",
                remediation_id="Lakukan dan selesaikan validasi proses pada 3 batch skala komersial, kemudian sertakan laporan validasi proses lengkap beserta CoA masing-masing batch.",
                remediation_en="Execute and finalize process validation on 3 commercial batches; submit complete validation summary report and batch CoAs."
            ))

        # 4. Audit Bioequivalence / Dissolution for Generics
        if product_type == "GENERIC":
            be_status = dossier_data.get("bioequivalence", {})
            has_be_report = be_status.get("has_be_report", False)
            is_bcs_waived = be_status.get("is_bcs_waived", False)
            comparator_recognized = be_status.get("comparator_recognized_by_bpom", True)
            has_udt_report = be_status.get("has_udt_report", False)

            if not has_be_report and not is_bcs_waived:
                findings.append(GapFinding(
                    item_code="GAP-KLIN-01",
                    module="Part IV Clinical (4.2)",
                    title_id="Laporan Uji Bioekivalensi (BE) In Vivo Belum Tersedia",
                    title_en="In Vivo Bioequivalence (BE) Study Report Missing",
                    severity="CRITICAL",
                    observation_id="Produk generik tidak memiliki laporan uji BE in vivo dan tidak memenuhi kriteria biowaiver BCS.",
                    observation_en="Generic product lacks in vivo BE trial report and does not qualify for BCS Biowaiver.",
                    impact_id="Penolakan pada tahap pra-registrasi. Permohonan izin edar tidak dapat diproses lebih lanjut.",
                    impact_en="Fatal deficiency: outright pre-registration rejection. Drug registration cannot proceed.",
                    bpom_basis="PerBPOM No. 11 Tahun 2022 tentang Tata Laksana Uji Bioekivalensi",
                    remediation_id="Lakukan uji bioekivalensi in vivo di Pusat Uji BE terakreditasi BPOM RI terhadap produk inovator pembanding resmi di Indonesia.",
                    remediation_en="Commission and complete an in vivo BE trial at a BPOM-inspected BE Center against the official Indonesian reference innovator."
                ))
            elif has_be_report and not comparator_recognized:
                findings.append(GapFinding(
                    item_code="GAP-KLIN-02",
                    module="Part IV Clinical (4.2)",
                    title_id="Obat Komparator Uji BE Bukan Komparator Resmi BPOM RI",
                    title_en="BE Comparator Product Not Recognized by BPOM RI",
                    severity="CRITICAL",
                    observation_id="Studi BE menggunakan komparator luar negeri yang belum terbukti identik dengan produk inovator yang terdaftar di BPOM RI.",
                    observation_en="BE study utilized a foreign comparator not verified or listed on BPOM official reference drug list.",
                    impact_id="Hasil uji BE dapat ditolak oleh Komite Penilai Obat BPOM, mewajibkan bridging study atau uji ulang.",
                    impact_en="BE study is deemed invalid by BPOM Evaluators, necessitating a clinical bridging study or complete re-trial.",
                    bpom_basis="PerBPOM No. 11/2022 & Keputusan Kepala BPOM tentang Daftar Obat Inovator Komparator",
                    remediation_id="Sertakan bukti ekivalensi farmasetik antara komparator yang digunakan dengan komparator terdaftar di Indonesia, atau ajukan permohonan kajian kesetaraan komparator ke BPOM.",
                    remediation_en="Submit physical and chemical characterization proving equivalence between the foreign comparator and Indonesian reference innovator."
                ))

            if not has_udt_report:
                findings.append(GapFinding(
                    item_code="GAP-KLIN-03",
                    module="Part IV Clinical (4.3)",
                    title_id="Laporan Uji Disolusi Terbanding (UDT) 3 Media Belum Ada",
                    title_en="Comparative Dissolution Profile (UDT) Report in 3 Media Missing",
                    severity="MAJOR",
                    observation_id="Belum ada laporan UDT pada 3 pH media (pH 1.2, pH 4.5, dan pH 6.8) dengan perhitungan faktor kemiripan (f2).",
                    observation_en="Comparative dissolution test across 3 pH media (pH 1.2, 4.5, 6.8) with f2 similarity calculation is missing.",
                    impact_id="Penerbitan Surat Permintaan Tambahan Data (TD) pada tahap evaluasi klinis/bioekivalensi.",
                    impact_en="Issuance of Tambahan Data (TD) query resulting in evaluation delay.",
                    bpom_basis="PerBPOM No. 11/2022 Lampiran II",
                    remediation_id="Lakukan pengujian UDT di laboratorium terakreditasi CPOB pada media pH 1.2, 4.5, 6.8 dan pastikan nilai f2 >= 50.",
                    remediation_en="Perform in vitro comparative dissolution in pH 1.2, 4.5, and 6.8 dissolution media demonstrating f2 similarity factor >= 50."
                ))

        # 5. Audit Product Information & Labeling in Bahasa Indonesia
        labeling = dossier_data.get("labeling", {})
        has_id_pil = labeling.get("has_indonesian_pil", False)
        if not has_id_pil:
            findings.append(GapFinding(
                item_code="GAP-ADM-03",
                module="Part I Administrative (1.9)",
                title_id="Informasi Produk untuk Pasien (PIL) Belum Tersedia dalam Bahasa Indonesia",
                title_en="Patient Information Leaflet (PIL) Not Available in Bahasa Indonesia",
                severity="MAJOR",
                observation_id="Leaflet pasien hanya tersedia dalam bahasa Inggris atau bahasa negara asal tanpa naskah resmi Bahasa Indonesia.",
                observation_en="Patient package insert is only provided in English/foreign language without official Indonesian translation.",
                impact_id="Pemberian status catatan evaluasi penandaan; dilarang mencetak kemasan tanpa persetujuan naskah Bahasa Indonesia.",
                impact_en="Labeling evaluation deficiency; approval of final packaging artwork blocked until Indonesian draft is approved.",
                bpom_basis="PerBPOM No. 24/2017 Bab V tentang Penandaan dan Informasi Produk",
                remediation_id="Susun naskah PIL dalam Bahasa Indonesia yang lugas dan sesuai dengan SmPC, lalu ajukan pada berkas registrasi.",
                remediation_en="Prepare draft Patient Information Leaflet in Bahasa Indonesia aligned with SmPC for evaluator review."
            ))

        # Summary Metrics
        critical_count = sum(1 for g in findings if g.severity == "CRITICAL")
        major_count = sum(1 for g in findings if g.severity == "MAJOR")
        minor_count = sum(1 for g in findings if g.severity == "MINOR")

        if critical_count > 0:
            overall_status = "HIGH_RISK_REJECTION"
            status_text_id = "RISIKO TINGGI: Berpotensi Ditolak pada Pra-Registrasi / Evaluasi"
            status_text_en = "HIGH RISK: Subject to Outright Rejection at Pre-Reg / Evaluation"
        elif major_count > 0:
            overall_status = "CONDITIONAL_ACCEPTANCE_WITH_TD"
            status_text_id = "DAPAT DIAJUKAN BERSYARAT: Memerlukan Pemenuhan Tambahan Data (TD)"
            status_text_en = "CONDITIONALLY VIABLE: Clock-Stop Queries (Tambahan Data) Anticipated"
        else:
            overall_status = "READY_FOR_SUBMISSION"
            status_text_id = "SIAP SUBMIT: Dossier Memenuhi Ketentuan Regulasi BPOM"
            status_text_en = "READY FOR SUBMISSION: Dossier Fully Meets BPOM Standards"

        return {
            "overall_status": overall_status,
            "status_text_id": status_text_id,
            "status_text_en": status_text_en,
            "total_gaps": len(findings),
            "critical_count": critical_count,
            "major_count": major_count,
            "minor_count": minor_count,
            "findings": [f.to_dict() for f in findings]
        }
