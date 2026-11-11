"""Analiza un volcado (volcar_plantilla.py): por hoja, veredictos (CUMPLE / NO CUMPLE), su cadena de dependencias
hasta los datos de entrada, constantes escritas dentro de las fórmulas, normas citadas y referencias rotas. Solo lee.

Uso: python analizar.py <volcado> <salida.json> <anexo.md>
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from openpyxl.utils import column_index_from_string, get_column_letter

REF = re.compile(r"(?:(?:'([^']+)'|([A-Za-zÁÉÍÓÚÑáéíóúñ_.][\wÁÉÍÓÚÑáéíóúñ.]*))!)?\$?([A-Z]{1,3})\$?(\d+)(?::\$?([A-Z]{1,3})\$?(\d+))?")
NUM = re.compile(r"(?<![A-Z$\d.])(\d+(?:\.\d+)?(?:[Ee][-+]?\d+)?)(?![\d(])")
NORMA = re.compile(r"\b(nch|NCh|Nch|NCH|AISC|ASCE|AASHTO|ACI|AWS|ANSI|Eurocódigo|Eurocode|norma|Norma|NORMA|DS\s?\d+|D\.S\.)\b")
VEREDICTO = re.compile(r"CUMPLE|OK!|NO CUMPLE|CAMBIAR|AUMENT|DISMINU", re.I)


def coord(c):
    m = re.match(r"([A-Z]+)(\d+)", c)
    return column_index_from_string(m.group(1)), int(m.group(2))


def referencias(formula, hoja):
    """Celdas a las que apunta una fórmula: [(hoja, celda)]. Los rangos se expanden (hasta 400 celdas)."""
    out = []
    texto = re.sub(r'"[^"]*"', '""', formula)  # sin literales de texto
    for m in REF.finditer(texto):
        h = m.group(1) or m.group(2) or hoja
        c1, f1 = m.group(3), int(m.group(4))
        if m.group(5):
            c2, f2 = m.group(5), int(m.group(6))
            for col in range(column_index_from_string(c1), column_index_from_string(c2) + 1):
                for fila in range(f1, f2 + 1):
                    out.append((h, f"{get_column_letter(col)}{fila}"))
                    if len(out) > 400:
                        return out
        else:
            out.append((h, f"{c1}{f1}"))
    return out


def main(d: Path, salida: Path, anexo: Path):
    cs = json.loads((d / "celdas.json").read_text(encoding="utf-8"))
    celda = {(c["hoja"], c["celda"]): c for c in cs}
    por_hoja = defaultdict(list)
    for c in cs:
        por_hoja[c["hoja"]].append(c)

    def rotulo(h, ref):
        """Texto más cercano: misma fila a la izquierda, o la celda de arriba (rótulo sobre el valor)."""
        col, fila = coord(ref)
        for cc in range(col - 1, 0, -1):
            x = celda.get((h, f"{get_column_letter(cc)}{fila}"))
            if x and not x["formula"] and isinstance(x["constante"], str) and x["constante"].strip():
                return x["constante"].strip()
        for ff in (fila - 1, fila - 2):
            x = celda.get((h, f"{get_column_letter(col)}{ff}"))
            if x and not x["formula"] and isinstance(x["constante"], str) and x["constante"].strip():
                return x["constante"].strip()
        return ""

    resultado = {}
    md = [f"# Anexo generado: {d.name}", "", "Generado por `herramientas/analizar.py` a partir del volcado. No editar a mano.", ""]
    normas_libro = Counter()
    for c in cs:
        t = c["constante"] if isinstance(c["constante"], str) else (c["formula"] or "")
        for m in NORMA.finditer(str(t)):
            normas_libro[(c["hoja"], c["celda"], str(t).strip()[:160])] += 1

    for h, lista in por_hoja.items():
        formulas = [c for c in lista if c["formula"]]
        if not formulas:
            continue
        veredictos = [c for c in formulas if VEREDICTO.search(c["formula"])]
        rotas = [c["celda"] for c in formulas if "#REF!" in c["formula"]]
        constantes = Counter()
        for c in formulas:
            texto = re.sub(r'"[^"]*"', '""', c["formula"])
            texto = REF.sub("R", texto)
            for m in NUM.finditer(texto):
                constantes[m.group(1)] += 1

        # entradas: constantes numéricas de la hoja de las que depende algún veredicto
        def cadena(h0, ref, vistos):
            if (h0, ref) in vistos:
                return
            vistos.add((h0, ref))
            x = celda.get((h0, ref))
            if x and x["formula"]:
                for r in referencias(x["formula"], h0):
                    cadena(r[0], r[1], vistos)

        verifs = []
        entradas_usadas = set()
        for v in veredictos:
            vistos = set()
            cadena(h, v["celda"], vistos)
            directas = [r for r in referencias(v["formula"], h)]
            entradas = sorted({r for r in vistos if (celda.get(r) and not celda[r]["formula"] and isinstance(celda[r]["constante"], (int, float)))}, key=lambda r: (r[0], coord(r[1])[1], coord(r[1])[0]))
            entradas_usadas |= set(entradas)
            verifs.append(
                {
                    "celda": v["celda"],
                    "rotulo": rotulo(h, v["celda"]),
                    "formula": v["formula"],
                    "valor": v["valor"],
                    "compara": [{"celda": f"{r[0]}!{r[1]}" if r[0] != h else r[1], "formula": (celda.get(r) or {}).get("formula"), "valor": (celda.get(r) or {}).get("valor"), "rotulo": rotulo(r[0], r[1])} for r in directas],
                    "entradas": [f"{r[0]}!{r[1]}" if r[0] != h else r[1] for r in entradas],
                    "rota": "#REF!" in json.dumps(v["formula"]) or any("#REF!" in str((celda.get(r) or {}).get("formula") or "") for r in vistos),
                }
            )
        entradas_tabla = [{"celda": f"{r[0]}!{r[1]}" if r[0] != h else r[1], "valor": celda[r]["constante"], "rotulo": rotulo(r[0], r[1])} for r in sorted(entradas_usadas, key=lambda r: (r[0] != h, coord(r[1])[1], coord(r[1])[0]))]
        resultado[h] = {"veredictos": verifs, "entradas": entradas_tabla, "constantes_en_formulas": constantes.most_common(), "refs_rotas": rotas}

        md += [f"## {h}", ""]
        md += [f"Fórmulas: {len(formulas)}. Veredictos: {len(veredictos)} ({sum(1 for v in verifs if v['rota'])} con `#REF!` en su cadena). Fórmulas con `#REF!`: {len(rotas)}" + (f" ({', '.join(rotas[:30])}{'…' if len(rotas) > 30 else ''})" if rotas else ""), ""]
        md += ["### Entradas de las que dependen los veredictos", "", "| Celda | Rótulo | Valor guardado |", "|---|---|---|"]
        md += [f"| {e['celda']} | {e['rotulo'][:70]} | {e['valor']} |" for e in entradas_tabla]
        md += ["", "### Veredictos", ""]
        for v in verifs:
            md.append(f"- **{v['celda']}** {('(cadena con #REF!) ' if v['rota'] else '')}`{v['formula'][:300]}` → {str(v['valor'])[:80]}")
            for x in v["compara"]:
                if x["formula"]:
                    md.append(f"  - {x['celda']} ({x['rotulo'][:50]}) = `{x['formula'][:260]}` → {x['valor']}")
        md += ["", "### Constantes escritas dentro de las fórmulas (valor: veces)", "", ", ".join(f"`{k}`: {n}" for k, n in constantes.most_common()), ""]

    md += ["## Normas y referencias citadas en el libro", ""]
    md += [f"- {h}!{c}: {t}" for (h, c, t) in sorted(normas_libro)] or ["- ninguna"]
    salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    anexo.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"hojas analizadas: {len(resultado)}; veredictos: {sum(len(r['veredictos']) for r in resultado.values())}; citas de normas: {len(normas_libro)}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
