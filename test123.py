#!/usr/bin/env python3
"""
aba_no_bic.py

Identifica los ABA en un fichero que NO tienen BIC.

- ABA empieza en posición 501 (1-based) de cada línea, longitud 9 dígitos.
- BIC esperado empieza en posición 537 (1-based). Consideramos que no hay BIC
  si los siguientes N caracteres (BIC_CHECK_LEN) son espacios o la posición no existe.
- Imprime cada ABA que cumpla la condición.
- Opción de omitir duplicados basados en ABA mediante SHOW_DUPLICATES.
Soporta UTF-8 (con BOM) y Latin-1.
"""
import sys

# ─── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
FICHERO            = "ruta/al/fichero.txt"  # Ruta al fichero de texto
ABA_POS_1BASED     = 501                     # Posición 1-based donde empieza ABA
FIELD_LENGTH       = 9                       # Longitud de los 9 dígitos del ABA
BIC_POS_1BASED     = 537                     # Posición 1-based donde empieza BIC
BIC_CHECK_LEN      = 5                       # Número de caracteres a verificar para BIC ausente
SHOW_DUPLICATES    = False                   # False: omite ABA repetidos; True: muestra todos
# ────────────────────────────────────────────────────────────────────────────────


def read_lines(filepath: str):
    """
    Lee todas las líneas de un fichero con fallback en utf-8-sig y latin-1.
    Devuelve lista de líneas sin salto final.
    """
    for enc in ("utf-8-sig", "latin-1"):
        try:
            with open(filepath, encoding=enc) as f:
                return [l.rstrip("\n") for l in f]
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"ERROR: No se encontró el fichero '{filepath}'", file=sys.stderr)
            sys.exit(1)
    print(f"ERROR: No se pudo leer '{filepath}' en utf-8-sig ni latin-1.", file=sys.stderr)
    sys.exit(1)


def extrae_aba_sin_bic(fichero: str, aba_pos: int, field_len: int,
                      bic_pos: int, bic_check_len: int, show_dups: bool):
    """
    Extrae ABAs que no tienen BIC.
    """
    vistos = set()
    # Conversión a índices 0-based
    skip = aba_pos - 1
    bic_index = bic_pos - 1
    lineas = read_lines(fichero)

    for linea in lineas:
        # Extraer ABA si la línea es lo bastante larga
        if len(linea) < skip + field_len:
            continue
        aba = linea[skip:skip + field_len].strip()
        if not aba:
            continue
        # Verificar ausencia de BIC: si no hay suficientes chars o todos son espacios
        bic_region = linea[bic_index:bic_index + bic_check_len] if len(linea) >= bic_index + bic_check_len else ""
        if bic_region.strip() != "":
            # Existe algún carácter no-espacio → hay BIC, ignorar
            continue
        # Control de duplicados
        if not show_dups and aba in vistos:
            continue
        vistos.add(aba)
        print(aba)


if __name__ == "__main__":
    extrae_aba_sin_bic(FICHERO, ABA_POS_1BASED, FIELD_LENGTH,
                      BIC_POS_1BASED, BIC_CHECK_LEN, SHOW_DUPLICATES)
