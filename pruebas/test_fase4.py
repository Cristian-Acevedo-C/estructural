"""Fase 4: buscador, capacidad del catálogo REV. M y aviso de entradas bloqueadas."""
import csv
import sys
from collections import defaultdict
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "herramientas"))

from fase4_catalogo import capacidad, postes  # noqa: E402
from motor.buscador import buscar, cadenas, canerias, peso_kg  # noqa: E402
from motor.validador import ErrorConfig, avisos_bloqueadas, validar  # noqa: E402

CSV = RAIZ / "fuentes" / "planos_tubulares_revM" / "catalogo_tubulares_revM_transcrito.csv"


def _por_codigo():
    out = defaultdict(list)
    with open(CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out[r["codigo"]].append(r)
    for v in out.values():
        v.sort(key=lambda r: int(r["posicion_desde_base"]))
    return out


def _caneria(tubos, d_mm, e_mm):
    return next(c for c in tubos if abs(c.d_cm * 10 - d_mm) <= 0.5 and abs(c.e_cm * 10 - e_mm) <= 0.05)


def test_peso_reproduce_el_de_los_24_planos():
    """El peso de cañerías del buscador (kg/m × corte) da el mismo valor que declara cada plano REV. M."""
    tubos = canerias()
    for codigo, cuerpos in _por_codigo().items():
        cadena = tuple(_caneria(tubos, float(c["D_mm"]), float(c["e_mm"])) for c in cuerpos)
        alturas = [float(c["visible_mm"]) / 1000 for c in cuerpos]
        embute = max(float(c["embute_mm"]) for c in cuerpos) / 1000
        assert peso_kg(cadena, alturas, embute) == pytest.approx(float(cuerpos[0]["peso_canerias_declarado_kg"]), abs=0.06), codigo


def test_todas_las_canerias_del_catalogo_revM_existen_en_el_catalogo_maestro():
    tubos = canerias()
    for cuerpos in _por_codigo().values():
        for c in cuerpos:
            _caneria(tubos, float(c["D_mm"]), float(c["e_mm"]))  # StopIteration si falta


def test_restricciones_geometricas():
    tubos = canerias()
    alturas = [3.0, 2.8, 2.8, 1.4]
    for cadena in cadenas(tubos, alturas, 0.2, punta_d_mm=60.32):
        assert abs(cadena[-1].d_cm * 10 - 60.32) <= 0.5
        for inf, sup in zip(cadena, cadena[1:]):
            assert sup.d_cm <= inf.interior_cm + 1e-9
        for i, (c, h) in enumerate(zip(cadena, alturas)):
            assert h + (0 if i == 0 else 0.2) <= c.largo_barra_m + 1e-9
    # un cuerpo superior de 6 m no cabe en una barra de 6 m si lleva embute
    assert list(cadenas(tubos, [3.0, 6.0], 0.2)) == []


def test_el_buscador_encuentra_el_poste_del_catalogo_en_su_capacidad():
    """Con las alturas de 7Mb, punta Ø60,3 y la carga en su límite, la solución más liviana es la del catálogo."""
    c7 = postes()["7Mb"]
    cap = capacidad(c7, 120)
    r = buscar([6.0, 1.0], {"viento_tablero_kg": cap["v_max_kg"], "velocidad_kmh": 120}, k=1, punta_d_mm=60.32)
    s = r["soluciones"][0]
    assert [(t["d_mm"], t["e_mm"]) for t in s["tramos_desde_base"]] == [(88.9, 3.2), (60.32, 2.9)]
    assert s["peso_canerias_kg"] == pytest.approx(45.2, abs=0.06)


def test_capacidad_monotona_y_estable():
    c = capacidad(postes()["3Ma"], 120)
    assert c["base"] == "cumple" and c["monotono"] is True
    assert c["v_max_kg"] == pytest.approx(101.6, abs=0.6)
    # justo sobre el límite ya no cumple
    from fase4_catalogo import config
    assert validar(config(postes()["3Ma"], 120, c["v_max_kg"] + 1))["resumen"] == "no cumple"


def test_cinco_tramos_fuera_de_alcance():
    with pytest.raises(ErrorConfig):
        buscar([3, 2.8, 2.8, 2.8, 0.6], {"viento_tablero_kg": 10})


def test_sin_proyectores_la_planilla_da_error_no_cumple():
    """La torsión divide por alto × ancho de proyectores: con 0 × 0 el resumen es 'error', nunca 'cumple'."""
    cfg = {"seccion": "circular", "ganchos": 0, "orden_tramos": "desde_base",
           "tramos": [{"altura_m": 2.8, "diametro_cm": 16.83, "espesor_cm": 0.5}, {"altura_m": 0.2, "diametro_cm": 6.03, "espesor_cm": 0.29}],
           "sobrecarga_kg": 0, "viento_tablero_kg": 0, "viento": {"velocidad_kmh": 120}, "proyectores": {"alto_cm": 0, "ancho_cm": 0}}
    assert validar(cfg)["resumen"] == "error"


def test_aviso_de_entradas_bloqueadas():
    hoja = "P.Var. 2 Tramos Circ. 1 gancho"
    assert avisos_bloqueadas(hoja, {"A27": 0, "B51": 0.6}) == []
    a = avisos_bloqueadas(hoja, {"A27": 30.0, "B51": 0.7})
    assert len(a) == 2 and "viento_tablero_kg (A27)" in a[0] and "coef_forma (B51)" in a[1]
    # la hoja sin proteger no avisa (la planilla sí deja editarla)
    assert avisos_bloqueadas("P.Var. 2 Tramos Circ. 2 ganchos", {"A27": 30.0}) == []
