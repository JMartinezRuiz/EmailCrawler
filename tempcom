#!/usr/bin/env python3
"""
compare_aba.py

Script para comparar dos ficheros de ABAs:
- FILE1: salida1.txt (ABAs del primer script)
- FILE2: salida2.txt (ABAs del segundo script)

El script imprime los ABAs que aparecen en FILE2 pero NO en FILE1.
Soporta ficheros en UTF-8 o Latin-1 y gestiona errores de lectura.
"""
import sys

# ─── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
FILE1 = "salida1.txt"   # Fichero con ABAs extraídos del primer script
FILE2 = "salida2.txt"   # Fichero con ABAs extraídos del segundo script
# ────────────────────────────────────────────────────────────────────────────────


def read_lines(filepath: str):
    """
    Intenta leer todas las líneas de un fichero usando utf-8 y, si falla,
    vuelve a intentarlo con latin-1. Devuelve una lista de líneas sin saltos de línea.
    """
    for enc in ("utf-8", "latin-1"):
        try:
            with open(filepath, encoding=enc) as f:
                return [line.rstrip("\n") for line in f]
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"ERROR: No se encontró el fichero '{filepath}'", file=sys.stderr)
            sys.exit(1)
    print(f"ERROR: No se pudo leer el fichero '{filepath}' en utf-8 ni latin-1.", file=sys.stderr)
    sys.exit(1)


def compara_abas(f1: str, f2: str):
    """
    Compara dos ficheros que contienen un ABA por línea (sin duplicados).
    Imprime los ABAs que están en f2 pero no en f1.
    """
    lines1 = read_lines(f1)
    lines2 = read_lines(f2)

    # Crear conjuntos y filtrar líneas vacías
    set1 = {line.strip() for line in lines1 if line.strip()}
    set2 = {line.strip() for line in lines2 if line.strip()}

    diff = set2 - set1
    if not diff:
        print("No hay ABAs únicos en el segundo fichero.")
    else:
        for aba in sorted(diff):
            print(aba)


if __name__ == "__main__":
    compara_abas(FILE1, FILE2)
