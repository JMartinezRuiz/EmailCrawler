#!/usr/bin/env python3
"""
aba2.py

Script avanzado para extraer ABA y BIC de un fichero basado en posición fija:

1. Lee cada línea, omite los primeros SKIP_CHARS caracteres.
2. Extrae FIELD_LENGTH caracteres como ABA, omitiendo espacios.
3. Busca el BIC en la posición fija BIC_POS:
   - Si en esa posición hay una letra, toma esa letra + los siguientes 10 caracteres (total 11).
   - En caso contrario (espacio, dígito u ausencia), considera que no hay BIC.
4. Imprime cada pareja en formato: ABA;BIC (o ABA; si no hay BIC).
5. Control de duplicados basado en ABA según SHOW_DUPLICATES.
Soporta ficheros en UTF-8 (con BOM) o Latin-1.
"""
import sys

# ─── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
FICHERO         = "ruta/al/fichero.txt"  # Ruta al fichero de texto de entrada
SKIP_CHARS      = 499                    # Posición inicial (0-based) para extraer ABA
FIELD_LENGTH    = 9                      # Longitud de los 9 dígitos del ABA
BIC_POS         = 743                    # Posición fija (0-based) donde empieza el BIC
SHOW_DUPLICATES = False                  # True: muestra duplicados; False: omite ABA repetidos
# ────────────────────────────────────────────────────────────────────────────────

def read_lines(filepath: str):
    """
    Lee todas las líneas de un fichero usando utf-8-sig (eliminando BOM) o Latin-1.
    Devuelve una lista de líneas sin salto final.
    """
    for enc in ("utf-8-sig", "latin-1"):
        try:
            with open(filepath, encoding=enc) as f:
                return [line.rstrip("\n") for line in f]
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"ERROR: No se encontró el fichero '{filepath}'", file=sys.stderr)
            sys.exit(1)
    print(f"ERROR: No se pudo leer '{filepath}' en utf-8-sig ni latin-1.", file=sys.stderr)
    sys.exit(1)

def extrae_aba2(fichero: str, skip_chars: int, field_len: int, bic_pos: int, show_dups: bool):
    """
    Extrae ABA y BIC de cada línea y los imprime en formato ABA;BIC.
    """
    vistos = set()
    lineas = read_lines(fichero)

    for linea in lineas:
        # Omitir los primeros skip_chars caracteres
        if len(linea) <= skip_chars:
            continue
        segmento = linea[skip_chars:skip_chars + field_len]
        aba = segmento.strip()
        if not aba:
            continue
        # Filtrar duplicados si corresponde
        if not show_dups and aba in vistos:
            continue
        vistos.add(aba)

        # Buscar BIC en posición fija
        bic = ""
        if len(linea) > bic_pos and linea[bic_pos].isalpha():
            bic = linea[bic_pos:bic_pos + 11]

        print(f"{aba};{bic}")

if __name__ == "__main__":
    extrae_aba2(FICHERO, SKIP_CHARS, FIELD_LENGTH, BIC_POS, SHOW_DUPLICATES)
