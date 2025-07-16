#!/usr/bin/env python3
# aba.py

import sys

# ─── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
FICHERO         = "ruta/al/fichero.txt"  # Ruta al fichero de texto
SKIP_CHARS      = 499                    # Posición de carácter a partir de la cual extraer
FIELD_LENGTH    = 9                      # Longitud del campo a extraer (9 dígitos para ABA)
SHOW_DUPLICATES = False                  # True: muestra todas las ocurrencias; False: omite duplicados
# ────────────────────────────────────────────────────────────────────────────────

def extrae_aba(fichero: str, skip_chars: int, field_len: int, show_dups: bool):
    """
    Lee cada línea de 'fichero', omite los primeros 'skip_chars' caracteres,
    extrae 'field_len' caracteres como el campo ABA, y los imprime.
    Si show_dups es False, suprime valores repetidos.
    """
    vistos = set()
    try:
        with open(fichero, encoding="utf-8") as f:
            for linea in f:
                linea = linea.rstrip("\n")
                if len(linea) <= skip_chars:
                    valor = ""
                else:
                    # Extraer campo fijo de longitud field_len
                    segmento = linea[skip_chars:skip_chars + field_len]
                    valor = segmento.strip()

                if show_dups or valor not in vistos:
                    print(valor)
                    vistos.add(valor)
    except FileNotFoundError:
        print(f"ERROR: No se encontró el fichero '{fichero}'.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    extrae_aba(FICHERO, SKIP_CHARS, FIELD_LENGTH, SHOW_DUPLICATES)
