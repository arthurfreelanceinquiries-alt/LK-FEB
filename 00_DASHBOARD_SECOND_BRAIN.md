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

### Dari Analisis PKKMB 2026:
- Proposal terdiri dari **16 halaman**
- Anggaran total: **Rp 10.710.000** (balance sempurna: Sisa Rp 0)
- Peserta: Mahasiswa baru 2026 + angkatan 2023-2025 yang belum PKKMB
- Kegiatan: 2 hari offline + 1 sesi online
- Narasumber: 3 orang (2 dosen + 1 pihak eksternal)
- Games: 5 jenis dengan tujuan berbeda
- Panitia inti: ~30 orang dengan 5 sie (Acara, Perlengkapan, Pubdok, Humas, Konsumsi)

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
| 28 Sep 2026 | Sesi 1 | Inisialisasi Git, setup .gitignore, dan push ke GitHub (Private) | Repo private terunggah di GitHub |

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
