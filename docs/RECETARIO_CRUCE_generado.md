# Cruce del RECETARIO con el catálogo maestro (generado)

Generado por `herramientas/recetario_a_csv.py` desde `insumos/recetario_2026-11-11.xlsx` (sha256 `9c8a60d8e3e56f75…`). Uso interno.
Solo medidas y pesos: no se copian precios, costos, márgenes ni valor por kilo.

kg/m teórico = π·(Ø − e)·e·7,85/1000 (tubo de acero). Sirve para detectar medidas mal digitadas, no para reemplazar el dato de ORBE.

## Resumen

- Hoja RECETARIO: 64 materiales (41 cañerías y 23 tubos redondos).
- Cañerías que coinciden con el catálogo maestro (Ø, espesor y kg/m): **18**.
- Mismo Ø y espesor, distinto kg/m: **0**.
- Están en el recetario y no en el catálogo (con ese Ø y espesor): **22**.
- Están en el catálogo y no en el recetario: **11**.
- Filas repetidas en el recetario: **1**.
- Tubos redondos con medidas coherentes: **19** (van a `datos/tubos_recetario.csv`). Con medidas incoherentes: **4** (no se cargan).
- Postes cuadrados: **70** · postes facetados: **10**.

## HALLAZGOS en el recetario (no se corrigió el archivo original)

### Tubos redondos con medidas que no calzan con su peso (no se cargaron)

| Fila | Norma | Medida | Ø (mm) | e (mm) | kg/m recetario | kg/m teórico | Diferencia |
|---|---|---|---|---|---|---|---|
| 179 | TUBO REDONDO | 1" | 25.4 | 2 | 1.015 | 1.154 | -12.1 % |
| 191 | TUBO REDONDO | 1" 3/4 | 1.5 | 2 | 1.59 | — |  |
| 195 | TUBO REDONDO | 1" 3/4 | 2.5 | 2 | 2.09 | 0.025 | +8374.7 % |
| 211 | TUBO REDONDO | 2" 1/2 | 63.5 | 2.5 | 3.03 | 3.761 | -19.4 % |

HIPÓTESIS: 1¾" son 44,45 mm. El peso de la fila 191 calza con Ø44,45 × 1,5 y el de la fila 195 con Ø44,45 × 2,0: el diámetro quedó mal digitado. Confirmar con ORBE.

### Cañerías del recetario que no están en el catálogo con ese Ø y espesor

| Fila | Norma | Medida | Ø (mm) | e (mm) | kg/m recetario | kg/m teórico | Diferencia |
|---|---|---|---|---|---|---|---|
| 11 | ISO R65 | 1" | 26.67 | 2.6 | 1.98 | 1.543 | +28.3 % |
| 47 | ASTM A53 | 2" 1/2 | 73.02 | 5.16 | 8.63 | 8.635 | -0.1 % |
| 87 | ASTM A53 | 10" | 273.5 | 4.78 | 31.62 | 31.677 | -0.2 % |
| 91 | ASTM A53 | 10" | 273.5 | 6.35 | 41.75 | 41.836 | -0.2 % |
| 95 | ASTM A53 | 10" | 273.5 | 7.92 | 46.49 | 51.873 | -10.4 % |
| 99 | ASTM A53 | 10" | 273.5 | 9.27 | 60.29 | 60.406 | -0.2 % |
| 103 | ASTM A53 | 12" | 323.85 | 5.16 | 40.55 | 40.554 | -0.0 % |
| 107 | ASTM A53 | 12" | 323.85 | 6.35 | 49.71 | 49.721 | -0.0 % |
| 111 | ASTM A53 | 12" | 323.85 | 7.92 | 61.69 | 61.707 | -0.0 % |
| 115 | ASTM A53 | 12" | 323.85 | 9.52 | 73.78 | 73.798 | -0.0 % |
| 119 | ASTM A53 | 14" | 355.6 | 6.35 | 54.69 | 54.693 | -0.0 % |
| 123 | ASTM A53 | 14" | 355.6 | 9.52 | 81.25 | 81.252 | -0.0 % |
| 127 | ASTM A53 | 16" | 406.4 | 6.35 | 62.64 | 62.648 | -0.0 % |
| 131 | ASTM A53 | 16" | 406.4 | 9.52 | 93.17 | 93.178 | -0.0 % |
| 135 | ASTM A53 | 18" | 457 | 6.35 | 70.6 | 70.572 | +0.0 % |
| 139 | ASTM A53 | 18" | 457 | 9.52 | 105.1 | 105.058 | +0.0 % |
| 143 | ASTM A53 | 20" | 508 | 6.35 | 75.55 | 78.559 | -3.8 % |
| 147 | ASTM A53 | 20" | 508 | 9.52 | 117.02 | 117.032 | -0.0 % |
| 151 | ASTM A53 | 22" | 558.8 | 6.35 | 86.5 | 86.514 | -0.0 % |
| 155 | ASTM A53 | 22" | 558.8 | 9.52 | 129.1 | 128.959 | +0.1 % |
| 159 | ASTM A53 | 22" | 610 | 6.35 | 92.793 | 94.532 | -1.8 % |
| 163 | ASTM A53 | 22" | 610 | 9.52 | 140.88 | 140.979 | -0.1 % |

### Cañerías del catálogo que no están en el recetario

| Material | Norma | Medida | Ø (mm) | e (mm) | kg/m |
|---|---|---|---|---|---|
| ISO-1 | ISO R65 | 1" | 33.4 | 2.6 | 1.98 |
| ASTM-0_5-2_77 | ASTM A53 | 0.5" | 21.34 | 2.77 | 1.27 |
| ASTM-0_75-2_87 | ASTM A53 | 0.75" | 26.67 | 2.87 | 1.69 |
| ASTM-1-3_38 | ASTM A53 | 1" | 33.4 | 3.38 | 2.5 |
| ASTM-1_25-3_56 | ASTM A53 | 1.25" | 42.16 | 3.56 | 3.39 |
| ASTM-1_5-3_68 | ASTM A53 | 1.5" | 48.26 | 3.68 | 4.05 |
| ASTM-2_5-5_16 | ASTM A53 | 2.5" | 76.1 | 5.16 | 8.63 |
| ASTM-10-4_78 | ASTM A53 | 10" | 273.05 | 4.78 | 31.62 |
| ASTM-10-6_35 | ASTM A53 | 10" | 273.05 | 6.35 | 41.75 |
| ASTM-10-7_92 | ASTM A53 | 10" | 273.05 | 7.92 | 46.49 |
| ASTM-10-9_27 | ASTM A53 | 10" | 273.05 | 9.27 | 60.29 |

Lectura de las dos tablas anteriores (HIPÓTESIS, confirmar con ORBE):
- ISO R65 1": el recetario dice Ø26,67 (el mismo de ¾") y el catálogo Ø33,4. El peso 1,98 kg/m calza con Ø33,4: error de digitación en el recetario.
- ASTM A53 2½": recetario Ø73,02 y catálogo Ø76,1, con el mismo espesor y peso. Ø73,02 es la medida nominal ASTM de 2½".
- ASTM A53 10": recetario Ø273,5 y catálogo Ø273,05, con los mismos espesores y pesos. La medida nominal ASTM es 273,05.
- ASTM A53 "22"" con Ø610: 610 mm corresponde a 24".

### Cañerías cuyo peso se aleja más de 5 % del teórico

| Fila | Norma | Medida | Ø (mm) | e (mm) | kg/m recetario | kg/m teórico | Diferencia |
|---|---|---|---|---|---|---|---|
| 11 | ISO R65 | 1" | 26.67 | 2.6 | 1.98 | 1.543 | +28.3 % |
| 95 | ASTM A53 | 10" | 273.5 | 7.92 | 46.49 | 51.873 | -10.4 % |

### Filas repetidas

| Fila | Norma | Medida | Ø (mm) | e (mm) | kg/m recetario | kg/m teórico | Diferencia |
|---|---|---|---|---|---|---|---|
| 43 | ASTM A53 | 2" | 60.32 | 3.91 | 5.44 | 5.439 | +0.0 % |

### Mismo Ø y espesor, distinto kg/m

Ninguna.
