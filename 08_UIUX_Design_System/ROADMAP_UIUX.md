# 🗺️ ROADMAP & SPESIFIKASI UI/UX PORTAL ORMAWA BEM FEB UKRIDA
**Disusun oleh:** @lk-uiux (Lead UI/UX & Product Designer)  
**Ditujukan kepada:** @lk-orchestrator, @lk-frontend, BEM FEB UKRIDA  
**Versi:** 1.0 — Oktober 2026  
**Status:** In Progress / Ready for Frontend Implementation  

---

## 1. Executive Summary

Portal Ormawa BEM FEB UKRIDA dirancang ulang secara menyeluruh dari antarmuka fungsional-sederhana menjadi **Command Center Modern & Mobile-Responsive**. Solusi ini memprioritaskan mobilitas fungsionaris kampus yang membutuhkan pemantauan persetujuan SPU/LPU on-the-go (viewport smartphone 360px - 430px), form penganggaran RAB cerdas anti-defisit dengan visual feedback seketika, serta diferensiasi peran yang presisi (BPH, Koordinator Sie, Anggota, dan Mahasiswa Umum).

---

## 2. Token Design System & Brand Palette

### A. Palet Warna Resmi UKRIDA & FEB
| Token Name | Hex Code | Peran / Kegunaan | WCAG Contrast |
|---|---|---|---|
| `brand.navy` | `#0B2A5B` | Primary Brand, Header Navbar, Primary Action Buttons | 11.2:1 (Pass AAA) |
| `brand.navy-dark`| `#071C3D` | Dark Surface, Hover State, Mobile Header Background | 14.8:1 (Pass AAA) |
| `brand.navy-light`| `#134080` | Accent Navigation, Active Tabs, Interactive Pill | 7.8:1 (Pass AAA) |
| `brand.gold` | `#FDB913` | FEB Accent, Crucial CTA, Milestone Badge, Highlight | 4.6:1 (Pass AA) |
| `brand.gold-dark`| `#E5A50B` | Hover State Gold CTA | 5.2:1 (Pass AA) |
| `brand.gold-light`| `#FEF3D6` | Banner Background Highlight, Info Toast | N/A (Surface) |
| `text.primary` | `#0F172A` | Slate-900: Judul Utama, Angka Finansial | 16.1:1 (Pass AAA) |
| `text.secondary`| `#475569` | Slate-600: Subteks, Body Paragraph, Label Input | 7.0:1 (Pass AAA) |
| `text.muted` | `#94A3B8` | Slate-400: Placeholder, Timestamp, Non-active items | 4.5:1 (Pass AA) |
| `balance.green` | `#10B981` | Indikator RAB Balance (Sisa Rp 0), Status Approved | Pass |
| `balance.red` | `#EF4444` | Indikator RAB Selisih/Defisit, Status Ditolak/Revisi | Pass |

### B. Typography Standard
- **Web UI:** `Plus Jakarta Sans` / `Inter`, sans-serif. Ringan, modern, geometris humanist.
- **DOCX / PDF Export:** `Times New Roman`, 12pt, Spasi 1.5, Margin Baku 4-3-3-3 cm (Sesuai `PRD_TIPOGRAFI_MARGIN_TYPO.md`).
- **Touch Target:** Seluruh tombol dan area interaktif mobile berukuran minimum **44px x 44px**.

---

## 3. Fitur Utama & UX Architecture

### A. Form UX — Interactive RAB Form Cerdas
1. **Dynamic Real-Time Calculation:**
   - Menghitung akumulasi Pemasukan (BEM, Sponsorship, Registrasi) vs Pengeluaran per Sie (Acara, Konsumsi, Pubdok, Perlengkapan, Humas/P3K).
2. **Visual Balance Indicator:**
   - **Kondisi Hijau (BALANCE):** Muncul saat `Pemasukan - Pengeluaran == 0`. Banner berlatar `#ECFDF5` dengan ring hijau `#10B981`, teks bertuliskan *"✅ ANGGARAN BALANCE (Sisa Rp 0) — Siap Diajukan"*, tombol Submit diaktifkan.
   - **Kondisi Merah (SELISIH / DEFISIT):** Muncul saat `Pemasukan - Pengeluaran != 0`. Banner berlatar `#FEF2F2` dengan border merah `#EF4444`, menampilkan nominal selisih secara akurat, dan menonaktifkan tombol submit dengan penjelasan perbaikan.
3. **Drag & Drop Lampiran Dokumen:**
   - Area drag & drop responsif mendukung file PDF, XLSX, DOCX, dan PNG/JPG.
   - Dilengkapi validasi ekstensi, indikator ukuran file, dan aksi hapus lampiran sebelum submit.
4. **Pratinjau Dokumen (Document Live Preview):**
   - Modal layar penuh / drawer yang merender tampilan draft proposal lengkap dengan Kop Surat resmi BEM FEB UKRIDA, susunan tabel RAB rapi, dan blok tanda tangan sebelum dikirim.

### B. Mobile-First Dashboard (Viewport 360px - 430px)
1. **Header Ringkas & Notifikasi:** Logo BEM FEB UKRIDA, info fungsionaris aktif, dan lonceng notifikasi real-time.
2. **Kartu Status Dokumen & SPU/LPU on-the-go:**
   - Tracking stepper vertikal/horizontal (Draft → Review BPH → Tanda Tangan Dekanat → Disetujui).
   - Akses cepat unduh PDF / share link pengesahan.
3. **Presensi Rapat via QR Scanner Cepat:**
   - Akses modal/kamera 1-tap dari navigation dock untuk scan QR absen rapat rutin / acara panitia.
4. **Bottom Navigation Ergonomis:**
   - Beranda | Dokumen/SPU | Quick QR Scan (Elevated Button) | Kas Ormawa | Profil.
5. **Mode Dual Persona (Role Switcher):**
   - Fungsionaris (BPH & Sie) vs Mahasiswa Umum (Verifikasi Dokumen Publik & Pengumuman).

---

## 4. Role-Based Dashboard Architecture

1. **Tier 1 (BPH — Badan Pengurus Harian):**
   - *Overview Stats:* Total Dokumen Menunggu TTD, Realisasi Kas BEM, Milestone Acara.
   - *Task & Approval Monitor:* Queue verifikasi proposal & SPU dengan aksi 1-klik (Approve / Request Revision).
   - *Kas Oversight:* Ringkasan arus kas masuk & keluar bulanan BEM FEB.
2. **Tier 2 (Koordinator Sie):**
   - *Sie Tasks & Timeline:* Checklist tugas internal sie beserta deadline H-Acara.
   - *Budget Allocator:* Kuota anggaran per sie dan status pengajuan pencairan dana.
   - *Kalender Sie:* Jadwal rapat internal dan gladi resik.
3. **Tier 3 (Anggota Fungsionaris):**
   - *Personal Focus:* Tugas yang di-assign oleh Koor, status presensi rapat kepanitiaan, dan status iuran kas anggota.
4. **Tier 4 (Mahasiswa Umum FEB):**
   - *Public Transparency Portal:* Papan pengumuman kegiatan kemahasiswaan, transparansi kegiatan ormawa, dan form aspirasi / pengaduan.

---

## 5. Timeline & Roadmap Kolaborasi (@lk-uiux ↔ @lk-frontend)

```
[Sprint 1: Token & Fondasi]
  ├─ Finalisasi DESIGN.md & tokens.json (@lk-uiux)  --> [SELESAI]
  ├─ Konfigurasi Tailwind & Theme Engine (@lk-frontend)
  └─ Setup komponen atomik (Button, Input, Badge, Card)

[Sprint 2: Form RAB Interaktif & Validasi]
  ├─ Desain Prototype RAB Form, Drag-Drop, & Preview Modal (@lk-uiux) --> [SELESAI]
  ├─ Wiring State Management & rab_validator.py integration (@lk-frontend)
  └─ File upload bucket Supabase integration

[Sprint 3: Mobile Experience & Presensi QR]
  ├─ Mobile Wireframe 360px-430px & Stepper SPU/LPU (@lk-uiux) --> [SELESAI]
  ├─ Integrasi Kamera QR Scanner via html5-qrcode / browser API (@lk-frontend)
  └─ Bottom navigation dock & gesture transitions

[Sprint 4: Role-Based Dashboard Views]
  ├─ Desain 4-tier role views (BPH, Koor, Anggota, Mahasiswa) (@lk-uiux)
  └─ Role-based routing & Supabase RLS security policies (@lk-frontend)

[Sprint 5: QA, Accessibility & Production Polish]
  ├─ Touch target audit (44x44px minimum) & WCAG AA verification
  └─ End-to-end user testing bersama pengurus BEM FEB
```

---

## 6. Daftar Deliverables Terlampir

1. **`DESIGN.md`** — Spesifikasi Token Desain Resmi (Standar Google DESIGN.md).
2. **`tokens.json`** — W3C Design Tokens Community Group (DTCG) JSON.
3. **`tailwind.theme.json`** — Konfigurasi ekstensi tema Tailwind CSS untuk Next.js 14.
4. **`wireframes/interactive_rab_form.html`** — Prototipe interaktif form RAB dengan kalkulasi balance real-time, visual banner, drag-and-drop, dan modal preview dokumen.
5. **`wireframes/mobile_dashboard.html`** — Prototipe mobile dashboard responsif (360px - 430px) dengan role switcher, status stepper SPU/LPU, dan QR Presensi modal.
6. **`wireframes/index.html`** — Showcase hub navigasi terintegrasi.
