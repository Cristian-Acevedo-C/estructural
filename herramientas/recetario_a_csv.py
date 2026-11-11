"""Fase 6 · tablas del RECETARIO de ORBE, sin costos ni precios (uso interno). Solo lee.

Del libro (insumos/recetario_2026-11-11.xlsx) se toman SOLO medidas y pesos:
  - hoja RECETARIO: cañerías ISO R65 / ASTM A53 y tubos redondos (norma, pulgadas, Ø, espesor, kg por barra de 6 m);
  - hoja CUADRADOS: postes cuadrados (código, altura, perfil, canastillo, placa, peso);
  - hoja FACETADOS: postes facetados de 8 lados (código, largo, espesor, Ø inferior y superior, placa, pernos).
No se copian precios, costos, márgenes, valor por kilo ni proveedores.

Escribe:
  datos/tubos_recetario.csv, datos/postes_cuadrados_recetario.csv, datos/postes_facetados_recetario.csv
  docs/RECETARIO_CRUCE_generado.md  (cruce con datos/canerias.csv y hallazgos)
`datos/tubos.csv` NO se toca: lo genera catalogo_a_csv.py desde el catálogo maestro.

Uso (desde estructural/): .venv/Scripts/python herramientas/recetario_a_csv.py
"""
from __future__ import annotations

import csv
import hashlib
import re
import sys
import warnings
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
XLSX = RAIZ / "insumos" / "recetario_2026-11-11.xlsx"
NORMAS = ("ISO R65", "ASTM A53", "TUBO REDONDO")
TOL_PESO = 0.05  # diferencia relativa entre el kg/m del recetario y el teórico de un tubo de acero


def num(x):
    try:
        return float(str(x).replace(",", "."))
    except (TypeError, ValueError):
        return None


def kg_m_teorico(d_mm: float, e_mm: float) -> float:
    """Tubo de acero (7.850 kg/m³): π·(D − e)·e·7,85/1000."""
    return 0.0246615 * (d_mm - e_mm) * e_mm


def materiales(wb) -> list[dict]:
    ws = wb["RECETARIO"]
    out = []
    for fila in range(1, ws.max_row + 1):
        if ws.cell(fila, 3).value != "PULGADAS" or ws.cell(fila, 2).value not in NORMAS:
            continue
        r = fila + 1
        norma, pulg = ws.cell(r, 2).value, ws.cell(r, 3).value
        d, e, barra = num(ws.cell(r, 4).value), num(ws.cell(r, 5).value), num(ws.cell(r, 14).value)
        if norma is None or d is None or e is None:
            continue
        kg = barra / 6 if barra else None
        teo = kg_m_teorico(d, e) if d > e else None
        out.append({"fila": r, "norma": norma, "medida": str(pulg).strip(), "d": d, "e": e, "kg_barra_6m": barra, "kg_m": kg, "kg_m_teorico": teo,
                    "dif": (kg - teo) / teo if kg and teo else None})
    return out


def cuadrados(wb) -> list[dict]:
    out = []
    for f in wb["CUADRADOS"].iter_rows(min_row=2, values_only=True):
        cod, altura, medidas = f[0], num(f[2]), f[3]
        m = re.fullmatch(r"\s*(\d+)\s*[xX]\s*(\d+)\s*[xX]\s*(\d+(?:[.,]\d+)?)\s*", str(medidas or ""))
        if not cod or not str(cod).startswith("CU") or altura is None or not m:
            continue
        out.append({"codigo": cod, "altura_m": altura, "lado_mm": float(m.group(1)), "lado2_mm": float(m.group(2)), "espesor_mm": num(m.group(3)),
                    "canastillo": f[4], "placa": f[5], "peso_kg": num(f[7])})
    return out


def facetados(wb) -> list[dict]:
    out = []
    for f in wb["FACETADOS"].iter_rows(values_only=True):
        cod = f[14] if len(f) > 21 else None
        if not isinstance(cod, str) or not cod.startswith("FAC-"):
            continue
        e = re.fullmatch(r"\s*(\d+(?:[.,]\d+)?)\s*MM\s*", str(f[16] or ""), re.I)
        out.append({"codigo": cod, "altura_m": num(f[15]), "espesor_mm": num(e.group(1)) if e else None, "lados": num(f[17]),
                    "diametro_inferior_mm": num(f[18]), "diametro_superior_mm": num(f[19]), "placa": f[20], "pernos": f[21]})
    return out


def escribir(ruta: Path, campos: list[str], filas: list[dict]) -> None:
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        w.writerows(filas)


def main() -> int:
    import openpyxl

    warnings.filterwarnings("ignore")
    h = hashlib.sha256(XLSX.read_bytes()).hexdigest()
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    mats, cuad, fac = materiales(wb), cuadrados(wb), facetados(wb)
    fuente = f"{XLSX.name} (sha256 {h[:16]}…)"
    g = lambda x, n=4: None if x is None else round(x, n)  # noqa: E731

    # ---- tubos: solo los que tienen medidas coherentes con su peso
    tubos_ok, tubos_malos = [], []
    for m in (x for x in mats if x["norma"] == "TUBO REDONDO"):
        (tubos_ok if m["dif"] is not None and abs(m["dif"]) <= TOL_PESO else tubos_malos).append(m)
    escribir(RAIZ / "datos" / "tubos_recetario.csv",
             ["material_id", "norma", "medida", "diametro_ext_mm", "espesor_mm", "diametro_ext_cm", "espesor_cm", "kg_m", "largo_barra_m", "estado", "fuente"],
             [{"material_id": f"TUB-{m['d']:g}x{m['e']:g}".replace(".", "_"), "norma": "TUBO REDONDO", "medida": m["medida"], "diametro_ext_mm": m["d"], "espesor_mm": m["e"],
               "diametro_ext_cm": g(m["d"] / 10), "espesor_cm": g(m["e"] / 10), "kg_m": g(m["kg_m"]), "largo_barra_m": 6, "estado": "RECETARIO (sin confirmar en catálogo maestro)",
               "fuente": f"{fuente} RECETARIO fila {m['fila']}"} for m in tubos_ok])
    escribir(RAIZ / "datos" / "postes_cuadrados_recetario.csv", ["codigo", "altura_m", "lado_mm", "espesor_mm", "canastillo", "placa", "peso_kg", "fuente"],
             [{**c, "fuente": f"{fuente} CUADRADOS"} for c in cuad])
    escribir(RAIZ / "datos" / "postes_facetados_recetario.csv",
             ["codigo", "altura_m", "lados", "diametro_inferior_mm", "diametro_superior_mm", "espesor_mm", "placa", "pernos", "fuente"],
             [{**c, "fuente": f"{fuente} FACETADOS"} for c in fac])

    # ---- cruce de cañerías con el catálogo maestro
    with open(RAIZ / "datos" / "canerias.csv", encoding="utf-8") as f:
        cat = {(r["norma"], float(r["diametro_ext_mm"]), float(r["espesor_mm"])): r for r in csv.DictReader(f)}
    can = [m for m in mats if m["norma"] != "TUBO REDONDO"]
    iguales, distintas, solo_rec, vistos, dup = [], [], [], set(), []
    for m in can:
        k = (m["norma"], m["d"], m["e"])
        if k in vistos:
            dup.append(m)
            continue
        vistos.add(k)
        c = cat.get(k)
        if c is None:
            solo_rec.append(m)
        elif abs(float(c["kg_m"]) - m["kg_m"]) <= 0.006:
            iguales.append(m)
        else:
            distintas.append((m, c))
    solo_cat = [r for k, r in cat.items() if k not in vistos]
    peso_raro = [m for m in can if m["dif"] is not None and abs(m["dif"]) > TOL_PESO]

    def linea(m):
        return f"| {m['fila']} | {m['norma']} | {m['medida']} | {m['d']:g} | {m['e']:g} | {g(m['kg_m'], 3)} | {g(m['kg_m_teorico'], 3) if m['kg_m_teorico'] else '—'} | {'' if m['dif'] is None else f'{m['dif'] * 100:+.1f} %'} |"

    enc = ["| Fila | Norma | Medida | Ø (mm) | e (mm) | kg/m recetario | kg/m teórico | Diferencia |", "|---|---|---|---|---|---|---|---|"]
    md = [
        "# Cruce del RECETARIO con el catálogo maestro (generado)",
        "",
        f"Generado por `herramientas/recetario_a_csv.py` desde `insumos/{XLSX.name}` (sha256 `{h[:16]}…`). Uso interno.",
        "Solo medidas y pesos: no se copian precios, costos, márgenes ni valor por kilo.",
        "",
        "kg/m teórico = π·(Ø − e)·e·7,85/1000 (tubo de acero). Sirve para detectar medidas mal digitadas, no para reemplazar el dato de ORBE.",
        "",
        "## Resumen",
        "",
        f"- Hoja RECETARIO: {len(mats)} materiales ({len(can)} cañerías y {len(tubos_ok) + len(tubos_malos)} tubos redondos).",
        f"- Cañerías que coinciden con el catálogo maestro (Ø, espesor y kg/m): **{len(iguales)}**.",
        f"- Mismo Ø y espesor, distinto kg/m: **{len(distintas)}**.",
        f"- Están en el recetario y no en el catálogo (con ese Ø y espesor): **{len(solo_rec)}**.",
        f"- Están en el catálogo y no en el recetario: **{len(solo_cat)}**.",
        f"- Filas repetidas en el recetario: **{len(dup)}**.",
        f"- Tubos redondos con medidas coherentes: **{len(tubos_ok)}** (van a `datos/tubos_recetario.csv`). Con medidas incoherentes: **{len(tubos_malos)}** (no se cargan).",
        f"- Postes cuadrados: **{len(cuad)}** · postes facetados: **{len(fac)}**.",
        "",
        "## HALLAZGOS en el recetario (no se corrigió el archivo original)",
        "",
        "### Tubos redondos con medidas que no calzan con su peso (no se cargaron)",
        "",
        *enc, *[linea(m) for m in tubos_malos],
        "",
        "HIPÓTESIS: 1¾\" son 44,45 mm. El peso de la fila 191 calza con Ø44,45 × 1,5 y el de la fila 195 con Ø44,45 × 2,0: el diámetro quedó mal digitado. Confirmar con ORBE.",
        "",
        "### Cañerías del recetario que no están en el catálogo con ese Ø y espesor",
        "",
        *enc, *[linea(m) for m in solo_rec],
        "",
        "### Cañerías del catálogo que no están en el recetario",
        "",
        "| Material | Norma | Medida | Ø (mm) | e (mm) | kg/m |", "|---|---|---|---|---|---|",
        *[f"| {r['material_id']} | {r['norma']} | {r['medida']} | {r['diametro_ext_mm']} | {r['espesor_mm']} | {r['kg_m']} |" for r in solo_cat],
        "",
        "Lectura de las dos tablas anteriores (HIPÓTESIS, confirmar con ORBE):",
        "- ISO R65 1\": el recetario dice Ø26,67 (el mismo de ¾\") y el catálogo Ø33,4. El peso 1,98 kg/m calza con Ø33,4: error de digitación en el recetario.",
        "- ASTM A53 2½\": recetario Ø73,02 y catálogo Ø76,1, con el mismo espesor y peso. Ø73,02 es la medida nominal ASTM de 2½\".",
        "- ASTM A53 10\": recetario Ø273,5 y catálogo Ø273,05, con los mismos espesores y pesos. La medida nominal ASTM es 273,05.",
        "- ASTM A53 \"22\"\" con Ø610: 610 mm corresponde a 24\".",
        "",
        "### Cañerías cuyo peso se aleja más de 5 % del teórico",
        "",
        *enc, *[linea(m) for m in peso_raro],
        "",
        "### Filas repetidas",
        "",
        *enc, *[linea(m) for m in dup],
        "",
        "### Mismo Ø y espesor, distinto kg/m",
        "",
        *([f"- fila {m['fila']} {m['norma']} {m['medida']}: recetario {g(m['kg_m'], 3)} · catálogo {c['kg_m']}" for m, c in distintas] or ["Ninguna."]),
        "",
    ]
    (RAIZ / "docs" / "RECETARIO_CRUCE_generado.md").write_text("\n".join(md), encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(md[7:18]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
