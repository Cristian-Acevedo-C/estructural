"""Imprime una hoja del volcado en orden (fila, columna): celda | fórmula o constante | valor guardado.

Uso: python leer_hoja.py <volcado> "<hoja>" [fila_desde] [fila_hasta]
"""
import json
import re
import sys
from pathlib import Path

from openpyxl.utils import column_index_from_string


def clave(c: str):
    m = re.match(r"([A-Z]+)(\d+)", c)
    return int(m.group(2)), column_index_from_string(m.group(1))


def main() -> None:
    d = Path(sys.argv[1])
    hoja = sys.argv[2]
    desde = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    hasta = int(sys.argv[4]) if len(sys.argv) > 4 else 10**6
    cs = [c for c in json.loads((d / "celdas.json").read_text(encoding="utf-8")) if c["hoja"] == hoja]
    for c in sorted(cs, key=lambda c: clave(c["celda"])):
        f, _ = clave(c["celda"])
        if not desde <= f <= hasta:
            continue
        v = c["valor"]
        if isinstance(v, float):
            v = round(v, 6)
        if c["formula"]:
            print(f"{c['celda']:>6} = {c['formula'][1:] if c['formula'].startswith('=') else c['formula']}   → {v}")
        else:
            print(f"{c['celda']:>6} : {str(c['constante'])[:140]}")


if __name__ == "__main__":
    main()
