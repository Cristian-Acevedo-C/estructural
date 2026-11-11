# Fase 4 · Tubulares del catálogo REV. M y buscador

Fecha: 11-11-2026. Uso interno: contiene la receta de fabricación. Nada de esto va a una web.

## 1. Datos de entrada, verificados

- **Catálogo:** `fuentes/planos_tubulares_revM/catalogo_tubulares_revM_transcrito.csv` (24 postes, 72 cuerpos), transcrito por otra sesión el 10-11.
- **Verificación:** el 11-11 se contrastó contra la lámina 1 de **los 24 PDF**. Coinciden en norma, Ø, e, visible, corte, embute, altura y peso de cañerías (`VERIFICACION_PDF.md`).
- **Cañerías:** todas las del catálogo REV. M existen en el catálogo maestro (`datos/canerias.csv`). Ø60,3 ≈ 60,32 y Ø168,3 ≈ 168,27 (ASTM, e = 5). Lo exige una prueba.
- **Peso:** el que calcula el buscador (kg/m × corte, embutes incluidos) reproduce el peso de cañerías de los 24 planos (±0,06 kg). Lo exige una prueba.

## 2. Capacidad de cada poste según la planilla

Herramienta: `herramientas/fase4_catalogo.py`. Tabla completa: `docs/FASE4_CAPACIDAD_generado.md`. Datos: `trabajo/fase4/capacidad_catalogo.json`.

**No se inventaron cargas de diseño.** Para cada poste y velocidad (100, 120 y 140 km/h) se calcula:
- **V máx:** la fuerza horizontal **adicional** máxima en la punta con la que la planilla dice "cumple". Se busca por bisección con paso de 0,5 kg y se comprueba que el veredicto sea monótono: lo es en los 63 casos.
- **Qué verificación manda en ese límite.**

**Cabeza de referencia: proyectores de 10 × 26 cm y P = 20 kg.** Es el caso que la planilla trae guardado en `P.Var.2 Tramos Circ.` en las versiones A y B. No es una carga de diseño de ORBE.

Se usa porque la planilla **no puede evaluar un poste sin proyectores**. La torsión divide por alto × ancho de los proyectores (celda F160): con 0 × 0 da `#DIV/0!` y el motor informa "error", nunca "cumple" (hay una prueba).

**Supuestos:**
- Fy 2.400 kg/cm² (el de la planilla; el grado del acero de las cañerías no está en el catálogo).
- 4 pernos (los de los planos) y coeficientes por omisión.
- Largo de cada tramo = el visible del plano. La planilla no modela el embute.

**HECHOS (a 120 km/h, cabeza de referencia):**
- Los 21 postes de hasta 4 cuerpos cumplen con su propio viento y la cabeza de referencia.
- En todos manda la **interacción flexo-compresión**: en la base (2 cuerpos) o en el segundo cuerpo desde la base (4 cuerpos).
- **Menor capacidad:** 10Ma (30,8 kg), 7Mb (32,7 kg), 10Mb (36,1 kg), 9Ma (42,5 kg) y 6Ma (43,0 kg).
- **Mayor capacidad:** 3Mc (604 kg), 4Mc (463 kg), 5Mc (372 kg) y 6Mc (306 kg).
- Entre 100 y 140 km/h la capacidad cambia poco en los postes bajos (3Ma: 103 → 100 kg) y bastante en los altos (10Mb: 43,5 → 27,3 kg).
- **11Ma, 12Ma y 12Mb (5 cuerpos) quedan fuera del alcance:** la planilla admite hasta 4 tramos.

**Qué NO dice esta tabla:**
- Si un poste sirve para una luminaria concreta. Eso depende de su peso, su área expuesta y su altura de montaje, que el catálogo no trae.
- Nada sobre soldadura, deflexión, placa ni pernos: la planilla no los verifica.
- Que la norma de viento esté vigente: duda 12, NCh 432 Of. 72 frente a NCh 432:2025.

## 3. Buscador

`motor/buscador.py` (`python -m motor.buscador`). Recibe las alturas visibles desde la base, la carga (V, P, velocidad, proyectores) y, si se quiere, el diámetro de la punta. Devuelve las combinaciones **más livianas** de cañerías ACTIVAS del catálogo maestro que cumplen según la planilla.

**Restricciones geométricas** (no normativas; revisar con el calculista):
- **Telescópico:** cada cuerpo cabe en el interior del de abajo. Sin holgura, porque en los planos está "por definir".
- **Corte:** visible + embute ≤ largo de barra (6 m).
- **Punta opcional (`--punta 60.32`):** todos los postes REV. M terminan en Ø60,3. Sin esa opción el buscador propone puntas de Ø26,7 o Ø33,4, que probablemente no reciben la luminaria.

**Método:** genera las combinaciones geométricas, las ordena por peso y evalúa con `validar` hasta encontrar k que cumplan. 1 a 2 s por búsqueda de 4 tramos (unas 15.000 combinaciones, menos de 1.000 evaluadas).

**Comprobación de coherencia (HECHO).** Se probaron 7 postes, con las alturas del catálogo, punta Ø60,3 y la carga igual a su propia capacidad. En los 7, la solución más liviana del buscador **es exactamente el poste del catálogo**, con su mismo peso:

| Poste | Catálogo | Buscador |
|---|---|---|
| 10Mb | 85,8 kg | 85,81 kg |
| 10Ma | 73,1 kg | 73,07 kg |
| 7Mb | 45,2 kg | 45,22 kg |
| 7Ma | 56,6 kg | 56,56 kg |
| 9Mb | 80,1 kg | 80,12 kg |
| 6Mb | 57,8 kg | 57,77 kg |
| 11Mb | 165,1 kg | 165,14 kg |

**Lectura:** con las alturas que fija cada diseño REV. M, no hay una combinación de cañerías del catálogo más liviana que alcance la misma capacidad según la planilla. Es coherencia interna, no una validación normativa.

```
python -m motor.buscador --alturas 6,1.8,1.8,0.4 --v 36 --punta 60.32 --k 3
```

## 4. Aviso de entradas bloqueadas (decisión pendiente de la Fase 3, resuelta con el criterio más prudente)

- `herramientas/extraer_bloqueadas.py` lee con openpyxl qué entradas protege la planilla y escribe `motor/modelo/bloqueadas_B.json`. Coincide al 100 % con lo que reporta Excel por COM.
- `validar()` ahora **avisa** (lista `avisos`) cuando una configuración cambia una de esas entradas. No cambia ningún cálculo.
- **HALLAZGO:** en las hojas con gancho, la planilla deja el viento sobre el tablero fijo en 0 y bloqueado.
- La hoja `P.Var. 2 Tramos Circ. 2 ganchos` es la única sin proteger, quizás por descuido, y no avisa.
- Si prefieres **rechazar** en vez de avisar, es un cambio de una línea.

## 5. No hecho

- **Configuración por nombres para cuadrado y octogonal.** No hace falta para los tubulares. Queda para cuando se trabajen otras líneas.
- **Postes de 5 cuerpos.** Requieren extender la planilla o un cálculo propio, que debe validar el calculista.
- **Carga de diseño real por poste** (luminaria, brazo, área, altura de montaje): la tiene que definir ORBE.

## Pruebas

`python -m pytest pruebas -q`: **61 de 61**. Hay 8 nuevas en `test_fase4.py`:
- pesos de los 24 planos;
- cañerías presentes en el catálogo maestro;
- restricciones geométricas;
- el buscador encuentra 7Mb;
- capacidad monótona y estable;
- 5 tramos fuera de alcance;
- error sin proyectores;
- avisos de entradas bloqueadas.
