"""Fase 6 · capacidad de los postes cuadrados y facetados del RECETARIO según la planilla (uso interno).

Mismo método que la Fase 4 (herramientas/fase4_catalogo.py): para cada poste y velocidad de viento se busca la mayor
fuerza horizontal ADICIONAL en la punta (kg) con la que la planilla dice "cumple", con la cabeza de referencia de la
planilla (proyectores 10 × 26 cm, P = 20 kg). No es una carga de diseño de ORBE.

  - Cuadrados (datos/postes_cuadrados_recetario.csv)  → hoja "P.Recto Cuad."      (sección cuadrada constante)
  - Facetados (datos/postes_facetados_recetario.csv)  → hoja "P.Var. Octogonal"   (octogonal de sección variable)

Supuestos: Fy 2.400 kg/cm², 4 pernos, coeficientes de la planilla (forma 1,6 cuadrado y 0,7 octogonal).
El "diámetro" del facetado se ingresa tal como viene en el recetario; la planilla no dice si es entre caras o vértices.

Uso (desde estructural/): .venv/Scripts/python herramientas/fase6_recetario.py
Escribe trabajo/fase6/capacidad_recetario.json y docs/FASE6_CAPACIDAD_generado.md.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "herramientas"))
from fase4_catalogo import CABEZA, P_REFERENCIA_KG, PASO, V_TOPE, VELOCIDADES, manda  # noqa: E402
from motor.validador import validar  # noqa: E402


def leer(nombre: str) -> list[dict]:
    with open(RAIZ / "datos" / nombre, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def cfg_cuadrado(p: dict, velocidad: float, v_kg: float) -> dict:
    return {"_origen": "fase6_recetario.py", "seccion": "cuadrada", "ganchos": 0,
            "tramos": [{"altura_m": float(p["altura_m"]), "ancho_cm": float(p["lado_mm"]) / 10, "espesor_cm": float(p["espesor_mm"]) / 10}],
            "sobrecarga_kg": P_REFERENCIA_KG, "viento_tablero_kg": v_kg, "viento": {"velocidad_kmh": velocidad}, "proyectores": dict(CABEZA), "pernos": 4}


def cfg_facetado(p: dict, velocidad: float, v_kg: float) -> dict:
    return {"_origen": "fase6_recetario.py", "seccion": "octogonal", "ganchos": 0,
            "tramos": [{"altura_m": float(p["altura_m"]), "diametro_superior_cm": float(p["diametro_superior_mm"]) / 10,
                        "diametro_base_cm": float(p["diametro_inferior_mm"]) / 10, "espesor_cm": float(p["espesor_mm"]) / 10}],
            "sobrecarga_kg": P_REFERENCIA_KG, "viento_tablero_kg": v_kg, "viento": {"velocidad_kmh": velocidad}, "proyectores": dict(CABEZA), "pernos": 4}


def capacidad(cfg, p: dict, velocidad: float) -> dict:
    """Igual que fase4_catalogo.capacidad, con el armado de la configuración como parámetro."""
    ok = lambda v: validar(cfg(p, velocidad, v))["resumen"] == "cumple"  # noqa: E731
    r0 = validar(cfg(p, velocidad, 0.0))
    res = {"velocidad_kmh": velocidad, "base": r0["resumen"]}
    if r0["resumen"] != "cumple":
        res["falla"] = [f"{v['nombre']} ({v['mensaje_planilla']})" for v in r0["verificaciones"] if v["estado"] in ("no cumple", "error")]
        res["v_max_kg"] = None
        return res
    if ok(V_TOPE):
        res["v_max_kg"] = f"> {V_TOPE:g}"
        return res
    lo, hi = 0.0, V_TOPE
    while hi - lo > PASO:
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if ok(mid) else (lo, mid)
    monotono = all(ok(lo * k / 10) for k in range(11)) and not any(ok(hi + d) for d in (0, 10, 50))
    m = manda(validar(cfg(p, velocidad, hi)))
    res.update({"v_max_kg": round(lo, 1), "monotono": monotono, "manda_en_limite": m["nombre"] if m else None})
    return res


def celda(c: dict) -> str:
    if c["base"] != "cumple":
        return "**error de la planilla**" if c["base"] == "error" else "**no cumple sin fuerza adicional**"
    return f"{c['v_max_kg']}" + ("" if c.get("monotono", True) else " (¡no monótono!)")


def main() -> int:
    cuad, fac = leer("postes_cuadrados_recetario.csv"), leer("postes_facetados_recetario.csv")
    res = {"cuadrados": {}, "facetados": {}}
    for p in cuad:
        res["cuadrados"][p["codigo"]] = {**{k: p[k] for k in ("altura_m", "lado_mm", "espesor_mm", "peso_kg")}, "capacidad": [capacidad(cfg_cuadrado, p, v) for v in VELOCIDADES]}
    for p in fac:
        res["facetados"][p["codigo"]] = {**{k: p[k] for k in ("altura_m", "diametro_inferior_mm", "diametro_superior_mm", "espesor_mm")}, "capacidad": [capacidad(cfg_facetado, p, v) for v in VELOCIDADES]}
    salida = RAIZ / "trabajo" / "fase6"
    salida.mkdir(parents=True, exist_ok=True)
    (salida / "capacidad_recetario.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")

    def manda120(i):
        c = next(c for c in i["capacidad"] if c["velocidad_kmh"] == 120)
        return c.get("manda_en_limite") or "; ".join(c.get("falla", [])) or "—"

    md = [
        "# Capacidad de los postes cuadrados y facetados del recetario según la planilla (generado)",
        "",
        "Generado por `herramientas/fase6_recetario.py`. Uso interno. Método y límites en `docs/FASE6.md`.",
        "",
        "V máx = fuerza horizontal ADICIONAL máxima en la punta (kg) con la que la planilla dice \"cumple\", con la cabeza de referencia",
        "de la planilla (proyectores 10 × 26 cm, P = 20 kg). No es una carga de diseño de ORBE.",
        "",
        "## Postes cuadrados (hoja P.Recto Cuad.)",
        "",
        "| Código | Altura (m) | Perfil (mm) | Peso (kg) | V máx a 100 km/h | V máx a 120 km/h | V máx a 140 km/h | Qué manda a 120 km/h |",
        "|---|---|---|---|---|---|---|---|",
        *[f"| {c} | {float(i['altura_m']):g} | {float(i['lado_mm']):g}×{float(i['lado_mm']):g}×{float(i['espesor_mm']):g} | {i['peso_kg']} | {' | '.join(celda(x) for x in i['capacidad'])} | {manda120(i)} |"
          for c, i in res["cuadrados"].items()],
        "",
        "## Postes facetados de 8 lados (hoja P.Var. Octogonal)",
        "",
        "| Código | Altura (m) | Ø inferior / superior (mm) | e (mm) | V máx a 100 km/h | V máx a 120 km/h | V máx a 140 km/h | Qué manda a 120 km/h |",
        "|---|---|---|---|---|---|---|---|",
        *[f"| {c} | {float(i['altura_m']):g} | {float(i['diametro_inferior_mm']):g} / {float(i['diametro_superior_mm']):g} | {float(i['espesor_mm']):g} | {' | '.join(celda(x) for x in i['capacidad'])} | {manda120(i)} |"
          for c, i in res["facetados"].items()],
        "",
    ]
    (RAIZ / "docs" / "FASE6_CAPACIDAD_generado.md").write_text("\n".join(md), encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(md[7:]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
