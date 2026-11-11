"""Compara dos volcados (volcar_plantilla.py): hojas, fórmulas, constantes y VBA. Solo lee.

Uso: python comparar_versiones.py <volcado_A> <volcado_B> <salida.md>
"""
import difflib
import json
import sys
from collections import defaultdict
from pathlib import Path


def carga(d: Path):
    cs = json.loads((d / "celdas.json").read_text(encoding="utf-8"))
    return {(c["hoja"], c["celda"]): c for c in cs}


def main(da: Path, db: Path, salida: Path) -> None:
    a, b = carga(da), carga(db)
    ha = [h["hoja"] for h in json.loads((da / "hojas.json").read_text(encoding="utf-8"))]
    hb = [h["hoja"] for h in json.loads((db / "hojas.json").read_text(encoding="utf-8"))]
    comunes = [h for h in hb if h in ha]
    formulas, constantes = defaultdict(list), defaultdict(list)
    for k in sorted(set(a) | set(b)):
        if k[0] not in comunes:
            continue
        ca, cb = a.get(k), b.get(k)
        fa, fb = (ca or {}).get("formula"), (cb or {}).get("formula")
        if fa or fb:
            if fa != fb:
                formulas[k[0]].append((k[1], fa, fb))
        else:
            xa, xb = (ca or {}).get("constante"), (cb or {}).get("constante")
            if xa != xb:
                constantes[k[0]].append((k[1], xa, xb))

    lineas = [f"# Comparación {da.name} → {db.name}", ""]
    lineas += ["## Hojas", "", f"- Solo en A: {[h for h in ha if h not in hb] or 'ninguna'}", f"- Solo en B: {[h for h in hb if h not in ha] or 'ninguna'}", f"- Orden A: {ha}", f"- Orden B: {hb}", ""]
    lineas += ["## Fórmulas distintas (hojas comunes)", ""]
    for h in comunes:
        for c, fa, fb in formulas[h]:
            lineas.append(f"- `{h}`!{c}: A `{fa}` → B `{fb}`")
    if not any(formulas.values()):
        lineas.append("- ninguna")
    lineas += ["", "## Constantes distintas (hojas comunes): en su mayoría, los datos de la última configuración que quedó cargada", ""]
    for h in comunes:
        if constantes[h]:
            lineas.append(f"- `{h}` ({len(constantes[h])}): " + "; ".join(f"{c}: {xa} → {xb}" for c, xa, xb in constantes[h]))
    va = (da / "vba.txt").read_text(encoding="utf-8").splitlines()
    vb = (db / "vba.txt").read_text(encoding="utf-8").splitlines()
    d = list(difflib.unified_diff(va, vb, "A/vba.txt", "B/vba.txt", n=1, lineterm=""))
    lineas += ["", f"## VBA: {len(d)} líneas de diferencia (diff unificado)", "", "```diff", *d[:400], "```"]
    salida.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"fórmulas distintas: {sum(len(v) for v in formulas.values())}, constantes distintas: {sum(len(v) for v in constantes.values())}, VBA diff: {len(d)} líneas")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
