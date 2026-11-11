"""Fase 5: el motor contra las 21 memorias de cálculo armadas en Excel el 11-11-2026.

Las memorias (insumos/interno_NO_PUBLICAR/memorias_calculo_postes/Memoria_Calculo_<plano>.xlsm) se llenaron con
Excel por COM y se guardaron recalculadas. Aquí se leen con openpyxl (valores guardados, sin abrir Excel), se arma
la configuración con config_desde_celdas y se compara cada veredicto y cada salida del motor con lo que Excel guardó.

Uso (desde estructural/):  .venv/Scripts/python herramientas/fase5_memorias.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from motor.validador import config_desde_celdas, mapa_hoja, validar  # noqa: E402

CARPETA = RAIZ.parent / "insumos" / "interno_NO_PUBLICAR" / "memorias_calculo_postes"


def main() -> int:
    import openpyxl

    archivos = sorted(CARPETA.glob("Memoria_Calculo_*.xlsm"), key=lambda p: (int(re.search(r"_(\d+)M", p.name).group(1)), p.name))
    if not archivos:
        print(f"No hay memorias en {CARPETA}")
        return 3
    filas, malas = [], 0
    for p in archivos:
        wb = openpyxl.load_workbook(p, data_only=True, keep_vba=False, read_only=False)
        hoja = wb.active.title  # la memoria quedó guardada con la hoja calculada activa
        ws = wb[hoja]
        valores = {f"{c.column_letter}{c.row}": c.value for fila in ws.iter_rows() for c in fila if c.value is not None}
        r = validar(config_desde_celdas(hoja, valores))
        dif = []
        for v in r["verificaciones"]:
            celda = v["celda"].split("!")[1]
            if str(v["mensaje_planilla"]).strip() != str(valores.get(celda, "")).strip():
                dif.append(f"{celda}: motor {v['mensaje_planilla']!r} / Excel {valores.get(celda)!r}")
        for clave, celda in mapa_hoja(hoja)["salidas"].items():
            if clave == "perno_diametro_nominal":
                continue
            m, x = r["salidas"].get(clave), valores.get(celda)
            if isinstance(m, (int, float)) and isinstance(x, (int, float)):
                if abs(m - x) > 1e-9 * max(1.0, abs(m), abs(x)):
                    dif.append(f"{clave}: motor {m} / Excel {x}")
        excel_no = sum(1 for v in r["verificaciones"] if "NO CUMPLE" in str(valores.get(v["celda"].split("!")[1], "")).upper())
        malas += len(dif)
        no_cumplen = [v["nombre"] for v in r["verificaciones"] if v["estado"] == "no cumple"]
        filas.append({"memoria": p.name, "hoja": hoja, "resumen_motor": r["resumen"], "no_cumple_excel": excel_no,
                      "no_cumple_motor": no_cumplen, "verificaciones": len(r["verificaciones"]), "diferencias": dif})
        print(f"{p.stem.replace('Memoria_Calculo_', ''):5} {hoja:22} motor: {r['resumen']:9} · {len(r['verificaciones'])} verificaciones · diferencias: {len(dif)}")
        for d in dif[:5]:
            print("      ", d)
    salida = RAIZ / "trabajo" / "fase5"
    salida.mkdir(parents=True, exist_ok=True)
    (salida / "memorias_vs_motor.json").write_text(json.dumps(filas, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{len(filas)} memorias · diferencias totales: {malas}")
    return 0 if malas == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
