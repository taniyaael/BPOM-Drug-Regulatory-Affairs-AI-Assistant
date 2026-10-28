"""Flask Web Server for BPOM Drug Regulatory Affairs AI Assistant.
Provides RESTful APIs for Pathway Decision Logic, ACTD Checklists, Gap Analysis,
and on-the-fly Word (.docx) document generation and downloads.
"""

import os
import sys
import tempfile
from flask import Flask, render_template, request, jsonify, send_file

# Add base directory to sys.path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from bpom_ra_agent.core.decision_engine import PathwayDecisionEngine
from bpom_ra_agent.core.ctd_checklist import get_bpom_actd_checklist
from bpom_ra_agent.core.gap_analyzer import DossierGapAnalyzer
from bpom_ra_agent.core.dossier_evaluator import DossierEvaluator, DossierEvaluationResult
from bpom_ra_agent.core.regulatory_database import STATUTES
from bpom_ra_agent.docx_generator.docx_builder import DocxReportBuilder
from test_scenarios.scenarios_data import (
    SCENARIO_1_IMPORTED_BIOLOGIC,
    SCENARIO_2_LOCAL_GENERIC,
    SCENARIO_3_GAP_CHECK_PAYLOAD
)

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))

@app.route("/")
def index():
    """Serves the main application dashboard."""
    return render_template("index.html")

@app.route("/api/evaluate", methods=["POST"])
def evaluate():
    """Calculates BPOM Category, Pathway, PNBP Fees, and ACTD Checklist."""
    data = request.json or {}
    assessment = PathwayDecisionEngine.evaluate(data)
    checklist = get_bpom_actd_checklist(data.get("product_type", "GENERIC"), data.get("origin", "LOCAL"))
    return jsonify({
        "assessment": assessment.to_dict(),
        "checklist": checklist
    })

@app.route("/api/gap-check", methods=["POST"])
def gap_check():
    """Runs compliance audit and returns critical, major, minor findings."""
    data = request.json or {}
    
    # Map form data to dossier structure
    is_zone_4b = (data.get("stability_zone") == "ZONE_4B")
    real_time_months = int(data.get("stability_months", 6))
    is_who_cpp = (data.get("cpp_format") == "WHO_VALID")
    foreign_gmp_valid = (data.get("foreign_gmp") == "VALID")
    pv_3_batches = (data.get("process_val") == "3_BATCHES")
    be_comparator_ok = (data.get("be_comparator") == "BPOM_RECOGNIZED")
    udt_complete = (data.get("udt") == "3_MEDIA")
    pil_id_ok = (data.get("pil_id") == "YES")

    dossier_data = {
        "product_name": data.get("product_name", "Target Drug"),
        "stability": {
            "climatic_zone": "Zone IVb (30°C/75% RH)" if is_zone_4b else "Zone II (25°C/60% RH)",
            "real_time_months": real_time_months,
            "temp_rh": "30C/75%RH" if is_zone_4b else "25C/60%RH",
            "has_commitment_letter": True
        },
        "cpp": {
            "is_who_format": is_who_cpp,
            "is_valid": is_who_cpp
        },
        "foreign_gmp": {
            "has_bpom_recognition": foreign_gmp_valid
        },
        "process_validation": {
            "commercial_batches_validated": 3 if pv_3_batches else 1,
            "protocol_only": not pv_3_batches
        },
        "bioequivalence": {
            "has_be_report": True,
            "is_bcs_waived": False,
            "comparator_recognized_by_bpom": be_comparator_ok,
            "has_udt_report": udt_complete
        },
        "labeling": {
            "has_indonesian_pil": pil_id_ok,
            "has_indonesian_smpc": True
        }
    }

    result = DossierGapAnalyzer.audit_dossier(
        dossier_data=dossier_data,
        product_type="GENERIC",
        origin="IMPORTED"
    )
    result["product_name"] = data.get("product_name", "Target Drug")
    return jsonify(result)

@app.route("/api/scenarios/<scenario_id>", methods=["GET"])
def get_scenario(scenario_id):
    """Returns preset realistic scenario payloads."""
    if scenario_id == "1":
        return jsonify(SCENARIO_1_IMPORTED_BIOLOGIC)
    elif scenario_id == "2":
        return jsonify(SCENARIO_2_LOCAL_GENERIC)
    elif scenario_id == "3":
        return jsonify(SCENARIO_3_GAP_CHECK_PAYLOAD)
    return jsonify({"error": "Scenario not found"}), 404

@app.route("/api/statutes", methods=["GET"])
def get_statutes():
    """Returns statutory database references."""
    return jsonify(STATUTES)

@app.route("/api/export-docx", methods=["POST"])
def export_docx():
    """Generates and downloads the Word (.docx) evaluation dossier."""
    data = request.json or {}
    product = data.get("product", {})
    language = data.get("language", "ID")

    assessment = PathwayDecisionEngine.evaluate(product)
    checklist = get_bpom_actd_checklist(product.get("product_type", "GENERIC"), product.get("origin", "LOCAL"))

    # Save to a temporary file
    temp_dir = tempfile.gettempdir()
    safe_name = "".join(c for c in product.get("product_name", "Drug") if c.isalnum() or c in (' ', '_')).rstrip()
    filename = f"BPOM_Dossier_Evaluation_{safe_name.replace(' ', '_')}_{language}.docx"
    file_path = os.path.join(temp_dir, filename)

    DocxReportBuilder.create_evaluation_document(assessment, product, checklist, language, file_path)

    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

@app.route("/api/export-gap-docx", methods=["POST"])
def export_gap_docx():
    """Generates and downloads the Word (.docx) gap audit report."""
    data = request.json or {}
    audit_result = data.get("audit_result", {})
    product = data.get("product", {})
    language = data.get("language", "ID")

    temp_dir = tempfile.gettempdir()
    filename = f"BPOM_Dossier_Gap_Audit_Report_{language}.docx"
    file_path = os.path.join(temp_dir, filename)

    DocxReportBuilder.create_gap_audit_document(audit_result, product, language, file_path)

@app.route("/api/evaluate-dossier", methods=["POST"])
def evaluate_dossier():
    """Evaluates comprehensive dossier and returns module scores, verdicts, and draft TD letter."""
    data = request.json or {}
    eval_result = DossierEvaluator.evaluate_dossier(data)
    return jsonify(eval_result.to_dict())

@app.route("/api/export-dossier-docx", methods=["POST"])
def export_dossier_docx():
    """Generates and downloads the Word (.docx) dossier evaluation report."""
    data = request.json or {}
    eval_dict = data.get("evaluation_result", {})
    product = data.get("product", {})
    language = data.get("language", "ID")

    eval_result = DossierEvaluationResult(eval_dict)

    temp_dir = tempfile.gettempdir()
    safe_name = "".join(c for c in product.get("product_name", "Dossier") if c.isalnum() or c in (' ', '_')).rstrip()
    filename = f"BPOM_Dossier_Evaluation_Report_{safe_name.replace(' ', '_')}_{language}.docx"
    file_path = os.path.join(temp_dir, filename)

    DocxReportBuilder.create_dossier_evaluation_report(eval_result, product, language, file_path)

    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

@app.route("/download/presentation", methods=["GET"])
def download_presentation():
    """Serves the PowerPoint (.pptx) presentation for direct browser download."""
    pptx_path = os.path.join(BASE_DIR, "outputs", "BPOM_Drug_Regulatory_Affairs_AI_Assistant_Presentation.pptx")
    return send_file(
        pptx_path,
        as_attachment=True,
        download_name="BPOM_Drug_Regulatory_Affairs_AI_Assistant_Presentation.pptx",
        mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  BPOM DRUG REGULATORY AFFAIRS AI ASSISTANT")
    print("  Server is starting on http://127.0.0.1:5000")
    print("="*70)
    app.run(host="127.0.0.1", port=5000, debug=False)
