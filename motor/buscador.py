"""Fase 4 · buscador de tubulares (uso interno).

Dadas las alturas visibles de los tramos (desde la base) y la carga en la punta, busca entre las cañerías ACTIVAS del
catálogo maestro (datos/canerias.csv) las combinaciones MÁS LIVIANAS con las que la planilla dice "cumple".

Restricciones (geométricas, no normativas; revisar con el calculista):
  - telescópico: el diámetro exterior de cada cuerpo cabe en el interior del de abajo (D_sup ≤ D_inf − 2·e_inf).
    No se exige una holgura: la real está "por definir" en los planos;
  - corte: visible + embute ≤ largo de barra del catálogo (6 m). La base no lleva embute; los demás, `embute_m`.
Peso = Σ kg/m × (visible + embute), como el "peso de cañerías" de los planos REV. M (incluye embutes).

"cumple" significa lo mismo que en validar(): cumple lo que la planilla verifica. Soldadura, deflexión, placa y
pernos quedan fuera (lista no_verificado), y la vigencia de la norma de viento de la planilla está en duda
(ESPECIFICACION.md, duda 12).

Uso:
    python -m motor.buscador --alturas 6,1.8,1.8,0.4 --v 30 [--p 20] [--velocidad 120] [--proyectores 10x26]
                             [--embute 0.2] [--punta 60.32] [--k 5] [--json salida.json]
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from itertools import product
from pathlib import Path

from .validador import ErrorConfig, validar

DATOS = Path(__file__).resolve().parents[1] / "datos" / "canerias.csv"


@dataclass(frozen=True)
class Caneria:
    id: str
    norma: str
    d_cm: float
    e_cm: float
    kg_m: float
    largo_barra_m: float

    @property
    def interior_cm(self) -> float:
        return self.d_cm - 2 * self.e_cm


def canerias(ruta: Path = DATOS) -> list[Caneria]:
    with open(ruta, encoding="utf-8") as f:
        filas = [r for r in csv.DictReader(f) if r["estado"].strip().upper() == "ACTIVO"]
    return sorted(
        (Caneria(r["material_id"], r["norma"], float(r["diametro_ext_cm"]), float(r["espesor_cm"]), float(r["kg_m"]), float(r["largo_barra_m"])) for r in filas),
        key=lambda c: (c.d_cm, c.e_cm),
    )


def peso_kg(cadena: tuple[Caneria, ...], alturas_m: list[float], embute_m: float) -> float:
    return sum(c.kg_m * (h + (0.0 if i == 0 else embute_m)) for i, (c, h) in enumerate(zip(cadena, alturas_m)))


def cadenas(tubos: list[Caneria], alturas_m: list[float], embute_m: float, punta_d_mm: float | None = None):
    """Combinaciones base → punta que cumplen las restricciones geométricas. punta_d_mm fija el diámetro del cuerpo de
    arriba (±0,5 mm), donde se monta la luminaria: en el catálogo REV. M todos terminan en Ø60,3."""
    n = len(alturas_m)
    aptos = [[c for c in tubos if h + (0.0 if i == 0 else embute_m) <= c.largo_barra_m + 1e-9] for i, h in enumerate(alturas_m)]
    if punta_d_mm is not None:
        aptos[-1] = [c for c in aptos[-1] if abs(c.d_cm * 10 - punta_d_mm) <= 0.5]

    def rec(i: int, previo: Caneria | None, acc: tuple):
        if i == n:
            yield acc
            return
        for c in aptos[i]:
            if previo is not None and c.d_cm > previo.interior_cm + 1e-9:
                continue
            yield from rec(i + 1, c, acc + (c,))

    yield from rec(0, None, ())


def config_de(cadena, alturas_m, carga: dict) -> dict:
    cfg = {
        "seccion": "circular",
        "ganchos": 0,
        "orden_tramos": "desde_base",
        "tramos": [{"altura_m": h, "diametro_cm": c.d_cm, "espesor_cm": c.e_cm} for c, h in zip(cadena, alturas_m)],
        "sobrecarga_kg": carga.get("sobrecarga_kg", 20.0),
        "viento_tablero_kg": carga["viento_tablero_kg"],
        "viento": {"velocidad_kmh": carga.get("velocidad_kmh", 120)},
        "proyectores": carga.get("proyectores", {"alto_cm": 10, "ancho_cm": 26}),
    }
    for k in ("pernos", "fy_kgcm2"):
        if k in carga:
            cfg[k] = carga[k]
    return cfg


def buscar(alturas_m: list[float], carga: dict, k: int = 5, embute_m: float = 0.2, tubos: list[Caneria] | None = None, max_evaluaciones: int = 50000, punta_d_mm: float | None = None) -> dict:
    if not 1 <= len(alturas_m) <= 4:
        raise ErrorConfig("la planilla admite de 1 a 4 tramos")
    if any(h <= 0 for h in alturas_m):
        raise ErrorConfig("las alturas deben ser positivas")
    tubos = tubos or canerias()
    candidatas = sorted(cadenas(tubos, alturas_m, embute_m, punta_d_mm), key=lambda c: peso_kg(c, alturas_m, embute_m))
    soluciones, evaluadas, errores = [], 0, 0
    for cadena in candidatas:
        if len(soluciones) >= k or evaluadas >= max_evaluaciones:
            break
        evaluadas += 1
        r = validar(config_de(cadena, alturas_m, carga))
        if r["resumen"] == "error":
            errores += 1
            continue
        if r["resumen"] != "cumple":
            continue
        vs = [v for v in r["verificaciones"] if v["estado"] == "cumple" and isinstance(v.get("razon_de_uso"), (int, float))]
        manda = max(vs, key=lambda v: v["razon_de_uso"]) if vs else None
        soluciones.append({
            "peso_canerias_kg": round(peso_kg(cadena, alturas_m, embute_m), 2),
            "tramos_desde_base": [{"caneria": c.id, "norma": c.norma, "d_mm": round(c.d_cm * 10, 2), "e_mm": round(c.e_cm * 10, 2), "visible_m": h} for c, h in zip(cadena, alturas_m)],
            "razon_de_uso_max": round(manda["razon_de_uso"], 3) if manda else None,
            "manda": manda["nombre"] if manda else None,
            "avisos": r["avisos"],
        })
    return {
        "alturas_m_desde_base": alturas_m,
        "carga": carga,
        "embute_m": embute_m,
        "punta_d_mm": punta_d_mm,
        "combinaciones_geometricas": len(candidatas),
        "evaluadas": evaluadas,
        "con_error_de_planilla": errores,
        "soluciones": soluciones,
        "alcance": "cumple = cumple lo que la planilla verifica; soldadura, deflexión, placa y pernos no están verificados",
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m motor.buscador")
    ap.add_argument("--alturas", required=True, help="alturas visibles en m, desde la base: 6,1.8,1.8,0.4")
    ap.add_argument("--v", type=float, required=True, help="fuerza horizontal en la punta (kg)")
    ap.add_argument("--p", type=float, default=20.0, help="peso en la punta (kg), por omisión 20")
    ap.add_argument("--velocidad", type=float, default=120.0)
    ap.add_argument("--proyectores", default="10x26", help="alto x ancho en cm (la planilla no admite 0x0)")
    ap.add_argument("--embute", type=float, default=0.2)
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--punta", type=float, help="diámetro exterior del cuerpo de arriba en mm (ej. 60.32, el del catálogo)")
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    alto, ancho = (float(x) for x in a.proyectores.lower().split("x"))
    carga = {"sobrecarga_kg": a.p, "viento_tablero_kg": a.v, "velocidad_kmh": a.velocidad, "proyectores": {"alto_cm": alto, "ancho_cm": ancho}}
    try:
        r = buscar([float(x) for x in a.alturas.split(",")], carga, k=a.k, embute_m=a.embute, punta_d_mm=a.punta)
    except ErrorConfig as e:
        print(f"Error de configuración: {e}", file=sys.stderr)
        return 3
    if a.json:
        Path(a.json).write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{r['combinaciones_geometricas']} combinaciones geométricas; evaluadas {r['evaluadas']}; con error de planilla {r['con_error_de_planilla']}")
    for i, s in enumerate(r["soluciones"], 1):
        cuerpos = " + ".join(f"Ø{t['d_mm']}×{t['e_mm']} ({t['visible_m']} m)" for t in s["tramos_desde_base"])
        print(f"{i}. {s['peso_canerias_kg']} kg · {cuerpos} · razón de uso {s['razon_de_uso_max']} ({s['manda']})")
    if not r["soluciones"]:
        print("Ninguna combinación de cañerías del catálogo cumple con esas alturas y esa carga.")
    print(r["alcance"])
    return 0 if r["soluciones"] else 1


if __name__ == "__main__":
    sys.exit(main())
