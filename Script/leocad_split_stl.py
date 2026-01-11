import os
import subprocess
import argparse

LDVIEW_PATH = "/Applications/LDView.app/Contents/MacOS/LDView"

def estrai_pezzi(input_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    pezzi = []
    idx = 0

    for line in lines:
        line = line.strip()
        if not line.startswith("1 "):
            continue

        idx += 1
        parts = line.split()
        part_file = parts[-1]
        part_name = os.path.splitext(os.path.basename(part_file))[0]

        out_ldr = os.path.join(output_dir, f"{idx:03d}_{part_name}.ldr")

        content = [
            f"0 FILE {out_ldr}",
            f"0 Name: {part_name}",
            "0 Generated automatically",
            line
        ]

        with open(out_ldr, "w", encoding="utf-8") as out_f:
            out_f.write("\n".join(content) + "\n")

        pezzi.append(out_ldr)

    return pezzi


def converti_in_stl(ldr_file):
    stl_file = ldr_file.replace(".ldr", ".stl")

    cmd = [
        LDVIEW_PATH,
        "-ExportFile=" + stl_file,
        "-SaveExportFile",
        "-ExportFormat=STL",
        ldr_file
    ]

    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return stl_file


def main():
    parser = argparse.ArgumentParser(description="Estrai e converti pezzi LeoCAD in STL")
    parser.add_argument("input", help="File .ldr esportato da LeoCAD")
    parser.add_argument("-o", "--output", default="pezzi_stl", help="Cartella di output")

    args = parser.parse_args()

    print("Estrazione pezzi…")
    pezzi = estrai_pezzi(args.input, args.output)

    print(f"Trovati {len(pezzi)} pezzi")

    print("Conversione in STL…")
    for p in pezzi:
        stl = converti_in_stl(p)
        print("Creato:", stl)

    print("Fatto!")


if __name__ == "__main__":
    main()
