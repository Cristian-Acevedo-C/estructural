# Especificación de la "Plantilla Memoria de Cálculo" (Fase 1: ingeniería inversa)

Fecha: 10-11-2026. Solo lectura de las plantillas; no se programó el validador.
Uso interno: describe la receta de cálculo (tramos, espesores, placa, pernos). Nada de aquí va a una web.

Marcas: **HECHO** (sale de una celda o del VBA, con su ubicación) · **HALLAZGO** (algo que se deduce leyendo las
fórmulas) · **HIPÓTESIS** (interpretación que debe confirmar el calculista) · **RECOMENDACIÓN**.

Material de apoyo, generado por los scripts de `herramientas/` (se puede regenerar):

| Archivo | Qué trae |
|---|---|
| `docs/ANEXO_B_generado.md` | Por cada hoja de la versión B: entradas de las que dependen los veredictos (celda, rótulo, valor), cada veredicto con la fórmula que compara, constantes escritas en las fórmulas y referencias rotas |
| `docs/ANEXO_A_generado.md` | Lo mismo para la versión A |
| `docs/COMPARACION_VERSIONES.md` | Diferencias entre A y B: hojas, fórmulas, constantes y VBA |
| `trabajo/volcado_*/` | Volcado completo: cada celda con fórmula y valor guardado, hojas, metadatos y VBA (`vba.txt`) |

---

## 1. Las tres versiones

| Copia en `insumos/` | Original | Guardado por última vez (metadatos) | Hojas | Fórmulas |
|---|---|---|---|---|
| A `plantilla_A_2026-10-16.xlsm` | `Plantilla Memoria de Calculo.xlsm` | 10-12-2025, Jonathan Tello | 22 | 3.208 |
| B `plantilla_B_2026-10-21.xlsm` | `Plantilla Memoria de Calculo (1).xlsm` | 02-06-2026, Felipe Valdés | 22 | 3.610 |
| C `plantilla_C_2026-10-21.xlsm` | `Plantilla Memoria de Calculo (2).xlsm` | igual a B | 22 | 3.610 |

- **HECHO.** B y C son el mismo archivo byte a byte (mismo SHA-256, `insumos/SHA256.txt`). En la práctica hay **dos** versiones.
- **HECHO.** El libro fue creado en 2000 (autor en metadatos: Christian Folch); las macros dicen "grabada el 30/10/00 por Manuel Tapia".
- **HECHO.** B es la más reciente (guardada en junio de 2026 contra diciembre de 2025).
- **HECHO. Qué cambia de A a B:**
  - B agrega la hoja **CAÑERIAS** (tabla de cañerías ISO serie liviana, ASTM y tubo; 402 fórmulas). Ninguna hoja de cálculo la usa.
  - B elimina la hoja **Precios**. Por eso 8 fórmulas de la hoja oculta `Datos` (Q3:T4) quedan en `#REF!`, y el formulario de cubicación (`UserForm2`) que leía precios de cañería queda roto.
  - En las 20 hojas comunes **ninguna fórmula de cálculo cambió**. Las otras diferencias son 71 valores de entrada: la última configuración que alguien dejó cargada en cada hoja.
  - El VBA es el mismo. Solo cambia el orden de los módulos y desaparece el módulo de la hoja Precios.
- **HALLAZGO.** La configuración guardada en B en "P.Recto Circ. 1 gancho" tiene el poste de 114,3 cm de diámetro y 3,05 cm de espesor, y el gancho de 88,9 cm. Son medidas en milímetros escritas en campos de centímetros (114,3 mm es una cañería de 4"). Los valores guardados en B no sirven como caso de prueba; los de A sí son coherentes (por ejemplo 8,9 cm × 0,3 cm).
- **RECOMENDACIÓN.** Usar las fórmulas de B, que son las mismas de A, y los casos guardados en A como primeros casos de prueba de la Fase 3.

## 2. Cómo está armado el libro

- **HECHO.** El cálculo vive entero en las fórmulas de las celdas. El VBA solo navega:
  - `UserForm1` elige una de las 18 hojas de cálculo.
  - `UserForm2` arma la cubicación con precios de cañería, hoy roto en B.
  - `ABOUT`/`ABOUT1` son pantallas de inicio.
  - Ninguna macro calcula esfuerzos ni decide si cumple.
- **HECHO.** No hay nombres definidos ni validaciones de datos. Las entradas son celdas libres: se puede escribir cualquier valor.
- **HECHO.** La hoja oculta `Datos` copia las alturas de cada hoja (para la cubicación) y guarda la hoja activa (Q8). Ninguna hoja de cálculo lee `Datos`.

Las 18 hojas de cálculo son seis familias. La sección y la cantidad de tramos cambian el método; el gancho agrega cargas.

| Familia | Hojas (sin gancho / 1 gancho / 2 ganchos) | Sección | Tramos |
|---|---|---|---|
| Recto circular | `P.Recto Circ.` / `… 1 gancho` / `… 2 ganchos` | tubo circular | 1 |
| Recto cuadrado | `P.Recto Cuad.` / `… 1 gancho` / `… 2 ganchos` | tubo cuadrado | 1 |
| Variable circular 2 tramos | `P.Var.2 Tramos Circ.` / `P.Var. 2 Tramos Circ. 1 gancho` / `… 2 ganchos` | tubos circulares | 2 |
| Variable circular 3 tramos | `P.Var.3 Tramos Circ.` / `… 1 gancho` / `… 2 ganchos` | tubos circulares | 3 |
| Variable circular 4 tramos | `P.Var.4 Tramos Circ.` / `… 1 gancho` / `… 2 ganchos` | tubos circulares | 4 |
| Variable octogonal | `P.Var. Octogonal` / `… 1 gancho` / `… 2 ganchos` | octógono cónico (diámetro superior y de base) | 1 |

Para la Fase 4 (tubulares hasta 12 m) importan las familias **recto circular** y **variable circular de 2 a 4 tramos**, con y sin gancho.

## 3. Unidades

**HECHO**, según los rótulos:
- **Alturas:** en m.
- **Diámetros, anchos y espesores:** en cm.
- **Cargas:** en kg.
- **Tensiones:** en kg/cm².
- **Momentos:** en kg·cm.
- **Viento:** velocidad en km/h, presión en kg/m².

Las fórmulas pasan de m a cm multiplicando por 100.

## 4. Entradas

### 4.1 Recto circular (`P.Recto Circ.`), versión B

| Celda | Nombre | Unidad | Valor guardado en B | Valores permitidos |
|---|---|---|---|---|
| D12 | Tensión de fluencia Fy | kg/cm² | 2400 | libre (sin validación) |
| A15 | h, altura del poste | m | 4 | libre |
| A18 | d, diámetro del poste | cm | 11,4 | libre |
| A21 | e, espesor del poste | cm | 0,36 | libre |
| A24 | P, sobrecarga | kg | 70 | libre |
| A27 | V, viento en el tablero (fuerza horizontal en la punta) | kg | 80 | libre |
| E44 | ¿Ingresar velocidad del viento? | texto | "SI" | "SI" o "NO" ("si" también vale; cualquier otro texto deja el factor de viento en 1) |
| H44 | Velocidad del viento (rótulo en G44) | km/h | 120 | libre |
| B51 | Coeficiente de forma | — | 0,6 | libre |
| C85 | β, razón de amortiguamiento | — | 0,02 | libre |
| C86 | CL, coeficiente de Von Karman | — | 0,2 | libre |
| B143 | G, módulo de corte | kg/cm² | 840000 | libre |
| D146 | Altura de proyectores | cm | 530 | libre |
| D147 | Ancho total de proyectores | cm | 110 | libre |
| C284 | Número de pernos | — | 4 | libre |
| C278 | Precio del kilo de acero | $/kg | (no se copia) | fuera de alcance |

**HECHO. Bloque auxiliar escondido a la derecha (columnas K–W).** Tiene alturas h1–h3 (S12:U12, en 0), diámetros d1–d3 (K16:M16) y espesores e1–e3 (K19:M19) de tres "secciones".
- **HALLAZGO.** Es un resto de las hojas de varios tramos. La altura total sí lo suma: `B15 = S12+T12+U12+A15`. Si alguien escribe un valor ahí, cambia L sin que se vea en el formulario.
- **HALLAZGO.** El mismo bloque alimenta 9 veredictos rotos (ver §7).

### 4.2 Variable circular de N tramos (`P.Var.2/3/4 Tramos Circ.`)

**HECHO.** Las mismas entradas generales que §4.1 (Fy, P, V, viento, coeficiente de forma, β, CL, G, proyectores, número de pernos). Además lleva una altura, un diámetro y un espesor por tramo:
- **2 tramos:** h1 y h2 en A15 y B15; d1 y d2 en A18 y B18; e1 y e2 en A21 y B21.
- **3 y 4 tramos:** siguen en C15, D15, etc.

**HALLAZGO.** El tramo 1 es el **superior** y el último es la **base**. Por ejemplo, en 2 tramos la base es el tramo 2: `B223 = 0.75*H75/C34` usa la carga vertical total.

**HECHO.** En estas hojas también hay entradas que solo existen aquí:
- **Módulo E:** en K132, con 2100000. En la hoja recta va escrito dentro de las fórmulas.
- **Factor de seguridad de pandeo general:** en E215, con 1,67.

**HECHO.** La altura total también suma un bloque auxiliar escondido (en 2 tramos, `C15 = S13+T13+A15+B15`).

La lista exacta de celdas de cada hoja está en `docs/ANEXO_B_generado.md`, en "Entradas de las que dependen los veredictos".

### 4.3 Con gancho (`… 1 gancho`, `… 2 ganchos`)

**HECHO.** Ejemplo en `P.Recto Circ. 1 gancho`:

| Celda | Nombre | Unidad |
|---|---|---|
| D15 | Diámetro del gancho | cm |
| D18 | Espesor del gancho | cm |
| D21 | R, radio | cm |
| D24 | Dist | cm |
| D27 | t | cm |
| F27 | t | cm (ninguna fórmula de la hoja la usa) |
| A24 | P, peso de la luminaria | kg |

En las otras hojas con gancho, las celdas cambian (ver el anexo).

### 4.4 Recto cuadrado y octogonal

- **HECHO. Cuadrado.** B, el ancho, va en B18, y e en B21. Las demás entradas, como en §4.1, pero corridas: el viento está en E46/H46.
- **HECHO. Octogonal.** Lleva d superior en A18, d de base en B18 y un espesor único en A21. Las demás entradas, como en §4.1.

## 5. Cálculo, paso a paso (hoja base `P.Recto Circ.`)

Todas las celdas son de la versión B, iguales en A.

### 5.1 Propiedades de la sección (fila 33)

**HECHO.**

```
Área   C33 = ROUND((3.14159/4)*(d² − (d−2e)²), 2)                 cm²
Peso   B33 = ROUND(7850*C33/10000, 2)                              kg/m
I      D33 = ROUND((3.14159/64)*(d⁴ − (d−2e)⁴), 2)                 cm⁴
W      E33 = ROUND(I/(0.5*d), 2)                                   cm³
i      F33 = ROUND((I/A)^0.5, 2)                                   cm
```

**HALLAZGO.** Cada propiedad se redondea a 2 decimales y lo siguiente se calcula sobre el valor redondeado. El motor tiene que redondear igual para coincidir con 0,1 % de tolerancia.

### 5.2 Viento estático

**HECHO.**
- **Factor por velocidad:** `D48 = IF(E44="SI", (V/120)^2, 1)`.
- **Si E44 = "NO":** la nota A46 dice "calculadas a partir de la NCh 432 Of. 72". Ninguna fórmula cambia, salvo que el factor queda en 1.
- **Fuerza horizontal equivalente del fuste, G51:**
  - Si h ≤ 4 m: `D48*Cf*70*d/100*h`.
  - Si h > 4 m: `D48*Cf*d/100*(70*4 + 32.595*LN(h^h/4^4) − 4*(h−4))`.
- **Punto de aplicación (centro de gravedad de la carga), F51:** usa 32,595 y 0,3772.

**HALLAZGO.** G51 es la integral, sobre la altura, de una presión:
- **Hasta 4 m:** q(z) = 70 kg/m².
- **Sobre 4 m:** q(z) = 32,595·ln(z) + 28,594 kg/m², con z en m.

Se comprueba porque ∫(a·ln z + b)dz = a·ln(h^h/4^4) + (b − a)(h − 4), con b − a = −4. El 28,594 aparece escrito en las hojas con gancho. F51 es ∫z·q dz / ∫q dz, y 0,3772 = b/a − 1/2.

**HALLAZGO.** El perfil salta de 70 a 73,8 kg/m² en z = 4 m.

**HIPÓTESIS.** Que este perfil corresponda a la NCh 432 Of. 72 con una velocidad base de 120 km/h. La planilla no lo dice; lo tiene que confirmar el calculista.

### 5.3 Cargas verticales

**HECHO.**
- **Peso propio:** `B75 = Peso(kg/m)*h`.
- **Carga vertical total:** `H75 = B75 + P` (más los tramos del bloque auxiliar, que valen 0).

### 5.4 Resonancia por desprendimiento de vórtices (fuerza lateral)

**HECHO.**

```
Frecuencia natural  D138 = ROUND(1/T, 2)            T = 0.2*SQRT(Pm/K)      (J133)
                    K = 3*2100000*I/L³ (J131)       Pm = Peso propio + 0.5*P (J132), L en cm
Vcr  C88 = f*(d/100)/0.2                            m/s
qcr  C89 = Vcr²/16                                  kg/m²
FL   C90 = ROUND((1/(2β))*CL*(d/100)*qcr, 2)        kg/m
```

**HALLAZGO.** 0,2 dentro de T equivale a 2π/√g con g ≈ 981 cm/s² (0,2006). 0,2 dentro de Vcr parece el número de Strouhal. Ninguno de los dos está rotulado.

### 5.5 Reacciones en la base

**HECHO.**

```
T88  = (L + hproy/100/2)*V*100 + G51*F51*100          momento del viento (kg·cm)
M0   B108 = SQRT(T88² + (0.5*FL*L²*100)²)             kg·cm
V0   B109 = SQRT((V + G51)² + (FL*L)²)                kg
N0   B110 = H75                                       kg
```

**HALLAZGO.** El momento por vórtices se suma al del viento como si actuaran en direcciones perpendiculares: raíz de la suma de cuadrados.

### 5.6 Verificaciones con veredicto (cumple / no cumple)

| # | Verificación | Celda veredicto | Fórmula de lo que se compara | Criterio de cumple |
|---|---|---|---|---|
| 1 | Pandeo general (compresión) | D218 | fa: `B218 = 0.75*N0/A`. Fa: `B212`; con Cc `C196 = (2*3.1415²*2100000/Fy)^0.5`, KL/i `C199 = 2*L*100/i`, FS `D209 = IF(KL/i<Cc, 5/3 + 3/8·λ − 1/8·λ³, 23/12)` con λ = (KL/i)/Cc; `B212 = IF(KL/i<Cc, (1/FS)*(1 − 0.5·λ²)*Fy, (1/FS)*(3.14159²*2100000/(KL/i)²))` | fa ≤ Fa |
| 2 | Pandeo local, compresión uniforme | E229 | D/t `B226 = d/e`; `D229 = IF(D/t ≤ 267330/Fy, Fy, IF(D/t ≤ 844200/Fy, 0.75·Fy + 66832.5/(D/t)))` | fa ≤ Fa local; si D/t > 844200/Fy: "DISMINUIR D / t" |
| 3 | Pandeo local, flexión pura | E230 | `D230 = IF(D/t ≤ 422100/Fy, Fy, IF(D/t ≤ 844200/Fy, 0.7·Fy + 126630/(D/t)))`; compara fb (D242) | fb ≤ Fb local; si D/t > 844200/Fy: "DISMINUIR D / t" |
| 4 | Tensión de flexión en la base | F242 | fb `D242 = 0.75*M0/W`; Fm `B238 = 0.66*Fy` | fb ≤ Fm |
| 5 | Torsión | F255 | Mt = `E249` (viento en tablero, **0 escrito a mano**) + no se suma; τ `C255 = E250*(d/2)/Jp` con `E250 = (bproy/4)*(Vcr_t²/16)*(hproy*bproy/2/10000)*2`, `Vcr_t D252 = f_t*(d/100)/(2*0.2)`, f_t `G165 = ROUND((2·3.14159)⁻¹*SQRT(G*Jp/(L*100*I_tablero)), 2)`, `Jp B144 = 2*I`, `I_tablero F161 = (1/12)*hproy*bproy³*P/(hproy*bproy)` | τ ≤ 0,4·Fy |
| 6 | Interacción flexo-compresión | F268 | `C268 = fb/Fm + fa/Fa` | C268 < 1 (con ≥ 1 no cumple) |

**HECHO.** Hay salidas sin veredicto de cumple: el pernos y la placa los dimensiona la planilla, no los verifica.

| Salida | Celda | Fórmula |
|---|---|---|
| Diámetro del círculo de pernos | C285 | `d + 10` (cm) |
| Carga axial por perno | C286 | `−(Peso propio + P)/n + 4*M0/(n*Dp)` (kg) |
| Área de tracción requerida | C287 | `T/(0.6*Fy)` (cm²) |
| Diámetro nominal del perno | C288:C290 | tabla por umbrales de área: ≤0,21 → 1/4"; ≤0,5 → 3/8"; ≤0,92 → 1/2"; ≤1,46 → 5/8"; ≤2,15 → 3/4"; ≤2,98 → 7/8"; ≤3,91 → 1"; ≤4,92 → 1 1/8"; ≤6,25 → 1 1/4"; ≤7,45 → 1 3/8"; ≤9,06 → 1 1/2"; ≤10,4 → 1 5/8"; ≤12,3 → 1 3/4"; ≤14,3 → 1 7/8"; ≤16,1 → 2"; ≤21 → 2 1/4"; ≤25,8 → 2 1/2"; más: "Aumente número de pernos" |
| Espesor de placa base | C293 | `SQRT((6*n*T*5)/(3.14159*d*0.75*Fy))` (cm) |

**HECHO. Lo que la planilla NO verifica:**
- **Soldadura:** no hay ninguna verificación.
- **Deflexión:** no hay deflexión con límite. Hay cálculos de giros y desplazamientos en R120:V126 ("t2(x2)", "d2(x2)"…), pero ningún veredicto los usa y dependen del bloque auxiliar.
- **Esbeltez:** el texto de A205 menciona "Ce < KL/i < 200", pero ninguna fórmula comprueba KL/i ≤ 200.
- **Placa y pernos:** no tienen criterio de cumple; solo se dimensionan.

## 6. Diferencias por familia

### 6.1 Variable circular de N tramos

**HECHO.** Ejemplo en `P.Var.2 Tramos Circ.`:

- **Viento:**
  - Cada tramo tiene su fuerza y su punto de aplicación (G51/F51 para el tramo 1, G52/F52 para el 2), integrando el mismo perfil de presión sobre la franja de altura del tramo.
  - El momento se calcula en la base de cada tramo (D96, D97) con los tramos de arriba.
- **Pandeo general:** otro método, el de una columna escalonada.
  - `B215 = 2.467/((1 − …)(1 − …)(1 − …))`, donde 2,467 ≈ π²/4.
  - Pcr `B216 = B215*2100000*I_base/(L*100)²`.
  - Fa `B217 = Pcr/A_base/FS`, con FS = E215 = **1,67 fijo**.
  - Cada tramo compara su fa = 0,75·(carga sobre su base)/A_tramo (B222, B223) con **el mismo** Fa.
  - **HALLAZGO.** El recto de un tramo usa el FS variable de §5.6 (#1); el de N tramos, un FS fijo. Son métodos distintos.
- **Pandeo local, flexión, interacción:** igual que en §5.6, pero por tramo (D/t, fb = 0,75·M_i/W_i, interacción por tramo).
- **Frecuencia por traslación:**
  - Usa una matriz de rigidez de vigas por tramo (L132:O135).
  - La condensa con `MMULT(MMULT(Kbi, MINVERSE(Kii)), Kib)` (fórmula matricial L138).
  - Kc = Kbb − …, y `T = 2·3.1415·SQRT((W/980)/Kc)` (g = 980).
- **Torsión:** usa el Jp de un diámetro y un espesor medios ponderados por largo (F144, G144, C144).
- **Pernos y placa:** igual que en la hoja recta, con el diámetro de la base.

### 6.2 Con gancho

**HECHO.** Ejemplo en `P.Recto Circ. 1 gancho`:

- **Peso del gancho:** `B76 = 0.00785*(A_tubo_gancho*(2·3.1415·R/4) + (Dist − R)*3.1415*t²/4)`. Es un cuarto de círculo de tubo más un tramo recto calculado como **barra maciza** de diámetro t.
- **Viento sobre el gancho:** `G52 = D48*(1.57*R*d_g*Cf*(32.595*LN(h + R/100) + 28.594)/10000)`, aplicado en `F52 = (h*100 + 0.63*R)/100`.
- **Momento en la base:** `B108 = SQRT((T88 + G52*F52*100)² + (0.5*FL*L²*100 + Peso_arco*0.37*R + Peso_recto*(R + (Dist − R)/2) + Dist*P)²)`. El momento por el peso excéntrico del gancho y la luminaria se suma en la dirección perpendicular al viento.
- **Dos ganchos:** el peso se duplica (B76 = 2·…). El momento en la base **no** suma pesos excéntricos: `B108 = SQRT((T88 + G52*F52*100)² + (0.5*FL*L²*100)²)`.
  - **HIPÓTESIS.** Supone ganchos opuestos que se equilibran. La planilla no lo dice.
- **Tensión en la base del gancho:** en las 10 hojas con gancho, de las dos versiones, la celda de "Tensiones en la base del gancho" es un **0 escrito a mano**, con su veredicto "cumple". Las celdas son D242, D240, D254, D255 y D241 en las de 1 gancho, y las equivalentes en las de 2.
  - **HALLAZGO.** Esa verificación da cumple siempre: el gancho no se verifica.

### 6.3 Recto cuadrado

**HECHO.**
- **Propiedades:** `A = B² − (B − 2e)²`, `I = (1/12)·(B⁴ − (B − 2e)⁴)`.
- **Pandeo local:**
  - `D229 = IF(B/t ≤ 2013/√Fy, Fy, IF(B/t ≤ 3229.18/√Fy, 70.35·(1.45·Fy/70.35)·(1 − 0.0001538·√Fy·B/t), 70.35·108000/(B/t)²))`.
  - Criterio distinto al circular: **fa + fb ≤ Fa** (E229).
- **Torsión:** `C251 = Mt*4.78/B³`.
  - **HALLAZGO.** 4,78/B³ es el coeficiente de una barra cuadrada **maciza**, no de un tubo.
- **HALLAZGO.** 70,35 convierte ksi a kg/cm². Es una fórmula pensada en unidades imperiales y adaptada.

### 6.4 Octogonal

**HECHO.**
- **Área:** `B33 = e*(6.122*d/2 − 3.31*e)`, la fórmula de un octógono.
- **Inercia:** `C33 = (3.14159/64)*(d⁴ − (d − 2e)⁴)`, la de un tubo **circular**.
  - **HALLAZGO.** El área es de octógono y la inercia de círculo: es inconsistente.
- **Pandeo local por cara:**
  - w/e `B208 = (d·0.3826)/e`.
  - `B210` con los límites 240/√(Fy/70,35) y 385/√(Fy/70,35), y el valor 108000·70,35/(w/e)².
  - Criterio fa + fb ≤ Fa local (D210).
- **Frecuencia:** `D133 = (3.9*(G138/2.54)/((G135/2.54)²))*SQRT(2100000*14.22/0.283)`, en pulgadas, psi y lb/in³ (0,283 lb/in³ es la densidad del acero).

## 7. Errores y riesgos encontrados

| # | Qué | Dónde | Efecto |
|---|---|---|---|
| 1 | Veredictos con `#REF!` | 9 por hoja en las de un tramo: recto circular, cuadrado y octogonal, con y sin gancho; 8 en algunas. Ejemplos: `P.Recto Circ.` D215:D217, F239:F241, F265:F267 | Muestran `#REF!` al lado de los veredictos buenos. Vienen del bloque de "tramo 1/2/3" copiado de las hojas de N tramos. Las hojas de N tramos no tienen ninguno |
| 2 | Tensión en la base del gancho = 0 fijo | 10 hojas con gancho, A y B | El gancho nunca se verifica |
| 3 | Momento torsional del viento en el tablero = 0 fijo | todas las hojas salvo `P.Var. Octogonal 1 gancho` (E227 sí lo calcula) | La torsión solo considera el vórtice |
| 4 | π con dos valores | 3,14159 en la mayoría; 3,1415 en Cc (C196), en el peso del gancho y en la frecuencia de N tramos | Diferencias menores, pero el motor tiene que copiarlas para coincidir |
| 5 | Redondeo intermedio | ROUND(…, 2) en propiedades, frecuencias, FL, Jp | Igual que el anterior |
| 6 | Bloque auxiliar suma a la altura | `B15 = S12+T12+U12+A15` (y equivalentes) | Un valor olvidado en columnas escondidas cambia L |
| 7 | Sin validación de datos | todas las entradas | Se aceptan mm en campos de cm (caso guardado en B, §1) |
| 8 | Hoja Precios eliminada | `Datos`!Q3:T4, `UserForm2` | Solo afecta la cubicación con precios (fuera de alcance) |
| 9 | Inercia circular en el octogonal | `P.Var. Octogonal` C33:C34 y en sus variantes | Tensiones y frecuencia con una sección que no es la real |
| 10 | Torsión de barra maciza en el cuadrado | `P.Recto Cuad.` C251 y en sus variantes | Subestima la tensión de corte del tubo |
| 11 | Mensaje equivocado | pandeo local por flexión dice "fa > Fa" cuando compara fb con Fb | Solo el texto |

## 8. Normas y coeficientes citados

- **HECHO. Única norma citada en el libro:** "NCh 432 of 72". Está en la nota de A46 (A48 en las cuadradas, A53 y A63 en las octogonales con gancho), y solo como texto. No hay ninguna otra norma, edición ni artículo citado.
- **HIPÓTESIS.** Ninguna de estas atribuciones está citada en la planilla; tiene que confirmarlas el calculista:
  - **Forma de las fórmulas:** se parecen a la especificación AISC de tensiones admisibles (ASD). Lo sugieren Cc, el FS de 5/3 a 23/12, Fm = 0,66·Fy y el corte en 0,4·Fy.
  - **Límites de pandeo local de los tubos:** 267330/Fy, 422100/Fy y 844200/Fy no los pude atribuir. No equivalen directamente a los límites en ksi que conozco: 3300/Fy da 232.023/Fy en kg/cm². Quedan como pregunta (§10).
  - **Factor 0,75:** el 0,75 sobre fa y fb equivale a un aumento de 1/0,75 = 33 % de las tensiones admisibles por carga de viento.
  - **Tabla de pernos:** parece áreas de tracción de pernos de rosca gruesa en pulgadas.

Coeficientes y su ubicación en `P.Recto Circ.`:

| Coeficiente | Valor | Celda o fórmula |
|---|---|---|
| Fy | 2400 kg/cm² | D12 (entrada) |
| E | 2100000 kg/cm² | dentro de C196, B212, J131 (en N tramos: K132) |
| G | 840000 kg/cm² | B143 |
| Densidad del acero | 7850 kg/m³ (0,00785 kg/cm³ en el gancho) | dentro de B33, B76 |
| Coeficiente de forma | 0,6 | B51 |
| Presión hasta 4 m | 70 kg/m² | dentro de G51, F51 |
| Perfil sobre 4 m | 32,595 · ln z + 28,594 | dentro de G51, F51, J51 (28,594 solo en ganchos) |
| Velocidad de referencia | 120 km/h | dentro de D48 |
| β amortiguamiento | 0,02 | C85 |
| CL Von Karman | 0,2 | C86 |
| Strouhal (sin rótulo) | 0,2 | dentro de C88, D252 |
| Presión dinámica | V²/16 | dentro de C89 |
| Factor en el período | 0,2 | dentro de J133 |
| K (pandeo de un tramo) | 2 | dentro de C199 |
| FS pandeo N tramos | 1,67 | E215 |
| Factor sobre fa y fb | 0,75 | dentro de B218, D242 |
| Fm | 0,66·Fy | B238 |
| Corte admisible | 0,4·Fy | dentro de F255 |
| Tracción admisible en perno | 0,6·Fy | dentro de C287 |
| Distancia del círculo de pernos | d + 10 cm | C285 |
| Voladizo de la placa | 5 cm | dentro de C293 |
| Límites de pandeo local | 267330, 422100, 844200 (/Fy); 66832,5; 126630; 0,7; 0,75 | dentro de D229, D230 |

## 9. Constantes escritas a mano y supuestos ocultos

Lista completa por hoja en los anexos ("Constantes escritas dentro de las fórmulas").

- **0 escritos a mano en lugar de cálculos:** tensión del gancho y torsión por viento en el tablero (§7, puntos 2 y 3).
- **Factor de seguridad de pandeo de N tramos:** 1,67 en E215, con aspecto de entrada y sin rótulo de norma.
- **Velocidad del viento:** solo cuenta si E44 dice "SI". Excel compara textos sin distinguir mayúsculas, así que "si" también vale. Pero "Sí", con tilde, o cualquier otro texto deja el factor en 1 sin avisar. (Corregido el 10-11 en la Fase 2: antes decía que "si" no valía.)
- **Período con g ≈ 981:** el 0,2 fijo (§5.4); en N tramos g = 980.
- **Vórtices y viento perpendiculares:** se combinan como fuerzas en direcciones perpendiculares (§5.5).
- **Tramo recto del gancho:** se calcula como barra maciza de diámetro t (§6.2).
- **Dos ganchos:** el momento por peso excéntrico se anula (§6.2).
- **Luminaria:** su peso se trata como sobrecarga P en el poste recto y como carga excéntrica a la distancia Dist en las hojas con gancho.
- **Viento del tablero:** se aplica a la altura L + mitad de la altura de los proyectores.
- **Pernos y placa:** se dimensionan, pero no se verifican.

## 10. Dudas que no pude resolver (para el calculista)

1. ¿El perfil q(z) = 70 kg/m² hasta 4 m y 32,595·ln z + 28,594 sobre 4 m sale de la NCh 432 Of. 72? ¿Para qué velocidad base y qué exposición? ¿Y cómo se elige el coeficiente de forma 0,6?
2. ¿De qué norma y edición salen Cc, el FS de 5/3 a 23/12, Fm = 0,66·Fy, el 0,4·Fy de corte, los límites de D/t y el factor 0,75? ¿El 0,75 es el aumento por viento?
3. ¿Por qué el pandeo de N tramos usa FS = 1,67 fijo y el de un tramo un FS variable? ¿Cuál vale para la Fase 4?
4. ¿Qué verificación del gancho debería existir? Hoy es 0: ¿tensión en el arranque del gancho con el peso de la luminaria y el viento?
5. ¿Qué son "Dist", "t" (D27) y "t" (F27) en el gancho? ¿El tramo recto es de verdad una barra maciza?
6. ¿Hay que verificar soldadura (fuste-placa, uniones entre tramos) y deflexión en la punta? ¿Con qué criterio y qué límite?
7. ¿Placa y pernos tienen criterio de cumple (flexión de placa, aplastamiento del hormigón, adherencia)? Hoy solo se dimensionan.
8. La tabla de diámetros de perno, ¿es de rosca gruesa UNC? ¿Qué calidad de perno supone (el 0,6·Fy usa la Fy del poste)?
9. En el octogonal, ¿la inercia circular es una aproximación aceptada o un error? ¿Y en el cuadrado, la torsión de barra maciza?
10. ¿Las hojas de un tramo deben conservar el bloque escondido de 3 secciones o es un resto?
11. ¿Qué versión es la oficial hoy? Las fórmulas de A y B son iguales, pero B perdió la hoja Precios.
12. **(Agregada el 10-11-2026, auditoría normativa de ORBE CONECTA.)** La planilla cita la NCh 432 Of. 72. El INN publicó la **NCh 432:2025** (27-06-2025, adopta ASCE/SEI 7-22). Según fuentes secundarias (madera21.cl, Instituto de la Construcción), un decreto del MOP la declaró norma oficial y derogó la versión antigua. **Falta confirmar el decreto y su fecha en el Diario Oficial.** Si se confirma, el perfil de viento de la planilla (duda 1) sale de una norma derogada. ¿Se rehace el viento con la NCh 432:2025 (velocidad básica por zona, exposición, factor de ráfaga) y, si es así, con qué datos de sitio? Mientras tanto, el motor replica la planilla tal como está, y eso no la hace vigente. Ver `orbe-conecta/docs/AUDITORIA_NORMATIVA.md` § 2.

## 11. Propuesta para la Fase 2 (sin empezar)

- **RECOMENDACIÓN. Primero:** replicar `P.Recto Circ.` y `P.Var.2/3/4 Tramos Circ.`, que son la base de los tubulares hasta 12 m.
  - Copiar los mismos redondeos y los mismos dos valores de π.
  - Reportar como "no verificado" lo que la planilla no verifica (gancho, soldadura, deflexión, placa), en vez de "cumple".
- **RECOMENDACIÓN. Después:** las variantes con gancho, replicando el 0 tal como está y marcándolo, hasta que el calculista defina la verificación del gancho.
- **RECOMENDACIÓN. Casos de prueba:**
  - Los valores guardados en A.
  - Un caso por familia preparado con el calculista.
  - Nunca los de B en "1 gancho" (unidades mezcladas).
