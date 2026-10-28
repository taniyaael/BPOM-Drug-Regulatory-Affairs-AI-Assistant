"""Realistic Test Datasets for BPOM Drug Regulatory Scenarios.
Scenario 1: Imported Biologic (Trastuzumab Biosimilar mAb)
Scenario 2: Local Generic (Metformin HCl 500mg Film-Coated Tablet)
Scenario 3: Dossier Gap-Check (Audit of Non-Compliant Oncology Generic Dossier)
"""

from typing import Dict, Any

# SCENARIO 1: IMPORTED BIOLOGIC (Trastuzumab Biosimilar mAb)
SCENARIO_1_IMPORTED_BIOLOGIC: Dict[str, Any] = {
    "product_name": "Herclonix 440 mg Lyophilized Powder",
    "active_substance": "Trastuzumab (Recombinant humanized IgG1 monoclonal antibody)",
    "dosage_form": "Serbuk Liofilisasi untuk Infus Intravena (Powder for Concentrate for Solution for Infusion)",
    "strength": "440 mg / vial",
    "product_type": "BIOSIMILAR",
    "origin": "IMPORTED",
    "foreign_country": "Netherlands",
    "manufacturer_name": "Biopharma Solutions EU B.V.",
    "applicant_company": "PT. Nusantara Biologika Farma",
    "pjt_pharmacist": "apt. Ratna Dewi Sartika, S.Farm.",
    "stra_number": "19880415/STRA-BPOM/2012/23491",
    "is_sra_approved": True,
    "sra_countries": ["EMA (European Medicines Agency)", "Health Canada"],
    "foreign_gmp_status": "DESK_EVALUATION_NEEDED",
    "is_public_health_emergency": False,
    "be_study_available": False,  # Biologics use comparability trial instead of small-molecule BE
    "has_innovator_in_indonesia": True,
    "innovator_name": "Herceptin 440mg (PT Roche Indonesia)",
    "stability": {
        "climatic_zone": "Zone IVb (30°C/75% RH)",
        "real_time_months": 12,
        "temp_rh": "30C/75%RH",
        "has_commitment_letter": True
    },
    "cpp": {
        "is_who_format": True,
        "is_valid": True,
        "issuing_agency": "Dutch Health and Youth Care Inspectorate (IGJ) / EMA"
    },
    "foreign_gmp": {
        "has_bpom_recognition": False,  # Will apply via desk evaluation
        "e_cpob_submission_ready": True
    },
    "process_validation": {
        "commercial_batches_validated": 3,
        "protocol_only": False
    },
    "labeling": {
        "has_indonesian_pil": True,
        "has_indonesian_smpc": True
    }
}

# SCENARIO 2: LOCAL GENERIC DRUG (Metformin HCl 500mg Tablet)
SCENARIO_2_LOCAL_GENERIC: Dict[str, Any] = {
    "product_name": "Metforin 500 Film-Coated Tablet",
    "active_substance": "Metformin Hydrochloride",
    "dosage_form": "Tablet Salut Selaput (Film-Coated Tablet)",
    "strength": "500 mg",
    "product_type": "GENERIC",
    "origin": "LOCAL",
    "manufacturer_name": "PT. Medika Sejahtera Farma (Plant Cikarang, Jawa Barat)",
    "applicant_company": "PT. Medika Sejahtera Farma",
    "pjt_pharmacist": "apt. Budi Santoso, S.Farm.",
    "stra_number": "19851120/STRA-BPOM/2010/11820",
    "is_sra_approved": False,
    "sra_countries": [],
    "foreign_gmp_status": "LOCAL_CPOB",
    "is_public_health_emergency": False,
    "be_study_available": True,
    "bcs_class": 3,  # Metformin is BCS Class 3 (High Solubility, Low Permeability)
    "has_innovator_in_indonesia": True,
    "innovator_name": "Glucophage 500mg (PT Merck Tbk)",
    "stability": {
        "climatic_zone": "Zone IVb (30°C/75% RH)",
        "real_time_months": 6,
        "temp_rh": "30C/75%RH",
        "has_commitment_letter": True
    },
    "process_validation": {
        "commercial_batches_validated": 3,
        "protocol_only": False
    },
    "bioequivalence": {
        "has_be_report": True,
        "is_bcs_waived": False,  # Fully validated in vivo BE executed
        "comparator_recognized_by_bpom": True,
        "has_udt_report": True
    },
    "labeling": {
        "has_indonesian_pil": True,
        "has_indonesian_smpc": True
    }
}

# SCENARIO 3: DOSSIER GAP-CHECK (Oncology Generic with Compliance Pitfalls)
SCENARIO_3_GAP_CHECK_PAYLOAD: Dict[str, Any] = {
    "product_name": "Pemetrexed Disodium 500mg Powder for Injection",
    "active_substance": "Pemetrexed Disodium Heptahydrate",
    "dosage_form": "Serbuk Liofilisasi untuk Infus (Lyophilized Powder for Injection)",
    "strength": "500 mg / vial",
    "product_type": "GENERIC",
    "origin": "IMPORTED",
    "foreign_country": "India",
    "applicant_company": "PT. Global Onkologi Indonesia",
    "pjt_pharmacist": "apt. Maya Anggraini, S.Farm.",
    "stra_number": "19920105/STRA-BPOM/2016/54210",
    "is_sra_approved": False,
    "sra_countries": [],
    "foreign_gmp_status": "NONE",
    # Deliberate Deficiencies:
    "stability": {
        "climatic_zone": "Zone II (25°C/60% RH)", # DEFICIENCY 1: Only Zone II submitted!
        "real_time_months": 24,
        "temp_rh": "25C/60%RH",
        "has_commitment_letter": False          # DEFICIENCY 2: Missing commitment letter!
    },
    "cpp": {
        "is_who_format": False,                 # DEFICIENCY 3: Not WHO scheme!
        "is_valid": False                       # Expired
    },
    "foreign_gmp": {
        "has_bpom_recognition": False           # DEFICIENCY 4: Missing BPOM recognition!
    },
    "process_validation": {
        "commercial_batches_validated": 1,      # DEFICIENCY 5: Only 1 batch validation!
        "protocol_only": True
    },
    "bioequivalence": {
        "has_be_report": True,
        "is_bcs_waived": False,
        "comparator_recognized_by_bpom": False, # DEFICIENCY 6: Unrecognized foreign comparator!
        "has_udt_report": False                 # DEFICIENCY 7: Missing 3-media dissolution!
    },
    "labeling": {
        "has_indonesian_pil": False,            # DEFICIENCY 8: Missing Indonesian PIL!
        "has_indonesian_smpc": True
    }
}
