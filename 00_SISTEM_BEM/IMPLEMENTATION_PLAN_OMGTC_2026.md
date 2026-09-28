# 🚀 IMPLEMENTATION PLAN
## Transformasi & Pembuatan Proposal Resmi BEM FEB UKRIDA: OMGTC 2026

- **Dokumen Target:** `01_Proposal/OMGTC_2026/proposal_OMGTC_2026.md`
- **Basis Rujukan:** `00_SISTEM_BEM/PRD_PROPOSAL_OMGTC_2026.md` & `05_Referensi_Template/TEMPLATE_PROPOSAL.md`
- **Standar Format:** Mengadopsi standar emas Proposal PKKMB 2026 (`04_Arsip_Acara/PKKMB_2026/`)
- **Tanggal:** 28 September 2026

---

## 📅 Roadmap Tahapan Eksekusi

```
Phase 1: Analisis & PRD ──► Phase 2: Drafting Proposal ──► Phase 3: Validasi Tool
      [SELESAI]                    [SIAP EKSEKUSI]                [RAB & Typo]
                                                                        │
Phase 5: Finalisasi & Dashboard ◄── Phase 4: Audit Lapis 1 & 2 ◄────────┘
```

---

## 🛠️ Rincian Rencana Kerja (Task Breakdown)

### Phase 1: Ekstraksi, Analisis & Spesifikasi Teknis (✅ SELESAI)
- [x] Ekstraksi teks dari `01_Proposal/Proposal Kegiatan OMGTC - Ukrida.pdf` menggunakan `execution/pdf_extractor.py`.
- [x] Evaluasi gap format proposal vendor vs standar BEM FEB UKRIDA.
- [x] Sinkronisasi data historis kepanitiaan dan invoice sponsorship (Rp 3.000.000,-).
- [x] Penyusunan file `07_Second_Brain/analisis_proposal_OMGTC_2026.md`.
- [x] Penyusunan PRD di `00_SISTEM_BEM/PRD_PROPOSAL_OMGTC_2026.md`.

---

### Phase 2: Penyusunan Dokumen Proposal Lengkap (🔵 TAHAP BERIKUTNYA)
Menyusun naskah utuh `01_Proposal/OMGTC_2026/proposal_OMGTC_2026.md` dengan muatan:
1. **Halaman Cover Resmi:** Kop Surat BEM FEB UKRIDA, Logo Lengkap, Judul, Tema, dan Alamat Sekretariat.
2. **Bab I Latar Belakang:** 3 Paragraf terstruktur (Konteks digital era & gaya hidup visual mahasiswa -> Relevansi akademik FEB UKRIDA -> Inisiasi kolaborasi OMGTC).
3. **Bab II Tema Kegiatan:** *"CLEAR VISION, BRIGHT FUTURE: Edukasi Kesehatan Visual dan Pemeriksaan Refraksi Bersama Optik Melawai"*.
4. **Bab III Kegiatan:**
   - Sub-bab A: Tujuan Kegiatan (5 poin terukur).
   - Sub-bab B: Manfaat Kegiatan (3 poin nyata bagi mahasiswa & institusi).
   - Sub-bab C: Target Peserta (100 peserta seminar, 200+ pemeriksaan refraksi).
   - Sub-bab D: Pelaksanaan Kegiatan (Kamis - Jumat, 10 - 11 September 2026 di Junction, Parkiran, dan Auditorium Kampus 1).
   - Sub-bab E: Narasumber (Tenaga Ahli Optometri & Edukator Profesional Optik Melawai).
   - Sub-bab F: Susunan Acara / Rundown rinci 2 hari (menit per menit).
   - Sub-bab G: Teknis Sarana Prasarana (Booth 4x3m butuh 4.000W di Junction + Bus Mobile Optik 12m butuh 8.000W di Parkir).
5. **Bab IV Susunan Kepanitiaan:**
   - Pelindung: Dr. Diana Frederica, S.E., M.Ak. (Dekan FEB)
   - Penasehat: Dr. Daniel Widjaja, S.E., M.M. (Wakil Dekan FEB)
   - Ketua BEM FEB: Arthur Reezan (312023002)
   - Wakil Ketua BEM FEB: Princess Auralia Barus (322024025)
   - Ketua Pelaksana: Fellicia Florens
   - Sekretaris: Jessica Violant Nathaniel
   - Bendahara: Jemima Putri Sutanta
   - Divisi Acara, Perlengkapan, Pubdok, Humas & Sponsorship, Konsumsi.
6. **Bab V Rencana Anggaran Biaya (RAB):**
   - Total Pemasukan: Rp. 3.000.000,- (Sponsorship PT. Inti Citra Agung).
   - Pengeluaran: Rincian 5 divisi total Rp. 3.000.000,- (Sisa: Rp. 0).
7. **Bab VI Penutup:** Pernyataan formal komitmen kegiatan dan Lembar Pengesahan berjenjang 5 tanda tangan.

---

### Phase 3: Validasi Otomatis via Execution Scripts (🟡 TAHAP 3)
1. **Validasi RAB:**
   - Jalankan `execution/rab_validator.py` untuk menguji konsistensi penjumlahan dan memastikan Sisa = Rp. 0.
2. **Validasi Tipografi & Ejaan:**
   - Jalankan `execution/typo_checker.py` untuk mendeteksi salah ketik, format rupiah (`Rp. `), format tanggal (`Jakarta, ...`), dan keselarasan gaya bahasa formal.

---

### Phase 4: Audit Dokumen & Quality Assurance (🟡 TAHAP 4)
Melakukan audit formal dengan standar BEM FEB:
- **Lapis 1 (Bobot 60%):** Struktur Bab Romawi I-VI, kelengkapan kepanitiaan, keseimbangan RAB, dan kejelasan rundown (`directives/04_audit_checklist.md`).
- **Lapis 2 (Bobot 40%):** Standar margin, font, konsistensi istilah, dan PUEBI (`directives/05_audit_tipografi_typo.md`).
- Output laporan audit disimpan di: `06_Audit_Review/audit_proposal_OMGTC_2026.md`.

---

### Phase 5: Integrasi & Update Kokpit Second Brain (🟡 TAHAP 5)
1. Perbarui status acara di `00_DASHBOARD_SECOND_BRAIN.md`:
   - Memindahkan OMGTC 2026 dari pending ke status aktif/selesai.
2. Arsipkan dokumen asli mitra ke folder `04_Arsip_Acara/OPTIK_MELAWAI_2026/` agar folder kerja `01_Proposal/` bersih dan terorganisir.
3. Siapkan file untuk opsi konversi format docx jika dibutuhkan oleh Ketua BEM.

---

## ⏱️ Estimasi Waktu Pengerjaan

| Tahap | Aktivitas | Durasi | Status |
| :--- | :--- | :--- | :--- |
| **Tahap 1** | Ekstraksi PDF, Analisis Gap, Penyusunan PRD & Implementation Plan | 5 menit | ✅ Selesai |
| **Tahap 2** | Penulisan Naskah Proposal Lengkap Versi UKRIDA | 8 menit | 🔵 Siap Dikerjakan |
| **Tahap 3** | Validasi Script Python (RAB & Typo) | 2 menit | ⏳ Menunggu Tahap 2 |
| **Tahap 4** | Audit Review Lapis 1 & 2 | 3 menit | ⏳ Menunggu Tahap 3 |
| **Tahap 5** | Pemutakhiran Dashboard & Second Brain | 2 menit | ⏳ Menunggu Tahap 4 |
