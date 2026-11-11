"""Extrae de una plantilla .xlsm las celdas (fórmulas y constantes) que usa el motor, y los valores que Excel dejó
guardados (para probar el intérprete). Solo lee la plantilla.

Uso (desde estructural/):
  python -m motor.extraer insumos/plantilla_B_2026-10-21.xlsm motor/modelo/plantilla_B.json motor/modelo/guardados_B.json
"""
from __future__ import annotations

import hashlib
import json
import sys
import warnings
from datetime import date
from pathlib import Path

import openpyxl
from openpyxl.worksheet.formula import ArrayFormula


def _plano(v):
    if hasattr(v, "isoformat"):
        return v.isoformat()
    return v


def extraer(xlsm: Path) -> tuple[dict, dict]:
    warnings.filterwarnings("ignore")
    wf = openpyxl.load_workbook(xlsm, data_only=False, keep_vba=False)
    wv = openpyxl.load_workbook(xlsm, data_only=True, keep_vba=False)
    celdas: dict[str, dict] = {}
    guardados: dict[str, dict] = {}
    for ws in wf.worksheets:
        hoja = {}
        guard = {}
        for fila in ws.iter_rows():
            for c in fila:
                v = c.value
                if v is None:
                    continue
                if isinstance(v, ArrayFormula):
                    hoja[c.coordinate] = {"f": v.text if v.text.startswith("=") else "=" + v.text, "matricial": v.ref}
                elif isinstance(v, str) and v.startswith("=") and v.strip() != "=":  # "=" solo es texto en Excel
                    hoja[c.coordinate] = {"f": v}
                else:
                    hoja[c.coordinate] = {"v": _plano(v)}
                gv = wv[ws.title][c.coordinate].value
                guard[c.coordinate] = _plano(gv)
        celdas[ws.title] = hoja
        guardados[ws.title] = guard
    h = hashlib.sha256(xlsm.read_bytes()).hexdigest()
    origen = {"archivo": xlsm.name, "sha256": h, "extraido": date.today().isoformat()}
    return {"origen": origen, "celdas": celdas}, {"origen": origen, "valores": guardados}


if __name__ == "__main__":
    modelo, guardados = extraer(Path(sys.argv[1]))
    Path(sys.argv[2]).parent.mkdir(parents=True, exist_ok=True)
    Path(sys.argv[2]).write_text(json.dumps(modelo, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    Path(sys.argv[3]).write_text(json.dumps(guardados, ensure_ascii=False, separators=(",", ":"), default=str), encoding="utf-8")
    print(f"{modelo['origen']['archivo']}: {sum(len(h) for h in modelo['celdas'].values())} celdas en {len(modelo['celdas'])} hojas")
