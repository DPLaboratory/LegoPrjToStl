import argparse
import os
import subprocess
from collections import Counter

LDRAW_PARTS_DIR = os.path.expanduser("~/Lego/ldraw/parts")
LDVIEW_CMD = "LDView"  # o percorso completo: "/usr/bin/ldview"

def estrai_codici(file_ldr):
    codici = []
    with open(file_ldr, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line.startswith("1 "):
                parts = line.split()
                codice = parts[-1].lower()
                codici.append(codice)
    return sorted(set(codici))  # solo codici unici

def converti_dat_in_stl(codice_dat, output_dir):
    nome_stl = codice_dat.replace(".dat", ".stl")
    path_dat = os.path.join(LDRAW_PARTS_DIR, codice_dat)
    path_stl = os.path.join(output_dir, nome_stl)

    if not os.path.exists(path_dat):
        print(f"❌ Pezzo non trovato: {path_dat}")
        return

    cmd = [
        LDVIEW_CMD,
        "-SaveExportFile",
        "-ExportFormat=STL",
        f"-ExportFile={path_stl}",
        "-Scale=2.5",
        path_dat
    ]

    print(f"command: {cmd} ")

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ {codice_dat} → {nome_stl}")
    except subprocess.CalledProcessError:
        print(f"⚠️ Errore nella conversione di {codice_dat}")


def main():
    parser = argparse.ArgumentParser(description="Estrai codici da file LeoCAD e converti in STL")
    parser.add_argument("input", help="File .ldr o .mpd")
    parser.add_argument("-o", "--output", default="pezzi_stl", help="Cartella output STL")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    codici = estrai_codici(args.input)
    print(f"Trovati {len(codici)} codici unici. Converto in STL…\n")

    for codice in codici:
        converti_dat_in_stl(codice, args.output)

    print("\n✅ Conversione completata.")


if __name__ == "__main__":
    main()

