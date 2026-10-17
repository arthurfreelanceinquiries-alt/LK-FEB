# HASIL AUDIT 2-LAPIS — Referensi Template & Arsip Acuan BEM FEB UKRIDA
**Tanggal Audit:** 2026-10-16
**Auditor:** lk-auditor (Lead Quality Auditor BEM FEB UKRIDA)
**Mandat dari:** lk-orchestrator / Meta Orchestrator
**Lokasi workspace:** D:/Perkuliahan/LK FEB
**Formula:** Skor Akhir = (Skor Lapis 1 x 0.6) + (Skor Lapis 2 x 0.4)
**Ambang:** >=8.5 SIAP SUBMIT | 7.0-8.4 PERLU REVISI MINOR | <7.0 PERLU REVISI MAYOR (Dilarang diajukan ke pimpinan)

## Acuan normatif yang dipakai
- directives/04_audit_checklist.md v1.1 (Lapis 1)
- directives/05_audit_tipografi_typo.md v1.0 (Lapis 2)
- 00_SISTEM_BEM/PRD_TIPOGRAFI_MARGIN_TYPO.md v1.0
- execution/typo_checker.py (dijalankan real via python -X utf8)
- execution/rab_validator.py (diinspeksi source; validasi aritmetika manual karena tidak ada file rab.json + eksekusi python -c diblokir policy single-query — TIDAK difabrikasi)
- execution/pdf_extractor.py GAGAL dijalankan (ModuleNotFoundError: No module named 'fitz' pada python 3.11.15 sistem; venv Optik hanya punya openpyxl/pillow/python-docx). Sebagai alternatif dipakai ekstraksi teks via read_file (terbukti bisa membaca PDF). Ini dilaporkan apa adanya.

## KONFLIK STANDAR KRITIS (wajib diputuskan pimpinan)
1. **Margin bertentangan:**
   - Instruksi mandat + Panduan_Birokrasi_LKMM_II.md + SOP SEBELUM PROPOSAL DIBUAT: **4-3-3-3 (Kiri 4.0, Atas 3.0, Kanan 3.0, Bawah 3.0, A4)** — binding kiri.
   - directives/05_audit_tipografi_typo.md + PRD_TIPOGRAFI_MARGIN_TYPO.md: **Atas 2.5, Bawah 2.5, Kiri 3.0, Kanan 2.5**.
   - Audit ini memakai **4-3-3-3 sebagai acuan kelulusan** sesuai mandat Meta Orchestrator, dan memflag directive 05/PRD sebagai PERLU REVISI agar diselaraskan. Untuk file .md murni, margin dinilai N/A sesuai catatan directive 05.
2. **Format Rupiah bertentangan:**
   - Baku mandat + 04 + 05: `Rp. X.XXX.XXX` (titik setelah Rp, spasi, titik ribuan).
   - Panduan_Birokrasi_LKMM_II.md baris 347 mengajarkan: pilih `Rp100.000` atau `Rp 100.000` (keduanya SALAH menurut baku). Ini sumber utama kesalahan massal di arsip LKMM II. Wajib dikoreksi panduannya.
3. **Penomoran Bab bertentangan:**
   - 04_audit_checklist: BAB I..VI Romawi, Sub A,B,C, Sub-sub 1,2,3.
   - Panduan/SOP LKMM II: BAB I..VI Romawi, subbab 1,2,3 Arab (contoh: di bawah BAB III pakai 1. Tujuan, 2. Sasaran...).
   - Arsip LKMM II memakai angka Arab untuk BAB (`1. LATAR BELAKANG`, `2. TEMA...`) — triple deviasi. Wajib harmonisasi: tetapkan satu (rekomendasi: ikut 04 — Romawi + Huruf + Angka).

---

## RINGKASAN EKSEKUTIF — Skor Akhir

| No | Dokumen | Lapis 1 (60%) | Lapis 2 (40%) | Skor Akhir | Status |
|----|---------|---------------|---------------|------------|--------|
| 1 | 05_Referensi_Template/TEMPLATE_PROPOSAL.md | 9.2 | 10.0 (tool) | **9.52** | SIAP SUBMIT (sebagai template, bersihkan petunjuk) |
| 2 | 05_Referensi_Template/TEMPLATE_SPU.md | 8.8 | 9.7 (tool, 1 warning) | **9.16** | SIAP SUBMIT setelah 1-line fix |
| 3 | 05_Referensi_Template/TEMPLATE_LPU.md | 9.0 | 10.0 (tool) | **9.40** | SIAP SUBMIT (sebagai template) |
| 4 | PKKMB_2026/Proposal Revisi 12 Agustuts 2026.pdf | 8.7 | 6.5 (human; tool tidak dijalankan untuk PDF karena fitz hilang) | **7.82** | PERLU REVISI MINOR (batas atas; jangan jadi gold tanpa errata) |
| 5 | PKKMB_2026/SPU samples (4 surat) | 6.0-6.5 | ~7.0 | **~6.4-6.7** | PERLU REVISI MAYOR — jangan ditiru mentah |
| 6 | LKMM_II_2026/PROPOSAL LKMM TINGKAT II 2026.md | 6.8 | 0.0 (tool, 29 error) | **4.08** | PERLU REVISI MAYOR — DILARANG jadi acuan |
| 7 | LKMM_II_2026/Format Proposal Peserta LKMM2.md | 7.0 | 3.0 (tool, 7 error) | **5.40** | PERLU REVISI MAYOR |
| 8 | LKMM_II_2026/Format LPJ Peserta LKMM2.md | 7.5 | 8.0 (tool, 2 error) | **7.70** | PERLU REVISI MINOR |
| 9 | LKMM_II_2026/Panduan_Birokrasi_LKMM_II.md (SOP) | N/A (bukan proposal) | 4.7 (tool, 5 error +1 warning) | **4.7 setara** | PERLU REVISI MAYOR (konten Rupiah salah) |
| 10 | LKMM_II_2026/Template_Proposal_LK_FEB.md | 7.5 | 10.0 (tool) | **8.50** | Batas SIAP SUBMIT/MINOR — tapi deviasi struktur, wajib harmonisasi |
| 11 | OPTIK_MELAWAI_2026/SPU Dokumentasi 017 | 6.5 | ~7.0 | **~6.70** | PERLU REVISI MAYOR |
| 12 | OPTIK_MELAWAI_2026/Invoice (xlsx/docx/pdf/html) | N/A | 5.0 | **5.0 setara** | PERLU REVISI MAYOR — bukan acuan proposal |

Catatan: skor Lapis 2 untuk .md adalah skor tool typo_checker (penalti 1.0/error, 0.3/warning). Skor Lapis 1 adalah penilaian manual checklist 04 (cover, bab Romawi, rundown, kepanitiaan+NIM, RAB, TTD). Detail per dokumen di bawah.

---

## OUTPUT TOOL REAL (bukan karangan)

- `TEMPLATE_PROPOSAL.md`: 220 baris, 0 error, 0 warning, Skor 10.0/10 LOLOS.
- `TEMPLATE_SPU.md`: 53 baris, 0 error, 1 warning, Skor 9.7/10. Warning Baris 7: `BEM-FEB-UKRIDA` seharusnya `FEB UKRIDA`.
- `TEMPLATE_LPU.md`: 146 baris, 0 error, 0 warning, Skor 10.0/10.
- `Format LPJ Peserta`: 250 baris, 2 error, 0 warning, Skor 8.0. Baris 234: `ketupel` + `Ketupel` (duplikat case-insensitive — bug tool, seharusnya 1 temuan).
- `Format Proposal Peserta`: 160 baris, 7 error, Skor 3.0. Baris 101,102,103,108,109,114,115: `Rp 900.000` dkk (tanpa titik setelah Rp).
- `Panduan_Birokrasi`: 438 baris, 5 error +1 warning, Skor 4.7. Baris 335,347,349 pola Rupiah salah; Baris 251 `BEM UKRIDA` seharusnya `BEM FEB UKRIDA`.
- `PROPOSAL LKMM II`: 193 baris, 29 error, Skor 0.0. Rincian: Baris 70-71 ketupel (4 temuan duplikat), Baris 134-176 ~25 temuan Rupiah (`Rp2.317.000`, `Rp25.000`, `Rp 5.000`, `Rp0`).
- `Template_Proposal_LK_FEB.md`: 280 baris, 0 error, 0 warning, Skor 10.0.

RAB aritmetika manual (terverifikasi penjumlahan, bukan output rab_validator.py):
- PKKMB: Pemasukan 2.700.000 + 8.010.000 = 10.710.000. Pengeluaran 2.525.000+6.615.000+480.000+220.000+870.000 = 10.710.000. Sisa 0. BALANCE PASS. Format FAIL (lihat temuan).
- LKMM II: Pemasukan 2.317.000. Pengeluaran 115.000+1.702.000+400.000+100.000 = 2.317.000. Sisa 0. BALANCE PASS. Format FAIL total.

---

## TEMUAN DEFISIENSI PER DOKUMEN

### A. TEMPLATE_PROPOSAL.md — 9.52 SIAP SUBMIT
Lapis 1 (9.2):
- ✅ Cover lengkap: judul KAPITAL, BADAN EKSEKUTIF MAHASISWA, FAKULTAS EKONOMI & BISNIS UKRIDA, PERIODE 2026, Jl. Tanjung Duren Raya no.4, Telp/Fax.
- ✅ Struktur I-VI + sub A-G (Tujuan 5 template, Manfaat 3, Target, Pelaksanaan tabel Hari/Tanggal/Tempat, Narasumber opsional, Rundown 3 kolom Waktu|Durasi(menit)|Kegiatan + Evaluasi penutup, Games opsional).
- ✅ Kepanitiaan: Pelindung, Penasehat, Ketua BEM+NIM baku, Waketum+NIM baku, Pengawas, Ketupel, Waka, Sekretaris, Bendahara, 5 Koordinator+Anggota. Minus: NIM masih placeholder [NIM] (wajar untuk template, tapi harus ada instruksi validasi 9 digit).
- ⚠️ TTD: hanya `[Jabatan][Nama]` dengan &nbsp; sejajar, TIDAK memakai `<u>Nama</u>` bold+underline sesuai syarat Lapis 1. Gelar Dekan placeholder. Wajib contoh baku.
- ⚠️ Ada `---` ganda baris 9-10 dan `#` ganda — minor markdown.
Lapis 2 (10.0): ✅ Rupiah placeholder sudah baku `Rp. [x]`, tanggal placeholder `Jakarta, [tanggal]` + contoh benar, penomoran Romawi/Huruf/Angka benar. Margin/Font N/A untuk .md.
Rekomendasi: tambah contoh TTD baku dengan `<u>`, tambah catatan hapus petunjuk, tambah validasi NIM 9 digit.

### B. TEMPLATE_SPU.md — 9.16 SIAP SUBMIT setelah fix
Lapis 1 (8.8):
- ✅ Nomor, tanggal, Kepada Yth, detail Hari/Tanggal/Waktu/Tempat tabel, keterangan permohonan, Hormat kami BEM FEB, Ketupel + Arthur Reezan (312023002), Mengetahui Dekan gelar lengkap.
- ⚠️ TTD tidak pakai `<u>`, NIM Ketupel placeholder ([NIM]).
- ⚠️ Tidak ada kop/logo instruksi (untuk SPU resmi perlu kop).
Lapis 2 (9.7): ❌ Baris 7 `BEM-FEB-UKRIDA` kena warning FEB-UKRIDA. Harus `BEM FEB UKRIDA` (spasi). Selebihnya bersih.
Fix 1 baris: `No: [No]/[Kode]/BEM-FEB-UKRIDA/[Bln-Romawi]/2026` → `No: [No]/[Kode]/BEM FEB UKRIDA/[Bln-Romawi]/2026`.

### C. TEMPLATE_LPU.md — 9.40 SIAP SUBMIT
Lapis 1 (9.0):
- ✅ Rencana vs Realisasi (waktu, peserta), rundown + Ket ✅/⚠️, evaluasi baik+kendala+solusi+saran, keuangan anggaran vs realisasi per divisi, rekap, sisa + keterangan, TTD.
- ⚠️ BAB IV Kepanitiaan hanya `[Salin dari proposal]` — perlu instruksi tambah catatan perubahan.
- ⚠️ TTD sama: tanpa `<u>`.
Lapis 2 (10.0): bersih.

### D. PKKMB Proposal Revisi — 7.82 REVISI MINOR (hampir mayor)
Lapis 1 (8.7):
- ✅ Struktur I-VI lengkap, Tujuan 5, Manfaat 3, Target (maba 2026 + 2023-2025 belum PKKMB), Pelaksanaan Kamis-Jumat 13-14 Agt 2026 Kampus 1, Narasumber 3, Rundown 3 sesi (Day1/Day2/Online) kolom Waktu|Durasi|Kegiatan, Games 5 dengan alat & tujuan, Kepanitiaan lengkap + NIM, Anggaran pemasukan+5 divisi+rekap+sisa, Penutup Jakarta 25 Juli 2026 + 5 TTD + Mengetahui Dekan + Menyetujui WR III.
- ❌ Cover baris 3: `FAKULTAS EKONOMI BISNIS UKRIDA` — hilang `&`/`dan`. Kritis organisasi.
- ❌ Dual NIM Juan Louis: Bendahara (322025002) vs Anggota Perlengkapan (322025003). Satu orang dua NIM — verifikasi.
- ⚠️ `Jessy` (Anggota Humas 322024030) nama tidak lengkap; `A Una` vs `Una` tidak konsisten; Koordinator Humas rangkap Sekretaris (Rachel) — perlu justifikasi.
- ⚠️ TTD pengesahan: hanya Dekan + WR III pakai `<u>`; jajaran BEM/BPM/pelaksana tanpa underline, tanpa NIM, layout collapsed di ekstraksi.
Lapis 2 (6.5):
- ❌ Rupiah: `Rp.10.710.000` (tanpa spasi), `RP.2.525.000` (kapital), `Rp200.000`, `Rp500.000`, `Rp185.000`, `Rp0`/`Rp 0` campur. Baku: `Rp. 10.710.000` dst.
- ❌ `Ketupel` di rundown 08:55-09:00 (informal).
- ❌ `Ukrida` vs `UKRIDA` campur; `FAKULTAS EKONOMI BISNIS` (lihat atas).
- ⚠️ Artefak ekstraksi `tidakpernahluputdari...` — kemungkinan spasi hilang saat export Google Docs→PDF; perlu cek file .docx asli sebelum vonis. Filename `Agustuts` typo (seharusnya Agustus).
- ✅ Tanggal `Jakarta, 25 Juli 2026` benar. RAB balance PASS (10.710.000=10.710.000 sisa 0).
Keputusan: boleh jadi referensi isi/RAB, TAPI wajib errata 1 halaman sebelum dijadikan gold.

### E. PKKMB SPU samples — ~6.4-6.7 MAYOR
Contoh: Parents Gathering 016, Akses Data 005, Wali 015, Parkir 011, Optik 017 (pola sama):
- ❌ Nomor `UKKW` vs `UKRIDA` tidak konsisten (005,011,015,016,017 semua UKKW). Baku template: `BEM-FEB-UKRIDA` (itu pun salah strip). Putuskan satu: `BEM FEB UKRIDA`.
- ❌ Typo konten: `Akutansi` → `Akuntansi` (005,015), `kegaitan` → `kegiatan` (005,015), `No : ... Hal : ...` sebaris (harus 2 baris), `08 September` leading zero (baku `8 September`/`13 Agustus` tanpa nol depan).
- ❌ Logika: 005 minta data `Manajemen dan Akutansi` tapi untuk `Program Studi Sistem Informasi` — mismatch. 015 Parents Gathering diselenggarakan `Fakultas` (bukan BEM?) tapi pemohon BEM — klarifikasi. Parents Gathering tanggal `Jumat, 13 Maret 2026` di surat Agustus — kronologi aneh.
- ❌ TTD: `Arthur ReezanRachel Angelina Tjahj` collapsed tanpa spasi, `Tjahj` hilang `a`, tanpa NIM, tanpa `<u>`. Mengetahui: `Wakil Dekan I Fakultas...` tapi nama Dekan (Dr. Diana...) — jabatan vs nama mismatch. Parkir 011: `Wakil)aekan` (kemungkinan artefak, tapi wajib cek asli).
- ❌ Optik 017 tabel: header `Hari Pertama|Hari Kedua|Hari Kedua` duplikat; seharusnya Hari Pertama/Kedua/Seminar. Tanpa `Mengetahui Dekan` sama sekali.
Jangan jadikan acuan SPU sebelum ada 1 contoh SPU gold yang benar.

### F. LKMM II PROPOSAL — 4.08 MAYOR (Dilarang diajukan)
Lapis 1 (6.8):
- ❌ Penomoran BAB pakai Arab `1. LATAR... 2. TEMA...` bukan Romawi `I. II.`. Subbab juga Arab `1. TUJUAN 2. SASARAN...` bukan A,B,C.
- ❌ Tujuan hanya 1 paragraf naratif, bukan min 3 poin operasional (Meningkatkan/Melatih...). Manfaat tidak ada (diganti Sasaran/Bentuk — deviasi dari 04).
- ⚠️ Rundown 5 kolom (Waktu|?|Kegiatan|Keterangan|kosong) + kolom PIC internal (`Perkap: ... PIC: ... PHD: ... denda 5K`) — seharusnya proposal hanya Waktu|Durasi|Kegiatan (+Keterangan umum opsional). PIC internal pindah ke dokumen internal.
- ⚠️ Waktu `06.30 - 16.30`, `16.20-16.30` pakai titik (baku `06:30`, `16:20-16:30`).
- ❌ Kepanitiaan: tanpa Wakil Ketua Pelaksana; tanpa Pengawas ganda?; `Anggota Humas: Monica...` di bawah Koordinator Konsumsi (salah label, harusnya Anggota Konsumsi); `Joey Joseph (322025039)` vs `Jericco Wijaya (322025039)`? — cek duplikat NIM di file (Koordinator Perlengkapan Joseph vs Anggota Joey? aktual baris 111-112 rancu).
- ❌ Penutup TTD: `Ketua BEM U` terpotong, `Witono Ng Septiawan` terbelah, tanpa NIM, Dekan `Dr. Diana Frederica, S.E...` koma setelah Frederica (baku tanpa koma: `Dr. Diana Frederica S.E...`).
- ✅ RAB balance PASS (2.317.000=2.317.000 sisa 0) — satu-satunya nilai plus.
Lapis 2 (0.0 tool): 25+ temuan Rupiah semua salah (`Rp2.317.000`, `Rp25.000`, `Rp115.000`, `Rp0`), 4 temuan ketupel. Bahkan jika koreksi duplikat tool, skor human ~3-4 — tetap MAYOR.

### G. Format Proposal/LPJ Peserta + Panduan + Template LK FEB
- Format Proposal Peserta (5.40 MAYOR): contoh anggaran `Rp 900.000`, `Rp 500.000`, `Rp 1.400.000` semua tanpa titik setelah Rp; rekap `Rp xxx` placeholder; `MISS Elita...` kapital tidak baku; `Ketua BEM U` terpotong.
- Format LPJ Peserta (7.70 MINOR): struktur LPJ bagus (Tujuan, Sasaran, Jadwal, Tema, Narasumber, Rundown Real Time, Pencapaian, Tantangan, Evaluasi Penghambat/Pendukung, RTL, Realisasi Anggaran, Dokumentasi, Penutup, Laporan SPU/LPU). Minus: Realisasi Anggaran masih `xxxx,-` (baku `Rp. X`), `16.20-16.30` titik, `ketupel` baris 234, `Jakarta, ………. 2026` placeholder, TTD tanpa NIM.
- Panduan_Birokrasi (4.7 MAYOR): sebagai SOP niat baik, tapi mengajarkan Rupiah salah (baris 347,335,349), `BEM UKRIDA` (baris 251), dan contoh `Rpxxx.xxx`/`Rp.xxx.xxx` campur. Wajib revisi sebelum disebar.
- Template_Proposal_LK_FEB (8.50 batas): tool 10.0 bersih, tapi struktur `II. NAMA KEGIATAN` (bukan TEMA), `III... 1-6 Arab` (bukan A-G), anggaran contoh `Rpxxx.xxx` — harmonisasi dengan TEMPLATE_PROPOSAL resmi.

### H. Optik Melawai Invoice — 5.0 MAYOR (bukan acuan proposal)
- Font `Arial` 9-16pt di generate_docs.py (baku TNR). Kop: `Jl. Tanjung Duren Raya No.4 Telp. 5666952-189 Fax 5666956` — baku `Jl. Tanjung Duren Raya no. 4, Jakarta Barat`, `021 566 6952`, `021 566 6956`. `No.` kapital, missing `021`, missing koma.
- Rupiah `Rp 3.000.000,00` (desimal ,00, tanpa titik setelah Rp) — baku proposal `Rp. 3.000.000`. Untuk invoice eksternal boleh ada ,00, tapi konsistenkan dan dokumentasikan pengecualian.
- Nomor `INV/BEM-FEB/OM/IX/2026` pakai strip (konsisten dengan SPU strip — tapi baku spasi). TTD `Ketua + Bendahara`, tanpa Dekan, tanpa `<u>`, tanpa gelar. Untuk invoice internal mungkin OK, tapi bukan standar SPU/proposal.
- File ganda membingungkan: `Invoice_BEM_FEB_Optik_Melawai.pdf` vs `Invoice BEM FEB UKRIDA - PT Optik Melawai.pdf` (duplikat via shutil.copy). Plus `.venv` ikut terarsip (ratusan file) — bersihkan arsip.

---

## DAFTAR REKOMENDASI PERBAIKAN

### Untuk @lk-drafter (isi & struktur)
1. Harmonisasi 1 standar Bab (usulan ikut 04): I Latar (3 paragraf: umum, urgensi/data, solusi), II Tema (nama + makna 2-3 kalimat), III Kegiatan A.Tujuan min5 B.Manfaat min3 C.Target+estimasi D.Pelaksanaan (Hari/Tanggal/Tempat) E.Narasumber+gelar F.Rundown 3 kolom + Evaluasi penutup G.Games opsional, IV Kepanitiaan + NIM 9 digit, V Anggaran (Pemasukan+Pengeluaran/divisi+TOTAL+Rekap+Sisa Rp.0), VI Penutup + Jakarta, DD Bulan YYYY + Hormat kami + TTD + Mengetahui Dekan (+Menyetujui WR III bila besar).
2. Perbaiki TTD semua template: contoh baku 2 kolom sejajar, nama bold + `<u>underline</u>`, jabatan, NIM dalam kurung, Mengetahui Dekan gelar penuh `Dr. Diana Frederica S.E., M.Ak., CFP®., CHCP-A`, hapus koma setelah Frederica.
3. Global replace informal: `Ketupel`→`Ketua Pelaksana`, `Akutansi`→`Akuntansi`, `kegaitan`→`kegiatan`, `Agustuts`→`Agustus`, `Ekonomi Bisnis`→`Ekonomi & Bisnis`/`Ekonomi dan Bisnis`, `Ukrida`→`UKRIDA`, `BEM UKRIDA`→`BEM FEB UKRIDA`, `BEM-FEB-UKRIDA`→`BEM FEB UKRIDA`, `UKKW`→putuskan `UKRIDA`, `Ketua BEM U`→`Ketua BEM UKRIDA`, `Wakil)aekan`→`Wakil Dekan`, `Tjahj`→`Tjahja`, label `Anggota Humas` di bawah Konsumsi→`Anggota Konsumsi`, `MISS`→hapus.
4. Verifikasi personalia: dual NIM Juan Louis (322025002 vs 322025003), duplikat NIM 322025039, nama `Jessy`/`A Una`/`Una`/`Princess` rangkap (Waketum+Koord Konsumsi+Anggota Acara) — buat tabel master NIM.
5. SPU gold: buat 1 contoh SPU benar (nomor baku, `No`/`Hal` 2 baris, Kepada jelas, tabel Hari/Tanggal|Waktu|Tempat, TTD Ketupel+NIM + Ketua BEM+NIM + Mengetahui Dekan). Arsip SPU PKKMB/Optik jangan dicontoh mentah.
6. Rundown: pastikan kolom Durasi menit terisi angka, format `HH:MM-HH:MM`, hari terakhir tutup `Evaluasi`/`Doa Penutup`, pindahkan PIC/denda internal keluar dari proposal.
7. RAB: pertahankan balance (PKKMB & LKMM sudah balance — apresiasi), tapi tambah baris TOTAL eksplisit, TOTAL bold KAPITAL, rekap + Sisa `Rp. 0` bold. Untuk LPJ tambah kolom Anggaran|Realisasi|Selisih + keterangan sisa.
8. Revisi Panduan_Birokrasi baris 335,347,349 (Rupiah), baris 251 (BEM UKRIDA), contoh `Rpxxx` → `Rp. xxx`. Selaraskan margin 4-3-3-3 dan penomoran dengan 04.

### Untuk @lk-formatter (tipografi, typo, RAB balance & margin)
1. Putuskan margin final dengan pimpinan: rekomendasi **4-3-3-3 A4** (binding kiri) sesuai mandat + SOP + Panduan; lalu revisi `directives/05_audit_tipografi_typo.md` + `PRD_TIPOGRAFI_MARGIN_TYPO.md` yang masih 2.5-2.5-3.0-2.5. Selama belum diputuskan, .md dinilai N/A, .docx/.pdf wajib cantumkan setting margin di properties.
2. Global find-replace Rupiah ke `Rp. X.XXX.XXX`: `RpXXX`→`Rp. XXX`, `Rp XXX`→`Rp. XXX`, `RP.`→`Rp.`, `Rp0`→`Rp. 0`, hapus `,00` untuk proposal (khusus invoice eksternal buat pengecualian tertulis). Perbaiki pesan tool: pola `Rp 900.000` saat ini dilabel `spasi berlebih` — ganti jadi `tanpa titik setelah Rp`.
3. Tanggal: `Jakarta, D Bulan YYYY` tanpa nol depan (`8 September` bukan `08 September`), tanpa koma sebelum tahun, tanpa `DD/MM/YYYY`. Waktu `HH:MM` colon (`06:30` bukan `06.30`, `16:20` bukan `16.20`).
4. Font: migrasi invoice Optik `Arial`→`Times New Roman` (12pt body, 14pt Bold cover, 11pt tabel), hitam #000000, 1.5 spasi isi / single tabel, Justify isi / Center cover / kiri judul bab / kanan angka tabel. Kop: `no` kecil, `021 566 6952`, `021 566 6956`.
5. TTD: implementasi `<u>Nama</u>` bold+underline, alignment sejajar, spasi 3-4 baris tanda tangan, gelar persis (`CFP®.` ada ®, tanpa koma setelah Frederica, urutan gelar jangan dibalik).
6. Perbaiki `execution/typo_checker.py`: hapus duplikat `ketupel`/`Ketupel` (pakai 1 entry case-insensitive), tambah entri `akutansi`, `kegaitan`, `agustuts`, tambah deteksi `Ukrida` vs `UKRIDA` opsional, perbaiki label Rupiah. Tambah `requirements.txt`/venv terpisah untuk `fitz` agar `pdf_extractor.py` bisa jalan; keluarkan `.venv` dari arsip Optik.
7. Jalankan ulang setelah fix: `python -X utf8 execution/typo_checker.py --input [file] --verbose` target ≥9.0; RAB target `Total Pemasukan = Total Pengeluaran, Sisa Rp. 0` via `execution/rab_validator.py --input rab.json` (buat rab.json untuk PKKMB & LKMM agar machine-checkable).
8. Rapikan arsip: rename `Agustuts`→`Agustus`, hapus duplikat PDF invoice, hapus `.venv` dari repo, pisahkan `08 Surat Undangan ... .docx` vs `.pdf` (nama mengandung `&` menyulitkan CLI — rename pakai `_`).

---

## KEPUTUSAN FINAL PER DOKUMEN
- TEMPLATE_PROPOSAL / SPU / LPU: **SIAP SUBMIT sebagai template** (SPU setelah 1-line fix strip). Bersihkan petunjuk [KURUNG] sebelum submit aktual.
- PKKMB Proposal Revisi: **PERLU REVISI MINOR** — terbitkan errata (cover DAN, Rupiah, Ketupel, dual NIM) lalu boleh jadi referensi isi/RAB.
- SPU arsip PKKMB + Optik: **PERLU REVISI MAYOR** — buat SPU gold baru, jangan tiru mentah.
- LKMM II Proposal + Format Proposal Peserta + Panduan: **PERLU REVISI MAYOR — DILARANG diajukan ke pimpinan** sebelum Rupiah + struktur + TTD diperbaiki.
- Format LPJ Peserta: **PERLU REVISI MINOR** — lengkapi Realisasi `Rp.` + NIM TTD.
- Template_Proposal_LK_FEB: **BORDERLINE 8.50** — harmonisasi struktur ke TEMPLATE_PROPOSAL resmi sebelum disebar.
- Invoice Optik: **PERLU REVISI MAYOR sebagai dokumen formal** (font/kop/Rupiah/TTD), tapi sah sebagai bukti transaksi internal.

Dilaporkan ke @lk-orchestrator untuk diteruskan ke @lk-drafter dan @lk-formatter.
