#!/usr/bin/env python3
# aba1.py

import re
import sys

# ─── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
FICHERO         = "ruta/al/fichero1.txt"  # Ruta al fichero de texto de entrada
SHOW_DUPLICATES = False                  # True: muestra duplicados; False: omite duplicados
# ────────────────────────────────────────────────────────────────────────────────

# Patrón para extraer el ABA: tres espacios, 'ABA', tres espacios, seguido de 9 dígitos
PATRON_ABA = re.compile(r"\s{3}ABA\s{3}(\d{9})")

def extrae_aba1(fichero: str, show_dups: bool):
    """
    Lee cada línea de 'fichero', busca todas las ocurrencias del patrón
    '   ABA   123456789' y extrae los 9 dígitos. Ignora líneas sin coincidencias.
    Si show_dups es False, omite valores repetidos.
    """
    vistos = set()
    try:
        with open(fichero, encoding="utf-8") as f:
            for linea in f:
                for match in PATRON_ABA.finditer(linea):
                    aba = match.group(1)
                    if show_dups or aba not in vistos:
                        print(aba)
                        vistos.add(aba)
    except FileNotFoundError:
        print(f"ERROR: No se encontró el fichero '{fichero}'.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    extrae_aba1(FICHERO, SHOW_DUPLICATES)
