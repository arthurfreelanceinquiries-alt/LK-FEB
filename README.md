# 🏛️ SEKRETARIS DIGITAL BEM FEB UKRIDA

> Repository resmi tata kelola administrasi, standardisasi dokumen, audit otomatis, dan knowledge base BEM FEB Universitas Kristen Krida Wacana (UKRIDA).

---

## 📌 Ringkasan Sistem

Sistem ini dirancang untuk mengotomatisasi, menyusun, mengaudit, dan mengarsipkan dokumen-dokumen resmi BEM FEB UKRIDA (Proposal Kegiatan, SPU, LPU/LPJ) dengan kepatuhan format 100% terhadap standar universitas dan fakultas.

### 🏛️ Identitas & Konteks Organisasi
- **Organisasi:** BEM FEB (Badan Eksekutif Mahasiswa Fakultas Ekonomi dan Bisnis)
- **Universitas:** UKRIDA (Universitas Kristen Krida Wacana)
- **Alamat:** Jl. Tanjung Duren Raya No. 4, Jakarta Barat
- **Telp:** 021 566 6952 | **Fax:** 021 566 6956
- **Ketua BEM:** Arthur Reezan (NIM: 312023002)
- **Pelindung:** Dekan FEB — Dr. Diana Frederica S.E., M.Ak., CFP®., CHCP-A
- **Penasehat:** Wakil Dekan — Dr. Daniel Widjaja, S.E., M.M., CSCU, CEAP

---

## 🏗️ Arsitektur 3-Layer

```
┌────────────────────────────────────────────────────────┐
│  Layer 1 — DIRECTIVES (SOP & Rules dalam Markdown)     │
│  • directives/01_workflow_proposal.md                  │
│  • directives/04_audit_checklist.md                    │
│  • directives/05_audit_tipografi_typo.md               │
└───────────────────────────▲────────────────────────────┘
                            │
┌───────────────────────────┴────────────────────────────┐
│  Layer 2 — ORCHESTRATION (Decision Maker & Context)     │
│  • AGENTS.md                                           │
│  • 00_DASHBOARD_SECOND_BRAIN.md                        │
│  • .agents/skills/bem-sekretaris/                      │
└───────────────────────────▲────────────────────────────┘
                            │
┌───────────────────────────┴────────────────────────────┐
│  Layer 3 — EXECUTION (Python Scripts Deterministik)    │
│  • execution/pdf_extractor.py                          │
│  • execution/rab_validator.py                          │
│  • execution/typo_checker.py                           │
└────────────────────────────────────────────────────────┘
```

---

## 📂 Struktur Direktori

```
LK FEB/
├── AGENTS.md                          # Instruksi agen & standar dokumen BEM
├── 00_DASHBOARD_SECOND_BRAIN.md       # Kokpit status proyek & log riwayat
├── 00_PROMPT_MULAI_SESI.md            # Prompt template sinkronisasi sesi
├── README.md                          # Dokumentasi repository
├── .gitignore                         # Rule ignore git
├── .graphifyignore                    # Filter Graphify knowledge graph
│
├── 00_SISTEM_BEM/                     # PRD, Architecture, Implementation Plan
│   ├── PRD_SEKRETARIS_BEM.md
│   ├── PRD_TIPOGRAFI_MARGIN_TYPO.md
│   ├── IMPLEMENTATION_PLAN.md
│   └── IMPLEMENTATION_PLAN_TIPOGRAFI.md
│
├── 01_Proposal/                       # Workspace pembuatan Proposal baru
├── 02_SPU/                            # Surat Pengajuan / Pernyataan Umum
├── 03_LPU/                            # Laporan Pertanggungjawaban / Pelaksanaan
│
├── 04_Arsip_Acara/                    # Arsip kegiatan BEM yang telah selesai
│   ├── PKKMB_2026/                    # Dokumen & surat PKKMB FEB 2026
│   ├── LKMM_II_2026/                  # Dokumen LKMM Tingkat II 2026
│   └── OPTIK_MELAWAI_2026/            # Kerjasama & invoice Optik Melawai
│
├── 05_Referensi_Template/             # Master template proposal, SPU, LPU
│   ├── TEMPLATE_PROPOSAL.md
│   ├── TEMPLATE_SPU.md
│   └── TEMPLATE_LPU.md
│
├── 06_Audit_Review/                   # Hasil audit skor & checklist dokumen
├── 07_Second_Brain/                   # Analisis benchmarking & catatan kontekstual
│   └── analisis_proposal_PKKMB_2026.md
│
├── directives/                        # Standard Operating Procedures (SOP)
│   ├── 01_workflow_proposal.md
│   ├── 04_audit_checklist.md
│   └── 05_audit_tipografi_typo.md
│
├── execution/                         # Script audit deterministik
│   ├── pdf_extractor.py               # Ekstraksi teks & tabel dari PDF
│   ├── rab_validator.py               # Audit aritmatika & balance RAB
│   └── typo_checker.py                # Audit tipografi & deteksi typo baku
│
├── graphify-out/                      # Graphify Knowledge Graph output
└── .agents/                           # Custom skills dan rules
```

---

## 🛠️ Script Audit & Penggunaan

### 1. Typo & Typography Checker
Memeriksa kepatuhan penulisan kata baku, istilah UKRIDA, penulisan rupiah, gelar pejabat, dan nomor surat:
```bash
python -X utf8 execution/typo_checker.py --input "01_Proposal/[nama_acara]/proposal.md" --verbose
```

### 2. RAB & Budget Validator
Memeriksa keakuratan perkalian subtotal, penjumlahan rekap divisi, serta balance pemasukan vs pengeluaran:
```bash
python execution/rab_validator.py --input "01_Proposal/[nama_acara]/rab.json"
```

### 3. PDF Extractor
Mengekstrak teks mentah dan tabel dari berkas acuan PDF untuk analisis komparasi:
```bash
python execution/pdf_extractor.py --input "path/to/document.pdf"
```

---

## 📋 Standar Dokumen Wajib BEM FEB UKRIDA

- **Format Penomoran Surat:** `[No]/[Kode-Acara]/BEM-FEB-UKRIDA/[Bulan-Romawi]/[Tahun]`
- **Tipografi:** Times New Roman, 12pt, Spasi 1.5, Justify
- **Margin Standar:** Atas 4 cm, Kiri 4 cm, Bawah 3 cm, Kanan 3 cm (A4)
- **Hierarki Bab:** Romawi (`I, II, III`) ➔ Huruf Kapital (`A, B, C`) ➔ Angka (`1, 2, 3`) ➔ Huruf Kecil (`a, b, c`)
- **Tabel RAB:** `No | Keterangan | Rincian | Qty | Satuan | Harga Satuan | Total`
- **Total Saldo:** Pemasukan = Pengeluaran (Balance Rp 0)

---
© BEM FEB UKRIDA — Sekretariat Jenderal
