# 🐞 PORTAL LK-FEB — Bug Log Tracking System
**Pusat Pencatatan & Monitoring Issue Portal LK-FEB**

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
- **Total Issues**: 0
- **Open**: 0
- **In Progress**: 0
- **Fixed**: 0
- **Closed**: 0

---

## 📋 Active Bug & Issue Registry

| ID | Tanggal | Pelapor | Komponen | Deskripsi Singkat | Severity | Status | Assignee | Fix PR/Commit | Keterangan |
|---|---|---|---|---|---|---|---|---|---|
| *Contoh: BUG-001* | *2026-10-14* | *@lk-drafter* | *Database/Supabase* | *Format NIM terpotong saat export* | *High* | *Open* | *@lk-formatter* | *-* | *Menunggu konfirmasi format teks* |

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
| - | - | - | Belum ada issue yang ditutup | - | - |

---

*Log ini dikelola oleh @lk-arsiparis berkoordinasi dengan @lk-drafter, @lk-formatter, dan @lk-auditor.*
