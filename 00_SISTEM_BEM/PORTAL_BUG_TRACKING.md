# 🐞 PORTAL LK-FEB — Bug Log Tracking System
**Pusat Pencatatan & Monitoring Issue Portal LK-FEB**

> [!IMPORTANT]
> **Batas Repositori Kanonis (18 November 2026):** Pelacakan bug aktif, bukti verifikasi rilis, dan gate peluncuran produksi (verifikasi pengiriman SMTP & human owner login/PKCE) kini berada di repositori terpisah **`portal-bem-feb-ukrida`** (`https://portal-lk-feb.vercel.app`). Dokumen ini menyimpan riwayat issue awal dari fase sprint di repositori `LK-FEB`.

---

## 📌 Status Workflow
```
[ Open ] ──► [ In Progress ] ──► [ Fixed ] ──► [ Verified & Closed ]
   ▲                                 │
   └────────── (Reopen) ─────────────┘
```

- **Open**: Issue dilaporkan (oleh @lk-drafter / tim) dan menunggu prioritas/alokasi
- **In Progress**: Sedang dikerjakan oleh developer/formatter/debugger
- **Fixed**: Perbaikan sudah selesai di branch pengembangan dan diajukan PR
- **Verified & Closed**: Telah diuji oleh @lk-auditor dan diverifikasi berjalan di production/main

---

## 📊 Summary Dashboard
- **Total Historical Issues (LK-FEB Sprint)**: 2
- **Open**: 0
- **In Progress**: 0
- **Fixed**: 0
- **Closed / Verified**: 2
- **Active Launch Gates (di repo `portal-bem-feb-ukrida`)**: Verifikasi pengiriman SMTP & human owner login/PKCE

---

## 📋 Active Bug & Issue Registry

| ID | Tanggal | Pelapor | Komponen | Deskripsi Singkat | Severity | Status | Assignee | Fix PR/Commit | Keterangan |
|---|---|---|---|---|---|---|---|---|---|
| BUG-001 | 2026-10-14 | @lk-orchestrator | Frontend (`LeftSidebar.tsx`) | Menu "Kalender Terpadu" mengarah ke `/kalender` (404) | High | Verified & Closed | @lk-frontend | `034c79b` | Diarahkan ke `/rundown`, lulus QA Round 2 |
| BUG-002 | 2026-10-14 | @lk-orchestrator | Frontend (`LeftSidebar.tsx`) | Menu "Admin Sync" mengarah ke `/admin-sync` (404) | High | Verified & Closed | @lk-frontend | `034c79b` | Diarahkan ke `/admin/sync`, lulus QA Round 2 |

*(Daftar issue akan diisi dan diperbarui secara berkala berdasarkan input temuan dari @lk-drafter dan hasil testing @lk-auditor)*

---

## 📝 Bug Details Log

### Template Pelaporan Bug Baru (Untuk @lk-drafter)
```markdown
### [BUG-XXX] Judul Masalah yang Jelas & Deskriptif
- **ID**: BUG-XXX
- **Tanggal Ditemukan**: YYYY-MM-DD
- **Pelapor**: @lk-drafter (atau nama anggota)
- **Komponen**: Frontend / Backend / Database / Script Generator / Integrasi
- **Severity**: Critical / High / Medium / Low
- **Status**: Open / In Progress / Fixed / Closed
- **Assignee**: @lk-formatter / @debugger / etc.
- **Link Commit / PR**: `[PR #XX / Commit hash](URL)`

#### 1. Gejala / Masalah
Jelaskan apa yang salah atau tidak sesuai spesifikasi.

#### 2. Langkah Mereproduksi (Steps to Reproduce)
1. Buka halaman/jalankan perintah...
2. Klik tombol atau masukkan input...
3. Perhatikan error yang muncul...

#### 3. Perilaku yang Diharapkan vs Aktual
- **Expected**: Data tersimpan rapi dan format 4-3-3-3 terjaga.
- **Actual**: Timbul error 500 / kolom bergeser.

#### 4. Catatan Perbaikan & Audit
- Catatan teknis solusi: ...
- Status audit (@lk-auditor): Pass / Fail
```

---

## 🔄 Riwayat Perbaikan (Resolved & Closed History)

| ID | Komponen | Tanggal Closed | Resolusi Singkat | PR / Commit | Verifikator |
|---|---|---|---|---|---|
| BUG-001 | `LeftSidebar.tsx` | 2026-10-14 | Perbaikan route `/kalender` → `/rundown` | `034c79b` | @lk-auditor (`06_Audit_Review/QA_VERIFICATION_ROUND_2_REPORT.md`) |
| BUG-002 | `LeftSidebar.tsx` | 2026-10-14 | Perbaikan route `/admin-sync` → `/admin/sync` | `034c79b` | @lk-auditor (`06_Audit_Review/QA_VERIFICATION_ROUND_2_REPORT.md`) |

---

*Log ini dikelola oleh @lk-arsiparis berkoordinasi dengan @lk-drafter, @lk-formatter, dan @lk-auditor.*
