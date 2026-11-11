"""Pruebas del motor (desde estructural/): python -m pytest pruebas -q"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "pruebas"))

from motor import validar  # noqa: E402
from motor.excel import DIV0, NUM, Libro  # noqa: E402
from motor.validador import HOJAS, TRAMO_CLAVES, ErrorConfig, config_desde_celdas, mapa_hoja  # noqa: E402
import contra_guardados  # noqa: E402


def ev(formula: str, celdas: dict | None = None):
    libro = Libro({"H": {"X1": {"f": formula}, **(celdas or {})}})
    return libro.calculo().valor("H", "X1")


# ---------------------------------------------------------------- semántica de Excel


@pytest.mark.parametrize(
    "formula, esperado",
    [
        ("=-2^2", 4.0),  # en Excel la negación va antes que la potencia
        ("=2^3^2", 64.0),  # ^ asocia a la izquierda
        ("=ROUND(2.5,0)", 3.0),
        ("=ROUND(-2.5,0)", -3.0),
        ("=ROUND(1.005,2)", 1.01),  # Excel redondea con 15 cifras significativas
        ('=IF("si"="SI",1,0)', 1.0),  # textos sin distinguir mayúsculas
        ("=IF(1>2,5)", False),  # IF sin rama falsa
        ("=16^(-1)", 0.0625),
        ("=A1+1", 1.0),  # celda vacía vale 0
        ("=SQRT(9)+ABS(-1)+MIN(3,2)", 6.0),
        ("=MMULT(MMULT(A2:B2,MINVERSE(A3:B4)),C3:C4)", 1.0),
    ],
)
def test_semantica(formula, esperado):
    celdas = {"A2": {"v": 1}, "B2": {"v": 0}, "A3": {"v": 2}, "B3": {"v": 0}, "A4": {"v": 0}, "B4": {"v": 4}, "C3": {"v": 2}, "C4": {"v": 0}}
    assert ev(formula, celdas) == pytest.approx(esperado) if not isinstance(esperado, bool) else ev(formula, celdas) is esperado


def test_errores_se_propagan():
    assert ev("=1/0") == DIV0
    assert ev("=LN(0)") == NUM
    assert ev("=IF(1/0>1,1,2)") == DIV0


# ---------------------------------------------------------------- contra lo que Excel dejó guardado


@pytest.mark.parametrize("version", ["A", "B"])
def test_todas_las_formulas_coinciden_con_excel(version):
    assert contra_guardados.main(version) == 0


@pytest.mark.parametrize("version", ["A", "B"])
@pytest.mark.parametrize("hoja", list(HOJAS.values()))
def test_validar_reproduce_la_planilla_guardada(version, hoja):
    guard = json.loads((RAIZ / f"motor/modelo/guardados_{version}.json").read_text(encoding="utf-8"))["valores"][hoja]
    r = validar(config_desde_celdas(hoja, guard))
    assert r["verificaciones"], "sin verificaciones"
    for v in r["verificaciones"]:
        celda = v["celda"].split("!")[1]
        assert str(v["mensaje_planilla"]).strip() == str(guard[celda]).strip(), v["nombre"]
    for clave, celda in mapa_hoja(hoja)["salidas"].items():
        if clave == "perno_diametro_nominal":
            continue
        assert r["salidas"][clave] == pytest.approx(guard[celda], rel=1e-9, abs=1e-9), clave


# ---------------------------------------------------------------- configuración

BASE = {
    "seccion": "circular",
    "ganchos": 0,
    "tramos": [{"altura_m": 6, "diametro_cm": 8.9, "espesor_cm": 0.3}],
    "sobrecarga_kg": 20,
    "viento_tablero_kg": 20,
    "viento": {"velocidad_kmh": 120},
    "proyectores": {"alto_cm": 30, "ancho_cm": 30},
}


GANCHO_CLAVES = {
    "circular": {"diametro_cm", "espesor_cm", "radio_cm", "distancia_cm", "t_cm"},
    "octogonal": {"diametro_cm", "espesor_cm", "radio_cm", "distancia_cm", "t_cm"},
    "cuadrada": {"d1_cm", "d2_cm", "d3_cm", "t_cm"},
}


def test_entradas_de_las_18_hojas_se_encuentran():
    assert len(HOJAS) == 18
    for (seccion, n, g), hoja in HOJAS.items():
        m = mapa_hoja(hoja)
        assert m["seccion"] == seccion
        for clave in ("fy_kgcm2", "sobrecarga_kg", "viento_tablero_kg", "viento_usar_velocidad", "viento_velocidad_kmh", "coef_forma", "amortiguamiento", "coef_von_karman", "g_kgcm2", "pernos"):
            assert clave in m["entradas"], (hoja, clave)
        assert len(m["tramos"]) == n
        assert all(set(t) == set(TRAMO_CLAVES[seccion]) for t in m["tramos"]), hoja
        assert set(m["gancho"]) == (GANCHO_CLAVES[seccion] if g else set()), hoja
        assert ("proyectores_alto_cm" in m["entradas"]) == (g == 0), hoja
        # todas las celdas de entrada son constantes en la planilla (no fórmulas)
        celdas = [*m["entradas"].values(), *[c for t in m["tramos"] for c in t.values()], *m["gancho"].values()]
        assert len(set(celdas)) == len(celdas), (hoja, "celda repetida")
    assert "cable_lateral_kg" in mapa_hoja("P.Var. Octogonal 2 ganchos")["entradas"]


CUAD = {"seccion": "cuadrada", "tramos": [{"altura_m": 6, "ancho_cm": 15, "espesor_cm": 0.4}], "sobrecarga_kg": 20, "viento_tablero_kg": 20,
        "viento": {"velocidad_kmh": 120}, "proyectores": {"alto_cm": 30, "ancho_cm": 30}}
OCTO = {"seccion": "octogonal", "tramos": [{"altura_m": 12, "diametro_superior_cm": 12, "diametro_base_cm": 30, "espesor_cm": 0.4}], "sobrecarga_kg": 20,
        "viento_tablero_kg": 20, "viento": {"velocidad_kmh": 120}, "proyectores": {"alto_cm": 30, "ancho_cm": 30}}


@pytest.mark.parametrize("cfg", [CUAD, OCTO])
def test_cuadrada_y_octogonal_por_nombres(cfg):
    r = validar(cfg)
    assert r["hoja"] in ("P.Recto Cuad.", "P.Var. Octogonal")
    assert r["resumen"] in ("cumple", "no cumple") and r["verificaciones"]


@pytest.mark.parametrize(
    "cfg, mensaje",
    [
        ({**CUAD, "tramos": [{"altura_m": 6, "diametro_cm": 15, "espesor_cm": 0.4}]}, "no corresponden a la sección"),
        ({**CUAD, "tramos": [{"altura_m": 6, "ancho_cm": 0.6, "espesor_cm": 0.4}]}, "doble del espesor"),
        ({**OCTO, "tramos": [{"altura_m": 12, "diametro_base_cm": 30, "espesor_cm": 0.4}]}, "falta tramos[0].diametro_superior_cm"),
        ({**CUAD, "tramos": CUAD["tramos"] * 2}, "no hay hoja"),
        ({**OCTO, "ganchos": 2, "gancho": {"diametro_cm": 6, "espesor_cm": 0.3, "radio_cm": 50, "distancia_cm": 100, "t_cm": 0}}, "falta cable_lateral_kg"),
    ],
)
def test_errores_cuadrada_octogonal(cfg, mensaje):
    import re

    with pytest.raises(ErrorConfig, match=re.escape(mensaje)):
        validar(cfg)


def test_aviso_de_milimetros_en_octogonal():
    r = validar({**OCTO, "tramos": [{"altura_m": 12, "diametro_superior_cm": 120, "diametro_base_cm": 300, "espesor_cm": 4}]})
    assert sum("milímetros" in a for a in r["avisos"]) == 2


@pytest.mark.parametrize(
    "cambio, mensaje",
    [
        ({"sobrecarga_kq": 1}, "claves desconocidas"),
        ({"tramos": [{"altura_m": 6, "diametro_cm": 8.9}]}, "falta tramos[0].espesor_cm"),
        ({"tramos": [{"altura_m": 6, "diametro_cm": 1, "espesor_cm": 0.5}]}, "doble del espesor"),
        ({"tramos": [{"altura_m": 1, "diametro_cm": 9, "espesor_cm": 0.3}] * 5}, "no hay hoja"),
        ({"viento": {}}, "velocidad_kmh"),
        ({"ganchos": 1}, "falta gancho."),
    ],
)
def test_errores_de_configuracion(cambio, mensaje):
    import re

    with pytest.raises(ErrorConfig, match=re.escape(mensaje)):
        validar({**BASE, **cambio})


def test_aviso_de_milimetros():
    r = validar({**BASE, "tramos": [{"altura_m": 6, "diametro_cm": 114.3, "espesor_cm": 3.6}]})
    assert any("milímetros" in a for a in r["avisos"])


def test_el_gancho_sale_no_verificado():
    cfg = {**BASE, "ganchos": 1, "gancho": {"diametro_cm": 6, "espesor_cm": 0.3, "radio_cm": 50, "distancia_cm": 100, "t_cm": 0}}
    del cfg["proyectores"]
    r = validar(cfg)
    gancho = [v for v in r["verificaciones"] if "gancho" in v["nombre"].lower()]
    assert gancho and all(v["estado"] == "no verificado" and not v["cumple"] for v in gancho)


def test_veredictos_rotos_y_auxiliares_no_entran_al_resumen():
    r = validar(BASE)
    assert all(v["estado"] in ("cumple", "no cumple", "no verificado") for v in r["verificaciones"])
    assert len(r["verificaciones"]) == 6


def test_mas_viento_mas_uso_a_flexion():
    def razon(vel):
        r = validar({**BASE, "viento": {"velocidad_kmh": vel}})
        return next(v["razon_de_uso"] for v in r["verificaciones"] if v["nombre"].startswith("Flexión"))

    assert razon(80) < razon(120) < razon(160)


def test_mas_espesor_menos_uso_a_flexion():
    def razon(e):
        r = validar({**BASE, "tramos": [{"altura_m": 6, "diametro_cm": 8.9, "espesor_cm": e}]})
        return next(v["razon_de_uso"] for v in r["verificaciones"] if v["nombre"].startswith("Flexión"))

    assert razon(0.4) < razon(0.3)


@pytest.mark.parametrize("cfg, esperado", [(CUAD, 1.6), (OCTO, 0.7), (BASE, 0.6)])
def test_coef_forma_por_omision_es_el_de_la_hoja(cfg, esperado):
    """Sin coef_forma en la configuración se usa el de la planilla para esa sección, y no hay aviso de entrada bloqueada."""
    r = validar(cfg)
    celda = mapa_hoja(r["hoja"])["entradas"]["coef_forma"]
    assert r["entradas_celdas"][f"'{r['hoja']}'!{celda}"] == esperado
    assert any(f"coef_forma = {esperado}" in s for s in r["supuestos"])
    assert not r["avisos"]


def test_cable_lateral_bloqueado_avisa():
    g = {"diametro_cm": 20, "espesor_cm": 1, "radio_cm": 130, "distancia_cm": 130, "t_cm": 3.5}
    r = validar({**{k: v for k, v in OCTO.items() if k != "proyectores"}, "ganchos": 2, "gancho": g, "viento_tablero_kg": 0, "cable_lateral_kg": 100})
    assert any("A27" in a and "bloqueada" in a for a in r["avisos"])
