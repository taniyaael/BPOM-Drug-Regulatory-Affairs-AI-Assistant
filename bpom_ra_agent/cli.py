"""Command-Line Interface for BPOM Drug Regulatory Affairs AI Agent.
Provides bilingual interactive and batch assessment of drug registration pathways,
ACTD compliance checklists, and Word report exports.
"""

import os
import sys
import argparse
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from bpom_ra_agent.core.decision_engine import PathwayDecisionEngine
from bpom_ra_agent.core.ctd_checklist import get_bpom_actd_checklist
from bpom_ra_agent.core.gap_analyzer import DossierGapAnalyzer
from bpom_ra_agent.core.template_engine import RegulatoryTemplateEngine
from bpom_ra_agent.docx_generator.docx_builder import DocxReportBuilder

def main():
    parser = argparse.ArgumentParser(
        description="BPOM Drug Regulatory Affairs AI Assistant (English & Bahasa Indonesia)"
    )
    parser.add_argument("--lang", choices=["EN", "ID"], default="ID", help="Output language: EN or ID")
    parser.add_argument("--scenario", choices=["1", "2", "3", "all"], help="Run specific test scenario")
    parser.add_argument("--json", type=str, help="Path to custom product JSON file for assessment")
    parser.add_argument("--out", type=str, default="outputs/evaluation_report.docx", help="Path to save Word document")
    
    args = parser.parse_args()

    if args.scenario:
        from test_scenarios.test_runner import run_scenario_1, run_scenario_2, run_scenario_3
        if args.scenario in ["1", "all"]:
            run_scenario_1()
        if args.scenario in ["2", "all"]:
            run_scenario_2()
        if args.scenario in ["3", "all"]:
            run_scenario_3()
        return

    if args.json:
        with open(args.json, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        is_id = (args.lang == "ID")
        assessment = PathwayDecisionEngine.evaluate(data)
        checklist = get_bpom_actd_checklist(data.get("product_type", "GENERIC"), data.get("origin", "LOCAL"))
        out_file = DocxReportBuilder.create_evaluation_document(assessment, data, checklist, args.lang, args.out)
        
        print("\n" + "="*70)
        print("BPOM DRUG REGULATORY AFFAIRS ASSESSMENT RESULT" if not is_id else "HASIL PENILAIAN REGULASI OBAT BPOM RI")
        print("="*70)
        print(f"Product / Produk       : {data.get('product_name')}")
        print(f"Category / Kategori    : {assessment.category_name_id if is_id else assessment.category_name_en}")
        print(f"Track / Jalur          : {assessment.track_name_id if is_id else assessment.track_name_en}")
        print(f"Review Days / Waktu    : {assessment.total_working_days} Hari Kerja (Working Days)")
        print(f"Total PNBP / Biaya     : Rp {assessment.total_fee_idr:,.0f} (PP 32/2017)")
        print(f"Report Saved / Laporan : {out_file}")
        print("="*70)
    else:
        print("Please specify --scenario [1|2|3|all] or provide a product JSON file with --json <path>")

if __name__ == "__main__":
    main()
