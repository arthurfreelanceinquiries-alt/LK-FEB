# 📜 PORTAL LK-FEB — Project Changelog
**Dokumentasi Perjalanan Rilis & Milestone Portal LK-FEB**

Semua perubahan, penambahan fitur, perbaikan bug, dan migrasi arsitektur pada Portal LK-FEB dicatat secara kronologis dalam dokumen ini mengikuti prinsip semantic versioning dan roadmap fase proyek.

---

## 🗺️ Roadmap Fase Proyek

```
Phase 0: Initial MVP Build (Current)
   │
   ▼
Phase 1: UI/UX Redesign
   │
   ▼
Phase 2: Supabase Migration
   │
   ▼
Phase 3: Production Deployment
```

---

## 🚀 Phase 0: Initial MVP Build
- **Status**: 🟡 In Progress (Sedang Berjalan)
- **Target Periode**: Oktober 2026 – Desember 2026
- **Fokus Utama**: Fondasi sistem, ekstraksi script otomatisasi lokal, dan perancangan arsitektur.

### Milestone & Deliverables
- [x] Inisialisasi struktur berkas repositori `LK-FEB`
- [x] Pembuatan script otomasi dokumen lokal:
  - `docx_generator.py` (Standardisasi margin 4-3-3-3, Times New Roman, logo resmi)
  - `rab_validator.py` (Validasi balance pemasukan vs pengeluaran Rp. 0)
  - `typo_checker.py` (Audit tipografi dan deteksi typo otomatis)
- [x] Integrasi SOP & Checklist Audit:
  - `directives/01_workflow_proposal.md`
  - `directives/04_audit_checklist.md` (Lapis 1 - Struktur & Isi 60%)
  - `directives/05_audit_tipografi_typo.md` (Lapis 2 - Tipografi & Typo 40%)
- [x] Penyusunan dokumentasi teknis awal:
  - `00_SISTEM_BEM/PORTAL_LK_TECHNICAL.md`
  - `00_SISTEM_BEM/PORTAL_BUG_TRACKING.md`
  - `00_SISTEM_BEM/PORTAL_CHANGELOG.md`
  - `00_SISTEM_BEM/PORTAL_DATA_MAPPING.md`
- [ ] Prototype dashboard internal berbasis Markdown / Local Web

---

## 🎨 Phase 1: UI/UX Redesign
- **Status**: 🔴 Upcoming (Belum Dimulai)
- **Target Periode**: Januari 2027 – Februari 2027
- **Fokus Utama**: Perancangan antarmuka pengguna, navigasi ramah pengguna bagi pengurus BEM, dan visualisasi status terpusat.

### Milestone & Deliverables
- [ ] Penyusunan Design System BEM FEB (Palet warna resmi UKRIDA: Biru Navy & Kuning Keemasan, Aksen Neutral Gray)
- [ ] Pembuatan Wireframe & High-Fidelity Prototype (Figma)
- [ ] Redesign antarmuka portal:
  - Halaman Dashboard Organisasi & Status Proker
  - Form Generator Dokumen (Proposal / SPU / LPU) interaktif
  - Interface Audit Dokumen dengan visualisasi skor 2-lapis
  - Panel Database Anggota & Timeline Kalender
- [ ] Responsive design testing (Desktop & Tablet/Mobile)
- [ ] Review UI/UX bersama tim BPH BEM FEB

---

## 🗄️ Phase 2: Supabase Migration
- **Status**: 🔴 Planned (Direncanakan)
- **Target Periode**: Maret 2027 – April 2027
- **Fokus Utama**: Migrasi dari format flat spreadsheet (`bem_feb_data_master.xlsx`) dan local markdown ke relational database Supabase (PostgreSQL) berkeamanan tinggi.

### Milestone & Deliverables
- [ ] Setup Instance & Environment Supabase
- [ ] Eksekusi DDL Migration Schema:
  - Tabel `events`, `documents`, `members`, `timeline_tasks`, `finance`, `sponsors`, `audit_logs`
- [ ] Script Data Ingestion & Sanitasi Data:
  - Migrasi master data pengurus (NIM, nomor rekening, alamat, link foto)
  - Migrasi riwayat timeline proker & status kehadiran/keuangan
  - Migrasi target sponsor & media partner
- [ ] Konfigurasi Row Level Security (RLS) & Policies per role (BPH, Koor Divisi, Anggota, Auditor)
- [ ] Setup Supabase Storage Bucket untuk arsip PDF & DOCX proposal bertanda tangan
- [ ] Integrasi REST API / Supabase Client SDK ke modul otomasi Python

---

## 🌐 Phase 3: Production Deployment
- **Status**: 🔴 Planned (Direncanakan)
- **Target Periode**: Mei 2027
- **Fokus Utama**: Go-live ke domain universitas/organisasi, integrasi CI/CD, pengujian performa, dan pelatihan operasional pengurus.

### Milestone & Deliverables
- [ ] Setup Host Server / Cloud Platform (Vercel / Railway / Cloud VM)
- [ ] Konfigurasi Domain Resmi (`portal.bemfeb-ukrida.org` atau subdomain civitas)
- [ ] Penerapan SSL/TLS Certificates & Enkripsi HTTPS
- [ ] Implementasi Automated CI/CD Pipeline via GitHub Actions
- [ ] End-to-End Testing & Security Audit oleh @lk-auditor
- [ ] Penyusunan Buku Panduan Pengguna (User Manual) untuk Pengurus BEM
- [ ] Peluncuran Resmi (Official Launch) & Serah Terima Operasional

---

*Changelog ini dirawat oleh @lk-arsiparis sebagai bagian dari Second Brain BEM FEB UKRIDA.*
