"""
execution/docx_generator.py
===========================
Script generator proposal Word (.docx) resmi BEM FEB UKRIDA.
Dirancang khusus mengikuti standar kerapihan dan tata letak autentik
dokumen resmi BEM FEB UKRIDA (referensi: PROPOSAL LKMM TINGKAT II 2026 & PKKMB 2026):

1. Standar Halaman & Margin:
   - Ukuran: A4 (21.0 x 29.7 cm)
   - Margin: Kiri 4.0 cm (Binding), Atas 3.0 cm, Kanan 3.0 cm, Bawah 3.0 cm
2. Standar Tipografi & Warna:
   - Font: Times New Roman 100% konsisten
   - Warna: Hitam murni (#000000)
   - Ukuran font: 12 pt untuk judul bab, sub-bab, narasi, dan tanda tangan;
     10.5 - 11 pt untuk tabel rundown/anggaran agar proporsional dan tidak berantakan
   - Line Spacing: 1.5 spasi untuk paragraf narasi, Justify, first-line indent 1.27 cm
3. Cover / Halaman Judul:
   - Judul & Tema: Times New Roman 12 pt Bold, Uppercase / Bold Italic, Centered
   - Logo: 1 Logo Resmi BEM FEB UKRIDA besar (~11.5 cm) di tengah halaman
   - Bawah: Identitas BEM FEB UKRIDA & Periode 2026, Alamat, Telp, Fax (Bold, 12 pt, Centered)
4. Halaman Tubuh:
   - Dimulai langsung dari Halaman 2 dengan "I. LATAR BELAKANG" (tanpa kop surat berulang)
5. Susunan Kepanitiaan:
   - Tata letak tabel borderless 3-kolom yang presisi (Jabatan : Nama (NIM))
   - Koordinator dan pimpinan di-bold, bersih tanpa kotak-kotak kaku
6. Tabel Rundown & Anggaran:
   - Border hitam solid 0.75 pt rapi
   - Header tabel anggaran beraksen soft green (#B3E4A1) khas Google Docs LK FEB
   - Baris Total dan Neraca Saldo di-bold (Sisa: Rp. 0 / Balance)
7. Penutup & Lembar Pengesahan:
   - Nama penandatangan di-bold dan digarisbawahi (underline)
   - Disusun dalam tabel borderless terpusat dan sejajar rapi
"""

import os
import docx
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls


def set_table_borders(table, val="single", sz="6", color="000000"):
    """Mengatur border luar dan dalam tabel menjadi hitam rapi."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def set_table_borderless(table):
    """Menghilangkan seluruh border pada tabel layout (Kepanitiaan & TTD)."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:left w:val="none"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:insideH w:val="none"/>\n'
        f'  <w:insideV w:val="none"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def set_table_cell_margins(table, top=100, bottom=100, left=140, right=140):
    """Mengatur padding internal sel tabel (100 dxa = 5 pt, 140 dxa = 7 pt)."""
    tblPr = table._tbl.tblPr
    tblCellMar = parse_xml(
        f'<w:tblCellMar {nsdecls("w")}>\n'
        f'  <w:top w:w="{top}" w:type="dxa"/>\n'
        f'  <w:bottom w:w="{bottom}" w:type="dxa"/>\n'
        f'  <w:left w:w="{left}" w:type="dxa"/>\n'
        f'  <w:right w:w="{right}" w:type="dxa"/>\n'
        f'</w:tblCellMar>'
    )
    tblPr.append(tblCellMar)


def set_cell_shading(cell, color_hex):
    """Memberikan latar belakang warna pada sel."""
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def prevent_row_split_and_repeat_header(table):
    """Memastikan baris tabel tidak terpotong halaman dan header terulang."""
    for idx, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if idx == 0:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))


def add_bab_heading(doc, text):
    """Menambahkan Heading Bab (I. LATAR BELAKANG, dll)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.left_indent = Cm(0)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p


def add_sub_heading(doc, text, space_before=10):
    """Menambahkan Sub-Heading (A. TUJUAN KEGIATAN, dll) dengan indentasi khas Google Docs LK FEB."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Cm(1.27)
    p.paragraph_format.first_line_indent = Cm(-1.27)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p


def add_body_paragraph(doc, text, space_after=6):
    """Menambahkan paragraf narasi standar (Justify, 1.5 spasi, first line indent 1.27 cm)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.left_indent = Cm(0)
    p.paragraph_format.first_line_indent = Cm(1.27)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p


def add_intro_line(doc, text, space_after=4):
    """Menambahkan kalimat pengantar sub-bab tanpa indentasi berlebih."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 1.25
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.left_indent = Cm(1.27)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p


def add_numbered_item(doc, num_str, title_str, text_str):
    """Menambahkan butir poin terurut (1., 2., dll) dengan hanging indent rapi."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Cm(2.1)
    p.paragraph_format.first_line_indent = Cm(-0.83)
    p.paragraph_format.line_spacing = 1.25
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    
    r_num = p.add_run(num_str + " ")
    r_num.font.name = "Times New Roman"
    r_num.font.size = Pt(12)
    r_num.font.color.rgb = RGBColor(0, 0, 0)
    
    if title_str:
        r_tit = p.add_run(title_str + " ")
        r_tit.font.name = "Times New Roman"
        r_tit.font.size = Pt(12)
        r_tit.bold = True
        r_tit.font.color.rgb = RGBColor(0, 0, 0)
        
    r_txt = p.add_run(text_str)
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(12)
    r_txt.font.color.rgb = RGBColor(0, 0, 0)
    return p


def format_standard_table(table, col_widths, headers, data, alignments=None, header_bg=None, font_size=11):
    """Memformat tabel standar dengan border hitam solid rapi khas dokumen resmi UKRIDA."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    set_table_borders(table, val="single", sz="6", color="000000")
    set_table_cell_margins(table, top=100, bottom=100, left=140, right=140)
    
    # 1. Header Row
    hdr_cells = table.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = h_text
        if header_bg:
            set_cell_shading(hdr_cells[i], header_bg)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        for run in p.runs:
            run.font.name = "Times New Roman"
            run.font.size = Pt(font_size)
            run.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)
            
    # 2. Data Rows
    for row_data in data:
        row_cells = table.add_row().cells
        for c_idx, cell_value in enumerate(row_data):
            row_cells[c_idx].text = str(cell_value)
            p = row_cells[c_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            
            if alignments and c_idx < len(alignments):
                p.alignment = alignments[c_idx]
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(font_size)
                run.font.color.rgb = RGBColor(0, 0, 0)
                
    # 3. Set precise widths
    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width
            
    prevent_row_split_and_repeat_header(table)


def generate_proposal_docx(output_path="01_Proposal/OMGTC_2026/Proposal_OMGTC_FEB_UKRIDA_2026.docx"):
    """Fungsi utama generator proposal Word resmi BEM FEB UKRIDA."""
    doc = docx.Document()
    
    # ==============================================================
    # 1. STANDAR MARGIN INDONESIA (4-3-3-3)
    # ==============================================================
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.left_margin = Cm(4.0)   # 4 cm (Binding kiri)
        section.top_margin = Cm(3.0)    # 3 cm (Atas)
        section.right_margin = Cm(3.0)  # 3 cm (Kanan)
        section.bottom_margin = Cm(3.0) # 3 cm (Bawah)
        
    logo_official = "05_Referensi_Template/BEM_FEB_LOGO_OFFICIAL.png"
    if not os.path.exists(logo_official):
        logo_official = "04_Arsip_Acara/OPTIK_MELAWAI_2026/BEM_FEB_LOGO_tight.png"
        
    # Lebar area isi (A4 width 21.0 - left 4.0 - right 3.0 = 14.0 cm)
    CONTENT_WIDTH = Cm(14.0)
    
    # ==============================================================
    # 2. HALAMAN COVER RESMI (PERSIS LKMM TINGKAT II 2026 & PKKMB)
    # ==============================================================
    p_cov_title = doc.add_paragraph()
    p_cov_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_title.paragraph_format.space_before = Pt(8)
    p_cov_title.paragraph_format.space_after = Pt(2)
    p_cov_title.paragraph_format.line_spacing = 1.15
    
    r_t1 = p_cov_title.add_run("PROPOSAL KEGIATAN\n")
    r_t1.font.name = "Times New Roman"
    r_t1.font.size = Pt(12)
    r_t1.bold = True
    r_t1.font.color.rgb = RGBColor(0, 0, 0)
    
    r_t2 = p_cov_title.add_run("OPTIK MELAWAI GOES TO CAMPUS (OMGTC) 2026\n")
    r_t2.font.name = "Times New Roman"
    r_t2.font.size = Pt(12)
    r_t2.bold = True
    r_t2.font.color.rgb = RGBColor(0, 0, 0)
    
    r_th = p_cov_title.add_run(
        "“CLEAR VISION, BRIGHT FUTURE: Edukasi Kesehatan Visual dan Pemeriksaan Refraksi Bersama Optik Melawai”"
    )
    r_th.font.name = "Times New Roman"
    r_th.font.size = Pt(12)
    r_th.bold = True
    r_th.italic = True
    r_th.font.color.rgb = RGBColor(0, 0, 0)
    
    # Logo BEM FEB UKRIDA Besar Terpusat di Tengah
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(28)
    p_logo.paragraph_format.space_after = Pt(28)
    if os.path.exists(logo_official):
        p_logo.add_run().add_picture(logo_official, width=Cm(11.5))
        
    # Identitas Organisasi Bagian Bawah
    p_cov_foot = doc.add_paragraph()
    p_cov_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_foot.paragraph_format.line_spacing = 1.15
    p_cov_foot.paragraph_format.space_before = Pt(10)
    p_cov_foot.paragraph_format.space_after = Pt(0)
    
    foot_runs = [
        ("BADAN EKSEKUTIF MAHASISWA\n", True),
        ("FAKULTAS EKONOMI & BISNIS UKRIDA\n", True),
        ("PERIODE 2026\n\n", True),
        ("Jl. Tanjung Duren Raya no. 4, Jakarta Barat\n", True),
        ("Telp. 021 566 6952\n", True),
        ("Fax. 021 566 6956", True),
    ]
    for text, is_bold in foot_runs:
        r = p_cov_foot.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        r.bold = is_bold
        r.font.color.rgb = RGBColor(0, 0, 0)
        
    # Halaman 1 Selesai -> Page Break ke Halaman 2
    doc.add_page_break()
    
    # ==============================================================
    # 3. BAB I: LATAR BELAKANG
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
    # 4. BAB II: TEMA KEGIATAN
    # ==============================================================
    add_bab_heading(doc, "II. TEMA KEGIATAN")
    
    # Format persis LKMM II: Paragraf tema dengan indent 1.27 cm
    p_th = doc.add_paragraph()
    p_th.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_th.paragraph_format.line_spacing = 1.5
    p_th.paragraph_format.first_line_indent = Cm(1.27)
    p_th.paragraph_format.space_after = Pt(6)
    r_th1 = p_th.add_run("Acara Optik Melawai Goes To Campus (OMGTC) tahun 2026 bertemakan ")
    r_th1.font.name = "Times New Roman"
    r_th1.font.size = Pt(12)
    r_th1.font.color.rgb = RGBColor(0, 0, 0)
    
    r_th2 = p_th.add_run("“CLEAR VISION, BRIGHT FUTURE: Edukasi Kesehatan Visual dan Pemeriksaan Refraksi Bersama Optik Melawai”")
    r_th2.font.name = "Times New Roman"
    r_th2.font.size = Pt(12)
    r_th2.bold = True
    r_th2.italic = True
    r_th2.font.color.rgb = RGBColor(0, 0, 0)
    
    r_th3 = p_th.add_run(".")
    r_th3.font.name = "Times New Roman"
    r_th3.font.size = Pt(12)
    
    add_body_paragraph(
        doc,
        "Tema ini merefleksikan keyakinan bahwa penglihatan yang sehat dan jernih (Clear Vision) merupakan modal dasar paling esensial "
        "bagi mahasiswa dalam menyerap ilmu pengetahuan, membangun daya saing intelektual, dan meraih masa depan yang gemilang (Bright Future). "
        "Melalui pendekatan preventif dan kuratif, kegiatan ini mengajak seluruh mahasiswa FEB UKRIDA untuk proaktif merawat kesehatan mata "
        "di tengah pesatnya dinamika digitalisasi modern."
    )
    
    # ==============================================================
    # 5. BAB III: KEGIATAN
    # ==============================================================
    add_bab_heading(doc, "III. KEGIATAN")
    
    # A. TUJUAN KEGIATAN
    add_sub_heading(doc, "A. TUJUAN KEGIATAN")
    add_intro_line(doc, "Tujuan dari kegiatan ini adalah:")
    add_numbered_item(doc, "1.", "", "Meningkatkan kesadaran (awareness) mahasiswa FEB UKRIDA dan civitas akademika akan urgensi menjaga kesehatan mata serta mencegah gangguan visual akibat digital eye strain.")
    add_numbered_item(doc, "2.", "", "Memfasilitasi deteksi dini kelainan refraksi (miopia, hipermetropia, dan astigmatisme) bagi mahasiswa melalui pemeriksaan mata berstandar profesional tanpa dipungut biaya.")
    add_numbered_item(doc, "3.", "", "Memberikan pelayanan sosial perawatan kacamata berupa pencucian dan penyetelan kacamata gratis guna mendukung kenyamanan beraktivitas di lingkungan kampus.")
    add_numbered_item(doc, "4.", "", "Membangun kemitraan strategis yang berkelanjutan antara BEM FEB UKRIDA dengan sektor industri kesehatan dan optik profesional.")
    add_numbered_item(doc, "5.", "", "Mendukung terciptanya lingkungan perkuliahan yang sehat, produktif, dan berorientasi pada kesejahteraan fisik mahasiswa.")
    
    # B. MANFAAT KEGIATAN
    add_sub_heading(doc, "B. MANFAAT KEGIATAN")
    add_intro_line(doc, "Manfaat yang diharapkan dari terselenggaranya kegiatan ini meliputi:")
    add_numbered_item(doc, "1.", "Bagi Mahasiswa:", "Memperoleh edukasi medis langsung dari para ahli optometri, menerima diagnosa refraksi mata secara akurat tanpa biaya, serta mendapatkan solusi perlindungan mata terjangkau.")
    add_numbered_item(doc, "2.", "Bagi BEM FEB UKRIDA:", "Mewujudkan program kerja pengabdian dan pelayanan mahasiswa yang berdampak nyata, meningkatkan citra kelembagaan, serta memperluas jejaring kemitraan eksternal.")
    add_numbered_item(doc, "3.", "Bagi Fakultas Ekonomi dan Bisnis UKRIDA:", "Mendukung pemenuhan indikator kesejahteraan mahasiswa dan mewujudkan suasana akademik kampus yang adaptif terhadap kesehatan civitas academica.")
    
    # C. TARGET PESERTA
    add_sub_heading(doc, "C. TARGET PESERTA")
    add_intro_line(doc, "Target sasaran dari kegiatan ini adalah:")
    add_numbered_item(doc, "1.", "Seminar Edukasi Kesehatan Mata:", "100 orang mahasiswa aktif Fakultas Ekonomi dan Bisnis UKRIDA serta perwakilan civitas akademika.")
    add_numbered_item(doc, "2.", "Pemeriksaan Refraksi & Layanan Kacamata (Booth & Mobile Optik):", "± 200 hingga 300 mahasiswa, dosen, dan staf di lingkungan Kampus 1 UKRIDA.")
    
    # D. PELAKSANAAN KEGIATAN (Format Persis LKMM II)
    add_sub_heading(doc, "D. PELAKSANAAN KEGIATAN")
    add_intro_line(doc, "Kegiatan Optik Melawai Goes To Campus (OMGTC) 2026 akan dilaksanakan pada:")
    
    # Layout List Pelaksanaan rapi tanpa border
    t_pelak = doc.add_table(rows=3, cols=3)
    t_pelak.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_pelak.autofit = False
    set_table_borderless(t_pelak)
    set_table_cell_margins(t_pelak, top=40, bottom=40, left=40, right=40)
    
    pelak_widths = [Cm(3.5), Cm(0.4), Cm(10.1)]
    pelak_rows = [
        ("Hari, Tanggal", ":", "Kamis – Jumat, 10 – 11 September 2026"),
        ("Waktu", ":", "08.30 – 16.30 WIB"),
        ("Tempat", ":", "1. Booth Pelayanan: Junction Kampus 1 UKRIDA\n2. Mobile Optik (Bus): Area Parkir Depan Kampus 1 UKRIDA\n3. Seminar Edukasi: Auditorium Gedung A Lantai 7 Kampus 1 UKRIDA"),
    ]
    for r_idx, (col0, col1, col2) in enumerate(pelak_rows):
        row = t_pelak.rows[r_idx]
        for c_idx, val in enumerate([col0, col1, col2]):
            cell = row.cells[c_idx]
            cell.text = val
            cell.width = pelak_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(12)
                r.font.color.rgb = RGBColor(0, 0, 0)
                
    # E. NARASUMBER KEGIATAN
    add_sub_heading(doc, "E. NARASUMBER KEGIATAN")
    add_intro_line(doc, "Narasumber kegiatan Seminar Edukasi Kesehatan Mata adalah:")
    add_numbered_item(
        doc, "1.", "Tim Dokter / Optometris Spesialis PT. Inti Citra Agung (Optik Melawai)",
        "— Topik: \"Mengenal Computer Vision Syndrome: Kiat Menjaga Ketajaman Visual Mahasiswa di Era Digital\""
    )
    add_numbered_item(
        doc, "2.", "Tim Konsultan Edukasi Kesehatan Visual Optik Melawai",
        "— Topik: \"Pencegahan Progresivitas Miopia dan Pemilihan Solusi Lensa Optik Ergonomis\""
    )
    
    # F. SUSUNAN ACARA / RUNDOWN
    add_sub_heading(doc, "F. SUSUNAN ACARA / RUNDOWN")
    
    # Hari Pertama
    p_rd1_tit = doc.add_paragraph()
    p_rd1_tit.paragraph_format.left_indent = Cm(1.27)
    p_rd1_tit.paragraph_format.space_before = Pt(6)
    p_rd1_tit.paragraph_format.space_after = Pt(4)
    r_rd1 = p_rd1_tit.add_run("Hari Pertama: Kamis, 10 September 2026 (Aktivasi Pelayanan & Pemeriksaan Refraksi)")
    r_rd1.font.name = "Times New Roman"
    r_rd1.font.size = Pt(12)
    r_rd1.bold = True
    
    rundown_d1 = [
        ("08.00 – 08.30", "30", "Briefing Panitia BEM FEB dan Tim Teknis Optik Melawai", "Junction & Parkiran", "Divisi Acara & Ketupel"),
        ("08.30 – 09.00", "30", "Persiapan Akhir (Final Checking) Booth & Mobile Optik Bus", "Junction & Parkiran", "Divisi Perlengkapan"),
        ("09.00 – 09.15", "15", "Seremoni Pembukaan Pelayanan OMGTC 2026 oleh Ketua BEM", "Junction Kampus 1", "Divisi Acara & Ketum BEM"),
        ("09.15 – 12.00", "165", "Pelayanan Sesi Pagi:\n- Pemeriksaan Refraksi Mata Komputerisasi (Gratis)\n- Penyetelan & Pencucian Kacamata (Gratis)\n- Edukasi Interaktif & Games Berhadiah", "Junction & Parkiran", "Panitia & Tim Mitra"),
        ("12.00 – 13.00", "60", "Ishoma (Istirahat, Sholat, Makan Siang Panitia & Tim Mitra)", "Posko Panitia", "Divisi Konsumsi"),
        ("13.00 – 16.00", "180", "Pelayanan Sesi Siang:\n- Lanjutan Pemeriksaan Mata & Uji ACP\n- Layanan Edging / Pasang Lensa di Bus Mobile\n- Bazar Kacamata & Promo Khusus Mahasiswa", "Junction & Parkiran", "Panitia & Tim Mitra"),
        ("16.00 – 16.30", "30", "Closing Booth Day 1 & Evaluasi Harian Panitia", "Posko Panitia", "Seluruh Panitia"),
    ]
    t_rd1 = doc.add_table(rows=1, cols=5)
    format_standard_table(
        t_rd1,
        [Cm(2.6), Cm(1.6), Cm(5.0), Cm(2.4), Cm(2.4)],
        ["Waktu", "Durasi", "Kegiatan", "Lokasi", "PJ"],
        rundown_d1,
        [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT],
        header_bg=None,
        font_size=10.5
    )
    
    # Hari Kedua
    p_rd2_tit = doc.add_paragraph()
    p_rd2_tit.paragraph_format.left_indent = Cm(1.27)
    p_rd2_tit.paragraph_format.space_before = Pt(10)
    p_rd2_tit.paragraph_format.space_after = Pt(4)
    r_rd2 = p_rd2_tit.add_run("Hari Kedua: Jumat, 11 September 2026 (Seminar Kesehatan Mata & Pelayanan Terpadu)")
    r_rd2.font.name = "Times New Roman"
    r_rd2.font.size = Pt(12)
    r_rd2.bold = True
    
    rundown_d2 = [
        ("08.00 – 08.30", "30", "Briefing Panitia Gabungan & Pengecekan Sistem Audio Visual", "Auditorium Gd. A", "Divisi Acara & Perkap"),
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
    format_standard_table(
        t_rd2,
        [Cm(2.6), Cm(1.6), Cm(5.0), Cm(2.4), Cm(2.4)],
        ["Waktu", "Durasi", "Kegiatan", "Lokasi", "PJ"],
        rundown_d2,
        [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT],
        header_bg=None,
        font_size=10.5
    )
    
    # G. TEKNIS SARANA DAN PRASARANA
    add_sub_heading(doc, "G. TEKNIS SARANA DAN PRASARANA")
    add_numbered_item(
        doc, "1.", "Booth Pelayanan Optik:",
        "Junction Kampus 1, luas minimal 4 x 3 meter. Membutuhkan daya listrik stabil 4.000 Watt untuk 2 unit Autorefraktometer, 2 unit Auto Chart Projector (ACP), perlengkapan setel kacamata, dan display produk."
    )
    add_numbered_item(
        doc, "2.", "Unit Mobile Optik (Bus Layanan):",
        "Area Parkir Depan Kampus 1 (akses manuver aman). Bus dimensi 12 m × 2,5 m × 3,8 m, mesin edging lensa, dan display kacamata. Membutuhkan daya listrik 8.000 Watt."
    )
    add_numbered_item(
        doc, "3.", "Fasilitas Seminar Edukasi:",
        "Auditorium Gedung A Lantai 7 Kampus 1 UKRIDA. Kapasitas 100 kursi, meja kursi pemateri, sound system nirkabel, LCD giant screen/proyektor, dan koneksi kabel HDMI/VGA."
    )
    
    # ==============================================================
    # 6. BAB IV: KEPANITIAAN (TATA LETAK PERSIS LKMM II & PKKMB)
    # ==============================================================
    add_bab_heading(doc, "IV. KEPANITIAAN")
    
    add_intro_line(
        doc,
        "Susunan Panitia Pelaksana Kegiatan Optik Melawai Goes To Campus (OMGTC) 2026 Badan Eksekutif Mahasiswa "
        "Fakultas Ekonomi dan Bisnis UKRIDA:",
        space_after=6
    )
    
    panitia_entries = [
        # (Jabatan, Colon, Nama + NIM, is_bold, space_after_pt)
        ("Pelindung", ":", "Dekan Fakultas Ekonomi dan Bisnis\nDr. Diana Frederica S.E., M.Ak., CFP®., CHCP-A", False, 4),
        ("Penasehat", ":", "Wakil Dekan Fakultas Ekonomi dan Bisnis\nDr. Daniel Widjaja, S.E., M.M., CSCU, CEAP", False, 4),
        ("Ketua BEM FEB", ":", "Arthur Reezan\t(312023002)", False, 2),
        ("Wakil Ketua BEM FEB", ":", "Princess Auralia Barus\t(322024025)", False, 2),
        ("Ketua Pelaksana", ":", "Fellicia Florens\t(322024018)", False, 2),
        ("Wakil Ketua Pelaksana", ":", "Michelle Angelina\t(312024012)", False, 2),
        ("Sekretaris I", ":", "Jessica Violant Nathaniel\t(322024015)", False, 2),
        ("Sekretaris II", ":", "Rachel Angelina Tjahja\t(322024033)", False, 2),
        ("Bendahara I", ":", "Jemima Putri Sutanta\t(312024022)", False, 2),
        ("Bendahara II", ":", "Vanessa Clarissa\t(322024008)", False, 6),
        
        ("Koordinator Acara", ":", "Jocelyn Jennifer\t(312024005)", True, 2),
        ("Anggota Acara", ":", "Christopher Kevin\t(322024030)\nStephanie Nicole\t(312024019)", False, 6),
        
        ("Koordinator Perlengkapan", ":", "William Hans\t(322024040)", True, 2),
        ("Anggota Perlengkapan", ":", "Michael Jonathan\t(312024028)\nDavid Surya\t(322024011)", False, 6),
        
        ("Koordinator Pubdok", ":", "Bryan Alexander\t(312024035)", True, 2),
        ("Anggota Pubdok", ":", "Sharon Priscilla\t(322024029)", False, 6),
        
        ("Koordinator Humas & Sponsor", ":", "Nathania Graciela\t(312024016)", True, 2),
        ("Anggota Humas & Sponsor", ":", "Steven Immanuel\t(322024021)", False, 6),
        
        ("Koordinator Konsumsi", ":", "Clarissa Evelyn\t(312024009)", True, 2),
        ("Anggota Konsumsi", ":", "Jennifer Amanda\t(322024027)", False, 4),
    ]
    
    t_panitia = doc.add_table(rows=len(panitia_entries), cols=3)
    t_panitia.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_panitia.autofit = False
    set_table_borderless(t_panitia)
    set_table_cell_margins(t_panitia, top=30, bottom=30, left=40, right=40)
    
    panitia_widths = [Cm(4.6), Cm(0.4), Cm(9.0)]
    
    for idx, (jabatan, colon, nama_nim, is_bold, sp_after) in enumerate(panitia_entries):
        row = t_panitia.rows[idx]
        
        # Col 0: Jabatan
        c0 = row.cells[0]
        c0.text = jabatan
        c0.width = panitia_widths[0]
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p0.paragraph_format.line_spacing = 1.15
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(sp_after)
        for r in p0.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(12)
            r.bold = is_bold
            r.font.color.rgb = RGBColor(0, 0, 0)
            
        # Col 1: Colon
        c1 = row.cells[1]
        c1.text = colon
        c1.width = panitia_widths[1]
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.line_spacing = 1.15
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(sp_after)
        for r in p1.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(12)
            r.bold = is_bold
            r.font.color.rgb = RGBColor(0, 0, 0)
            
        # Col 2: Nama Lengkap & NIM
        c2 = row.cells[2]
        c2.text = nama_nim
        c2.width = panitia_widths[2]
        p2 = c2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p2.paragraph_format.line_spacing = 1.15
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(sp_after)
        for r in p2.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(12)
            r.bold = is_bold
            r.font.color.rgb = RGBColor(0, 0, 0)
            
    prevent_row_split_and_repeat_header(t_panitia)
    
    # ==============================================================
    # 7. BAB V: ANGGARAN (STANDAR LKMM II DENGAN SHADING SOFT GREEN)
    # ==============================================================
    add_bab_heading(doc, "V. ANGGARAN")
    
    # Header color khas Google Docs LK FEB (#B3E4A1)
    ACCENT_GREEN = "B3E4A1"
    
    # A. PEMASUKAN
    add_sub_heading(doc, "A. RENCANA PEMASUKAN")
    
    t_masuk = doc.add_table(rows=1, cols=3)
    format_standard_table(
        t_masuk,
        [Cm(1.2), Cm(9.3), Cm(3.5)],
        ["No", "Susunan Anggaran Keseluruhan", "Jumlah"],
        [
            ("1", "Dana Sponsorship PT. Inti Citra Agung (Optik Melawai)", "Rp. 3.000.000"),
            ("", "TOTAL PEMASUKAN", "Rp. 3.000.000"),
        ],
        [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT],
        header_bg=ACCENT_GREEN,
        font_size=11
    )
    # Bold baris total pemasukan
    for c in t_masuk.rows[-1].cells:
        for p in c.paragraphs:
            for r in p.runs:
                r.bold = True
                
    # B. PENGELUARAN
    add_sub_heading(doc, "B. RENCANA PENGELUARAN")
    
    div_tables_data = [
        ("1. Divisi Acara", [
            ("1", "Plakat Akrilik Penghargaan Narasumber", "1 buah", "Rp. 250.000", "Rp. 250.000"),
            ("2", "Paket Cinderamata / Goodie Bag Pemateri & Mitra", "2 paket", "Rp. 150.000", "Rp. 300.000"),
            ("3", "Cetak Sertifikat Kertas Linen & Map Panitia/Peserta", "40 lembar", "Rp. 5.000", "Rp. 200.000"),
            ("", "TOTAL DIVISI ACARA", "", "", "Rp. 750.000"),
        ]),
        ("2. Divisi Konsumsi", [
            ("1", "Snack Box Narasumber & Tamu Khusus", "10 box", "Rp. 25.000", "Rp. 250.000"),
            ("2", "Makan Siang Panitia Pelaksana (2 Hari)", "32 porsi", "Rp. 25.000", "Rp. 800.000"),
            ("", "TOTAL DIVISI KONSUMSI", "", "", "Rp. 1.050.000"),
        ]),
        ("3. Divisi Publikasi dan Dokumentasi (Pubdok)", [
            ("1", "Cetak Backdrop Panggung Auditorium (Ukuran 4 x 2 m)", "1 buah", "Rp. 250.000", "Rp. 250.000"),
            ("2", "Cetak Standing Banner / X-Banner Edukasi & Petunjuk", "2 buah", "Rp. 100.000", "Rp. 200.000"),
            ("3", "Tali Lanyard & ID Card Panitia Pelaksana", "20 pcs", "Rp. 2.500", "Rp. 50.000"),
            ("", "TOTAL DIVISI PUBDOK", "", "", "Rp. 500.000"),
        ]),
        ("4. Divisi Perlengkapan dan Logistik", [
            ("1", "Sewa Kabel Roll Heavy Duty (Daya Tinggi)", "2 unit", "Rp. 100.000", "Rp. 200.000"),
            ("2", "Baterai Wireless Microphone (Alkaline AA/9V)", "4 set", "Rp. 25.000", "Rp. 100.000"),
            ("3", "Lakban Hitam Kabel & Floor Marking Booth", "3 roll", "Rp. 25.000", "Rp. 75.000"),
            ("4", "Kantong Plastik Trash Bag & Sarung Tangan", "3 pack", "Rp. 25.000", "Rp. 75.000"),
            ("", "TOTAL DIVISI PERLENGKAPAN", "", "", "Rp. 450.000"),
        ]),
        ("5. Divisi Humas dan P3K", [
            ("1", "Air Mineral Botol & Dus Meja Registrasi", "3 dus", "Rp. 50.000", "Rp. 150.000"),
            ("2", "Kotak Obat P3K & Sanitizer Area Pemeriksaan", "1 paket", "Rp. 100.000", "Rp. 100.000"),
            ("", "TOTAL DIVISI HUMAS & P3K", "", "", "Rp. 250.000"),
        ]),
    ]
    
    for div_title, div_items in div_tables_data:
        p_div = doc.add_paragraph()
        p_div.paragraph_format.left_indent = Cm(1.27)
        p_div.paragraph_format.space_before = Pt(8)
        p_div.paragraph_format.space_after = Pt(2)
        r_dt = p_div.add_run(div_title)
        r_dt.font.name = "Times New Roman"
        r_dt.font.size = Pt(11.5)
        r_dt.bold = True
        
        t_div = doc.add_table(rows=1, cols=5)
        format_standard_table(
            t_div,
            [Cm(1.0), Cm(5.8), Cm(2.2), Cm(2.5), Cm(2.5)],
            ["No", "Uraian Kebutuhan", "Qty", "Harga Satuan", "Subtotal"],
            div_items,
            [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT],
            header_bg=ACCENT_GREEN,
            font_size=10.5
        )
        for c in t_div.rows[-1].cells:
            for p in c.paragraphs:
                for r in p.runs:
                    r.bold = True
                    
    # C. REKAPITULASI ANGGARAN BIAYA
    add_sub_heading(doc, "C. REKAPITULASI ANGGARAN BIAYA")
    
    rekap_data = [
        ("1", "Divisi Acara", "Rp. 750.000"),
        ("2", "Divisi Konsumsi", "Rp. 1.050.000"),
        ("3", "Divisi Publikasi dan Dokumentasi (Pubdok)", "Rp. 500.000"),
        ("4", "Divisi Perlengkapan dan Logistik", "Rp. 450.000"),
        ("5", "Divisi Humas dan P3K", "Rp. 250.000"),
        ("", "TOTAL PENGELUARAN", "Rp. 3.000.000"),
    ]
    t_rekap = doc.add_table(rows=1, cols=3)
    format_standard_table(
        t_rekap,
        [Cm(1.2), Cm(9.3), Cm(3.5)],
        ["No", "Divisi Operasional", "Alokasi Dana"],
        rekap_data,
        [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT],
        header_bg=ACCENT_GREEN,
        font_size=11
    )
    for c in t_rekap.rows[-1].cells:
        for p in c.paragraphs:
            for r in p.runs:
                r.bold = True
                
    # Tabel Neraca Balance (Total Pemasukan = Total Pengeluaran, Sisa = 0)
    p_sp_neraca = doc.add_paragraph()
    p_sp_neraca.paragraph_format.space_before = Pt(6)
    p_sp_neraca.paragraph_format.space_after = Pt(2)
    
    t_neraca = doc.add_table(rows=3, cols=2)
    t_neraca.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_neraca.autofit = False
    set_table_borders(t_neraca, val="single", sz="6", color="000000")
    set_table_cell_margins(t_neraca, top=90, bottom=90, left=140, right=140)
    
    neraca_widths = [Cm(10.5), Cm(3.5)]
    neraca_rows = [
        ("Total Rencana Pemasukan", "Rp. 3.000.000"),
        ("Total Rencana Pengeluaran", "Rp. 3.000.000"),
        ("Sisa Saldo Anggaran (BALANCE)", "Rp. 0"),
    ]
    for idx, (label, val) in enumerate(neraca_rows):
        row = t_neraca.rows[idx]
        row.cells[0].text = label
        row.cells[1].text = val
        row.cells[0].width = neraca_widths[0]
        row.cells[1].width = neraca_widths[1]
        
        # Beri shading hijau pada baris Sisa Saldo (BALANCE)
        if idx == 2:
            set_cell_shading(row.cells[0], ACCENT_GREEN)
            set_cell_shading(row.cells[1], ACCENT_GREEN)
            
        p0 = row.cells[0].paragraphs[0]
        p1 = row.cells[1].paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p0.paragraph_format.line_spacing = 1.15
        p1.paragraph_format.line_spacing = 1.15
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(0)
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        
        for r in p0.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)
            r.bold = True
            r.font.color.rgb = RGBColor(0, 0, 0)
        for r in p1.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)
            r.bold = True
            r.font.color.rgb = RGBColor(0, 0, 0)
            
    prevent_row_split_and_repeat_header(t_neraca)
    
    # ==============================================================
    # 8. BAB VI: PENUTUP & LEMBAR PENGESAHAN (STANDAR TTD LKMM II)
    # ==============================================================
    add_bab_heading(doc, "VI. PENUTUP")
    
    add_body_paragraph(
        doc,
        "Demikianlah proposal ini kami ajukan dengan penuh harapan agar kegiatan yang direncanakan dapat berjalan "
        "dengan sukses dan memberikan dampak positif bagi seluruh civitas akademika Fakultas Ekonomi dan Bisnis UKRIDA. "
        "Kami sangat mengapresiasi segala bentuk dukungan, kerja sama, dan partisipasi aktif dari berbagai pihak. "
        "Atas perhatian dan kerja sama yang baik dari Bapak/Ibu pimpinan serta rekan-rekan mahasiswa, kami sampaikan terima kasih."
    )
    
    # Tanggal di atas TTD
    p_tgl = doc.add_paragraph()
    p_tgl.paragraph_format.space_before = Pt(12)
    p_tgl.paragraph_format.space_after = Pt(4)
    p_tgl.paragraph_format.left_indent = Cm(7.0)
    p_tgl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_tgl = p_tgl.add_run("Jakarta, 01 September 2026")
    r_tgl.font.name = "Times New Roman"
    r_tgl.font.size = Pt(12)
    r_tgl.font.color.rgb = RGBColor(0, 0, 0)
    
    # Hormat Kami
    p_hk = doc.add_paragraph()
    p_hk.paragraph_format.space_before = Pt(0)
    p_hk.paragraph_format.space_after = Pt(8)
    p_hk.paragraph_format.left_indent = Cm(7.0)
    p_hk.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_hk = p_hk.add_run("Hormat kami,")
    r_hk.font.name = "Times New Roman"
    r_hk.font.size = Pt(12)
    r_hk.bold = True
    r_hk.font.color.rgb = RGBColor(0, 0, 0)
    
    # Baris 1 TTD: Panitia Pelaksana & Ketua BEM (3 Kolom)
    t_ttd1 = doc.add_table(rows=1, cols=3)
    t_ttd1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_ttd1.autofit = False
    set_table_borderless(t_ttd1)
    set_table_cell_margins(t_ttd1, top=40, bottom=40, left=40, right=40)
    
    ttd1_widths = [Cm(4.6), Cm(4.7), Cm(4.7)]
    ttd1_data = [
        ("Ketua Pelaksana\n\n\n\n\n", "Fellicia Florens", "NIM: 322024018"),
        ("Sekretaris Pelaksana\n\n\n\n\n", "Jessica Violant Nathaniel", "NIM: 322024015"),
        ("Ketua BEM FEB UKRIDA\n\n\n\n\n", "Arthur Reezan", "NIM: 312023002"),
    ]
    for c_idx, (jabatan, nama, nim) in enumerate(ttd1_data):
        cell = t_ttd1.rows[0].cells[c_idx]
        cell.width = ttd1_widths[c_idx]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        
        # Jabatan
        r_j = p.add_run(jabatan)
        r_j.font.name = "Times New Roman"
        r_j.font.size = Pt(11)
        r_j.font.color.rgb = RGBColor(0, 0, 0)
        
        # Nama (Bold & Underline)
        r_n = p.add_run(nama + "\n")
        r_n.font.name = "Times New Roman"
        r_n.font.size = Pt(11.5)
        r_n.bold = True
        r_n.underline = True
        r_n.font.color.rgb = RGBColor(0, 0, 0)
        
        # NIM
        r_m = p.add_run(nim)
        r_m.font.name = "Times New Roman"
        r_m.font.size = Pt(10.5)
        r_m.font.color.rgb = RGBColor(0, 0, 0)
        
    prevent_row_split_and_repeat_header(t_ttd1)
    
    # Mengetahui Pimpinan Fakultas
    p_mengetahui = doc.add_paragraph()
    p_mengetahui.paragraph_format.space_before = Pt(18)
    p_mengetahui.paragraph_format.space_after = Pt(8)
    p_mengetahui.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_mgt = p_mengetahui.add_run("Mengetahui,")
    r_mgt.font.name = "Times New Roman"
    r_mgt.font.size = Pt(12)
    r_mgt.bold = True
    r_mgt.font.color.rgb = RGBColor(0, 0, 0)
    
    # Baris 2 TTD: Wakil Dekan & Dekan FEB UKRIDA (2 Kolom)
    t_ttd2 = doc.add_table(rows=1, cols=2)
    t_ttd2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_ttd2.autofit = False
    set_table_borderless(t_ttd2)
    set_table_cell_margins(t_ttd2, top=40, bottom=40, left=40, right=40)
    
    ttd2_widths = [Cm(7.0), Cm(7.0)]
    ttd2_data = [
        ("Wakil Dekan FEB UKRIDA\n\n\n\n\n", "Dr. Daniel Widjaja, S.E., M.M., CSCU, CEAP"),
        ("Dekan Fakultas Ekonomi & Bisnis\n\n\n\n\n", "Dr. Diana Frederica S.E., M.Ak., CFP®., CHCP-A"),
    ]
    for c_idx, (jabatan, nama) in enumerate(ttd2_data):
        cell = t_ttd2.rows[0].cells[c_idx]
        cell.width = ttd2_widths[c_idx]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        
        # Jabatan
        r_j = p.add_run(jabatan)
        r_j.font.name = "Times New Roman"
        r_j.font.size = Pt(11)
        r_j.font.color.rgb = RGBColor(0, 0, 0)
        
        # Nama (Bold & Underline)
        r_n = p.add_run(nama)
        r_n.font.name = "Times New Roman"
        r_n.font.size = Pt(11.5)
        r_n.bold = True
        r_n.underline = True
        r_n.font.color.rgb = RGBColor(0, 0, 0)
        
    prevent_row_split_and_repeat_header(t_ttd2)
    
    # Simpan file docx
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"✅ Dokumen resmi Word berhasil digenerate ke: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_proposal_docx()
