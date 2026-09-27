"""
execution/pdf_extractor.py
===========================
Ekstrak teks dari PDF dokumen BEM FEB UKRIDA untuk analisis dan referensi.
Menggunakan PyMuPDF (fitz) yang sudah terinstall.

Penggunaan:
    python execution/pdf_extractor.py --input "path/ke/file.pdf"
    python execution/pdf_extractor.py --input "path/ke/file.pdf" --output "output.txt"
    python execution/pdf_extractor.py --input "path/ke/file.pdf" --analyze
"""

import fitz  # PyMuPDF
import argparse
import sys
from pathlib import Path


def extract_pdf(pdf_path: str) -> list[dict]:
    """
    Ekstrak teks dari PDF per halaman.
    
    Returns:
        List of dicts: [{"page": int, "text": str}]
    """
    doc = fitz.open(pdf_path)
    pages = []
    
    for i, page in enumerate(doc):
        text = page.get_text()
        pages.append({
            "page": i + 1,
            "text": text.strip()
        })
    
    doc.close()
    return pages


def analyze_proposal_structure(pages: list[dict]) -> dict:
    """
    Analisis struktur proposal BEM FEB UKRIDA dari teks yang diekstrak.
    Deteksi keberadaan bagian-bagian wajib.
    """
    full_text = " ".join(p["text"] for p in pages).upper()
    
    sections = {
        "cover": any(kw in full_text for kw in ["BEM", "BADAN EKSEKUTIF", "FAKULTAS EKONOMI"]),
        "latar_belakang": "LATAR BELAKANG" in full_text,
        "tema": "TEMA KEGIATAN" in full_text,
        "tujuan": "TUJUAN KEGIATAN" in full_text,
        "manfaat": "MANFAAT KEGIATAN" in full_text,
        "target_peserta": "TARGET PESERTA" in full_text,
        "pelaksanaan": "PELAKSANAAN KEGIATAN" in full_text,
        "rundown": any(kw in full_text for kw in ["SUSUNAN ACARA", "RUNDOWN"]),
        "kepanitiaan": "KEPANITIAAN" in full_text,
        "anggaran": "ANGGARAN" in full_text,
        "pemasukan": "PEMASUKAN" in full_text,
        "pengeluaran": "PENGELUARAN" in full_text,
        "penutup": "PENUTUP" in full_text,
    }
    
    found = sum(1 for v in sections.values() if v)
    total = len(sections)
    score = found / total * 10
    
    return {
        "sections": sections,
        "score": round(score, 1),
        "page_count": len(pages),
        "total_chars": sum(len(p["text"]) for p in pages)
    }


def print_analysis(analysis: dict, pages: list[dict]) -> None:
    """Print laporan analisis struktur proposal."""
    print("\n" + "="*60)
    print("  ANALISIS STRUKTUR PROPOSAL BEM FEB UKRIDA")
    print("="*60)
    
    print(f"\n📄 Jumlah Halaman : {analysis['page_count']}")
    print(f"📝 Total Karakter : {analysis['total_chars']:,}")
    print(f"⭐ Skor Kelengkapan: {analysis['score']}/10")
    
    print("\n📋 Checklist Bagian Wajib:")
    for section, found in analysis["sections"].items():
        status = "✅" if found else "❌"
        name = section.replace("_", " ").title()
        print(f"   {status} {name}")
    
    print("\n" + "="*60)
    
    if analysis["score"] >= 9:
        print("  ✅ STRUKTUR LENGKAP — Proposal siap dianalisis lebih lanjut")
    elif analysis["score"] >= 7:
        print("  ⚠️  STRUKTUR CUKUP — Ada beberapa bagian yang mungkin perlu ditambahkan")
    else:
        print("  ❌ STRUKTUR KURANG — Banyak bagian wajib yang tidak ditemukan")
    
    print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Ekstrak dan analisis PDF dokumen BEM FEB UKRIDA"
    )
    parser.add_argument("--input", required=True, help="Path ke file PDF")
    parser.add_argument("--output", help="Path output file teks (opsional)")
    parser.add_argument("--analyze", action="store_true", help="Analisis struktur proposal")
    
    args = parser.parse_args()
    
    # Cek file ada
    if not Path(args.input).exists():
        print(f"❌ File tidak ditemukan: {args.input}")
        sys.exit(1)
    
    print(f"📖 Mengekstrak: {args.input}")
    pages = extract_pdf(args.input)
    print(f"✅ Berhasil: {len(pages)} halaman diekstrak")
    
    # Output ke file jika diminta
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            for page in pages:
                f.write(f"\n\n=== HALAMAN {page['page']} ===\n")
                f.write(page["text"])
        print(f"💾 Teks disimpan ke: {args.output}")
    else:
        # Print ke stdout (preview 1000 char pertama)
        for page in pages[:3]:
            print(f"\n--- HALAMAN {page['page']} ---")
            print(page["text"][:500] + "..." if len(page["text"]) > 500 else page["text"])
    
    # Analisis jika diminta
    if args.analyze:
        analysis = analyze_proposal_structure(pages)
        print_analysis(analysis, pages)
    
    return pages


if __name__ == "__main__":
    main()
