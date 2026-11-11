"""Tablas comerciales para el motor y el buscador, tomadas de CATALOGO_MAESTRO_ORBE (hoja MATERIALES). Solo lee.

Separa cañería de tubo (no se mezclan), y deja fuera costos y precios.
Uso (desde estructural/): python herramientas/catalogo_a_csv.py insumos/catalogo_maestro_v7.xlsx datos/
"""
import csv
import hashlib
import re
import sys
import warnings
from pathlib import Path

import openpyxl

CAMPOS_PERFIL = ["material_id", "norma", "medida", "diametro_ext_mm", "espesor_mm", "diametro_ext_cm", "espesor_cm", "kg_m", "largo_barra_m", "estado", "origen_suministro", "fuente"]


def main(xlsx: Path, salida: Path) -> None:
    warnings.filterwarnings("ignore")
    salida.mkdir(parents=True, exist_ok=True)
    wb = openpyxl.load_workbook(xlsx, data_only=True, read_only=True)
    ws = wb["MATERIALES"]
    filas = list(ws.iter_rows(values_only=True))
    enc = [str(x) if x is not None else "" for x in filas[3]]
    i = {k: enc.index(k) for k in enc if k}
    h = hashlib.sha256(xlsx.read_bytes()).hexdigest()[:16]
    canerias, tubos, placas, pernos, avisos = [], [], [], [], []
    for n, f in enumerate(filas[4:], start=5):
        if not any(f):
            continue
        cat = (f[i["CATEGORIA"]] or "").strip().upper()
        fuente = f"{xlsx.name} (sha256 {h}…) MATERIALES fila {n}"
        if cat in ("CAÑERÍA", "CAÑERIA", "TUBO"):
            d, e, kg = f[i["DIAM_EXT_MM"]], f[i["ESPESOR_MM"]], f[i["KG_M"]]
            largo = f[i["LARGO_BARRA_MM"]]
            # el catálogo trae el largo de barra de las cañerías como 6 (en m) en una columna en mm; los perfiles traen 6000
            largo_m = (largo / 1000 if largo and largo > 100 else largo) if largo else None
            if largo and largo <= 100:
                avisos.append(f"{f[i['MATERIAL_ID']]}: LARGO_BARRA_MM = {largo} (se leyó como metros)")
            fila = {
                "material_id": f[i["MATERIAL_ID"]],
                "norma": f[i["NORMA"]],
                "medida": f[i["MEDIDA"]],
                "diametro_ext_mm": d,
                "espesor_mm": e,
                "diametro_ext_cm": round(d / 10, 4) if d else None,
                "espesor_cm": round(e / 10, 4) if e else None,
                "kg_m": round(kg, 4) if kg is not None else None,
                "largo_barra_m": largo_m,
                "estado": f[i["ESTADO"]],
                "origen_suministro": f[i["ORIGEN_SUMINISTRO"]],
                "fuente": fuente,
            }
            (tubos if cat == "TUBO" else canerias).append(fila)
        elif cat == "PLACA BASE":
            desc = f[i["DESCRIPCION"]] or ""
            m = re.search(r"(\d+)\s*[Xx×]\s*(\d+)\s*[Xx×]\s*(\d+)", desc)
            placas.append(
                {
                    "material_id": f[i["MATERIAL_ID"]],
                    "descripcion": desc,
                    "lado_a_mm": int(m.group(1)) if m else None,
                    "lado_b_mm": int(m.group(2)) if m else None,
                    "espesor_mm": f[i["ESPESOR_MM"]],
                    "kg": f[i["KG_BARRA"]],
                    "estado": f[i["ESTADO"]],
                    "fuente": fuente,
                }
            )
        elif cat == "CANASTILLO" and (f[i["DESCRIPCION"]] or "").upper().startswith("PERNO"):
            desc = f[i["DESCRIPCION"]]
            m = re.search(r"PERNO\s+(\d+/\d+|\d+)\s*x\s*(\d+)\s*mm", desc, re.I)
            pernos.append(
                {
                    "material_id": f[i["MATERIAL_ID"]],
                    "descripcion": desc,
                    "diametro_pulg": m.group(1) if m else None,
                    "largo_mm": int(m.group(2)) if m else None,
                    "estado": f[i["ESTADO"]],
                    "origen_suministro": f[i["ORIGEN_SUMINISTRO"]],
                    "fuente": fuente,
                }
            )

    def escribir(nombre, filas, campos):
        with open(salida / nombre, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=campos)
            w.writeheader()
            w.writerows(filas)

    escribir("canerias.csv", canerias, CAMPOS_PERFIL)
    escribir("tubos.csv", tubos, CAMPOS_PERFIL)
    escribir("placas_base.csv", placas, ["material_id", "descripcion", "lado_a_mm", "lado_b_mm", "espesor_mm", "kg", "estado", "fuente"])
    escribir("pernos_anclaje.csv", pernos, ["material_id", "descripcion", "diametro_pulg", "largo_mm", "estado", "origen_suministro", "fuente"])
    print(f"cañerías: {len(canerias)}, tubos: {len(tubos)}, placas: {len(placas)}, pernos: {len(pernos)}")
    for a in avisos[:3]:
        print("aviso:", a)
    if len(avisos) > 3:
        print(f"aviso: … y {len(avisos) - 3} más con el mismo problema")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
