# Verificación de `catalogo_tubulares_revM_transcrito.csv` contra los planos (11-11-2026)

Uso interno: contiene la receta de fabricación.

**Método.** Se leyó la lámina 1 de los 24 PDF de `pdf/` (REV. M). En la tabla "Especificaciones de fabricación" y en el pie se compararon, cuerpo por cuerpo:
- norma, Ø, e, largo visible, corte y embute;
- altura armada y peso de cañerías declarado.

No se modificó el CSV (lo generó otra sesión). Este archivo deja constancia de la verificación.

**Resultado.** Los 24 postes (3Ma a 12Mb, 72 filas) **coinciden** con sus planos en todos esos campos. La columna `estado` del CSV (`POR_VERIFICAR_CONTRA_PDF`) puede leerse como **VERIFICADO_CONTRA_PDF (11-11-2026)**.

**Observaciones de los planos** (texto del propio plano):
- Todos dicen "PLANO PRELIMINAR · Validación estructural normativa pendiente. Placa y anclaje: disposición referencial".
- De 3 a 6 m: el cuerpo superior es una "reducción" de Ø60,3 con 200 mm visibles y 100 mm de embute.
- De 7 a 12 m: "Base sin embute. Cada cuerpo siguiente entra 200 mm en el anterior".
- "Barras de catálogo: 6.000 mm".
- **11Ma, 12Ma y 12Mb tienen 5 cuerpos.** La planilla de cálculo admite hasta 4 tramos, así que no se pueden verificar con ella (`docs/FASE4.md`).
- El 3Ma trae una lámina 2 de desglose de pesos. Sus valores de cañerías (18,8 + 1,2 = 20,0 kg) coinciden con el CSV.
