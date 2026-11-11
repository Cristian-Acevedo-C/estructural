# Tablas comerciales (uso interno)

Generadas por `herramientas/catalogo_a_csv.py` desde `insumos/catalogo_maestro_v7.xlsx`, una copia de
`CATALOGO_MAESTRO_ORBE_v7_CONTROL_GALVANIZADO.xlsx`, hoja MATERIALES. Cada fila trae su fuente: archivo, hash y fila.
Sin costos ni precios.

Los tres archivos `*_recetario.csv` los genera `herramientas/recetario_a_csv.py` desde `insumos/recetario_2026-11-11.xlsx`.
Solo medidas y pesos: sin precios, costos ni márgenes. Ver `docs/FASE6.md`.

| Archivo | Filas | Contenido |
|---|---|---|
| `canerias.csv` | 29 | Cañerías ISO R65 y ASTM A53: diámetro exterior y espesor (mm y cm), kg/m y largo de barra |
| `tubos.csv` | 0 | **[COMPLETAR: el catálogo maestro no tiene tubos]**. Solo trae el encabezado, para no mezclar tubo con cañería |
| `tubos_recetario.csv` | 19 | Tubos redondos del RECETARIO (Fase 6). Sin confirmar en el catálogo maestro; el buscador no los usa |
| `postes_cuadrados_recetario.csv` | 70 | Postes cuadrados del RECETARIO: altura, perfil, canastillo, placa y peso |
| `postes_facetados_recetario.csv` | 10 | Postes facetados de 8 lados del RECETARIO: altura, Ø inferior y superior, espesor, placa y pernos |
| `placas_base.csv` | 4 | PL200, PL240, PL300, PL340: lados, espesor y kg |
| `pernos_anclaje.csv` | 4 | Pernos 1/2", 5/8", 3/4" y 7/8": diámetro y largo |

Observaciones del catálogo (no se corrigieron allá):

- **Tubos:** la hoja MATERIALES no tiene ninguna fila de categoría TUBO.
  - La hoja CAÑERIAS de la plantilla de cálculo (versión B) sí trae una tabla "TUBO".
  - No se usó, porque la regla es tomar las tablas del catálogo maestro.
  - Para completarla hay dos caminos: cargar los tubos en el catálogo, o aprobar el uso de la tabla de la plantilla.
- **Largo de barra:** en las cañerías, `LARGO_BARRA_MM` vale 6 (son metros), mientras que en los perfiles vale 6000 (milímetros). Aquí se lee como 6 m.
- **Pernos:** el catálogo no dice su calidad ni su tensión de fluencia. La planilla calcula su área con 0,6·Fy del poste.
