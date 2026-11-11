"""Fase 3: el generador de configuraciones nuevas (sin Excel). La comparación contra Excel vive en
herramientas/fase3_excel.py porque necesita Excel instalado; aquí se prueba que lo que genera sea válido y reproducible."""
import random
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "herramientas"))

from fase3_excel import canerias, config_nueva, iguales  # noqa: E402
from motor.excel import ErrorExcel  # noqa: E402
from motor.validador import HOJAS, validar  # noqa: E402

BLOQUEADAS = {"coef_forma", "amortiguamiento", "coef_von_karman", "g_kgcm2", "e_kgcm2", "fs_pandeo_general"}


def test_reproducible_con_la_misma_semilla():
    tubos = canerias()
    a = [config_nueva(random.Random(7), tubos, n, g, s) for (s, n, g) in HOJAS]
    b = [config_nueva(random.Random(7), tubos, n, g, s) for (s, n, g) in HOJAS]
    assert a == b


def test_configuraciones_validas_y_sin_claves_bloqueadas():
    tubos = canerias()
    assert len(tubos) >= 4
    rng = random.Random(20261110)
    resumenes = set()
    for (s, n, g), hoja in HOJAS.items():
        for _ in range(5):
            cfg = config_nueva(rng, tubos, n, g, s)
            assert not BLOQUEADAS & set(cfg), cfg
            assert len(cfg["tramos"]) == n
            if s == "circular":
                # el de arriba primero: diámetros no decrecientes hacia la base
                d = [t["diametro_cm"] for t in cfg["tramos"]]
                assert d == sorted(d)
                assert all(2 * t["espesor_cm"] < t["diametro_cm"] for t in cfg["tramos"])
            elif s == "octogonal":
                assert all(t["diametro_superior_cm"] < t["diametro_base_cm"] for t in cfg["tramos"])
            r = validar(cfg)
            assert r["hoja"] == hoja
            resumenes.add(r["resumen"])
    # la muestra recorre las dos ramas del veredicto
    assert {"cumple", "no cumple"} <= resumenes


def test_iguales_compara_como_excel():
    assert iguales(1.0, 1.0 + 1e-12, 1e-9)
    assert not iguales(1.0, 1.001, 1e-9)
    assert iguales(ErrorExcel("#DIV/0!"), "#DIV/0!", 1e-9)
    assert not iguales(ErrorExcel("#DIV/0!"), 0.0, 1e-9)
    assert iguales(None, "", 1e-9)
    assert iguales("OK! CUMPLE", "OK! CUMPLE", 1e-9)
