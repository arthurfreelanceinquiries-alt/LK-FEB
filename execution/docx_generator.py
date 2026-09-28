"""
execution/docx_generator.py
===========================
Script generator proposal Word (.docx) resmi BEM FEB UKRIDA.
Mengikuti standar baku tipografi, margin, dan layout:
- 00_SISTEM_BEM/PRD_TIPOGRAFI_MARGIN_TYPO.md
- Kop surat resmi BEM FEB UKRIDA & UKRIDA (Dual Logo)
- Standar margin: Atas 2.5 cm, Bawah 2.5 cm, Kiri 3.0 cm, Kanan 2.5 cm
- Font: Times New Roman, line spacing 1.5 pt (body), 1.0 pt (tabel)

Penggunaan:
    py -X utf8 execution/docx_generator.py
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn


def set_cell_border(cell, **kwargs):
    """Mengatur border sel tabel docx."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="{kwargs.get("top", "single")}" w:sz="{kwargs.get("top_sz", "4")}" w:space="0" w:color="{kwargs.get("top_color", "BDC3C7")}"/>\n'
        f'  <w:left w:val="{kwargs.get("left", "none")}" w:sz="{kwargs.get("left_sz", "4")}" w:space="0" w:color="{kwargs.get("left_color", "BDC3C7")}"/>\n'
        f'  <w:bottom w:val="{kwargs.get("bottom", "single")}" w:sz="{kwargs.get("bottom_sz", "4")}" w:space="0" w:color="{kwargs.get("bottom_color", "BDC3C7")}"/>\n'
        f'  <w:right w:val="{kwargs.get("right", "none")}" w:sz="{kwargs.get("right_sz", "4")}" w:space="0" w:color="{kwargs.get("right_color", "BDC3C7")}"/>\n'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)


def set_cell_shading(cell, color_hex):
    """Memberikan latar belakang warna pada sel."""
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    """Memberikan padding internal pada sel (dalam dxa, 20 dxa = 1 pt)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>\n'
        f'  <w:top w:w="{top}" w:type="dxa"/>\n'
        f'  <w:bottom w:w="{bottom}" w:type="dxa"/>\n'
        f'  <w:left w:w="{left}" w:type="dxa"/>\n'
        f'  <w:right w:w="{right}" w:type="dxa"/>\n'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def add_bab_heading(doc, text):
    """Menambahkan Heading Bab (I. LATAR BELAKANG, dll)."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True
    r.font.color.rgb = RGBColor(20, 30, 55)
    return p


def add_sub_heading(doc, text):
    """Menambahkan Sub-Heading (A. TUJUAN KEGIATAN, dll)."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True
    return p


def add_body_paragraph(doc, text, space_after=6):
    """Menambahkan paragraf isi dengan format standar (Justify, 1.5 line spacing)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    return p


def add_numbered_item(doc, num_str, text):
    """Menambahkan butir poin terurut."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.first_line_indent = Cm(-0.8)
    p.paragraph_format.line_spacing = 1.25
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    
    r_num = p.add_run(num_str + " ")
    r_num.font.name = "Times New Roman"
    r_num.font.size = Pt(12)
    r_num.bold = True
    
    r_txt = p.add_run(text)
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(12)
    return p


def format_table(table, col_widths, headers, data, alignments=None):
    """Memformat tabel profesional dengan header shaded dan cell padding."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Header Row
    hdr_cells = table.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = h_text
        set_cell_shading(hdr_cells[i], "EAECEE")
        set_cell_border(hdr_cells[i], top="single", top_color="566573", bottom="single", bottom_color="566573")
        set_cell_margins(hdr_cells[i], top=140, bottom=140, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        for run in p.runs:
            run.font.name = "Times New Roman"
            run.font.size = Pt(10.5)
            run.bold = True
            run.font.color.rgb = RGBColor(27, 38, 59)
            
    # Data Rows
    for r_idx, row_data in enumerate(data):
        row_cells = table.add_row().cells
        bg_color = "FDFEFE" if r_idx % 2 == 0 else "F8F9F9"
        for c_idx, cell_value in enumerate(row_data):
            row_cells[c_idx].text = str(cell_value)
            set_cell_shading(row_cells[c_idx], bg_color)
            set_cell_border(row_cells[c_idx], top="single", top_color="D5D8DC", bottom="single", bottom_color="D5D8DC")
            set_cell_margins(row_cells[c_idx], top=100, bottom=100, left=140, right=140)
            p = row_cells[c_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            
            # Alignments
            if alignments and c_idx < len(alignments):
                p.alignment = alignments[c_idx]
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(10)
                
    # Set widths
    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width


def generate_proposal_docx(output_path="01_Proposal/OMGTC_2026/Proposal_OMGTC_FEB_UKRIDA_2026.docx"):
    """Fungsi utama pembuatan dokumen Word Proposal OMGTC 2026."""
    doc = docx.Document()
    
    # 1. Konfigurasi Margin Halaman A4 Sesuai PRD
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(3.0)  # Binding margin
        section.right_margin = Cm(2.5)
        
    ukrida_logo = "04_Arsip_Acara/OPTIK_MELAWAI_2026/ukrida_logo_tight.png"
    bem_logo = "04_Arsip_Acara/OPTIK_MELAWAI_2026/BEM_FEB_LOGO_tight.png"
    
    # ==============================================================
    # HALAMAN COVER / JUDUL
    # ==============================================================
    p_cov_space = doc.add_paragraph()
    p_cov_space.paragraph_format.space_before = Pt(30)
    
    p_title1 = doc.add_paragraph()
    p_title1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_title1.add_run("PROPOSAL KEGIATAN")
    r_t1.font.name = "Times New Roman"
    r_t1.font.size = Pt(18)
    r_t1.bold = True
    r_t1.font.color.rgb = RGBColor(20, 30, 55)
    
    p_title2 = doc.add_paragraph()
    p_title2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title2.paragraph_format.space_before = Pt(4)
    r_t2 = p_title2.add_run("OPTIK MELAWAI GOES TO CAMPUS (OMGTC) 2026")
    r_t2.font.name = "Times New Roman"
    r_t2.font.size = Pt(15)
    r_t2.bold = True
    r_t2.font.color.rgb = RGBColor(180, 40, 40)
    
    p_theme = doc.add_paragraph()
    p_theme.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_theme.paragraph_format.space_before = Pt(8)
    p_theme.paragraph_format.space_after = Pt(36)
    r_th = p_theme.add_run('"CLEAR VISION, BRIGHT FUTURE:\nEdukasi Kesehatan Visual dan Pemeriksaan Refraksi Bersama Optik Melawai"')
    r_th.font.name = "Times New Roman"
    r_th.font.size = Pt(12)
    r_th.italic = True
    r_th.font.color.rgb = RGBColor(50, 50, 50)
    
    # Logo Tengah Bersandingan
    logo_table = doc.add_table(rows=1, cols=2)
    logo_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    logo_table.columns[0].width = Cm(5.0)
    logo_table.columns[1].width = Cm(5.0)
    
    cell_l = logo_table.cell(0, 0)
    p_l = cell_l.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if os.path.exists(ukrida_logo):
        p_l.add_run().add_picture(ukrida_logo, width=Inches(1.5))
        
    cell_r = logo_table.cell(0, 1)
    p_r = cell_r.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if os.path.exists(bem_logo):
        p_r.add_run().add_picture(bem_logo, width=Inches(1.55))
        
    p_space2 = doc.add_paragraph()
    p_space2.paragraph_format.space_before = Pt(48)
    
    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot.paragraph_format.line_spacing = 1.2
    
    r_f1 = p_foot.add_run("BADAN EKSEKUTIF MAHASISWA\n")
    r_f1.font.name = "Times New Roman"
    r_f1.font.size = Pt(13)
    r_f1.bold = True
    
    r_f2 = p_foot.add_run("FAKULTAS EKONOMI DAN BISNIS\n")
    r_f2.font.name = "Times New Roman"
    r_f2.font.size = Pt(13)
    r_f2.bold = True
    
    r_f3 = p_foot.add_run("UNIVERSITAS KRISTEN KRIDA WACANA\nJAKARTA\n2026")
    r_f3.font.name = "Times New Roman"
    r_f3.font.size = Pt(12)
    r_f3.bold = True
    
    doc.add_page_break()
    
    # ==============================================================
    # KOP SURAT RESMI (HALAMAN 2 DST)
    # ==============================================================
    kop_table = doc.add_table(rows=1, cols=3)
    kop_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    kop_table.columns[0].width = Cm(2.4)
    kop_table.columns[1].width = Cm(10.7)
    kop_table.columns[2].width = Cm(2.4)
    
    # Logo Kiri UKRIDA
    c_kl = kop_table.cell(0, 0)
    p_kl = c_kl.paragraphs[0]
    p_kl.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if os.path.exists(ukrida_logo):
        p_kl.add_run().add_picture(ukrida_logo, width=Inches(0.88))
        
    # Teks Tengah Kop
    c_kc = kop_table.cell(0, 1)
    p_kc = c_kc.paragraphs[0]
    p_kc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_kc.paragraph_format.line_spacing = 1.15
    p_kc.paragraph_format.space_before = Pt(0)
    p_kc.paragraph_format.space_after = Pt(0)
    
    rk1 = p_kc.add_run("UNIVERSITAS KRISTEN KRIDA WACANA\n")
    rk1.font.name = "Times New Roman"
    rk1.font.size = Pt(12.5)
    rk1.bold = True
    
    rk2 = p_kc.add_run("BADAN EKSEKUTIF MAHASISWA FAKULTAS EKONOMI & BISNIS\n")
    rk2.font.name = "Arial"
    rk2.font.size = Pt(9.5)
    rk2.bold = True
    rk2.font.color.rgb = RGBColor(20, 30, 55)
    
    rk3 = p_kc.add_run("Jl. Tanjung Duren Raya No. 4 Telp. 5666952-189 Fax. 5666956, Jakarta Barat 11470")
    rk3.font.name = "Times New Roman"
    rk3.font.size = Pt(8.5)
    
    # Logo Kanan BEM
    c_kr = kop_table.cell(0, 2)
    p_kr = c_kr.paragraphs[0]
    p_kr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if os.path.exists(bem_logo):
        p_kr.add_run().add_picture(bem_logo, width=Inches(0.92))
        
    # Garis Pembatas Kop Surat Ganda (Decorative Divider)
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(2)
    p_div.paragraph_format.space_after = Pt(12)
    r_div = p_div.add_run("―" * 58)
    r_div.font.name = "Arial"
    r_div.font.size = Pt(13)
    r_div.bold = True
    r_div.font.color.rgb = RGBColor(20, 30, 55)

    # ==============================================================
    # BAB I: LATAR BELAKANG
    # ==============================================================
    add_bab_heading(doc, "I. LATAR BELAKANG")
    
    add_body_paragraph(
        doc,
        "Kesehatan penglihatan merupakan salah satu pilar fundamental yang menunjang efektivitas proses pembelajaran "
        "dan produktivitas generasi muda. Di era transformasi digital saat ini, intensitas interaksi manusia dengan perangkat "
        "elektronik seperti komputer jinjing (laptop), gawai (smartphone), dan tablet mengalami lonjakan yang sangat signifikan. "
        "Berdasarkan data kesehatan global, diperkirakan lebih dari 34% populasi dunia saat ini mengalami gangguan refraksi miopia "
        "(rabun jauh), dan persentase tersebut diproyeksikan terus meningkat seiring bertambahnya beban aktivitas visual jarak dekat "
        "sehari-hari. Di Indonesia sendiri, prevalensi kelainan refraksi tergolong tinggi, khususnya pada kelompok usia produktif "
        "dan civitas akademika di perguruan tinggi."
    )
    
    add_body_paragraph(
        doc,
        "Mahasiswa Fakultas Ekonomi dan Bisnis Universitas Kristen Krida Wacana (FEB UKRIDA) memiliki tuntutan akademik yang sangat padat, "
        "mulai dari telaah literatur ilmiah, komputasi data keuangan, penyusunan analisis studi kelayakan bisnis, hingga keikutsertaan "
        "dalam berbagai forum diskusi digital. Tingginya durasi paparan layar monitor (screen time) tanpa diimbangi kesadaran akan kesehatan "
        "mata sering kali memicu keluhan ketegangan mata digital (digital eye strain), kelelahan visual (asthenopia), serta penurunan fokus belajar. "
        "Sayangnya, kondisi penurunan ketajaman penglihatan ini sering kali tidak disadari secara dini dan baru ditangani ketika telah mengganggu "
        "kenyamanan belajar maupun aktivitas perkuliahan sehari-hari."
    )
    
    add_body_paragraph(
        doc,
        "Menjawab tantangan tersebut, Badan Eksekutif Mahasiswa Fakultas Ekonomi dan Bisnis Universitas Kristen Krida Wacana (BEM FEB UKRIDA) "
        "berinisiatif menginisiasi kolaborasi strategis bersama mitra profesional penyedia layanan kesehatan mata terkemuka di Indonesia, "
        "yaitu PT. Inti Citra Agung (Optik Melawai), melalui penyelenggaraan program bertajuk \"Optik Melawai Goes To Campus (OMGTC) 2026\". "
        "Kegiatan ini dirancang sebagai bentuk pelayanan nyata kemahasiswaan yang memadukan seminar edukasi interaktif, pemeriksaan refraksi "
        "dini secara cuma-cuma, layanan perawatan kacamata, serta fasilitas Mobile Optik terpadu di lingkungan kampus. Melalui kegiatan ini, "
        "diharapkan seluruh mahasiswa dan civitas akademika FEB UKRIDA dapat memperoleh wawasan komprehensif serta akses fasilitas kesehatan "
        "visual yang prima guna menunjang kesuksesan akademik dan profesional di masa depan."
    )

    # ==============================================================
    # BAB II: TEMA KEGIATAN
    # ==============================================================
    add_bab_heading(doc, "II. TEMA KEGIATAN")
    
    p_theme_box = doc.add_paragraph()
    p_theme_box.paragraph_format.left_indent = Cm(0.5)
    p_theme_box.paragraph_format.space_before = Pt(2)
    p_theme_box.paragraph_format.space_after = Pt(6)
    r_th_b = p_theme_box.add_run(
        "\"CLEAR VISION, BRIGHT FUTURE: Edukasi Kesehatan Visual dan Pemeriksaan Refraksi Bersama Optik Melawai\""
    )
    r_th_b.font.name = "Times New Roman"
    r_th_b.font.size = Pt(12)
    r_th_b.bold = True
    
    add_body_paragraph(
        doc,
        "Tema ini merefleksikan keyakinan bahwa penglihatan yang sehat dan jernih (Clear Vision) merupakan modal dasar paling esensial "
        "bagi mahasiswa dalam menyerap ilmu pengetahuan, membangun daya saing intelektual, dan meraih masa depan yang gemilang (Bright Future). "
        "Melalui pendekatan preventif dan kuratif, kegiatan ini mengajak seluruh mahasiswa FEB UKRIDA untuk proaktif merawat kesehatan mata "
        "di tengah pesatnya dinamika digitalisasi modern."
    )

    # ==============================================================
    # BAB III: KEGIATAN
    # ==============================================================
    add_bab_heading(doc, "III. KEGIATAN")
    
    add_sub_heading(doc, "A. TUJUAN KEGIATAN")
    add_numbered_item(doc, "1.", "Meningkatkan kesadaran (awareness) mahasiswa FEB UKRIDA dan civitas akademika akan urgensi menjaga kesehatan mata serta mencegah gangguan visual akibat digital eye strain.")
    add_numbered_item(doc, "2.", "Memfasilitasi deteksi dini kelainan refraksi (miopia, hipermetropia, dan astigmatisme) bagi mahasiswa melalui pemeriksaan mata berstandar profesional tanpa dipungut biaya.")
    add_numbered_item(doc, "3.", "Memberikan pelayanan sosial perawatan kacamata berupa pencucian dan penyetelan kacamata gratis guna mendukung kenyamanan beraktivitas di lingkungan kampus.")
    add_numbered_item(doc, "4.", "Membangun kemitraan strategis yang berkelanjutan antara BEM FEB UKRIDA dengan sektor industri kesehatan dan optik profesional.")
    add_numbered_item(doc, "5.", "Mendukung terciptanya lingkungan perkuliahan yang sehat, produktif, dan berorientasi pada kesejahteraan fisik mahasiswa.")

    add_sub_heading(doc, "B. MANFAAT KEGIATAN")
    add_numbered_item(doc, "1.", "Bagi Mahasiswa: Memperoleh edukasi medis langsung dari para ahli optometri, menerima diagnosa refraksi mata secara akurat tanpa biaya, serta mendapatkan solusi perlindungan mata terjangkau.")
    add_numbered_item(doc, "2.", "Bagi BEM FEB UKRIDA: Mewujudkan program kerja pengabdian dan pelayanan mahasiswa yang berdampak nyata, meningkatkan citra kelembagaan, serta memperluas jejaring kemitraan eksternal.")
    add_numbered_item(doc, "3.", "Bagi Fakultas Ekonomi dan Bisnis UKRIDA: Mendukung pemenuhan indikator kesejahteraan mahasiswa dan mewujudkan suasana akademik kampus yang adaptif terhadap kesehatan civitas academica.")

    add_sub_heading(doc, "C. TARGET PESERTA")
    add_numbered_item(doc, "1.", "Seminar Edukasi Kesehatan Mata: 100 orang mahasiswa aktif Fakultas Ekonomi dan Bisnis UKRIDA serta perwakilan civitas akademika.")
    add_numbered_item(doc, "2.", "Pemeriksaan Refraksi & Layanan Kacamata (Booth & Mobile Optik): ± 200 hingga 300 mahasiswa, dosen, dan staf di lingkungan Kampus 1 UKRIDA.")

    add_sub_heading(doc, "D. PELAKSANAAN KEGIATAN")
    pelaksanaan_table = doc.add_table(rows=1, cols=2)
    format_table(
        pelaksanaan_table,
        [Cm(4.5), Cm(11.0)],
        ["Rincian", "Keterangan Pelaksanaan"],
        [
            ("Hari / Tanggal", "Kamis – Jumat, 10 – 11 September 2026"),
            ("Waktu Pelaksanaan", "08.30 – 16.30 WIB"),
            ("Tempat Pelaksanaan", "1. Booth Pelayanan: Junction Kampus 1 UKRIDA\n2. Mobile Optik (Bus): Area Parkir Depan Kampus 1 UKRIDA\n3. Seminar Edukasi: Auditorium Gedung A Lantai 7 Kampus 1 UKRIDA")
        ],
        [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    )

    add_sub_heading(doc, "E. NARASUMBER")
    add_numbered_item(doc, "1.", "Tim Dokter / Optometris Spesialis PT. Inti Citra Agung (Optik Melawai) — Topik: \"Mengenal Computer Vision Syndrome: Kiat Menjaga Ketajaman Visual Mahasiswa di Era Digital\"")
    add_numbered_item(doc, "2.", "Tim Konsultan Edukasi Kesehatan Visual Optik Melawai — Topik: \"Pencegahan Progresivitas Miopia dan Pemilihan Solusi Lensa Optik Ergonomis\"")

    add_sub_heading(doc, "F. SUSUNAN ACARA / RUNDOWN")
    
    p_rd1 = doc.add_paragraph()
    p_rd1.paragraph_format.space_before = Pt(4)
    p_rd1.paragraph_format.space_after = Pt(2)
    p_rd1.add_run("HARI PERTAMA: Kamis, 10 September 2026 (Aktivasi Pelayanan & Pemeriksaan Refraksi)").bold = True

    rundown_d1 = [
        ("08.00 – 08.30", "30", "Briefing Panitia BEM FEB dan Tim Teknis Optik Melawai", "Junction & Parkiran", "Divisi Acara & Ketua Pelaksana"),
        ("08.30 – 09.00", "30", "Persiapan Akhir (Final Checking) Booth & Mobile Optik Bus", "Junction & Parkiran", "Divisi Perlengkapan"),
        ("09.00 – 09.15", "15", "Seremoni Pembukaan Pelayanan OMGTC 2026 oleh Ketua BEM", "Junction Kampus 1", "Divisi Acara & Ketum BEM"),
        ("09.15 – 12.00", "165", "Pelayanan Sesi Pagi:\n- Pemeriksaan Refraksi Mata Komputerisasi (Gratis)\n- Penyetelan & Pencucian Kacamata (Gratis)\n- Edukasi Interaktif & Games Berhadiah", "Junction & Parkiran", "Panitia & Tim Mitra"),
        ("12.00 – 13.00", "60", "Ishoma (Istirahat, Sholat, Makan Siang Panitia & Tim Mitra)", "Posko Panitia", "Divisi Konsumsi"),
        ("13.00 – 16.00", "180", "Pelayanan Sesi Siang:\n- Lanjutan Pemeriksaan Mata & Uji ACP\n- Layanan Edging / Pasang Lensa di Bus Mobile\n- Bazar Kacamata & Promo Khusus Mahasiswa", "Junction & Parkiran", "Panitia & Tim Mitra"),
        ("16.00 – 16.30", "30", "Closing Booth Day 1 & Evaluasi Harian Panitia", "Posko Panitia", "Seluruh Panitia"),
    ]
    t_rd1 = doc.add_table(rows=1, cols=5)
    format_table(
        t_rd1,
        [Cm(2.6), Cm(1.6), Cm(5.6), Cm(2.7), Cm(3.0)],
        ["Waktu", "Durasi", "Kegiatan", "Lokasi", "PJ"],
        rundown_d1,
        [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    )

    p_rd2 = doc.add_paragraph()
    p_rd2.paragraph_format.space_before = Pt(8)
    p_rd2.paragraph_format.space_after = Pt(2)
    p_rd2.add_run("HARI KEDUA: Jumat, 11 September 2026 (Seminar Edukasi & Pelayanan Terpadu)").bold = True

    rundown_d2 = [
        ("08.00 – 08.30", "30", "Briefing Panitia Gabungan & Pengecekan Sistem Audio Visual", "Auditorium Gd. A", "Divisi Acara & Perlengkapan"),
        ("08.30 – 09.00", "30", "Registrasi Peserta Seminar & Pembagian Seminar Kit", "Foyer Auditorium", "Divisi Acara & Humas"),
        ("09.00 – 09.10", "10", "Pembukaan Seminar oleh MC & Doa Pembuka", "Auditorium Gd. A", "MC Divisi Acara"),
        ("09.10 – 09.20", "10", "Menyanyikan Lagu Indonesia Raya & Mars UKRIDA", "Auditorium Gd. A", "Operator Pubdok"),
        ("09.20 – 09.30", "10", "Kata Sambutan Ketua Pelaksana OMGTC 2026", "Auditorium Gd. A", "Fellicia Florens"),
        ("09.30 – 09.40", "10", "Kata Sambutan Ketua BEM FEB UKRIDA", "Auditorium Gd. A", "Arthur Reezan"),
        ("09.40 – 09.50", "10", "Kata Sambutan Dekan FEB UKRIDA & Pembukaan Resmi", "Auditorium Gd. A", "Dr. Diana Frederica"),
        ("09.50 – 10.50", "60", "Pemaparan Materi Seminar oleh Tim Pakar Optik Melawai", "Auditorium Gd. A", "Moderator & Narasumber"),
        ("10.50 – 11.20", "30", "Sesi Diskusi Panel & Tanya Jawab Interaktif", "Auditorium Gd. A", "Moderator"),
        ("11.20 – 11.30", "10", "Penyerahan Plakat Penghargaan & Cinderamata", "Auditorium Gd. A", "Ketua BEM & Dekan FEB"),
        ("11.30 – 11.40", "10", "Sesi Foto Bersama & Penutupan Seminar", "Auditorium Gd. A", "Divisi Pubdok & MC"),
        ("11.40 – 13.00", "80", "Ishoma (Istirahat & Sholat Jumat)", "Posko Panitia", "Divisi Konsumsi"),
        ("13.00 – 16.00", "180", "Layanan Puncak Pemeriksaan Mata, Mobile Optik, & Promo", "Junction & Parkiran", "Panitia & Tim Mitra"),
        ("16.00 – 16.30", "30", "Rekapitulasi Akhir Layanan & Serah Terima Area", "Junction & Parkiran", "Panitia & Pihak Kampus"),
        ("16.30 – Selesai", "-", "Evaluasi Penutupan Kegiatan & Pembongkaran Fasilitas", "Posko Panitia", "Seluruh Panitia"),
    ]
    t_rd2 = doc.add_table(rows=1, cols=5)
    format_table(
        t_rd2,
        [Cm(2.6), Cm(1.6), Cm(5.6), Cm(2.7), Cm(3.0)],
        ["Waktu", "Durasi", "Kegiatan", "Lokasi", "PJ"],
        rundown_d2,
        [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    )

    add_sub_heading(doc, "G. TEKNIS SARANA DAN PRASARANA")
    add_numbered_item(doc, "1.", "Booth Pelayanan Optik: Junction Kampus 1, luas minimal 4 x 3 m. Membutuhkan daya listrik stabil 4.000 Watt untuk 2 unit Autorefraktometer, 2 unit ACP, perlengkapan setel kacamata, dan display produk.")
    add_numbered_item(doc, "2.", "Unit Mobile Optik (Bus Layanan): Area Parkir Depan Kampus 1 (akses manuver aman). Bus dimensi 12 m × 2,5 m × 3,8 m, mesin edging lensa, dan display. Membutuhkan daya listrik 8.000 Watt.")
    add_numbered_item(doc, "3.", "Fasilitas Seminar Edukasi: Auditorium Gedung A Lantai 7 Kampus 1. Kapasitas 100 kursi, meja kursi pemateri, sound system nirkabel, LCD giant screen/proyektor, dan koneksi kabel HDMI/VGA.")

    # ==============================================================
    # BAB IV: KEPANITIAAN
    # ==============================================================
    add_bab_heading(doc, "IV. KEPANITIAAN")
    
    panitia_data = [
        ("Pelindung", "Dr. Diana Frederica S.E., M.Ak., CFP®., CHCP-A (Dekan FEB)", "-"),
        ("Penasehat", "Dr. Daniel Widjaja, S.E., M.M., CSCU, CEAP (Wakil Dekan FEB)", "-"),
        ("Ketua BEM FEB", "Arthur Reezan", "312023002"),
        ("Wakil Ketua BEM FEB", "Princess Auralia Barus", "322024025"),
        ("Ketua Pelaksana", "Fellicia Florens", "322024018"),
        ("Wakil Ketua Pelaksana", "Michelle Angelina", "312024012"),
        ("Sekretaris I", "Jessica Violant Nathaniel", "322024015"),
        ("Sekretaris II", "Rachel Angelina Tjahja", "322024033"),
        ("Bendahara I", "Jemima Putri Sutanta", "312024022"),
        ("Bendahara II", "Vanessa Clarissa", "322024008"),
        ("Koordinator Acara", "Jocelyn Jennifer", "312024005"),
        ("Anggota Divisi Acara", "Christopher Kevin", "322024030"),
        ("Anggota Divisi Acara", "Stephanie Nicole", "312024019"),
        ("Koordinator Perlengkapan", "William Hans", "322024040"),
        ("Anggota Divisi Perlengkapan", "Michael Jonathan", "312024028"),
        ("Anggota Divisi Perlengkapan", "David Surya", "322024011"),
        ("Koordinator Pubdok", "Bryan Alexander", "312024035"),
        ("Anggota Divisi Pubdok", "Sharon Priscilla", "322024029"),
        ("Koordinator Humas & Sponsor", "Nathania Graciela", "312024016"),
        ("Anggota Divisi Humas & Sponsor", "Steven Immanuel", "322024021"),
        ("Koordinator Konsumsi", "Clarissa Evelyn", "312024009"),
        ("Anggota Divisi Konsumsi", "Jennifer Amanda", "322024027"),
    ]
    t_panitia = doc.add_table(rows=1, cols=3)
    format_table(
        t_panitia,
        [Cm(5.0), Cm(7.5), Cm(3.0)],
        ["Jabatan Kepanitiaan", "Nama Lengkap", "NIM"],
        panitia_data,
        [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER]
    )

    # ==============================================================
    # BAB V: ANGGARAN
    # ==============================================================
    add_bab_heading(doc, "V. ANGGARAN")
    
    add_sub_heading(doc, "A. RENCANA PEMASUKAN")
    t_masuk = doc.add_table(rows=1, cols=4)
    format_table(
        t_masuk,
        [Cm(1.2), Cm(6.5), Cm(4.8), Cm(3.0)],
        ["No", "Sumber Pendanaan", "Rincian Dokumen", "Jumlah (Rp)"],
        [
            ("1", "Dana Sponsorship PT. Inti Citra Agung (Optik Melawai)", "Invoice No. INV/BEM-FEB/OM/IX/2026", "Rp. 3.000.000"),
            ("", "TOTAL PEMASUKAN", "", "Rp. 3.000.000"),
        ],
        [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT]
    )
    # Bold total pemasukan row
    for r in t_masuk.rows[-1].cells:
        for p in r.paragraphs:
            for run in p.runs:
                run.bold = True

    add_sub_heading(doc, "B. RENCANA PENGELUARAN")
    
    # 1. Acara
    p_div1 = doc.add_paragraph()
    p_div1.paragraph_format.space_before = Pt(4)
    p_div1.paragraph_format.space_after = Pt(2)
    p_div1.add_run("1. Divisi Acara").bold = True
    
    t_kel1 = doc.add_table(rows=1, cols=5)
    format_table(
        t_kel1,
        [Cm(1.0), Cm(6.0), Cm(2.5), Cm(3.0), Cm(3.0)],
        ["No", "Uraian Kebutuhan", "Kuantitas", "Harga Satuan", "Subtotal"],
        [
            ("1", "Plakat Akrilik Penghargaan Narasumber", "1 buah", "Rp. 250.000", "Rp. 250.000"),
            ("2", "Paket Cinderamata / Goodie Bag Pemateri & Mitra", "2 paket", "Rp. 150.000", "Rp. 300.000"),
            ("3", "Cetak Sertifikat Kertas Linen & Map Panitia/Peserta", "40 lembar", "Rp. 5.000", "Rp. 200.000"),
            ("", "TOTAL DIVISI ACARA", "", "", "Rp. 750.000"),
        ],
        [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT]
    )
    for r in t_kel1.rows[-1].cells:
        for p in r.paragraphs:
            for run in p.runs:
                run.bold = True

    # 2. Konsumsi
    p_div2 = doc.add_paragraph()
    p_div2.paragraph_format.space_before = Pt(6)
    p_div2.paragraph_format.space_after = Pt(2)
    p_div2.add_run("2. Divisi Konsumsi").bold = True
    
    t_kel2 = doc.add_table(rows=1, cols=5)
    format_table(
        t_kel2,
        [Cm(1.0), Cm(6.0), Cm(2.5), Cm(3.0), Cm(3.0)],
        ["No", "Uraian Kebutuhan", "Kuantitas", "Harga Satuan", "Subtotal"],
        [
            ("1", "Snack Box Narasumber & Tamu Khusus", "10 box", "Rp. 25.000", "Rp. 250.000"),
            ("2", "Makan Siang Panitia Pelaksana (2 Hari)", "32 porsi", "Rp. 25.000", "Rp. 800.000"),
            ("", "TOTAL DIVISI KONSUMSI", "", "", "Rp. 1.050.000"),
        ],
        [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT]
    )
    for r in t_kel2.rows[-1].cells:
        for p in r.paragraphs:
            for run in p.runs:
                run.bold = True

    # 3. Pubdok
    p_div3 = doc.add_paragraph()
    p_div3.paragraph_format.space_before = Pt(6)
    p_div3.paragraph_format.space_after = Pt(2)
    p_div3.add_run("3. Divisi Publikasi dan Dokumentasi (Pubdok)").bold = True
    
    t_kel3 = doc.add_table(rows=1, cols=5)
    format_table(
        t_kel3,
        [Cm(1.0), Cm(6.0), Cm(2.5), Cm(3.0), Cm(3.0)],
        ["No", "Uraian Kebutuhan", "Kuantitas", "Harga Satuan", "Subtotal"],
        [
            ("1", "Cetak Backdrop Panggung Auditorium (Ukuran 4 x 2 m)", "1 buah", "Rp. 250.000", "Rp. 250.000"),
            ("2", "Cetak Standing Banner / X-Banner Edukasi & Petunjuk", "2 buah", "Rp. 100.000", "Rp. 200.000"),
            ("3", "Tali Lanyard & ID Card Panitia Pelaksana", "20 pcs", "Rp. 2.500", "Rp. 50.000"),
            ("", "TOTAL DIVISI PUBDOK", "", "", "Rp. 500.000"),
        ],
        [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT]
    )
    for r in t_kel3.rows[-1].cells:
        for p in r.paragraphs:
            for run in p.runs:
                run.bold = True

    # 4. Perlengkapan
    p_div4 = doc.add_paragraph()
    p_div4.paragraph_format.space_before = Pt(6)
    p_div4.paragraph_format.space_after = Pt(2)
    p_div4.add_run("4. Divisi Perlengkapan dan Logistik").bold = True
    
    t_kel4 = doc.add_table(rows=1, cols=5)
    format_table(
        t_kel4,
        [Cm(1.0), Cm(6.0), Cm(2.5), Cm(3.0), Cm(3.0)],
        ["No", "Uraian Kebutuhan", "Kuantitas", "Harga Satuan", "Subtotal"],
        [
            ("1", "Sewa Kabel Roll Heavy Duty (Daya Tinggi)", "2 unit", "Rp. 100.000", "Rp. 200.000"),
            ("2", "Baterai Wireless Microphone (Alkaline AA/9V)", "4 set", "Rp. 25.000", "Rp. 100.000"),
            ("3", "Lakban Hitam Kabel & Floor Marking Booth", "3 roll", "Rp. 25.000", "Rp. 75.000"),
            ("4", "Kantong Plastik Trash Bag & Sarung Tangan", "3 pack", "Rp. 25.000", "Rp. 75.000"),
            ("", "TOTAL DIVISI PERLENGKAPAN", "", "", "Rp. 450.000"),
        ],
        [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT]
    )
    for r in t_kel4.rows[-1].cells:
        for p in r.paragraphs:
            for run in p.runs:
                run.bold = True

    # 5. Humas & P3K
    p_div5 = doc.add_paragraph()
    p_div5.paragraph_format.space_before = Pt(6)
    p_div5.paragraph_format.space_after = Pt(2)
    p_div5.add_run("5. Divisi Humas dan P3K").bold = True
    
    t_kel5 = doc.add_table(rows=1, cols=5)
    format_table(
        t_kel5,
        [Cm(1.0), Cm(6.0), Cm(2.5), Cm(3.0), Cm(3.0)],
        ["No", "Uraian Kebutuhan", "Kuantitas", "Harga Satuan", "Subtotal"],
        [
            ("1", "Air Mineral Botol & Dus Meja Registrasi", "3 dus", "Rp. 50.000", "Rp. 150.000"),
            ("2", "Kotak Obat P3K & Sanitizer Area Pemeriksaan", "1 paket", "Rp. 100.000", "Rp. 100.000"),
            ("", "TOTAL DIVISI HUMAS & P3K", "", "", "Rp. 250.000"),
        ],
        [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT]
    )
    for r in t_kel5.rows[-1].cells:
        for p in r.paragraphs:
            for run in p.runs:
                run.bold = True

    # C. Rekapitulasi
    add_sub_heading(doc, "C. REKAPITULASI ANGGARAN BIAYA")
    
    t_rekap = doc.add_table(rows=1, cols=3)
    format_table(
        t_rekap,
        [Cm(1.5), Cm(10.0), Cm(4.0)],
        ["No", "Divisi Operasional", "Alokasi Dana (Rp)"],
        [
            ("1", "Divisi Acara", "Rp. 750.000"),
            ("2", "Divisi Konsumsi", "Rp. 1.050.000"),
            ("3", "Divisi Publikasi dan Dokumentasi (Pubdok)", "Rp. 500.000"),
            ("4", "Divisi Perlengkapan dan Logistik", "Rp. 450.000"),
            ("5", "Divisi Humas dan P3K", "Rp. 250.000"),
            ("", "TOTAL PENGELUARAN", "Rp. 3.000.000"),
        ],
        [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT]
    )
    for r in t_rekap.rows[-1].cells:
        for p in r.paragraphs:
            for run in p.runs:
                run.bold = True

    # Neraca Balance Box Table
    p_neraca_space = doc.add_paragraph()
    p_neraca_space.paragraph_format.space_before = Pt(4)
    p_neraca_space.paragraph_format.space_after = Pt(2)
    
    t_neraca = doc.add_table(rows=3, cols=2)
    t_neraca.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_neraca.columns[0].width = Cm(11.5)
    t_neraca.columns[1].width = Cm(4.0)
    
    neraca_rows = [
        ("Total Rencana Pemasukan", "Rp. 3.000.000"),
        ("Total Rencana Pengeluaran", "Rp. 3.000.000"),
        ("Sisa Saldo Anggaran (BALANCE)", "Rp. 0"),
    ]
    for idx, (label, val) in enumerate(neraca_rows):
        c0 = t_neraca.rows[idx].cells[0]
        c1 = t_neraca.rows[idx].cells[1]
        c0.text = label
        c1.text = val
        bg_col = "EAECEE" if idx == 2 else "F8F9F9"
        set_cell_shading(c0, bg_col)
        set_cell_shading(c1, bg_col)
        set_cell_border(c0, top="single", bottom="single", top_color="566573", bottom_color="566573")
        set_cell_border(c1, top="single", bottom="single", top_color="566573", bottom_color="566573")
        set_cell_margins(c0, top=100, bottom=100, left=140, right=140)
        set_cell_margins(c1, top=100, bottom=100, left=140, right=140)
        
        p0 = c0.paragraphs[0]
        p1 = c1.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p0.paragraph_format.line_spacing = 1.0
        p1.paragraph_format.line_spacing = 1.0
        
        for r in p0.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(10.5)
            r.bold = True
        for r in p1.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(10.5)
            r.bold = True

    # ==============================================================
    # BAB VI: PENUTUP & LEMBAR PENGESAHAN
    # ==============================================================
    add_bab_heading(doc, "VI. PENUTUP")
    
    add_body_paragraph(
        doc,
        "Demikian Proposal Kegiatan Optik Melawai Goes To Campus (OMGTC) 2026 ini kami susun dengan itikad baik sebagai "
        "kerangka acuan operasional, dasar perizinan tempat, serta transparansi alokasi anggaran kegiatan. Program kolaboratif ini "
        "diharapkan mampu memberikan kontribusi nyata dalam meningkatkan derajat kesehatan penglihatan mahasiswa dan civitas akademika "
        "Fakultas Ekonomi dan Bisnis UKRIDA guna menyongsong masa depan perkuliahan yang lebih produktif dan berdaya saing tinggi."
    )
    
    add_body_paragraph(
        doc,
        "Atas perhatian, bimbingan, kerja sama, dan persetujuan yang diberikan oleh Pimpinan Fakultas Ekonomi dan Bisnis Universitas Kristen "
        "Krida Wacana, kami selaku panitia pelaksana dan pengurus BEM FEB UKRIDA mengucapkan terima kasih sebesar-besarnya."
    )

    # Tanggal Dokumen
    p_tgl = doc.add_paragraph()
    p_tgl.paragraph_format.space_before = Pt(12)
    p_tgl.paragraph_format.space_after = Pt(4)
    r_tgl = p_tgl.add_run("Jakarta, 01 September 2026")
    r_tgl.font.name = "Times New Roman"
    r_tgl.font.size = Pt(12)

    # Identitas Pengesahan
    p_org = doc.add_paragraph()
    p_org.paragraph_format.space_before = Pt(2)
    p_org.paragraph_format.space_after = Pt(14)
    r_org = p_org.add_run(
        "PANITIA PELAKSANA OPTIK MELAWAI GOES TO CAMPUS (OMGTC) 2026\n"
        "BADAN EKSEKUTIF MAHASISWA FAKULTAS EKONOMI DAN BISNIS\n"
        "UNIVERSITAS KRISTEN KRIDA WACANA"
    )
    r_org.font.name = "Times New Roman"
    r_org.font.size = Pt(11)
    r_org.bold = True

    # Baris 1: Ketua Pelaksana & Sekretaris Pelaksana
    t_ttd1 = doc.add_table(rows=1, cols=2)
    t_ttd1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_ttd1.columns[0].width = Cm(7.7)
    t_ttd1.columns[1].width = Cm(7.7)
    
    c_ketupel = t_ttd1.cell(0, 0)
    p_kp = c_ketupel.paragraphs[0]
    p_kp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_kp.paragraph_format.line_spacing = 1.15
    p_kp.add_run("Hormat kami,\nKetua Pelaksana\n\n\n\n\n").font.name = "Times New Roman"
    r_nkp = p_kp.add_run("Fellicia Florens\n")
    r_nkp.font.name = "Times New Roman"
    r_nkp.bold = True
    r_nkp.font.size = Pt(11)
    p_kp.add_run("NIM: 322024018").font.name = "Times New Roman"
    
    c_sekre = t_ttd1.cell(0, 1)
    p_sk = c_sekre.paragraphs[0]
    p_sk.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sk.paragraph_format.line_spacing = 1.15
    p_sk.add_run("Hormat kami,\nSekretaris Pelaksana\n\n\n\n\n").font.name = "Times New Roman"
    r_nsk = p_sk.add_run("Jessica Violant Nathaniel\n")
    r_nsk.font.name = "Times New Roman"
    r_nsk.bold = True
    r_nsk.font.size = Pt(11)
    p_sk.add_run("NIM: 322024015").font.name = "Times New Roman"

    # Baris 2: Ketua BEM FEB UKRIDA (Center)
    p_ttd_space2 = doc.add_paragraph()
    p_ttd_space2.paragraph_format.space_before = Pt(10)
    p_ttd_space2.paragraph_format.space_after = Pt(2)
    
    t_ttd2 = doc.add_table(rows=1, cols=1)
    t_ttd2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_ttd2.columns[0].width = Cm(8.5)
    
    c_bem = t_ttd2.cell(0, 0)
    p_bm = c_bem.paragraphs[0]
    p_bm.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bm.paragraph_format.line_spacing = 1.15
    p_bm.add_run("Mengetahui,\nKetua BEM FEB UKRIDA\n\n\n\n\n").font.name = "Times New Roman"
    r_nbm = p_bm.add_run("Arthur Reezan\n")
    r_nbm.font.name = "Times New Roman"
    r_nbm.bold = True
    r_nbm.font.size = Pt(11)
    p_bm.add_run("NIM: 312023002").font.name = "Times New Roman"

    # Baris 3: Wakil Dekan & Dekan FEB UKRIDA
    p_ttd_space3 = doc.add_paragraph()
    p_ttd_space3.paragraph_format.space_before = Pt(10)
    p_ttd_space3.paragraph_format.space_after = Pt(2)
    
    t_ttd3 = doc.add_table(rows=1, cols=2)
    t_ttd3.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_ttd3.columns[0].width = Cm(7.7)
    t_ttd3.columns[1].width = Cm(7.7)
    
    c_wadek = t_ttd3.cell(0, 0)
    p_wd = c_wadek.paragraphs[0]
    p_wd.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_wd.paragraph_format.line_spacing = 1.15
    p_wd.add_run("Mengetahui,\nWakil Dekan FEB UKRIDA\n\n\n\n\n").font.name = "Times New Roman"
    r_nwd = p_wd.add_run("Dr. Daniel Widjaja, S.E., M.M., CSCU, CEAP")
    r_nwd.font.name = "Times New Roman"
    r_nwd.bold = True
    r_nwd.font.size = Pt(11)
    
    c_dekan = t_ttd3.cell(0, 1)
    p_dk = c_dekan.paragraphs[0]
    p_dk.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dk.paragraph_format.line_spacing = 1.15
    p_dk.add_run("Menyetujui,\nDekan FEB UKRIDA\n\n\n\n\n").font.name = "Times New Roman"
    r_ndk = p_dk.add_run("Dr. Diana Frederica S.E., M.Ak., CFP®., CHCP-A")
    r_ndk.font.name = "Times New Roman"
    r_ndk.bold = True
    r_ndk.font.size = Pt(11)

    # Simpan file docx
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"✅ Dokumen berhasil diekspor ke: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_proposal_docx()
