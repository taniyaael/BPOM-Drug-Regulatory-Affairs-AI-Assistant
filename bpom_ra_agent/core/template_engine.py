"""Regulatory Document Templates Engine for BPOM Submissions.
Generates standard official templates in English and Bahasa Indonesia:
1. Formal BPOM Registration Cover Letter (Surat Pengantar Registrasi Obat)
2. BCS Biowaiver Justification Statement (Justifikasi Ilmiah Biowaiver BCS)
3. Ongoing Zone IVb Stability Commitment Letter (Surat Komitmen Uji Stabilitas Zona IVb)
4. Biosimilar Comparability & Pharmacovigilance Statement
"""

from typing import Dict, Any

class RegulatoryTemplateEngine:

    @staticmethod
    def get_cover_letter_id(company_name: str, pjt_name: str, stra_number: str,
                            product_name: str, active_substance: str, dosage_form: str,
                            strength: str, category_name: str, track_name: str) -> str:
        """Generates standard official Indonesian BPOM Cover Letter."""
        return f"""KOP SURAT INDUSTRI FARMASI
{company_name.upper()}
Alamat Terdaftar, Jakarta, Indonesia | Telp: (021) 555-XXXX | Email: regulatory@{company_name.lower().replace(' ', '')}.co.id
__________________________________________________________________________________________________

Nomor    : REG/BPOM/{product_name.replace(' ', '_').upper()}/2026
Lampiran : 1 (satu) Berkas Dokumen Registrasi Format ACTD
Perihal  : Permohonan Registrasi Obat - {product_name} ({category_name})

Kepada Yth.
Kepala Badan Pengawas Obat dan Makanan Republik Indonesia
c.q. Deputi Bidang Pengawasan Obat, Narkotika, Psikotropika, Prekursor, dan Zat Adiktif
Direktur Registrasi Obat
Jl. Percetakan Negara No. 23, Jakarta Pusat 10560

Dengan hormat,

Sehubungan dengan rencana peredaran produk farmasi yang bermutu, berkhasiat, dan aman di wilayah Republik Indonesia, bersama ini kami dari PT. {company_name} bertindak sebagai pemegang Izin Industri Farmasi mengajukan permohonan registrasi obat dengan rincian data sebagai berikut:

1. Nama Dagang Obat        : {product_name}
2. Nama Zat Aktif (INN)    : {active_substance}
3. Bentuk Sediaan & Rute   : {dosage_form}
4. Kekuatan / Dosis        : {strength}
5. Kategori Registrasi     : {category_name}
6. Jalur Evaluasi          : {track_name}

Sebagai kelengkapan administrasi dan teknis, bersama surat ini kami lampirkan:
a. Bukti Pembayaran PNBP (Surat Setoran Bukan Pajak - SIMPONI) Pra-Registrasi dan Registrasi;
b. Surat Hasil Pra-Registrasi (SHPR) BPOM RI;
c. Dokumen Teknis Format ACTD (Part I Administratif, Part II Mutu, Part III Non-Klinis, Part IV Klinis);
d. Data Stabilitas Kondisi Iklim Zona IVb (30°C ± 2°C / 75% ± 5% RH) dan Surat Komitmen Stabilitas;
e. Dokumen Pemenuhan CPOB Fasilitas Manufaktur dan Pernyataan Jaminan Keaslian Dokumen.

Kami menyatakan dengan sesungguhnya bahwa seluruh data dan dokumen yang diserahkan adalah benar, sah, dan dapat dipertanggungjawabkan sesuai ketentuan perundang-undangan yang berlaku.

Demikian permohonan ini kami sampaikan. Atas perhatian, bimbingan, dan kerjasama Bapak/Ibu Direktur Registrasi Obat beserta tim penilai BPOM RI, kami ucapkan terima kasih.


Hormat kami,
PT. {company_name}


[Tanda Tangan & Materai Rp 10.000]


{pjt_name}, S.Farm., Apt.
Apoteker Penanggung Jawab Teknis (PJT) / Head of Regulatory Affairs
STRA No. : {stra_number}
"""

    @staticmethod
    def get_cover_letter_en(company_name: str, pjt_name: str, stra_number: str,
                            product_name: str, active_substance: str, dosage_form: str,
                            strength: str, category_name: str, track_name: str) -> str:
        """Generates standard English version of BPOM Cover Letter."""
        return f"""COMPANY LETTERHEAD
{company_name.upper()}
Registered Office, Jakarta, Indonesia | Phone: +62-21-555-XXXX | Email: regulatory@{company_name.lower().replace(' ', '')}.co.id
__________________________________________________________________________________________________

Ref No.   : REG/BPOM/{product_name.replace(' ', '_').upper()}/2026
Enclosure : 1 (One) Complete ACTD Dossier Submission Package
Subject   : Marketing Authorization Application for {product_name} ({category_name})

To:
Head of the Indonesian Food and Drug Authority (Badan POM RI)
c.q. Deputy for Therapeutic Products, Narcotics, Psychotropics, and Addictive Substances
Director of Drug Registration
Jl. Percetakan Negara No. 23, Central Jakarta 10560, Indonesia

Dear Director of Drug Registration,

In accordance with prevailing drug regulations in the Republic of Indonesia (BPOM Regulation No. 24 of 2017 jo. BPOM Reg No. 13 of 2021 & Reg No. 24 of 2023), PT. {company_name}, as a licensed Indonesian Pharmaceutical Industry, hereby formally submits an application for marketing authorization for the following medicinal product:

1. Proprietary / Brand Name: {product_name}
2. Active Substance (INN)   : {active_substance}
3. Dosage Form & Route      : {dosage_form}
4. Strength / Concentration : {strength}
5. Registration Category   : {category_name}
6. Evaluation Pathway       : {track_name}

In support of this application, we enclose the following documentation:
a. Official Non-Tax State Revenue (PNBP SIMPONI) payment receipts for Pre-Registration and Registration;
b. Valid Pre-Registration Assessment Outcome Letter (SHPR) issued by BPOM RI;
c. Complete ASEAN Common Technical Dossier (ACTD) Parts I through IV;
d. Finished product stability study reports conducted under ASEAN Climatic Zone IVb (30°C ± 2°C / 75% ± 5% RH) along with formal Stability Commitment Letter;
e. GMP Compliance Certificates for all involved manufacturing sites and Applicant Commitment Statements.

We hereby certify and declare under full legal responsibility that all scientific data and administrative documentation submitted herein are authentic, accurate, and fully conform to all regulatory requirements established by Badan POM RI.

Thank you very much for your kind consideration and assistance during this regulatory review.


Yours sincerely,
For and on behalf of PT. {company_name}


[Signature & Legal Stamp]


{pjt_name}, Pharmacist
Pharmacist-in-Charge / Head of Regulatory Affairs
Registered Pharmacist License (STRA) No. : {stra_number}
"""

    @staticmethod
    def get_stability_commitment_letter(company_name: str, product_name: str,
                                       language: str = "ID") -> str:
        """Generates formal Stability Commitment Letter for Climatic Zone IVb."""
        if language == "ID":
            return f"""SURAT PERNYATAAN KOMITMEN PELAKSANAAN UJI STABILITAS ZONA IKLIM IVb
PT. {company_name.upper()}

Yang bertanda tangan di bawah ini:
Nama                  : Apoteker Penanggung Jawab Mutu / Regulatory Affairs
Jabatan               : Quality Assurance / Regulatory Affairs Manager
Nama Perusahaan       : PT. {company_name}

Menyatakan dengan sesungguhnya terkait produk:
Nama Produk           : {product_name}
Bentuk Sediaan        : Sediaan Farmasi Terdaftar
Kondisi Penyimpanan   : Simpan pada suhu di bawah 30°C, terlindung dari cahaya dan kelembapan.

Dengan ini kami memberikan komitmen tertulis kepada Badan Pengawas Obat dan Makanan (BPOM) Republik Indonesia bahwa:
1. Kami berkomitmen untuk melanjutkan pelaksanaan uji stabilitas jangka panjang (real-time stability testing) pada kondisi Zona Iklim IVb (suhu 30°C ± 2°C dan kelembapan relatif 75% ± 5% RH) terhadap 3 (tiga) bets produksi komersial hingga masa kedaluwarsa penuh yang diajukan.
2. Kami berkomitmen untuk melaporkan secara berkala setiap hasil uji di luar spesifikasi (Out of Specification / OOS) atau kecenderungan penurunan mutu kepada BPOM RI.
3. Apabila di kemudian hari terbukti terdapat ketidakstabilan produk selama pengujian real-time, kami bersedia menarik produk dari peredaran dan menerima sanksi administratif sesuai peraturan perundang-undangan yang berlaku.

Demikian surat komitmen ini dibuat dengan sebenarnya dan penuh rasa tanggung jawab.

Jakarta, 2026
PT. {company_name}

[Materai Rp 10.000 & Tanda Tangan]
"""
        else:
            return f"""FORMAL COMMITMENT LETTER FOR ONGOING STABILITY TESTING UNDER CLIMATIC ZONE IVb
PT. {company_name.upper()}

The undersigned:
Name                  : Pharmacist-in-Charge of Quality Assurance / Regulatory Affairs
Title                 : QA & Regulatory Affairs Director
Company Name          : PT. {company_name}

Hereby formally declares and commits regarding the medicinal product:
Product Name          : {product_name}
Storage Condition     : Store below 30°C, protect from excessive heat, light, and moisture.

We hereby submit this binding commitment to the Indonesian Food and Drug Authority (Badan POM RI):
1. We commit to continue long-term real-time stability studies under ASEAN Climatic Zone IVb conditions (30°C ± 2°C / 75% ± 5% RH) on three consecutive commercial production batches throughout the entire claimed shelf-life.
2. We commit to immediately notify Badan POM RI in the event of any Out-of-Specification (OOS) results or adverse stability trends observed during ongoing testing.
3. If real-time stability results fail to substantiate the approved shelf-life, we commit to implement immediate corrective actions, including voluntary batch recall if warranted.

Issued in good faith and under full regulatory accountability.

Jakarta, 2026
PT. {company_name}

[Authorized Signatory & Company Seal]
"""
