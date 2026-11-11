"""Fase 3: compara el motor contra el Excel ORIGINAL recalculado con configuraciones NUEVAS.

La Fase 2 comparó contra los valores que Excel dejó guardados (las configuraciones que ya estaban en la planilla).
Aquí se generan configuraciones que la planilla nunca vio, se escriben en una COPIA de la planilla abierta con Excel
(macros desactivadas), se recalcula el libro completo y se compara CADA fórmula de la hoja con lo que calcula el motor.

Reglas:
- `insumos/` nunca se abre con Excel: se copia a `trabajo/fase3/` y la copia se borra al terminar.
  Se verifica el SHA-256 de la plantilla antes y después.
- Excel se abre invisible, sin alertas, sin eventos y con AutomationSecurity = 3 (no ejecuta macros).
- Las configuraciones salen de una semilla fija: la corrida es reproducible.

Uso (desde estructural/):
    .venv/Scripts/python herramientas/fase3_excel.py [--por-hoja 10] [--semilla 20261110] [--tol 1e-9]
Escribe trabajo/fase3/resultado_<semilla>.json e imprime el resumen. Código de salida 0 si no hay diferencias.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import re
import shutil
import sys
import time
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from motor.excel import es_error  # noqa: E402
from motor.validador import HOJAS, ErrorConfig, _modelo, validar  # noqa: E402

# Value2 de COM devuelve los errores de Excel como enteros
ERRORES_COM = {-2146826288: "#NULL!", -2146826281: "#DIV/0!", -2146826273: "#VALUE!", -2146826265: "#REF!", -2146826259: "#NAME?", -2146826252: "#NUM!", -2146826246: "#N/A"}


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def canerias() -> list[tuple[float, float]]:
    """(diámetro exterior cm, espesor cm) de las cañerías ACTIVAS del catálogo maestro (datos/canerias.csv)."""
    with open(RAIZ / "datos" / "canerias.csv", encoding="utf-8") as f:
        filas = [r for r in csv.DictReader(f) if r["estado"].strip().upper() == "ACTIVO"]
    return sorted({(float(r["diametro_ext_cm"]), float(r["espesor_cm"])) for r in filas})


def tramos_nuevos(rng: random.Random, tubos: list[tuple[float, float]], n: int, seccion: str) -> list[dict]:
    """Circular: cañerías del catálogo maestro. Cuadrada y octogonal: el catálogo no trae tubos ni perfiles
    (datos/tubos.csv vacío), así que las medidas se sortean en rangos plausibles. Son casos de PRUEBA del motor
    contra Excel, no productos de ORBE."""
    if seccion == "circular":
        return [{"altura_m": round(rng.uniform(0.5, 6.0), 2), "diametro_cm": d, "espesor_cm": e} for d, e in sorted(rng.sample(tubos, n))]
    if seccion == "cuadrada":
        return [{"altura_m": round(rng.uniform(2.0, 10.0), 2), "ancho_cm": round(rng.uniform(7.5, 30.0), 1), "espesor_cm": round(rng.uniform(0.2, 0.95), 3)}]
    dsup = round(rng.uniform(8.0, 25.0), 1)
    return [{"altura_m": round(rng.uniform(6.0, 20.0), 2), "diametro_superior_cm": dsup, "diametro_base_cm": round(dsup + rng.uniform(5.0, 35.0), 1),
             "espesor_cm": round(rng.uniform(0.3, 0.8), 3)}]


def config_nueva(rng: random.Random, tubos: list[tuple[float, float]], n: int, ganchos: int, seccion: str = "circular") -> dict:
    """Configuración plausible y nueva. Tramos en el orden de la planilla: el de arriba primero (el más delgado)."""
    cfg: dict = {
        "_origen": "fase3_excel.py (generada)",
        "seccion": seccion,
        "ganchos": ganchos,
        "tramos": tramos_nuevos(rng, tubos, n, seccion),
        "sobrecarga_kg": round(rng.uniform(5, 80), 1),
        "viento_tablero_kg": round(rng.choice([0, rng.uniform(5, 120)]), 1),
        "viento": {"velocidad_kmh": rng.choice([80, 100, 110, 120, 140, 160])},
    }
    if seccion == "octogonal" and ganchos == 2:
        cfg["cable_lateral_kg"] = round(rng.uniform(0, 400), 1)
    if ganchos == 0:
        cfg["proyectores"] = {"alto_cm": round(rng.uniform(20, 80)), "ancho_cm": round(rng.uniform(30, 120))}
    elif seccion == "cuadrada":
        d1 = round(rng.uniform(20, 60))
        cfg["gancho"] = {"d1_cm": d1, "d2_cm": round(rng.uniform(20, 80)), "d3_cm": round(rng.uniform(5, min(15, d1 - 5))), "t_cm": rng.choice([0, round(rng.uniform(5, 40))])}
    else:
        dg, eg = rng.choice([t for t in tubos if 4 <= t[0] <= 20] or tubos)
        cfg["gancho"] = {
            "diametro_cm": dg,
            "espesor_cm": eg,
            "radio_cm": round(rng.uniform(40, 200)),
            "t_cm": rng.choice([0, round(rng.uniform(1, 5), 1)]),
            "distancia_cm": round(rng.uniform(30, 200)),
        }
    # opcionales que la planilla deja editar (herramientas/fase3_bloqueos.py). coef_forma, amortiguamiento,
    # coef_von_karman, g, e y fs_pandeo_general están bloqueados en las hojas protegidas: quedan en su valor por omisión.
    for clave, opciones in {"fy_kgcm2": [2400, 2530, 3500], "pernos": [4, 6, 8]}.items():
        if rng.random() < 0.5:
            cfg[clave] = rng.choice(opciones)
    return cfg


def iguales(motor, excel, tol: float) -> bool:
    if es_error(motor):
        return excel == motor.codigo
    if isinstance(motor, bool) or isinstance(excel, bool):
        return motor == excel
    if isinstance(motor, (int, float)) and isinstance(excel, (int, float)):
        return math.isclose(motor, excel, rel_tol=tol, abs_tol=1e-9)
    if motor in (None, "") and excel in (None, ""):
        return True
    if isinstance(motor, (int, float)) and excel in (None, ""):
        return motor == 0
    return motor == excel


def dif_relativa(a, b) -> float | None:
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        return abs(a - b) / max(abs(a), abs(b), 1e-12)
    return None


def leer_hoja(ws) -> dict[str, object]:
    """Todos los valores calculados de la hoja en una sola llamada COM (UsedRange.Value2)."""
    from motor.excel import col_letras

    ur = ws.UsedRange
    f0, c0 = ur.Row, ur.Column
    datos = ur.Value2
    if not isinstance(datos, tuple):
        datos = ((datos,),)
    out = {}
    for i, fila in enumerate(datos):
        for j, v in enumerate(fila):
            if isinstance(v, int) and v in ERRORES_COM:
                v = ERRORES_COM[v]
            out[f"{col_letras(c0 + j)}{f0 + i}"] = v
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--por-hoja", type=int, default=10)
    ap.add_argument("--semilla", type=int, default=20261110)
    ap.add_argument("--tol", type=float, default=1e-9)
    ap.add_argument("--secciones", default="circular,cuadrada,octogonal", help="secciones a recalcular, separadas por coma")
    a = ap.parse_args()
    secciones = set(a.secciones.split(","))

    modelo, libro = _modelo()
    plantilla = RAIZ / "insumos" / modelo["origen"]["archivo"]
    sha_antes = sha256(plantilla)
    if sha_antes != modelo["origen"]["sha256"]:
        print(f"La plantilla no coincide con el modelo extraído ({sha_antes[:12]}… ≠ {modelo['origen']['sha256'][:12]}…)")
        return 3
    salida = RAIZ / "trabajo" / "fase3"
    salida.mkdir(parents=True, exist_ok=True)
    for vieja in salida.glob("copia_*.xlsm"):  # copias que Excel no soltó en corridas anteriores
        try:
            vieja.unlink()
        except OSError:
            print(f"AVISO: sigue en uso {vieja}")
    copia = salida / f"copia_{int(time.time())}.xlsm"
    shutil.copy2(plantilla, copia)
    copia.chmod(0o666)  # insumos/ es de solo lectura y copy2 copia ese atributo: sin esto la copia no se puede borrar

    import pythoncom
    import win32com.client as win32

    pythoncom.CoInitialize()
    excel = win32.DispatchEx("Excel.Application")
    wb = ws = None
    resultados, diferencias, rechazadas = [], [], []
    conteo = Counter()
    t0 = time.time()
    try:
        excel.Visible = False
        excel.DisplayAlerts = False
        excel.ScreenUpdating = False
        excel.EnableEvents = False
        excel.AutomationSecurity = 3  # msoAutomationSecurityForceDisable: no ejecuta macros
        wb = excel.Workbooks.Open(str(copia), UpdateLinks=0, ReadOnly=False, AddToMru=False)
        excel.Calculation = -4135  # manual: se recalcula solo con CalculateFull
        # Las hojas vienen protegidas con contraseña: NO se desprotegen ni se prueban contraseñas. Se escribe solo en
        # las celdas desbloqueadas (las que puede editar un usuario real). Si una configuración necesita otro valor en
        # una celda bloqueada, se fija esa celda a su valor original con la clave "celdas" del motor: así el motor y
        # Excel calculan con lo mismo (herramientas/fase3_bloqueos.py lista esas celdas).
        rng = random.Random(a.semilla)
        tubos = canerias()
        originales: dict[tuple[str, str], object] = {}

        def entradas_de(r):
            out = {}
            for ref, v in r["entradas_celdas"].items():
                h, c = re.fullmatch(r"'(.+)'!([A-Z]+\d+)", ref).groups()
                out[(h, c)] = v
            return out

        def mismo(a_, b_):
            if isinstance(a_, (int, float)) and isinstance(b_, (int, float)):
                return math.isclose(a_, b_, rel_tol=1e-12, abs_tol=1e-12)
            return str(a_).strip().upper() == str(b_).strip().upper()

        for (seccion, n, ganchos), hoja in HOJAS.items():
            if seccion not in secciones:
                continue
            ws = wb.Worksheets(hoja)
            protegida = bool(ws.ProtectContents)
            formulas = [c for c, d in modelo["celdas"][hoja].items() if d.get("f") is not None]
            for k in range(a.por_hoja):
                cfg = config_nueva(rng, tubos, n, ganchos, seccion)
                try:
                    r = validar(cfg)
                    fijadas = {}
                    if protegida:
                        for (h, c), v in entradas_de(r).items():
                            orig = modelo["celdas"][h].get(c, {}).get("v")
                            if ws.Range(c).Locked and not mismo(v, orig):
                                fijadas[c] = orig
                    if fijadas:
                        cfg["celdas"] = {**cfg.get("celdas", {}), **fijadas}
                        cfg["_celdas_bloqueadas_fijadas"] = sorted(fijadas)
                        conteo["casos_con_celdas_bloqueadas_fijadas"] += 1
                        r = validar(cfg)
                except ErrorConfig as e:
                    rechazadas.append({"hoja": hoja, "config": cfg, "error": str(e)})
                    continue
                entradas = entradas_de(r)
                # restaurar lo escrito antes y escribir la configuración nueva (solo celdas que cambian)
                for (h, c), v in originales.items():
                    if (h, c) not in entradas:
                        wb.Worksheets(h).Range(c).Value = v
                for (h, c), v in entradas.items():
                    orig = modelo["celdas"][h].get(c, {}).get("v")
                    if protegida and ws.Range(c).Locked:
                        if not mismo(v, orig):
                            raise RuntimeError(f"{hoja}!{c} está bloqueada y la configuración pide {v!r} (original {orig!r})")
                        continue
                    originales.setdefault((h, c), orig)
                    wb.Worksheets(h).Range(c).Value = v
                excel.CalculateFull()
                xl = leer_hoja(ws)
                calc = libro.calculo(entradas)
                malas, max_rel = 0, 0.0
                for c in formulas:
                    try:
                        mv = calc.valor(hoja, c)
                    except Exception as e:  # noqa: BLE001
                        mv = f"EXCEPCIÓN {type(e).__name__}: {e}"
                    xv = xl.get(c)
                    d = dif_relativa(mv, xv)
                    if d is not None:
                        max_rel = max(max_rel, d)
                    if not iguales(mv, xv, a.tol):
                        # Excel lleva a 0 una resta cuyo resultado es despreciable frente a sus operandos; el motor deja
                        # el residuo de redondeo. Se cuenta APARTE (no se esconde) y se lista con su fórmula.
                        cancelacion = xv == 0 and isinstance(mv, float) and abs(mv) < 1e-6 and "-" in modelo["celdas"][hoja][c]["f"]
                        if cancelacion:
                            conteo["formulas_cancelacion_numerica"] += 1
                        else:
                            malas += 1
                        if len(diferencias) < 200:
                            diferencias.append({"hoja": hoja, "caso": k, "celda": c, "tipo": "cancelación numérica (Excel da 0)" if cancelacion else "DISTINTA", "formula": modelo["celdas"][hoja][c]["f"][:120], "motor": repr(mv), "excel": repr(xv)})
                # veredictos: el estado del motor contra el texto que escribe Excel
                verd_malos = 0
                for v in r["verificaciones"]:
                    celda = v["celda"].split("!")[1]
                    texto = xl.get(celda)
                    if v["estado"] == "no verificado":
                        continue
                    ok_excel = isinstance(texto, str) and texto.strip().upper().startswith("OK")
                    if (v["estado"] == "cumple") != ok_excel:
                        verd_malos += 1
                conteo["formulas"] += len(formulas)
                conteo["formulas_distintas"] += malas
                conteo["veredictos"] += len(r["verificaciones"])
                conteo["veredictos_distintos"] += verd_malos
                conteo[f"resumen {r['resumen']}"] += 1
                resultados.append({"hoja": hoja, "caso": k, "resumen": r["resumen"], "formulas": len(formulas), "distintas": malas, "max_dif_relativa": max_rel, "veredictos_distintos": verd_malos, "config": cfg})
    finally:
        # cerrar sin guardar y soltar TODAS las referencias COM; si no, Excel queda vivo y no suelta la copia
        try:
            if wb is not None:
                wb.Close(SaveChanges=False)
        except Exception:  # noqa: BLE001
            pass
        ws = wb = None
        import gc

        gc.collect()
        excel.Quit()
        excel = None
        gc.collect()
        pythoncom.CoUninitialize()
        for _ in range(120):  # Excel puede tardar varios segundos en soltar el archivo después de Quit
            try:
                copia.unlink()
                break
            except OSError:
                time.sleep(0.5)
        if copia.exists():
            print(f"AVISO: no se pudo borrar la copia temporal {copia}")
    sha_despues = sha256(plantilla)
    informe = {
        "semilla": a.semilla,
        "por_hoja": a.por_hoja,
        "tolerancia_relativa": a.tol,
        "plantilla": {"archivo": modelo["origen"]["archivo"], "sha256_antes": sha_antes, "sha256_despues": sha_despues, "intacta": sha_antes == sha_despues},
        "segundos": round(time.time() - t0, 1),
        "casos": len(resultados),
        "rechazadas": rechazadas,
        "conteo": dict(conteo),
        "max_dif_relativa": max((x["max_dif_relativa"] for x in resultados), default=0.0),
        "diferencias": diferencias,
        "resultados": resultados,
    }
    archivo = salida / f"resultado_{a.semilla}.json"
    archivo.write_text(json.dumps(informe, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(resultados)} casos nuevos en {len({x['hoja'] for x in resultados})} hojas ({informe['segundos']} s); rechazadas por configuración: {len(rechazadas)}")
    print(f"fórmulas comparadas: {conteo['formulas']}, distintas: {conteo['formulas_distintas']} (tolerancia relativa {a.tol})")
    print(f"aparte (no cuentan como distintas), por cancelación numérica (Excel da 0, el motor un residuo < 1e-6): {conteo['formulas_cancelacion_numerica']}")
    print(f"veredictos comparados: {conteo['veredictos']}, distintos: {conteo['veredictos_distintos']}")
    print("resúmenes:", {k: v for k, v in conteo.items() if k.startswith("resumen")})
    print(f"máxima diferencia relativa: {informe['max_dif_relativa']:.3e}")
    print(f"plantilla intacta: {informe['plantilla']['intacta']}")
    for d in diferencias[:15]:
        print("  ", d)
    print(f"detalle: {archivo.relative_to(RAIZ)}")
    return 0 if conteo["formulas_distintas"] == 0 and conteo["veredictos_distintos"] == 0 and informe["plantilla"]["intacta"] else 1


if __name__ == "__main__":
    sys.exit(main())
