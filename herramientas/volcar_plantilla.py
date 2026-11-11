"""Vuelca una plantilla .xlsm a JSON y texto para la ingeniería inversa (Fase 1). Solo lee.

Uso: python volcar_plantilla.py <archivo.xlsm> <carpeta_salida>

Deja en la carpeta:
  celdas.json      todas las celdas no vacías: hoja, celda, fórmula (si tiene), valor calculado guardado, formato
  hojas.json       hojas, dimensiones, estado (visible/oculta), celdas combinadas
  nombres.json     nombres definidos (rangos con nombre)
  validaciones.json validaciones de datos (listas, rangos permitidos) por hoja
  meta.json        propiedades del archivo (autor, fechas, última modificación)
  vba.txt          código VBA extraído con oletools (olevba)
"""
import json
import sys
from pathlib import Path

import openpyxl
from openpyxl.worksheet.formula import ArrayFormula
from oletools.olevba import VBA_Parser


def volcar(ruta: Path, salida: Path) -> None:
    salida.mkdir(parents=True, exist_ok=True)
    # dos lecturas: una con fórmulas, otra con los valores que Excel guardó al último cálculo
    wf = openpyxl.load_workbook(ruta, data_only=False, keep_vba=True)
    wv = openpyxl.load_workbook(ruta, data_only=True, keep_vba=True)

    p = wf.properties
    meta = {
        "archivo": ruta.name,
        "creador": p.creator,
        "ultimo_modificado_por": p.lastModifiedBy,
        "creado": str(p.created) if p.created else None,
        "modificado": str(p.modified) if p.modified else None,
        "titulo": p.title,
        "revision": p.revision,
    }

    hojas, celdas, validaciones = [], [], []
    for ws in wf.worksheets:
        wsv = wv[ws.title]
        hojas.append(
            {
                "hoja": ws.title,
                "estado": ws.sheet_state,
                "dimension": ws.dimensions,
                "max_fila": ws.max_row,
                "max_col": ws.max_column,
                "combinadas": [str(r) for r in ws.merged_cells.ranges],
            }
        )
        for fila in ws.iter_rows():
            for c in fila:
                if c.value is None:
                    continue
                v = wsv[c.coordinate].value
                matricial = isinstance(c.value, ArrayFormula)
                es_formula = matricial or (isinstance(c.value, str) and c.value.startswith("="))
                texto_formula = (f"{{{c.value.text}}} (matricial {c.value.ref})" if matricial else c.value) if es_formula else None
                celdas.append(
                    {
                        "hoja": ws.title,
                        "celda": c.coordinate,
                        "formula": texto_formula,
                        "valor": v if not hasattr(v, "isoformat") else v.isoformat(),
                        "constante": None if es_formula else (c.value if not hasattr(c.value, "isoformat") else c.value.isoformat()),
                        "formato": c.number_format,
                    }
                )
        for dv in ws.data_validations.dataValidation:
            validaciones.append(
                {
                    "hoja": ws.title,
                    "rango": str(dv.sqref),
                    "tipo": dv.type,
                    "operador": dv.operator,
                    "formula1": dv.formula1,
                    "formula2": dv.formula2,
                    "mensaje": dv.prompt,
                    "error": dv.error,
                }
            )

    nombres = []
    for nombre, dn in wf.defined_names.items():
        nombres.append({"nombre": nombre, "destino": dn.attr_text, "ambito": "libro"})
    for ws in wf.worksheets:
        for nombre, dn in ws.defined_names.items():
            nombres.append({"nombre": nombre, "destino": dn.attr_text, "ambito": ws.title})

    vba = []
    parser = VBA_Parser(str(ruta))
    if parser.detect_vba_macros():
        for (_archivo, _flujo, modulo, codigo) in parser.extract_macros():
            vba.append(f"' ===== módulo: {modulo} =====\n{codigo}\n")
    parser.close()

    (salida / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    (salida / "hojas.json").write_text(json.dumps(hojas, ensure_ascii=False, indent=2), encoding="utf-8")
    (salida / "celdas.json").write_text(json.dumps(celdas, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    (salida / "nombres.json").write_text(json.dumps(nombres, ensure_ascii=False, indent=2), encoding="utf-8")
    (salida / "validaciones.json").write_text(json.dumps(validaciones, ensure_ascii=False, indent=2), encoding="utf-8")
    (salida / "vba.txt").write_text("\n".join(vba) or "(sin VBA)\n", encoding="utf-8")
    print(f"{ruta.name}: {len(hojas)} hojas, {len(celdas)} celdas, {sum(1 for c in celdas if c['formula'])} fórmulas, {len(nombres)} nombres, {len(validaciones)} validaciones, {len(vba)} módulos VBA")


if __name__ == "__main__":
    volcar(Path(sys.argv[1]), Path(sys.argv[2]))
