#!/usr/bin/env python3
# aba.py

import re

# ─── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
FICHERO         = "ruta/al/fichero.txt"  # ← Ruta a tu fichero de texto
COLUMNA         = 3                      # ← Número de columna que deseas extraer (1 = primera)
MIN_ESPACIOS    = 4                      # ← Mínimo de espacios seguidos que actúan como separador
SHOW_DUPLICATES = False                  # ← True: muestra todos los valores
                                         #    False: omite las ocurrencias repetidas
# ────────────────────────────────────────────────────────────────────────────────

def extrae_columna(fichero: str, columna: int, min_espacios: int, show_dups: bool):
    """
    Lee cada línea de 'fichero', divide en columnas usando bloques
    de 'min_espacios' o más espacios, e imprime la 'columna'-ésima.
    Si show_dups es False, suprime los valores repetidos.
    """
    patron = re.compile(rf"\s{{{min_espacios},}}")
    vistos = set()

    try:
        with open(fichero, encoding="utf-8") as f:
            for linea in f:
                linea = linea.rstrip("\n")
                campos = patron.split(linea)
                idx = columna - 1

                if 0 <= idx < len(campos):
                    valor = campos[idx]
                else:
                    # Si no existe esa columna, considerar valor vacío
                    valor = ""

                if show_dups:
                    print(valor)
                else:
                    if valor not in vistos:
                        print(valor)
                        vistos.add(valor)
    except FileNotFoundError:
        print(f"ERROR: No se encontró el fichero '{fichero}'.")

if __name__ == "__main__":
    extrae_columna(FICHERO, COLUMNA, MIN_ESPACIOS, SHOW_DUPLICATES)
