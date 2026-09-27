"""
execution/rab_validator.py
==========================
Validator otomatis RAB (Rencana Anggaran Biaya) untuk proposal BEM FEB UKRIDA.
Memastikan: Total Pemasukan = Total Pengeluaran (Sisa = Rp 0)

Penggunaan:
    python execution/rab_validator.py --input "01_Proposal/PKKMB_2026/rab.json"
    python execution/rab_validator.py --interactive
"""

import json
import sys
import argparse
from typing import Optional


def format_rupiah(amount: int) -> str:
    """Format integer ke string Rupiah Indonesia."""
    return f"Rp. {amount:,}".replace(",", ".")


def validate_rab(data: dict) -> dict:
    """
    Validasi RAB BEM FEB UKRIDA.
    
    Args:
        data: dict dengan struktur:
            {
                "pemasukan": [{"sumber": str, "jumlah": int}],
                "pengeluaran": {
                    "acara": [{"item": str, "qty": int, "harga": int}],
                    "konsumsi": [...],
                    "pubdok": [...],
                    "perlengkapan": [...],
                    "humas_p3k": [...]
                }
            }
    
    Returns:
        dict hasil validasi
    """
    hasil = {
        "status": "PASS",
        "errors": [],
        "warnings": [],
        "pemasukan_total": 0,
        "pengeluaran_total": 0,
        "sisa": 0,
        "per_divisi": {}
    }
    
    # Hitung total pemasukan
    for item in data.get("pemasukan", []):
        hasil["pemasukan_total"] += item.get("jumlah", 0)
    
    # Hitung total pengeluaran per divisi
    for divisi, items in data.get("pengeluaran", {}).items():
        total_divisi = 0
        for item in items:
            subtotal = item.get("qty", 1) * item.get("harga", 0)
            total_divisi += subtotal
        hasil["per_divisi"][divisi] = total_divisi
        hasil["pengeluaran_total"] += total_divisi
    
    # Hitung sisa
    hasil["sisa"] = hasil["pemasukan_total"] - hasil["pengeluaran_total"]
    
    # Validasi
    if hasil["sisa"] != 0:
        hasil["status"] = "FAIL"
        if hasil["sisa"] > 0:
            hasil["errors"].append(
                f"❌ TIDAK BALANCE: Pemasukan lebih besar {format_rupiah(hasil['sisa'])}. "
                f"Tambahkan pengeluaran atau kurangi pemasukan."
            )
        else:
            hasil["errors"].append(
                f"❌ TIDAK BALANCE: Pengeluaran melebihi pemasukan sebesar {format_rupiah(abs(hasil['sisa']))}. "
                f"Tambahkan sumber dana atau kurangi pengeluaran."
            )
    
    # Warnings
    if hasil["pemasukan_total"] == 0:
        hasil["warnings"].append("⚠️ Total pemasukan Rp 0 — pastikan sumber dana sudah diisi")
    
    if not data.get("pengeluaran"):
        hasil["warnings"].append("⚠️ Tidak ada item pengeluaran — pastikan RAB sudah diisi")
    
    return hasil


def print_report(hasil: dict) -> None:
    """Print laporan validasi RAB."""
    print("\n" + "="*60)
    print("  LAPORAN VALIDASI RAB — BEM FEB UKRIDA")
    print("="*60)
    
    print(f"\n📥 Total Pemasukan  : {format_rupiah(hasil['pemasukan_total'])}")
    print(f"📤 Total Pengeluaran: {format_rupiah(hasil['pengeluaran_total'])}")
    print(f"💰 Sisa            : {format_rupiah(hasil['sisa'])}")
    
    if hasil.get("per_divisi"):
        print("\n📊 Rincian Per Divisi:")
        for divisi, total in hasil["per_divisi"].items():
            print(f"   {divisi.replace('_', ' ').title():<25} : {format_rupiah(total)}")
    
    print("\n" + "-"*60)
    
    if hasil["errors"]:
        for err in hasil["errors"]:
            print(f"  {err}")
    
    if hasil["warnings"]:
        for warn in hasil["warnings"]:
            print(f"  {warn}")
    
    print("-"*60)
    
    if hasil["status"] == "PASS":
        print("  ✅ RAB VALID — Pemasukan = Pengeluaran (Sisa Rp. 0)")
    else:
        print("  ❌ RAB TIDAK VALID — Perbaiki sebelum submit proposal!")
    
    print("="*60 + "\n")


def interactive_mode() -> dict:
    """Mode interaktif untuk input RAB dari terminal."""
    print("\n🧮 RAB VALIDATOR — Mode Interaktif")
    print("Masukkan data anggaran BEM FEB UKRIDA\n")
    
    data = {"pemasukan": [], "pengeluaran": {}}
    
    # Input pemasukan
    print("--- PEMASUKAN ---")
    n_masuk = int(input("Berapa sumber dana? "))
    for i in range(n_masuk):
        sumber = input(f"Sumber {i+1}: ")
        jumlah = int(input(f"Jumlah (Rp): "))
        data["pemasukan"].append({"sumber": sumber, "jumlah": jumlah})
    
    # Input pengeluaran
    print("\n--- PENGELUARAN ---")
    divisi_list = ["acara", "konsumsi", "pubdok", "perlengkapan", "humas_p3k"]
    
    for divisi in divisi_list:
        print(f"\nDivisi {divisi.replace('_', ' ').upper()}:")
        n_item = int(input(f"  Jumlah item? (0 = lewati): "))
        
        if n_item == 0:
            continue
        
        data["pengeluaran"][divisi] = []
        for i in range(n_item):
            item = input(f"  Item {i+1}: ")
            qty = int(input(f"  Qty: "))
            harga = int(input(f"  Harga satuan (Rp): "))
            data["pengeluaran"][divisi].append({
                "item": item, "qty": qty, "harga": harga
            })
    
    return data


def main():
    parser = argparse.ArgumentParser(description="Validator RAB BEM FEB UKRIDA")
    parser.add_argument("--input", help="Path ke file JSON RAB")
    parser.add_argument("--interactive", action="store_true", help="Mode interaktif")
    
    args = parser.parse_args()
    
    if args.interactive or not args.input:
        data = interactive_mode()
    else:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    
    hasil = validate_rab(data)
    print_report(hasil)
    
    # Return exit code
    sys.exit(0 if hasil["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
