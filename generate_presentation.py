"""PowerPoint (.pptx) Presentation Generator for BPOM Drug Regulatory Affairs AI Assistant.
Generates an executive 13-slide deck with corporate healthcare styling, color schemes,
structured cards, tables, and statutory regulatory citations.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Brand Palette
COLOR_NAVY = RGBColor(26, 54, 93)       # #1A365D Primary Deep Navy
COLOR_BLUE = RGBColor(43, 108, 176)     # #2B6CB0 Secondary Blue
COLOR_TEAL = RGBColor(49, 151, 149)     # #319795 Accent Teal
COLOR_DARK = RGBColor(45, 55, 72)       # #2D3748 Text Dark
COLOR_MUTED = RGBColor(113, 128, 150)   # #718096 Muted Gray
COLOR_LIGHT_BG = RGBColor(247, 250, 252)# #F7FAFC
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_EMERALD = RGBColor(40, 116, 75)   # #28744B Green (MS)
COLOR_AMBER = RGBColor(183, 121, 31)    # #B7791F Amber (TD)
COLOR_RED = RGBColor(197, 48, 48)       # #C53030 Red (TMS)

def apply_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, title_text, category_text="BPOM DRUG REGULATORY AFFAIRS AI ASSISTANT"):
    # Category tag
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.5), Inches(0.35))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(9.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_TEAL

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_NAVY

def add_card(slide, left, top, width, height, bg_color=COLOR_WHITE, border_color=COLOR_MUTED):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape

def create_presentation(output_path: str):
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Cover)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_background(s1, COLOR_NAVY)

    # Accent decorative bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.15), Inches(3.6))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLOR_TEAL
    bar.line.fill.background()

    # Title box
    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(1.7), Inches(11.2), Inches(3.8))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "BADAN PENGAWAS OBAT DAN MAKANAN REPUBLIK INDONESIA"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_TEAL
    p0.space_after = Pt(12)

    p1 = tf1.add_paragraph()
    p1.text = "BPOM Drug Regulatory Affairs\nAI Assistant"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.space_after = Pt(14)

    p2 = tf1.add_paragraph()
    p2.text = "Sistem Cerdas Pendukung Keputusan Jalur Registrasi Obat, Verifikasi Tarif PNBP,\nEvaluasi Dossier Format ACTD, dan Analisis Kesenjangan (Gap-Check)"
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(226, 232, 240)
    p2.space_after = Pt(24)

    p3 = tf1.add_paragraph()
    p3.text = "Bilingual: Bahasa Indonesia & English  |  Platform Terintegrasi Web UI & Ekspor Word (.docx)"
    p3.font.size = Pt(11)
    p3.font.color.rgb = RGBColor(160, 174, 192)

    # =========================================================================
    # SLIDE 2: LATAR BELAKANG & TANTANGAN (Pain Points)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_background(s2, COLOR_LIGHT_BG)
    add_header(s2, "Latar Belakang & Tantangan Registrasi Obat di Indonesia")

    cards_data = [
        ("Kompleksitas Regulasi BPOM", 
         "Banyaknya peraturan yang terus diperbarui (PerBPOM 24/2017, 13/2021, 24/2023) membuat penentuan kategori pendaftaran (Kategori 1-7) dan jalur evaluasi rentan salah tafsir."),
        ("Risiko Surat Permintaan Tambahan Data (TD)",
         "Kekurangan dokumen teknis saat penyerahan berkas memicu diterbitkannya Surat TD dengan batas waktu ketat 20 Hari Kerja (clock-stop) yang dapat memperlambat peluncuran produk 3-9 bulan."),
        ("Persyaratan Spesifik Iklim Zona IVb & Mutu",
         "BPOM mewajibkan data stabilitas kondisi iklim tropis ekstrim Zona IVb (30°C/75% RH) dan validasi 3 bets komersial yang kerap luput dari dossier prinsipal global (hanya Zona II)."),
        ("Sertifikasi CPOB Luar Negeri & CPP WHO",
         "Registrasi obat impor mensyaratkan Surat Pengakuan CPOB LN dari BPOM dan Certificate of Pharmaceutical Product (CPP) format resmi WHO dengan validitas aktif.")
    ]

    for idx, (title, desc) in enumerate(cards_data):
        x = Inches(0.8 + (idx % 2) * 5.9)
        y = Inches(1.8 + (idx // 2) * 2.5)
        add_card(s2, x, y, Inches(5.6), Inches(2.2), COLOR_WHITE, RGBColor(226, 232, 240))
        
        box = s2.shapes.add_textbox(x + Inches(0.3), y + Inches(0.25), Inches(5.0), Inches(1.7))
        tf = box.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = f"0{idx+1}. {title}"
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_NAVY
        pt.space_after = Pt(8)
        
        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_DARK

    # =========================================================================
    # SLIDE 3: TUJUAN PENGEMBANGAN APLIKASI
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_background(s3, COLOR_LIGHT_BG)
    add_header(s3, "Tujuan & Nilai Strategis AI Assistant Bagi Tim Regulatory Affairs")

    goals = [
        ("Otomatisasi Penentuan Jalur & Biaya Resmi",
         "Menentukan Kategori 1 s/d 7 dan Jalur Evaluasi (40, 100, 120, 150, 300 HK) secara otomatis disertai kalkulasi akurat tagihan PNBP (PP No. 32 Tahun 2017) dan estimasi kalender."),
        ("Memaksimalkan First-Cycle Approval Rate",
         "Mendeteksi dini defisiensi dokumen (gap-check) sebelum pendaftaran diajukan ke portal ASROT BPOM, menghindari penolakan pada pra-registrasi dan meminimalkan siklus Tambahan Data."),
        ("Standardisasi Dossier Sesuai Format ACTD",
         "Menyediakan panduan daftar periksa modul Part I (Administratif), Part II (Mutu), Part III (Non-Klinis), dan Part IV (Klinis) yang telah disesuaikan dengan kriteria khusus BPOM RI."),
        ("Simulasi Evaluasi Dossier & Draf Surat Resmi",
         "Mensimulasikan penilaian ala evaluator BPOM untuk menghasilkan skor kepatuhan, status keputusan (MS / TD / TMS), serta menyusun draf resmi Surat Permintaan Tambahan Data secara instan.")
    ]

    for idx, (title, desc) in enumerate(goals):
        x = Inches(0.8 + (idx % 2) * 5.9)
        y = Inches(1.8 + (idx // 2) * 2.5)
        add_card(s3, x, y, Inches(5.6), Inches(2.2), COLOR_WHITE, RGBColor(226, 232, 240))
        
        box = s3.shapes.add_textbox(x + Inches(0.3), y + Inches(0.25), Inches(5.0), Inches(1.7))
        tf = box.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = f"🎯 {title}"
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_BLUE
        pt.space_after = Pt(8)
        
        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_DARK

    # =========================================================================
    # SLIDE 4: SUMBER DATA & RUJUKAN RESMI BPOM
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_background(s4, COLOR_LIGHT_BG)
    add_header(s4, "Sumber Data Regulasi & Rujukan Statutori Resmi BPOM RI")

    sources = [
        ("Peraturan BPOM No. 24 Tahun 2017 & No. 13 Tahun 2021",
         "Kriteria dan Tata Laksana Registrasi Obat manusia di Indonesia, mekanisme registrasi elektronik (ASROT), kategori pendaftaran, dan jangka waktu evaluasi."),
        ("Peraturan BPOM No. 24 Tahun 2023 (Pembaruan Kedua)",
         "Mekanisme evaluasi Reliance (Jalur 100 & 120 HK) untuk obat baru dan biosimilar yang telah disetujui oleh otoritas regulasi terpercaya (SRA / WHO Listed Authorities)."),
        ("Peraturan Pemerintah (PP) No. 32 Tahun 2017",
         "Tarif resmi Penerimaan Negara Bukan Pajak (PNBP) yang berlaku pada Badan POM untuk pra-registrasi, registrasi obat baru, obat copy/generik, variasi, dan inspeksi CPOB."),
        ("Peraturan BPOM No. 15 Tahun 2019 jo. No. 28 Tahun 2022",
         "Pedoman registrasi Produk Biologi & Biosimilar: comparability exercise, karakterisasi mutu, uji klinis fase 3 ekivalensi, dan Risk Management Plan (RMP)."),
        ("Peraturan BPOM No. 27 Tahun 2020 (CPOB & CPOB Luar Negeri)",
         "Penerapan Cara Pembuatan Obat yang Baik, persyaratan penilaian dokumen pemenuhan CPOB fasilitas luar negeri (Desk Evaluation) dan inspeksi on-site BPOM."),
        ("Peraturan BPOM No. 11 Tahun 2022 & ASEAN Stability Zone IVb",
         "Tata Laksana Uji Bioekivalensi in vivo, kriteria Biowaiver BCS Kelas 1 & 3, serta Pedoman Stabilitas ASEAN Kondisi Iklim Zona IVb (30°C ± 2°C / 75% ± 5% RH).")
    ]

    for idx, (title, desc) in enumerate(sources):
        col = idx % 3
        row = idx // 3
        x = Inches(0.8 + col * 3.9)
        y = Inches(1.8 + row * 2.5)
        add_card(s4, x, y, Inches(3.7), Inches(2.25), COLOR_WHITE, RGBColor(203, 213, 225))

        box = s4.shapes.add_textbox(x + Inches(0.2), y + Inches(0.2), Inches(3.3), Inches(1.85))
        tf = box.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(11)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_NAVY
        pt.space_after = Pt(6)

        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = COLOR_DARK

    # =========================================================================
    # SLIDE 5: ARSITEKTUR SISTEM & PIPELINE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_background(s5, COLOR_LIGHT_BG)
    add_header(s5, "Arsitektur Sistem & Alur Kerja Terintegrasi")

    steps = [
        ("1. Input Data Produk", "Molekul (NCE/Biologi/Generik), Manufaktur (Lokal/Impor), SRA Approval, Status BE & CPOB."),
        ("2. Rule-Based Engine", "Evaluasi PerBPOM 24/2017 & 24/2023, Klasifikasi Kategori 1-7, Jalur HK & Biaya PNBP PP 32/2017."),
        ("3. ACTD Checklist & Audit", "Verifikasi kelengkapan dokumen Modul I-IV, analisis kesenjangan (Critical / Major / Minor Gaps)."),
        ("4. Dossier Evaluator", "Simulasi penilaian evaluator BPOM, kalkulasi skor kepatuhan (0-100%), dan penentuan vonis MS / TD / TMS."),
        ("5. Output & Ekspor", "Tampilan interaktif Web UI, draft resmi Surat Tambahan Data, serta unduhan dokumen Word (.docx).")
    ]

    for idx, (title, desc) in enumerate(steps):
        x = Inches(0.8 + idx * 2.38)
        y = Inches(2.2)
        add_card(s5, x, y, Inches(2.2), Inches(3.8), COLOR_WHITE, COLOR_BLUE)

        box = s5.shapes.add_textbox(x + Inches(0.15), y + Inches(0.3), Inches(1.9), Inches(3.2))
        tf = box.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_NAVY
        pt.space_after = Pt(10)

        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10)
        pd.font.color.rgb = COLOR_DARK

    # =========================================================================
    # SLIDE 6: FITUR UTAMA 1 - PATHWAY & TARIF PNBP
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_background(s6, COLOR_LIGHT_BG)
    add_header(s6, "Fitur 1: Penentuan Jalur Registrasi & Kalkulator PNBP")

    # Left Card
    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), COLOR_WHITE, RGBColor(226, 232, 240))
    lbox = s6.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.3))
    ltf = lbox.text_frame
    ltf.word_wrap = True
    lp0 = ltf.paragraphs[0]
    lp0.text = "Logika Penentuan Kategori & Jalur (Hari Kerja)"
    lp0.font.size = Pt(14)
    lp0.font.bold = True
    lp0.font.color.rgb = COLOR_NAVY
    lp0.space_after = Pt(10)

    items_left = [
        "Kategori 1 (NCE / Produk Biologi Baru / Biosimilar)",
        "Kategori 2 (Indikasi Baru / Posologi Baru)",
        "Kategori 3 (Bentuk Sediaan Baru / Rute Baru / Kekuatan Baru)",
        "Kategori 4 (Obat Copy dengan Uji Bioekivalensi / Biowaiver BCS)",
        "Kategori 5 & 6 (Obat Copy tanpa Uji BE / Perubahan Tertentu)",
        "Jalur Khusus 40 HK: Program kesehatan nasional / darurat.",
        "Jalur 100 HK: Obat Copy BE standar & Obat Baru via Reliance SRA.",
        "Jalur 120 HK: Biosimilar terdaftar SRA via Reliance Parsial.",
        "Jalur 150 HK: Kategori 2 & 3 modifikasi bentuk sediaan.",
        "Jalur 300 HK: Evaluasi penuh Komnas Penilai Obat untuk NCE lokal/non-SRA."
    ]
    for it in items_left:
        p = ltf.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_DARK

    # Right Card
    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), COLOR_WHITE, RGBColor(226, 232, 240))
    rbox = s6.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.3))
    rtf = rbox.text_frame
    rtf.word_wrap = True
    rp0 = rtf.paragraphs[0]
    rp0.text = "Tarif Resmi PNBP BPOM (PP No. 32 Tahun 2017)"
    rp0.font.size = Pt(14)
    rp0.font.bold = True
    rp0.font.color.rgb = COLOR_NAVY
    rp0.space_after = Pt(10)

    fees_items = [
        ("Pra-Registrasi (Semua Kategori)", "Rp 1.000.000"),
        ("Registrasi Baru Kategori 1 (NCE / Biologi)", "Rp 100.000.000"),
        ("Registrasi Baru Kategori 2 (Indikasi Baru)", "Rp 75.000.000"),
        ("Registrasi Baru Kategori 3 (Bentuk/Dosis Baru)", "Rp 50.000.000"),
        ("Registrasi Kategori 4 (Obat Copy dengan Uji BE)", "Rp 30.000.000"),
        ("Registrasi Kategori 5 (Obat Copy Standar)", "Rp 20.000.000"),
        ("Penilaian CPOB Luar Negeri (Desk Evaluation)", "Rp 10.000.000"),
        ("Inspeksi CPOB Luar Negeri (On-site)", "Rp 50.000.000")
    ]
    for name, fee in fees_items:
        p = rtf.add_paragraph()
        p.text = f"• {name} : {fee}"
        p.font.size = Pt(10)
        p.font.bold = True if "Rp 100" in fee or "Rp 30" in fee else False
        p.font.color.rgb = COLOR_EMERALD if "Rp 100" in fee or "Rp 30" in fee else COLOR_DARK

    # =========================================================================
    # SLIDE 7: FITUR UTAMA 2 - DAFTAR PERIKSA MODUL ACTD
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_background(s7, COLOR_LIGHT_BG)
    add_header(s7, "Fitur 2: Daftar Periksa Modul ACTD (Parts I - IV)")

    actd_modules = [
        ("Part I: Administratif & Legal",
         "• Surat Pengantar & Pernyataan Komitmen Pendaftar\n• Izin Industri Farmasi & Sertifikat CPOB\n• CPP Format WHO & Letter of Authorization (LoA)\n• Naskah Brosur Pasien (PIL) Bahasa Indonesia\n• Pernyataan Keabsahan Dokumen & Status Halal (UU JPH)"),
        ("Part II: Mutu / CMC (Quality)",
         "• Ringkasan Dokumen Mutu (QOS)\n• Zat Aktif (S1-S7): Sintesis, Impuritas Nitrosamin/ICH Q3D\n• Produk Jadi (P1-P8): Formula & Pengembangan\n• Laporan Validasi Proses 3 Bets Komersial\n• Stabilitas Zona IVb (30°C/75% RH) real-time & accelerated"),
        ("Part III: Dokumen Non-Klinis",
         "• Ringkasan Studi Non-Klinis (Overview)\n• Studi Farmakodinamika & Farmakokinetika in vitro/in vivo\n• Studi Toksikologi GLP komparatif\n• ⚡ Auto-Waiver: Otomatis Dikecualikan untuk Obat Copy/Generik."),
        ("Part IV: Dokumen Klinis & BE",
         "• Laporan Uji Bioekivalensi (BE) in vivo vs Inovator Resmi BPOM\n• Uji Disolusi Terbanding (UDT) 3 pH Media (f2 >= 50)\n• Uji Klinis Komparatif Fase 1 & 3 Efikasi/Keamanan (Biologi)\n• Rencana Manajemen Risiko (RMP) & Farmakovigilans")
    ]

    for idx, (title, desc) in enumerate(actd_modules):
        x = Inches(0.8 + (idx % 2) * 5.9)
        y = Inches(1.8 + (idx // 2) * 2.5)
        add_card(s7, x, y, Inches(5.6), Inches(2.25), COLOR_WHITE, RGBColor(226, 232, 240))

        box = s7.shapes.add_textbox(x + Inches(0.25), y + Inches(0.2), Inches(5.1), Inches(1.85))
        tf = box.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_NAVY
        pt.space_after = Pt(6)

        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = COLOR_DARK

    # =========================================================================
    # SLIDE 8: FITUR UTAMA 3 - AUDIT KESENJANGAN (GAP-CHECK)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_background(s8, COLOR_LIGHT_BG)
    add_header(s8, "Fitur 3: Audit Kesenjangan Dossier Pra-Pengajuan (Gap-Check)")

    gap_categories = [
        ("CRITICAL GAPS (Temuan Kritis)", COLOR_RED,
         "Menyebabkan penolakan mutlak (Pre-reg rejection / SHPR Ditolak):\n"
         "• Stabilitas hanya diuji pada Zona II (25°C/60% RH) - tanpa data Zona IVb.\n"
         "• CPP tidak sesuai skema WHO atau telah habis masa berlakunya.\n"
         "• Pabrik luar negeri belum memiliki status pengakuan CPOB BPOM RI.\n"
         "• Uji BE menggunakan komparator asing yang belum diakui BPOM."),
        ("MAJOR GAPS (Temuan Mayor)", COLOR_AMBER,
         "Memicu Surat Permintaan Tambahan Data (TD) dengan clock-stop 20 HK:\n"
         "• Validasi proses komersial belum lengkap 3 bets (hanya 1 bets/protokol).\n"
         "• Laporan Uji Disolusi Terbanding (UDT) 3 pH media belum lengkap.\n"
         "• Brosur Pasien (PIL) belum tersedia dalam terjemahan resmi Bahasa Indonesia.\n"
         "• Durasi pengujian stabilitas real-time Zona IVb kurang dari 6 bulan."),
        ("MINOR GAPS (Temuan Minor)", COLOR_MUTED,
         "Catatan minor yang diselesaikan sebelum penerbitan Izin Edar (NIE):\n"
         "• Surat komitmen pengujian stabilitas lanjutan belum dilampirkan.\n"
         "• Penyesuaian redaksional tata letak kemasan dus / blister (mockup).\n"
         "• Surat pernyataan asal bahan baku porcine/non-porcine.")
    ]

    for idx, (title, color, desc) in enumerate(gap_categories):
        x = Inches(0.8 + idx * 3.9)
        y = Inches(1.8)
        add_card(s8, x, y, Inches(3.7), Inches(4.8), COLOR_WHITE, color)

        box = s8.shapes.add_textbox(x + Inches(0.25), y + Inches(0.3), Inches(3.2), Inches(4.2))
        tf = box.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = color
        pt.space_after = Pt(12)

        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10)
        pd.font.color.rgb = COLOR_DARK

    # =========================================================================
    # SLIDE 9: FITUR UTAMA 4 - EVALUASI DOSSIER & SURAT TD
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_background(s9, COLOR_LIGHT_BG)
    add_header(s9, "Fitur 4: Evaluasi Dossier Komprehensif & Generator Surat TD")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), COLOR_WHITE, RGBColor(226, 232, 240))
    b1 = s9.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.3))
    tf1 = b1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "Sistem Penilaian & Status Keputusan BPOM"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(10)

    verdicts = [
        ("🟢 MEMENUHI SYARAT (MS) - Skor >= 90%", "Seluruh dokumen administratif, mutu, non-klinis, dan klinis lengkap tanpa defisiensi kritis/mayor. Direkomendasikan untuk penerbitan Izin Edar (NIE)."),
        ("🟡 PERMINTAAN TAMBAHAN DATA (TD) - Skor 60-89%", "Dossier layak diproses bersyarat. Terdapat kekurangan data mayor yang harus dipenuhi oleh pendaftar dalam batas waktu 20 Hari Kerja."),
        ("🔴 TIDAK MEMENUHI SYARAT (TMS) - Skor < 60%", "Terdapat defisiensi fatal yang melanggar kriteria registrasi BPOM. Permohonan izin edar dinyatakan ditolak / batal demi hukum.")
    ]
    for v_title, v_desc in verdicts:
        pv = tf1.add_paragraph()
        pv.text = v_title
        pv.font.size = Pt(11)
        pv.font.bold = True
        pv.font.color.rgb = COLOR_NAVY
        pv.space_after = Pt(2)
        pd = tf1.add_paragraph()
        pd.text = v_desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = COLOR_DARK
        pd.space_after = Pt(8)

    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), COLOR_WHITE, RGBColor(226, 232, 240))
    b2 = s9.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.3))
    tf2 = b2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "Otomatisasi Konsep Surat Permintaan Tambahan Data"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(10)

    td_features = [
        "Mengadopsi format resmi Surat Dinas Direktorat Registrasi Obat BPOM RI.",
        "Mencantumkan nomor surat resmi, identitas obat, dan batas waktu 20 Hari Kerja sesuai Pasal 29 PerBPOM 24/2017.",
        "Menyusun daftar pertanyaan teknis evaluator secara butir per butir berdasarkan temuan kesenjangan spesifik.",
        "Dilengkapi fitur satu klik 'Salin Naskah' ke clipboard.",
        "Dapat diekspor secara otomatis ke dalam dokumen Word (.docx) lengkap dengan tabel penilaian per modul dan kolom tanda tangan evaluator."
    ]
    for feat in td_features:
        pf = tf2.add_paragraph()
        pf.text = f"✓ {feat}"
        pf.font.size = Pt(10)
        pf.font.color.rgb = COLOR_DARK
        pf.space_after = Pt(6)

    # =========================================================================
    # SLIDE 10: HASIL PENGUJIAN 3 SKENARIO REALISTIS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_background(s10, COLOR_LIGHT_BG)
    add_header(s10, "Validasi Sistem: Pengujian 3 Skenario Kasus Nyata")

    scenarios = [
        ("Skenario 1: Biologi Impor (Trastuzumab Biosimilar 440mg)", COLOR_BLUE,
         "• Asal: Impor Belanda (EU), disetujui EMA & Health Canada\n"
         "• Kategori: Kategori 1 (Produk Biologi / Biosimilar)\n"
         "• Jalur Evaluasi: Jalur 120 HK (Reliance Parsial SRA)\n"
         "• Waktu Total: 140 Hari Kerja (~9 Bulan Kalender)\n"
         "• Total PNBP: Rp 111.000.000 (Pra-reg + Kat 1 + Desk CPOB LN)\n"
         "• Status: MEMENUHI SYARAT (MS) - Skor 100%"),
        ("Skenario 2: Generik Lokal (Metformin HCl 500mg Tablet)", COLOR_TEAL,
         "• Asal: Manufaktur Lokal Cikarang, Jawa Barat\n"
         "• Kategori: Kategori 4 (Obat Copy dengan Uji Bioekivalensi)\n"
         "• Jalur Evaluasi: Jalur 100 HK (Obat Copy BE Terstandar)\n"
         "• Waktu Total: 120 Hari Kerja (~7.7 Bulan Kalender)\n"
         "• Total PNBP: Rp 31.000.000 (Pra-reg + Kat 4)\n"
         "• Modul Non-Klinis: WAIVED (Dikecualikan)\n"
         "• Status: MEMENUHI SYARAT BERSYARAT (TD) jika UDT belum ada"),
        ("Skenario 3: Audit Gap-Check (Dossier Onkologi Impor Pemetrexed)", COLOR_RED,
         "• Asal: Impor Luar Negeri dengan 8 Defisiensi\n"
         "• Temuan Kritis: Hanya Zona II (bukan IVb), CPP kedaluwarsa, belum ada pengakuan CPOB BPOM, komparator BE tidak diakui\n"
         "• Temuan Mayor: Validasi komersial belum ada, UDT absen, brosur hanya bahasa asing\n"
         "• Status: TIDAK MEMENUHI SYARAT (TMS) - Fatal Rejection")
    ]

    for idx, (title, color, desc) in enumerate(scenarios):
        x = Inches(0.8 + idx * 3.9)
        y = Inches(1.8)
        add_card(s10, x, y, Inches(3.7), Inches(4.8), COLOR_WHITE, color)

        box = s10.shapes.add_textbox(x + Inches(0.2), y + Inches(0.25), Inches(3.3), Inches(4.3))
        tf = box.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(11.5)
        pt.font.bold = True
        pt.font.color.rgb = color
        pt.space_after = Pt(10)

        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = COLOR_DARK

    # =========================================================================
    # SLIDE 11: DUKUNGAN BILINGUAL & EKSPOR WORD (.DOCX)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    apply_background(s11, COLOR_LIGHT_BG)
    add_header(s11, "Kemampuan Bilingual & Ekspor Dokumen Resmi (.docx)")

    add_card(s11, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), COLOR_WHITE, RGBColor(226, 232, 240))
    b1 = s11.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.3))
    tf1 = b1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🌐 Pengalih Bahasa Real-Time (Bilingual Engine)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(10)

    bil_items = [
        ("Bahasa Indonesia (ID)", "Dirancang khusus menggunakan terminologi baku regulasi BPOM RI (misal: Surat Izin Edar / NIE, Surat Hasil Pra-Registrasi / SHPR, Uji Disolusi Terbanding / UDT, Pelaporan MESO, dsb.)."),
        ("English (EN)", "Ditujukan bagi koordinasi internasional dengan principal luar negeri, ekspatriat RA, dan mitra lisensi global untuk menyamakan persepsi persyaratan regulasi BPOM.")
    ]
    for name, desc in bil_items:
        pn = tf1.add_paragraph()
        pn.text = name
        pn.font.size = Pt(11)
        pn.font.bold = True
        pn.font.color.rgb = COLOR_BLUE
        pn.space_after = Pt(2)
        pd = tf1.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = COLOR_DARK
        pd.space_after = Pt(10)

    add_card(s11, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), COLOR_WHITE, RGBColor(226, 232, 240))
    b2 = s11.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.3))
    tf2 = b2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "📄 Ekspor Microsoft Word (.docx) Otomatis"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(10)

    docx_features = [
        "Format Eksekutif Resmi: Header, footer 'CONFIDENTIAL', margin standar regulasi.",
        "Tabel Tarif PNBP & Timeline: Berisi rincian kode biaya, landasan hukum PP 32/2017, dan total tagihan SIMPONI.",
        "Tabel Daftar Periksa ACTD: Berisi modul lengkap Part I-IV dengan status [WAJIB] atau [WAIVED].",
        "Laporan Audit Gap-Check: Tabel berkode warna (Merah: Kritis, Oranye: Mayor, Hijau: Memenuhi Syarat) disertai langkah remediasi.",
        "Laporan Evaluasi Dossier: Skor kepatuhan, catatan evaluator BPOM, draf Surat Tambahan Data, dan kolom tanda tangan evaluator/PJT."
    ]
    for feat in docx_features:
        pf = tf2.add_paragraph()
        pf.text = f"• {feat}"
        pf.font.size = Pt(9.5)
        pf.font.color.rgb = COLOR_DARK
        pf.space_after = Pt(6)

    # =========================================================================
    # SLIDE 12: PANDUAN PENGGUNAAN APLIKASI
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    apply_background(s12, COLOR_LIGHT_BG)
    add_header(s12, "Panduan Akses & Implementasi Aplikasi")

    usage_steps = [
        ("Metode 1: Double-Click Launcher", "Cukup klik dua kali berkas 'run_app.bat' di direktori project. Server akan langsung aktif dan otomatis membuka browser di http://127.0.0.1:5000."),
        ("Metode 2: Terminal / PowerShell", "Jalankan perintah:\npython app.py\nServer lokal akan melayani peramban web pada port 5000."),
        ("Metode 3: CLI Programmatic Batch", "Jalankan evaluasi langsung dari terminal menggunakan argumen:\npython bpom_ra_agent/cli.py --scenario 1 --lang ID\nMenghasilkan berkas Word secara instan.")
    ]

    for idx, (title, desc) in enumerate(usage_steps):
        x = Inches(0.8 + idx * 3.9)
        y = Inches(1.8)
        add_card(s12, x, y, Inches(3.7), Inches(4.8), COLOR_WHITE, COLOR_NAVY)

        box = s12.shapes.add_textbox(x + Inches(0.25), y + Inches(0.3), Inches(3.2), Inches(4.2))
        tf = box.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_NAVY
        pt.space_after = Pt(12)

        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10)
        pd.font.color.rgb = COLOR_DARK

    # =========================================================================
    # SLIDE 13: KESIMPULAN & NILAI BISNIS (Conclusion)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    apply_background(s13, COLOR_NAVY)

    cbox = s13.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(11.0), Inches(4.5))
    ctf = cbox.text_frame
    ctf.word_wrap = True

    cp0 = ctf.paragraphs[0]
    cp0.text = "KESIMPULAN & MANFAAT STRATEGIS"
    cp0.font.size = Pt(13)
    cp0.font.bold = True
    cp0.font.color.rgb = COLOR_TEAL
    cp0.space_after = Pt(10)

    cp1 = ctf.add_paragraph()
    cp1.text = "Akselerasi Izin Edar & Kepatuhan Regulasi BPOM"
    cp1.font.size = Pt(28)
    cp1.font.bold = True
    cp1.font.color.rgb = COLOR_WHITE
    cp1.space_after = Pt(16)

    benefits = [
        "⚡ Menghemat waktu analisis regulasi hingga 80% bagi tim Regulatory Affairs.",
        "🛡️ Mencegah kerugian finansial akibat penolakan pra-registrasi dan denda keterlambatan izin edar.",
        "📊 Menyediakan audit trail dan dokumentasi Word resmi yang siap diserahkan ke manajemen maupun auditor.",
        "🤝 Menjembatani komunikasi regulasi antara prinsipal farmasi multinasional dan persyaratan lokal BPOM RI."
    ]
    for b in benefits:
        pb = ctf.add_paragraph()
        pb.text = b
        pb.font.size = Pt(13)
        pb.font.color.rgb = RGBColor(226, 232, 240)
        pb.space_after = Pt(8)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"PowerPoint Presentation successfully saved to: {output_path}")

if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(__file__), "outputs", "BPOM_Drug_Regulatory_Affairs_AI_Assistant_Presentation.pptx")
    create_presentation(out_file)
