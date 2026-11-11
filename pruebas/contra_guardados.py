"""Evalúa con el intérprete TODAS las fórmulas de una plantilla, sin cambiar ninguna entrada, y las compara con los
valores que Excel dejó guardados en el archivo. Si el intérprete replica bien a Excel, deben coincidir.

Uso (desde estructural/): python pruebas/contra_guardados.py A|B [tolerancia_relativa=1e-9]
"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "motor"))
from excel import Libro, es_error  # noqa: E402


def iguales(a, b, tol):
    if es_error(a):
        return isinstance(b, str) and b == a.codigo
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if math.isclose(a, b, rel_tol=tol, abs_tol=1e-9):
            return True
        return False
    if a is None and b in (None, ""):
        return True
    if isinstance(a, str) and isinstance(b, str):
        return a == b
    if isinstance(a, float) and b is None:
        return a == 0
    return a == b


def main(version: str, tol: float = 1e-9) -> int:
    modelo = json.loads((RAIZ / f"motor/modelo/plantilla_{version}.json").read_text(encoding="utf-8"))
    guard = json.loads((RAIZ / f"motor/modelo/guardados_{version}.json").read_text(encoding="utf-8"))["valores"]
    libro = Libro(modelo["celdas"])
    calc = libro.calculo()
    total, malas = 0, []
    por_hoja = Counter()
    for hoja, celdas in modelo["celdas"].items():
        for celda, c in celdas.items():
            if c.get("f") is None:
                continue
            total += 1
            try:
                v = calc.valor(hoja, celda)
            except Exception as e:  # noqa: BLE001
                v = f"EXCEPCIÓN {type(e).__name__}: {e}"
            g = guard[hoja].get(celda)
            if not iguales(v, g, tol):
                malas.append((hoja, celda, c["f"][:90], v, g))
                por_hoja[hoja] += 1
    print(f"versión {version}: {total} fórmulas, {total - len(malas)} coinciden con lo guardado por Excel, {len(malas)} no")
    for h, n in por_hoja.most_common():
        print(f"  {h}: {n}")
    for m in malas[:40]:
        print("  ", m)
    return 1 if malas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 1e-9))
