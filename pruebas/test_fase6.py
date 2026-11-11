"""Fase 6: tablas del recetario (sin costos) y capacidad de cuadrados y facetados."""
import csv
import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "herramientas"))

from fase6_recetario import capacidad, cfg_cuadrado, cfg_facetado  # noqa: E402
from motor.validador import validar  # noqa: E402
from recetario_a_csv import kg_m_teorico  # noqa: E402

ARCHIVOS = ["tubos_recetario.csv", "postes_cuadrados_recetario.csv", "postes_facetados_recetario.csv"]


def leer(nombre):
    with open(RAIZ / "datos" / nombre, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_cantidades():
    assert [len(leer(a)) for a in ARCHIVOS] == [19, 70, 10]


@pytest.mark.parametrize("archivo", ARCHIVOS + ["../docs/RECETARIO_CRUCE_generado.md", "../docs/FASE6_CAPACIDAD_generado.md", "../trabajo/fase6/capacidad_recetario.json"])
def test_sin_costos_ni_precios(archivo):
    """Regla 3 del proyecto: nada de precios, costos, márgenes ni valor por kilo en lo que se genera."""
    texto = (RAIZ / "datos" / archivo).read_text(encoding="utf-8").lower()
    for palabra in ("precio", "costo", "margen", "venta", "clp", "$", "galva", "proveedor", "provedor"):
        if palabra in ("precio", "costo") and archivo.endswith("CRUCE_generado.md"):
            continue  # el informe dice "no se copian precios, costos…"
        assert palabra not in texto, (archivo, palabra)


def test_tubos_coherentes_con_su_peso():
    for t in leer("tubos_recetario.csv"):
        teo = kg_m_teorico(float(t["diametro_ext_mm"]), float(t["espesor_mm"]))
        assert abs(float(t["kg_m"]) - teo) / teo <= 0.05, t["material_id"]
        assert 15 < float(t["diametro_ext_mm"]) < 200


def test_peso_de_los_cuadrados_es_el_de_la_planilla():
    """El peso del recetario (kg) = kg/m que calcula la hoja P.Recto Cuad. × altura, con 6 % de tolerancia (la planilla da entre 1,8 % y 5 % más)
    (el recetario usa pesos de tabla del perfil; la planilla, el área de un cuadrado de esquinas vivas)."""
    for p in leer("postes_cuadrados_recetario.csv"):
        r = validar(cfg_cuadrado(p, 120, 0))
        kg_m = r["salidas"]["peso_propio_kg"] / float(p["altura_m"])
        assert abs(kg_m * float(p["altura_m"]) - float(p["peso_kg"])) / float(p["peso_kg"]) <= 0.06, (p["codigo"], kg_m, p["peso_kg"])


def test_capacidad_baja_con_la_altura_y_con_el_viento():
    cuad = {p["codigo"]: p for p in leer("postes_cuadrados_recetario.csv")}
    v = [capacidad(cfg_cuadrado, cuad[c], 120)["v_max_kg"] for c in ("CU1", "CU3", "CU5", "CU7")]
    assert v == sorted(v, reverse=True)
    a, b = (capacidad(cfg_cuadrado, cuad["CU5"], vel) for vel in (100, 140))
    assert a["v_max_kg"] > b["v_max_kg"] and a["monotono"] and b["monotono"]


def test_facetado_usa_la_hoja_octogonal():
    p = leer("postes_facetados_recetario.csv")[0]
    r = validar(cfg_facetado(p, 120, 0))
    assert r["hoja"] == "P.Var. Octogonal" and r["resumen"] == "cumple"


def test_resultado_guardado_coincide():
    g = json.loads((RAIZ / "trabajo/fase6/capacidad_recetario.json").read_text(encoding="utf-8"))
    assert len(g["cuadrados"]) == 70 and len(g["facetados"]) == 10
    p = next(x for x in leer("postes_cuadrados_recetario.csv") if x["codigo"] == "CU6")
    assert g["cuadrados"]["CU6"]["capacidad"][1]["v_max_kg"] == capacidad(cfg_cuadrado, p, 120)["v_max_kg"]
    assert all(c.get("monotono", True) for grupo in g.values() for i in grupo.values() for c in i["capacidad"])
