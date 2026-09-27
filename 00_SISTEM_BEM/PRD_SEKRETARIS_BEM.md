# PRD — Product Requirements Document
## Sistem Sekretaris Digital BEM FEB UKRIDA

**Versi:** 1.0  
**Tanggal:** 28 September 2026  
**Penulis:** Antigravity AI (atas instruksi Arthur Reezan — Ketua BEM FEB UKRIDA)

---

## 1. Latar Belakang & Masalah

### Masalah yang Ada:
1. **Dokumen tidak konsisten** — setiap acara format proposal berbeda-beda
2. **Anggaran sering tidak balance** — total pemasukan ≠ total pengeluaran
3. **Struktur kepanitiaan tidak seragam** — kadang ada NIM, kadang tidak
4. **Tidak ada arsip terstruktur** — dokumen tersebar di berbagai folder
5. **AI tidak ingat konteks** — setiap sesi mulai dari nol

### Tujuan Sistem Ini:
- Standarisasi format seluruh dokumen BEM FEB UKRIDA
- Otomatisasi pembuatan, validasi, dan audit dokumen
- Persistensi konteks melalui Second Brain & Graphify
- Kecepatan produksi dokumen: dari **3 jam → 15 menit**

---

## 2. User Stories

### US-01: Membuat Proposal Baru
**Sebagai** Ketua/Sekretaris BEM  
**Saya ingin** mengisi detail acara dan mendapatkan proposal lengkap  
**Agar** proposal siap diajukan ke Dekan dalam 15 menit

**Acceptance Criteria:**
- [ ] Proposal mengikuti struktur I-VI wajib
- [ ] RAB balance (Pemasukan = Pengeluaran)
- [ ] Kepanitiaan lengkap dengan NIM
- [ ] Rundown lengkap per hari dengan durasi
- [ ] Format tanggal: "Jakarta, DD Bulan YYYY"

### US-02: Mengaudit Dokumen
**Sebagai** Ketua BEM  
**Saya ingin** mengetahui kesalahan/kekurangan dalam dokumen  
**Agar** dapat diperbaiki sebelum diajukan

**Acceptance Criteria:**
- [ ] Sistem memberikan laporan: ✅/⚠️/❌ per item
- [ ] Menyebutkan baris/bagian yang bermasalah
- [ ] Memberikan saran perbaikan konkret
- [ ] Hasil disimpan di 06_Audit_Review/

### US-03: Membuat LPU
**Sebagai** Sekretaris BEM  
**Saya ingin** membuat laporan berdasarkan proposal awal  
**Agar** pertanggungjawaban selesai dalam 1 hari setelah acara

**Acceptance Criteria:**
- [ ] LPU membandingkan rencana vs realisasi
- [ ] Anggaran realisasi vs anggaran rencana
- [ ] Dokumentasi foto (placeholder)
- [ ] Tanda tangan pejabat yang berwenang

### US-04: Persistensi Konteks
**Sebagai** pengguna sistem  
**Saya ingin** AI mengingat semua keputusan dan konteks  
**Agar** tidak perlu mengulang penjelasan di setiap sesi

**Acceptance Criteria:**
- [ ] Dashboard diupdate setiap selesai sesi
- [ ] Second Brain mencatat keputusan penting
- [ ] Graphify memvisualisasikan relasi antar dokumen

---

## 3. Spesifikasi Teknis

### Stack:
- **AI Engine:** Antigravity (Google DeepMind)
- **Second Brain:** Obsidian-compatible Markdown vault
- **Knowledge Graph:** Graphify (via `.graphifyignore`)
- **Scripting:** Python 3.12+ (PyMuPDF untuk PDF, docx untuk Word)
- **Format Output:** Markdown → dapat dikonversi ke Word/PDF

### Struktur Folder:
```
d:\Perkuliahan\LK FEB\
├── AGENTS.md                    ← Instruksi AI (auto-loaded)
├── 00_DASHBOARD_SECOND_BRAIN.md ← Kokpit utama
├── 00_PROMPT_MULAI_SESI.md      ← Template prompt sesi baru
├── 00_SISTEM_BEM/
│   ├── PRD_SEKRETARIS_BEM.md    ← File ini
│   ├── IMPLEMENTATION_PLAN.md   ← Rencana implementasi
│   └── CHANGELOG.md             ← Log perubahan sistem
├── 01_Proposal/
│   └── [NAMA_ACARA_TAHUN]/
│       ├── proposal_v1.md       ← Draft awal
│       ├── proposal_final.md    ← Versi final
│       └── proposal_final.docx  ← Export Word
├── 02_SPU/
│   └── [NAMA_ACARA_TAHUN]/
│       └── spu_[keterangan].md
├── 03_LPU/
│   └── [NAMA_ACARA_TAHUN]/
│       ├── lpu_draft.md
│       └── lpu_final.md
├── 04_Arsip_Acara/
│   └── [NAMA_ACARA_TAHUN]/      ← Semua dokumen acara selesai
├── 05_Referensi_Template/
│   ├── TEMPLATE_PROPOSAL.md
│   ├── TEMPLATE_SPU.md
│   ├── TEMPLATE_LPU.md
│   └── PKKMB_2026/              ← Referensi format terbaik
├── 06_Audit_Review/
│   └── [NAMA_ACARA]/audit_[tanggal].md
├── 07_Second_Brain/
│   ├── keputusan/               ← Log keputusan penting
│   ├── pembelajaran/            ← Apa yang dipelajari
│   └── konteks_acara/           ← Konteks per acara
├── directives/                  ← SOP
├── execution/                   ← Python scripts
├── graphify-out/                ← Knowledge graph
└── .agents/                     ← Skills & rules Antigravity
```

---

## 4. Non-Functional Requirements

- **Kecepatan:** Proposal draft selesai < 10 menit
- **Akurasi RAB:** Validasi otomatis, tidak ada ketidakseimbangan
- **Konsistensi:** Format sama di semua dokumen
- **Kemudahan:** Tidak perlu coding untuk menggunakan sistem
- **Ekstensibilitas:** Mudah menambah template acara baru

---

## 5. Out of Scope (Untuk Versi 1.0)

- Integrasi dengan Google Drive
- Notifikasi otomatis via WhatsApp/Email
- Sistem persetujuan digital (e-signature)
- Database mahasiswa anggota BEM
