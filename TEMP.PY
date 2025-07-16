#!/usr/bin/env python3
import re
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Extrae una columna de un fichero de texto con columnas separadas por N espacios."
    )
    parser.add_argument("fichero", help="Ruta al fichero de texto")
    parser.add_argument(
        "columna",
        type=int,
        help="Número de columna a extraer (1 = primera columna, 2 = segunda, …)",
    )
    parser.add_argument(
        "--espacios",
        type=int,
        default=2,
        help="Mínimo de espacios que definen el separador (por defecto: 2)",
    )
    args = parser.parse_args()

    # Construimos el patrón: al menos N espacios seguidos
    patron = re.compile(rf"\s{{{args.espacios},}}")

    try:
        with open(args.fichero, encoding="utf-8") as f:
            for linea in f:
                linea = linea.rstrip("\n")
                # Partimos la línea usando el patrón
                campos = patron.split(linea)
                idx = args.columna - 1
                if 0 <= idx < len(campos):
                    print(campos[idx])
                else:
                    # Si no hay ese campo, imprimimos vacío o un warning:
                    print("", file=sys.stderr)
    except FileNotFoundError:
        print(f"ERROR: No existe el fichero {args.fichero}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

