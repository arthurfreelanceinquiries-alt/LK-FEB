"""
execution/typo_checker.py
# Windows UTF-8 fix: set PYTHONIOENCODING=utf-8 or run with: python -X utf8 typo_checker.py
==========================
Cek typo dan kesalahan penulisan otomatis untuk dokumen BEM FEB UKRIDA.
Berdasarkan standar di: 00_SISTEM_BEM/PRD_TIPOGRAFI_MARGIN_TYPO.md

Penggunaan:
    python execution/typo_checker.py --input "01_Proposal/PKKMB_2026/proposal.md"
    python execution/typo_checker.py --input "01_Proposal/PKKMB_2026/proposal.md" --verbose
    python execution/typo_checker.py --input "01_Proposal/PKKMB_2026/proposal.md" --output "06_Audit_Review/typo_report.md"
"""

import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field


# ─────────────────────────────────────────────
# KAMUS TYPO — Tambahkan di sini jika ada temuan baru
# ─────────────────────────────────────────────

TYPO_KAMUS = {
    # Ejaan bahasa Indonesia
    "praktek": "praktik",
    "sistim": "sistem",
    "analisa": "analisis",
    "aktifitas": "aktivitas",
    "nomer": "nomor",
    "sekedar": "sekadar",
    "merubah": "mengubah",
    "mahsiswa": "mahasiswa",
    "mahasisiwa": "mahasiswa",
    "acadmik": "akademik",
    "perobahan": "perubahan",
    "kreatifitas": "kreativitas",
    "produktifitas": "produktivitas",
    "effektif": "efektif",
    "effisien": "efisien",
    "managemen": "manajemen",
    "resiko": "risiko",
    "legalisir": "legalisasi",
    "ijin": "izin",
    "apotik": "apotek",
    "atlit": "atlet",
    "subyek": "subjek",
    "obyek": "objek",
    "standardisasi": "standarisasi",
    "standarisir": "standarisasi",

    # Kesalahan umum kemahasiswaan
    "ketupel": "Ketua Pelaksana",
    "Ketupel": "Ketua Pelaksana",
    "mahasiswa baru 2026": "mahasiswa baru angkatan 2026",  # reminder
}

TYPO_EJAAN_SALAH = {
    # Kata yang sering salah eja
    "dll,": "dll.",          # titik, bukan koma
    "dsb,": "dsb.",
    "etc,": "dll.",          # jangan pakai "etc" di dokumen formal Indonesia
    "dll :": "dll.",
    "dsb :": "dsb.",
}

# Format rupiah yang SALAH → flagging
POLA_RUPIAH_SALAH = [
    (r'\bRp(\d)', "Rp (tanpa titik/spasi setelah Rp) — contoh salah: Rp10.000"),
    (r'\bRp\.\d', "Rp. tanpa spasi setelah titik — contoh salah: Rp.10.000"),
    (r'\bRp\s+\d', "Ada spasi berlebih antara Rp dan angka"),
    (r'\bRp\.\s+[\d,]+,\d{3}', "Menggunakan koma sebagai pemisah ribuan, seharusnya titik"),
]

# Nama pejabat baku (cek apakah ada versi yang salah)
NAMA_BAKU = {
    "Dr. Diana Frederica S.E., M.Ak., CFP®., CHCP-A": [
        "Dr. Diana Frederica",     # tanpa gelar lengkap → WARNING
        "CFP.",                    # CFP tanpa ® → ERROR
        "Diana Frederica",         # tanpa "Dr." → WARNING
    ],
    "Dr. Daniel Widjaja, S.E., M.M., CSCU, CEAP": [
        "Daniel Widjaja",          # tanpa "Dr." → WARNING
        "Dr. Daniel Widjaja",      # tanpa gelar belakang → WARNING
    ],
    "Arthur Reezan": [],          # nama saja sudah cukup untuk ketua BEM
    "312023002": [],              # NIM ketua BEM
}

# Nama organisasi yang salah
NAMA_ORG_SALAH = {
    "BEM UKRIDA": "BEM FEB UKRIDA",
    "Fakultas Ekonomi UKRIDA": "Fakultas Ekonomi dan Bisnis UKRIDA",
    "Ekonomi Bisnis": "Ekonomi dan Bisnis",  # tanpa "dan"
    "FEB-UKRIDA": "FEB UKRIDA",  # tidak perlu tanda hubung
}


@dataclass
class TypoError:
    baris: int
    teks_asli: str
    masalah: str
    saran: str
    level: str  # ERROR | WARNING | INFO


@dataclass
class HasilAuditTypo:
    errors: list[TypoError] = field(default_factory=list)
    warnings: list[TypoError] = field(default_factory=list)
    infos: list[TypoError] = field(default_factory=list)
    total_baris: int = 0
    nama_file: str = ""


def cek_typo_per_baris(baris: str, no_baris: int) -> list[TypoError]:
    """Cek satu baris teks untuk semua jenis typo."""
    temuan = []

    # 1. Cek kamus typo ejaan
    for salah, benar in TYPO_KAMUS.items():
        if re.search(r'\b' + re.escape(salah) + r'\b', baris, re.IGNORECASE):
            temuan.append(TypoError(
                baris=no_baris,
                teks_asli=baris.strip(),
                masalah=f'Typo: "{salah}"',
                saran=f'Ganti dengan: "{benar}"',
                level="ERROR"
            ))

    # 2. Cek ejaan "dll." vs "dll,"
    for salah, benar in TYPO_EJAAN_SALAH.items():
        if salah in baris:
            temuan.append(TypoError(
                baris=no_baris,
                teks_asli=baris.strip(),
                masalah=f'Penulisan: "{salah}"',
                saran=f'Seharusnya: "{benar}"',
                level="WARNING"
            ))

    # 3. Cek format Rupiah
    for pola, keterangan in POLA_RUPIAH_SALAH:
        if re.search(pola, baris):
            temuan.append(TypoError(
                baris=no_baris,
                teks_asli=baris.strip(),
                masalah=f"Format Rupiah: {keterangan}",
                saran='Format baku: "Rp. X.XXX.XXX" (spasi setelah titik, titik sebagai pemisah ribuan)',
                level="ERROR"
            ))

    # 4. Cek nama organisasi yang salah
    for salah, benar in NAMA_ORG_SALAH.items():
        if salah in baris:
            temuan.append(TypoError(
                baris=no_baris,
                teks_asli=baris.strip(),
                masalah=f'Nama organisasi: "{salah}"',
                saran=f'Seharusnya: "{benar}"',
                level="WARNING"
            ))

    # 5. Cek gelar CFP tanpa simbol ®
    if "CFP." in baris and "CFP®" not in baris:
        temuan.append(TypoError(
            baris=no_baris,
            teks_asli=baris.strip(),
            masalah='Gelar "CFP." tanpa simbol registered ®',
            saran='Gunakan "CFP®." — simbol ® wajib ada',
            level="ERROR"
        ))

    # 6. Cek format tanggal angka (seharusnya nama bulan)
    if re.search(r'\b\d{1,2}/\d{1,2}/\d{4}\b', baris):
        temuan.append(TypoError(
            baris=no_baris,
            teks_asli=baris.strip(),
            masalah='Format tanggal angka (DD/MM/YYYY)',
            saran='Gunakan format teks: "13 Agustus 2026" atau "Jakarta, 13 Agustus 2026"',
            level="WARNING"
        ))

    # 7. Cek tanda hubung dalam NIM (NIM tidak boleh ada tanda hubung)
    if re.search(r'\b3\d{2}\d{3}-\d{3}\b', baris):
        temuan.append(TypoError(
            baris=no_baris,
            teks_asli=baris.strip(),
            masalah='NIM menggunakan tanda hubung',
            saran='NIM ditulis tanpa tanda hubung: "312023002"',
            level="WARNING"
        ))

    return temuan


def audit_file(path_file: str) -> HasilAuditTypo:
    """Baca file dan jalankan semua cek typo."""
    hasil = HasilAuditTypo(nama_file=path_file)

    with open(path_file, "r", encoding="utf-8") as f:
        baris_list = f.readlines()

    hasil.total_baris = len(baris_list)

    for i, baris in enumerate(baris_list, start=1):
        temuan = cek_typo_per_baris(baris, i)
        for item in temuan:
            if item.level == "ERROR":
                hasil.errors.append(item)
            elif item.level == "WARNING":
                hasil.warnings.append(item)
            else:
                hasil.infos.append(item)

    return hasil


def hitung_skor(hasil: HasilAuditTypo) -> float:
    """Hitung skor tipografi dari 10."""
    penalti = (len(hasil.errors) * 1.0) + (len(hasil.warnings) * 0.3)
    skor = max(0.0, 10.0 - penalti)
    return round(skor, 1)


def format_laporan(hasil: HasilAuditTypo, verbose: bool = False) -> str:
    """Format laporan audit ke string Markdown."""
    skor = hitung_skor(hasil)
    total_masalah = len(hasil.errors) + len(hasil.warnings)

    laporan = []
    laporan.append(f"\n## HASIL AUDIT TYPO & FORMAT — {Path(hasil.nama_file).name}")
    laporan.append(f"**File:** {hasil.nama_file}")
    laporan.append(f"**Total Baris:** {hasil.total_baris}")
    laporan.append(f"**Total Masalah Ditemukan:** {total_masalah} ({len(hasil.errors)} error, {len(hasil.warnings)} warning)\n")

    if hasil.errors:
        laporan.append(f"### ❌ ERROR — Harus Diperbaiki ({len(hasil.errors)} item)\n")
        for e in hasil.errors:
            laporan.append(f"- **Baris {e.baris}:** {e.masalah}")
            if verbose:
                laporan.append(f"  - Teks: `{e.teks_asli[:80]}{'...' if len(e.teks_asli) > 80 else ''}`")
            laporan.append(f"  - 💡 {e.saran}")
    else:
        laporan.append("### ❌ ERROR: ✅ Tidak ada error\n")

    if hasil.warnings:
        laporan.append(f"\n### ⚠️ WARNING — Perlu Diperhatikan ({len(hasil.warnings)} item)\n")
        for w in hasil.warnings:
            laporan.append(f"- **Baris {w.baris}:** {w.masalah}")
            if verbose:
                laporan.append(f"  - Teks: `{w.teks_asli[:80]}{'...' if len(w.teks_asli) > 80 else ''}`")
            laporan.append(f"  - 💡 {w.saran}")
    else:
        laporan.append("\n### ⚠️ WARNING: ✅ Tidak ada warning\n")

    laporan.append(f"\n### 📊 Skor Tipografi & Typo: {skor}/10")

    if skor >= 9.0:
        status = "✅ LOLOS — Kerapihan tipografi sangat baik"
    elif skor >= 8.0:
        status = "✅ LOLOS — Perbaiki warning minor sebelum final"
    elif skor >= 7.0:
        status = "⚠️ PERLU REVISI MINOR — Perbaiki semua error sebelum submit"
    else:
        status = "❌ PERLU REVISI MAYOR — Banyak kesalahan format, perbaiki dulu"

    laporan.append(f"**Status:** {status}")

    return "\n".join(laporan)


def main():
    parser = argparse.ArgumentParser(
        description="Cek typo dan format penulisan dokumen BEM FEB UKRIDA"
    )
    parser.add_argument("--input", required=True, help="Path ke file Markdown/teks yang akan dicek")
    parser.add_argument("--output", help="Path output laporan (opsional — default: print ke layar)")
    parser.add_argument("--verbose", action="store_true", help="Tampilkan cuplikan teks yang bermasalah")

    args = parser.parse_args()

    # Cek file ada
    # Fix Windows console encoding
    sys.stdout.reconfigure(encoding='utf-8')

    if not Path(args.input).exists():
        print(f"[ERROR] File tidak ditemukan: {args.input}")
        sys.exit(1)

    print(f"[AUDIT] Mengaudit: {args.input}")

    hasil = audit_file(args.input)
    laporan = format_laporan(hasil, verbose=args.verbose)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(laporan)
        print(f"[SAVED] Laporan disimpan ke: {args.output}")
    else:
        print(laporan)

    # Exit code berdasarkan ada-tidaknya error
    sys.exit(0 if not hasil.errors else 1)


if __name__ == "__main__":
    main()
