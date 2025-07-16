#!/usr/bin/env python3
"""
aba11.py

Script avanzado para extraer pares ABA;BIC de un fichero:

1. Busca ABA con el patrón: tres espacios + 'ABA' + tres espacios + 9 dígitos.
2. Para cada ABA encontrado, tras el número salta espacios y:
   - Si la primera posición no espacio es una letra, toma esa letra + los siguientes 10 caracteres como BIC (total 11).
   - Si es un dígito o no existe, considera que no hay BIC.
3. Imprime cada pareja en formato: ABA;BIC (o ABA; si no hay BIC).
4. Controla duplicados basados en ABA según SHOW_DUPLICATES.
Soporta ficheros en UTF-8 (con o sin BOM) o Latin-1.
"""
import re
import sys

# ─── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
FICHERO = "ruta/al/fichero.txt"  # Ruta al fichero de texto de entrada
SHOW_DUPLICATES = False           # True: muestra todos los pares; False: omite ABA repetidos
# ────────────────────────────────────────────────────────────────────────────────

# Patrón para identificar ABA: 3 espacios + 'ABA' + 3 espacios + 9 dígitos
PATRON_ABA = re.compile(r"\s{3}ABA\s{3}(\d{9})")


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


def extrae_aba11(fichero: str, show_dups: bool):
    """
    Extrae de cada línea los pares ABA;BIC y los imprime.
    """
    vistos = set()
    lineas = read_lines(fichero)

    for linea in lineas:
        # Buscar cada ocurrencia de ABA en la línea
        for match in PATRON_ABA.finditer(linea):
            aba = match.group(1)
            # Filtrar duplicados
            if not show_dups and aba in vistos:
                continue
            vistos.add(aba)

            # Hacer espacio después del ABA para buscar BIC
            pos = match.end()
            # Saltar espacios
            while pos < len(linea) and linea[pos].isspace():
                pos += 1

            bic = ""
            # Si el primer char no espacio es letra, extraer 11 caracteres
            if pos < len(linea) and linea[pos].isalpha():
                bic = linea[pos:pos+11]

            # Imprimir resultado
            print(f"{aba};{bic}")


if __name__ == "__main__":
    extrae_aba11(FICHERO, SHOW_DUPLICATES)
