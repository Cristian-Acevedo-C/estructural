# Fase 6 · Recetario: tablas sin costos, cruce con el catálogo y capacidad de cuadrados y facetados

Fecha: 11-11-2026. Uso interno. Nada de esto va a una web.

Cristian entregó el 11-11 el recetario (`RECETARIO (1).xlsx`) y pidió dejar todo listo. Copia de solo lectura: `insumos/recetario_2026-11-11.xlsx` (sha256 `9c8a60d8e3e56f75…`). El original no se modificó.

**Regla aplicada.** El recetario trae precios, costos, márgenes, valor por kilo y proveedores de luminarias. De ahí se tomaron **solo medidas y pesos**. Una prueba revisa que ningún archivo generado contenga precios ni costos.

## 1. Qué se extrajo (`herramientas/recetario_a_csv.py`)

| Archivo | Filas | Hoja de origen | Contenido |
|---|---|---|---|
| `datos/tubos_recetario.csv` | 19 | RECETARIO | Tubos redondos: Ø, espesor, kg/m |
| `datos/postes_cuadrados_recetario.csv` | 70 | CUADRADOS | Código, altura, perfil, canastillo, placa, peso |
| `datos/postes_facetados_recetario.csv` | 10 | FACETADOS | Código, altura, 8 lados, Ø inferior y superior, espesor, placa, pernos |

- `datos/tubos.csv` sigue vacío a propósito: lo genera `catalogo_a_csv.py` desde el catálogo maestro, que no tiene tubos. Los del recetario quedan aparte y marcados "sin confirmar en catálogo maestro".
- El buscador de la Fase 4 **no** usa estos tubos: sigue trabajando solo con cañerías ACTIVAS del catálogo maestro.

## 2. Cruce con el catálogo maestro (HECHO)

Detalle fila por fila en `docs/RECETARIO_CRUCE_generado.md`.

- La hoja RECETARIO tiene 64 materiales: 41 cañerías y 23 tubos redondos.
- **18 cañerías coinciden** con el catálogo maestro en Ø, espesor y kg/m. Entre ellas están todas las que usan los postes tubulares REV. M.
- Ninguna tiene el mismo Ø y espesor con distinto peso.

**HALLAZGOS (el recetario no se corrigió; confirmar con ORBE):**

| Fila | Qué dice el recetario | Qué indica el peso o el catálogo |
|---|---|---|
| 11 | ISO R65 1" con Ø26,67 (el mismo de ¾") | El peso 1,98 kg/m y el catálogo corresponden a Ø33,4 |
| 43 | ASTM A53 2" Ø60,32 × 3,91 | Fila repetida (igual a la 39) |
| 47 | ASTM A53 2½" con Ø73,02 | El catálogo dice Ø76,1 con el mismo espesor y peso |
| 87 a 99 | ASTM A53 10" con Ø273,5 | El catálogo dice Ø273,05 con los mismos espesores y pesos |
| 95 | ASTM A53 10" × 7,92 con 46,49 kg/m | 10 % menos que el peso teórico; el catálogo trae el mismo valor |
| 159 y 163 | ASTM A53 "22"" con Ø610 | 610 mm corresponde a 24" |
| 179 | Tubo 1" Ø25,4 × 2 con 1,015 kg/m | 12 % menos que el teórico |
| 191 y 195 | Tubo 1¾" con Ø1,5 y Ø2,5 | Diámetros imposibles. Los pesos calzan con Ø44,45 × 1,5 y Ø44,45 × 2,0 |
| 211 | Tubo 2½" Ø63,5 × 2,5 con 3,03 kg/m | El peso calza con espesor 2,0 |

- Las 4 filas de tubos con medidas incoherentes (179, 191, 195 y 211) **no se cargaron**.
- 20 cañerías ASTM de 12" a 24" están en el recetario y no en el catálogo. 6 cañerías ASTM delgadas (½" a 1½") están en el catálogo y no en el recetario.
- Las hojas BRAZOS RECTOS y GANCHOS CURVOS muestran `#ERROR!` en peso y costo, y varias filas de TUBULARES también.

**HALLAZGO: los tubulares del recetario no son los de los planos REV. M.** La hoja TUBULARES tiene 49 recetas (códigos TTUB e ITUB). Sus tramos difieren de los planos: por ejemplo, el de 9 m "ITUB9A" es 3.000 + 2.500 + 2.500 + 1.600 y el plano 9Ma es 3.000 + 2.800 + 2.800 + 400. No se cargaron ni se calcularon: hay que definir cuál es la receta vigente.

## 3. Capacidad de cuadrados y facetados según la planilla (HECHO)

`herramientas/fase6_recetario.py`. Tabla completa: `docs/FASE6_CAPACIDAD_generado.md`. Datos: `trabajo/fase6/capacidad_recetario.json`.

Mismo método de la Fase 4: la mayor fuerza horizontal **adicional** en la punta con la que la planilla dice "cumple", a 100, 120 y 140 km/h, con la cabeza de referencia de la planilla (proyectores 10 × 26 cm, P = 20 kg). **No es una carga de diseño de ORBE.**

- **Cuadrados → hoja `P.Recto Cuad.`** Peso propio de la planilla entre 1,8 % y 5 % sobre el del recetario (la planilla usa esquinas vivas).
- **Facetados → hoja `P.Var. Octogonal`.**
- En todos manda la interacción flexo-compresión. El veredicto es monótono en los 240 casos.

**Postes que no cumplen ni con su propio viento y la cabeza de referencia:**

| Viento | Cuadrados (de 70) | Facetados (de 10) |
|---|---|---|
| 100 km/h | 4: CU39, CU40, CU50, CU60 | 2: FAC-15M-3MM, FAC-20M-4MM |
| 120 km/h | 9: los anteriores más CU10, CU38, CU49, CU59, CU70 | 2: los mismos |
| 140 km/h | 14 | 4: los anteriores más FAC-15M-4MM y FAC-16M-4MM |

Son los perfiles 75 × 75 de 8 a 10 m y los 100 × 100 × 3 de 9 y 10 m, y los facetados más esbeltos.

**Qué NO dice esta tabla (límites):**
- No es un veredicto sobre los productos. Depende de la planilla, que usa la NCh 432 Of. 72 y un coeficiente de forma 1,6 para el cuadrado (valor bloqueado).
- **Facetados:** la planilla no dice si el diámetro es entre caras o entre vértices, y calcula la inercia con la fórmula de un tubo circular (hipótesis de la Fase 5). El resultado puede ser optimista.
- No verifica soldadura, deflexión, placa ni pernos.
- No dice si un poste sirve para una luminaria concreta: falta la carga de diseño.

## 4. No hecho

- **Cónicos (hoja CÓNICOS):** la planilla no tiene hoja de poste circular cónico. No se pueden calcular con este motor.
- **Brazos, ganchos y accesorios:** el recetario trae su despiece, pero la verificación del gancho en la planilla es un 0 escrito a mano (Fase 1).
- **Luminarias:** la hoja trae códigos, proveedor y precios, pero **no** peso ni área al viento. Sigue faltando la carga de diseño.
- **Corregir el recetario:** no se tocó. Los hallazgos de la sección 2 son para que ORBE los corrija en su archivo.

## Pruebas

`python -m pytest pruebas -q`: **97 de 97** (12 nuevas en `test_fase6.py`): cantidades, ausencia de precios y costos en todo lo generado, tubos coherentes con su peso, peso de los cuadrados contra la planilla, capacidad decreciente con la altura y el viento, y resultado guardado.

## Copia del recetario para revisar (11-11-2026)

`herramientas/recetario_para_revisar.ps1` (necesita Excel) genera `insumos/interno_NO_PUBLICAR/recetario_revision/RECETARIO_para_revisar_2026-11-11.xlsx`.

- **No cambia ningún valor ni fórmula** (comprobado: 35.720 celdas, 0 distintas respecto de la copia de `insumos/`).
- Hoja nueva **REVISAR**, al inicio: 18 puntos con hoja, celda (con vínculo), qué dice, observación, propuesta y una columna vacía para la respuesta de ORBE.
- **Naranja + nota:** las celdas dudosas de las hojas RECETARIO y TUBULARES.
- **Rojo:** las 692 celdas que en el original muestran `#ERROR!` (TUBULARES 336, BRAZOS RECTOS 288, GANCHOS CURVOS 68). Excel las recalcula como 0 o como totales incompletos, y el error deja de verse: por eso se pintan.
- Las fórmulas con error apuntan a la hoja `Hoja1` de otro libro, `RECETARIOnuevo.xlsx`, que no está junto al archivo.
- Las propuestas son hipótesis. El recetario original lo corrige ORBE.
