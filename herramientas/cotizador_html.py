"""Arma las dos versiones del cotizador (un solo HTML cada una, sin internet) con trabajo/cotizador/datos.json.

Salida en ../insumos/interno_NO_PUBLICAR/cotizador/:
  - cotizador_interno.html     costos, partidas y margen elegible. Solo para quien administra precios.
  - cotizador_vendedores.html  solo precio de venta. Sus datos NO contienen costos, partidas ni márgenes
                               (se eliminan aquí, no se ocultan en pantalla). Precio = costo ÷ (1 − margen de venta).
Ninguna de las dos se publica: uso interno de ORBE.

Uso (desde estructural/): .venv/Scripts/python herramientas/cotizador_html.py [margen_vendedores, por omisión 0.30]
"""
import copy
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
datos = json.loads((RAIZ / "trabajo" / "cotizador" / "datos.json").read_text(encoding="utf-8"))
plantilla = (RAIZ / "herramientas" / "cotizador_plantilla.html").read_text(encoding="utf-8")
assert plantilla.count("/*DATOS*/") == 1
margen = float(sys.argv[1]) if len(sys.argv) > 1 else datos["comercial"]["margen_minimo"]
assert datos["comercial"]["margen_minimo"] <= margen < 1, "el margen de venta no puede ser menor que el mínimo"

sys.path.insert(0, str(RAIZ / "herramientas"))
from accesorios_recetario import accesorios  # noqa: E402

datos["accesorios"] = accesorios()   # hojas ACCESORIOS, BRAZOS RECTOS y GANCHOS CURVOS del recetario (con costo)
for p in datos["postes"]:            # costos al peso: el recetario trae decimales (97.138,4)
    p["costo"] = round(p["costo"])
interno = copy.deepcopy(datos)
interno["modo"] = "interno"

vend = copy.deepcopy(datos)
vend["modo"] = "vendedor"
for a in vend["accesorios"]:   # vendedores: solo precio; sin costo ni notas internas
    a["precio"] = round(a["costo"] / (1 - margen)) if a["costo"] else None
    a.pop("costo", None)
    a.pop("nota", None)
SOLO_INTERNO = ("costo", "costo_origen", "costo_recalculado", "partidas", "notas")
for p in vend["postes"]:
    p["precio"] = round(p["costo"] / (1 - margen))
    for k in SOLO_INTERNO:
        p.pop(k, None)
c = vend["comercial"]
vend["comercial"] = {"iva": c["iva"], "flete_santiago": c["flete_santiago"], "viento_por_omision": c["viento_por_omision"], "margenes": [], "margen_minimo": 0}

salida = RAIZ.parent / "insumos" / "interno_NO_PUBLICAR" / "cotizador"
salida.mkdir(parents=True, exist_ok=True)
viejo = salida / "cotizador_postes.html"   # versión del 11-11 basada en los planos REV. M (reemplazada)
if viejo.exists():
    viejo.unlink()
sys.stdout.reconfigure(encoding="utf-8")
for nombre, d in (("cotizador_interno.html", interno), ("cotizador_vendedores.html", vend)):
    js = json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = plantilla.replace("/*DATOS*/", js)
    (salida / nombre).write_text(html, encoding="utf-8", newline="\n")
    print(f"{nombre} · {len(html) / 1024:.0f} KB")
texto = (salida / "cotizador_vendedores.html").read_text(encoding="utf-8")
datos_v = texto[texto.index("const D = "):texto.index("const INT")]
for palabra in ('"costo', '"partidas"', '"margen_minimo":0.', "galvanizado", "Acero ("):
    assert palabra not in datos_v, f"la versión de vendedores contiene {palabra!r}"
print(f"versión de vendedores: precio con margen {margen:.0%}, sin costos en sus datos (comprobado)")
