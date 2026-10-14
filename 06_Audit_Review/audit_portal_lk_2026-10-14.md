# 🔍 QA TEST CHECKLIST — PORTAL LK BEM FEB UKRIDA

**Tanggal Audit:** 14 Oktober 2026  
**Auditor:** @lk-auditor  
**Target:** Portal LK-FEB (`http://localhost:3000`)  
**Standar Kelulusan:** ≥ 8.5/10  

**Formula Skor Akhir:**
$$\text{Skor Akhir} = (\text{Skor Lapis 1} \times 0.6) + (\text{Skor Lapis 2} \times 0.4)$$

---

## 📐 AUDIT FRAMEWORK 2-LAPIS

### LAPIS 1: FUNGSIONAL & INTEGRITAS DATA (Bobot 60%)

#### 1.1 Autentikasi & Authorization (RBAC)
- [ ] **TC-AUTH-001:** Dev login `bph@dev.local` berhasil dan mendapat Tier 1 badge
- [ ] **TC-AUTH-002:** Dev login `fungsionaris@dev.local` berhasil dan mendapat Tier 2 badge
- [ ] **TC-AUTH-003:** Dev login `umum@dev.local` berhasil dan mendapat Tier 3 badge
- [ ] **TC-AUTH-004:** Logout berhasil dan redirect ke landing page
- [ ] **TC-AUTH-005:** Session persistence setelah refresh browser

#### 1.2 RBAC Access Control (Route Protection)
**Tier 3 (Mahasiswa Umum):**
- [ ] **TC-RBAC-001:** Akses `/` (home) berhasil
- [ ] **TC-RBAC-002:** Akses `/berita` berhasil
- [ ] **TC-RBAC-003:** Akses `/bulletin` berhasil
- [ ] **TC-RBAC-004:** Akses `/layanan-surat` berhasil
- [ ] **TC-RBAC-005:** Akses `/dashboard` dilarang (redirect ke `/`)
- [ ] **TC-RBAC-006:** Akses `/tugas` dilarang (redirect ke `/`)
- [ ] **TC-RBAC-007:** Akses `/anggota` dilarang (redirect ke `/`)
- [ ] **TC-RBAC-008:** Akses `/admin/sync` dilarang (redirect ke `/`)

**Tier 2 (Fungsionaris):**
- [ ] **TC-RBAC-009:** Akses `/dashboard` berhasil
- [ ] **TC-RBAC-010:** Akses `/tugas` (WBS) berhasil
- [ ] **TC-RBAC-011:** Akses `/rapat` berhasil
- [ ] **TC-RBAC-012:** Akses `/rundown` berhasil
- [ ] **TC-RBAC-013:** Akses `/pubdoc` berhasil
- [ ] **TC-RBAC-014:** Akses `/logistik` berhasil
- [ ] **TC-RBAC-015:** Akses `/anggota` dilarang (redirect)
- [ ] **TC-RBAC-016:** Akses `/kas` dilarang (redirect)
- [ ] **TC-RBAC-017:** Akses `/keuangan` dilarang (redirect)
- [ ] **TC-RBAC-018:** Akses `/admin/sync` dilarang (redirect)

**Tier 1 (BPH/Admin):**
- [ ] **TC-RBAC-019:** Akses `/anggota` berhasil
- [ ] **TC-RBAC-020:** Akses `/kas` berhasil
- [ ] **TC-RBAC-021:** Akses `/keuangan` berhasil
- [ ] **TC-RBAC-022:** Akses `/crm` berhasil
- [ ] **TC-RBAC-023:** Akses `/surat-maker` berhasil
- [ ] **TC-RBAC-024:** Akses `/proposal-maker` berhasil
- [ ] **TC-RBAC-025:** Akses `/admin/sync` berhasil

#### 1.3 Pengujian Modul Fungsional (17 Modul)
- [ ] **TC-MOD-001 - 005:** Modul WBS Timeline (`/tugas`) — 4 view mode & Auto-OffTrack
- [ ] **TC-MOD-006 - 010:** Modul Rapat & Presensi QR (`/rapat`) — SlotFinder & notulen
- [ ] **TC-MOD-011 - 014:** Modul Kas Pengurus (`/kas`) — Matriks 10 bulan & verifikasi BPH
- [ ] **TC-MOD-015 - 019:** Modul Keuangan RPK (`/keuangan`) — Balance RAB & approval transaksi
- [ ] **TC-MOD-020 - 022:** Modul Anggota (`/anggota`) — Pencarian alias nama & Org Chart
- [ ] **TC-MOD-023 - 027:** Modul Surat Maker (`/surat-maker`) — Penomoran Romawi & cetak A4
- [ ] **TC-MOD-028 - 034:** Modul Proposal Maker (`/proposal-maker`) — 5-Step wizard export MD/HTML
- [ ] **TC-MOD-035 - 039:** Modul Presensi Check-in (`/presensi/[token]`) — Denda telat 5 menit
- [ ] **TC-MOD-040 - 044:** Modul Admin Sync (`/admin/sync`) — Diagnostic audit data & export JSON

#### 1.4 Integritas Data
- [ ] **TC-DATA-001 - 003:** Anti-Float Rupiah (Integer only, pembulatan aman)
- [ ] **TC-DATA-004 - 005:** Format waktu ISO UTC di backend & WIB di tampilan
- [ ] **TC-DATA-006 - 008:** Format nomor surat resmi Romawi valid
- [ ] **TC-DATA-009 - 010:** RAB Balance (Total Pemasukan = Total Pengeluaran, Saldo Rp0)

---

## 🎨 LAPIS 2: TIPOGRAFI, UI/UX & MARGIN (Bobot 40%)

#### 2.1 Design Tokens & Palet UKRIDA
- [ ] **TC-UI-001 - 005:** Penggunaan warna baku Navy `#0B2A5B` & Yellow `#FDB913`
- [ ] **TC-UI-006 - 008:** Tipografi web konsisten & hierarki heading jelas
- [ ] **TC-UI-009 - 011:** Konsistensi border radius (`rounded-2xl`) & container width

#### 2.2 Responsivitas & Tampilan Layar
- [ ] **TC-RESP-001 - 005:** Adaptasi Mobile (375px), Tablet (768px), dan Desktop (1280px+)
- [ ] **TC-RESP-006 - 007:** Minimum ukuran tombol interaktif (min 44×44px)

#### 2.3 Validasi Form & Pesan Galat
- [ ] **TC-FORM-001 - 004:** Indikator wajib isi & pesan galat Bahasa Indonesia baku
- [ ] **TC-FORM-005 - 007:** Penanganan respon HTTP (403 Forbidden, 500 Server Error)

#### 2.4 Margin A4 & Pratinjau Dokumen
- [ ] **TC-MARGIN-001 - 003:** Tampilan A4Preview rasio proporsional & zoom control
- [ ] **TC-MARGIN-004 - 007:** Pengaturan `@page` print A4 portrait dengan margin rapi

#### 2.5 Aksesibilitas (WCAG 2.1 AA)
- [ ] **TC-A11Y-001 - 003:** Navigasi Keyboard & indikator fokus
- [ ] **TC-A11Y-004 - 009:** Kontras warna teks dan elemen UI

---

*Checklist resmi BEM FEB UKRIDA disimpan di `LK-FEB/06_Audit_Review/audit_portal_lk_2026-10-14.md`.*
