# IMPLEMENTATION PLAN — Standar Tipografi, Margin & Typo
## BEM FEB UKRIDA

**Versi:** 1.0 | **Tanggal:** 28 September 2026  
**Status:** ✅ PRD & Directive Selesai | 🔵 Script Typo Checker Selesai

---

## Ringkasan

Sistem audit dokumen BEM FEB UKRIDA kini memiliki **2 lapis audit**:

```
LAPIS 1: Audit Struktur & Isi        → directives/04_audit_checklist.md
LAPIS 2: Audit Tipografi & Typo      → directives/05_audit_tipografi_typo.md
                                        execution/typo_checker.py (otomatis)
```

**Skor Gabungan:** Isi (60%) + Tipografi (40%) → min 8,5/10 untuk "SIAP SUBMIT"

---

## Fase 1: Komponen yang Sudah Dibuat ✅

| Komponen | File | Status |
|----------|------|--------|
| PRD Tipografi/Margin/Typo | `00_SISTEM_BEM/PRD_TIPOGRAFI_MARGIN_TYPO.md` | ✅ |
| Directive audit tipografi | `directives/05_audit_tipografi_typo.md` | ✅ |
| Script typo checker | `execution/typo_checker.py` | ✅ |
| Update audit checklist | `directives/04_audit_checklist.md` (referensi) | ✅ |

---

## Fase 2: Yang Perlu Dilakukan Secara Manual (Margin & Font) 🔵

Margin dan font **tidak bisa dicek otomatis dari Markdown** — harus dicek saat membuka file Word/Google Docs.

### Panduan Cek Margin di Google Docs:
1. Buka dokumen di Google Docs
2. Klik **File → Page Setup**
3. Cek: Top=2.54cm, Bottom=2.54cm, Left=3.0cm, Right=2.54cm
4. Jika salah → ubah di sana

### Panduan Cek Margin di Microsoft Word:
1. Klik **Layout (Page Layout) → Margins → Custom Margins**
2. Set: Top=2.5cm, Bottom=2.5cm, Left=3.0cm, Right=2.5cm
3. Apply to: Whole Document

### Panduan Cek Font di Google Docs/Word:
1. **Ctrl+A** (pilih semua teks)
2. Lihat font bar — jika menunjukkan "(Multiple)" → ada font berbeda-beda → harus diseragamkan
3. Set ke **Times New Roman, 12pt** untuk seluruh isi
4. Cover/judul: Times New Roman, 14pt, Bold

---

## Fase 3: Integrasi Script ke Workflow (Future) 🔮

| Task | Prioritas | Keterangan |
|------|-----------|------------|
| Jalankan `typo_checker.py` otomatis setelah generate proposal | Tinggi | Perlu integrasi di `audit_dokumen.py` |
| Export laporan audit ke .docx | Medium | python-docx |
| Cek margin dari file .docx | Rendah | python-docx bisa baca margin |

---

## Cara Menjalankan Audit Lengkap

### 1. Audit Typo Otomatis (via script):
```bash
cd "d:\Perkuliahan\LK FEB"
python execution/typo_checker.py --input "01_Proposal/NAMA_ACARA/proposal_draft.md"
```

### 2. Audit Struktur (manual/AI):
> Minta Antigravity: "Audit struktur proposal [nama file] menggunakan `directives/04_audit_checklist.md`"

### 3. Audit Tipografi (manual/AI):
> Minta Antigravity: "Audit tipografi proposal [nama file] menggunakan `directives/05_audit_tipografi_typo.md`"

### 4. Cek Margin & Font (manual di Word/Docs):
> Ikuti panduan di Fase 2 di atas

---

## Standar Referensi: PKKMB 2026

Berdasarkan analisis `07_Second_Brain/analisis_proposal_PKKMB_2026.md`:
- PKKMB 2026 memiliki **tipografi yang baik** dan konsisten
- Format Rp. konsisten dengan titik ribuan
- Nama gelar dosen ditulis lengkap
- Tidak ada typo nama/NIM yang ditemukan

**Ini yang harus dipertahankan di semua proposal berikutnya.**
