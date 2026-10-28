"""Automated test suite for Dossier Evaluator and Document Generator."""
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from bpom_ra_agent.core.dossier_evaluator import DossierEvaluator
from bpom_ra_agent.docx_generator.docx_builder import DocxReportBuilder
from app import app

def test_evaluator_samples():
    print("\n" + "="*70)
    print("TESTING DOSSIER EVALUATOR ENGINE")
    print("="*70)

    # 1. Sample A: Compliant Biosimilar
    sample_a = {
        "product_name": "Herclonix 440 mg Lyophilized Powder",
        "product_type": "BIOSIMILAR",
        "origin": "IMPORTED",
        "gmp_status": "VALID_BPOM_RECOGNITION",
        "cpp_status": "WHO_VALID",
        "has_indonesian_pil": True,
        "has_halal_declaration": True,
        "process_validation_batches": 3,
        "stability_zone": "ZONE_4B",
        "stability_months": 12,
        "has_stability_commitment": True,
        "has_nonclinical_studies": True,
        "has_clinical_trials": True,
        "has_rmp": True
    }
    res_a = DossierEvaluator.evaluate_dossier(sample_a)
    print(f"Sample A (Biosimilar) : Verdict = {res_a.verdict_code}, Score = {res_a.compliance_score}%")
    assert res_a.verdict_code == "MS", f"Expected MS, got {res_a.verdict_code}"
    assert res_a.compliance_score == 100.0, f"Expected 100%, got {res_a.compliance_score}"
    assert len(res_a.queries_id) == 0, "Compliant dossier should have zero queries"
    print("  [PASS] Sample A -> MS (Memenuhi Syarat)")

    # 2. Sample B: Generic with queries (Missing UDT & commitment)
    sample_b = {
        "product_name": "Metforin 500 mg Film-Coated Tablet",
        "product_type": "GENERIC",
        "origin": "LOCAL",
        "gmp_status": "VALID_LOCAL",
        "has_indonesian_pil": True,
        "has_halal_declaration": True,
        "process_validation_batches": 3,
        "stability_zone": "ZONE_4B",
        "stability_months": 6,
        "has_stability_commitment": False, # TD
        "has_be_study": True,
        "be_ci_passed": True,
        "comparator_ok": True,
        "has_udt_3_media": False # TD
    }
    res_b = DossierEvaluator.evaluate_dossier(sample_b)
    print(f"Sample B (Generic)    : Verdict = {res_b.verdict_code}, Score = {res_b.compliance_score}%")
    assert res_b.verdict_code == "TD", f"Expected TD, got {res_b.verdict_code}"
    assert len(res_b.queries_id) == 2, f"Expected 2 queries, got {len(res_b.queries_id)}"
    assert "Permintaan Tambahan Data" in res_b.draft_letter_id
    print("  [PASS] Sample B -> TD (Permintaan Tambahan Data with 2 queries)")

    # 3. Sample C: Non-compliant Oncology (Fatal Zone II & invalid CPP)
    sample_c = {
        "product_name": "Pemetrexed Disodium 500mg Powder",
        "product_type": "GENERIC",
        "origin": "IMPORTED",
        "gmp_status": "NONE", # TMS
        "cpp_status": "INVALID", # TMS
        "has_indonesian_pil": False,
        "has_halal_declaration": False,
        "process_validation_batches": 0, # TMS
        "stability_zone": "ZONE_2", # TMS (Fatal)
        "stability_months": 12,
        "has_stability_commitment": False,
        "has_be_study": True,
        "be_ci_passed": True,
        "comparator_ok": False, # TMS (Fatal)
        "has_udt_3_media": False
    }
    res_c = DossierEvaluator.evaluate_dossier(sample_c)
    print(f"Sample C (Oncology)   : Verdict = {res_c.verdict_code}, Score = {res_c.compliance_score}%")
    assert res_c.verdict_code == "TMS", f"Expected TMS, got {res_c.verdict_code}"
    print("  [PASS] Sample C -> TMS (Tidak Memenuhi Syarat - Fatal Deficiencies)")

    # 4. Test Word Document Generation for Dossier Evaluation
    out_docx = os.path.join(BASE_DIR, "outputs", "Test_Dossier_Evaluation_Report_Bilingual.docx")
    DocxReportBuilder.create_dossier_evaluation_report(res_b, sample_b, "ID", out_docx)
    assert os.path.exists(out_docx) and os.path.getsize(out_docx) > 10000
    print(f"  [PASS] Word Dossier Evaluation Report successfully created: {out_docx}")

    # 5. Test Flask Endpoints
    client = app.test_client()
    res_api = client.post("/api/evaluate-dossier", json=sample_b)
    assert res_api.status_code == 200
    data = res_api.get_json()
    assert data["verdict_code"] == "TD"
    print("  [PASS] Flask POST /api/evaluate-dossier -> 200 OK")

    res_docx_api = client.post("/api/export-dossier-docx", json={"evaluation_result": res_b.to_dict(), "product": sample_b, "language": "ID"})
    assert res_docx_api.status_code == 200
    assert len(res_docx_api.data) > 10000
    print("  [PASS] Flask POST /api/export-dossier-docx -> 200 OK (Word file returned)")

    print("\nALL DOSSIER EVALUATOR TESTS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    test_evaluator_samples()
