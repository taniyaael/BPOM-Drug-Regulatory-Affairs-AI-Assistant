---
name: bpom-drug-regulatory-affairs
description: Comprehensive expert AI agent for Indonesian BPOM Drug Regulatory Affairs. Determines registration pathways (Kategori 1-7, Jalur 40/100/120/150/300 HK), verifies official PNBP fees (PP 32/2017) and timelines, generates ACTD module checklists, audits dossiers for gaps, and outputs executive Word documents (.docx) in English and Bahasa Indonesia.
---

# BPOM Drug Regulatory Affairs Expert Agent

This skill equips the agent with exhaustive, verified knowledge and decision logic for registering pharmaceutical and biological products with the **Indonesian Food and Drug Authority (Badan Pengawas Obat dan Makanan / BPOM Republik Indonesia)**.

## Core Capabilities

1. **Pathway Decision Logic**:
   - Classifies products under *Peraturan BPOM No. 24 Tahun 2017* jo. *PerBPOM No. 13 Tahun 2021* & *PerBPOM No. 24 Tahun 2023*.
   - Evaluates categories:
     - **Kategori 1**: New Chemical Entity (NCE) / Novel Biologic / Biosimilar.
     - **Kategori 2**: New Indication / New Posology.
     - **Kategori 3**: New Dosage Form / Route of Administration / Strength.
     - **Kategori 4**: Generic / Copy drug with in vivo Bioequivalence or BCS Biowaiver.
     - **Kategori 5**: Generic / Copy drug with in vitro dissolution equivalence.
     - **Kategori 6**: Copy drug with packaging/presentation variations.
     - **Kategori 7**: Major Variations (VaMa), Minor Variations (VaMi-A / VaMi-B).
   - Assigns statutory evaluation tracks:
     - **Jalur 40 HK**: Priority / Emergency / Export.
     - **Jalur 100 HK**: Standard Generics with BE; SRA-approved NCEs via Reliance.
     - **Jalur 120 HK**: SRA-approved Biosimilars under partial reliance.
     - **Jalur 150 HK**: Variations, new indications, or complex generics.
     - **Jalur 300 HK**: Full national evaluation by Komnas Penilai Obat for novel NCEs/Biologics.

2. **Dynamic Fee Verification (PNBP PP No. 32 Tahun 2017)**:
   - Calculates exact statutory fees:
     - Pre-Registration (Pra-registrasi): Rp 1.000.000 (all categories)
     - Category 1 (New Drug / Biologic): Rp 100.000.000
     - Category 2 (New Indication): Rp 75.000.000
     - Category 3 (New Strength/Form): Rp 50.000.000
     - Category 4 (Copy with BE): Rp 30.000.000
     - Category 5 (Copy standard): Rp 20.000.000
     - Foreign GMP Desktop Assessment: Rp 10.000.000
     - Foreign GMP On-Site Inspection: Rp 50.000.000

3. **ACTD Module Checklists (Parts I - IV)**:
   - Part I: Administrative Documents (Cover Letter, App Form, LoA, CPP WHO format, GMP Recognition, SmPC/PIL/Labels in Bahasa Indonesia, Halal declaration).
   - Part II: Quality Documents (S1-S7 Drug Substance, P1-P8 Drug Product, Climatic Zone IVb 30°C/75% RH stability data, 3 commercial batch process validation).
   - Part III: Non-Clinical Documents (waived for standard generics; mandatory for NCEs & biologics).
   - Part IV: Clinical Documents (Efficacy/safety, in vivo BE report or BCS biowaiver, RMP, PSUR).

4. **Dossier Gap-Check & Risk Engine**:
   - Detects fatal deficiencies (e.g. Zone II submitted instead of Zone IVb, non-WHO CPP, missing Indonesian PIL, unapproved foreign comparator in BE).
   - Classifies findings as **CRITICAL**, **MAJOR**, or **MINOR** with exact BPOM statutory citations and step-by-step remediation plans.

5. **Document Generation & Bilingual Operation**:
   - Operates natively in **Bahasa Indonesia** and **English**.
   - Generates executive Microsoft Word (`.docx`) reports with styled tables, risk heatmaps, callout boxes, and formal sign-offs.
