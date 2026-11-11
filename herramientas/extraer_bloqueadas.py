"""Extrae qué celdas de ENTRADA del motor están bloqueadas (Locked) en las hojas protegidas de la planilla.

Con eso el motor avisa cuando una configuración cambia algo que la planilla no deja editar (Fase 3, hallazgo 1).
Solo lee la planilla con openpyxl, sin Excel. El 11-11-2026 se comprobó que estos flags coinciden con los que
reporta Excel por COM en las 12 hojas (herramientas/fase3_bloqueos.py).

Uso (desde estructural/): .venv/Scripts/python herramientas/extraer_bloqueadas.py
Escribe motor/modelo/bloqueadas_B.json.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import warnings
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from motor.validador import HOJAS, _modelo, mapa_hoja  # noqa: E402


def main() -> int:
    import openpyxl

    modelo, _ = _modelo()
    plantilla = RAIZ / "insumos" / modelo["origen"]["archivo"]
    sha = hashlib.sha256(plantilla.read_bytes()).hexdigest()
    if sha != modelo["origen"]["sha256"]:
        print("La plantilla no coincide con el modelo extraído")
        return 3
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wb = openpyxl.load_workbook(plantilla, keep_vba=False)
    hojas = {}
    for hoja in HOJAS.values():
        ws = wb[hoja]
        m = mapa_hoja(hoja)
        nombres = {c: k for k, c in m["entradas"].items() if isinstance(c, str) and re.fullmatch(r"[A-Z]+\d+", c)}
        for t in m["tramos"]:
            nombres.update({c: f"tramo.{k}" for k, c in t.items()})
        nombres.update({c: f"gancho.{k}" for k, c in m["gancho"].items()})
        nombres.update({c: "altura oculta" for c in m["alturas_ocultas"]})
        bloqueadas = {}
        if ws.protection.sheet:
            for c, nombre in sorted(nombres.items()):
                if ws[c].protection.locked:
                    bloqueadas[c] = {"entrada": nombre, "valor_planilla": modelo["celdas"][hoja].get(c, {}).get("v")}
        hojas[hoja] = {"protegida": bool(ws.protection.sheet), "bloqueadas": bloqueadas}
    salida = RAIZ / "motor" / "modelo" / "bloqueadas_B.json"
    salida.write_text(json.dumps({"origen": {"archivo": modelo["origen"]["archivo"], "sha256": sha}, "hojas": hojas}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{salida.relative_to(RAIZ)}: {sum(len(h['bloqueadas']) for h in hojas.values())} entradas bloqueadas en {sum(h['protegida'] for h in hojas.values())} hojas protegidas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
