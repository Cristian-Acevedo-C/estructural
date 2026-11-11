"""validar(config) → verificaciones de un poste, replicando la Plantilla Memoria de Cálculo.

La hoja de la planilla se elige por sección, cantidad de tramos y de ganchos. Las entradas se ubican por sus rótulos
dentro de la planilla (no hay coordenadas escritas a mano) y cada verificación se lee de la fórmula de su veredicto:
lo que compara (valor), contra qué (límite), la razón de uso y si la planilla dice que cumple.

Lo que la planilla no verifica de verdad (por ejemplo el gancho, que tiene un 0 escrito a mano) sale como
"no verificado", nunca como "cumple". Ver docs/ESPECIFICACION.md y docs/MOTOR.md.
"""
from __future__ import annotations

import json
import re
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

from .excel import Analizador, Libro, col_letras, col_num, es_error

MODELO = Path(__file__).resolve().parent / "modelo" / "plantilla_B.json"

# hoja de la planilla según sección, cantidad de tramos y de ganchos
HOJAS = {
    ("circular", 1, 0): "P.Recto Circ.",
    ("circular", 1, 1): "P.Recto Circ. 1 gancho",
    ("circular", 1, 2): "P.Recto Circ. 2 ganchos",
    ("circular", 2, 0): "P.Var.2 Tramos Circ.",
    ("circular", 2, 1): "P.Var. 2 Tramos Circ. 1 gancho",
    ("circular", 2, 2): "P.Var. 2 Tramos Circ. 2 ganchos",
    ("circular", 3, 0): "P.Var.3 Tramos Circ.",
    ("circular", 3, 1): "P.Var.3 Tramos Circ. 1 gancho",
    ("circular", 3, 2): "P.Var.3 Tramos Circ. 2 ganchos",
    ("circular", 4, 0): "P.Var.4 Tramos Circ.",
    ("circular", 4, 1): "P.Var.4 Tramos Circ. 1 gancho",
    ("circular", 4, 2): "P.Var.4 Tramos Circ. 2 ganchos",
    # Fase 5: sección cuadrada constante y octogonal variable (un solo cuerpo)
    ("cuadrada", 1, 0): "P.Recto Cuad.",
    ("cuadrada", 1, 1): "P.Recto Cuad. 1 gancho",
    ("cuadrada", 1, 2): "P.Recto Cuad. 2 ganchos",
    ("octogonal", 1, 0): "P.Var. Octogonal",
    ("octogonal", 1, 1): "P.Var. Octogonal 1 gancho",
    ("octogonal", 1, 2): "P.Var. Octogonal 2 ganchos",
}
SECCION_DE_HOJA = {h: s for (s, _, _), h in HOJAS.items()}

# claves de cada tramo según la sección (las dimensiones en cm, la altura en m)
TRAMO_CLAVES = {
    "circular": ("altura_m", "diametro_cm", "espesor_cm"),
    "cuadrada": ("altura_m", "ancho_cm", "espesor_cm"),
    "octogonal": ("altura_m", "diametro_superior_cm", "diametro_base_cm", "espesor_cm"),
}
# Rótulos de las hojas cuadradas y octogonales (valor en la fila de abajo). Tienen otra disposición que las circulares:
# en la cuadrada sin gancho los datos van en la columna B, el gancho cuadrado se describe con d1, d2, d3 y t, y la
# octogonal de 2 ganchos agrega el cable lateral H y pone el viento sobre el tablero bajo su rótulo de texto.
ROTULOS_NO_CIRCULAR_TRAMO = [
    (r"^h \(m\)$", "altura_m"),
    (r"^B \(cm\)$", "ancho_cm"),
    (r"^d sup\. \(cm\)$", "diametro_superior_cm"),
    (r"^d base\s*\(cm\)$", "diametro_base_cm"),
]
ROTULOS_NO_CIRCULAR_GANCHO = {
    "cuadrada": [(r"^d1 \(cm\)$", "d1_cm"), (r"^d2 \(cm\)$", "d2_cm"), (r"^d3 \(cm\)$", "d3_cm"), (r"^t \(cm\)$", "t_cm")],
    "octogonal": [(r"^d \(cm\)$", "diametro_cm"), (r"^R \(cm\)$", "radio_cm"), (r"^t \(cm\)$", "t_cm"), (r"^Dist \(cm\)$", "distancia_cm")],
}
ROTULOS_NO_CIRCULAR_CARGAS = [(r"^P \(Kg\)$", "sobrecarga_kg"), (r"^V \(Kg\)$", "viento_tablero_kg"), (r"^H \(Kg\)$", "cable_lateral_kg")]

# valores por omisión: los que la planilla trae en todas sus hojas (se informan como supuestos en la salida)
POR_OMISION = {
    "fy_kgcm2": 2400,
    "coef_forma": 0.6,
    "amortiguamiento": 0.02,
    "coef_von_karman": 0.2,
    "g_kgcm2": 840000,
    "e_kgcm2": 2100000,
    "fs_pandeo_general": 1.67,
    "pernos": 4,
}
# el coeficiente de forma depende de la sección: es el valor (bloqueado) que la planilla trae en esas hojas
POR_OMISION_SECCION = {"cuadrada": {"coef_forma": 1.6}, "octogonal": {"coef_forma": 0.7}}

# rótulo de la planilla → clave de la configuración (entradas generales, valor a la derecha del rótulo)
ROTULOS = [
    (r"^Tension de Fluencia Fy", "fy_kgcm2"),
    (r"^Coef\. Forma", "coef_forma"),
    (r"^b$", "amortiguamiento"),
    (r"^CL$", "coef_von_karman"),
    (r"^G \(Kg/cm2\)", "g_kgcm2"),
    (r"^E \(kg/cm2\)", "e_kgcm2"),
    (r"^Altura de proyectores", "proyectores_alto_cm"),
    (r"^Ancho total de proyectores", "proyectores_ancho_cm"),
    (r"^FS$", "fs_pandeo_general"),
    (r"^Número de pernos", "pernos"),
    (r"^Desea ingresar velocidad del viento", "viento_usar_velocidad"),
]
# rótulos con el valor debajo (fila siguiente)
ROTULO_ARRIBA = re.compile(r"^(h\d?|d\d?|e\d?|P|V|R|Dist|t) \((m|cm|Kg)\)$")


class ErrorConfig(ValueError):
    pass


@lru_cache(maxsize=1)
def _modelo():
    m = json.loads(MODELO.read_text(encoding="utf-8"))
    return m, Libro(m["celdas"])


BLOQUEADAS = Path(__file__).resolve().parent / "modelo" / "bloqueadas_B.json"


@lru_cache(maxsize=1)
def _bloqueadas() -> dict:
    """Entradas que la planilla protege (Locked en hojas protegidas). Generado por herramientas/extraer_bloqueadas.py."""
    if not BLOQUEADAS.exists():
        return {}
    return json.loads(BLOQUEADAS.read_text(encoding="utf-8"))["hojas"]


def _mismo(a, b) -> bool:
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        return abs(a - b) <= 1e-12 * max(1.0, abs(a), abs(b))
    return str(a).strip().upper() == str(b).strip().upper()


def avisos_bloqueadas(hoja: str, entradas: dict[str, object]) -> list[str]:
    """Fase 3, hallazgo 1: avisa cuando la configuración cambia una entrada que la planilla no deja editar.
    No cambia el cálculo: el motor usa el valor pedido, pero quien hizo la planilla fijó ese valor."""
    out = []
    for celda, info in (_bloqueadas().get(hoja, {}).get("bloqueadas") or {}).items():
        if celda in entradas and not _mismo(entradas[celda], info["valor_planilla"]):
            out.append(
                f"{info['entrada']} ({celda}) está bloqueada en la planilla con {info['valor_planilla']!r}; se usó {entradas[celda]!r}. "
                "La planilla no deja cambiarla: confirmar con el calculista"
            )
    return out


def _rc(celda: str) -> tuple[int, int]:
    m = re.match(r"([A-Z]+)(\d+)$", celda)
    return col_num(m.group(1)), int(m.group(2))


def _txt(c: dict | None) -> str:
    if not c or c.get("f") is not None or not isinstance(c.get("v"), str):
        return ""
    return c["v"].strip()


def _referenciadas(hoja_celdas: dict) -> set[str]:
    usadas = set()
    for c in hoja_celdas.values():
        f = c.get("f")
        if f:
            for m in re.finditer(r"\$?([A-Z]{1,3})\$?(\d+)", re.sub(r'"[^"]*"', "", f)):
                usadas.add(f"{m.group(1)}{m.group(2)}")
    return usadas


@lru_cache(maxsize=32)
def mapa_hoja(hoja: str) -> dict:
    """Ubica en la hoja las celdas de entrada, los veredictos y las salidas, por sus rótulos."""
    modelo, libro = _modelo()
    celdas = modelo["celdas"][hoja]
    usadas = _referenciadas(celdas)
    # hojas sin configuración por nombres (cuadrado, octogonal): un tramo; se usan con "hoja" + "celdas"
    n_tramos = next((n for (s, n, g), h in HOJAS.items() if h == hoja), 1)
    entradas: dict[str, str] = {}
    tramos = [dict() for _ in range(n_tramos)]
    gancho: dict[str, str] = {}

    for celda, c in celdas.items():
        t = _txt(c)
        if not t:
            continue
        col, fila = _rc(celda)
        if col > 8:  # bloque auxiliar escondido (columnas I en adelante), salvo E y FS que se buscan abajo
            if not re.match(r"^E \(kg/cm2\)", t):
                continue
        m = ROTULO_ARRIBA.match(t)
        if m and col <= 8:
            abajo = f"{col_letras(col)}{fila + 1}"
            ca = celdas.get(abajo)
            if not ca or ca.get("f") is not None:
                continue
            letra = m.group(1)
            base = letra[0] if letra[0] in "hde" and len(letra) <= 2 else letra
            if base in ("h", "d", "e") and fila in (14, 17, 20) and col <= n_tramos:
                clave = {"h": "altura_m", "d": "diametro_cm", "e": "espesor_cm"}[base]
                tramos[col - 1][clave] = abajo
            elif base == "d":
                gancho["diametro_cm"] = abajo
            elif base == "e":
                gancho["espesor_cm"] = abajo
            elif letra == "R":
                gancho["radio_cm"] = abajo
            elif letra == "Dist":
                gancho["distancia_cm"] = abajo
            elif letra == "t":
                # hay dos "t" en algunas hojas: vale la que usa alguna fórmula
                if abajo in usadas or "t_cm" not in gancho:
                    gancho["t_cm"] = abajo
            elif letra == "P":
                entradas["sobrecarga_kg"] = abajo
            elif letra == "V":
                entradas["viento_tablero_kg"] = abajo
            continue
        for patron, clave in ROTULOS:
            if re.search(patron, t):
                # primer valor a la derecha en la misma fila: un número (o el texto SI/NO del viento), o una fórmula
                # que solo copia otra celda (=B52), en cuyo caso vale la celda copiada
                texto_ok = clave == "viento_usar_velocidad"
                for cc in range(col + 1, col + 9):
                    ref = f"{col_letras(cc)}{fila}"
                    x = celdas.get(ref)
                    if not x:
                        continue
                    if x.get("f"):
                        m2 = re.fullmatch(r"=\$?([A-Z]{1,3})\$?(\d+)", x["f"].strip())
                        if m2 and celdas.get(f"{m2.group(1)}{m2.group(2)}", {}).get("f") is None:
                            entradas[clave] = f"{m2.group(1)}{m2.group(2)}"
                            break
                        continue
                    v = x.get("v")
                    if isinstance(v, (int, float)) and not isinstance(v, bool) or (texto_ok and isinstance(v, str) and v.strip()):
                        entradas[clave] = ref
                        break
                break
        # velocidad del viento: a la derecha de la fórmula que escribe "V (km/hr) :"
    for celda, c in celdas.items():
        if c.get("f") and "V (km/hr)" in c["f"]:
            col, fila = _rc(celda)
            entradas["viento_velocidad_kmh"] = f"{col_letras(col + 1)}{fila}"

    # alturas del bloque auxiliar escondido que suman a la altura total (B15 = S12+T12+U12+A15 y equivalentes)
    ocultas = []
    for celda, c in celdas.items():
        f = c.get("f") or ""
        col, fila = _rc(celda)
        if fila == 15 and col <= 8 and f:
            for m in re.finditer(r"\$?([A-Z]{1,3})\$?(\d+)", f):
                ref = f"{m.group(1)}{m.group(2)}"
                if col_num(m.group(1)) > 8:
                    ocultas.append(ref)

    seccion = SECCION_DE_HOJA.get(hoja)
    if seccion in ("cuadrada", "octogonal"):
        tramos, gancho, cargas = _mapa_no_circular(seccion, celdas)
        for clave in ("sobrecarga_kg", "viento_tablero_kg", "cable_lateral_kg"):
            entradas.pop(clave, None)
        entradas.update(cargas)

    veredictos = _veredictos(hoja, celdas)
    salidas = _salidas(celdas)
    return {
        "hoja": hoja,
        "seccion": seccion,
        "n_tramos": n_tramos,
        "entradas": entradas,
        "tramos": tramos,
        "gancho": gancho,
        "alturas_ocultas": sorted(set(ocultas)),
        "veredictos": veredictos,
        "salidas": salidas,
    }


def _mapa_no_circular(seccion: str, celdas: dict) -> tuple[list[dict], dict, dict]:
    """Entradas de las hojas cuadradas y octogonales, por sus rótulos (valor constante en la fila de abajo).

    El espesor "e (cm)" aparece dos veces en las hojas octogonales con gancho: el de arriba (fila < 30) es el del
    poste y el de abajo es el del gancho."""
    tramo: dict[str, str] = {}
    gancho: dict[str, str] = {}
    cargas: dict[str, str] = {}
    texto_viento = None
    for celda, c in sorted(celdas.items(), key=lambda x: _rc(x[0])[::-1]):
        t = _txt(c)
        col, fila = _rc(celda)
        if not t or col > 8 or fila > 40:
            continue
        abajo = f"{col_letras(col)}{fila + 1}"
        ca = celdas.get(abajo)
        constante = bool(ca) and ca.get("f") is None and isinstance(ca.get("v"), (int, float)) and not isinstance(ca.get("v"), bool)
        if t == "Viento en el tablero" and constante:
            texto_viento = abajo
        if not constante:
            continue
        if re.match(r"^e \(cm\)$", t):
            (tramo if fila < 30 else gancho).setdefault("espesor_cm", abajo)
            continue
        for patron, clave in ROTULOS_NO_CIRCULAR_TRAMO:
            if re.match(patron, t):
                tramo.setdefault(clave, abajo)
        for patron, clave in ROTULOS_NO_CIRCULAR_GANCHO[seccion]:
            if re.match(patron, t):
                gancho.setdefault(clave, abajo)
        for patron, clave in ROTULOS_NO_CIRCULAR_CARGAS:
            if re.match(patron, t):
                cargas.setdefault(clave, abajo)
    if "viento_tablero_kg" not in cargas and texto_viento:
        cargas["viento_tablero_kg"] = texto_viento
    return [tramo], gancho, cargas


TITULOS = {
    "PANDEO GENERAL": "Pandeo general",
    "PANDEO LOCAL": "Pandeo local",
    "TENSIONES A LA FLEXION": "Flexión",
    "TENSIONES A LA TORSION": "Torsión",
    "INTERACCION FLEXO - COMPRESION": "Interacción flexo-compresión",
}
SUBTITULOS = ("Compresión uniforme", "Flexión pura")


def _seccion(celdas: dict, fila: int) -> tuple[str, str]:
    """Verificación (fila "VERIFICACION DE …" más cercana arriba) y subtítulo (Compresión uniforme / Flexión pura)."""
    titulo, sub = "", ""
    for f in range(fila, 0, -1):
        t = _txt(celdas.get(f"A{f}"))
        limpio = t.rstrip(":").strip()
        if not sub and limpio in SUBTITULOS:
            sub = limpio
        if t.upper().startswith("VERIFICACION"):
            resto = re.sub(r"^VERIFICACION DE\s+", "", t.upper()).strip()
            titulo = TITULOS.get(resto, t.capitalize())
            break
    return titulo, sub


def _rotulo_fila(celdas: dict, fila: int) -> str:
    for col in ("A", "B"):
        t = _txt(celdas.get(f"{col}{fila}"))
        if t:
            return t
    return ""


def _a_texto(n) -> str:
    """Árbol → fórmula legible (para mostrar el límite cuando es una expresión)."""
    t = n[0]
    if t == "num":
        v = n[1]
        return str(int(v)) if float(v).is_integer() else repr(v)
    if t == "ref":
        return f"{col_letras(n[2])}{n[3]}"
    if t == "bin":
        return f"{_a_texto(n[2])}{n[1]}{_a_texto(n[3])}"
    if t == "neg":
        return f"-{_a_texto(n[1])}"
    if t == "err":
        return n[1].codigo
    if t == "fn":
        return f"{n[1]}({','.join(_a_texto(a) for a in n[2] if a)})"
    if t == "txt":
        return f'"{n[1]}"'
    return str(n)


def _cadena_con_ref_rota(celdas: dict, celda: str, vistos: set | None = None) -> bool:
    """¿Alguna fórmula de la que depende esta celda (en la misma hoja) tiene #REF!?"""
    vistos = set() if vistos is None else vistos
    if celda in vistos:
        return False
    vistos.add(celda)
    f = (celdas.get(celda) or {}).get("f")
    if not f:
        return False
    if "#REF!" in f:
        return True
    texto = re.sub(r'"[^"]*"', "", f)
    for m in re.finditer(r"(?<![!A-Z])\$?([A-Z]{1,3})\$?(\d+)(?::\$?([A-Z]{1,3})\$?(\d+))?", texto):
        if m.group(3):
            for c in range(col_num(m.group(1)), col_num(m.group(3)) + 1):
                for fl in range(int(m.group(2)), int(m.group(4)) + 1):
                    if _cadena_con_ref_rota(celdas, f"{col_letras(c)}{fl}", vistos):
                        return True
        elif _cadena_con_ref_rota(celdas, f"{m.group(1)}{m.group(2)}", vistos):
            return True
    return False


def _veredictos(hoja: str, celdas: dict) -> list[dict]:
    out = []
    for celda, c in celdas.items():
        f = c.get("f") or ""
        if "OK!" not in f:
            continue
        arbol = Analizador(f, hoja).analizar()
        pre = []
        nodo = arbol
        comp = None
        while nodo[0] == "fn" and nodo[1] == "IF":
            cond, a, b = nodo[2][0], nodo[2][1], (nodo[2][2] if len(nodo[2]) > 2 else None)
            es_ok = lambda x: x is not None and x[0] == "txt" and x[1].strip().upper().startswith("OK")  # noqa: E731
            if es_ok(a) or es_ok(b):
                comp = {"op": cond[1], "valor": cond[2], "limite": cond[3], "ok_si_verdadero": es_ok(a)}
                break
            if b is not None and b[0] == "fn" and b[1] == "IF":
                pre.append({"condicion": _a_texto(cond), "mensaje": a[1] if a[0] == "txt" else _a_texto(a)})
                nodo = b
                continue
            break
        if not comp or cond[0] != "bin":
            continue
        _, fila = _rc(celda)
        valor_ref = comp["valor"]
        rota = _cadena_con_ref_rota(celdas, celda)
        titulo, sub = _seccion(celdas, fila)
        fila_rot = _rotulo_fila(celdas, fila)
        if not fila_rot and valor_ref[0] == "ref":
            fila_rot = _rotulo_fila(celdas, valor_ref[3])
        valor_es_constante = valor_ref[0] == "ref" and celdas.get(f"{col_letras(valor_ref[2])}{valor_ref[3]}", {}).get("f") is None
        # veredicto sobre el bloque auxiliar escondido (columnas I en adelante): no es parte del poste ingresado
        auxiliar = valor_ref[0] == "ref" and valor_ref[2] > 8
        out.append(
            {
                "celda": celda,
                "nombre": " · ".join(dict.fromkeys(x for x in (titulo, sub, fila_rot.rstrip(":").strip()) if x)),
                "bloque_auxiliar": auxiliar,
                "op": comp["op"],
                "ok_si_verdadero": comp["ok_si_verdadero"],
                "valor": _a_texto(valor_ref),
                "limite": _a_texto(comp["limite"]),
                "precondiciones": pre,
                "rota_en_planilla": rota,
                "valor_fijo_en_planilla": valor_es_constante,
            }
        )
    out.sort(key=lambda v: _rc(v["celda"])[1])
    return out


def _salidas(celdas: dict) -> dict[str, str]:
    """Reacciones, frecuencia, peso, pernos y placa: valor a la derecha del rótulo."""
    buscar = {
        "momento_base_kgcm": r"^M0$",
        "corte_base_kg": r"^V0$",
        "normal_base_kg": r"^N0$",
        "peso_propio_kg": r"^Peso propio$",
        "pernos_diametro_circulo_cm": r"^Diámetro \(cm\)$",
        "perno_carga_axial_kg": r"^Carga axial sobre c/ perno",
        "perno_area_traccion_cm2": r"^Area de tracción",
        "placa_espesor_cm": r"^Espesor Placa",
        "frecuencia_traslacion_hz": r"^f =$",
    }
    out = {}
    for clave, patron in buscar.items():
        for celda, c in celdas.items():
            if re.search(patron, _txt(c)):
                col, fila = _rc(celda)
                for cc in range(col + 1, col + 5):
                    x = celdas.get(f"{col_letras(cc)}{fila}")
                    if x and x.get("f"):
                        out[clave] = f"{col_letras(cc)}{fila}"
                        break
                if clave in out:
                    break
    # diámetro nominal del perno: tres celdas con la tabla por tramos de área (una sola tiene texto)
    nominal = [cel for cel, c in celdas.items() if c.get("f") and ('"3/4"' in c["f"] or '"1 1/8"' in c["f"] or '"1 3/4"' in c["f"])]
    out["perno_diametro_nominal"] = ",".join(sorted(nominal, key=lambda x: _rc(x)[1]))
    return out


# ---------------------------------------------------------------- configuración → celdas


def _num(cfg, clave, ruta, positivo=True):
    v = cfg.get(clave)
    if v is None:
        raise ErrorConfig(f"falta {ruta}{clave}")
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        raise ErrorConfig(f"{ruta}{clave} debe ser un número")
    if positivo and v <= 0:
        raise ErrorConfig(f"{ruta}{clave} debe ser mayor que 0")
    return float(v)


def elegir_hoja(config: dict) -> str:
    if config.get("hoja"):
        h = config["hoja"]
        _, libro = _modelo()
        if h not in libro.celdas:
            raise ErrorConfig(f"la planilla no tiene la hoja {h!r}")
        return h
    seccion = config.get("seccion", "circular")
    tramos = config.get("tramos") or []
    ganchos = int(config.get("ganchos", 0))
    clave = (seccion, len(tramos), ganchos)
    if clave not in HOJAS:
        raise ErrorConfig(f"no hay hoja para sección {seccion!r}, {len(tramos)} tramos y {ganchos} ganchos (disponibles: circular de 1 a 4 tramos; cuadrada y octogonal de 1 tramo; 0 a 2 ganchos)")
    return HOJAS[clave]


ORDENES = ("desde_arriba", "desde_base")


def orden_tramos(config: dict) -> str:
    """Orden de config["tramos"]: "desde_arriba" (el de la planilla, por omisión) o "desde_base" (la base primero)."""
    o = config.get("orden_tramos", "desde_arriba")
    if o not in ORDENES:
        raise ErrorConfig(f"orden_tramos debe ser {' o '.join(ORDENES)} (vino {o!r})")
    return o


def celdas_de_config(config: dict, hoja: str) -> tuple[dict[str, object], list[str], list[str]]:
    """Celdas de entrada (celda → valor), supuestos usados y avisos."""
    mapa = mapa_hoja(hoja)
    ent = mapa["entradas"]
    out: dict[str, object] = {}
    supuestos, avisos = [], []
    if config.get("hoja") and not config.get("tramos"):
        # modo celdas: solo lo que viene en "celdas"
        pass
    else:
        # la planilla pone el tramo de arriba primero; con "desde_base" la configuración trae la base primero
        desde_base = orden_tramos(config) == "desde_base"
        n = len(config["tramos"])
        en_planilla = list(reversed(config["tramos"])) if desde_base else config["tramos"]
        claves_tramo = TRAMO_CLAVES[mapa["seccion"] or "circular"]
        for i, (t, celdas) in enumerate(zip(en_planilla, mapa["tramos"])):
            ruta = f"tramos[{n - 1 - i if desde_base else i}]."
            sobran = [k for k in t if k not in claves_tramo and not k.startswith("_")]
            if sobran:
                raise ErrorConfig(f"{ruta}: claves que no corresponden a la sección {mapa['seccion']!r}: {sobran} (se esperan {list(claves_tramo)})")
            vals = {k: _num(t, k, ruta) for k in claves_tramo}
            e = vals["espesor_cm"]
            for k, d in vals.items():
                if k in ("altura_m", "espesor_cm"):
                    continue
                if 2 * e >= d:
                    raise ErrorConfig(f"{ruta}espesor_cm: el doble del espesor ({2 * e} cm) no puede ser mayor o igual a {k} ({d} cm)")
                if d > 100:
                    avisos.append(f"{ruta}{k} = {d} cm: ¿está en milímetros? La planilla trabaja en cm")
            for k, v in vals.items():
                out[celdas[k]] = v
        for clave in ("sobrecarga_kg", "viento_tablero_kg", "cable_lateral_kg"):
            if clave in ent:
                out[ent[clave]] = _num(config, clave, "", positivo=False)
        viento = config.get("viento") or {}
        if "velocidad_kmh" not in viento:
            raise ErrorConfig("falta viento.velocidad_kmh")
        out[ent["viento_usar_velocidad"]] = "SI"
        out[ent["viento_velocidad_kmh"]] = _num(viento, "velocidad_kmh", "viento.")
        if "proyectores_alto_cm" in ent:
            p = config.get("proyectores") or {}
            out[ent["proyectores_alto_cm"]] = _num(p, "alto_cm", "proyectores.", positivo=False)
            out[ent["proyectores_ancho_cm"]] = _num(p, "ancho_cm", "proyectores.", positivo=False)
        if mapa["gancho"]:
            g = config.get("gancho") or {}
            for clave, celda in mapa["gancho"].items():
                # t (barra recta del gancho) puede ser 0: la planilla lo acepta (sin tramo recto)
                out[celda] = _num(g, clave, "gancho.", positivo=clave != "t_cm")
        for clave, omision in {**POR_OMISION, **POR_OMISION_SECCION.get(mapa["seccion"], {})}.items():
            if clave not in ent:
                continue
            if clave in config:
                out[ent[clave]] = _num(config, clave, "")
            else:
                out[ent[clave]] = float(omision)
                supuestos.append(f"{clave} = {omision} (valor por omisión de la planilla)")
        # el bloque auxiliar escondido suma a la altura total: en 0, como en la planilla
        for celda in mapa["alturas_ocultas"]:
            out[celda] = 0.0
    for celda, v in (config.get("celdas") or {}).items():
        out[celda] = v
    return out, supuestos, avisos


# ---------------------------------------------------------------- validar


def _razon(valor, limite, op, ok_si_verdadero):
    if not isinstance(valor, (int, float)) or not isinstance(limite, (int, float)) or isinstance(valor, bool) or isinstance(limite, bool) or limite == 0:
        return None
    return valor / limite


CLAVES = {
    "seccion", "ganchos", "tramos", "gancho", "sobrecarga_kg", "viento_tablero_kg", "cable_lateral_kg", "viento", "proyectores",
    "hoja", "celdas", "incluir_rotas", "orden_tramos", *POR_OMISION,
}


def validar(config: dict) -> dict:
    """Verifica un poste. config: ver docs/MOTOR.md. Devuelve un dict serializable a JSON."""
    config = deepcopy(config)
    desconocidas = [k for k in config if k not in CLAVES and not k.startswith("_")]
    if desconocidas:
        raise ErrorConfig(f"claves desconocidas en la configuración: {desconocidas} (las que empiezan con _ se ignoran)")
    hoja = elegir_hoja(config)
    mapa = mapa_hoja(hoja)
    modelo, libro = _modelo()
    entradas, supuestos, avisos = celdas_de_config(config, hoja)
    avisos = avisos + avisos_bloqueadas(hoja, entradas)
    calc = libro.calculo({(hoja, c): v for c, v in entradas.items()})

    def val(expr: str):
        if re.fullmatch(r"[A-Z]{1,3}\d+", expr):
            return calc.valor(hoja, expr)
        return calc.ev(Analizador("=" + expr, hoja).analizar())

    def plano(v):
        if es_error(v):
            return v.codigo
        return v

    verificaciones = []
    incluir_rotas = bool(config.get("incluir_rotas"))
    for v in mapa["veredictos"]:
        if (v["rota_en_planilla"] or v["bloque_auxiliar"]) and not incluir_rotas:
            continue
        texto = calc.valor(hoja, v["celda"])
        valor, limite = val(v["valor"]), val(v["limite"])
        precond = []
        for p in v["precondiciones"]:
            r = calc.ev(Analizador("=" + p["condicion"], hoja).analizar())
            precond.append({"condicion": p["condicion"], "se_cumple_la_condicion_de_falla": plano(r), "mensaje": p["mensaje"]})
        if es_error(texto):
            estado = "error"
        elif v["valor_fijo_en_planilla"]:
            estado = "no verificado"
        else:
            estado = "cumple" if isinstance(texto, str) and texto.strip().upper().startswith("OK") else "no cumple"
        verificaciones.append(
            {
                "nombre": v["nombre"],
                "estado": estado,
                "cumple": estado == "cumple",
                "valor": plano(valor),
                "limite": plano(limite),
                "razon_de_uso": _razon(valor, limite, v["op"], v["ok_si_verdadero"]),
                "unidad": "—" if v["nombre"].startswith("Interacción") else "kg/cm²",
                "criterio": f"{v['valor']} {v['op']} {v['limite']} → {'cumple' if v['ok_si_verdadero'] else 'no cumple'}",
                "mensaje_planilla": plano(texto),
                "precondiciones": precond,
                "celda": f"'{hoja}'!{v['celda']}",
                **({"nota": "La planilla tiene un 0 escrito a mano en lugar de este cálculo: no se verifica"} if v["valor_fijo_en_planilla"] else {}),
            }
        )
    salidas = {}
    for clave, celda in mapa["salidas"].items():
        if clave == "perno_diametro_nominal":
            textos = [plano(calc.valor(hoja, c)) for c in celda.split(",") if c]
            textos = [t for t in textos if isinstance(t, str) and t.strip()]
            salidas[clave] = textos[0].strip() if textos else None
        else:
            salidas[clave] = plano(calc.valor(hoja, celda))
    salidas["pernos"] = entradas.get(mapa["entradas"].get("pernos", ""), None)
    estados = [v["estado"] for v in verificaciones]
    resumen = "no cumple" if "no cumple" in estados else ("error" if "error" in estados else "cumple")
    return {
        "hoja": hoja,
        "planilla": modelo["origen"],
        "orden_tramos": orden_tramos(config),
        "resumen": resumen,
        "alcance": "El resumen considera solo las verificaciones que tiene la planilla. Lo de 'no_verificado' queda pendiente.",
        "no_verificado": [v["nombre"] for v in verificaciones if v["estado"] == "no verificado"]
        + ["soldadura (la planilla no la verifica)", "deflexión (la planilla no la verifica)", "placa base y pernos (la planilla los dimensiona, no los verifica)"],
        "verificaciones": verificaciones,
        "salidas": salidas,
        "supuestos": supuestos,
        "avisos": avisos,
        "entradas_celdas": {f"'{hoja}'!{c}": v for c, v in sorted(entradas.items(), key=lambda x: (_rc(x[0])[1], _rc(x[0])[0]))},
    }


def config_desde_celdas(hoja: str, valores: dict[str, object]) -> dict:
    """Arma una configuración a partir de los valores de las celdas de entrada de una hoja (lo inverso de
    celdas_de_config). Sirve para reproducir una planilla guardada y para las pruebas contra Excel."""
    mapa = mapa_hoja(hoja)
    seccion, n, g = next(k for k, h in HOJAS.items() if h == hoja)
    ent = mapa["entradas"]
    cfg: dict = {"seccion": seccion, "ganchos": g, "tramos": []}
    for t in mapa["tramos"]:
        cfg["tramos"].append({k: valores[c] for k, c in t.items()})
    cfg["sobrecarga_kg"] = valores[ent["sobrecarga_kg"]]
    cfg["viento_tablero_kg"] = valores[ent["viento_tablero_kg"]]
    if "cable_lateral_kg" in ent:
        cfg["cable_lateral_kg"] = valores[ent["cable_lateral_kg"]]
    cfg["viento"] = {"velocidad_kmh": valores[ent["viento_velocidad_kmh"]]}
    if "proyectores_alto_cm" in ent:
        cfg["proyectores"] = {"alto_cm": valores[ent["proyectores_alto_cm"]], "ancho_cm": valores[ent["proyectores_ancho_cm"]]}
    if mapa["gancho"]:
        cfg["gancho"] = {k: valores[c] for k, c in mapa["gancho"].items()}
    for clave in POR_OMISION:
        if clave in ent:
            cfg[clave] = valores[ent[clave]]
    celdas = {}
    usar = valores.get(ent["viento_usar_velocidad"])
    if usar != "SI":
        celdas[ent["viento_usar_velocidad"]] = usar
    for c in mapa["alturas_ocultas"]:
        if valores.get(c) not in (None, 0, 0.0):
            celdas[c] = valores[c]
    if celdas:
        cfg["celdas"] = celdas
    return cfg


def tipos_disponibles() -> list[dict]:
    return [{"seccion": s, "tramos": n, "ganchos": g, "hoja": h} for (s, n, g), h in HOJAS.items()]
