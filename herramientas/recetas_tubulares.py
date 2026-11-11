"""Recetas de tubulares del RECETARIO (receta vigente según ORBE, 11-11-2026): geometría y costo.

Lee la hoja TUBULARES de insumos/recetario_2026-11-11b.xlsx. Cada bloque CODIGO trae los cuerpos ("Ø*e*largo de corte"),
la placa, los pernos, los atiezadores, las tarifas de acero y de galvanizado, y los insumos.
- **Largo visible:** el de corte en la base; el corte − 200 mm (embute) en los cuerpos siguientes. Con esa regla, las
  recetas de 7 a 15 m suman su altura.
- **Peso de cañería:** kg/m de datos/canerias.csv o datos/tubos_recetario.csv. Si la medida no está en esas tablas, el
  teórico π·(Ø − e)·e·7,85/1000.
- **Costo:** se recalcula con las partidas de la misma receta (placa, pernos, atiezadores, insumos) más
  acero = kg × tarifa de la receta y galvanizado = (cañerías + placa + atiezadores) kg × 490 $/kg (valor confirmado por
  ORBE). Así se reemplazan los #ERROR! del archivo. Donde el recetario sí trae su COSTO, se informa la diferencia.
Uso: from recetas_tubulares import recetas
"""
from __future__ import annotations

import csv
import re
import warnings
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
XLSX = RAIZ / "insumos" / "recetario_2026-11-11b.xlsx"
EMBUTE_MM = 200
GALVA_KG = 490
ATIEZADOR_KG = 0.8
SEG = re.compile(r"^\s*([\d.,]+)\s*\*\s*([\d.,]+)\s*\*\s*(\d+)\s*$")
# medidas mal digitadas en el recetario (hoja REVISAR, puntos 11 a 13): se corrigen para calcular y la receta queda marcada
CORRECCIONES = {(58.8, 2.0): (50.8, 2.0), (114.6, 3.6): (114.3, 3.6), (114.3, 3.0): (114.3, 3.6)}
PLACAS_KG = {"200*200*10": 3.14, "240*240*10": 4.91, "250*250*10": 4.91, "300*300*12": 8.48, "340*340*12": 10.74, "340*340*20": 18.15}


def _num(x):
    try:
        # en los valores guardados del recetario la coma es separador de miles ("$ 11,920") y el punto es decimal ("29.3")
        return float(str(x).replace("$", "").replace("CLP", "").replace(",", "").strip()) if not isinstance(x, (int, float)) else float(x)
    except ValueError:
        return None


def _kg_m_tablas():
    t = {}
    for archivo in ("datos/canerias.csv", "datos/tubos_recetario.csv"):
        with open(RAIZ / archivo, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                t[(round(float(r["diametro_ext_mm"]), 1), round(float(r["espesor_mm"]), 2))] = (float(r["kg_m"]), r["norma"])
    return t


def _kg_m(d, e, tabla):
    for dd in (d, round(d - 0.02, 2), round(d + 0.02, 2), round(d - 0.03, 2)):
        if (round(dd, 1), round(e, 2)) in tabla:
            return tabla[(round(dd, 1), round(e, 2))][0], "tabla"
    return 0.0246615 * (d - e) * e, "teórico"


def _valor(ws_f, ws_v, fila, col):
    """Valor de una partida: el guardado; si es error, la fórmula simple N*celda o N*M."""
    v = _num(ws_v.cell(fila, col).value)
    if v is not None:
        return v
    f = str(ws_f.cell(fila, col).value or "")
    m = re.fullmatch(r"=\s*([\d.]+)\s*\*\s*\$?([A-Z]+)\$?(\d+)", f)
    if m:
        q = _num(ws_v[f"{m.group(2)}{m.group(3)}"].value)
        return float(m.group(1)) * (q or 0)
    m = re.fullmatch(r"=\s*([\d.]+)\s*\*\s*([\d.]+)", f)
    if m:
        return float(m.group(1)) * float(m.group(2))
    return None


def recetas() -> list[dict]:
    import openpyxl

    warnings.filterwarnings("ignore")
    wf, wv = openpyxl.load_workbook(XLSX), openpyxl.load_workbook(XLSX, data_only=True)
    sf, sv = wf["TUBULARES"], wv["TUBULARES"]
    tabla = _kg_m_tablas()
    out = []
    for fila in sf.iter_rows():
        for c in fila:
            if c.value != "CODIGO":
                continue
            r0, col = c.row, c.column
            codigo = sf.cell(r0, col + 2).value
            titulo = " ".join(str(sf.cell(r, col).value or "") for r in (r0 + 1, r0 + 2) if sf.cell(r, col).value not in (None, "ALTURA", "Ficha tecnica"))
            cuerpos, partidas, placa, perno, notas = [], [], None, None, []
            acero_tarifa, costo_recetario, n_atiez = 750.0, None, 4
            for r in range(r0 + 2, r0 + 45):
                lab = sf.cell(r, col).value
                labs = str(lab or "").strip()
                if lab == "CODIGO":
                    break
                if labs == "COSTO":
                    costo_recetario = _num(sv.cell(r, col + 2).value)
                    break
                m = SEG.match(labs)
                if m and not re.fullmatch(r"\d+\*\d+\*\d+", labs.replace(",", "").replace(".", "")) or (m and len(cuerpos) < 6 and float(m.group(3).replace(",", ".")) > 60 and _num(m.group(1).replace(",", ".")) and float(m.group(1).replace(",", ".")) < 200 and labs.count("*") == 2 and not labs.startswith(("200*", "240*", "250*", "300*", "340*"))):
                    d, e, largo = float(m.group(1).replace(",", ".")), float(m.group(2).replace(",", ".")), float(m.group(3))
                    if (d, e) in CORRECCIONES:
                        notas.append(f"Cuerpo {labs} corregido a Ø{CORRECCIONES[(d, e)][0]}×{CORRECCIONES[(d, e)][1]} (dato del recetario dudoso)")
                        d, e = CORRECCIONES[(d, e)]
                    kgm, origen = _kg_m(d, e, tabla)
                    cuerpos.append({"D_mm": d, "e_mm": e, "corte_mm": largo, "kg_m": round(kgm, 4), "kg_m_origen": origen})
                    continue
                if re.fullmatch(r"\d+[\*xX]\d+[\*xX]\d+", labs):  # placa: "250*250*10" o "200x200x10"
                    labs = re.sub(r"[xX]", "*", labs)
                    placa = labs
                    partidas.append([f"Placa {labs.replace('*', '×')}", _valor(sf, sv, r, col + 2)])
                elif re.fullmatch(r"\d+/\d+\s*[\*xX]\s*\d+", labs):
                    perno = labs
                    q = _num(sv.cell(r, col + 1).value) or 4
                    partidas.append([f"{int(q)} pernos {labs.split('*')[0].split('x')[0].split('X')[0]}\"", _valor(sf, sv, r, col + 2)])
                elif labs.upper() == "ATIEZADOR" or (lab is None and _num(sv.cell(r, col + 1).value) in (2.0, 4.0) and _num(sv.cell(r, col + 2).value) in (1440.0, 2000.0)):
                    n_atiez = int(_num(sv.cell(r, col + 1).value) or 4)
                    partidas.append([f"{n_atiez} atiezadores", _valor(sf, sv, r, col + 2)])
                elif labs.upper() == "ACERO":
                    acero_tarifa = _num(sv.cell(r, col + 1).value) or 750.0
                elif labs.upper() in ("TAPA DE REGISTRO", "PERNOS DE TAPA", "RIEL DIEN", "DISCO DE CORTE", "DISCO DESBASTE", "DISCO TRONZADORA", "TAPA DE PUNTA", "GAS MIG", "ALAMBRE MIG", "OTROS INSUMOS", "MANO OBRA"):
                    v = _valor(sf, sv, r, col + 2)
                    if v:
                        partidas.append([labs.capitalize(), v])
            if not cuerpos:
                continue
            visibles = [cu["corte_mm"] if i == 0 else cu["corte_mm"] - EMBUTE_MM for i, cu in enumerate(cuerpos)]
            if min(visibles) <= 0:
                notas.append("Algún cuerpo es más corto que el embute de 200 mm: revisar la receta")
            for cu, v in zip(cuerpos, visibles):
                cu["visible_mm"] = max(v, 1)
            kg_acero = sum(cu["kg_m"] * cu["corte_mm"] / 1000 for cu in cuerpos)
            kg_placa = PLACAS_KG.get(placa or "", 0.0)
            kg_galv = kg_acero + kg_placa + n_atiez * ATIEZADOR_KG
            partidas = [p for p in partidas if p[1] is not None]
            costo = sum(p[1] for p in partidas) + kg_acero * acero_tarifa + kg_galv * GALVA_KG
            if any(cu["kg_m_origen"] == "teórico" for cu in cuerpos):
                notas.append("Peso de alguna cañería o tubo calculado con la fórmula teórica (la medida no está en las tablas)")
            altura = sum(visibles) / 1000
            out.append({"codigo": codigo, "titulo": titulo.strip(), "altura_m": round(altura, 2), "cuerpos": cuerpos, "placa": placa, "perno": perno,
                        "kg_acero": round(kg_acero, 2), "kg_galvanizado": round(kg_galv, 2), "acero_tarifa": acero_tarifa,
                        "partidas": [[l, round(v)] for l, v in partidas] + [[f"Acero ({kg_acero:.2f} kg × ${acero_tarifa:,.0f})".replace(",", "."), round(kg_acero * acero_tarifa)],
                                                                         [f"Galvanizado ({kg_galv:.2f} kg × ${GALVA_KG})", round(kg_galv * GALVA_KG)]],
                        "costo": round(costo), "costo_recetario": costo_recetario, "notas": notas})
    return out


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")
    rs = recetas()
    for r in rs:
        dif = f"{(r['costo'] / r['costo_recetario'] - 1) * 100:+.1f} %" if r["costo_recetario"] else "—"
        print(f"{r['codigo']:9} {r['altura_m']:5.2f} m {len(r['cuerpos'])} cuerpos · costo {r['costo']:>8,} · recetario {r['costo_recetario'] or '#ERROR!':>9} ({dif}) {'· ' + '; '.join(r['notas']) if r['notas'] else ''}")
    print(len(rs), "recetas")
