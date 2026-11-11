"""Accesorios del RECETARIO (hoja ACCESORIOS) para el cotizador. Uso interno: trae costos.

Cada fila con código (AC1…AC92, L150, L400) pasa a un accesorio con grupo, nombre, detalle, peso y costo sin IVA.
- **Sin precio:** costo 0 en el recetario, o costo incompleto (solo galvanizado, sin cañería: AC5 a AC8). Se listan
  para que se sepa que existen, pero no se pueden cotizar.
- **fuera_eje:** brazos, ganchos, crucetas y coronas alejan el equipo del eje del poste; la planilla no calcula ese
  esfuerzo, así que cualquier cotización que los lleve va a revisión técnica.
Uso: from accesorios_recetario import accesorios
"""
from __future__ import annotations

import re
import warnings
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
XLSX = RAIZ / "insumos" / "recetario_2026-11-11b.xlsx"
GRUPOS = [  # (patrón del título de la sección, grupo que se muestra, fuera del eje)
    (r"BRAZOS RECTOS", "Brazos rectos", True), (r"GANCHOS CURVOS", "Ganchos curvos", True), (r"CRUCETAS", "Crucetas", True),
    (r"CORONAS", "Coronas", True), (r"^CANASTILLO", "Canastillos de anclaje", False), (r"^PLACA \+ CANASTILLO", "Placa + canastillo", False),
    (r"^PLACA", "Placas base", False), (r"BRAZO POSTE HORMIGON", "Brazos para poste de hormigón", True), (r"BRAZO PARA CAMARA", "Brazos para cámara", True),
]


def _num(x):
    if isinstance(x, (int, float)):
        return float(x)
    try:
        return float(str(x).replace("$", "").replace(",", "").replace("-", "").strip() or 0)
    except ValueError:
        return None


def accesorios() -> list[dict]:
    import openpyxl

    warnings.filterwarnings("ignore")
    ws = openpyxl.load_workbook(XLSX, data_only=True)["ACCESORIOS"]
    out, grupo, fuera, ancho = [], None, False, False
    for f in ws.iter_rows(values_only=True):
        cod, nom = f[0], f[1]
        if isinstance(nom, str) and (cod is None or str(cod).strip().upper() == "CODIGO") and not re.match(r"^(AC|L)\d+", str(cod or ""), re.I):
            titulo = nom.strip().upper().replace("ACCESORIOS ", "")
            for patron, g, fe in sorted(GRUPOS, key=lambda x: -len(x[0])):
                if re.search(patron, titulo):
                    grupo, fuera = g, fe
                    break
            ancho = "PESO" in [str(x).strip().upper() for x in f[7:9] if x]  # secciones con columnas PESO/CAÑERIA/GALVA/COSTO
            continue
        if not isinstance(cod, str) or not re.match(r"^(AC|L)\d+$", cod.strip(), re.I) or not grupo:
            continue
        cod = cod.strip().upper()
        if ancho:
            detalle, peso, caneria, galva, costo = f[4], _num(f[8]), _num(f[9]), _num(f[10]), _num(f[11])
            incompleto = bool(costo) and not caneria and bool(galva)   # solo trae el galvanizado
        else:
            detalle, peso, caneria, galva, costo, incompleto = None, None, None, None, _num(f[4]), False
        nombre = str(nom).strip().capitalize() if nom else cod
        item = {"codigo": cod, "grupo": grupo, "nombre": nombre, "detalle": str(detalle).strip() if detalle else "", "peso_kg": peso or None,
                "costo": round(costo) if costo and not incompleto else None, "fuera_eje": fuera}
        if not costo:
            item["nota"] = "Sin costo en el recetario"
        elif incompleto:
            item["nota"] = "Costo incompleto en el recetario (falta la cañería)"
        elif fuera and not peso:
            item["nota"] = "Sin peso en el recetario"
        out.append(item)
    # Brazos rectos y ganchos curvos: las hojas propias traen el costo completo (cañerías, galvanizado, pernos, tapa,
    # mano de obra e insumos). Reemplazan a los AC1–AC40 de la hoja ACCESORIOS, que solo traen cañería y galvanizado
    # (o $0) y darían un segundo precio, más bajo, para el mismo producto.
    det = detallados()
    if det:
        out = [a for a in out if a["grupo"] not in ("Brazos rectos", "Ganchos curvos")]
        out = det + out
    return out


def detallados() -> list[dict]:
    """Recetas de las hojas BRAZOS RECTOS y GANCHOS CURVOS (bloques CODIGO … COSTO)."""
    import openpyxl

    wb = openpyxl.load_workbook(XLSX, data_only=True)
    out, vistos = [], set()
    for hoja, grupo in (("BRAZOS RECTOS", "Brazos rectos"), ("GANCHOS CURVOS", "Ganchos curvos")):
        ws = wb[hoja]
        for fila in ws.iter_rows():
            for c in fila:
                if c.value != "CODIGO":
                    continue
                nombre = str(ws.cell(c.row + 1, c.column).value or "").strip()
                partes, peso, costo = [], None, None
                for r in range(c.row + 2, c.row + 22):
                    lab = ws.cell(r, c.column).value
                    if lab == "CODIGO":
                        break
                    if isinstance(lab, str) and "*" in lab:
                        partes.append((lab.strip(), _num(ws.cell(r, c.column + 2).value)))
                    elif lab == "PESO":
                        peso = _num(ws.cell(r, c.column + 3).value)
                    elif lab == "COSTO":
                        costo = _num(ws.cell(r, c.column + 3).value)
                        break
                if not nombre or not partes:
                    continue
                # código a partir del nombre (el de la hoja se repite): "BRAZO RECTO 2*1500" → BR2*1500; se agrega la cañería del brazo
                base = re.sub(r"^BRAZO RECTO\s*", "BR", nombre.upper())
                base = re.sub(r"^GANCHO CURVO\s*", "GC", base).replace(" ", "")
                cano = partes[-1][0].split("*")[0].replace(",", ".")
                pulg = {"48.26": '1,5"', "60.3": '2"'}.get(cano, f"Ø{cano}")
                codigo = f"{base}-{pulg.replace(',', '.').replace(chr(34), '')}" if grupo == "Brazos rectos" else base
                n = 2
                while codigo in vistos:   # nunca dos accesorios con el mismo código
                    codigo, n = f"{codigo.split('#')[0]}#{n}", n + 1
                vistos.add(codigo)
                malo = not costo or not peso or peso > 200 or costo > 1_000_000   # p. ej. manguito de 11.994 kg en 3 recetas
                item = {"codigo": codigo, "grupo": grupo, "nombre": nombre.capitalize().replace("*", " × "),
                        "detalle": f"cañería {pulg} · " + " + ".join(f"{p[0].replace('*', '×')}{'' if p[0].count('*') > 1 else '×' + format(p[1], 'g')}" for p in partes),
                        "peso_kg": None if malo else round(peso, 2), "costo": None if malo else round(costo), "fuera_eje": True}
                if malo:
                    item["nota"] = "Valores imposibles en el recetario (peso o costo): revisar la receta"
                out.append(item)
    return out


if __name__ == "__main__":
    import sys
    from collections import Counter

    sys.stdout.reconfigure(encoding="utf-8")
    acc = accesorios()
    for a in acc:
        print(f"{a['codigo']:5} {a['grupo']:30} {a['nombre'][:28]:28} {a['detalle'][:24]:24} peso {a['peso_kg'] or '—':>6} costo {a['costo'] or '—':>7} {a.get('nota', '')}")
    print(len(acc), "accesorios ·", sum(1 for a in acc if a["costo"]), "con costo ·", dict(Counter(a["grupo"] for a in acc)))
