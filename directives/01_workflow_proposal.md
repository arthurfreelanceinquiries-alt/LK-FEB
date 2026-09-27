# SOP: Workflow Pembuatan Proposal BEM FEB UKRIDA
## directive: 01_workflow_proposal

**Versi:** 1.0 | **Update Terakhir:** 28 Sep 2026

---

## Tujuan
Menghasilkan proposal kegiatan BEM FEB UKRIDA yang rapi, lengkap, dan siap diajukan dalam < 15 menit.

## Referensi Kerapihan
File referensi: `04_Arsip_Acara/PKKMB_2026/` — ini adalah standar gold untuk format.

---

## Input yang Dibutuhkan dari User

Sebelum generate, tanyakan (jika belum ada):

1. **Nama acara lengkap** (contoh: Pengenalan Kehidupan Kampus Mahasiswa Baru)
2. **Singkatan acara** (contoh: PKKMB)
3. **Tema** (nama tema + singkatan + kepanjangan + makna)
4. **Tanggal pelaksanaan** (hari, tanggal, bulan, tahun)
5. **Tempat** (gedung/ruang, kampus)
6. **Estimasi peserta** (jumlah, angkatan, prodi)
7. **Kepanitiaan** (nama + NIM semua posisi, atau minta user kirim daftarnya)
8. **Anggaran** (sumber dana + estimasi per divisi)
9. **Narasumber** (jika ada: nama, gelar, topik)
10. **Rundown** (detail acara per jam, atau minta user jelaskan alur)
11. **Kegiatan khusus** (games, workshop, dll + tujuan masing-masing)

---

## Alur Pengerjaan

```
1. Terima input dari user
   ↓
2. Validasi kelengkapan (cek semua 11 poin di atas)
   ↓
3. Hitung & validasi RAB:
   - Total per divisi
   - Grand total pengeluaran
   - Pastikan = total pemasukan (sisa = Rp 0)
   ↓
4. Generate draft menggunakan TEMPLATE_PROPOSAL.md
   ↓
5. Review otomatis dengan checklist di directives/04_audit_checklist.md
   ↓
6. Output ke 01_Proposal/[NAMA_ACARA_TAHUN]/proposal_draft.md
   ↓
7. Beritahu user dan minta feedback
   ↓
8. Revisi jika ada masukan
   ↓
9. Simpan final ke 01_Proposal/[NAMA_ACARA_TAHUN]/proposal_final.md
   ↓
10. Update 00_DASHBOARD_SECOND_BRAIN.md
```

---

## Validasi Wajib Sebelum Output

| Check | Cara Validasi |
|-------|--------------|
| Struktur BAB I-VI | Semua ada |
| Setiap tujuan minimal 5 poin | Hitung |
| RAB balance | Pemasukan - Pengeluaran = 0 |
| Kepanitiaan ada NIM | Cek setiap nama |
| Rundown ada durasi | Setiap baris ada kolom durasi |
| Format tanggal | "Jakarta, DD Bulan YYYY" |
| Tanda tangan minimal 2 | Ketupel + Ketua BEM |

---

## Edge Cases

- **Tidak ada narasumber:** Hapus bagian E (Narasumber) dari proposal
- **1 hari saja:** Hanya tampilkan rundown 1 hari
- **Ada sesi online:** Tambahkan rundown Online terpisah (seperti di PKKMB 2026)
- **Anggaran tidak balance:** STOP, notif user, minta revisi angka sebelum lanjut

---

## Output Format

```
01_Proposal/
└── [NAMA_ACARA]_[TAHUN]/
    ├── proposal_draft_v1.md     ← Draft awal
    ├── proposal_final.md        ← Final setelah revisi
    └── audit_[tanggal].md       ← Hasil audit otomatis
```
