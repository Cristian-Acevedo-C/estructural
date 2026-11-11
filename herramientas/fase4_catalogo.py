"""Fase 4 · capacidad de los tubulares del catálogo REV. M según la planilla (uso interno).

No se inventan cargas de diseño. Para cada poste (geometría verificada contra los planos, ver
fuentes/planos_tubulares_revM/VERIFICACION_PDF.md) y para cada velocidad de viento, se calcula:
  - base: ¿cumple con su propio viento y la cabeza de referencia, sin fuerza adicional en la punta?
  - V máx: la mayor fuerza horizontal ADICIONAL en la punta (kg) con la que la planilla dice "cumple";
  - qué verificación manda en ese límite (la de mayor razón de uso).
Cabeza de referencia: proyectores de 10 × 26 cm y P = 20 kg, el caso que la planilla trae guardado en
"P.Var.2 Tramos Circ." en las versiones A y B. No es una carga de diseño de ORBE. Se usa porque la planilla NO puede
evaluar un poste sin proyectores: la torsión divide por alto × ancho de los proyectores (F160) y da #DIV/0!.
Supuestos (los de la planilla salvo que se diga): Fy 2.400 kg/cm², 4 pernos (planos), coeficientes por omisión.
El largo de cada tramo es el VISIBLE del plano; la planilla no modela el embute (traslapo de 100 o 200 mm).
Postes de 5 cuerpos: fuera del alcance de la planilla (admite hasta 4 tramos).

Uso (desde estructural/): .venv/Scripts/python herramientas/fase4_catalogo.py
Escribe trabajo/fase4/capacidad_catalogo.json y docs/FASE4_CAPACIDAD_generado.md.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from motor.validador import validar  # noqa: E402

CSV = RAIZ / "fuentes" / "planos_tubulares_revM" / "catalogo_tubulares_revM_transcrito.csv"
VELOCIDADES = (100, 120, 140)
V_TOPE = 2000.0  # kg: si cumple aún aquí, se informa "> 2.000"
PASO = 0.5  # kg: precisión de la bisección


def postes() -> dict[str, list[dict]]:
    out = defaultdict(list)
    with open(CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out[r["codigo"]].append(r)
    for c in out.values():
        c.sort(key=lambda r: int(r["posicion_desde_base"]))
    return dict(out)


CABEZA = {"alto_cm": 10, "ancho_cm": 26}
P_REFERENCIA_KG = 20.0


def config(cuerpos: list[dict], velocidad: float, v_kg: float, p_kg: float = P_REFERENCIA_KG) -> dict:
    return {
        "_origen": "fase4_catalogo.py",
        "seccion": "circular",
        "ganchos": 0,
        "orden_tramos": "desde_base",
        "tramos": [{"altura_m": float(c["visible_mm"]) / 1000, "diametro_cm": float(c["D_mm"]) / 10, "espesor_cm": float(c["e_mm"]) / 10} for c in cuerpos],
        "sobrecarga_kg": p_kg,
        "viento_tablero_kg": v_kg,
        "viento": {"velocidad_kmh": velocidad},
        "proyectores": dict(CABEZA),
        "pernos": 4,
    }


def manda(r: dict) -> dict | None:
    vs = [v for v in r["verificaciones"] if v["estado"] in ("cumple", "no cumple") and isinstance(v.get("razon_de_uso"), (int, float))]
    return max(vs, key=lambda v: v["razon_de_uso"]) if vs else None


def capacidad(cuerpos: list[dict], velocidad: float) -> dict:
    r0 = validar(config(cuerpos, velocidad, 0.0))
    m0 = manda(r0)
    res = {"velocidad_kmh": velocidad, "base": r0["resumen"], "manda_sin_carga": m0["nombre"] if m0 else None, "razon_sin_carga": round(m0["razon_de_uso"], 3) if m0 else None}
    if r0["resumen"] != "cumple":
        estado = "error" if r0["resumen"] == "error" else "no cumple"
        res.update({"v_max_kg": None, "nota": f"{estado} sin fuerza adicional en la punta",
                    "falla": [f"{v['nombre']} ({v['estado']}: {v['mensaje_planilla']})" for v in r0["verificaciones"] if v["estado"] in ("no cumple", "error")]})
        return res
    if validar(config(cuerpos, velocidad, V_TOPE))["resumen"] == "cumple":
        res.update({"v_max_kg": f"> {V_TOPE:g}"})
        return res
    lo, hi = 0.0, V_TOPE
    while hi - lo > PASO:
        mid = (lo + hi) / 2
        if validar(config(cuerpos, velocidad, mid))["resumen"] == "cumple":
            lo = mid
        else:
            hi = mid
    # comprobación de monotonía: en una grilla de 0 a lo, todos cumplen; sobre hi, ninguno
    grilla = [lo * k / 10 for k in range(11)]
    monotono = all(validar(config(cuerpos, velocidad, v))["resumen"] == "cumple" for v in grilla) and all(
        validar(config(cuerpos, velocidad, hi + d))["resumen"] != "cumple" for d in (0, 10, 50)
    )
    r = validar(config(cuerpos, velocidad, hi))
    m = manda(r)
    res.update({"v_max_kg": round(lo, 1), "monotono": monotono, "manda_en_limite": m["nombre"] if m else None})
    return res


def main() -> int:
    salida = RAIZ / "trabajo" / "fase4"
    salida.mkdir(parents=True, exist_ok=True)
    resultado = {}
    for codigo, cuerpos in sorted(postes().items(), key=lambda kv: (int(kv[0].split("M")[0]), kv[0])):
        info = {"altura_mm": int(cuerpos[0]["altura_armada_mm"]), "cuerpos": len(cuerpos), "peso_canerias_kg": float(cuerpos[0]["peso_canerias_declarado_kg"]),
                "base": f"Ø{cuerpos[0]['D_mm']}×{cuerpos[0]['e_mm']}"}
        if len(cuerpos) > 4:
            info["fuera_de_alcance"] = "5 cuerpos: la planilla admite hasta 4 tramos"
        else:
            info["capacidad"] = [capacidad(cuerpos, v) for v in VELOCIDADES]
        resultado[codigo] = info
    (salida / "capacidad_catalogo.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=1), encoding="utf-8")

    filas = []
    for codigo, i in resultado.items():
        if "fuera_de_alcance" in i:
            filas.append(f"| {codigo} | {i['altura_mm'] / 1000:g} | {i['cuerpos']} | {i['base']} | {i['peso_canerias_kg']:g} | fuera del alcance de la planilla (5 cuerpos) | | | |")
            continue
        celdas = []
        for c in i["capacidad"]:
            if c["base"] != "cumple":
                celdas.append("**error de la planilla**" if c["base"] == "error" else "**no cumple sin fuerza adicional**")
            else:
                celdas.append(f"{c['v_max_kg']}" + ("" if c.get("monotono", True) else " (¡no monótono!)"))
        manda120 = next(c for c in i["capacidad"] if c["velocidad_kmh"] == 120)
        manda_txt = manda120.get("manda_en_limite") or ", ".join(manda120.get("falla", [])) or "—"
        filas.append(f"| {codigo} | {i['altura_mm'] / 1000:g} | {i['cuerpos']} | {i['base']} | {i['peso_canerias_kg']:g} | {' | '.join(celdas)} | {manda_txt} |")
    md = [
        "# Capacidad de los tubulares REV. M según la planilla (generado)",
        "",
        "Generado por `herramientas/fase4_catalogo.py`. Uso interno. Ver `docs/FASE4.md` para el método y los límites.",
        "",
        "V máx = fuerza horizontal ADICIONAL máxima en la punta (kg) con la que la planilla dice \"cumple\".",
        "Siempre con la cabeza de referencia de la planilla (proyectores 10 × 26 cm, P = 20 kg; caso guardado en P.Var.2 Tramos Circ., versiones A y B). No es una carga de diseño de ORBE.",
        "\"no cumple sin fuerza adicional\" = no cumple ni siquiera con su propio viento y la cabeza de referencia.",
        "",
        "| Código | Altura (m) | Cuerpos | Base (mm) | Peso cañerías (kg) | V máx a 100 km/h | V máx a 120 km/h | V máx a 140 km/h | Qué manda a 120 km/h |",
        "|---|---|---|---|---|---|---|---|---|",
        *filas,
        "",
    ]
    (RAIZ / "docs" / "FASE4_CAPACIDAD_generado.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
