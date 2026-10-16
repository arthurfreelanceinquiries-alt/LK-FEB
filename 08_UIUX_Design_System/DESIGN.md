---
version: alpha
name: Portal Ormawa BEM FEB UKRIDA Design System
description: Modern, professional, accessible, and mobile-first design system for BEM Faculty of Economics and Business UKRIDA.
colors:
  primary: "#0B2A5B"
  primary-dark: "#071C3D"
  primary-light: "#134080"
  secondary: "#FDB913"
  secondary-dark: "#E5A50B"
  secondary-light: "#FEF3D6"
  surface: "#FFFFFF"
  surface-subtle: "#F8FAFC"
  surface-muted: "#F1F5F9"
  text-primary: "#0F172A"
  text-secondary: "#475569"
  text-muted: "#94A3B8"
  text-inverse: "#FFFFFF"
  border-subtle: "#E2E8F0"
  border-strong: "#CBD5E1"
  success: "#10B981"
  success-surface: "#ECFDF5"
  success-border: "#A7F3D0"
  danger: "#EF4444"
  danger-surface: "#FEF2F2"
  danger-border: "#FECACA"
  warning: "#F59E0B"
  warning-surface: "#FFFBEB"
  warning-border: "#FDE68A"
  info: "#3B82F6"
  info-surface: "#EFF6FF"
  info-border: "#BFDBFE"
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans, sans-serif
    fontSize: 2rem
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.025em"
  display-md:
    fontFamily: Plus Jakarta Sans, sans-serif
    fontSize: 1.5rem
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "-0.02em"
  h1:
    fontFamily: Plus Jakarta Sans, sans-serif
    fontSize: 1.25rem
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "-0.015em"
  h2:
    fontFamily: Plus Jakarta Sans, sans-serif
    fontSize: 1.125rem
    fontWeight: 600
    lineHeight: 1.35
    letterSpacing: "-0.01em"
  h3:
    fontFamily: Plus Jakarta Sans, sans-serif
    fontSize: 1rem
    fontWeight: 600
    lineHeight: 1.4
  body-lg:
    fontFamily: Plus Jakarta Sans, sans-serif
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.5
  body-md:
    fontFamily: Plus Jakarta Sans, sans-serif
    fontSize: 0.875rem
    fontWeight: 400
    lineHeight: 1.5
  body-sm:
    fontFamily: Plus Jakarta Sans, sans-serif
    fontSize: 0.75rem
    fontWeight: 400
    lineHeight: 1.4
  caption:
    fontFamily: Plus Jakarta Sans, sans-serif
    fontSize: 0.6875rem
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "0.02em"
rounded:
  none: 0px
  xs: 4px
  sm: 6px
  md: 8px
  lg: 12px
  xl: 16px
  2xl: 20px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 20px
  2xl: 24px
  3xl: 32px
  4xl: 48px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.text-inverse}"
    rounded: "{rounded.lg}"
    padding: 12px 20px
    typography: "{typography.body-md}"
  button-primary-hover:
    backgroundColor: "{colors.primary-dark}"
    textColor: "{colors.text-inverse}"
  button-secondary:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.primary-dark}"
    rounded: "{rounded.lg}"
    padding: 12px 20px
    typography: "{typography.body-md}"
  button-secondary-hover:
    backgroundColor: "{colors.secondary-dark}"
    textColor: "{colors.primary-dark}"
  button-outline:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    rounded: "{rounded.lg}"
    padding: 12px 20px
  card-base:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.xl}"
    padding: 20px
  badge-success:
    backgroundColor: "{colors.success-surface}"
    textColor: "{colors.success}"
    rounded: "{rounded.full}"
    padding: 4px 10px
  badge-danger:
    backgroundColor: "{colors.danger-surface}"
    textColor: "{colors.danger}"
    rounded: "{rounded.full}"
    padding: 4px 10px
---

# Design System Portal Ormawa BEM FEB UKRIDA

## Overview

Design System ini disusun khusus sebagai fondasi antarmuka digital **Portal Ormawa BEM FEB UKRIDA**. Sistem ini mengawinkan wibawa akademis universitas dengan kelincahan operasional organisasi mahasiswa abad ke-21.

### Nilai Desain Utama:
1. **Academic Dignity & Fresh Energy:** Perpaduan Navy UKRIDA (#0B2A5B) yang stabil dan terpercaya dengan sentuhan Gold (#FDB913) FEB yang hangat, energik, dan optimis.
2. **Mobile First & On-the-Go Efficiency:** Dirancang presisi untuk pengurus dan mahasiswa yang sering mengakses persetujuan dokumen, presensi rapat via QR, dan cek saldo kas langsung dari ponsel (viewport 360px - 430px).
3. **Clarity & Zero Ambiguity (RAB Balance Guarantee):** Setiap data numerik, khususnya penganggaran (RAB), didukung visual indicator tegas (Hijau = Balance Rp 0, Merah = Selisih/Defisit) agar tidak ada kesalahan pengajuan ke Dekanat.
4. **Standardized & Deterministic:** Kode UI menggunakan token Tailwind yang konsisten tanpa hardcoded pixel acak, memudahkan kolaborasi erat dengan `@lk-frontend`.

---

## Colors

### Primary Palette (Identitas Resmi UKRIDA)
- **Primary Navy (`#0B2A5B`):** Warna institusional universitas, dipakai untuk top navbar, sidebar desktop, header card, dan aksi primer.
- **Primary Dark (`#071C3D`):** Varian navy gelap untuk status bar mobile, sidebar background, dan hover button primer.
- **Primary Light / Royal (`#134080`):** Aksen interaktif, badge terpilih, dan active tab.

### Accent Palette (Semangat FEB)
- **Gold Accent (`#FDB913`):** Warna kebanggaan Fakultas Ekonomi & Bisnis. Digunakan untuk CTA krusial, indikator milestone, badge peran BPH, dan aksen visual.
- **Gold Dark (`#E5A50B`):** Hover state tombol aksen gold.
- **Gold Light (`#FEF3D6`):** Latar belakang highlight kartu pengumuman atau info penting.

### Neutral & Semantic Palette
- **Pure Slate (`#0F172A`):** Teks judul dan label utama untuk kontras maksimal.
- **Body Slate (`#475569`):** Teks paragraf, deskripsi form, dan catatan.
- **Muted Slate (`#94A3B8`):** Placeholder input, helper text, dan tanggal sekunder.
- **Neutral Surface (`#F8FAFC` & `#FFFFFF`):** Latar belakang halaman yang bersih dan tidak melelahkan mata.
- **Border Subtle (`#E2E8F0`):** Pembatas kartu dan form input yang rapi.

### Status Indicators (Audit & Validasi)
- **Success / Balance (`#10B981`):** Latar `#ECFDF5`, Border `#A7F3D0`. Dipakai saat RAB Balance (Sisa Rp 0) dan Dokumen Disetujui.
- **Danger / Deficit (`#EF4444`):** Latar `#FEF2F2`, Border `#FECACA`. Dipakai saat RAB Defisit/Selisih dan Dokumen Ditolak/Revisi.
- **Warning / Review (`#F59E0B`):** Latar `#FFFBEB`, Border `#FDE68A`. Menandakan dokumen menunggu review BPH / Dekan.
- **Info / Draft (`#3B82F6`):** Latar `#EFF6FF`, Border `#BFDBFE`. Menandakan draft baru disimpan.

---

## Typography

### Web UI Font Stack
- **Primary Web Font:** `Plus Jakarta Sans`, `Inter`, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif.
- **Karakter:** Sans-serif modern, geometric yet humanist, sangat tajam di layar Retina maupun budget Android (360px).
- **Aturan Tipografi Web:** Tidak menggunakan serif pada antarmuka web dashboard agar ergonomis dan modern.

### Formal Document Export (DOCX/PDF)
- **Formal Print Font:** `Times New Roman` (12pt, spasi 1.5, margin 4-3-3-3 cm) sesuai standar baku PRD Tipografi BEM FEB UKRIDA.

### Type Scale (Rem & Px):
- `display-lg`: 32px (2rem) / Bold / leading 1.2 — Headline Hero / Landing
- `display-md`: 24px (1.5rem) / Bold / leading 1.25 — Judul Halaman Dashboard
- `h1`: 20px (1.25rem) / SemiBold / leading 1.3 — Judul Modul / Card Header
- `h2`: 18px (1.125rem) / SemiBold / leading 1.35 — Sub-bagian Form
- `h3`: 16px (1rem) / SemiBold / leading 1.4 — Label Field & Card Title
- `body-lg`: 16px (1rem) / Regular / leading 1.5 — Teks konten utama
- `body-md`: 14px (0.875rem) / Regular / leading 1.5 — Default tabel & input form
- `body-sm`: 12px (0.75rem) / Regular / leading 1.4 — Meta timestamp, tag
- `caption`: 11px (0.6875rem) / SemiBold uppercase — Kategori & badge counter

---

## Layout

### Responsive Breakpoints
- **Mobile Small (360px - 389px):** Target minimum (e.g. Galaxy A series, compact phones). 1 kolom, full width cards, padding horizontal 16px (`px-4`).
- **Mobile Large (390px - 430px):** Target iPhone 13/14/15/Pro Max & modern Android. Padding horizontal 16px-20px.
- **Tablet (768px - 1023px):** 2 kolom grid, collapsible sidebar navigation.
- **Desktop (1024px+):** Fixed sidebar (260px), multi-column layout (stats 4-grid, table responsive).

### Touch Ergonomics & Accessibility
- **Target Sentuh Minimum:** 44px x 44px untuk seluruh tombol, link navigasi, dan icon trigger.
- **Thumb Zone Navigation:** Tombol aksi utama (Scan QR Presensi, Submit Dokumen) ditempatkan di 60% area bawah layar pada perangkat mobile.
- **Bottom Navigation Bar:** 5 menu utama di mobile (`Beranda`, `SPU/LPU`, `Scan QR`, `Kas`, `Profil`) dengan safe-area padding untuk notch/home indicator.

---

## Elevation & Depth

- **Level 0 (Flat):** Background halaman (`#F8FAFC`).
- **Level 1 (Card Default):** `0 1px 3px 0 rgba(15, 23, 42, 0.05), 0 1px 2px -1px rgba(15, 23, 42, 0.05)` dengan border `1px solid #E2E8F0`.
- **Level 2 (Dropdown & Hover Card):** `0 4px 6px -1px rgba(15, 23, 42, 0.08), 0 2px 4px -2px rgba(15, 23, 42, 0.06)`.
- **Level 3 (Modal Dialog & Bottom Sheet):** `0 20px 25px -5px rgba(15, 23, 42, 0.15), 0 8px 10px -6px rgba(15, 23, 42, 0.1)`.

---

## Shapes

- **Badges & Tags:** `rounded-full` (Pill shape) untuk kesan dinamis.
- **Buttons & Form Inputs:** `rounded-lg` (8px) untuk konsistensi form modern.
- **Cards & Modals:** `rounded-xl` (12px) hingga `rounded-2xl` (16px) untuk frame kontainer elegan.
- **Avatar:** `rounded-full` dengan border putih 2px dan ring Navy.

---

## Components

### 1. Interactive RAB Form Component
- **Pemasukan Section:** Multi-row sumber dana (BEM, Sponsorship, Kontribusi Peserta).
- **Pengeluaran Section:** Dikelompokkan per Divisi (Acara, Konsumsi, Pubdok, Perlengkapan, Humas & P3K).
- **Live Visual Balance Banner:**
  - *Kondisi Hijau:* Sisa = Rp 0 -> Muncul banner emerald bertuliskan `"✅ ANGGARAN BALANCE (Sisa Rp 0)"` dan tombol submit aktif.
  - *Kondisi Merah:* Sisa != Rp 0 -> Muncul banner rose bertuliskan `"❌ ANGGARAN BELUM BALANCE (Selisih: Rp X)"` dan tombol submit terkunci dengan tooltips.
- **Drag-and-Drop Lampiran:** Dropzone interaktif dengan feedback visual hover, indikator ukuran file, dan list lampiran yang bisa dihapus.
- **Preview Modal:** Tombol "Preview Dokumen" membuka modal pratinjau format baku sebelum data dikirim ke Supabase / reviewer.

### 2. Mobile Document Approval Card
- Header: Nomor surat, Jenis (SPU / Proposal / LPU), Nama Acara.
- Stepper Progress Bar: 4 titik alur (Pengajuan -> Verifikasi BPH -> Review Dekanat -> Approved).
- Action Trigger: Tombol "Lihat Detail" & "Unduh PDF Resmi".

### 3. Presensi & QR Scanner
- Tombol aksi mengambang (Floating Action Button) atau menu tengah Bottom Bar untuk membuka kamera QR Scanner dalam 1 detik.
- Konfirmasi instan haptic/suara ringan dan badge sukses hijau.

---

## Do's and Don'ts

### Do's:
- ✅ Gunakan Navy `#0B2A5B` sebagai jangkar warna utama dan Gold `#FDB913` sebagai aksen aksi prioritas tinggi.
- ✅ Pastikan setiap field angka uang memiliki auto-formatter `Rp. xx.xxx.xxx`.
- ✅ Selalu sediakan status visual ganda (ikon + warna + teks) agar ramah penderita buta warna (WCAG AA).
- ✅ Uji setiap tampilan pada viewport sempit (360px) tanpa ada horizontal scrolling yang tidak diinginkan.

### Don'ts:
- ❌ Jangan menggunakan font Serif (Times New Roman) untuk UI aplikasi web; gunakan font sans-serif modern.
- ❌ Jangan biarkan user submit proposal jika RAB belum balance (Sisa != Rp 0).
- ❌ Jangan gunakan target sentuh di bawah 44px pada layar smartphone.
- ❌ Jangan gunakan warna merah murni `#FF0000` atau kuning menyilaukan; gunakan semantic palette yang telah dikalibrasi kontrasnya.
