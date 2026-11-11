#!/usr/bin/env python3
"""Regressionstest: vergleicht einen neuen Chart-Export mit einer Referenz (tests/reference/).

Aufruf:
  python3 tests/compare_reference.py tests/reference/<Referenz>.csv <neuer Export>.csv
  python3 tests/compare_reference.py --all            (alle Referenzen gegen tests/current/)

TradingView-Export: Chart-Menü → „Chart-Daten exportieren“ (ISO-Zeit). Dateiname z. B. „BATS_XLU, 1D_76ccd.csv“;
der Teil vor dem letzten „_“ (Symbol und Zeitrahmen) dient bei --all als Schlüssel, der Hash danach ist egal.

Verglichen werden die Plots des Indikators „AKJ2.0 – Trend & Setup Detector“ (Liste COLUMNS) für alle Kerzen,
die in beiden Dateien vorkommen – bis zur vorletzten Kerze der Referenz (die letzte ist meist die laufende Kerze).
Leere Felder gelten als na. Zahlen gelten als gleich bei |a − b| ≤ 1e-6 · max(1, |a|).
Doppelte Spaltennamen (weitere Indikatoren im Chart) werden positionsweise unterschieden; für COLUMNS zählt
das erste Vorkommen – der Indikator sollte deshalb der erste Indikator im Chart sein.
"""
import argparse
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REFERENCE_DIR = ROOT / "reference"
CURRENT_DIR = ROOT / "current"

# Plots des Indikators (Titel wie im Skript). „Tage bis Earnings“ ändert sich täglich → nicht vergleichen.
COLUMNS = [
    "Setup-Status (1 Long / -1 Short / 0)",
    "Setup Entry",
    "Setup SL",
    "Setup Risiko (%)",
    "Entry (Stop-Order)",
    "Stop-Loss",
    "Trend übergeordnet W bzw. M (1 / -1)",
    "Trend Trade-TF D bzw. W (1 / -1)",
    "Williams %R (abgeschl. Kerze)",
    "Offene FVGs (Anzahl)",
    "FVG im Gewinnbereich (1 / 0)",
    "BB Mid",
    "BB Upper",
    "BB Lower",
    "MA 20",
    "MA 50",
    "MA 150",
    "MA 200",
]
REL_TOL = 1e-6


def read_export(path: Path):
    """Liest einen TradingView-Export. Rückgabe: (Spaltennamen, {Zeit: Zeile als Liste})."""
    with path.open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.reader(fh))
    if not rows or rows[0][0] != "time":
        sys.exit(f"{path}: kein TradingView-Export (erste Spalte muss „time“ sein)")
    header = rows[0]
    data = {r[0]: r for r in rows[1:] if r}
    return header, data


def first_index(header, name):
    try:
        return header.index(name)
    except ValueError:
        return None


def parse(value: str):
    value = value.strip()
    if value == "" or value.lower() in ("nan", "na"):
        return None
    return float(value)


def equal(a, b) -> bool:
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    if math.isnan(a) and math.isnan(b):
        return True
    return abs(a - b) <= REL_TOL * max(1.0, abs(a))


def fmt(v) -> str:
    return "na" if v is None else (f"{v:.6g}" if abs(v) >= 1e-4 or v == 0 else f"{v:.6e}")


def compare(ref_path: Path, new_path: Path, max_show: int, include_last: bool) -> int:
    ref_header, ref = read_export(ref_path)
    new_header, new = read_export(new_path)
    ref_times = list(ref.keys())
    if not include_last and ref_times:
        ref_times = ref_times[:-1]
    common = [t for t in ref_times if t in new]
    print(f"{ref_path.name}  ↔  {new_path.name}")
    print(f"  Referenz {len(ref)} Kerzen ({next(iter(ref))} … {ref_times[-1] if ref_times else '–'}), "
          f"neu {len(new)} Kerzen, gemeinsam verglichen: {len(common)}")
    missing_new = [t for t in ref_times if t not in new]
    if missing_new:
        print(f"  Hinweis: {len(missing_new)} Referenz-Kerzen fehlen im neuen Export (z. B. {missing_new[0]}) – "
              "weniger Historie geladen?")
    total_diff = 0
    for col in COLUMNS:
        ri, ni = first_index(ref_header, col), first_index(new_header, col)
        if ri is None or ni is None:
            where = "Referenz" if ri is None else "neuem Export"
            print(f"  ⚠ Spalte „{col}“ fehlt im {where} – übersprungen")
            continue
        diffs = []
        for t in common:
            a, b = parse(ref[t][ri]), parse(new[t][ni])
            if not equal(a, b):
                diffs.append((t, a, b))
        if diffs:
            total_diff += len(diffs)
            print(f"  ✘ {col}: {len(diffs)} Abweichungen")
            for t, a, b in diffs[:max_show]:
                print(f"      {t}: Referenz {fmt(a)}, neu {fmt(b)}")
            if len(diffs) > max_show:
                print(f"      … und {len(diffs) - max_show} weitere")
        else:
            print(f"  ✔ {col}")
    print("  → " + ("KEINE Abweichungen" if total_diff == 0 else f"{total_diff} Abweichungen"))
    return total_diff


def key_of(path: Path) -> str:
    """„BATS_XLU, 1D_76ccd.csv“ → „BATS_XLU, 1D“ (Hash nach dem letzten „_“ weg)."""
    stem = path.stem
    return stem.rsplit("_", 1)[0] if "_" in stem else stem


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("reference", nargs="?", help="Referenz-CSV (tests/reference/…)")
    ap.add_argument("new", nargs="?", help="neuer Export")
    ap.add_argument("--all", action="store_true", help="alle Referenzen gegen gleichnamige Dateien in tests/current/")
    ap.add_argument("--show", type=int, default=10, help="max. gezeigte Abweichungen je Spalte (Standard 10)")
    ap.add_argument("--include-last", action="store_true", help="auch die letzte (laufende) Kerze vergleichen")
    args = ap.parse_args()

    pairs = []
    if args.all:
        current = {key_of(p): p for p in CURRENT_DIR.glob("*.csv")} if CURRENT_DIR.exists() else {}
        for ref in sorted(REFERENCE_DIR.glob("*.csv")):
            new = current.get(key_of(ref))
            if new is None:
                print(f"{ref.name}: kein neuer Export in {CURRENT_DIR.relative_to(ROOT.parent)}/ (Schlüssel „{key_of(ref)}“)")
                continue
            pairs.append((ref, new))
        if not pairs:
            sys.exit("Nichts zu vergleichen.")
    elif args.reference and args.new:
        pairs.append((Path(args.reference), Path(args.new)))
    else:
        ap.error("Referenz und neuen Export angeben oder --all verwenden")

    total = sum(compare(r, n, args.show, args.include_last) for r, n in pairs)
    print()
    print("ERGEBNIS: " + ("alle Referenzen unverändert ✔" if total == 0 else f"{total} Abweichungen ✘"))
    sys.exit(0 if total == 0 else 1)


if __name__ == "__main__":
    main()
