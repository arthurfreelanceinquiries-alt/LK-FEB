# 🧠 DASHBOARD SECOND BRAIN — SEKRETARIS BEM FEB UKRIDA
### *Badan Eksekutif Mahasiswa — Fakultas Ekonomi & Bisnis — Universitas Kristen Krida Wacana*
### *Periode 2026*

> [!SUMMARY] Tujuan & Fungsi Dashboard Ini
> - **Untuk Apa:** Kokpit utama (*Master Dashboard*) yang WAJIB dibaca Antigravity di setiap awal sesi untuk sinkronisasi konteks instan.
> - **Masalah yang Diselesaikan:** Menghilangkan fragmentasi dokumen; menghubungkan semua proposal, SPU, LPU, template, dan arsip ke dalam satu pusat navigasi.
> - **Output:** Digunakan untuk generate, audit, dan arsip dokumen BEM FEB UKRIDA (Proposal, SPU, LPU) dengan standar kerapihan tinggi.

---

## 📌 1. Identitas & Parameter Kunci Organisasi

- **Organisasi:** BEM FEB UKRIDA (Badan Eksekutif Mahasiswa Fakultas Ekonomi dan Bisnis UKRIDA)
- **Periode:** 2026
- **Alamat:** Jl. Tanjung Duren Raya No. 4, Jakarta Barat
- **Telepon:** 021 566 6952 | **Fax:** 021 566 6956
- **Ketua BEM FEB:** Arthur Reezan (312023002)
- **Wakil Ketua BEM FEB:** Princess Auralia Barus (322024025)
- **Pelindung:** Dr. Diana Frederica S.E., M.Ak., CFP®., CHCP-A (Dekan FEB)
- **Penasehat:** Dr. Daniel Widjaja, S.E., M.M., CSCU, CEAP (Wakil Dekan)
- **GitHub Repository:** [arthurfreelanceinquiries-alt/LK-FEB](https://github.com/arthurfreelanceinquiries-alt/LK-FEB) (Private)

---

## 🗺️ 2. Map of Content — Navigasi Vault

```
                    [ 00_DASHBOARD_SECOND_BRAIN ]
                                 │
     ┌──────────┬───────────┬────┴────┬──────────┬──────────┐
     ▼          ▼           ▼         ▼          ▼          ▼
[01_Proposal] [02_SPU]  [03_LPU]  [04_Arsip] [05_Template] [06_Audit]
  Proposal     Surat      Laporan   Acara      Referensi     Review
  Per Acara    Pengajuan  Per Acara Selesai    & Contoh      Dokumen
```

---

## 📋 3. Status Acara & Dokumen Terkini

### 🟢 Selesai & Diarsipkan
| Acara | Dokumen | Tanggal | Lokasi Arsip |
|-------|---------|---------|-------------|
| PKKMB FEB 2026 | Proposal, Surat Undangan, SPU | Agt 2026 | `04_Arsip_Acara/PKKMB_2026/` |
| LKMM Tingkat II 2026 | Proposal, LPJ | 2026 | `04_Arsip_Acara/LKMM_II_2026/` |
| Seminar Optik Melawai | SPU, Invoice | 2026 | `04_Arsip_Acara/OPTIK_MELAWAI_2026/` |
| OMGTC FEB UKRIDA 2026 | Proposal Resmi (.md & .docx), RAB, Audit Review | Sep 2026 | `01_Proposal/OMGTC_2026/` |

### 🟡 Sedang Berjalan
| Acara | Dokumen | Status | Lokasi File |
|-------|---------|--------|-------------|
| *(belum ada)* | - | - | - |

### 🔴 Belum Dimulai
| Acara | Jenis Dokumen | Target |
|-------|--------------|--------|
| *(tambahkan di sini)* | - | - |

---

## 📁 4. Navigasi File Penting

### A. Sistem & Panduan
- **AGENTS.md** → Instruksi lengkap agen AI
- **00_PROMPT_MULAI_SESI.md** → Copy-paste untuk mulai sesi baru
- **00_SISTEM_BEM/PRD_SEKRETARIS_BEM.md** → Product Requirements Document
- **00_SISTEM_BEM/PRD_TIPOGRAFI_MARGIN_TYPO.md** → Standar margin, font, typo
- **00_SISTEM_BEM/IMPLEMENTATION_PLAN.md** → Rencana implementasi sistem
- **00_SISTEM_BEM/IMPLEMENTATION_PLAN_TIPOGRAFI.md** → Rencana implementasi tipografi

### B. Templates & Referensi Format
- **05_Referensi_Template/TEMPLATE_PROPOSAL.md** → Template proposal standar
- **05_Referensi_Template/TEMPLATE_SPU.md** → Template SPU standar
- **05_Referensi_Template/TEMPLATE_LPU.md** → Template LPU standar
- **07_Second_Brain/analisis_proposal_PKKMB_2026.md** → Analisis gold standard PKKMB 2026

### C. Directives (SOP)
- **directives/01_workflow_proposal.md** → SOP membuat proposal
- **directives/04_audit_checklist.md** → Checklist audit struktur & isi (Lapis 1, 60%)
- **directives/05_audit_tipografi_typo.md** → Checklist audit tipografi & typo (Lapis 2, 40%)

### D. Execution Scripts
- **execution/pdf_extractor.py** → Ekstrak teks dari PDF referensi
- **execution/rab_validator.py** → Validasi balance RAB (Pemasukan = Pengeluaran)
- **execution/typo_checker.py** → Cek typo & format otomatis (jalankan: `python -X utf8 execution/typo_checker.py --input [file]`)

### E. Arsip Acara
- **04_Arsip_Acara/PKKMB_2026/** → Semua dokumen PKKMB 2026
- **04_Arsip_Acara/LKMM_II_2026/** → Semua dokumen LKMM II 2026
- **04_Arsip_Acara/OPTIK_MELAWAI_2026/** → Semua dokumen Optik Melawai 2026

---

## 🔍 5. Standar Kerapihan Dokumen (Referensi: PKKMB 2026)

Berdasarkan analisis **Proposal PKKMB FEB 2026**, standar kerapihan yang WAJIB diikuti:

### ✅ Struktur Wajib:
```
I.   LATAR BELAKANG          → Minimal 3 paragraf, kontekstual
II.  TEMA KEGIATAN           → Nama tema + singkatan + makna
III. KEGIATAN
     A. Tujuan Kegiatan      → Minimal 5 poin
     B. Manfaat Kegiatan     → Minimal 3 poin
     C. Target Peserta       → Deskripsi jelas siapa pesertanya
     D. Pelaksanaan          → Hari, Tanggal, Tempat
     E. Narasumber           → (jika ada)
     F. Susunan Acara        → Rundown lengkap per hari
     G. Games/Khusus        → (jika ada, dengan tujuan masing-masing)
IV.  KEPANITIAAN             → Hierarki lengkap + NIM
V.   ANGGARAN                → Pemasukan + Pengeluaran (balance)
VI.  PENUTUP                 → Paragraf + tanggal + tanda tangan
```

### ✅ Format RAB Wajib:
```
PEMASUKAN:
No | Sumber Dana            | Jumlah
---+------------------------+-------------
1  | Dana Universitas       | Rp. X
2  | Dana Fakultas          | Rp. Y
   | TOTAL                  | Rp. X+Y

PENGELUARAN (per divisi):
No | Keterangan | Rincian | Qty | Harga Satuan | Total
   | ...        | ...     | ... | ...          | ...
   | TOTAL per divisi      |     |              | Rp. Z
   
REKAP:
Acara: Rp. A | Konsumsi: Rp. B | Pubdok: Rp. C | dll.
TOTAL PENGELUARAN = TOTAL PEMASUKAN (SISA = Rp. 0)
```

### ✅ Format Kepanitiaan Wajib:
```
Pelindung       : [Jabatan] — [Nama lengkap gelar]
Penasehat       : [Jabatan] — [Nama lengkap gelar]
Ketua BEM FEB   : [Nama] ([NIM])
Wakil Ketua     : [Nama] ([NIM])
Pengawas        : [Nama] ([NIM])
Ketua Pelaksana : [Nama] ([NIM])
Wakil Ketupel   : [Nama] ([NIM])
Sekretaris      : [Nama] ([NIM])
Bendahara       : [Nama] ([NIM])
Koordinator [Sie] : [Nama] ([NIM])
Anggota [Sie]   : [Nama] ([NIM])
```

---

## 🧠 6. Catatan Konteks & Pembelajaran

### Dari Analisis LKMM II & PKKMB 2026 (Format Baku Autentik Google Docs):
- **Margin Baku:** Kiri 4.0 cm (Binding), Atas 3.0 cm, Kanan 3.0 cm, Bawah 3.0 cm (Standar 4-3-3-3).
- **Tipografi Murni:** 100% Times New Roman, warna hitam pekat `#000000`, 12 pt konsisten (10.5-11 pt untuk tabel padat).
- **Cover Resmi:** Judul 12 pt Bold Centered, Tema 12 pt Bold Italic Centered, 1 Logo Besar BEM FEB UKRIDA (~11.5 cm) di tengah, identitas organisasi lengkap di bawah.
- **Halaman Isi:** Dimulai langsung Halaman 2 dengan `I. LATAR BELAKANG` (TANPA kop surat berulang di dalam proposal multi-halaman).
- **Format Kepanitiaan:** Tabel borderless 3 kolom (`Jabatan : Nama (NIM)`), rapi sejajar tanpa kotak-kotak kaku/zebra striping.
- **Format Tabel (Rundown & Anggaran):** Border solid hitam 0.75 pt, header anggaran beraksen soft green `#B3E4A1`, baris Total dan Sisa Saldo Rp. 0 (Balance).
- **Lembar Pengesahan (TTD):** Nama penandatangan **Bold + Underline** (`<u>Nama Lengkap</u>`), penataan borderless horizontal sejajar.

### Keputusan Format:
- Nomor bab: Angka Romawi (I, II, III...)
- Sub-poin: Huruf kapital (A, B, C...)
- Sub-sub: Angka (1, 2, 3...)
- Tanggal: "Jakarta, DD Bulan YYYY"
- Rupiah: "Rp. X.XXX.XXX" (dengan titik pemisah ribuan)

---

## 🔄 7. Log Sesi Terkini

| Tanggal | Sesi | Kegiatan | Output |
|---------|------|----------|--------|
| 28 Sep 2026 | Sesi 1 | Setup sistem, analisis PKKMB 2026 | Sistem lengkap + analisis proposal |
| 28 Sep 2026 | Sesi 1 | Buat PRD + SOP tipografi, margin, typo checker | 4 file baru, script Python berfungsi |
| 28 Sep 2026 | Sesi 1 | Konsolidasi struktur folder — arsipkan PKKMB, LKMM II, Optik Melawai | Semua dalam 1 folder besar, bersih |
| 28 Sep 2026 | Sesi 2 | Analisis proposal vendor OMGTC, rancang PRD & Implementation Plan, drafting Proposal resmi UKRIDA, & Audit Lapis 1-2 | Analisis, PRD, Plan, Proposal final, RAB JSON, & Audit lolos 10/10 |
| 29 Sep 2026 | Sesi 3 | Analisis mendalam referensi `PROPOSAL LKMM TINGKAT II 2026 - Google Docs.pdf` & perombakan total `docx_generator.py` | Format 100% identik Google Docs: Margin 4-3-3-3, Cover 1 Logo HD BEM FEB, hapus kop berulang, TTD bold+underline |
| 29 Sep 2026 | Sesi 3 | Revisi visual: ubah warna header tabel ke abu-abu netral (#E0E0E0) & presisi perataan NIM via tabel 4-kolom | Tabel anggaran & rundown seragam abu-abu elegan; NIM kepanitiaan 100% sejajar vertikal |
| 29 Sep 2026 | Sesi 4 | Hilangkan rincian pengeluaran divisi OMGTC (Swadana Vendor, Pengeluaran BEM FEB: Rp. 0) & perbaiki transparansi logo BEM FEB (buang background kotak hitam) | Proposal docx, md, rab.json diperbarui, logo transparan murni RGBA, validasi RAB PASS |

---

## ⚡ 8. Quick Start — Perintah Cepat

**Untuk membuat proposal baru:**
> "Buat proposal [nama acara] dengan tema [tema], tanggal [tanggal], tempat [tempat]"

**Untuk mengaudit dokumen:**
> "Audit proposal [nama file]"

**Untuk membuat SPU:**
> "Buat SPU untuk [nama acara] — kebutuhan: [deskripsi]"

**Untuk membuat LPU:**
> "Buat LPU untuk [nama acara] berdasarkan proposal [nama file]"
