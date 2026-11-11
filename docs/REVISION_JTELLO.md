# Revisión técnica de Jonathan Tello · 11-11-2026

Respuesta escrita a las dudas de la especificación (Fase 1) y de la Fase 4, recibida a través de Cristian. Uso interno.
Su rol en ORBE y si puede firmar memorias: **[COMPLETAR]**. Su respuesta distingue lo que comprobó en la planilla de lo que "necesita una definición del calculista responsable": no se presenta como la firma de un cálculo.

## Lo que confirmó (HECHO, coincide con la Fase 1)

| Punto | Confirmación | Estado en el motor |
|---|---|---|
| Viento | 70 kgf/m² hasta 4 m, perfil logarítmico sobre 4 m, factor (V/120)². 120 km/h es una referencia interna de la planilla, no una velocidad normativa trazable | Replicado tal cual |
| Gancho | D242 es un 0 fijo: puede decir "cumple" sin calcular | El motor ya lo marca "no verificado" |
| "t" del gancho | La primera "t" (D27) se usa como diámetro de barra maciza; la segunda (F27) no la usa ninguna fórmula | Documentado |
| Octogonal | C33 y C34 usan la inercia de un anillo circular. No se puede afirmar de antemano que sea conservador | Facetados: revisión técnica en el cotizador |
| Pernos | El área corresponde a la rosca UNC, pero la fórmula usa el Fy del poste | No se verifican (ya era así) |
| Bloque lateral | Tiene #REF! y algunos datos alimentan las hojas principales | El motor excluye los veredictos rotos |

## HALLAZGO NUEVO

- **Torsión del cuadrado:** `P.Recto Cuad.!C251` usa τ = 4,78·T/B³, fórmula de una sección cuadrada **maciza**. Para un tubo hueco corresponde τ ≈ T/(2·A_m·t). En un 100×100×3 la planilla subestima τ unas 3,7 veces.
  → **Cotizador:** los 70 cuadrados quedan en "Revisión técnica" hasta corregir la fórmula (11-11-2026).

## Norma de viento (corrige ESTADO.md)

- D.Ex. MOP N.º 584, del 28-07-2026, publicado el 18-08-2026: oficializa la NCh432:2025 y deroga la **NCh432.Of71** (no "Of.72", como dice la planilla).
- Rige seis meses después de su publicación (**18-02-2027**). Al 11-11-2026 sigue el período de transición.
- Para programar un módulo NCh432:2025 se necesita el texto oficial de la norma. Él no lo consultó, y nosotros tampoco lo tenemos.

## Recomendaciones (decisiones que requieren un responsable técnico)

1. Corregir los "cumple" falsos (gancho, torsión del cuadrado) y las referencias rotas.
2. Fijar el método: ASD o LRFD, con norma, edición y cláusula por cada verificación. Retirar el 0,75 global salvo justificación (NCh427/1:2016 como base chilena).
3. Pandeo de varios tramos: hoy se divide la carga de Euler por 1,67, sin transición inelástica. Se debe modelar cada segmento con estabilidad global y segundo orden.
4. Agregar las verificaciones que faltan: gancho completo, soldaduras, deflexión con un límite y su fuente, placa, anclaje al hormigón (ACI 318 cap. 17) y fundación.
5. Propiedades por material: fuste, placa, pernos (por ejemplo ASTM F1554 y su grado) y soldadura.
6. Fy: debe salir del grado certificado. 2.400 kgf/cm² ≈ 235 MPa; ASTM A53 Gr. B = 240 MPa, solo si se exige y certifica.
7. Postes de 5 cuerpos: modelarlos con 5 segmentos reales, sin promediar.
8. Holgura entre cuerpos: la define el diseño de la unión y sus tolerancias.
9. Versión oficial A o B: la determina la empresa. Propone una versión maestra con código, revisión, normas, responsable y casos de validación, con la parte comercial separada.

## Qué cambia en lo que tenemos

- **Motor (`estructural/`):** sigue siendo una réplica exacta de la planilla, con sus defectos. Sirve como referencia para comparar un motor nuevo. No es un cálculo normativo.
- **Cotizador:** solo los tubulares de hasta 4 cuerpos pueden salir "Disponible". Cuadrados, facetados y tubulares de 5 cuerpos van a revisión técnica.
- **Siguiente paso técnico posible:** un "motor v2" con las correcciones 1, 3 y 5 y la torsión del tubo cuadrado, contrastado con el motor actual. Lo debe validar un responsable técnico antes de usarlo.
