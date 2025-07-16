#!/usr/bin/env python3
# aba11.py

"""
Script avanzado para extraer ABA y opcionalmente BIC de un fichero.

- Identifica el ABA con el patrón: 3 espacios + 'ABA' + 3 espacios + 9 dígitos.
- Para cada ABA encontrado, busca el BIC justo después:
  - Omite espacios tras el número ABA.
  - Si el siguiente carácter no numérico es letra, toma esa letra + los siguientes 10 caracteres como BIC (total 11).
  - Si el primer carácter no espacio tras el ABA es un dígito o no hay letra, se considera que no hay BIC.
- Imprime cada resultado en formato: ABA;BIC (o ABA; si no hay BIC).
- Permite suprimir duplicados basados en el valor de ABA.
"""
import re
import sys

# ─── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
FICHERO         = "ruta/al/fichero.txt"  # Ruta al fichero de texto de entrada\SHOW_DUPLICATES = False                  # True: muestra duplicados; False: omite duplicados
# ────────────────────────────────────────────────────────────────────────────────

# Patrón para identificar ABA: tres espacios, 'ABA', tres espacios, 9 dígitos
PATRON_ABA = re.compile(r"\s{3}ABA\s{3}(\d{9})")


def extrae_aba11(fichero: str, show_dups: bool):
    """
    Extrae pares ABA;BIC de cada línea del fichero.
    Sólo imprime líneas con ABA. Si show_dups es False, omite ABA repetidos.
    """
    vistos = set()
    try:
        with open(fichero, encoding="utf-8-sig") as f:
            for linea in f:
                for match in PATRON_ABA.finditer(linea):
                    aba = match.group(1)
                    # Control de duplicados por ABA
                    if not show_dups and aba in vistos:
                        continue
                    vistos.add(aba)

                    # Buscar BIC a partir del final del match
                    pos = match.end()
                    # Omitir espacios tras ABA
                    while pos < len(linea) and linea[pos].isspace():
                        pos += 1

                    bic = ""
                    # Si el primer carácter no-espacio es letra, extraer 11 caracteres
                    if pos < len(linea) and linea[pos].isalpha():
                        bic = linea[pos:pos+11]
                    # Imprimir en formato ABA;BIC
                    print(f"{aba};{bic}")
    except FileNotFoundError:
        print(f"ERROR: No se encontró el fichero '{fichero}'.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    extrae_aba11(FICHERO, SHOW_DUPLICATES)
