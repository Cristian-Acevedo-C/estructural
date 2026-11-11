# Motor de verificación (Fase 2)

Fecha: 10-11-2026. Uso interno.

## Qué hace

`validar(config)` recibe un poste en JSON y devuelve, para cada verificación de la planilla:
- **valor:** lo que se compara, por ejemplo fa.
- **límite:** contra qué se compara, por ejemplo Fa.
- **razón de uso:** valor / límite.
- **estado:** cumple, no cumple o no verificado.
- **origen:** la celda de la planilla de la que sale.

También devuelve:
- **Reacciones en la base:** M0, V0 y N0.
- **Frecuencia** y **peso propio**.
- **Pernos:** carga por perno, área de tracción y diámetro nominal.
- **Placa:** espesor.

```
python -m motor ejemplos/variable_3_tramos.json            # resultado en pantalla
python -m motor ejemplos/variable_3_tramos.json salida.json
```

Código de salida: 0 cumple · 1 no cumple · 2 error de cálculo · 3 error de configuración.

Desde Python:

```python
from motor import validar
r = validar(config)
```

## Cómo está hecho, y por qué

El motor **no reescribe las fórmulas a mano**. Las lee de la planilla y las evalúa con un intérprete de fórmulas de Excel escrito en Python puro (`motor/excel.py`).

**Por qué.** En la Fase 1 aparecieron hojas que, en apariencia, hacen lo mismo con fórmulas distintas:
- **Brazos del momento:** en 2 tramos, el viento del tablero tiene un brazo fijo de 50 cm. En 4 tramos usa la mitad de la altura de los proyectores.
- **Viento sobre 4 m:** la fuerza de los tramos que cruzan los 4 m ignora la parte a 70 kg/m².
- **Pandeo:** el factor de seguridad del pandeo general cambia según la cantidad de tramos.

Una versión "general" escrita a mano no coincidiría con el Excel. Así se replica exactamente lo existente, como pide la regla del proyecto, con sus defectos incluidos.

- **Determinístico:** sin Excel, sin red y sin modelos de lenguaje. Solo Python 3 estándar; openpyxl se usa únicamente para extraer.
- **Las fórmulas son datos:** `motor/modelo/plantilla_B.json`, extraído de `insumos/plantilla_B_2026-10-21.xlsm`, con su SHA-256 en `planilla.sha256` de cada resultado. Para regenerarlo:
  `python -m motor.extraer insumos/plantilla_B_2026-10-21.xlsm motor/modelo/plantilla_B.json motor/modelo/guardados_B.json`
- **Mapa por rótulos:** las entradas, los veredictos y las salidas se ubican por sus rótulos dentro de la planilla, no con coordenadas escritas a mano (`mapa_hoja` en `motor/validador.py`).
- **Verificaciones:** cada una se lee de la fórmula de su veredicto, por ejemplo `IF(B218<=B212,"OK!…","…")`. De ahí salen el valor (B218), el límite (B212) y el criterio. El estado "cumple" o "no cumple" es el mismo texto que escribe la planilla.
- **Velocidad:** unos 1,6 ms por validación, suficiente para el buscador de la Fase 4.

Cuando se incorporen normas nuevas (con el calculista), se pueden escribir las verificaciones como código explícito y probarlas contra este motor, que es la referencia exacta de la planilla.

## Alcance actual

| Sección | Tramos | Ganchos | Hoja |
|---|---|---|---|
| circular | 1 | 0 / 1 / 2 | `P.Recto Circ.` / `… 1 gancho` / `… 2 ganchos` |
| circular | 2 | 0 / 1 / 2 | `P.Var.2 Tramos Circ.` / `P.Var. 2 Tramos Circ. 1 gancho` / `… 2 ganchos` |
| circular | 3 | 0 / 1 / 2 | `P.Var.3 Tramos Circ.` / `… 1 gancho` / `… 2 ganchos` |
| circular | 4 | 0 / 1 / 2 | `P.Var.4 Tramos Circ.` / `… 1 gancho` / `… 2 ganchos` |

**Cuadrado y octogonal (desde la Fase 5, 11-11-2026).** Tienen configuración por nombres con `"seccion": "cuadrada"` u `"octogonal"`, un solo tramo y 0, 1 o 2 ganchos. Sus claves de tramo y de gancho son distintas a las circulares: ver `docs/FASE5.md`.

## Configuración

```json
{
  "seccion": "circular",
  "ganchos": 0,
  "tramos": [
    {"altura_m": 0.6, "diametro_cm": 11.4,  "espesor_cm": 0.305},
    {"altura_m": 5.4, "diametro_cm": 16.83, "espesor_cm": 0.34},
    {"altura_m": 6,   "diametro_cm": 21.9,  "espesor_cm": 0.5}
  ],
  "sobrecarga_kg": 25,
  "viento_tablero_kg": 50,
  "viento": {"velocidad_kmh": 120},
  "proyectores": {"alto_cm": 30, "ancho_cm": 50}
}
```

| Clave | Unidad | Obligatoria | Nota |
|---|---|---|---|
| `seccion` | — | no (circular) | `circular`, `cuadrada` u `octogonal` |
| `ganchos` | — | no (0) | 0, 1 o 2 |
| `tramos` | — | sí | de 1 a 4, **en el orden de la planilla: el primero es el de arriba y el último la base** |
| `tramos[].altura_m` / `diametro_cm` / `espesor_cm` | m / cm / cm | sí | 2·espesor < diámetro; avisa si el diámetro supera 100 cm (¿milímetros?) |
| `sobrecarga_kg` | kg | sí | P. En las hojas con gancho es el peso de la luminaria |
| `viento_tablero_kg` | kg | sí | V, fuerza horizontal en la punta |
| `viento.velocidad_kmh` | km/h | sí | el motor siempre usa la velocidad (E44 = "SI") |
| `proyectores.alto_cm` / `ancho_cm` | cm | sí, en hojas sin gancho | |
| `gancho.diametro_cm` / `espesor_cm` / `radio_cm` / `distancia_cm` / `t_cm` | cm | sí, con gancho | `t_cm` puede ser 0 |
| `fy_kgcm2` | kg/cm² | no (2400) | |
| `coef_forma`, `amortiguamiento`, `coef_von_karman` | — | no (0,6 / 0,02 / 0,2) | |
| `g_kgcm2`, `e_kgcm2` | kg/cm² | no (840000 / 2100000) | `e_kgcm2` existe como celda solo en las hojas de 2 a 4 tramos |
| `fs_pandeo_general` | — | no (1,67) | solo hojas de 2 a 4 tramos |
| `pernos` | — | no (4) | |
| `celdas` | — | no | modo avanzado: `{"A15": 6}` escribe celdas directo (para la Fase 3) |
| `hoja` | — | no | elige la hoja por nombre (con `celdas`, sirve para cualquiera de las 18) |
| `incluir_rotas` | — | no | incluye los veredictos con `#REF!` y los del bloque auxiliar escondido |

- **Valores por omisión:** cuando falta una clave opcional, se usa el valor que la planilla trae en todas sus hojas, y la salida lo lista en `supuestos`.
- **Claves desconocidas:** se rechazan. Las que empiezan con `_` se ignoran y sirven para notas.

## Salida (resumen)

```json
{
  "hoja": "P.Var.3 Tramos Circ.",
  "planilla": {"archivo": "plantilla_B_2026-10-21.xlsm", "sha256": "d9fd0a55…"},
  "resumen": "cumple",
  "alcance": "El resumen considera solo las verificaciones que tiene la planilla…",
  "no_verificado": ["soldadura (la planilla no la verifica)", "…"],
  "verificaciones": [
    {"nombre": "Pandeo general · Base tramo 1", "estado": "cumple", "valor": 8.11, "limite": 105.58,
     "razon_de_uso": 0.077, "unidad": "kg/cm²", "criterio": "B221 <= B217 → cumple",
     "mensaje_planilla": "OK! TRAMO No 1 CUMPLE A LA COMPRESION", "celda": "'P.Var.3 Tramos Circ.'!D221"}
  ],
  "salidas": {"momento_base_kgcm": 0, "peso_propio_kg": 0, "perno_diametro_nominal": "3/4", "placa_espesor_cm": 0},
  "supuestos": ["fy_kgcm2 = 2400 (valor por omisión de la planilla)"],
  "avisos": [],
  "entradas_celdas": {"'P.Var.3 Tramos Circ.'!A15": 0.6}
}
```

- **"no verificado":** la verificación existe en la planilla, pero su valor es un 0 escrito a mano, como la tensión en la base del gancho. Nunca cuenta como "cumple".
- **Veredictos que no se muestran:** los rotos (`#REF!`) y los del bloque auxiliar escondido. Se ven con `incluir_rotas: true`.
- **El resumen:** dice "no cumple" si alguna verificación no cumple. "cumple" significa que cumple lo que la planilla verifica, no más.

## Pruebas

```
.venv/Scripts/python -m pytest pruebas -q        # 50 pruebas
python pruebas/contra_guardados.py B             # cada fórmula contra el valor que Excel dejó guardado
```

- **Todas las fórmulas, contra lo guardado por Excel:** A 3.196 de 3.196 y B 3.598 de 3.598 coinciden (tolerancia relativa 1e-9). Incluye las fórmulas matriciales (MMULT/MINVERSE) de la frecuencia.
- **`validar` en las 12 hojas, contra la configuración guardada en A y en B:** 278 comparaciones por versión, 0 distintas (veredictos y salidas).
- **Semántica de Excel:** precedencia, ROUND, textos, IF sin rama falsa y errores.
- **Errores de configuración y aviso de milímetros.**
- **El gancho sale "no verificado"**, y a más viento y menos espesor sube la razón de uso.

Esto no reemplaza la Fase 3: ahí se recalcula el Excel original con configuraciones nuevas, no solo con las guardadas.

## Tablas comerciales

En `datos/` (ver `datos/LEEME.md`): cañerías ISO R65 y ASTM A53 (29), tubos (0, **[COMPLETAR]**: el catálogo maestro no tiene), placas base (4) y pernos (4). Sin costos.

## Agregado en la Fase 4 (11-11-2026)

- **Avisos de entradas bloqueadas.** Si la configuración cambia una entrada que la planilla protege, `avisos` lo dice; el cálculo no cambia. Las entradas protegidas son los coeficientes y, en las hojas con gancho, el viento sobre el tablero. Fuente: `motor/modelo/bloqueadas_B.json`, generado por `herramientas/extraer_bloqueadas.py`.
- **Buscador:** `python -m motor.buscador --alturas 6,1.8,1.8,0.4 --v 36 --punta 60.32`. Devuelve las combinaciones más livianas de cañerías del catálogo que cumplen. Ver `docs/FASE4.md`.
- **Sin proyectores (0 × 0) la planilla no se puede evaluar:** la torsión divide por su área. El resumen sale "error", nunca "cumple".
