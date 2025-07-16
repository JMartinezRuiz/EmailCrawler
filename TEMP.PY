#!/usr/bin/env python3
# aba.py

import re

# ─── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
FICHERO      = "ruta/al/fichero.txt"  # ← Pon aquí la ruta a tu fichero de texto
COLUMNA      = 3                      # ← Número de columna que deseas extraer (1 = primera columna)
MIN_ESPACIOS = 4                      # ← Mínimo de espacios seguidos que actúan como separador
# ────────────────────────────────────────────────────────────────────────────────

def extrae_columna(fichero: str, columna: int, min_espacios: int):
    """
    Lee cada línea de 'fichero', divide en columnas usando como separador
    bloques de 'min_espacios' o más espacios, e imprime la 'columna'-ésima.
    """
    # Compila patrón para N o más espacios
    patron = re.compile(rf"\s{{{min_espacios},}}")
    try:
        with open(fichero, encoding="utf-8") as f:
            for linea in f:
                linea = linea.rstrip("\n")
                campos = patron.split(linea)
                idx = columna - 1
                if 0 <= idx < len(campos):
                    print(campos[idx])
                else:
                    # Línea sin suficiente número de columnas: imprime vacío
                    print("")
    except FileNotFoundError:
        print(f"ERROR: No se encontró el fichero '{fichero}'.")

if __name__ == "__main__":
    extrae_columna(FICHERO, COLUMNA, MIN_ESPACIOS)
