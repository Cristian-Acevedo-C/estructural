# Fase 5 · Cuadrado y octogonal por nombres, y control cruzado con las memorias en Excel

Fecha: 11-11-2026. Uso interno. Nada de esto va a una web.

Cristian pidió "continúa con las fases". No había una Fase 5 definida: se tomó el primer pendiente técnico que no depende de datos de ORBE ni del calculista (la configuración por nombres para cuadrado y octogonal, pendiente desde la Fase 2).

## 1. Configuración por nombres para las 6 hojas que faltaban

El motor ahora cubre las 18 hojas de cálculo de la planilla con `validar(config)`.

| Sección | Ganchos | Hoja | Claves del tramo |
|---|---|---|---|
| `cuadrada` | 0 / 1 / 2 | `P.Recto Cuad.` / `… 1 gancho` / `… 2 ganchos` | `altura_m`, `ancho_cm`, `espesor_cm` |
| `octogonal` | 0 / 1 / 2 | `P.Var. Octogonal` / `… 1 gancho` / `… 2 ganchos` | `altura_m`, `diametro_superior_cm`, `diametro_base_cm`, `espesor_cm` |

Diferencias con las hojas circulares (todas leídas de la planilla, por rótulos):
- **Un solo cuerpo.** La planilla no tiene cuadrado ni octogonal de varios tramos.
- **Gancho del poste cuadrado:** se describe con `d1_cm`, `d2_cm`, `d3_cm` y `t_cm`, no con diámetro y radio.
- **Octogonal con 2 ganchos:** agrega `cable_lateral_kg` (rótulo "Cable lateral · H (Kg)").
- **Coeficiente de forma por omisión:** 1,6 en cuadrada y 0,7 en octogonal (0,6 en circular). Es el valor que la planilla trae bloqueado en esas hojas.
- **Frecuencia por traslación:** las hojas octogonales no la entregan con el rótulo `f =`; no sale en `salidas`.

Ejemplo:

```json
{"seccion": "cuadrada", "tramos": [{"altura_m": 6, "ancho_cm": 10, "espesor_cm": 0.3}],
 "sobrecarga_kg": 20, "viento_tablero_kg": 20, "viento": {"velocidad_kmh": 120},
 "proyectores": {"alto_cm": 30, "ancho_cm": 30}}
```

## 2. Motor contra Excel recalculado (HECHO)

`herramientas/fase3_excel.py --secciones cuadrada,octogonal --por-hoja 25 --semilla 20261111`. Detalle: `trabajo/fase3/resultado_20261111.json`.

- **Casos:** 150 configuraciones nuevas (25 por hoja), recalculadas en una copia de la planilla con macros desactivadas.
- **Fórmulas:** 22.375 comparadas, **0 distintas** (diferencia relativa máxima 6·10⁻¹⁴).
- **Veredictos:** 800 comparados, **0 distintos**. 135 casos cumplen y 15 no.
- **Plantilla:** intacta (SHA-256 igual antes y después).
- **Medidas de prueba.** El catálogo maestro no trae tubos cuadrados ni octogonales (`datos/tubos.csv` vacío), así que anchos, diámetros y espesores se sortearon en rangos plausibles. Son casos de prueba del motor, no productos de ORBE.

**Límite de esta comparación.** Estas entradas están bloqueadas en la planilla y no se pudieron variar en Excel (quedaron en su valor original en los 150 casos):

| Entrada | Hojas | Valor fijo |
|---|---|---|
| Coeficiente de forma | las 6 | 1,6 (cuadrada) · 0,7 (octogonal) |
| Viento sobre el tablero | las 4 con gancho | 0 |
| `t` del gancho | cuadrada con 1 y 2 ganchos | 30 cm |
| Cable lateral H | octogonal con 2 ganchos | 330 kg |

El motor acepta otros valores y **avisa** (lista `avisos`), igual que en las circulares. `motor/modelo/bloqueadas_B.json` se regeneró: 132 entradas bloqueadas en 17 hojas.

## 3. Control cruzado con las 21 memorias en Excel (HECHO)

El 11-11 se armaron 21 memorias `Memoria_Calculo_<plano>.xlsm` con Excel, una por plano REV. M de hasta 4 cuerpos (`insumos/interno_NO_PUBLICAR/memorias_calculo_postes/`). `herramientas/fase5_memorias.py` lee lo que Excel dejó guardado en cada una y lo compara con el motor.

- **Resultado:** 21 memorias, 301 veredictos y todas las salidas: **0 diferencias**.
- 17 cumplen y 4 no (9Ma, 9Mb, 10Ma y 10Mb, por interacción flexo-compresión).
- **Coherencia con la Fase 4.** Las memorias de 4 cuerpos usan V = 50 kg (valor heredado de la hoja). La capacidad a 120 km/h de la Fase 4 para esos cuatro postes es 42,5 · 47,9 · 30,8 · 36,1 kg, menor que 50 kg: por eso no cumplen. La cabeza de referencia de la Fase 4 no es idéntica a la de la hoja de 4 tramos, así que la comparación es aproximada, pero no hay contradicción.
- Esas cargas son heredadas de la planilla, no de diseño. El "cumple / no cumple" de las memorias no dice si el poste sirve para una luminaria concreta.

## 4. HALLAZGOS

- **Pernos por omisión.** El motor usa 4 pernos si no se indican. Las hojas cuadradas y octogonales traen guardados 5, 10 y 16. Hay que indicar `pernos` siempre en estas secciones.
- **Cable lateral fijo en 330 kg** y bloqueado en la octogonal de 2 ganchos: parece un dato de un proyecto anterior que quedó como constante.
- **HIPÓTESIS (para el calculista).** La hoja octogonal calcula el área con una fórmula de octógono, pero la inercia con la de un tubo circular (`π/64·(d⁴ − (d − 2e)⁴)`). Si `d` es la medida entre vértices, la inercia real del octógono es menor. Una estimación gruesa da entre 3 % y 10 % menos; no es un cálculo validado. El motor replica la planilla tal cual.

## 5. Arreglo menor

`fase3_excel.py` dejaba copias temporales sin borrar: `insumos/` es de solo lectura y la copia heredaba ese atributo. Ahora se le quita al copiar.

## 6. No hecho (sigue pendiente)

- **Carga de diseño real por poste** (luminaria, área, altura de montaje): la define ORBE.
- **Postes de 5 cuerpos** (11Ma, 12Ma y 12Mb): requieren extender la planilla o un cálculo propio validado por el calculista.
- **Conectar el asistente de vendedores** (`insumos/interno_NO_PUBLICAR/ventas-chat/`) a este motor. Hoy usa el motor v1 de ORBE Experience, que es otro cálculo. Conviene hacerlo después de tu revisión de las Fases 2 a 5.

## Pruebas

`python -m pytest pruebas -q`: **85 de 85** (24 nuevas): entradas de las 18 hojas, configuración por nombres de cuadrada y octogonal, errores de configuración, aviso de milímetros, coeficiente de forma por omisión según sección, aviso del cable lateral bloqueado y el generador de casos para las secciones nuevas.
