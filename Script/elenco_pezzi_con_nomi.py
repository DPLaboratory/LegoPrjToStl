import argparse
from collections import Counter
import os

def carica_nomi_pezzi(parts_lst_path):
    nomi = {}
    with open(parts_lst_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.strip() == "" or line.startswith("= "):
                continue
            parts = line.strip().split(" ", 1)
            if len(parts) == 2:
                codice, nome = parts
                nomi[codice.lower()] = nome.strip()
    return nomi


def estrai_codici_pezzi(file_ldr):
    codici = []
    with open(file_ldr, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line.startswith("1 "):
                parts = line.split()
                codice = parts[-1]
                codici.append(codice.lower())
    return Counter(codici)


def salva_elenco(counter, nomi, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("Elenco pezzi LeoCAD (quantità, codice, nome):\n\n")
        for codice, count in sorted(counter.items()):
            nome = nomi.get(codice, "??")
            f.write(f"{count:3d} × {codice:15s} {nome}\n")


def main():
    parser = argparse.ArgumentParser(description="Estrai elenco pezzi con nomi da file LeoCAD")
    parser.add_argument("input", help="File .ldr o .mpd")
    parser.add_argument("-p", "--parts", default="parts.lst", help="Percorso al file parts.lst")
    parser.add_argument("-o", "--output", default="elenco_pezzi.txt", help="File di output")

    args = parser.parse_args()

    nomi = carica_nomi_pezzi(args.parts)
    counter = estrai_codici_pezzi(args.input)
    salva_elenco(counter, nomi, args.output)

    print(f"Creato file: {args.output}")


if __name__ == "__main__":
    main()
