"""Automated Test Runner for BPOM Drug Regulatory Affairs AI Agent.
Executes 3 realistic scenarios:
1. Imported Biologic (Trastuzumab Biosimilar mAb)
2. Local Generic Drug (Metformin HCl 500mg Film-Coated Tablet)
3. Dossier Gap-Check (Comprehensive audit of non-compliant oncology generic)
Generates native Word (.docx) documents in English and Bahasa Indonesia.
"""

import os
import sys

# Configure UTF-8 for console output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure root package directory is in sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from bpom_ra_agent.core.decision_engine import PathwayDecisionEngine
from bpom_ra_agent.core.ctd_checklist import get_bpom_actd_checklist
from bpom_ra_agent.core.gap_analyzer import DossierGapAnalyzer
from bpom_ra_agent.core.template_engine import RegulatoryTemplateEngine
from bpom_ra_agent.docx_generator.docx_builder import DocxReportBuilder
from test_scenarios.scenarios_data import (
    SCENARIO_1_IMPORTED_BIOLOGIC,
    SCENARIO_2_LOCAL_GENERIC,
    SCENARIO_3_GAP_CHECK_PAYLOAD
)

OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUTS_DIR, exist_ok=True)

def run_scenario_1():
    print("\n" + "="*80)
    print(">> EXECUTING SCENARIO 1: IMPORTED BIOLOGIC (Trastuzumab Biosimilar mAb)")
    print("="*80)
    product = SCENARIO_1_IMPORTED_BIOLOGIC
    
    # 1. Decision Logic & Fee/Timeline Verification
    assessment = PathwayDecisionEngine.evaluate(product)
    print(f"Product           : {product['product_name']}")
    print(f"Classification    : {product['product_type']} ({product['origin']})")
    print(f"Category (BPOM)   : {assessment.category_name_id}")
    print(f"Evaluation Track  : {assessment.track_name_id}")
    print(f"Total Review Time : {assessment.total_working_days} Hari Kerja (~{assessment.estimated_calendar_months} Months)")
    print(f"Total PNBP Fees   : Rp {assessment.total_fee_idr:,.0f} (PP 32/2017)")
    print(f"Reliance Review   : {assessment.reliance_details}")
    
    # 2. ACTD Checklist
    checklist = get_bpom_actd_checklist(product['product_type'], product['origin'])
    
    # 3. Generate Word Documents (EN & ID)
    path_en = os.path.join(OUTPUTS_DIR, "Scenario_1_Imported_Biologic_Evaluation_EN.docx")
    path_id = os.path.join(OUTPUTS_DIR, "Scenario_1_Evaluasi_Produk_Biologi_Impor_ID.docx")
    
    DocxReportBuilder.create_evaluation_document(assessment, product, checklist, "EN", path_en)
    DocxReportBuilder.create_evaluation_document(assessment, product, checklist, "ID", path_id)
    
    print(f"[OK] Generated Word Document (EN): {path_en}")
    print(f"[OK] Generated Word Document (ID): {path_id}")
    return assessment, checklist

def run_scenario_2():
    print("\n" + "="*80)
    print(">> EXECUTING SCENARIO 2: LOCAL GENERIC DRUG (Metformin HCl 500mg Tablet)")
    print("="*80)
    product = SCENARIO_2_LOCAL_GENERIC
    
    # 1. Decision Logic & Fee/Timeline Verification
    assessment = PathwayDecisionEngine.evaluate(product)
    print(f"Product           : {product['product_name']}")
    print(f"Classification    : {product['product_type']} ({product['origin']})")
    print(f"Category (BPOM)   : {assessment.category_name_id}")
    print(f"Evaluation Track  : {assessment.track_name_id}")
    print(f"Total Review Time : {assessment.total_working_days} Hari Kerja (~{assessment.estimated_calendar_months} Months)")
    print(f"Total PNBP Fees   : Rp {assessment.total_fee_idr:,.0f} (PP 32/2017)")
    
    # 2. ACTD Checklist (Notice: Module 3 Non-Clinical is waived for Generics)
    checklist = get_bpom_actd_checklist(product['product_type'], product['origin'])
    print(f"Non-Clinical Waived: {checklist['is_non_clinical_waived']}")
    
    # 3. Generate Word Documents (EN & ID)
    path_en = os.path.join(OUTPUTS_DIR, "Scenario_2_Local_Generic_Evaluation_EN.docx")
    path_id = os.path.join(OUTPUTS_DIR, "Scenario_2_Evaluasi_Obat_Generik_Lokal_ID.docx")
    
    DocxReportBuilder.create_evaluation_document(assessment, product, checklist, "EN", path_en)
    DocxReportBuilder.create_evaluation_document(assessment, product, checklist, "ID", path_id)
    
    print(f"[OK] Generated Word Document (EN): {path_en}")
    print(f"[OK] Generated Word Document (ID): {path_id}")
    return assessment, checklist

def run_scenario_3():
    print("\n" + "="*80)
    print(">> EXECUTING SCENARIO 3: DOSSIER GAP-CHECK & AUDIT (Oncology Generic)")
    print("="*80)
    product = SCENARIO_3_GAP_CHECK_PAYLOAD
    
    # 1. Run Audit against BPOM Standards
    audit_result = DossierGapAnalyzer.audit_dossier(
        dossier_data=product,
        product_type=product['product_type'],
        origin=product['origin']
    )
    
    print(f"Audit Target      : {product['product_name']}")
    print(f"Overall Status    : {audit_result['status_text_en']}")
    print(f"Total Deficiencies: {audit_result['total_gaps']} findings")
    print(f" - CRITICAL       : {audit_result['critical_count']}")
    print(f" - MAJOR          : {audit_result['major_count']}")
    print(f" - MINOR          : {audit_result['minor_count']}")
    
    for f in audit_result['findings']:
        print(f"   [{f['severity']}] {f['item_code']}: {f['title_en']}")
    
    # 2. Generate Word Documents (EN & ID)
    path_en = os.path.join(OUTPUTS_DIR, "Scenario_3_Dossier_Gap_Check_Audit_Report_EN.docx")
    path_id = os.path.join(OUTPUTS_DIR, "Scenario_3_Laporan_Audit_Gap_Check_Dossier_ID.docx")
    
    DocxReportBuilder.create_gap_audit_document(audit_result, product, "EN", path_en)
    DocxReportBuilder.create_gap_audit_document(audit_result, product, "ID", path_id)
    
    print(f"[OK] Generated Word Document (EN): {path_en}")
    print(f"[OK] Generated Word Document (ID): {path_id}")
    return audit_result

if __name__ == "__main__":
    print("Starting BPOM Drug Regulatory Affairs AI Agent Test Suite...")
    s1_assess, s1_chk = run_scenario_1()
    s2_assess, s2_chk = run_scenario_2()
    s3_audit = run_scenario_3()
    
    print("\n" + "="*80)
    print("ALL 3 TEST SCENARIOS COMPLETED SUCCESSFULLY!")
    print(f"Output files stored in: {OUTPUTS_DIR}")
    print("="*80)
