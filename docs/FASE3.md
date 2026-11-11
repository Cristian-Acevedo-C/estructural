# Fase 3 · El motor contra Excel recalculado con configuraciones nuevas

Fecha: 10 y 11-11-2026. Uso interno. Herramientas: `herramientas/fase3_excel.py` y `herramientas/fase3_bloqueos.py`.
Resultado completo: `trabajo/fase3/resultado_20261110.json` y `trabajo/fase3/corrida_20261110.txt`.

## Qué se probó

La Fase 2 comparó el motor contra los valores que Excel había dejado guardados: solo las configuraciones que ya estaban en la planilla. Aquí se generaron **300 configuraciones nuevas** (25 por cada una de las 12 hojas circulares, semilla 20261110) y se compararon contra el **Excel original recalculando** el libro completo.

- **Medidas reales:** tramos con cañerías ACTIVAS de `datos/canerias.csv`, el de arriba más delgado. Alturas de 0,5 a 6 m.
- **Cargas:** sobrecarga de 5 a 80 kg; viento sobre el tablero de 0 a 120 kg; velocidad de 80 a 160 km/h.
- **Proyectores o gancho, según la hoja.** Además, Fy (2.400, 2.530 o 3.500) y la cantidad de pernos (4, 6 u 8).
- **Comparación:** **cada fórmula de la hoja** (no solo los veredictos), con tolerancia relativa 1e-9, y el estado de cada veredicto contra el texto "OK!…" que escribe Excel.

## Resultado

| | Comparados | Distintos |
|---|---|---|
| Casos nuevos (12 hojas) | 300 (145 cumplen, 155 no cumplen; cada hoja tiene casos de los dos) | 0 rechazados |
| Fórmulas | 56.200 | **3** (más 2 de cancelación numérica, contadas aparte). Ver abajo |
| Veredictos (cumple o no cumple) | 4.250 | **0** |
| Plantilla `insumos/plantilla_B_2026-10-21.xlsm` | SHA-256 antes y después | Intacta |

**HECHO.** En configuraciones que la planilla nunca vio, el motor entrega los mismos veredictos que Excel en el 100 % de los casos, y las mismas cifras en todas las fórmulas, salvo el ruido de redondeo descrito abajo.

### Las 5 fórmulas que no coinciden exactamente

| Hoja · caso | Celda | Motor | Excel | Escala de los términos que se restan | Residuo relativo |
|---|---|---|---|---|---|
| P.Var.2 Tramos Circ. · 4 | Z125, Z126, Z127 | −2,98·10⁻⁷ | −2,68·10⁻⁷ | 1,085·10⁹ kg·cm | 2,7·10⁻¹⁶ |
| P.Var.2 Tramos Circ. · 0 y 24 | Z125 | 1,79·10⁻⁷ y 8,9·10⁻⁸ | 0 | 7,99·10⁸ kg·cm | 2,2·10⁻¹⁶ |
| (corrida corta de prueba) P.Recto Circ. | R123 | 3,7·10⁻⁹ | 0 | — | — |

- **Son momentos que analíticamente valen 0** (en la punta del poste): términos de unos 10⁹ kg·cm que se cancelan.
- **El residuo es del orden de la precisión de la máquina** (ε ≈ 2,2·10⁻¹⁶). Excel lleva a 0 algunas restas casi nulas y suma en otro orden: por eso los residuos difieren.
- **No se propaga:** las demás fórmulas y los 4.250 veredictos coinciden.
- **No se ajustó la tolerancia** después de ver el resultado. Se midió la escala de cada caso (script en la sesión del 11-11) y queda documentado aquí.

## Cómo se trató la protección de la planilla

**Las hojas de cálculo están protegidas con contraseña** (todas, salvo `P.Var. 2 Tramos Circ. 2 ganchos`, `CAÑERIAS` y `Datos`). **No se quitó la protección ni se probó ninguna contraseña.**

Un primer intento con `Unprotect()` sin contraseña dejó a Excel esperando un diálogo invisible. Se detuvo el proceso, se borró la copia y se cambió el método:
- **Solo se escriben celdas desbloqueadas**, las mismas que puede editar un usuario real de la planilla.
- `herramientas/fase3_bloqueos.py` lee `Range.Locked` de cada entrada del motor.
- Si una configuración pedía otro valor en una celda bloqueada (94 casos), esa celda se fijó a su valor original con la clave `celdas` del motor. Así ambos calculan con lo mismo.
- **Siempre:** Excel con macros desactivadas (`AutomationSecurity = 3`), sobre una copia en `trabajo/fase3/` que se borra al terminar. `insumos/` nunca se abre con Excel.

**Entradas bloqueadas en la planilla (HECHO):**
- **En todas las hojas:** `coef_forma`, `amortiguamiento`, `coef_von_karman`, `g_kgcm2`, `e_kgcm2` y `fs_pandeo_general`, además de las alturas del bloque oculto.
- **En las 8 hojas con gancho:** también `viento_tablero_kg` (A27).

**Libres:** tramos, sobrecarga, velocidad del viento, proyectores, geometría del gancho, Fy y pernos.

## Hallazgos y recomendaciones

1. **HALLAZGO.** El motor acepta cambiar entradas que la planilla bloquea: los coeficientes y, con gancho, el viento sobre el tablero. Excel no deja editarlas; quien hizo la planilla las fijó.
   **RECOMENDACIÓN (decide Cristian):** que el motor avise cuando una configuración cambia una entrada bloqueada, o que la rechace salvo autorización. No se cambió el motor: la Fase 2 sigue en revisión.
2. **HALLAZGO.** Los coeficientes bloqueados (forma 0,6, amortiguamiento 0,02, von Kármán 0,2, FS de pandeo 1,67) no se pudieron variar contra Excel sin quitar la protección. El motor los calcula igual que Excel con sus valores originales (Fase 2 y esta fase), pero **no se comprobó** contra Excel con otros valores. Si el calculista quiere cambiarlos, hay que repetir esta prueba con la planilla desprotegida por ORBE.
3. **LIMITACIÓN.** La corrida completa tardó 24.253 s (6,7 h). La corrida de prueba hizo 24 casos en 37 s, así que se esperaban unos 8 minutos. La causa más probable es que el equipo se suspendió durante la noche; el resultado no cambia. Para repetir: `.venv/Scripts/python herramientas/fase3_excel.py --por-hoja 25 --semilla 20261110`.
4. **Cuadrado y octogonal no se probaron:** no tienen configuración por nombres (`docs/MOTOR.md`).
5. **Validez normativa: esta fase no la cubre.** Que el motor coincida con Excel no hace vigente la planilla. Ver la duda 12 de `ESPECIFICACION.md` (NCh 432 Of. 72 frente a NCh 432:2025).

## Pruebas

- `pruebas/test_fase3_generador.py` (3 pruebas nuevas, sin Excel): el generador es reproducible, entrega configuraciones válidas, no toca claves bloqueadas y recorre "cumple" y "no cumple". También prueba la comparación de valores al estilo de Excel.
- `python -m pytest pruebas -q`: **53 de 53**.
