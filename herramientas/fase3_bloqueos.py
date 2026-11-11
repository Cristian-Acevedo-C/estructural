"""Fase 3 · diagnóstico: qué celdas de entrada del motor están bloqueadas (Locked) en las hojas protegidas.

Las hojas vienen protegidas con contraseña. No se quita la protección ni se prueba ninguna contraseña: solo se lee
Range.Locked en una COPIA abierta con macros desactivadas. Así se sabe qué entradas puede editar un usuario real.
Uso (desde estructural/): .venv/Scripts/python herramientas/fase3_bloqueos.py
"""
from __future__ import annotations

import json
import re
import shutil
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from motor.validador import HOJAS, _modelo, mapa_hoja, validar  # noqa: E402

EJEMPLO = {"seccion": "circular", "sobrecarga_kg": 25, "viento_tablero_kg": 50, "viento": {"velocidad_kmh": 120},
           "proyectores": {"alto_cm": 30, "ancho_cm": 50},
           "gancho": {"diametro_cm": 11.4, "espesor_cm": 0.3, "radio_cm": 100, "t_cm": 2, "distancia_cm": 100}}


def main() -> int:
    modelo, _ = _modelo()
    plantilla = RAIZ / "insumos" / modelo["origen"]["archivo"]
    salida = RAIZ / "trabajo" / "fase3"
    salida.mkdir(parents=True, exist_ok=True)
    copia = salida / f"copia_bloqueos_{int(time.time())}.xlsm"
    shutil.copy2(plantilla, copia)
    import pythoncom
    import win32com.client as win32

    pythoncom.CoInitialize()
    excel = win32.DispatchEx("Excel.Application")
    informe = {}
    try:
        excel.Visible = False
        excel.DisplayAlerts = False
        excel.EnableEvents = False
        excel.AutomationSecurity = 3
        wb = excel.Workbooks.Open(str(copia), UpdateLinks=0, ReadOnly=True, AddToMru=False)
        for (_, n, g), hoja in HOJAS.items():
            cfg = dict(EJEMPLO, ganchos=g, tramos=[{"altura_m": 3, "diametro_cm": 11.4 + 5 * i, "espesor_cm": 0.4} for i in range(n)])
            if g:
                cfg.pop("proyectores")
            else:
                cfg.pop("gancho")
            r = validar(cfg)
            ws = wb.Worksheets(hoja)
            ent = mapa_hoja(hoja)["entradas"]
            nombre = {v: k for k, v in ent.items() if isinstance(v, str)}
            celdas = [re.fullmatch(r"'.+'!([A-Z]+\d+)", k).group(1) for k in r["entradas_celdas"]]
            bloqueadas = [c for c in celdas if ws.Range(c).Locked]
            informe[hoja] = {"protegida": bool(ws.ProtectContents), "entradas": len(celdas), "bloqueadas": {c: nombre.get(c, "(tramo, gancho u oculta)") for c in bloqueadas}}
        wb.Close(SaveChanges=False)
    finally:
        excel.Quit()
        del excel
        pythoncom.CoUninitialize()
        for _ in range(20):
            try:
                copia.unlink()
                break
            except OSError:
                time.sleep(0.5)
    (salida / "bloqueos.json").write_text(json.dumps(informe, ensure_ascii=False, indent=1), encoding="utf-8")
    for h, d in informe.items():
        print(f"{h}: protegida={d['protegida']} entradas={d['entradas']} bloqueadas={d['bloqueadas']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
