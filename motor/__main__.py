"""Línea de comandos: python -m motor <config.json> [salida.json]

Lee la configuración en JSON, verifica el poste y escribe el resultado en JSON (en la salida estándar si no se da
archivo). Código de salida: 0 cumple, 1 no cumple, 2 error de cálculo, 3 error de configuración.
"""
import json
import sys
from pathlib import Path

from .validador import ErrorConfig, validar


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 3
    config = json.loads(Path(argv[0]).read_text(encoding="utf-8"))
    try:
        r = validar(config)
    except ErrorConfig as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 3
    texto = json.dumps(r, ensure_ascii=False, indent=2)
    if len(argv) > 1:
        Path(argv[1]).write_text(texto + "\n", encoding="utf-8")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(texto)
    return {"cumple": 0, "no cumple": 1}.get(r["resumen"], 2)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
