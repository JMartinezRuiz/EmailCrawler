#!/usr/bin/env python3
# aba1.py

import re
import sys

# ─── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
FICHERO         = "ruta/al/fichero1.txt"  # Ruta al fichero de texto de entrada
SKIP_CHARS      = 495                    # Posición de carácter donde comienza el campo ABA
SHOW_DUPLICATES = False                  # True: muestra duplicados; False: omuta duplicados
# ────────────────────────────────────────────────────────────────────────────────

# Expresión regular para extraer el ABA: 3 letras 'ABA', espacios y 9 dígitos
PATRON_ABA = re.compile(r"^ABA\s+(\d{9})")

def extrae_aba1(fichero: str, skip_chars: int, show_dups: bool):
    """
    Lee cada línea de 'fichero', omite los primeros 'skip_chars' caracteres,
    busca un campo que empiece con 'ABA   123456789' y extrae solo los 9 dígitos.
    Ignora líneas sin ese patrón. Si show_dups es False, suprime valores repetidos.
    """
    vistos = set()
    try:
        with open(fichero, encoding="utf-8") as f:
            for linea in f:
                linea = linea.rstrip("\n")
                # Saltar líneas cortas
                if len(linea) <= skip_chars:
                    continue
                fragmento = linea[skip_chars:]
                match = PATRON_ABA.match(fragmento)
                if not match:
                    # No hay campo ABA en esta línea
                    continue
                aba = match.group(1)
                # Control de duplicados
                if show_dups or aba not in vistos:
                    print(aba)
                    vistos.add(aba)
    except FileNotFoundError:
        print(f"ERROR: No se encontró el fichero '{fichero}'.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    extrae_aba1(FICHERO, SKIP_CHARS, SHOW_DUPLICATES)

