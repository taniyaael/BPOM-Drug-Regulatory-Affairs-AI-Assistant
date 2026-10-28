"""Integration test for Flask App endpoints."""
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import app
from test_scenarios.scenarios_data import SCENARIO_1_IMPORTED_BIOLOGIC, SCENARIO_2_LOCAL_GENERIC

def test_routes():
    client = app.test_client()
    
    # 1. Test Index
    res_index = client.get("/")
    assert res_index.status_code == 200, f"Index failed: {res_index.status_code}"
    assert b"BPOM Drug Regulatory Affairs" in res_index.data, "Index title missing"
    print("[PASS] GET / -> 200 OK")

    # 2. Test Evaluate Endpoint (Scenario 1)
    res_eval = client.post("/api/evaluate", json=SCENARIO_1_IMPORTED_BIOLOGIC)
    assert res_eval.status_code == 200, f"Evaluate failed: {res_eval.status_code}"
    data_eval = res_eval.get_json()
    assert data_eval["assessment"]["category_code"] == "KATEGORI_1"
    assert data_eval["assessment"]["total_fee_idr"] == 111000000
    assert "checklist" in data_eval
    print("[PASS] POST /api/evaluate -> 200 OK (Kategori 1, Rp 111.000.000 verified)")

    # 3. Test Gap Check Endpoint
    res_gap = client.post("/api/gap-check", json={"stability_zone": "ZONE_2", "cpp_format": "NON_WHO"})
    assert res_gap.status_code == 200, f"Gap check failed: {res_gap.status_code}"
    data_gap = res_gap.get_json()
    assert data_gap["critical_count"] > 0
    print(f"[PASS] POST /api/gap-check -> 200 OK ({data_gap['critical_count']} critical gaps flagged)")

    # 4. Test Export Docx Endpoint
    res_docx = client.post("/api/export-docx", json={"product": SCENARIO_2_LOCAL_GENERIC, "language": "ID"})
    assert res_docx.status_code == 200, f"Export docx failed: {res_docx.status_code}"
    assert len(res_docx.data) > 10000, "Docx file too small"
    print(f"[PASS] POST /api/export-docx -> 200 OK ({len(res_docx.data)} bytes returned)")

    print("\nALL FLASK APP ENDPOINT TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_routes()
