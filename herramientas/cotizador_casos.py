"""Casos al azar para probar el cotizador contra el motor exacto (sin grilla).

Para cada caso calcula con la misma fórmula del cotizador la fuerza en la punta (EPA × presión de la planilla) y el
peso, y corre validar() con esos valores exactos. Escribe trabajo/cotizador/casos.json; lo lee cotizador_test.mjs.
Uso (desde estructural/): .venv/Scripts/python herramientas/cotizador_casos.py [n]
"""
import csv
import json
import math
import random
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "herramientas"))
from cotizador_datos import cfg_cuadrado, cfg_facetado, cfg_tubular  # noqa: E402
from motor.validador import validar  # noqa: E402
from recetas_tubulares import recetas  # noqa: E402

d = json.loads((RAIZ / "trabajo" / "cotizador" / "datos.json").read_text(encoding="utf-8"))
p_ = d["presion"]
tub = {r["codigo"]: r["cuerpos"] for r in recetas()}
cuad = {r["codigo"]: r for r in csv.DictReader(open(RAIZ / "datos" / "postes_cuadrados_recetario.csv", encoding="utf-8"))}
fac = {r["codigo"]: r for r in csv.DictReader(open(RAIZ / "datos" / "postes_facetados_recetario.csv", encoding="utf-8"))}


def q(h, v):
    return (p_["hasta_4m"] if h <= 4 else p_["a"] * math.log(h) + p_["b"]) * (v / p_["v_ref"]) ** 2


rng = random.Random(20261111)
casos = []
n = int(sys.argv[1]) if len(sys.argv) > 1 else 400
candidatos = [x for x in d["postes"] if x["capacidad"]]
# la mitad de los casos son tubulares: son los únicos que pueden salir "Disponible"
tubulares = [x for x in candidatos if x["tipo"] == "tubular"]
while len(casos) < n:
    x = rng.choice(tubulares if len(casos) % 2 == 0 else candidatos)
    V = rng.choice(d["velocidades"])
    N, kg, epa, sop = rng.choice([1, 1, 2, 3, 4]), round(rng.uniform(3, 35), 1), round(rng.uniform(0.02, 0.6), 2), rng.choice([0, 0, 5, 12])
    F, P = N * epa * q(x["altura_m"], V), N * kg + sop
    if P > d["pesos"][-1]:
        continue
    cfg = cfg_tubular(tub[x["codigo"]], V, F, P) if x["tipo"] == "tubular" else cfg_cuadrado(cuad[x["codigo"]], V, F, P) if x["tipo"] == "cuadrado" else cfg_facetado(fac[x["codigo"]], V, F, P)
    casos.append({"codigo": x["codigo"], "tipo": x["tipo"], "V": V, "N": N, "kg": kg, "epa": epa, "sop": sop, "F": F, "P": P, "motor": validar(cfg)["resumen"]})
(RAIZ / "trabajo" / "cotizador" / "casos.json").write_text(json.dumps(casos), encoding="utf-8")
print(len(casos), "casos ·", {k: sum(c["motor"] == k for c in casos) for k in ("cumple", "no cumple", "error")})
