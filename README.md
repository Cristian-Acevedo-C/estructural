# Validador estructural de postes (uso interno)

Replica la "Plantilla Memoria de Cálculo" de ORBE en un motor determinístico en Python. Estado por fases en `../ESTADO.md`.

| Carpeta | Qué hay |
|---|---|
| `insumos/` | Copias de solo lectura de las plantillas y del catálogo maestro (origen y hashes en `ORIGEN.md`) |
| `docs/` | `ESPECIFICACION.md` (Fase 1), `MOTOR.md` (Fase 2), `FASE3.md`, `FASE4.md`, anexos generados y comparación de versiones |
| `motor/` | `excel.py` (intérprete de fórmulas), `validador.py` (`validar(config)`), `buscador.py` (Fase 4), `extraer.py`, `modelo/` (fórmulas extraídas y entradas bloqueadas) |
| `datos/` | Tablas del catálogo maestro: cañerías, tubos (vacía), placas y pernos (sin costos) |
| `ejemplos/` | Configuraciones de ejemplo (casos guardados en la plantilla A) |
| `pruebas/` | `pytest` y la comparación contra los valores guardados por Excel |
| `herramientas/` | Scripts de la Fase 1 (volcado, comparación, análisis) y del catálogo |
| `trabajo/` | Volcados y salidas intermedias (regenerables) |

```
python -m venv .venv && .venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python -m motor ejemplos/variable_3_tramos.json
.venv/Scripts/python -m pytest pruebas -q
```

Contiene la receta de fabricación (tramos, espesores, placa, pernos): nada de aquí va a una web.
