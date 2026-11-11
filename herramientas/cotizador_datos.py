"""Datos del cotizador de postes (uso interno: contiene costos del recetario).

Postes (respuestas de ORBE del 11-11-2026: la receta vigente es la del RECETARIO):
  - tubulares: las 49 recetas ITUB / TTUB de la hoja TUBULARES (herramientas/recetas_tubulares.py);
  - cuadrados y facetados: hojas CUADRADOS y FACETADOS.
Los planos REV. M no se incluyen: son configuraciones nuevas que aún no se venden ni tienen código.

Capacidad: con el motor (réplica exacta de la Plantilla Memoria de Cálculo) se busca la mayor fuerza horizontal en la
punta con la que la planilla dice "cumple", en una grilla de velocidades de viento y pesos en la punta. El cotizador
convierte la EPA de la luminaria en fuerza con el mismo perfil de presión de la planilla y compara.

Costo (sin IVA):
  - si el recetario trae su COSTO calculado, se usa ese;
  - si trae #ERROR!, se recalcula con las partidas de la misma receta (ver recetas_tubulares.py) y se marca.

Uso (desde estructural/): .venv/Scripts/python herramientas/cotizador_datos.py
Escribe trabajo/cotizador/datos.json (con costos). cotizador_html.py arma de ahí la versión interna y la de vendedores.
"""
from __future__ import annotations

import csv
import json
import sys
import time
import warnings
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "herramientas"))
from motor.validador import validar  # noqa: E402
from recetas_tubulares import recetas  # noqa: E402

VELOCIDADES = [100, 110, 120, 130, 140, 150]
PESOS = [20, 35, 50, 75, 100, 150]   # kg en la punta (equipos + soporte); bajo 20 se usa 20 (más exigente)
V_TOPE, PASO = 2000.0, 0.5
CABEZA = {"alto_cm": 10, "ancho_cm": 26}   # cabeza de referencia de la planilla (Fase 4)
COMERCIAL = {  # respuestas de ORBE del 11-11-2026
    "iva": 0.19, "costos_sin_iva": True,
    "margenes": [0.30, 0.35, 0.40], "margen_minimo": 0.30,
    "flete_santiago": 80000, "flete_nota": "Flete solo en Santiago. Fuera de Santiago se terceriza: dar el contacto al cliente.",
    "viento_por_omision": 150, "viento_nota": "Si no se conoce la comuna, se cotiza con el peor escenario.",
    "galvanizado_kg": 490,
}
NOTA_CUADRADO = "Cuadrado: la planilla calcula la torsión con la fórmula de una sección maciza, no la de un tubo (revisión del Ing. J. Tello, 11-11-2026). Va a revisión técnica hasta corregirla."
NOTA_FACETADO = "Facetado: la planilla calcula la inercia como la de un tubo circular y no dice si el Ø es entre caras o vértices. Va a revisión técnica."


def leer(nombre: str) -> list[dict]:
    with open(RAIZ / nombre, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def cfg_tubular(cuerpos, vel, v, p):
    """cuerpos: desde la base, con D_mm, e_mm y visible_mm."""
    return {"seccion": "circular", "ganchos": 0, "orden_tramos": "desde_base",
            "tramos": [{"altura_m": float(c["visible_mm"]) / 1000, "diametro_cm": float(c["D_mm"]) / 10, "espesor_cm": float(c["e_mm"]) / 10} for c in cuerpos],
            "sobrecarga_kg": p, "viento_tablero_kg": v, "viento": {"velocidad_kmh": vel}, "proyectores": dict(CABEZA), "pernos": 4}


def cfg_cuadrado(x, vel, v, p):
    return {"seccion": "cuadrada", "tramos": [{"altura_m": float(x["altura_m"]), "ancho_cm": float(x["lado_mm"]) / 10, "espesor_cm": float(x["espesor_mm"]) / 10}],
            "sobrecarga_kg": p, "viento_tablero_kg": v, "viento": {"velocidad_kmh": vel}, "proyectores": dict(CABEZA), "pernos": 4}


def cfg_facetado(x, vel, v, p):
    return {"seccion": "octogonal", "tramos": [{"altura_m": float(x["altura_m"]), "diametro_superior_cm": float(x["diametro_superior_mm"]) / 10,
            "diametro_base_cm": float(x["diametro_inferior_mm"]) / 10, "espesor_cm": float(x["espesor_mm"]) / 10}],
            "sobrecarga_kg": p, "viento_tablero_kg": v, "viento": {"velocidad_kmh": vel}, "proyectores": dict(CABEZA), "pernos": 4}


def v_max(cfg, x, vel, p):
    """Mayor fuerza en la punta (kg) con 'cumple'. None si no cumple ni con 0. Bisección de 0,5 kg."""
    ok = lambda v: validar(cfg(x, vel, v, p))["resumen"] == "cumple"  # noqa: E731
    if not ok(0.0):
        return None
    if ok(V_TOPE):
        return V_TOPE
    lo, hi = 0.0, V_TOPE
    while hi - lo > PASO:
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if ok(mid) else (lo, mid)
    return round(lo, 1)


def grilla(cfg, x):
    return {str(vel): [v_max(cfg, x, vel, p) for p in PESOS] for vel in VELOCIDADES}


def main() -> int:
    warnings.filterwarnings("ignore")
    t0 = time.time()
    out = []

    # ---- tubulares del recetario (receta vigente)
    for r in recetas():
        n = len(r["cuerpos"])
        propio = r["costo_recetario"] is not None
        notas = list(r["notas"])
        item = {"tipo": "tubular", "codigo": r["codigo"], "nombre": f"Tubular {r['altura_m']:g} m · {r['codigo']}", "altura_m": r["altura_m"], "cuerpos": n,
                "descripcion": " + ".join(f"Ø{c['D_mm']:g}×{c['e_mm']:g}" for c in r["cuerpos"]) + f" · placa {(r['placa'] or '—').replace('*', '×')} · pernos {(r['perno'] or '—').replace('*', '×')}",
                "costo": r["costo_recetario"] if propio else r["costo"],
                "costo_origen": "recetario (hoja TUBULARES, COSTO)" if propio else "recalculado: el recetario muestra #ERROR! en esta receta",
                "costo_recalculado": r["costo"], "partidas": r["partidas"], "notas": notas}
        if n > 4:
            item["capacidad"] = None
            item["nota_tecnica"] = "5 cuerpos: la planilla de cálculo llega a 4 tramos. Sin preverificación: va a revisión técnica."
        else:
            item["capacidad"] = grilla(cfg_tubular, r["cuerpos"])
            if any("corregido" in x for x in notas):
                item["nota_tecnica"] = "La receta tiene una medida dudosa en el recetario (se calculó con la corregida). Va a revisión técnica hasta confirmarla."
        out.append(item)

    # ---- cuadrados y facetados del recetario (costo = columna COSTO)
    import openpyxl
    wb = openpyxl.load_workbook(RAIZ / "insumos" / "recetario_2026-11-11b.xlsx", data_only=True)
    num = lambda x: float(str(x).replace("$", "").replace(",", "").strip()) if x not in (None, "") else None  # noqa: E731
    costo_cu = {f[0]: num(f[11]) for f in wb["CUADRADOS"].iter_rows(min_row=2, values_only=True) if isinstance(f[0], str) and f[0].startswith("CU")}
    costo_fa = {f[14]: num(f[22]) for f in wb["FACETADOS"].iter_rows(values_only=True) if len(f) > 23 and isinstance(f[14], str) and f[14].startswith("FAC-")}
    for x in leer("datos/postes_cuadrados_recetario.csv"):
        out.append({"tipo": "cuadrado", "codigo": x["codigo"], "nombre": f"Cuadrado {float(x['altura_m']):g} m · {x['codigo']}", "altura_m": float(x["altura_m"]),
                    "descripcion": f"{float(x['lado_mm']):g}×{float(x['lado_mm']):g}×{float(x['espesor_mm']):g} mm · placa {x['placa']} · pernos {x['canastillo']}",
                    "costo": costo_cu.get(x["codigo"]), "costo_origen": "recetario (hoja CUADRADOS, COSTO)", "partidas": [], "notas": [],
                    "nota_tecnica": NOTA_CUADRADO, "capacidad": grilla(cfg_cuadrado, x)})
    for x in leer("datos/postes_facetados_recetario.csv"):
        out.append({"tipo": "facetado", "codigo": x["codigo"], "nombre": f"Facetado {float(x['altura_m']):g} m · {x['codigo']}", "altura_m": float(x["altura_m"]),
                    "descripcion": f"8 lados · Ø{float(x['diametro_inferior_mm']):g}/{float(x['diametro_superior_mm']):g} mm · e {float(x['espesor_mm']):g} mm · placa {x['placa']} · pernos {x['pernos']}",
                    "costo": costo_fa.get(x["codigo"]), "costo_origen": "recetario (hoja FACETADOS, COSTO)", "partidas": [], "notas": [],
                    "nota_tecnica": NOTA_FACETADO, "capacidad": grilla(cfg_facetado, x)})

    datos = {"generado": time.strftime("%d-%m-%Y %H:%M"), "velocidades": VELOCIDADES, "pesos": PESOS, "comercial": COMERCIAL,
             "presion": {"hasta_4m": 70, "a": 32.595, "b": 28.594, "v_ref": 120, "nota": "perfil de la planilla (G51) y factor (V/120)² (D48)"},
             "cabeza_referencia": CABEZA, "postes": out}
    salida = RAIZ / "trabajo" / "cotizador"
    salida.mkdir(parents=True, exist_ok=True)
    (salida / "datos.json").write_text(json.dumps(datos, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    sin_costo = [p["codigo"] for p in out if p.get("costo") is None]
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"{len(out)} postes en {time.time() - t0:.0f} s · sin costo: {sin_costo} · tubulares recalculados: {sum(1 for p in out if p['tipo'] == 'tubular' and p['costo_origen'].startswith('recalc'))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
