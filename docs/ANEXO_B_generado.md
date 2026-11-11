# Anexo generado: volcado_B_2026-10-21

Generado por `herramientas/analizar.py` a partir del volcado. No editar a mano.

## CUBICACIONES

Fórmulas: 8. Veredictos: 0 (0 con `#REF!` en su cadena). Fórmulas con `#REF!`: 0

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|

### Veredictos


### Constantes escritas dentro de las fórmulas (valor: veces)

`1`: 1, `100`: 1

## CAÑERIAS

Fórmulas: 402. Veredictos: 0 (0 con `#REF!` en su cadena). Fórmulas con `#REF!`: 0

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|

### Veredictos


### Constantes escritas dentro de las fórmulas (valor: veces)

`4`: 68, `2`: 67, `3`: 67, `5`: 67, `6`: 67, `1950`: 1, `200000`: 1, `1`: 1

## P.Recto Circ.

Fórmulas: 144. Veredictos: 16 (9 con `#REF!` en su cadena). Fórmulas con `#REF!`: 9 (S83, S84, S85, D215, D216, D217, M228, M229, M230)

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|
| D12 | Tension de Fluencia Fy (kg/cm2) | 2400 |
| S12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| T12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| U12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| A15 | h (m) | 4 |
| K16 | d1 (cm) | 5 |
| L16 | d2 (cm) | 20 |
| M16 | d3 (cm) | 25 |
| A18 | d (cm) | 11.4 |
| K19 | e1 (cm) | 1 |
| L19 | e2 (cm) | 0.635 |
| M19 | e3 (cm) | 0.818 |
| A21 | e (cm) | 0.36 |
| A24 | P (Kg) | 70 |
| A27 | V (Kg) | 80 |
| H44 | SI | 120 |
| B51 | Coef. Forma | 0.6 |
| C85 | b | 0.02 |
| C86 | CL | 0.2 |
| B143 | G (Kg/cm2) | 840000 |
| D146 | Altura de proyectores (cm) : | 530 |
| D147 | Ancho total de proyectores (cm) : | 110 |
| C284 | Número de pernos | 4 |

### Veredictos

- **D215** (cadena con #REF!) `=IF(#REF!<=#REF!,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
- **D216** (cadena con #REF!) `=IF(V192<=#REF!,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
  - V192 (Base tramo 2) = `=(S64+S65+C71)/T28` → 1.8120631633445508
- **D217** (cadena con #REF!) `=IF(V193<=#REF!,"OK! TRAMO No 3 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
  - V193 (Base tramo 3) = `=(S64+S65+S66+C71)/T32` → 1.126488574187319
- **D218** `=IF(B218<=B212,"OK! TRAMO CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO CUMPLE A LA COMPRESION
  - B218 (Base tramo) = `=0.75*(H75)/C33` → 6.55724579663731
  - B212 () = `=IF(C199<C196,(1/D209)*(1-0.5*(C199/C196)^2)*D12,(1/D209)*(3.14159^2*2100000/C199^2))` → 256.99280023633855
- **E229** `=IF(B226>844200/D12,"DISMINUIR D / t",IF(B218<=D229,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B226 (D / t) = `=A18/A21` → 31.666666666666668
  - B218 (Base tramo) = `=0.75*(H75)/C33` → 6.55724579663731
  - D229 (Fa (Kg/cm2) :) = `=IF(B226<=267330/D12,D12,IF(AND(267330/D12<=B226,B226<=844200/D12),0.75*D12+66832.5/B226))` → 2400
- **E230** `=IF(B226>844200/D12,"DISMINUIR D / t",IF(D242<=D230,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B226 (D / t) = `=A18/A21` → 31.666666666666668
  - D242 (Tensiones en la base tramo) = `=0.75*D97/E33` → 1280.240066464422
  - D230 (Fb (Kg/cm2) :) = `=IF(B226<=422100/D12,D12,IF(AND(422100/D12<=B226,B226<=844200/D12),0.7*D12+126630/B226))` → 2400
- **F239** (cadena con #REF!) `=IF(U226<=B238,"OK! SECCION CUMPLE","f < Fy: CAMBIAR SECCION")` → #REF!
  - U226 (Tensiones en la base del primer tramo) = `=S83/V27` → #REF!
  - B238 (Fm) = `=0.66*D12` → 1584
- **F240** (cadena con #REF!) `=IF(U227<=B238,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → #REF!
  - U227 (Tensiones en la base del segundo tramo) = `=S84/V28` → #REF!
  - B238 (Fm) = `=0.66*D12` → 1584
- **F241** (cadena con #REF!) `=IF(U228<=B238,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → #REF!
  - U228 (Tensiones en la base del tercer tramo) = `=S85/V32` → #REF!
  - B238 (Fm) = `=0.66*D12` → 1584
- **F242** `=IF(D242<=B238,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D242 (Tensiones en la base tramo) = `=0.75*D97/E33` → 1280.240066464422
  - B238 (Fm) = `=0.66*D12` → 1584
- **F255** `=IF(C255<=0.4*D12,"OK! SECCION CUMPLE"," CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - C255 (Tension de corte máxima:) = `=E250*(A18/2)/B144` → 0.0035519594423680943
- **F265** (cadena con #REF!) `=IF(M228>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M228 (Tramo 1) = `=U226/(B238)+((#REF!)/#REF!)` → #REF!
- **F266** (cadena con #REF!) `=IF(M229>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M229 (Tramo 2) = `=U227/(B238)+((V192)/#REF!)` → #REF!
- **F267** (cadena con #REF!) `=IF(M230>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M230 (Tramo 3) = `=U228/(B238)+((V193)/#REF!)` → #REF!
- **F268** `=IF(C268>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C268 (Tramo) = `=D242/(B238)+((B218)/B212)` → 0.8337476550781554
- **C290** `=IF(AND(C287>10.4,C287<=12.3),"1 3/4",IF(AND(C287>12.3,C287<=14.3),"1 7/8",IF(AND(C287>14.3,C287<=16.1),"2",IF(AND(C287>16.1,C287<=21),"2 1/4",IF(AND(C287>21,C287<=25.8),"2 1/2",IF(C287>25.8,"Aumente número de pernos"," "))))))` →  
  - C287 (Area de tracción) = `=C286/(0.6*D12)` → 1.8317175329082873
  - C287 (Area de tracción) = `=C286/(0.6*D12)` → 1.8317175329082873
  - C287 (Area de tracción) = `=C286/(0.6*D12)` → 1.8317175329082873
  - C287 (Area de tracción) = `=C286/(0.6*D12)` → 1.8317175329082873
  - C287 (Area de tracción) = `=C286/(0.6*D12)` → 1.8317175329082873
  - C287 (Area de tracción) = `=C286/(0.6*D12)` → 1.8317175329082873
  - C287 (Area de tracción) = `=C286/(0.6*D12)` → 1.8317175329082873
  - C287 (Area de tracción) = `=C286/(0.6*D12)` → 1.8317175329082873
  - C287 (Area de tracción) = `=C286/(0.6*D12)` → 1.8317175329082873
  - C287 (Area de tracción) = `=C286/(0.6*D12)` → 1.8317175329082873
  - C287 (Area de tracción) = `=C286/(0.6*D12)` → 1.8317175329082873

### Constantes escritas dentro de las fórmulas (valor: veces)

`2`: 147, `100`: 43, `4`: 41, `1`: 33, `3`: 27, `0.5`: 15, `3.14159`: 14, `6`: 14, `10000`: 5, `7850`: 4, `64`: 4, `0.6`: 4, `70`: 4, `32.595`: 4, `0.75`: 4, `844200`: 4, `3.91`: 4, `10.4`: 4, `126`: 3, `50`: 3, `0.2`: 3, `2100000`: 3, `0.3772`: 2, `16`: 2, `12`: 2, `5`: 2, `8`: 2, `267330`: 2, `422100`: 2, `0.21`: 2, `0.92`: 2, `1.46`: 2, `2.15`: 2, `2.98`: 2, `4.92`: 2, `6.25`: 2, `7.45`: 2, `9.06`: 2, `12.3`: 2, `14.3`: 2, `16.1`: 2, `21`: 2, `25.8`: 2, `120`: 1, `3.1415`: 1, `23`: 1, `66832.5`: 1, `0.7`: 1, `126630`: 1, `0.66`: 1, `0.4`: 1, `10`: 1

## P.Var.2 Tramos Circ.

Fórmulas: 177. Veredictos: 18 (0 con `#REF!` en su cadena). Fórmulas con `#REF!`: 0

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|
| D12 | Tension de Fluencia Fy (kg/cm2) | 2400 |
| S13 | h1 (m) | 0 |
| T13 | h2 (m) | 0 |
| A15 | h1 (m) | 1 |
| B15 | h2 (m) | 6 |
| S16 | d1 (cm) | 5 |
| T16 | d2 (cm) | 20 |
| A18 | d1 (cm) | 7.61 |
| B18 | d2 (cm) | 8.89 |
| S19 | e1 (cm) | 1 |
| T19 | e2 (cm) | 0.635 |
| A21 | e1 (cm) | 0.29 |
| B21 | e2 (cm) | 0.32 |
| B24 | P (Kg) | 20 |
| B27 | V (Kg) | 20 |
| H44 | SI | 120 |
| B50 | Coef. Forma | 0.6 |
| C85 | b | 0.02 |
| C86 | CL | 0.2 |
| K132 | E (kg/cm2) | 2100000 |
| B142 | G (Kg/cm2) | 840000 |
| D146 | Altura de proyectores (cm) : | 10 |
| D147 | Ancho total de proyectores (cm) : | 26 |
| E215 | FS | 1.67 |
| C300 | Número de pernos | 4 |

### Veredictos

- **D220** `=IF(S210<=B217,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 1 CUMPLE A LA COMPRESION
  - S210 (Base tramo 1) = `=(R72+C71)/S20` → 1.5910898965791567
  - B217 (Fa) = `=B216/C34/E215` → 57.66451825073785
- **D221** `=IF(S211<=B217,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 2 CUMPLE A LA COMPRESION
  - S211 (Base tramo 2) = `=(R72+R73+C71)/S21` → 0.5177323323841574
  - B217 (Fa) = `=B216/C34/E215` → 57.66451825073785
- **D222** `=IF(B222<=B217,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 1 CUMPLE A LA COMPRESION
  - B222 (Base tramo 1) = `=0.75*(R72+R73+B76+C71)/C33` → 2.83808095952024
  - B217 (Fa) = `=B216/C34/E215` → 57.66451825073785
- **D223** `=IF(B223<=B217,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 2 CUMPLE A LA COMPRESION
  - B223 (Base tramo 2) = `=0.75*(H75)/C34` → 5.730278422273782
  - B217 (Fa) = `=B216/C34/E215` → 57.66451825073785
- **E232** `=IF(B232>844200/D12,"DISMINUIR D / t",IF(B222<=C232,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B232 (Tramo 1) = `=A18/A21` → 26.24137931034483
  - B222 (Base tramo 1) = `=0.75*(R72+R73+B76+C71)/C33` → 2.83808095952024
  - C232 (Tramo 1) = `=IF(B232<=267330/D12,D12,IF(AND(267330/D12<=B232,B232<=844200/D12),0.75*D12+66832.5/B232))` → 2400
- **E233** `=IF(B233>844200/D12,"DISMINUIR D / t",IF(B223<=C233,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B233 (Tramo 2) = `=B18/B21` → 27.78125
  - B223 (Base tramo 2) = `=0.75*(H75)/C34` → 5.730278422273782
  - C233 (Tramo 2) = `=IF(B233<=267330/D12,D12,IF(AND(267330/D12<=B233,B233<=844200/D12),0.75*D12+66832.5/B233))` → 2400
- **E237** `=IF(B237>844200/D12,"DISMINUIR D / t",IF(D251<=C237,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B237 (Tramo 1) = `=A18/A21` → 26.24137931034483
  - D251 (Tensiones en la base del primer tramo) = `=0.75*D96/E33` → 147.0873135186751
  - C237 (Tramo 1) = `=IF(B237<=422100/D12,D12,IF(AND(422100/D12<=B237,B237<=844200/D12),0.7*D12+126630/B237))` → 2400
- **E238** `=IF(B238>844200/D12,"DISMINUIR D / t",IF(D252<=C238,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B238 (Tramo 2) = `=B18/B21` → 27.78125
  - D252 (Tensiones en la base del segundo tramo) = `=0.75*D97/E34` → 1040.6593083392952
  - C238 (Tramo 2) = `=IF(B238<=422100/D12,D12,IF(AND(422100/D12<=B238,B238<=844200/D12),0.7*D12+126630/B238))` → 2400
- **F249** `=IF(U230<=B248,"OK! SECCION CUMPLE","f < Fy: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - U230 (Tensiones en la base del primer tramo) = `=T95/U20` → 96.28980463933296
  - B248 (Fm) = `=0.66*D12` → 1584
- **F250** `=IF(U231<=B248,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - U231 (Tensiones en la base del segundo tramo) = `=T96/U21` → 5.566304572652692
  - B248 (Fm) = `=0.66*D12` → 1584
- **F251** `=IF(D251<=B248,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D251 (Tensiones en la base del primer tramo) = `=0.75*D96/E33` → 147.0873135186751
  - B248 (Fm) = `=0.66*D12` → 1584
- **F252** `=IF(D252<=B248,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D252 (Tensiones en la base del segundo tramo) = `=0.75*D97/E34` → 1040.6593083392952
  - B248 (Fm) = `=0.66*D12` → 1584
- **F264** `=IF(C264<=0.4*D12,"OK! SECCION CUMPLE"," CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - C264 (Tension de corte máxima:) = `=E259*(B18/2)/B144` → 5.7971984900119154e-05
- **F271** `=IF(S243>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - S243 (Tramo 1) = `=U230/(B248)+((S210)/B217)` → 0.08838120032425402
- **F272** `=IF(S244>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - S244 (Tramo 2) = `=U231/(B248)+((S211)/B217)` → 0.012492432989573138
- **F273** `=IF(C273>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C273 (Tramo 1) = `=D251/(B248)+((B222)/B217)` → 0.14207526284982103
- **F274** `=IF(C274>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C274 (Tramo 2) = `=D252/(B248)+((B223)/B217)` → 0.7563545787653853
- **C306** `=IF(AND(C303>10.4,C303<=12.3),"1 3/4",IF(AND(C303>12.3,C303<=14.3),"1 7/8",IF(AND(C303>14.3,C303<=16.1),"2",IF(AND(C303>16.1,C303<=21),"2 1/4",IF(AND(C303>21,C303<=25.8),"2 1/2",IF(C303>25.8,"Aumente número de pernos"," "))))))` →  
  - C303 (Area de tracción) = `=C302/(0.6*D12)` → 0.897559015504296
  - C303 (Area de tracción) = `=C302/(0.6*D12)` → 0.897559015504296
  - C303 (Area de tracción) = `=C302/(0.6*D12)` → 0.897559015504296
  - C303 (Area de tracción) = `=C302/(0.6*D12)` → 0.897559015504296
  - C303 (Area de tracción) = `=C302/(0.6*D12)` → 0.897559015504296
  - C303 (Area de tracción) = `=C302/(0.6*D12)` → 0.897559015504296
  - C303 (Area de tracción) = `=C302/(0.6*D12)` → 0.897559015504296
  - C303 (Area de tracción) = `=C302/(0.6*D12)` → 0.897559015504296
  - C303 (Area de tracción) = `=C302/(0.6*D12)` → 0.897559015504296
  - C303 (Area de tracción) = `=C302/(0.6*D12)` → 0.897559015504296
  - C303 (Area de tracción) = `=C302/(0.6*D12)` → 0.897559015504296

### Constantes escritas dentro de las fórmulas (valor: veces)

`2`: 177, `4`: 59, `100`: 57, `1`: 31, `3`: 27, `6`: 24, `0.5`: 14, `3.14159`: 13, `32.595`: 8, `844200`: 8, `0.75`: 7, `70`: 6, `0.3772`: 6, `12`: 6, `10000`: 5, `64`: 5, `7850`: 4, `267330`: 4, `422100`: 4, `3.91`: 4, `10.4`: 4, `0.6`: 3, `50`: 3, `126`: 2, `0.2`: 2, `16`: 2, `66832.5`: 2, `0.7`: 2, `126630`: 2, `0.21`: 2, `0.92`: 2, `1.46`: 2, `2.15`: 2, `2.98`: 2, `4.92`: 2, `6.25`: 2, `7.45`: 2, `9.06`: 2, `12.3`: 2, `14.3`: 2, `16.1`: 2, `21`: 2, `25.8`: 2, `120`: 1, `3.1415`: 1, `980`: 1, `2.467`: 1, `2100000`: 1, `0.66`: 1, `0.4`: 1, `10`: 1, `5`: 1

## P.Var.3 Tramos Circ.

Fórmulas: 193. Veredictos: 20 (0 con `#REF!` en su cadena). Fórmulas con `#REF!`: 0

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|
| D12 | Tension de Fluencia Fy (kg/cm2) | 2400 |
| Y12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| A15 | h1 (m) | 1.5 |
| B15 | h2 (m) | 6 |
| C15 | h3 (m) | 6 |
| Y15 | d1 (cm) | 5 |
| A18 | d1 (cm) | 32.3 |
| B18 | d2 (cm) | 27.305 |
| C18 | d3 (cm) | 32.3 |
| Y18 | e1 (cm) | 1 |
| A21 | e1 (cm) | 0.635 |
| B21 | e2 (cm) | 0.5 |
| C21 | e3 (cm) | 0.635 |
| C24 | P (Kg) | 250 |
| C27 | V (Kg) | 120 |
| H44 | SI | 120 |
| B51 | Coef. Forma | 0.6 |
| C85 | b | 0.02 |
| C86 | CL | 0.2 |
| N131 | Largo (cm) | 0 |
| Q131 | Largo (cm) | 0 |
| K132 | E (kg/cm2) | 2100000 |
| L133 | Peso (kg) | 0 |
| O133 | Peso (kg) | 0 |
| N134 | La frecuencia queda determinada por: | 0 |
| Q134 | La frecuencia queda determinada por: | 0 |
| L136 |  | 0 |
| O136 |  | 0 |
| B142 | G (Kg/cm2) | 840000 |
| D146 | Altura de proyectores (cm) : | 150 |
| D147 | Ancho total de proyectores (cm) : | 200 |
| E215 | FS | 1.67 |
| C295 | Número de pernos | 6 |

### Veredictos

- **D220** `=IF(V203<=B217,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 1 CUMPLE A LA COMPRESION
  - V203 (Base tramo 1) = `=(W67+C71)/V33` → 19.888623707239457
  - B217 (Fa) = `=B216/C35/E215` → 186.30584445627073
- **D221** `=IF(B221<=B217,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 1 CUMPLE A LA COMPRESION
  - B221 (Base tramo 1) = `=0.75*(W67+B75+C71)/C33` → 3.851333702706981
  - B217 (Fa) = `=B216/C35/E215` → 186.30584445627073
- **D222** `=IF(B222<=B217,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 2 CUMPLE A LA COMPRESION
  - B222 (Base tramo 2) = `=0.75*(W67+B75+B76+C71)/C34` → 9.310347898361435
  - B217 (Fa) = `=B216/C35/E215` → 186.30584445627073
- **D223** `=IF(B223<=B217,"OK! TRAMO No 3 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 3 CUMPLE A LA COMPRESION
  - B223 (Base tramo 3) = `=0.75*(H75)/C35` → 9.739017729935098
  - B217 (Fa) = `=B216/C35/E215` → 186.30584445627073
- **E231** `=IF(B231>844200/D12,"DISMINUIR D / t",IF(B221<=C231,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B231 (Tramo 1) = `=A18/A21` → 50.86614173228346
  - B221 (Base tramo 1) = `=0.75*(W67+B75+C71)/C33` → 3.851333702706981
  - C231 (Tramo 1) = `=IF(B231<=267330/D12,D12,IF(AND(267330/D12<=B231,B231<=844200/D12),0.75*D12+66832.5/B231))` → 2400
- **E232** `=IF(B232>844200/D12,"DISMINUIR D / t",IF(B222<=C232,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B232 (Tramo 2) = `=B18/B21` → 54.61
  - B222 (Base tramo 2) = `=0.75*(W67+B75+B76+C71)/C34` → 9.310347898361435
  - C232 (Tramo 2) = `=IF(B232<=267330/D12,D12,IF(AND(267330/D12<=B232,B232<=844200/D12),0.75*D12+66832.5/B232))` → 2400
- **E233** `=IF(B233>844200/D12,"DISMINUIR D / t",IF(B223<=C233,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B233 (Tramo 3) = `=C18/C21` → 50.86614173228346
  - B223 (Base tramo 3) = `=0.75*(H75)/C35` → 9.739017729935098
  - C233 (Tramo 3) = `=IF(B233<=267330/D12,D12,IF(AND(267330/D12<=B233,B233<=844200/D12),0.75*D12+66832.5/B233))` → 2400
- **E237** `=IF(B237>844200/D12,"DISMINUIR D / t",IF(D252<=C237,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B237 (Tramo 1) = `=A18/A21` → 50.86614173228346
  - D252 (Tensiones en la base del primer tramo) = `=0.75*D97/E33` → 45.02933407348892
  - C237 (Tramo 1) = `=IF(B237<=422100/D12,D12,IF(AND(422100/D12<=B237,B237<=844200/D12),0.7*D12+126630/B237))` → 2400
- **E238** `=IF(B238>844200/D12,"DISMINUIR D / t",IF(D253<=C238,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B238 (Tramo 2) = `=B18/B21` → 54.61
  - D253 (Tensiones en la base del segundo tramo) = `=0.75*D98/E34` → 434.04793968547665
  - C238 (Tramo 2) = `=IF(B238<=422100/D12,D12,IF(AND(422100/D12<=B238,B238<=844200/D12),0.7*D12+126630/B238))` → 2400
- **E239** `=IF(B239>844200/D12,"DISMINUIR D / t",IF(D254<=C239,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B239 (Tramo 3) = `=C18/C21` → 50.86614173228346
  - D254 (Tensiones en la base del tercer tramo) = `=0.75*D99/E35` → 501.8428441441211
  - C239 (Tramo 3) = `=IF(B239<=422100/D12,D12,IF(AND(422100/D12<=B239,B239<=844200/D12),0.7*D12+126630/B239))` → 2400
- **F251** `=IF(U222<=B249,"OK! SECCION CUMPLE","f < Fy: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - U222 (Tensiones en la base del primer tramo) = `=X87/X33` → 628.9385454198746
  - B249 (Fm) = `=0.66*D12` → 1584
- **F252** `=IF(D252<=B249,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D252 (Tensiones en la base del primer tramo) = `=0.75*D97/E33` → 45.02933407348892
  - B249 (Fm) = `=0.66*D12` → 1584
- **F253** `=IF(D253<=B249,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D253 (Tensiones en la base del segundo tramo) = `=0.75*D98/E34` → 434.04793968547665
  - B249 (Fm) = `=0.66*D12` → 1584
- **F254** `=IF(D254<=B249,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D254 (Tensiones en la base del tercer tramo) = `=0.75*D99/E35` → 501.8428441441211
  - B249 (Fm) = `=0.66*D12` → 1584
- **F266** `=IF(C266<=0.4*D12,"OK! SECCION CUMPLE"," CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - C266 (Tension de corte máxima:) = `=E261*(C18/2)/C144` → 0.0013767275983117711
- **F272** `=IF(I241>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - I241 () = `=U222/(B249)+((V203)/B217)` → 0.5038097110720618
- **F273** `=IF(C273>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C273 (Tramo 1) = `=D252/(B249)+(B221/B217)` → 0.04909971341340831
- **F274** `=IF(C274>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C274 (Tramo 2) = `=D253/(B249)+(B222)/B217` → 0.323993625191657
- **F275** `=IF(C275>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C275 (Tramo 3) = `=D254/(B249)+(B223)/B217` → 0.36909433171023476
- **C301** `=IF(AND(C298>10.4,C298<=12.3),"1 3/4",IF(AND(C298>12.3,C298<=14.3),"1 7/8",IF(AND(C298>14.3,C298<=16.1),"2",IF(AND(C298>16.1,C298<=21),"2 1/4",IF(AND(C298>21,C298<=25.8),"2 1/2",IF(C298>25.8,"Aumente número de pernos"," "))))))` →  
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 3.496671345873848
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 3.496671345873848
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 3.496671345873848
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 3.496671345873848
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 3.496671345873848
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 3.496671345873848
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 3.496671345873848
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 3.496671345873848
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 3.496671345873848
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 3.496671345873848
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 3.496671345873848

### Constantes escritas dentro de las fórmulas (valor: veces)

`2`: 160, `4`: 74, `100`: 52, `1`: 30, `6`: 19, `3`: 18, `0.5`: 15, `3.14159`: 12, `32.595`: 12, `844200`: 12, `0.3772`: 10, `12`: 10, `0.75`: 10, `70`: 8, `267330`: 6, `422100`: 6, `10000`: 5, `64`: 5, `7850`: 4, `3.91`: 4, `10.4`: 4, `66832.5`: 3, `0.7`: 3, `126630`: 3, `0.6`: 2, `0.2`: 2, `16`: 2, `0.21`: 2, `0.92`: 2, `1.46`: 2, `2.15`: 2, `2.98`: 2, `4.92`: 2, `6.25`: 2, `7.45`: 2, `9.06`: 2, `12.3`: 2, `14.3`: 2, `16.1`: 2, `21`: 2, `25.8`: 2, `126`: 1, `120`: 1, `50`: 1, `3.1415`: 1, `980`: 1, `2.467`: 1, `2100000`: 1, `0.66`: 1, `0.4`: 1, `10`: 1, `5`: 1

## P.Var.4 Tramos Circ.

Fórmulas: 212. Veredictos: 22 (0 con `#REF!` en su cadena). Fórmulas con `#REF!`: 0

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|
| D12 | Tension de Fluencia Fy (kg/cm2) | 2400 |
| A15 | h1 (m) | 2.7 |
| B15 | h2 (m) | 3.3 |
| C15 | h3 (m) | 6 |
| D15 | h4 (m) | 6 |
| A18 | d1 (cm) | 11.43 |
| B18 | d2 (cm) | 14.13 |
| C18 | d3 (cm) | 16.827 |
| D18 | d4 (cm) | 21.9 |
| A21 | e1 (cm) | 0.36 |
| B21 | e2 (cm) | 0.5 |
| C21 | e3 (cm) | 0.5 |
| D21 | e4 (cm) | 0.478 |
| D24 | P (Kg) | 25 |
| D27 | V (Kg) | 50 |
| H44 | SI | 120 |
| B52 | Coef. Forma | 0.6 |
| C86 | b | 0.02 |
| C87 | CL | 0.2 |
| N132 | Inercia (cm4) | 0 |
| O132 | Inercia (cm4) | 0 |
| R132 | Inercia (cm4) | 0 |
| S132 | Inercia (cm4) | 0 |
| O133 | Largo (cm) | 0 |
| S133 | Largo (cm) | 0 |
| K134 | E (kg/cm2) | 2100000 |
| L134 | E (kg/cm2) | 0 |
| P134 | E (kg/cm2) | 0 |
| L135 | Peso (kg) | 0 |
| M135 | Peso (kg) | 0 |
| P135 | Peso (kg) | 0 |
| Q135 | Peso (kg) | 0 |
| N136 |  | 0 |
| O136 |  | 0 |
| R136 |  | 0 |
| S136 |  | 0 |
| O137 |  | 0 |
| S137 |  | 0 |
| L138 | ciclos/s | 0 |
| P138 | ciclos/s | 0 |
| L139 | Matriz de Rigidez | 0 |
| M139 | Matriz de Rigidez | 0 |
| P139 | Matriz de Rigidez | 0 |
| Q139 | Matriz de Rigidez | 0 |
| B143 | G (Kg/cm2) | 840000 |
| D147 | Altura de proyectores (cm) : | 15 |
| D148 | Ancho total de proyectores (cm) : | 5 |
| E216 | FS | 1.67 |
| C297 | Número de pernos | 4 |

### Veredictos

- **D221** `=IF(B221<=B218,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 1 CUMPLE A LA COMPRESION
  - B221 (Base tramo 1) = `=0.75*(B75+C72)/C33` → 3.0875199680511183
  - B218 (Fa) = `=B217/C36/E216` → 41.81920643922529
- **D222** `=IF(B222<=B218,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 2 CUMPLE A LA COMPRESION
  - B222 (Base tramo 2) = `=0.75*(B75+B76+C72)/C34` → 3.7487389070527786
  - B218 (Fa) = `=B217/C36/E216` → 41.81920643922529
- **D223** `=IF(B223<=B218,"OK! TRAMO No 3 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 3 CUMPLE A LA COMPRESION
  - B223 (Base tramo 3) = `=0.75*(B75+B76+B77+C72)/C35` → 6.662397660818713
  - B218 (Fa) = `=B217/C36/E216` → 41.81920643922529
- **D224** `=IF(B224<=B218,"OK! TRAMO No 4 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 4 CUMPLE A LA COMPRESION
  - B224 (Base tramo 4) = `=0.75*(H76)/C36` → 8.844124961143923
  - B218 (Fa) = `=B217/C36/E216` → 41.81920643922529
- **E233** `=IF(B233>844200/D12,"DISMINUIR D / t",IF(B221<=C233,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B233 (Tramo 1) = `=A18/A21` → 31.75
  - B221 (Base tramo 1) = `=0.75*(B75+C72)/C33` → 3.0875199680511183
  - C233 (Tramo 1) = `=IF(B233<=267330/D12,D12,IF(AND(267330/D12<=B233,B233<=844200/D12),0.75*D12+66832.5/B233))` → 2400
- **E234** `=IF(B234>844200/D12,"DISMINUIR D / t",IF(B222<=C234,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B234 (Tramo 2) = `=B18/B21` → 28.26
  - B222 (Base tramo 2) = `=0.75*(B75+B76+C72)/C34` → 3.7487389070527786
  - C234 (Tramo 2) = `=IF(B234<=267330/D12,D12,IF(AND(267330/D12<=B234,B234<=844200/D12),0.75*D12+66832.5/B234))` → 2400
- **E235** `=IF(B235>844200/D12,"DISMINUIR D / t",IF(B223<=C235,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B235 (Tramo 3) = `=C18/C21` → 33.654
  - B223 (Base tramo 3) = `=0.75*(B75+B76+B77+C72)/C35` → 6.662397660818713
  - C235 (Tramo 3) = `=IF(B235<=267330/D12,D12,IF(AND(267330/D12<=B235,B235<=844200/D12),0.75*D12+66832.5/B235))` → 2400
- **E236** `=IF(B236>844200/D12,"DISMINUIR D / t",IF(B224<=C236,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B236 (Tramo 4) = `=D18/D21` → 45.81589958158996
  - B224 (Base tramo 4) = `=0.75*(H76)/C36` → 8.844124961143923
  - C236 (Tramo 4) = `=IF(B236<=267330/D12,D12,IF(AND(267330/D12<=B236,B236<=844200/D12),0.75*D12+66832.5/B236))` → 2400
- **E240** `=IF(B240>844200/D12,"DISMINUIR D / t",IF(D256<=C240,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B240 (Tramo 1) = `=A18/A21` → 31.75
  - D256 (Tensiones en la base del primer tramo) = `=0.75*D97/E33` → 377.38152637184504
  - C240 (Tramo 1) = `=IF(B240<=422100/D12,D12,IF(AND(422100/D12<=B240,B240<=844200/D12),0.7*D12+126630/B240))` → 2400
- **E241** `=IF(B241>844200/D12,"DISMINUIR D / t",IF(D257<=C241,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B241 (Tramo 2) = `=B18/B21` → 28.26
  - D257 (Tensiones en la base del segundo tramo) = `=0.75*D98/E34` → 490.179115002492
  - C241 (Tramo 2) = `=IF(B241<=422100/D12,D12,IF(AND(422100/D12<=B241,B241<=844200/D12),0.7*D12+126630/B241))` → 2400
- **E242** `=IF(B242>844200/D12,"DISMINUIR D / t",IF(D258<=C242,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B242 (Tramo 3) = `=C18/C21` → 33.654
  - D258 (Tensiones en la base del tercer tramo) = `=0.75*D99/E35` → 938.8690947163277
  - C242 (Tramo 3) = `=IF(B242<=422100/D12,D12,IF(AND(422100/D12<=B242,B242<=844200/D12),0.7*D12+126630/B242))` → 2400
- **E243** `=IF(B243>844200/D12,"DISMINUIR D / t",IF(D259<=C243,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B243 (Tramo 4) = `=D18/D21` → 45.81589958158996
  - D259 (Tensiones en la base del cuarto tramo) = `=0.75*D100/E36` → 1085.198368921775
  - C243 (Tramo 4) = `=IF(B243<=422100/D12,D12,IF(AND(422100/D12<=B243,B243<=844200/D12),0.7*D12+126630/B243))` → 2400
- **F256** `=IF(D256<=B254,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D256 (Tensiones en la base del primer tramo) = `=0.75*D97/E33` → 377.38152637184504
  - B254 (Fm) = `=0.66*D12` → 1584
- **F257** `=IF(D257<=B254,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D257 (Tensiones en la base del segundo tramo) = `=0.75*D98/E34` → 490.179115002492
  - B254 (Fm) = `=0.66*D12` → 1584
- **F258** `=IF(D258<=B254,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D258 (Tensiones en la base del tercer tramo) = `=0.75*D99/E35` → 938.8690947163277
  - B254 (Fm) = `=0.66*D12` → 1584
- **F259** `=IF(D259<=B254,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D259 (Tensiones en la base del cuarto tramo) = `=0.75*D100/E36` → 1085.198368921775
  - B254 (Fm) = `=0.66*D12` → 1584
- **F271** `=IF(C271<=0.4*D12,"OK! SECCION CUMPLE"," CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - C271 (Tension de corte máxima:) = `=E266*(D18/2)/D145` → 0.00020564395472116298
- **F278** `=IF(C278>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C278 (Tramo 1) = `=D256/(B254)+(B221)/B218` → 0.3120761033764295
- **F279** `=IF(C279>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C279 (Tramo 2) = `=D257/(B254)+(B222)/B218` → 0.39909807208926906
- **F280** `=IF(C280>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C280 (Tramo 3) = `=D258/(B254)+B223/B218` → 0.7520346895227553
- **F281** `=IF(C281>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C281 (Tramo 4) = `=D259/(B254)+(B224)/B218` → 0.8965847433439511
- **C303** `=IF(AND(C300>10.4,C300<=12.3),"1 3/4",IF(AND(C300>12.3,C300<=14.3),"1 7/8",IF(AND(C300>14.3,C300<=16.1),"2",IF(AND(C300>16.1,C300<=21),"2 1/4",IF(AND(C300>21,C300<=25.8),"2 1/2",IF(C300>25.8,"Aumente número de pernos"," "))))))` →  
  - C300 (Area de tracción) = `=C299/(0.6*D12)` → 5.24484598536257
  - C300 (Area de tracción) = `=C299/(0.6*D12)` → 5.24484598536257
  - C300 (Area de tracción) = `=C299/(0.6*D12)` → 5.24484598536257
  - C300 (Area de tracción) = `=C299/(0.6*D12)` → 5.24484598536257
  - C300 (Area de tracción) = `=C299/(0.6*D12)` → 5.24484598536257
  - C300 (Area de tracción) = `=C299/(0.6*D12)` → 5.24484598536257
  - C300 (Area de tracción) = `=C299/(0.6*D12)` → 5.24484598536257
  - C300 (Area de tracción) = `=C299/(0.6*D12)` → 5.24484598536257
  - C300 (Area de tracción) = `=C299/(0.6*D12)` → 5.24484598536257
  - C300 (Area de tracción) = `=C299/(0.6*D12)` → 5.24484598536257
  - C300 (Area de tracción) = `=C299/(0.6*D12)` → 5.24484598536257

### Constantes escritas dentro de las fórmulas (valor: veces)

`2`: 186, `4`: 89, `100`: 58, `6`: 27, `1`: 25, `3`: 20, `0.5`: 16, `32.595`: 16, `844200`: 16, `0.3772`: 14, `12`: 14, `0.75`: 13, `3.14159`: 11, `70`: 10, `267330`: 8, `422100`: 8, `10000`: 5, `64`: 5, `7850`: 4, `66832.5`: 4, `0.7`: 4, `126630`: 4, `3.91`: 4, `10.4`: 4, `200`: 3, `0.2`: 2, `16`: 2, `0.21`: 2, `0.92`: 2, `1.46`: 2, `2.15`: 2, `2.98`: 2, `4.92`: 2, `6.25`: 2, `7.45`: 2, `9.06`: 2, `12.3`: 2, `14.3`: 2, `16.1`: 2, `21`: 2, `25.8`: 2, `120`: 1, `3.1415`: 1, `980`: 1, `2.467`: 1, `2100000`: 1, `0.66`: 1, `0.4`: 1, `10`: 1, `0.6`: 1, `5`: 1

## P.Recto Circ. 1 gancho

Fórmulas: 151. Veredictos: 16 (8 con `#REF!` en su cadena). Fórmulas con `#REF!`: 8 (S83, S84, S85, D215, D216, M228, M229, M230)

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|
| D12 | Tension de Fluencia Fy (kg/cm2) | 2400 |
| S12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| T12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| U12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| A15 | h (m) | 5.89 |
| D15 | d (cm) | 88.9 |
| K16 | d1 (cm) | 5 |
| L16 | d2 (cm) | 20 |
| M16 | d3 (cm) | 25 |
| A18 | d (cm) | 114.3 |
| D18 | e (cm) | 4 |
| K19 | e1 (cm) | 1 |
| L19 | e2 (cm) | 0.635 |
| M19 | e3 (cm) | 0.818 |
| A21 | e (cm) | 3.05 |
| D21 | R (cm) | 150 |
| A24 | P (Kg) | 15 |
| D24 | Dist (cm) | 400 |
| A27 | V (Kg) | 0 |
| D27 | t (cm) | 3.5 |
| H44 | SI | 150 |
| B51 | Coef. Forma | 0.6 |
| C85 | b | 0.02 |
| C86 | CL | 0.2 |
| B143 | G (Kg/cm2) | 840000 |
| D242 | Tensiones en la base del gancho | 0 |
| C281 | Número de pernos | 6 |

### Veredictos

- **D215** (cadena con #REF!) `=IF(#REF!<=#REF!,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
- **D216** (cadena con #REF!) `=IF(V192<=#REF!,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
  - V192 (Base tramo 2) = `=(S64+S65+C71)/T28` → 0.38829924928811804
- **D218** `=IF(B218<=B212,"OK! TRAMO CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO CUMPLE A LA COMPRESION
  - B218 (Base tramo) = `=0.75*(H75)/C33` → 4.879862694431355
  - B212 () = `=IF(C199<C196,(1/D209)*(1-0.5*(C199/C196)^2)*D12,(1/D209)*(3.14159^2*2100000/C199^2))` → 1335.3792020294986
- **E229** `=IF(B226>844200/D12,"DISMINUIR D / t",IF(B218<=D229,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B226 (D / t) = `=A18/A21` → 37.47540983606557
  - B218 (Base tramo) = `=0.75*(H75)/C33` → 4.879862694431355
  - D229 (Fa (Kg/cm2) :) = `=IF(B226<=267330/D12,D12,IF(AND(267330/D12<=B226,B226<=844200/D12),0.75*D12+66832.5/B226))` → 2400
- **E230** `=IF(B226>844200/D12,"DISMINUIR D / t",IF(D241<=D230,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B226 (D / t) = `=A18/A21` → 37.47540983606557
  - D241 (Tensiones en la base tramo) = `=0.75*D97/E33` → 99.86944623579093
  - D230 (Fb (Kg/cm2) :) = `=IF(B226<=422100/D12,D12,IF(AND(422100/D12<=B226,B226<=844200/D12),0.7*D12+126630/B226))` → 2400
- **F238** (cadena con #REF!) `=IF(U226<=B237,"OK! SECCION CUMPLE","f < Fy: CAMBIAR SECCION")` → #REF!
  - U226 (Tensiones en la base del primer tramo) = `=S83/V27` → #REF!
  - B237 (Fm) = `=0.66*D12` → 1584
- **F239** (cadena con #REF!) `=IF(U227<=B237,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → #REF!
  - U227 (Tensiones en la base del segundo tramo) = `=S84/V28` → #REF!
  - B237 (Fm) = `=0.66*D12` → 1584
- **F240** (cadena con #REF!) `=IF(U228<=B237,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → #REF!
  - U228 (Tensiones en la base del tercer tramo) = `=S85/V32` → #REF!
  - B237 (Fm) = `=0.66*D12` → 1584
- **F241** `=IF(D241<=B237,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D241 (Tensiones en la base tramo) = `=0.75*D97/E33` → 99.86944623579093
  - B237 (Fm) = `=0.66*D12` → 1584
- **F242** `=IF(D242<=B237,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - B237 (Fm) = `=0.66*D12` → 1584
- **F253** `=IF(C253<=0.4*D12,"OK! SECCION CUMPLE"," CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - C253 (Tension de corte máxima:) = `=(E248+E247)*(A18/2)/B144` → 0.12294975082347873
- **F261** (cadena con #REF!) `=IF(M228>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M228 (Tramo 1) = `=U226/(B237)+((#REF!)/#REF!)` → #REF!
- **F262** (cadena con #REF!) `=IF(M229>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M229 (Tramo 2) = `=U227/(B237)+((V192)/#REF!)` → #REF!
- **F263** (cadena con #REF!) `=IF(M230>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M230 (Tramo 3) = `=U228/(B237)+((V193)/#REF!)` → #REF!
- **F264** `=IF(C264>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C264 (Tramo) = `=D241/(B237)+B218/B212` → 0.06670318269850588
- **C287** `=IF(AND(C284>10.4,C284<=12.3),"1 3/4",IF(AND(C284>12.3,C284<=14.3),"1 7/8",IF(AND(C284>14.3,C284<=16.1),"2",IF(AND(C284>16.1,C284<=21),"2 1/4",IF(AND(C284>21,C284<=25.8),"2 1/2",IF(C284>25.8,"Aumente número de pernos"," "))))))` → 1 7/8
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 13.519654721852918
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 13.519654721852918
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 13.519654721852918
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 13.519654721852918
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 13.519654721852918
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 13.519654721852918
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 13.519654721852918
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 13.519654721852918
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 13.519654721852918
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 13.519654721852918
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 13.519654721852918

### Constantes escritas dentro de las fórmulas (valor: veces)

`2`: 167, `100`: 53, `4`: 51, `1`: 32, `3`: 27, `0.5`: 16, `3.14159`: 15, `6`: 14, `3.1415`: 11, `32.595`: 6, `10000`: 5, `64`: 5, `0.6`: 5, `7850`: 4, `70`: 4, `0.37`: 4, `0.75`: 4, `844200`: 4, `3.91`: 4, `10.4`: 4, `126`: 3, `1.57`: 3, `0.00785`: 3, `50`: 3, `0.2`: 3, `2100000`: 3, `0.3772`: 2, `28.594`: 2, `16`: 2, `5`: 2, `8`: 2, `267330`: 2, `422100`: 2, `0.21`: 2, `0.92`: 2, `1.46`: 2, `2.15`: 2, `2.98`: 2, `4.92`: 2, `6.25`: 2, `7.45`: 2, `9.06`: 2, `12.3`: 2, `14.3`: 2, `16.1`: 2, `21`: 2, `25.8`: 2, `120`: 1, `0.63`: 1, `0.356`: 1, `23`: 1, `12`: 1, `66832.5`: 1, `0.7`: 1, `126630`: 1, `0.66`: 1, `0.4`: 1, `10`: 1

## P.Var. 2 Tramos Circ. 1 gancho

Fórmulas: 184. Veredictos: 19 (0 con `#REF!` en su cadena). Fórmulas con `#REF!`: 0

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|
| D12 | Tension de Fluencia Fy (kg/cm2) | 2400 |
| S13 | h1 (m) | 0 |
| T13 | h2 (m) | 0 |
| A15 | h1 (m) | 1.8 |
| B15 | h2 (m) | 6 |
| S16 | Diámetro del gancho | 5 |
| T16 | Diámetro del gancho | 20 |
| A18 | d1 (cm) | 14.13 |
| B18 | d2 (cm) | 127 |
| D18 | d (cm) | 11.4 |
| S19 | Espesor del gancho | 1 |
| T19 | Espesor del gancho | 0.635 |
| A21 | e1 (cm) | 6.35 |
| B21 | e2 (cm) | 4 |
| D21 | e (cm) | 4 |
| A24 | P (Kg) | 100 |
| D24 | R (cm) | 150 |
| E24 | t (cm) | 3.5 |
| A27 | V (Kg) | 0 |
| D27 | Dist (cm) | 400 |
| H44 | si | 120 |
| B51 | Coef. Forma | 0.6 |
| C86 | b | 0.02 |
| C87 | CL | 0.2 |
| J128 | E (kg/cm2) | 2100000 |
| B143 | G (Kg/cm2) | 840000 |
| E216 | FS | 1.67 |
| D254 | Tensiones en la base del gancho | 0 |
| C290 | Número de pernos | 6 |

### Veredictos

- **D221** `=IF(S210<=B218,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 1 CUMPLE A LA COMPRESION
  - S210 (Base tramo 1) = `=(R72+C72)/S20` → 7.955449482895784
  - B218 (Fa) = `=B217/C34/E216` → 9165.245104007534
- **D222** `=IF(S211<=B218,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 2 CUMPLE A LA COMPRESION
  - S211 (Base tramo 2) = `=(R72+R73+C72)/S21` → 2.5886616619207867
  - B218 (Fa) = `=B217/C34/E216` → 9165.245104007534
- **D223** `=IF(B223<=B218,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 1 CUMPLE A LA COMPRESION
  - B223 (Base tramo 1) = `=0.75*(R72+R73+B77+C72)/C33` → 1.5429800257731958
  - B218 (Fa) = `=B217/C34/E216` → 9165.245104007534
- **D224** `=IF(B224<=B218,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 2 CUMPLE A LA COMPRESION
  - B224 (Base tramo 2) = `=0.75*(H76)/C34` → 3.780036856396357
  - B218 (Fa) = `=B217/C34/E216` → 9165.245104007534
- **E233** `=IF(B233>844200/D12,"DISMINUIR D / t",IF(B223<=C233,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B233 (Tramo 1) = `=A18/A21` → 2.225196850393701
  - B223 (Base tramo 1) = `=0.75*(R72+R73+B77+C72)/C33` → 1.5429800257731958
  - C233 (Tramo 1) = `=IF(B233<=267330/D12,D12,IF(AND(267330/D12<=B233,B233<=844200/D12),0.75*D12+66832.5/B233))` → 2400
- **E234** `=IF(B234>844200/D12,"DISMINUIR D / t",IF(B224<=C234,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B234 (Tramo 2) = `=B18/B21` → 31.75
  - B224 (Base tramo 2) = `=0.75*(H76)/C34` → 3.780036856396357
  - C234 (Tramo 2) = `=IF(B234<=267330/D12,D12,IF(AND(267330/D12<=B234,B234<=844200/D12),0.75*D12+66832.5/B234))` → 2400
- **E238** `=IF(B238>844200/D12,"DISMINUIR D / t",IF(D252<=C238,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B238 (Tramo 1) = `=A18/A21` → 2.225196850393701
  - D252 (Tensiones en la base del primer tramo) = `=0.75*D97/E33` → 194.15854053660834
  - C238 (Tramo 1) = `=IF(B238<=422100/D12,D12,IF(AND(422100/D12<=B238,B238<=844200/D12),0.7*D12+126630/B238))` → 2400
- **E239** `=IF(B239>844200/D12,"DISMINUIR D / t",IF(D253<=C239,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B239 (Tramo 2) = `=B18/B21` → 31.75
  - D253 (Tensiones en la base del segundo tramo) = `=0.75*D98/E34` → 6.337092238522881
  - C239 (Tramo 2) = `=IF(B239<=422100/D12,D12,IF(AND(422100/D12<=B239,B239<=844200/D12),0.7*D12+126630/B239))` → 2400
- **F250** `=IF(R229<=B249,"OK! SECCION CUMPLE","f < Fy: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - R229 (Tensiones en la base del primer tramo) = `=T95/U20` → 0
  - B249 (Fm) = `=0.66*D12` → 1584
- **F251** `=IF(R230<=B249,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - R230 (Tensiones en la base del segundo tramo) = `=T96/U21` → 0
  - B249 (Fm) = `=0.66*D12` → 1584
- **F252** `=IF(D252<=B249,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D252 (Tensiones en la base del primer tramo) = `=0.75*D97/E33` → 194.15854053660834
  - B249 (Fm) = `=0.66*D12` → 1584
- **F253** `=IF(D253<=B249,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D253 (Tensiones en la base del segundo tramo) = `=0.75*D98/E34` → 6.337092238522881
  - B249 (Fm) = `=0.66*D12` → 1584
- **F254** `=IF(D254<=B249,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - B249 (Fm) = `=0.66*D12` → 1584
- **F265** `=IF(C265<=0.4*D12,"OK! SECCION CUMPLE"," CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - C265 (Tension de corte máxima:) = `=(E260+E259)*(B18/2)/B145` → 0.010349574544923234
- **F271** `=IF(S235>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - S235 (Tramo 1) = `=R229/(B249)+((S210)/B218)` → 0.0008680018256595492
- **F272** `=IF(S236>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - S236 (Tramo 2) = `=R230/(B249)+((S211)/B218)` → 0.00028244325520425915
- **F273** `=IF(C273>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C273 (Tramo 1) = `=D252/(B249)+B223/B218` → 0.1227431873989052
- **F274** `=IF(C274>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C274 (Tramo 2) = `=D253/(B249)+B224/B218` → 0.004413121161298262
- **C296** `=IF(AND(C293>10.4,C293<=12.3),"1 3/4",IF(AND(C293>12.3,C293<=14.3),"1 7/8",IF(AND(C293>14.3,C293<=16.1),"2",IF(AND(C293>16.1,C293<=21),"2 1/4",IF(AND(C293>21,C293<=25.8),"2 1/2",IF(C293>25.8,"Aumente número de pernos"," "))))))` →  
  - C293 (Area de tracción) = `=C292/(0.6*D12)` → 0.41411004655018185
  - C293 (Area de tracción) = `=C292/(0.6*D12)` → 0.41411004655018185
  - C293 (Area de tracción) = `=C292/(0.6*D12)` → 0.41411004655018185
  - C293 (Area de tracción) = `=C292/(0.6*D12)` → 0.41411004655018185
  - C293 (Area de tracción) = `=C292/(0.6*D12)` → 0.41411004655018185
  - C293 (Area de tracción) = `=C292/(0.6*D12)` → 0.41411004655018185
  - C293 (Area de tracción) = `=C292/(0.6*D12)` → 0.41411004655018185
  - C293 (Area de tracción) = `=C292/(0.6*D12)` → 0.41411004655018185
  - C293 (Area de tracción) = `=C292/(0.6*D12)` → 0.41411004655018185
  - C293 (Area de tracción) = `=C292/(0.6*D12)` → 0.41411004655018185
  - C293 (Area de tracción) = `=C292/(0.6*D12)` → 0.41411004655018185

### Constantes escritas dentro de las fórmulas (valor: veces)

`2`: 199, `4`: 70, `100`: 69, `1`: 30, `3`: 27, `6`: 24, `0.5`: 15, `3.1415`: 14, `3.14159`: 13, `32.595`: 10, `844200`: 8, `0.75`: 7, `64`: 6, `70`: 6, `0.3772`: 6, `10000`: 5, `0.37`: 5, `12`: 5, `7850`: 4, `0.6`: 4, `0.00785`: 4, `267330`: 4, `422100`: 4, `3.91`: 4, `10.4`: 4, `1.57`: 3, `50`: 3, `126`: 2, `28.594`: 2, `0.2`: 2, `16`: 2, `66832.5`: 2, `0.7`: 2, `126630`: 2, `0.21`: 2, `0.92`: 2, `1.46`: 2, `2.15`: 2, `2.98`: 2, `4.92`: 2, `6.25`: 2, `7.45`: 2, `9.06`: 2, `12.3`: 2, `14.3`: 2, `16.1`: 2, `21`: 2, `25.8`: 2, `120`: 1, `0.63`: 1, `980`: 1, `0.356`: 1, `2.467`: 1, `2100000`: 1, `0.66`: 1, `0.4`: 1, `10`: 1, `5`: 1

## P.Var.3 Tramos Circ. 1 gancho

Fórmulas: 206. Veredictos: 21 (0 con `#REF!` en su cadena). Fórmulas con `#REF!`: 0

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|
| D12 | Tension de Fluencia Fy (kg/cm2) | 2400 |
| Y12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| A15 | h1 (m) | 6 |
| B15 | h2 (m) | 6 |
| C15 | h3 (m) | 6 |
| Y15 | d1 (cm) | 5 |
| A18 | d1 (cm) | 20 |
| B18 | d2 (cm) | 25 |
| C18 | d3 (cm) | 30 |
| E18 | d (cm) | 20 |
| Y18 | e1 (cm) | 1 |
| A21 | e1 (cm) | 0.635 |
| B21 | e2 (cm) | 0.818 |
| C21 | e3 (cm) | 0.952 |
| E21 | e (cm) | 1 |
| A24 | P (Kg) | 50 |
| E24 | R (cm) | 130 |
| F24 | t (cm) | 3.5 |
| A27 | V (Kg) | 0 |
| E27 | Dist (cm) | 130 |
| H44 | SI | 130 |
| B51 | Coef. Forma | 0.6 |
| C85 | b | 0.02 |
| C86 | CL | 0.2 |
| J127 | E (kg/cm2) | 2100000 |
| M131 |  | 0 |
| P131 |  | 0 |
| K133 |  | 0 |
| N133 |  | 0 |
| M134 | La frecuencia queda determinada por: | 0 |
| P134 | La frecuencia queda determinada por: | 0 |
| K136 |  | 0 |
| N136 |  | 0 |
| B142 | G (Kg/cm2) | 840000 |
| E215 | FS | 1.67 |
| D255 | Tensiones en la base del gancho | 0 |
| C291 | Número de pernos | 10 |

### Veredictos

- **D220** `=IF(V203<=B217,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 1 CUMPLE A LA COMPRESION
  - V203 (Base tramo 1) = `=(W67+C71)/V33` → 3.977724741447892
  - B217 (Fa) = `=B216/C35/E215` → 77.41212764524649
- **D221** `=IF(B221<=B217,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 1 CUMPLE A LA COMPRESION
  - B221 (Base tramo 1) = `=0.75*(W67+B75+C71)/C33` → 4.502718094745016
  - B217 (Fa) = `=B216/C35/E215` → 77.41212764524649
- **D222** `=IF(B222<=B217,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 2 CUMPLE A LA COMPRESION
  - B222 (Base tramo 2) = `=0.75*(W67+B75+B76+C71)/C34` → 6.331670421628582
  - B217 (Fa) = `=B216/C35/E215` → 77.41212764524649
- **D223** `=IF(B223<=B217,"OK! TRAMO No 3 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 3 CUMPLE A LA COMPRESION
  - B223 (Base tramo 3) = `=0.75*(H75)/C35` → 8.887065810239882
  - B217 (Fa) = `=B216/C35/E215` → 77.41212764524649
- **E231** `=IF(B231>844200/D12,"DISMINUIR D / t",IF(B221<=C231,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B231 (Tramo 1) = `=A18/A21` → 31.496062992125985
  - B221 (Base tramo 1) = `=0.75*(W67+B75+C71)/C33` → 4.502718094745016
  - C231 (Tramo 1) = `=IF(B231<=267330/D12,D12,IF(AND(267330/D12<=B231,B231<=844200/D12),0.75*D12+66832.5/B231))` → 2400
- **E232** `=IF(B232>844200/D12,"DISMINUIR D / t",IF(B222<=C232,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B232 (Tramo 2) = `=B18/B21` → 30.56234718826406
  - B222 (Base tramo 2) = `=0.75*(W67+B75+B76+C71)/C34` → 6.331670421628582
  - C232 (Tramo 2) = `=IF(B232<=267330/D12,D12,IF(AND(267330/D12<=B232,B232<=844200/D12),0.75*D12+66832.5/B232))` → 2400
- **E233** `=IF(B233>844200/D12,"DISMINUIR D / t",IF(B223<=C233,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B233 (Tramo 3) = `=C18/C21` → 31.51260504201681
  - B223 (Base tramo 3) = `=0.75*(H75)/C35` → 8.887065810239882
  - C233 (Tramo 3) = `=IF(B233<=267330/D12,D12,IF(AND(267330/D12<=B233,B233<=844200/D12),0.75*D12+66832.5/B233))` → 2400
- **E237** `=IF(B237>844200/D12,"DISMINUIR D / t",IF(D252<=C237,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B237 (Tramo 1) = `=A18/A21` → 31.496062992125985
  - D252 (Tensiones en la base del primer tramo) = `=0.75*D97/E33` → 230.72707674115992
  - C237 (Tramo 1) = `=IF(B237<=422100/D12,D12,IF(AND(422100/D12<=B237,B237<=844200/D12),0.7*D12+126630/B237))` → 2400
- **E238** `=IF(B238>844200/D12,"DISMINUIR D / t",IF(D253<=C238,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B238 (Tramo 2) = `=B18/B21` → 30.56234718826406
  - D253 (Tensiones en la base del segundo tramo) = `=0.75*D98/E34` → 347.2870046901397
  - C238 (Tramo 2) = `=IF(B238<=422100/D12,D12,IF(AND(422100/D12<=B238,B238<=844200/D12),0.7*D12+126630/B238))` → 2400
- **E239** `=IF(B239>844200/D12,"DISMINUIR D / t",IF(D254<=C239,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B239 (Tramo 3) = `=C18/C21` → 31.51260504201681
  - D254 (Tensiones en la base del tercer tramo) = `=0.75*D99/E35` → 418.3380098669746
  - C239 (Tramo 3) = `=IF(B239<=422100/D12,D12,IF(AND(422100/D12<=B239,B239<=844200/D12),0.7*D12+126630/B239))` → 2400
- **F251** `=IF(U222<=B249,"OK! SECCION CUMPLE","f < Fy: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - U222 (Tensiones en la base del primer tramo) = `=X87/X33` → 0
  - B249 (Fm) = `=0.66*D12` → 1584
- **F252** `=IF(D252<=B249,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D252 (Tensiones en la base del primer tramo) = `=0.75*D97/E33` → 230.72707674115992
  - B249 (Fm) = `=0.66*D12` → 1584
- **F253** `=IF(D253<=B249,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D253 (Tensiones en la base del segundo tramo) = `=0.75*D98/E34` → 347.2870046901397
  - B249 (Fm) = `=0.66*D12` → 1584
- **F254** `=IF(D254<=B249,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D254 (Tensiones en la base del tercer tramo) = `=0.75*D99/E35` → 418.3380098669746
  - B249 (Fm) = `=0.66*D12` → 1584
- **F255** `=IF(D255<=B249,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - B249 (Fm) = `=0.66*D12` → 1584
- **F266** `=IF(C266<=0.4*D12,"OK! SECCION CUMPLE"," CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - C266 (Tension de corte máxima:) = `=(E261+E260)*(C18/2)/C144` → 1.2048156699374974
- **F272** `=IF(I245>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - I245 () = `=U222/(B249)+((V203)/B217)` → 0.05138374131346001
- **F273** `=IF(C273>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C273 (Tramo 1) = `=D252/(B249)+B221/B217` → 0.20382657184564312
- **F274** `=IF(C274>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C274 (Tramo 2) = `=D253/(B249)+B222/B217` → 0.30103855803309043
- **F275** `=IF(C275>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C275 (Tramo 3) = `=D254/(B249)+B223/B217` → 0.3789042625805693
- **C297** `=IF(AND(C294>10.4,C294<=12.3),"1 3/4",IF(AND(C294>12.3,C294<=14.3),"1 7/8",IF(AND(C294>14.3,C294<=16.1),"2",IF(AND(C294>16.1,C294<=21),"2 1/4",IF(AND(C294>21,C294<=25.8),"2 1/2",IF(C294>25.8,"Aumente número de pernos"," "))))))` →  
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 2.2972700036853198
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 2.2972700036853198
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 2.2972700036853198
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 2.2972700036853198
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 2.2972700036853198
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 2.2972700036853198
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 2.2972700036853198
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 2.2972700036853198
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 2.2972700036853198
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 2.2972700036853198
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 2.2972700036853198

### Constantes escritas dentro de las fórmulas (valor: veces)

`2`: 226, `4`: 90, `100`: 67, `6`: 32, `3`: 31, `1`: 29, `3.1415`: 17, `0.5`: 16, `32.595`: 14, `3.14159`: 13, `844200`: 12, `0.3772`: 10, `0.75`: 10, `12`: 9, `70`: 8, `64`: 6, `0.37`: 6, `267330`: 6, `422100`: 6, `10000`: 5, `0.00785`: 5, `7850`: 4, `3.91`: 4, `10.4`: 4, `0.6`: 3, `1.57`: 3, `66832.5`: 3, `0.7`: 3, `126630`: 3, `28.594`: 2, `0.2`: 2, `16`: 2, `0.21`: 2, `0.92`: 2, `1.46`: 2, `2.15`: 2, `2.98`: 2, `4.92`: 2, `6.25`: 2, `7.45`: 2, `9.06`: 2, `12.3`: 2, `14.3`: 2, `16.1`: 2, `21`: 2, `25.8`: 2, `126`: 1, `120`: 1, `0.63`: 1, `50`: 1, `980`: 1, `0.356`: 1, `2.467`: 1, `2100000`: 1, `0.66`: 1, `0.4`: 1, `10`: 1, `5`: 1

## P.Var.4 Tramos Circ. 1 gancho

Fórmulas: 221. Veredictos: 23 (0 con `#REF!` en su cadena). Fórmulas con `#REF!`: 0

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|
| D12 | Tension de Fluencia Fy (kg/cm2) | 2400 |
| A15 | h1 (m) | 3 |
| B15 | h2 (m) | 4 |
| C15 | h3 (m) | 4.5 |
| D15 | h4 (m) | 4.5 |
| A18 | d1 (cm) | 15 |
| B18 | d2 (cm) | 20 |
| C18 | d3 (cm) | 25 |
| D18 | d4 (cm) | 30 |
| A21 | e1 (cm) | 1 |
| B21 | e2 (cm) | 1 |
| C21 | e3 (cm) | 1 |
| D21 | e4 (cm) | 1 |
| A24 | P (Kg) | 50 |
| C24 | d (cm) | 15 |
| E24 | R (cm) | 130 |
| A27 | V (Kg) | 0 |
| C27 | e (cm) | 1 |
| E27 | t (cm) | 0 |
| F27 | Dist (cm) | 130 |
| H44 | SI | 130 |
| B51 | Coef. Forma | 0.6 |
| C76 | b | 0.02 |
| C77 | CL | 0.2 |
| J116 | E (kg/cm2) | 2100000 |
| M121 | Matriz de Rigidez | 0 |
| N121 | Matriz de Rigidez | 0 |
| Q121 | Matriz de Rigidez | 0 |
| R121 | Matriz de Rigidez | 0 |
| N122 | La frecuencia queda determinada por: | 0 |
| R122 | La frecuencia queda determinada por: | 0 |
| K123 |  | 0 |
| O123 |  | 0 |
| K124 |  | 0 |
| L124 |  | 0 |
| O124 |  | 0 |
| P124 |  | 0 |
| M125 | ciclos/s | 0 |
| N125 | ciclos/s | 0 |
| Q125 | ciclos/s | 0 |
| R125 | ciclos/s | 0 |
| N126 |  | 0 |
| R126 |  | 0 |
| K127 |  | 0 |
| O127 |  | 0 |
| K128 | 2.- FRECUENCIA POR TORSION | 0 |
| L128 | 2.- FRECUENCIA POR TORSION | 0 |
| O128 | 2.- FRECUENCIA POR TORSION | 0 |
| P128 | 2.- FRECUENCIA POR TORSION | 0 |
| B130 | G (Kg/cm2) | 840000 |
| E200 | FS | 1.67 |
| D241 | Tensiones en la base del gancho | 0 |
| C278 | Número de pernos | 4 |

### Veredictos

- **D205** `=IF(B205<=B202,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 1 CUMPLE A LA COMPRESION
  - B205 (Base tramo 1) = `=0.75*(B65+C62)/C33` → 2.6186903137789908
  - B202 (Fa) = `=B201/C36/E200` → 93.10896644271234
- **D206** `=IF(B206<=B202,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 2 CUMPLE A LA COMPRESION
  - B206 (Base tramo 2) = `=0.75*(B65+B66+C62)/C34` → 4.284637292678841
  - B202 (Fa) = `=B201/C36/E200` → 93.10896644271234
- **D207** `=IF(B207<=B202,"OK! TRAMO No 3 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 3 CUMPLE A LA COMPRESION
  - B207 (Base tramo 3) = `=0.75*(B65+B66+B67+C62)/C35` → 6.041329575596817
  - B202 (Fa) = `=B201/C36/E200` → 93.10896644271234
- **D208** `=IF(B208<=B202,"OK! TRAMO No 4 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 4 CUMPLE A LA COMPRESION
  - B208 (Base tramo 4) = `=0.75*(H66)/C36` → 8.229291738910726
  - B202 (Fa) = `=B201/C36/E200` → 93.10896644271234
- **E217** `=IF(B217>844200/D12,"DISMINUIR D / t",IF(B205<=C217,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B217 (Tramo 1) = `=A18/A21` → 15
  - B205 (Base tramo 1) = `=0.75*(B65+C62)/C33` → 2.6186903137789908
  - C217 (Tramo 1) = `=IF(B217<=267330/D12,D12,IF(AND(267330/D12<=B217,B217<=844200/D12),0.75*D12+66832.5/B217))` → 2400
- **E218** `=IF(B218>844200/D12,"DISMINUIR D / t",IF(B206<=C218,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B218 (Tramo 2) = `=B18/B21` → 20
  - B206 (Base tramo 2) = `=0.75*(B65+B66+C62)/C34` → 4.284637292678841
  - C218 (Tramo 2) = `=IF(B218<=267330/D12,D12,IF(AND(267330/D12<=B218,B218<=844200/D12),0.75*D12+66832.5/B218))` → 2400
- **E219** `=IF(B219>844200/D12,"DISMINUIR D / t",IF(B207<=C219,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B219 (Tramo 3) = `=C18/C21` → 25
  - B207 (Base tramo 3) = `=0.75*(B65+B66+B67+C62)/C35` → 6.041329575596817
  - C219 (Tramo 3) = `=IF(B219<=267330/D12,D12,IF(AND(267330/D12<=B219,B219<=844200/D12),0.75*D12+66832.5/B219))` → 2400
- **E220** `=IF(B220>844200/D12,"DISMINUIR D / t",IF(B208<=C220,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B220 (Tramo 4) = `=D18/D21` → 30
  - B208 (Base tramo 4) = `=0.75*(H66)/C36` → 8.229291738910726
  - C220 (Tramo 4) = `=IF(B220<=267330/D12,D12,IF(AND(267330/D12<=B220,B220<=844200/D12),0.75*D12+66832.5/B220))` → 2400
- **E224** `=IF(B224>844200/D12,"DISMINUIR D / t",IF(D237<=C224,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B224 (Tramo 1) = `=A18/A21` → 15
  - D237 (Tensiones en la base del primer tramo) = `=0.75*D87/E33` → 95.80133462060485
  - C224 (Tramo 1) = `=IF(B224<=422100/D12,D12,IF(AND(422100/D12<=B224,B224<=844200/D12),0.7*D12+126630/B224))` → 2400
- **E225** `=IF(B225>844200/D12,"DISMINUIR D / t",IF(D238<=C225,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B225 (Tramo 2) = `=B18/B21` → 20
  - D238 (Tensiones en la base del segundo tramo) = `=0.75*D88/E34` → 149.57730219422672
  - C225 (Tramo 2) = `=IF(B225<=422100/D12,D12,IF(AND(422100/D12<=B225,B225<=844200/D12),0.7*D12+126630/B225))` → 2400
- **E226** `=IF(B226>844200/D12,"DISMINUIR D / t",IF(D239<=C226,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B226 (Tramo 3) = `=C18/C21` → 25
  - D239 (Tensiones en la base del tercer tramo) = `=0.75*D89/E35` → 216.16042865508217
  - C226 (Tramo 3) = `=IF(B226<=422100/D12,D12,IF(AND(422100/D12<=B226,B226<=844200/D12),0.7*D12+126630/B226))` → 2400
- **E227** `=IF(B227>844200/D12,"DISMINUIR D / t",IF(D240<=C227,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B227 (Tramo 4) = `=D18/D21` → 30
  - D240 (Tensiones en la base del cuarto tramo) = `=0.75*D90/E36` → 267.3873002302284
  - C227 (Tramo 4) = `=IF(B227<=422100/D12,D12,IF(AND(422100/D12<=B227,B227<=844200/D12),0.7*D12+126630/B227))` → 2400
- **F237** `=IF(D237<=B235,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D237 (Tensiones en la base del primer tramo) = `=0.75*D87/E33` → 95.80133462060485
  - B235 (Fm) = `=0.66*D12` → 1584
- **F238** `=IF(D238<=B235,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D238 (Tensiones en la base del segundo tramo) = `=0.75*D88/E34` → 149.57730219422672
  - B235 (Fm) = `=0.66*D12` → 1584
- **F239** `=IF(D239<=B235,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D239 (Tensiones en la base del tercer tramo) = `=0.75*D89/E35` → 216.16042865508217
  - B235 (Fm) = `=0.66*D12` → 1584
- **F240** `=IF(D240<=B235,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D240 (Tensiones en la base del cuarto tramo) = `=0.75*D90/E36` → 267.3873002302284
  - B235 (Fm) = `=0.66*D12` → 1584
- **F241** `=IF(D241<=B235,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - B235 (Fm) = `=0.66*D12` → 1584
- **F252** `=IF(C252<=0.4*D12,"OK! SECCION CUMPLE"," CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - C252 (Tension de corte máxima:) = `=(E247+E246)*(D18/2)/D132` → 0.8397800508236707
- **F260** `=IF(C260>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C260 (Tramo 1) = `=D237/(B235)+B205/B202` → 0.08860564733726162
- **F261** `=IF(C261>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C261 (Tramo 2) = `=D238/(B235)+B206/B202` → 0.14044756593290184
- **F262** `=IF(C262>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C262 (Tramo 3) = `=D239/(B235)+B207/B202` → 0.20134942612817192
- **F263** `=IF(C263>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C263 (Tramo 4) = `=D240/(B235)+B208/B202` → 0.2571885644129013
- **C284** `=IF(AND(C281>10.4,C281<=12.3),"1 3/4",IF(AND(C281>12.3,C281<=14.3),"1 7/8",IF(AND(C281>14.3,C281<=16.1),"2",IF(AND(C281>16.1,C281<=21),"2 1/4",IF(AND(C281>21,C281<=25.8),"2 1/2",IF(C281>25.8,"Aumente número de pernos"," "))))))` →  
  - C281 (Area de tracción) = `=C280/(0.6*D12)` → 3.783155042635515
  - C281 (Area de tracción) = `=C280/(0.6*D12)` → 3.783155042635515
  - C281 (Area de tracción) = `=C280/(0.6*D12)` → 3.783155042635515
  - C281 (Area de tracción) = `=C280/(0.6*D12)` → 3.783155042635515
  - C281 (Area de tracción) = `=C280/(0.6*D12)` → 3.783155042635515
  - C281 (Area de tracción) = `=C280/(0.6*D12)` → 3.783155042635515
  - C281 (Area de tracción) = `=C280/(0.6*D12)` → 3.783155042635515
  - C281 (Area de tracción) = `=C280/(0.6*D12)` → 3.783155042635515
  - C281 (Area de tracción) = `=C280/(0.6*D12)` → 3.783155042635515
  - C281 (Area de tracción) = `=C280/(0.6*D12)` → 3.783155042635515
  - C281 (Area de tracción) = `=C280/(0.6*D12)` → 3.783155042635515

### Constantes escritas dentro de las fórmulas (valor: veces)

`2`: 208, `4`: 108, `100`: 77, `1`: 28, `6`: 27, `3`: 22, `3.1415`: 20, `32.595`: 18, `0.5`: 17, `844200`: 16, `0.3772`: 14, `12`: 13, `0.75`: 13, `3.14159`: 12, `70`: 10, `267330`: 8, `422100`: 8, `0.37`: 7, `64`: 6, `0.00785`: 6, `10000`: 5, `7850`: 4, `66832.5`: 4, `0.7`: 4, `126630`: 4, `3.91`: 4, `10.4`: 4, `1.57`: 3, `200`: 3, `28.594`: 2, `0.2`: 2, `16`: 2, `0.6`: 2, `0.21`: 2, `0.92`: 2, `1.46`: 2, `2.15`: 2, `2.98`: 2, `4.92`: 2, `6.25`: 2, `7.45`: 2, `9.06`: 2, `12.3`: 2, `14.3`: 2, `16.1`: 2, `21`: 2, `25.8`: 2, `120`: 1, `0.63`: 1, `980`: 1, `0.356`: 1, `2.467`: 1, `2100000`: 1, `0.66`: 1, `0.4`: 1, `10`: 1, `5`: 1

## P.Recto Cuad.

Fórmulas: 142. Veredictos: 15 (9 con `#REF!` en su cadena). Fórmulas con `#REF!`: 9 (S84, S85, S86, D215, D216, D217, M232, M233, M234)

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|
| D12 | Tension de Fluencia Fy (kg/cm2) | 2400 |
| S12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| T12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| U12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| A15 | h (m) | 7 |
| K16 | d1 (cm) | 5 |
| L16 | d2 (cm) | 20 |
| M16 | d3 (cm) | 25 |
| B18 | B (cm) | 30 |
| K19 | e1 (cm) | 1 |
| L19 | e2 (cm) | 0.635 |
| M19 | e3 (cm) | 0.818 |
| B21 | e (cm) | 0.952 |
| B24 | P (Kg) | 50 |
| B27 | V (Kg) | 250 |
| H46 | SI | 130 |
| B53 | Coef. Forma | 1.6 |
| C85 | b | 0.02 |
| C86 | CL | 0.2 |
| B142 | G (Kg/cm2) | 840000 |
| D145 | Altura de proyectores (cm) : | 100 |
| D146 | Ancho total de proyectores (cm) : | 200 |
| C282 | Número de pernos | 5 |

### Veredictos

- **D215** (cadena con #REF!) `=IF(#REF!<=#REF!,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
- **D216** (cadena con #REF!) `=IF(V193<=#REF!,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
  - V193 (Base tramo 2) = `=(S65+S66+C71)/T28` → 1.2943308309603934
- **D217** (cadena con #REF!) `=IF(V194<=#REF!,"OK! TRAMO No 3 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
  - V194 (Base tramo 3) = `=(S65+S66+S67+C71)/T32` → 0.804634695848085
- **D218** `=IF(B218<=B212,"OK! TRAMO CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO CUMPLE A LA COMPRESION
  - B218 (Base tramo) = `=0.75*(H75)/C33` → 4.46033360455655
  - B212 () = `=IF(C199<C196,(1/D209)*(1-0.5*(C199/C196)^2)*D12,(1/D209)*(3.14159^2*2100000/C199^2))` → 749.3762245588362
- **E229** `=IF(B218+D239<=D229,"OK! SECCION CUMPLE","fa+fb > Fa: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - B218 (Base tramo) = `=0.75*(H75)/C33` → 4.46033360455655
  - D239 (Tensiones en la base tramo) = `=0.75*D97/E33` → 215.0714462690075
  - D229 (Fa (Kg/cm2) :) = `=IF(B226<=2013/SQRT(D12),D12,IF(AND(2013/SQRT(D12)<=B226,B226<=3229.18/SQRT(D12)),70.35*(1.45*D12/70.35)*(1-0.0001538*SQRT(D12)*B226),70.35*108000/B226^2))` → 2400
- **F236** (cadena con #REF!) `=IF(U228<=B235,"OK! SECCION CUMPLE","f < Fy: CAMBIAR SECCION")` → #REF!
  - U228 (Tensiones en la base del primer tramo) = `=S84/V27` → #REF!
  - B235 (Fm) = `=0.66*D12` → 1584
- **F237** (cadena con #REF!) `=IF(U231<=B235,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → #REF!
  - U231 (Tensiones en la base del segundo tramo) = `=S85/V28` → #REF!
  - B235 (Fm) = `=0.66*D12` → 1584
- **F238** (cadena con #REF!) `=IF(U232<=B235,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → #REF!
  - U232 (Tensiones en la base del tercer tramo) = `=S86/V32` → #REF!
  - B235 (Fm) = `=0.66*D12` → 1584
- **F239** `=IF(D239<=B235,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D239 (Tensiones en la base tramo) = `=0.75*D97/E33` → 215.0714462690075
  - B235 (Fm) = `=0.66*D12` → 1584
- **F251** `=IF(C251<=0.4*D12,"OK! SECCION CUMPLE"," CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - C251 (Tension de corte máxima:) = `=E246*4.78/(B18^3)` → 0.0035254989583333334
- **F259** (cadena con #REF!) `=IF(M232>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M232 (Tramo 1) = `=U228/(B235)+((#REF!)/#REF!)` → #REF!
- **F260** (cadena con #REF!) `=IF(M233>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M233 (Tramo 2) = `=U231/(B235)+((V193)/#REF!)` → #REF!
- **F261** (cadena con #REF!) `=IF(M234>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M234 (Tramo 3) = `=U232/(B235)+((V194)/#REF!)` → #REF!
- **F262** `=IF(C262>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C262 (Tramo) = `=D239/(B235)+((B218)/MIN(B212,E228))` → 0.14172949000617827
- **C288** `=IF(AND(C285>10.4,C285<=12.3),"1 3/4",IF(AND(C285>12.3,C285<=14.3),"1 7/8",IF(AND(C285>14.3,C285<=16.1),"2",IF(AND(C285>16.1,C285<=21),"2 1/4",IF(AND(C285>21,C285<=25.8),"2 1/2",IF(C285>25.8,"Aumente número de pernos"," "))))))` →  
  - C285 (Area de tracción) = `=C284/(0.6*D12)` → 4.04346571061288
  - C285 (Area de tracción) = `=C284/(0.6*D12)` → 4.04346571061288
  - C285 (Area de tracción) = `=C284/(0.6*D12)` → 4.04346571061288
  - C285 (Area de tracción) = `=C284/(0.6*D12)` → 4.04346571061288
  - C285 (Area de tracción) = `=C284/(0.6*D12)` → 4.04346571061288
  - C285 (Area de tracción) = `=C284/(0.6*D12)` → 4.04346571061288
  - C285 (Area de tracción) = `=C284/(0.6*D12)` → 4.04346571061288
  - C285 (Area de tracción) = `=C284/(0.6*D12)` → 4.04346571061288
  - C285 (Area de tracción) = `=C284/(0.6*D12)` → 4.04346571061288
  - C285 (Area de tracción) = `=C284/(0.6*D12)` → 4.04346571061288
  - C285 (Area de tracción) = `=C284/(0.6*D12)` → 4.04346571061288

### Constantes escritas dentro de las fórmulas (valor: veces)

`2`: 144, `100`: 42, `4`: 40, `1`: 35, `3`: 28, `0.5`: 14, `6`: 14, `3.14159`: 12, `10000`: 5, `7850`: 4, `0.6`: 4, `70`: 4, `32.595`: 4, `3.91`: 4, `10.4`: 4, `64`: 3, `12`: 3, `126`: 3, `50`: 3, `0.2`: 3, `2100000`: 3, `0.75`: 3, `70.35`: 3, `0.3772`: 2, `16`: 2, `5`: 2, `8`: 2, `2013`: 2, `0.21`: 2, `0.92`: 2, `1.46`: 2, `2.15`: 2, `2.98`: 2, `4.92`: 2, `6.25`: 2, `7.45`: 2, `9.06`: 2, `12.3`: 2, `14.3`: 2, `16.1`: 2, `21`: 2, `25.8`: 2, `120`: 1, `3.1415`: 1, `23`: 1, `3229.18`: 1, `1.45`: 1, `0.0001538`: 1, `108000`: 1, `0.66`: 1, `4.78`: 1, `0.4`: 1, `10`: 1

## P.Recto Circ. 2 ganchos

Fórmulas: 149. Veredictos: 16 (8 con `#REF!` en su cadena). Fórmulas con `#REF!`: 8 (S83, S84, S85, D215, D216, M229, M230, M231)

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|
| D12 | Tension de Fluencia Fy (kg/cm2) | 2400 |
| S12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| T12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| U12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| A15 | h (m) | 6 |
| D15 | d (cm) | 20 |
| K16 | Espesor del gancho | 5 |
| L16 | Espesor del gancho | 20 |
| M16 | Espesor del gancho | 25 |
| A18 | d (cm) | 30 |
| D18 | e (cm) | 1 |
| K19 | Radio | 1 |
| L19 | Radio | 0.635 |
| M19 | Radio | 0.818 |
| A21 | e (cm) | 0.952 |
| D21 | R (cm) | 130 |
| A24 | P (Kg) | 50 |
| D24 | Dist (cm) | 130 |
| A27 | V (Kg) | 0 |
| D27 | t (cm) | 3.5 |
| H44 | SI | 130 |
| B51 | Coef. Forma | 0.6 |
| C85 | b | 0.02 |
| C86 | CL | 0.2 |
| B143 | G (Kg/cm2) | 840000 |
| D242 | Tensiones en la base de cada gancho | 0 |
| E247 | Momento torsional generado por viento en gancho: | 0 |
| C281 | Número de pernos | 10 |

### Veredictos

- **D215** (cadena con #REF!) `=IF(#REF!<=#REF!,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
- **D216** (cadena con #REF!) `=IF(V192<=#REF!,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
  - V192 (Base tramo 2) = `=(S64+S65+C71)/T28` → 2.5886616619207867
- **D218** `=IF(B218<=B212,"OK! TRAMO CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO CUMPLE A LA COMPRESION
  - B218 (Base tramo) = `=0.75*(H75)/C33` → 6.047612283463184
  - B212 () = `=IF(C199<C196,(1/D209)*(1-0.5*(C199/C196)^2)*D12,(1/D209)*(3.14159^2*2100000/C199^2))` → 759.9939363351695
- **E229** `=IF(B226>844200/D12,"DISMINUIR D / t",IF(B218<=D229,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B226 (D / t) = `=A18/A21` → 31.51260504201681
  - B218 (Base tramo) = `=0.75*(H75)/C33` → 6.047612283463184
  - D229 (Fa (Kg/cm2) :) = `=IF(B226<=267330/D12,D12,IF(AND(267330/D12<=B226,B226<=844200/D12),0.75*D12+66832.5/B226))` → 2400
- **E230** `=IF(B226>844200/D12,"DISMINUIR D / t",IF(D241<=D230,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B226 (D / t) = `=A18/A21` → 31.51260504201681
  - D241 (Tensiones en la base tramo) = `=0.75*D97/E33` → 80.60600389659986
  - D230 (Fb (Kg/cm2) :) = `=IF(B226<=422100/D12,D12,IF(AND(422100/D12<=B226,B226<=844200/D12),0.7*D12+126630/B226))` → 2400
- **F238** (cadena con #REF!) `=IF(U226<=B237,"OK! SECCION CUMPLE","f < Fy: CAMBIAR SECCION")` → #REF!
  - U226 (Tensiones en la base del primer tramo) = `=S83/V27` → #REF!
  - B237 (Fm) = `=0.66*D12` → 1584
- **F239** (cadena con #REF!) `=IF(U227<=B237,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → #REF!
  - U227 (Tensiones en la base del segundo tramo) = `=S84/V28` → #REF!
  - B237 (Fm) = `=0.66*D12` → 1584
- **F240** (cadena con #REF!) `=IF(U229<=B237,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → #REF!
  - U229 (Tensiones en la base del tercer tramo) = `=S85/V32` → #REF!
  - B237 (Fm) = `=0.66*D12` → 1584
- **F241** `=IF(D241<=B237,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D241 (Tensiones en la base tramo) = `=0.75*D97/E33` → 80.60600389659986
  - B237 (Fm) = `=0.66*D12` → 1584
- **F242** `=IF(D242<=B237,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - B237 (Fm) = `=0.66*D12` → 1584
- **F253** `=IF(C253<=0.4*D12,"OK! SECCION CUMPLE"," CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - C253 (Tension de corte máxima:) = `=(E248+E247)*(A18/2)/B144` → 0.0003052159137550419
- **F263** (cadena con #REF!) `=IF(M229>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M229 (Tramo 1) = `=U226/(B237)+((#REF!)/#REF!)` → #REF!
- **F264** (cadena con #REF!) `=IF(M230>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M230 (Tramo 2) = `=U227/(B237)+((V192)/#REF!)` → #REF!
- **F265** (cadena con #REF!) `=IF(M231>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M231 (Tramo 3) = `=U229/(B237)+((V193)/#REF!)` → #REF!
- **F266** `=IF(C266>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C266 (Tramo) = `=D241/(B237)+B218/B212` → 0.05884507679465513
- **C287** `=IF(AND(C284>10.4,C284<=12.3),"1 3/4",IF(AND(C284>12.3,C284<=14.3),"1 7/8",IF(AND(C284>14.3,C284<=16.1),"2",IF(AND(C284>16.1,C284<=21),"2 1/4",IF(AND(C284>21,C284<=25.8),"2 1/2",IF(C284>25.8,"Aumente número de pernos"," "))))))` →  
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 0.40776688899087865
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 0.40776688899087865
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 0.40776688899087865
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 0.40776688899087865
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 0.40776688899087865
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 0.40776688899087865
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 0.40776688899087865
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 0.40776688899087865
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 0.40776688899087865
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 0.40776688899087865
  - C284 (Area de tracción) = `=C283/(0.6*D12)` → 0.40776688899087865

### Constantes escritas dentro de las fórmulas (valor: veces)

`2`: 160, `100`: 50, `4`: 45, `1`: 32, `3`: 27, `0.5`: 16, `3.14159`: 15, `6`: 14, `10000`: 5, `64`: 5, `32.595`: 5, `3.1415`: 5, `7850`: 4, `0.6`: 4, `70`: 4, `0.75`: 4, `844200`: 4, `3.91`: 4, `10.4`: 4, `126`: 3, `50`: 3, `0.2`: 3, `2100000`: 3, `0.3772`: 2, `1.57`: 2, `16`: 2, `5`: 2, `8`: 2, `267330`: 2, `422100`: 2, `0.21`: 2, `0.92`: 2, `1.46`: 2, `2.15`: 2, `2.98`: 2, `4.92`: 2, `6.25`: 2, `7.45`: 2, `9.06`: 2, `12.3`: 2, `14.3`: 2, `16.1`: 2, `21`: 2, `25.8`: 2, `120`: 1, `0.63`: 1, `28.594`: 1, `0.00785`: 1, `0.356`: 1, `23`: 1, `12`: 1, `66832.5`: 1, `0.7`: 1, `126630`: 1, `0.66`: 1, `0.37`: 1, `0.4`: 1, `10`: 1

## P.Recto Cuad. 1 gancho

Fórmulas: 157. Veredictos: 16 (9 con `#REF!` en su cadena). Fórmulas con `#REF!`: 9 (S83, S84, S85, D215, D216, D217, M228, M229, M230)

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|
| D12 | Tension de Fluencia Fy (kg/cm2) | 2400 |
| S12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| T12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| U12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| A15 | h (m) | 6 |
| K16 | d1 (cm) | 5 |
| L16 | d2 (cm) | 20 |
| M16 | d3 (cm) | 25 |
| A18 | B (cm) | 15 |
| D18 | d1 (cm) | 40 |
| K19 | e1 (cm) | 1 |
| L19 | e2 (cm) | 0.635 |
| M19 | e3 (cm) | 0.818 |
| A21 | e (cm) | 0.952 |
| D21 | d2 (cm) | 50 |
| A24 | P (Kg) | 50 |
| D24 | d3 (cm) | 10 |
| A27 | V (Kg) | 0 |
| H46 | SI | 130 |
| B53 | Coef. Forma | 1.6 |
| C85 | b | 0.02 |
| C86 | CL | 0.2 |
| B142 | G (Kg/cm2) | 840000 |
| D240 | Tensiones en la base del gancho | 0 |
| C280 | Número de pernos | 10 |

### Veredictos

- **D215** (cadena con #REF!) `=IF(#REF!<=#REF!,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
- **D216** (cadena con #REF!) `=IF(V192<=#REF!,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
  - V192 (Base tramo 2) = `=(S64+S65+C71)/T28` → 1.2943308309603934
- **D217** (cadena con #REF!) `=IF(V193<=#REF!,"OK! TRAMO No 3 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
  - V193 (Base tramo 3) = `=(S64+S65+S66+C71)/T32` → 0.804634695848085
- **D218** `=IF(B218<=B212,"OK! TRAMO CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO CUMPLE A LA COMPRESION
  - B218 (Base tramo) = `=0.75*(H75)/C33` → 4.635767357307055
  - B212 () = `=IF(C199<C196,(1/D209)*(1-0.5*(C199/C196)^2)*D12,(1/D209)*(3.14159^2*2100000/C199^2))` → 248.2818162850156
- **E229** `=IF(B218+D239<=D229,"OK! SECCION CUMPLE","fa+fb > Fa: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - B218 (Base tramo) = `=0.75*(H75)/C33` → 4.635767357307055
  - D239 (Tensiones en la base tramo) = `=0.75*D97/E33` → 152.3935982059275
  - D229 (Fa (Kg/cm2) :) = `=IF(B226<=2013/SQRT(D12),D12,IF(AND(2013/SQRT(D12)<=B226,B226<=3229.18/SQRT(D12)),70.35*(1.45*D12/70.35)*(1-0.0001538*SQRT(D12)*B226),70.35*108000/B226^2))` → 2400
- **F236** (cadena con #REF!) `=IF(U226<=B235,"OK! SECCION CUMPLE","f < Fy: CAMBIAR SECCION")` → #REF!
  - U226 (Tensiones en la base del primer tramo) = `=S83/V27` → #REF!
  - B235 (Fm) = `=0.66*D12` → 1584
- **F237** (cadena con #REF!) `=IF(U227<=B235,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → #REF!
  - U227 (Tensiones en la base del segundo tramo) = `=S84/V28` → #REF!
  - B235 (Fm) = `=0.66*D12` → 1584
- **F238** (cadena con #REF!) `=IF(U228<=B235,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → #REF!
  - U228 (Tensiones en la base del tercer tramo) = `=S85/V32` → #REF!
  - B235 (Fm) = `=0.66*D12` → 1584
- **F239** `=IF(D239<=B235,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D239 (Tensiones en la base tramo) = `=0.75*D97/E33` → 152.3935982059275
  - B235 (Fm) = `=0.66*D12` → 1584
- **F240** `=IF(D240<=B235,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - B235 (Fm) = `=0.66*D12` → 1584
- **F251** `=IF(C251<=0.4*D12,"OK! SECCION CUMPLE"," CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - C251 (Tension de corte máxima:) = `=(E246+E245)*4.78/(A18^3)` → 0.46148480791320245
- **F260** (cadena con #REF!) `=IF(M228>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M228 (Tramo 1) = `=U226/(B235)+((#REF!)/#REF!)` → #REF!
- **F261** (cadena con #REF!) `=IF(M229>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M229 (Tramo 2) = `=U227/(B235)+((V192)/#REF!)` → #REF!
- **F262** (cadena con #REF!) `=IF(M230>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M230 (Tramo 3) = `=U228/(B235)+((V193)/#REF!)` → #REF!
- **F263** `=IF(C263>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C263 (Tramo) = `=D239/(B235)+B218/B212` → 0.11487947263798465
- **C286** `=IF(AND(C283>10.4,C283<=12.3),"1 3/4",IF(AND(C283>12.3,C283<=14.3),"1 7/8",IF(AND(C283>14.3,C283<=16.1),"2",IF(AND(C283>16.1,C283<=21),"2 1/4",IF(AND(C283>21,C283<=25.8),"2 1/2",IF(C283>25.8,"Aumente número de pernos"," "))))))` →  
  - C283 (Area de tracción) = `=C282/(0.6*D12)` → 0.5091307888967893
  - C283 (Area de tracción) = `=C282/(0.6*D12)` → 0.5091307888967893
  - C283 (Area de tracción) = `=C282/(0.6*D12)` → 0.5091307888967893
  - C283 (Area de tracción) = `=C282/(0.6*D12)` → 0.5091307888967893
  - C283 (Area de tracción) = `=C282/(0.6*D12)` → 0.5091307888967893
  - C283 (Area de tracción) = `=C282/(0.6*D12)` → 0.5091307888967893
  - C283 (Area de tracción) = `=C282/(0.6*D12)` → 0.5091307888967893
  - C283 (Area de tracción) = `=C282/(0.6*D12)` → 0.5091307888967893
  - C283 (Area de tracción) = `=C282/(0.6*D12)` → 0.5091307888967893
  - C283 (Area de tracción) = `=C282/(0.6*D12)` → 0.5091307888967893
  - C283 (Area de tracción) = `=C282/(0.6*D12)` → 0.5091307888967893

### Constantes escritas dentro de las fórmulas (valor: veces)

`2`: 156, `100`: 47, `4`: 37, `1`: 36, `3`: 30, `0.5`: 14, `6`: 14, `3.14159`: 11, `10000`: 7, `32.595`: 6, `7850`: 4, `0.6`: 4, `70`: 4, `3.91`: 4, `10.4`: 4, `64`: 3, `12`: 3, `0.00785`: 3, `126`: 3, `50`: 3, `0.2`: 3, `2100000`: 3, `0.75`: 3, `70.35`: 3, `0.3772`: 2, `28.594`: 2, `16`: 2, `5`: 2, `8`: 2, `2013`: 2, `0.21`: 2, `0.92`: 2, `1.46`: 2, `2.15`: 2, `2.98`: 2, `4.92`: 2, `6.25`: 2, `7.45`: 2, `9.06`: 2, `12.3`: 2, `14.3`: 2, `16.1`: 2, `21`: 2, `25.8`: 2, `120`: 1, `0.333`: 1, `3.1415`: 1, `23`: 1, `3229.18`: 1, `1.45`: 1, `0.0001538`: 1, `108000`: 1, `0.66`: 1, `1.6`: 1, `0.666`: 1, `4.78`: 1, `0.4`: 1, `10`: 1

## P.Recto Cuad. 2 ganchos

Fórmulas: 157. Veredictos: 16 (9 con `#REF!` en su cadena). Fórmulas con `#REF!`: 9 (S83, S84, S85, D215, D216, D217, M228, M229, M230)

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|
| D12 | Tension de Fluencia Fy (kg/cm2) | 2400 |
| S12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| T12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| U12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| A15 | h (m) | 6 |
| K16 | d1 (cm) | 5 |
| L16 | d2 (cm) | 20 |
| M16 | d3 (cm) | 25 |
| A18 | B (cm) | 15 |
| D18 | d1 (cm) | 40 |
| K19 | e1 (cm) | 1 |
| L19 | e2 (cm) | 0.635 |
| M19 | e3 (cm) | 0.818 |
| A21 | e (cm) | 0.952 |
| D21 | d2 (cm) | 50 |
| A24 | P (Kg) | 50 |
| D24 | d3 (cm) | 10 |
| A27 | V (Kg) | 0 |
| H46 | SI | 130 |
| B53 | Coef. Forma | 1.6 |
| C85 | b | 0.02 |
| C86 | CL | 0.2 |
| B142 | G (Kg/cm2) | 840000 |
| D240 | Tensiones en la base de cada gancho | 0 |
| E245 | Momento torsional generado por viento en gancho: | 0 |
| C277 | Número de pernos | 10 |

### Veredictos

- **D215** (cadena con #REF!) `=IF(#REF!<=#REF!,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
- **D216** (cadena con #REF!) `=IF(V192<=#REF!,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
  - V192 (Base tramo 2) = `=(S64+S65+C71)/T28` → 2.5886616619207867
- **D217** (cadena con #REF!) `=IF(V193<=#REF!,"OK! TRAMO No 3 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
  - V193 (Base tramo 3) = `=(S64+S65+S66+C71)/T32` → 1.60926939169617
- **D218** `=IF(B218<=B212,"OK! TRAMO CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO CUMPLE A LA COMPRESION
  - B218 (Base tramo) = `=0.75*(H75)/C33` → 5.739005269858079
  - B212 () = `=IF(C199<C196,(1/D209)*(1-0.5*(C199/C196)^2)*D12,(1/D209)*(3.14159^2*2100000/C199^2))` → 248.2818162850156
- **E229** `=IF(B218+D239<=D229,"OK! SECCION CUMPLE","fa+fb > Fa: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - B218 (Base tramo) = `=0.75*(H75)/C33` → 5.739005269858079
  - D239 (Tensiones en la base del tramo) = `=0.75*D97/E33` → 181.2576410558752
  - D229 (Fa (Kg/cm2) :) = `=IF(B226<=2013/SQRT(D12),D12,IF(AND(2013/SQRT(D12)<=B226,B226<=3229.18/SQRT(D12)),70.35*(1.45*D12/70.35)*(1-0.0001538*SQRT(D12)*B226),70.35*108000/B226^2))` → 2400
- **F236** (cadena con #REF!) `=IF(U226<=B235,"OK! SECCION CUMPLE","f < Fy: CAMBIAR SECCION")` → #REF!
  - U226 (Tensiones en la base del primer tramo) = `=S83/V27` → #REF!
  - B235 (Fm) = `=0.66*D12` → 1584
- **F237** (cadena con #REF!) `=IF(U227<=B235,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → #REF!
  - U227 (Tensiones en la base del segundo tramo) = `=S84/V28` → #REF!
  - B235 (Fm) = `=0.66*D12` → 1584
- **F238** (cadena con #REF!) `=IF(U228<=B235,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → #REF!
  - U228 (Tensiones en la base del tercer tramo) = `=S85/V32` → #REF!
  - B235 (Fm) = `=0.66*D12` → 1584
- **F239** `=IF(D239<=B235,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D239 (Tensiones en la base del tramo) = `=0.75*D97/E33` → 181.2576410558752
  - B235 (Fm) = `=0.66*D12` → 1584
- **F240** `=IF(D240<=B235,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - B235 (Fm) = `=0.66*D12` → 1584
- **F251** `=IF(C251<=0.4*D12,"OK! SECCION CUMPLE"," CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - C251 (Tension de corte máxima:) = `=(E246+E245)*4.78/(A18^3)` → 4.087665458207272e-05
- **F259** (cadena con #REF!) `=IF(M228>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M228 (Tramo 1) = `=U226/(B235)+((#REF!)/#REF!)` → #REF!
- **F260** (cadena con #REF!) `=IF(M229>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M229 (Tramo 2) = `=U227/(B235)+((V192)/#REF!)` → #REF!
- **F261** (cadena con #REF!) `=IF(M230>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M230 (Tramo 3) = `=U228/(B235)+((V193)/#REF!)` → #REF!
- **F262** `=IF(C262>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C262 (Tramo) = `=D239/(B235)+B218/B212` → 0.13754521249477406
- **C283** `=IF(AND(C280>10.4,C280<=12.3),"1 3/4",IF(AND(C280>12.3,C280<=14.3),"1 7/8",IF(AND(C280>14.3,C280<=16.1),"2",IF(AND(C280>16.1,C280<=21),"2 1/4",IF(AND(C280>21,C280<=25.8),"2 1/2",IF(C280>25.8,"Aumente número de pernos"," "))))))` →  
  - C280 (Area de tracción) = `=C279/(0.6*D12)` → 0.6044471058484333
  - C280 (Area de tracción) = `=C279/(0.6*D12)` → 0.6044471058484333
  - C280 (Area de tracción) = `=C279/(0.6*D12)` → 0.6044471058484333
  - C280 (Area de tracción) = `=C279/(0.6*D12)` → 0.6044471058484333
  - C280 (Area de tracción) = `=C279/(0.6*D12)` → 0.6044471058484333
  - C280 (Area de tracción) = `=C279/(0.6*D12)` → 0.6044471058484333
  - C280 (Area de tracción) = `=C279/(0.6*D12)` → 0.6044471058484333
  - C280 (Area de tracción) = `=C279/(0.6*D12)` → 0.6044471058484333
  - C280 (Area de tracción) = `=C279/(0.6*D12)` → 0.6044471058484333
  - C280 (Area de tracción) = `=C279/(0.6*D12)` → 0.6044471058484333
  - C280 (Area de tracción) = `=C279/(0.6*D12)` → 0.6044471058484333

### Constantes escritas dentro de las fórmulas (valor: veces)

`2`: 161, `100`: 47, `4`: 39, `1`: 36, `3`: 30, `0.5`: 14, `6`: 14, `3.14159`: 12, `10000`: 6, `32.595`: 6, `7850`: 4, `0.6`: 4, `70`: 4, `3.91`: 4, `10.4`: 4, `64`: 3, `12`: 3, `126`: 3, `50`: 3, `0.2`: 3, `2100000`: 3, `0.75`: 3, `70.35`: 3, `0.3772`: 2, `28.594`: 2, `16`: 2, `5`: 2, `8`: 2, `2013`: 2, `0.21`: 2, `0.92`: 2, `1.46`: 2, `2.15`: 2, `2.98`: 2, `4.92`: 2, `6.25`: 2, `7.45`: 2, `9.06`: 2, `12.3`: 2, `14.3`: 2, `16.1`: 2, `21`: 2, `25.8`: 2, `0.00785`: 1, `120`: 1, `0.333`: 1, `3.1415`: 1, `23`: 1, `3229.18`: 1, `1.45`: 1, `0.0001538`: 1, `108000`: 1, `0.66`: 1, `0.666`: 1, `4.78`: 1, `0.4`: 1, `10`: 1

## P.Var. 2 Tramos Circ. 2 ganchos

Fórmulas: 184. Veredictos: 19 (0 con `#REF!` en su cadena). Fórmulas con `#REF!`: 0

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|
| D12 | Tension de Fluencia Fy (kg/cm2) | 2400 |
| S13 | h1 (m) | 0 |
| T13 | h2 (m) | 0 |
| A15 | h1 (m) | 6 |
| B15 | h2 (m) | 6 |
| S16 | Diámetro del gancho | 5 |
| T16 | Diámetro del gancho | 20 |
| A18 | d1 (cm) | 25 |
| B18 | d2 (cm) | 30 |
| D18 | d (cm) | 20 |
| S19 | Espesor del gancho | 1 |
| T19 | Espesor del gancho | 0.635 |
| A21 | e1 (cm) | 0.818 |
| B21 | e2 (cm) | 0.952 |
| D21 | e (cm) | 1 |
| A24 | P (Kg) | 50 |
| D24 | R (cm) | 130 |
| E24 | t (cm) | 3.5 |
| A27 | V (Kg) | 0 |
| D27 | Dist (cm) | 130 |
| H44 | SI | 130 |
| B50 | Coef. Forma | 0.6 |
| C85 | b | 0.02 |
| C86 | CL | 0.2 |
| I128 | E (kg/cm2) | 2100000 |
| B142 | G (Kg/cm2) | 840000 |
| E215 | FS | 1.67 |
| D253 | Tensiones en la base de cada gancho | 0 |
| E258 | Momento torsional generado por viento en gancho: | 0 |
| C291 | Número de pernos | 10 |

### Veredictos

- **D220** `=IF(S210<=B217,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 1 CUMPLE A LA COMPRESION
  - S210 (Base tramo 1) = `=(R72+C71)/S20` → 7.955449482895784
  - B217 (Fa) = `=B216/C34/E215` → 201.9946574126292
- **D221** `=IF(S211<=B217,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 2 CUMPLE A LA COMPRESION
  - S211 (Base tramo 2) = `=(R72+R73+C71)/S21` → 2.5886616619207867
  - B217 (Fa) = `=B216/C34/E215` → 201.9946574126292
- **D222** `=IF(B222<=B217,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 1 CUMPLE A LA COMPRESION
  - B222 (Base tramo 1) = `=0.75*(R72+R73+B76+C71)/C33` → 4.73945928548439
  - B217 (Fa) = `=B216/C34/E215` → 201.9946574126292
- **D223** `=IF(B223<=B217,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 2 CUMPLE A LA COMPRESION
  - B223 (Base tramo 2) = `=0.75*(H75)/C34` → 8.574200681253238
  - B217 (Fa) = `=B216/C34/E215` → 201.9946574126292
- **E232** `=IF(B232>844200/D12,"DISMINUIR D / t",IF(B222<=C232,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B232 (Tramo 1) = `=A18/A21` → 30.56234718826406
  - B222 (Base tramo 1) = `=0.75*(R72+R73+B76+C71)/C33` → 4.73945928548439
  - C232 (Tramo 1) = `=IF(B232<=267330/D12,D12,IF(AND(267330/D12<=B232,B232<=844200/D12),0.75*D12+66832.5/B232))` → 2400
- **E233** `=IF(B233>844200/D12,"DISMINUIR D / t",IF(B223<=C233,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B233 (Tramo 2) = `=B18/B21` → 31.51260504201681
  - B223 (Base tramo 2) = `=0.75*(H75)/C34` → 8.574200681253238
  - C233 (Tramo 2) = `=IF(B233<=267330/D12,D12,IF(AND(267330/D12<=B233,B233<=844200/D12),0.75*D12+66832.5/B233))` → 2400
- **E237** `=IF(B237>844200/D12,"DISMINUIR D / t",IF(D251<=C237,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B237 (Tramo 1) = `=A18/A21` → 30.56234718826406
  - D251 (Tensiones en la base del primer tramo) = `=0.75*D96/E33` → 158.7454428714985
  - C237 (Tramo 1) = `=IF(B237<=422100/D12,D12,IF(AND(422100/D12<=B237,B237<=844200/D12),0.7*D12+126630/B237))` → 2400
- **E238** `=IF(B238>844200/D12,"DISMINUIR D / t",IF(D252<=C238,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B238 (Tramo 2) = `=B18/B21` → 31.51260504201681
  - D252 (Tensiones en la base del segundo tramo) = `=0.75*D97/E34` → 252.51890909926058
  - C238 (Tramo 2) = `=IF(B238<=422100/D12,D12,IF(AND(422100/D12<=B238,B238<=844200/D12),0.7*D12+126630/B238))` → 2400
- **F249** `=IF(R229<=B248,"OK! SECCION CUMPLE","f < Fy: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - R229 (Tensiones en la base del primer tramo) = `=T95/U20` → 0
  - B248 (Fm) = `=0.66*D12` → 1584
- **F250** `=IF(R230<=B248,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - R230 (Tensiones en la base del segundo tramo) = `=T96/U21` → 0
  - B248 (Fm) = `=0.66*D12` → 1584
- **F251** `=IF(D251<=B248,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D251 (Tensiones en la base del primer tramo) = `=0.75*D96/E33` → 158.7454428714985
  - B248 (Fm) = `=0.66*D12` → 1584
- **F252** `=IF(D252<=B248,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D252 (Tensiones en la base del segundo tramo) = `=0.75*D97/E34` → 252.51890909926058
  - B248 (Fm) = `=0.66*D12` → 1584
- **F253** `=IF(D253<=B248,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - B248 (Fm) = `=0.66*D12` → 1584
- **F264** `=IF(C264<=0.4*D12,"OK! SECCION CUMPLE"," CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - C264 (Tension de corte máxima:) = `=(E259+E258)*(B18/2)/B144` → 0.0001084735551474095
- **F270** `=IF(S235>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - S235 (Tramo 1) = `=R229/(B248)+((S210)/B217)` → 0.03938445493954133
- **F271** `=IF(S236>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - S236 (Tramo 2) = `=R230/(B248)+((S211)/B217)` → 0.01281549569220902
- **F272** `=IF(C272>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C272 (Tramo 1) = `=D251/(B248)+B222/B217` → 0.12368137291873124
- **F273** `=IF(C273>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C273 (Tramo 2) = `=D252/(B248)+B223/B217` → 0.2018661639201669
- **C297** `=IF(AND(C294>10.4,C294<=12.3),"1 3/4",IF(AND(C294>12.3,C294<=14.3),"1 7/8",IF(AND(C294>14.3,C294<=16.1),"2",IF(AND(C294>16.1,C294<=21),"2 1/4",IF(AND(C294>21,C294<=25.8),"2 1/2",IF(C294>25.8,"Aumente número de pernos"," "))))))` →  
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 1.3608668789777592
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 1.3608668789777592
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 1.3608668789777592
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 1.3608668789777592
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 1.3608668789777592
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 1.3608668789777592
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 1.3608668789777592
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 1.3608668789777592
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 1.3608668789777592
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 1.3608668789777592
  - C294 (Area de tracción) = `=C293/(0.6*D12)` → 1.3608668789777592

### Constantes escritas dentro de las fórmulas (valor: veces)

`2`: 190, `100`: 67, `4`: 63, `1`: 30, `3`: 27, `6`: 24, `0.5`: 15, `3.14159`: 14, `32.595`: 10, `844200`: 8, `0.75`: 7, `64`: 6, `70`: 6, `0.3772`: 6, `10000`: 5, `3.1415`: 5, `12`: 5, `7850`: 4, `267330`: 4, `422100`: 4, `3.91`: 4, `10.4`: 4, `0.6`: 3, `50`: 3, `126`: 2, `1.57`: 2, `28.594`: 2, `0.2`: 2, `16`: 2, `66832.5`: 2, `0.7`: 2, `126630`: 2, `0.21`: 2, `0.92`: 2, `1.46`: 2, `2.15`: 2, `2.98`: 2, `4.92`: 2, `6.25`: 2, `7.45`: 2, `9.06`: 2, `12.3`: 2, `14.3`: 2, `16.1`: 2, `21`: 2, `25.8`: 2, `120`: 1, `0.63`: 1, `0.00785`: 1, `980`: 1, `0.356`: 1, `2.467`: 1, `2100000`: 1, `0.66`: 1, `0.37`: 1, `0.4`: 1, `10`: 1, `5`: 1

## P.Var.3 Tramos Circ. 2 ganchos

Fórmulas: 205. Veredictos: 21 (0 con `#REF!` en su cadena). Fórmulas con `#REF!`: 0

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|
| D12 | Tension de Fluencia Fy (kg/cm2) | 2400 |
| Y12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| A15 | h1 (m) | 1.3 |
| B15 | h2 (m) | 2.7 |
| C15 | h3 (m) | 6 |
| Y15 | d1 (cm) | 5 |
| A18 | d1 (cm) | 8.89 |
| B18 | d2 (cm) | 11.4 |
| C18 | d3 (cm) | 13 |
| E18 | d (cm) | 6.03 |
| Y18 | e1 (cm) | 1 |
| A21 | e1 (cm) | 0.32 |
| B21 | e2 (cm) | 0.36 |
| C21 | e3 (cm) | 0.36 |
| E21 | e (cm) | 0.26 |
| A24 | P (Kg) | 17 |
| E24 | R (cm) | 150 |
| F24 | t (cm) | 6.03 |
| A27 | V (Kg) | 0 |
| E27 | Dist (cm) | 150 |
| H44 | SI | 130 |
| B50 | Coef. Forma | 0.6 |
| C84 | b | 0.02 |
| C85 | CL | 0.2 |
| J128 | E (kg/cm2) | 2100000 |
| M132 |  | 0 |
| P132 |  | 0 |
| K134 |  | 0 |
| N134 |  | 0 |
| M135 |  | 0 |
| P135 |  | 0 |
| K137 |  | 0 |
| N137 |  | 0 |
| B141 | G (Kg/cm2) | 840000 |
| E214 | FS | 1.67 |
| D254 | Tensiones en la base de cada gancho | 0 |
| E259 | Momento torsional generado por viento en gancho: | 0 |
| C288 | Número de pernos | 4 |

### Veredictos

- **D219** `=IF(V203<=B216,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 1 CUMPLE A LA COMPRESION
  - V203 (Base tramo 1) = `=(W67+C70)/V33` → 2.704852824184566
  - B216 (Fa) = `=B215/C35/E214` → 58.27029653824987
- **D220** `=IF(B220<=B216,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 1 CUMPLE A LA COMPRESION
  - B220 (Base tramo 1) = `=0.75*(W67+B74+C70)/C33` → 3.7239849187935046
  - B216 (Fa) = `=B215/C35/E214` → 58.27029653824987
- **D221** `=IF(B221<=B216,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 2 CUMPLE A LA COMPRESION
  - B221 (Base tramo 2) = `=0.75*(W67+B74+B75+C70)/C34` → 4.158987189751801
  - B216 (Fa) = `=B215/C35/E214` → 58.27029653824987
- **D222** `=IF(B222<=B216,"OK! TRAMO No 3 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 3 CUMPLE A LA COMPRESION
  - B222 (Base tramo 3) = `=0.75*(H74)/C35` → 8.080829617332293
  - B216 (Fa) = `=B215/C35/E214` → 58.27029653824987
- **E230** `=IF(B230>844200/D12,"DISMINUIR D / t",IF(B220<=C230,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B230 (Tramo 1) = `=A18/A21` → 27.78125
  - B220 (Base tramo 1) = `=0.75*(W67+B74+C70)/C33` → 3.7239849187935046
  - C230 (Tramo 1) = `=IF(B230<=267330/D12,D12,IF(AND(267330/D12<=B230,B230<=844200/D12),0.75*D12+66832.5/B230))` → 2400
- **E231** `=IF(B231>844200/D12,"DISMINUIR D / t",IF(B221<=C231,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B231 (Tramo 2) = `=B18/B21` → 31.666666666666668
  - B221 (Base tramo 2) = `=0.75*(W67+B74+B75+C70)/C34` → 4.158987189751801
  - C231 (Tramo 2) = `=IF(B231<=267330/D12,D12,IF(AND(267330/D12<=B231,B231<=844200/D12),0.75*D12+66832.5/B231))` → 2400
- **E232** `=IF(B232>844200/D12,"DISMINUIR D / t",IF(B222<=C232,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B232 (Tramo 3) = `=C18/C21` → 36.111111111111114
  - B222 (Base tramo 3) = `=0.75*(H74)/C35` → 8.080829617332293
  - C232 (Tramo 3) = `=IF(B232<=267330/D12,D12,IF(AND(267330/D12<=B232,B232<=844200/D12),0.75*D12+66832.5/B232))` → 2400
- **E236** `=IF(B236>844200/D12,"DISMINUIR D / t",IF(D251<=C236,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B236 (Tramo 1) = `=A18/A21` → 27.78125
  - D251 (Tensiones en la base del primer tramo) = `=0.75*D96/E33` → 227.20704751042194
  - C236 (Tramo 1) = `=IF(B236<=422100/D12,D12,IF(AND(422100/D12<=B236,B236<=844200/D12),0.7*D12+126630/B236))` → 2400
- **E237** `=IF(B237>844200/D12,"DISMINUIR D / t",IF(D252<=C237,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B237 (Tramo 2) = `=B18/B21` → 31.666666666666668
  - D252 (Tensiones en la base del segundo tramo) = `=0.75*D97/E34` → 365.0537049023221
  - C237 (Tramo 2) = `=IF(B237<=422100/D12,D12,IF(AND(422100/D12<=B237,B237<=844200/D12),0.7*D12+126630/B237))` → 2400
- **E238** `=IF(B238>844200/D12,"DISMINUIR D / t",IF(D253<=C238,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B238 (Tramo 3) = `=C18/C21` → 36.111111111111114
  - D253 (Tensiones en la base del tercer tramo) = `=0.75*D98/E35` → 1005.1320707614034
  - C238 (Tramo 3) = `=IF(B238<=422100/D12,D12,IF(AND(422100/D12<=B238,B238<=844200/D12),0.7*D12+126630/B238))` → 2400
- **F250** `=IF(U222<=B248,"OK! SECCION CUMPLE","f < Fy: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - U222 (Tensiones en la base del primer tramo) = `=X87/X33` → 0
  - B248 (Fm) = `=0.66*D12` → 1584
- **F251** `=IF(D251<=B248,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D251 (Tensiones en la base del primer tramo) = `=0.75*D96/E33` → 227.20704751042194
  - B248 (Fm) = `=0.66*D12` → 1584
- **F252** `=IF(D252<=B248,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D252 (Tensiones en la base del segundo tramo) = `=0.75*D97/E34` → 365.0537049023221
  - B248 (Fm) = `=0.66*D12` → 1584
- **F253** `=IF(D253<=B248,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D253 (Tensiones en la base del tercer tramo) = `=0.75*D98/E35` → 1005.1320707614034
  - B248 (Fm) = `=0.66*D12` → 1584
- **F254** `=IF(D254<=B248,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - B248 (Fm) = `=0.66*D12` → 1584
- **F265** `=IF(C265<=0.4*D12,"OK! SECCION CUMPLE"," CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - C265 (Tension de corte máxima:) = `=(E260+E259)*(C18/2)/C143` → 1.4321576653014794e-05
- **F271** `=IF(I243>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - I243 () = `=U222/(B248)+((V203)/B216)` → 0.04641906743016217
- **F272** `=IF(C272>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C272 (Tramo 1) = `=D251/(B248)+B220/B216` → 0.20734759590473323
- **F273** `=IF(C273>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C273 (Tramo 2) = `=D252/(B248)+B221/B216` → 0.30183724978947796
- **F274** `=IF(C274>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C274 (Tramo 3) = `=D253/(B248)+B222/B216` → 0.773231442813145
- **C294** `=IF(AND(C291>10.4,C291<=12.3),"1 3/4",IF(AND(C291>12.3,C291<=14.3),"1 7/8",IF(AND(C291>14.3,C291<=16.1),"2",IF(AND(C291>16.1,C291<=21),"2 1/4",IF(AND(C291>21,C291<=25.8),"2 1/2",IF(C291>25.8,"Aumente número de pernos"," "))))))` →  
  - C291 (Area de tracción) = `=C290/(0.6*D12)` → 1.7520595658368014
  - C291 (Area de tracción) = `=C290/(0.6*D12)` → 1.7520595658368014
  - C291 (Area de tracción) = `=C290/(0.6*D12)` → 1.7520595658368014
  - C291 (Area de tracción) = `=C290/(0.6*D12)` → 1.7520595658368014
  - C291 (Area de tracción) = `=C290/(0.6*D12)` → 1.7520595658368014
  - C291 (Area de tracción) = `=C290/(0.6*D12)` → 1.7520595658368014
  - C291 (Area de tracción) = `=C290/(0.6*D12)` → 1.7520595658368014
  - C291 (Area de tracción) = `=C290/(0.6*D12)` → 1.7520595658368014
  - C291 (Area de tracción) = `=C290/(0.6*D12)` → 1.7520595658368014
  - C291 (Area de tracción) = `=C290/(0.6*D12)` → 1.7520595658368014
  - C291 (Area de tracción) = `=C290/(0.6*D12)` → 1.7520595658368014

### Constantes escritas dentro de las fórmulas (valor: veces)

`2`: 207, `4`: 78, `100`: 65, `6`: 32, `3`: 31, `1`: 29, `0.5`: 16, `32.595`: 14, `3.14159`: 13, `844200`: 12, `0.3772`: 10, `0.75`: 10, `12`: 9, `70`: 8, `64`: 6, `267330`: 6, `422100`: 6, `10000`: 5, `3.1415`: 5, `7850`: 4, `3.91`: 4, `10.4`: 4, `66832.5`: 3, `0.7`: 3, `126630`: 3, `0.6`: 2, `1.57`: 2, `28.594`: 2, `0.2`: 2, `16`: 2, `0.21`: 2, `0.92`: 2, `1.46`: 2, `2.15`: 2, `2.98`: 2, `4.92`: 2, `6.25`: 2, `7.45`: 2, `9.06`: 2, `12.3`: 2, `14.3`: 2, `16.1`: 2, `21`: 2, `25.8`: 2, `126`: 1, `120`: 1, `0.63`: 1, `0.00785`: 1, `50`: 1, `980`: 1, `0.356`: 1, `2.467`: 1, `2100000`: 1, `0.66`: 1, `0.37`: 1, `0.4`: 1, `10`: 1, `5`: 1

## P.Var.4 Tramos Circ. 2 ganchos

Fórmulas: 222. Veredictos: 23 (0 con `#REF!` en su cadena). Fórmulas con `#REF!`: 0

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|
| D12 | Tension de Fluencia Fy (kg/cm2) | 2400 |
| A15 | h1 (m) | 1.2 |
| B15 | h2 (m) | 5.4 |
| C15 | h3 (m) | 5.4 |
| D15 | h4 (m) | 6 |
| A18 | d1 (cm) | 11.4 |
| B18 | d2 (cm) | 16.83 |
| C18 | d3 (cm) | 21.91 |
| D18 | d4 (cm) | 27.31 |
| A21 | e1 (cm) | 0.36 |
| B21 | e2 (cm) | 0.5 |
| C21 | e3 (cm) | 0.635 |
| D21 | e4 (cm) | 0.635 |
| A24 | P (Kg) | 17 |
| C24 | d (cm) | 6.03 |
| E24 | R (cm) | 150 |
| A27 | V (Kg) | 0 |
| C27 | e (cm) | 0.29 |
| E27 | t (cm) | 6.03 |
| F27 | Dist (cm) | 150 |
| H44 | SI | 130 |
| B52 | Coef. Forma | 0.6 |
| C86 | b | 0.02 |
| C87 | CL | 0.2 |
| J127 | E (kg/cm2) | 2100000 |
| M131 | 1.- FRECUENCIA POR TRASLACION | 0 |
| N131 | 1.- FRECUENCIA POR TRASLACION | 0 |
| Q131 | 1.- FRECUENCIA POR TRASLACION | 0 |
| R131 | 1.- FRECUENCIA POR TRASLACION | 0 |
| N132 | Matriz de Rigidez | 0 |
| R132 | Matriz de Rigidez | 0 |
| K133 |  | 0 |
| O133 |  | 0 |
| K134 |  | 0 |
| L134 |  | 0 |
| O134 |  | 0 |
| P134 |  | 0 |
| M135 | La frecuencia queda determinada por: | 0 |
| N135 | La frecuencia queda determinada por: | 0 |
| Q135 | La frecuencia queda determinada por: | 0 |
| R135 | La frecuencia queda determinada por: | 0 |
| N136 |  | 0 |
| R136 |  | 0 |
| K137 |  | 0 |
| O137 |  | 0 |
| K138 | ciclos/s | 0 |
| L138 | ciclos/s | 0 |
| O138 | ciclos/s | 0 |
| P138 | ciclos/s | 0 |
| B143 | G (Kg/cm2) | 840000 |
| E216 | FS | 1.67 |
| D260 | Tensiones en la base de cada gancho | 0 |
| E265 | Momento torsional generado por viento en gancho: | 0 |
| C295 | Número de pernos | 4 |

### Veredictos

- **D221** `=IF(B221<=B218,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 1 CUMPLE A LA COMPRESION
  - B221 (Base tramo 1) = `=0.75*(B75+C72)/C33` → 2.747798238590873
  - B218 (Fa) = `=B217/C36/E216` → 64.12187851516951
- **D222** `=IF(B222<=B218,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 2 CUMPLE A LA COMPRESION
  - B222 (Base tramo 2) = `=0.75*(B75+B76+C72)/C34` → 4.518011695906433
  - B218 (Fa) = `=B217/C36/E216` → 64.12187851516951
- **D223** `=IF(B223<=B218,"OK! TRAMO No 3 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 3 CUMPLE A LA COMPRESION
  - B223 (Base tramo 3) = `=0.75*(B75+B76+B77+C72)/C35` → 5.910296889726674
  - B218 (Fa) = `=B217/C36/E216` → 64.12187851516951
- **D224** `=IF(B224<=B218,"OK! TRAMO No 4 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO No 4 CUMPLE A LA COMPRESION
  - B224 (Base tramo 4) = `=0.75*(H76)/C36` → 8.519187275417867
  - B218 (Fa) = `=B217/C36/E216` → 64.12187851516951
- **E233** `=IF(B233>844200/D12,"DISMINUIR D / t",IF(B221<=C233,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B233 (Tramo 1) = `=A18/A21` → 31.666666666666668
  - B221 (Base tramo 1) = `=0.75*(B75+C72)/C33` → 2.747798238590873
  - C233 (Tramo 1) = `=IF(B233<=267330/D12,D12,IF(AND(267330/D12<=B233,B233<=844200/D12),0.75*D12+66832.5/B233))` → 2400
- **E234** `=IF(B234>844200/D12,"DISMINUIR D / t",IF(B222<=C234,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B234 (Tramo 2) = `=B18/B21` → 33.66
  - B222 (Base tramo 2) = `=0.75*(B75+B76+C72)/C34` → 4.518011695906433
  - C234 (Tramo 2) = `=IF(B234<=267330/D12,D12,IF(AND(267330/D12<=B234,B234<=844200/D12),0.75*D12+66832.5/B234))` → 2400
- **E235** `=IF(B235>844200/D12,"DISMINUIR D / t",IF(B223<=C235,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B235 (Tramo 3) = `=C18/C21` → 34.503937007874015
  - B223 (Base tramo 3) = `=0.75*(B75+B76+B77+C72)/C35` → 5.910296889726674
  - C235 (Tramo 3) = `=IF(B235<=267330/D12,D12,IF(AND(267330/D12<=B235,B235<=844200/D12),0.75*D12+66832.5/B235))` → 2400
- **E236** `=IF(B236>844200/D12,"DISMINUIR D / t",IF(B224<=C236,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B236 (Tramo 4) = `=D18/D21` → 43.00787401574803
  - B224 (Base tramo 4) = `=0.75*(H76)/C36` → 8.519187275417867
  - C236 (Tramo 4) = `=IF(B236<=267330/D12,D12,IF(AND(267330/D12<=B236,B236<=844200/D12),0.75*D12+66832.5/B236))` → 2400
- **E240** `=IF(B240>844200/D12,"DISMINUIR D / t",IF(D256<=C240,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B240 (Tramo 1) = `=A18/A21` → 31.666666666666668
  - D256 (Tensiones en la base del primer tramo) = `=0.75*D97/E33` → 136.6023618931038
  - C240 (Tramo 1) = `=IF(B240<=422100/D12,D12,IF(AND(422100/D12<=B240,B240<=844200/D12),0.7*D12+126630/B240))` → 2400
- **E241** `=IF(B241>844200/D12,"DISMINUIR D / t",IF(D257<=C241,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B241 (Tramo 2) = `=B18/B21` → 33.66
  - D257 (Tensiones en la base del segundo tramo) = `=0.75*D98/E34` → 340.1855254018496
  - C241 (Tramo 2) = `=IF(B241<=422100/D12,D12,IF(AND(422100/D12<=B241,B241<=844200/D12),0.7*D12+126630/B241))` → 2400
- **E242** `=IF(B242>844200/D12,"DISMINUIR D / t",IF(D258<=C242,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B242 (Tramo 3) = `=C18/C21` → 34.503937007874015
  - D258 (Tensiones en la base del tercer tramo) = `=0.75*D99/E35` → 439.51666717999365
  - C242 (Tramo 3) = `=IF(B242<=422100/D12,D12,IF(AND(422100/D12<=B242,B242<=844200/D12),0.7*D12+126630/B242))` → 2400
- **E243** `=IF(B243>844200/D12,"DISMINUIR D / t",IF(D259<=C243,"OK! SECCION CUMPLE","fa > Fa: CAMBIAR SECCION"))` → OK! SECCION CUMPLE
  - B243 (Tramo 4) = `=D18/D21` → 43.00787401574803
  - D259 (Tensiones en la base del cuarto tramo) = `=0.75*D100/E36` → 584.6167612661277
  - C243 (Tramo 4) = `=IF(B243<=422100/D12,D12,IF(AND(422100/D12<=B243,B243<=844200/D12),0.7*D12+126630/B243))` → 2400
- **F256** `=IF(D256<=B254,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D256 (Tensiones en la base del primer tramo) = `=0.75*D97/E33` → 136.6023618931038
  - B254 (Fm) = `=0.66*D12` → 1584
- **F257** `=IF(D257<=B254,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D257 (Tensiones en la base del segundo tramo) = `=0.75*D98/E34` → 340.1855254018496
  - B254 (Fm) = `=0.66*D12` → 1584
- **F258** `=IF(D258<=B254,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D258 (Tensiones en la base del tercer tramo) = `=0.75*D99/E35` → 439.51666717999365
  - B254 (Fm) = `=0.66*D12` → 1584
- **F259** `=IF(D259<=B254,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D259 (Tensiones en la base del cuarto tramo) = `=0.75*D100/E36` → 584.6167612661277
  - B254 (Fm) = `=0.66*D12` → 1584
- **F260** `=IF(D260<=B254,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - B254 (Fm) = `=0.66*D12` → 1584
- **F271** `=IF(C271<=0.4*D12,"OK! SECCION CUMPLE"," CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - C271 (Tension de corte máxima:) = `=(E266+E265)*(D18/2)/D145` → 3.8135232056157405e-05
- **F277** `=IF(C277>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C277 (Tramo 1) = `=D256/(B254)+B221/B218` → 0.12909160561546085
- **F278** `=IF(C278>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C278 (Tramo 2) = `=D257/(B254)+B222/B218` → 0.28522334186074005
- **F279** `=IF(C279>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C279 (Tramo 3) = `=D258/(B254)+B223/B218` → 0.36964550277311936
- **F280** `=IF(C280>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C280 (Tramo 4) = `=D259/(B254)+B224/B218` → 0.5019355285228035
- **C301** `=IF(AND(C298>10.4,C298<=12.3),"1 3/4",IF(AND(C298>12.3,C298<=14.3),"1 7/8",IF(AND(C298>14.3,C298<=16.1),"2",IF(AND(C298>16.1,C298<=21),"2 1/4",IF(AND(C298>21,C298<=25.8),"2 1/2",IF(C298>25.8,"Aumente número de pernos"," "))))))` →  
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 4.926903070563834
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 4.926903070563834
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 4.926903070563834
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 4.926903070563834
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 4.926903070563834
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 4.926903070563834
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 4.926903070563834
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 4.926903070563834
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 4.926903070563834
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 4.926903070563834
  - C298 (Area de tracción) = `=C297/(0.6*D12)` → 4.926903070563834

### Constantes escritas dentro de las fórmulas (valor: veces)

`2`: 193, `4`: 93, `100`: 75, `1`: 28, `6`: 27, `3`: 22, `32.595`: 18, `0.5`: 17, `844200`: 16, `0.3772`: 14, `12`: 13, `0.75`: 13, `3.14159`: 12, `70`: 10, `267330`: 8, `422100`: 8, `64`: 6, `10000`: 5, `3.1415`: 5, `7850`: 4, `66832.5`: 4, `0.7`: 4, `126630`: 4, `3.91`: 4, `10.4`: 4, `200`: 3, `1.57`: 2, `28.594`: 2, `0.2`: 2, `16`: 2, `0.21`: 2, `0.92`: 2, `1.46`: 2, `2.15`: 2, `2.98`: 2, `4.92`: 2, `6.25`: 2, `7.45`: 2, `9.06`: 2, `12.3`: 2, `14.3`: 2, `16.1`: 2, `21`: 2, `25.8`: 2, `120`: 1, `0.63`: 1, `0.00785`: 1, `980`: 1, `0.356`: 1, `2.467`: 1, `2100000`: 1, `0.66`: 1, `0.37`: 1, `0.4`: 1, `10`: 1, `0.6`: 1, `5`: 1

## P.Var. Octogonal

Fórmulas: 148. Veredictos: 15 (9 con `#REF!` en su cadena). Fórmulas con `#REF!`: 9 (S83, S84, S85, D197, D198, D199, M228, M229, M230)

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|
| D12 | Tension de Fluencia Fy (kg/cm2) | 2400 |
| S12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| T12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| U12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| A15 | h (m) | 20 |
| K16 | Diámetro extremos del poste | 5 |
| L16 | Diámetro extremos del poste | 20 |
| M16 | Diámetro extremos del poste | 25 |
| A18 | d sup. (cm) | 20 |
| B18 | d base(cm) | 50 |
| K19 | e1 (cm) | 1 |
| L19 | e2 (cm) | 0.635 |
| M19 | e3 (cm) | 0.818 |
| A21 | e (cm) | 0.5 |
| A24 | P (Kg) | 300 |
| A27 | V (Kg) | 1120 |
| H44 | SI | 120 |
| B51 | Coef. Forma | 0.7 |
| C84 | b | 0.02 |
| C85 | CL | 0.2 |
| B140 | G (Kg/cm2) | 840000 |
| D143 | Altura de proyectores (cm) : | 100 |
| D144 | Ancho total de proyectores (cm) : | 200 |
| C259 | Número de pernos | 16 |

### Veredictos

- **D197** (cadena con #REF!) `=IF(#REF!<=#REF!,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
- **D198** (cadena con #REF!) `=IF(V192<=#REF!,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
  - V192 (Base tramo 2) = `=(S64+S65+C70)/T28` → 7.76598498576236
- **D199** (cadena con #REF!) `=IF(V193<=#REF!,"OK! TRAMO No 3 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
  - V193 (Base tramo 3) = `=(S64+S65+S66+C70)/S32` → 4.82780817508851
- **D200** `=IF(B200<=F195,"OK! TRAMO CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO CUMPLE A LA COMPRESION
  - B200 (Base tramo) = `=0.75*(H74)/B34` → 11.175871862615587
  - F195 (Por lo tanto se tiene que la carga admisible a la ) = `=(G190/E193)/B34` → 56.66671034492206
- **D210** `=IF(B200+D221<=B210,"OK! SECCION CUMPLE ","PANDEO LOCAL. CAMBIAR SECCION")` → PANDEO LOCAL. CAMBIAR SECCION
  - B200 (Base tramo) = `=0.75*(H74)/B34` → 11.175871862615587
  - D221 (Tensión máxima en la base) = `=0.75*D96/D34` → 2416.1913158887496
  - B210 () = `=IF(B208<=(240/SQRT(D12/70.35)),D12,IF(AND(B208>=240/SQRT(D12/70.35),B208<=385/SQRT(D12/70.35)),1.45*D12*(1-0.00129*SQRT(D12/70.35)*B208),108000*70.35/B208^2))` → 2400
- **F218** (cadena con #REF!) `=IF(U226<=B217,"OK! SECCION CUMPLE","f < Fy: CAMBIAR SECCION")` → #REF!
  - U226 (Tensiones en la base del primer tramo) = `=S83/V27` → #REF!
  - B217 (Fm) = `=0.66*D12` → 1584
- **F219** (cadena con #REF!) `=IF(U227<=B217,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → #REF!
  - U227 (Tensiones en la base del segundo tramo) = `=S84/V28` → #REF!
  - B217 (Fm) = `=0.66*D12` → 1584
- **F220** (cadena con #REF!) `=IF(U228<=B217,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → #REF!
  - U228 (Tensiones en la base del tercer tramo) = `=S85/U32` → #REF!
  - B217 (Fm) = `=0.66*D12` → 1584
- **F221** `=IF(D221<=B217,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → fm > Fm: CAMBIAR SECCION
  - D221 (Tensión máxima en la base) = `=0.75*D96/D34` → 2416.1913158887496
  - B217 (Fm) = `=0.66*D12` → 1584
- **F234** `=IF(C234<=0.4*D12,"OK! SECCION CUMPLE"," CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - C234 (Tension de corte máxima:) = `=E229*(B18/2)/B141` → 0.0008615655845708528
- **F241** (cadena con #REF!) `=IF(M228>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M228 (Tramo 1) = `=U226/(B217)+((#REF!)/#REF!)` → #REF!
- **F242** (cadena con #REF!) `=IF(M229>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M229 (Tramo 2) = `=U227/(B217)+((V192)/#REF!)` → #REF!
- **F243** (cadena con #REF!) `=IF(M230>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M230 (Tramo 3) = `=U228/(B217)+((V193)/#REF!)` → #REF!
- **F244** `=IF(C244>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → INTERACCION > 1. NO CUMPLE
  - C244 (Tramo) = `=D221/(B217)+B200/F195` → 1.7225944216325213
- **C265** `=IF(AND(C262>10.4,C262<=12.3),"1 3/4",IF(AND(C262>12.3,C262<=14.3),"1 7/8",IF(AND(C262>14.3,C262<=16.1),"2",IF(AND(C262>16.1,C262<=21),"2 1/4",IF(AND(C262>21,C262<=25.8),"2 1/2",IF(C262>25.8,"Aumente número de pernos"," "))))))` →  
  - C262 (Area de tracción) = `=C261/(0.6*D12)` → 8.831755795656068
  - C262 (Area de tracción) = `=C261/(0.6*D12)` → 8.831755795656068
  - C262 (Area de tracción) = `=C261/(0.6*D12)` → 8.831755795656068
  - C262 (Area de tracción) = `=C261/(0.6*D12)` → 8.831755795656068
  - C262 (Area de tracción) = `=C261/(0.6*D12)` → 8.831755795656068
  - C262 (Area de tracción) = `=C261/(0.6*D12)` → 8.831755795656068
  - C262 (Area de tracción) = `=C261/(0.6*D12)` → 8.831755795656068
  - C262 (Area de tracción) = `=C261/(0.6*D12)` → 8.831755795656068
  - C262 (Area de tracción) = `=C261/(0.6*D12)` → 8.831755795656068
  - C262 (Area de tracción) = `=C261/(0.6*D12)` → 8.831755795656068
  - C262 (Area de tracción) = `=C261/(0.6*D12)` → 8.831755795656068

### Constantes escritas dentro de las fórmulas (valor: veces)

`2`: 156, `4`: 44, `100`: 44, `1`: 30, `3`: 22, `3.14159`: 15, `0.5`: 15, `6`: 14, `64`: 6, `70.35`: 5, `10000`: 4, `0.6`: 4, `70`: 4, `32.595`: 4, `3.91`: 4, `10.4`: 4, `7850`: 3, `126`: 3, `50`: 3, `16`: 3, `0.75`: 3, `6.122`: 2, `3.31`: 2, `0.3772`: 2, `0.2`: 2, `2.54`: 2, `2100000`: 2, `12`: 2, `240`: 2, `0.21`: 2, `0.92`: 2, `1.46`: 2, `2.15`: 2, `2.98`: 2, `4.92`: 2, `6.25`: 2, `7.45`: 2, `9.06`: 2, `12.3`: 2, `14.3`: 2, `16.1`: 2, `21`: 2, `25.8`: 2, `120`: 1, `0.00785`: 1, `3.9`: 1, `14.22`: 1, `0.283`: 1, `23`: 1, `0.3826`: 1, `385`: 1, `1.45`: 1, `0.00129`: 1, `108000`: 1, `0.66`: 1, `0.4`: 1, `10`: 1, `5`: 1

## P.Var. Octogonal 1 gancho

Fórmulas: 153. Veredictos: 15 (9 con `#REF!` en su cadena). Fórmulas con `#REF!`: 9 (S83, S84, S85, D197, D198, D199, M228, M229, M230)

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|
| D12 | Tension de Fluencia Fy (kg/cm2) | 2400 |
| S12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| T12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| U12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| A15 | h (m) | 20 |
| K16 | Diámetro extremos del poste | 5 |
| L16 | Diámetro extremos del poste | 20 |
| M16 | Diámetro extremos del poste | 25 |
| A18 | d sup. (cm) | 20 |
| B18 | d base(cm) | 30 |
| K19 | e1 (cm) | 1 |
| L19 | e2 (cm) | 0.635 |
| M19 | e3 (cm) | 0.818 |
| A21 | e (cm) | 0.952 |
| A24 | P (Kg) | 50 |
| A27 | V (Kg) | 0 |
| A33 | d (cm) | 20 |
| C33 | R (cm) | 130 |
| D33 | t (cm) | 3.5 |
| A36 | e (cm) | 1 |
| C36 | Dist (cm) | 130 |
| H51 | SI | 130 |
| B58 | Coef. Forma | 0.7 |
| C84 | b | 0.02 |
| C85 | CL | 0.2 |
| B140 | G (Kg/cm2) | 840000 |
| C258 | Número de pernos | 10 |

### Veredictos

- **D197** (cadena con #REF!) `=IF(#REF!<=#REF!,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
- **D198** (cadena con #REF!) `=IF(V192<=#REF!,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
  - V192 (Base tramo 2) = `=(S64+S65+C70)/T28` → 1.2943308309603934
- **D199** (cadena con #REF!) `=IF(V193<=#REF!,"OK! TRAMO No 3 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
  - V193 (Base tramo 3) = `=(S64+S65+S66+C70)/S32` → 0.804634695848085
- **D200** `=IF(B200<=F195,"OK! TRAMO CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO CUMPLE A LA COMPRESION
  - B200 (Base tramo) = `=0.75*(H74)/B44` → 11.036982084738694
  - F195 (Por lo tanto se tiene que la carga admisible a la ) = `=(G190/E193)/B44` → 40.38645173134493
- **D210** `=IF(B200+D221<=B210,"OK! SECCION CUMPLE ","PANDEO LOCAL. CAMBIAR SECCION")` → OK! SECCION CUMPLE 
  - B200 (Base tramo) = `=0.75*(H74)/B44` → 11.036982084738694
  - D221 (Tensión máxima en la base) = `=0.75*D96/D44` → 777.7377423675633
  - B210 () = `=IF(B208<=(240/SQRT(D12/70.35)),D12,IF(AND(B208>=240/SQRT(D12/70.35),B208<=385/SQRT(D12/70.35)),1.45*D12*(1-0.00129*SQRT(D12/70.35)*B208),108000*70.35/B208^2))` → 2400
- **F218** (cadena con #REF!) `=IF(U226<=B217,"OK! SECCION CUMPLE","f < Fy: CAMBIAR SECCION")` → #REF!
  - U226 (Tensiones en la base del primer tramo) = `=S83/V27` → #REF!
  - B217 (Fm) = `=0.66*D12` → 1584
- **F219** (cadena con #REF!) `=IF(U227<=B217,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → #REF!
  - U227 (Tensiones en la base del segundo tramo) = `=S84/V28` → #REF!
  - B217 (Fm) = `=0.66*D12` → 1584
- **F220** (cadena con #REF!) `=IF(U228<=B217,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → #REF!
  - U228 (Tensiones en la base del tercer tramo) = `=S85/U32` → #REF!
  - B217 (Fm) = `=0.66*D12` → 1584
- **F221** `=IF(D221<=B217,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D221 (Tensión máxima en la base) = `=0.75*D96/D44` → 777.7377423675633
  - B217 (Fm) = `=0.66*D12` → 1584
- **F233** `=IF(C233<=0.4*D12,"OK! SECCION CUMPLE"," CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - C233 (Tension de corte máxima:) = `=(E228+E227)*(B18/2)/B141` → 1.2357724516134663
- **F241** (cadena con #REF!) `=IF(M228>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M228 (Tramo 1) = `=U226/(B217)+((#REF!)/#REF!)` → #REF!
- **F242** (cadena con #REF!) `=IF(M229>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M229 (Tramo 2) = `=U227/(B217)+((V192)/#REF!)` → #REF!
- **F243** (cadena con #REF!) `=IF(M230>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M230 (Tramo 3) = `=U228/(B217)+((V193)/#REF!)` → #REF!
- **F244** `=IF(C244>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C244 (Tramo) = `=D221/(B217)+B200/F195` → 0.7642803220854429
- **C264** `=IF(AND(C261>10.4,C261<=12.3),"1 3/4",IF(AND(C261>12.3,C261<=14.3),"1 7/8",IF(AND(C261>14.3,C261<=16.1),"2",IF(AND(C261>16.1,C261<=21),"2 1/4",IF(AND(C261>21,C261<=25.8),"2 1/2",IF(C261>25.8,"Aumente número de pernos"," "))))))` →  
  - C261 (Area de tracción) = `=C260/(0.6*D12)` → 4.317523530686107
  - C261 (Area de tracción) = `=C260/(0.6*D12)` → 4.317523530686107
  - C261 (Area de tracción) = `=C260/(0.6*D12)` → 4.317523530686107
  - C261 (Area de tracción) = `=C260/(0.6*D12)` → 4.317523530686107
  - C261 (Area de tracción) = `=C260/(0.6*D12)` → 4.317523530686107
  - C261 (Area de tracción) = `=C260/(0.6*D12)` → 4.317523530686107
  - C261 (Area de tracción) = `=C260/(0.6*D12)` → 4.317523530686107
  - C261 (Area de tracción) = `=C260/(0.6*D12)` → 4.317523530686107
  - C261 (Area de tracción) = `=C260/(0.6*D12)` → 4.317523530686107
  - C261 (Area de tracción) = `=C260/(0.6*D12)` → 4.317523530686107
  - C261 (Area de tracción) = `=C260/(0.6*D12)` → 4.317523530686107

### Constantes escritas dentro de las fórmulas (valor: veces)

`2`: 173, `100`: 54, `4`: 52, `1`: 29, `3`: 22, `3.14159`: 15, `0.5`: 15, `6`: 14, `3.1415`: 10, `64`: 6, `32.595`: 6, `0.6`: 5, `70.35`: 5, `10000`: 4, `70`: 4, `0.00785`: 4, `3.91`: 4, `10.4`: 4, `7850`: 3, `126`: 3, `1.57`: 3, `50`: 3, `16`: 3, `0.75`: 3, `6.122`: 2, `3.31`: 2, `0.3772`: 2, `28.594`: 2, `0.2`: 2, `0.5756`: 2, `2.54`: 2, `2100000`: 2, `240`: 2, `0.37`: 2, `0.21`: 2, `0.92`: 2, `1.46`: 2, `2.15`: 2, `2.98`: 2, `4.92`: 2, `6.25`: 2, `7.45`: 2, `9.06`: 2, `12.3`: 2, `14.3`: 2, `16.1`: 2, `21`: 2, `25.8`: 2, `120`: 1, `0.63`: 1, `3.9`: 1, `14.22`: 1, `0.283`: 1, `0.356`: 1, `23`: 1, `12`: 1, `0.3826`: 1, `385`: 1, `1.45`: 1, `0.00129`: 1, `108000`: 1, `0.66`: 1, `0.4`: 1, `10`: 1, `5`: 1

## P.Var. Octogonal 2 ganchos

Fórmulas: 150. Veredictos: 15 (9 con `#REF!` en su cadena). Fórmulas con `#REF!`: 9 (S93, S94, S95, D207, D208, D209, M238, M239, M240)

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|
| D12 | Tension de Fluencia Fy (kg/cm2) | 2400 |
| S12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| T12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| U12 | Tension de Fluencia Fy (kg/cm2) | 0 |
| A15 | h (m) | 21 |
| K16 | Diámetro extremos del poste | 5 |
| L16 | Diámetro extremos del poste | 20 |
| M16 | Diámetro extremos del poste | 25 |
| A18 | d sup. (cm) | 25 |
| B18 | d base(cm) | 50 |
| K19 | Espesor del poste | 1 |
| L19 | Espesor del poste | 0.635 |
| M19 | Espesor del poste | 0.818 |
| A21 | e (cm) | 0.6 |
| A24 | P (Kg) | 125 |
| A27 | H (Kg) | 330 |
| E27 | Viento en el tablero | 0 |
| A33 | d (cm) | 20 |
| C33 | R (cm) | 130 |
| D33 | t (cm) | 3.5 |
| A36 | e (cm) | 1 |
| C36 | Dist (cm) | 130 |
| H61 | SI | 130 |
| B68 | Coef. Forma | 0.7 |
| C94 | b | 0.02 |
| C95 | CL | 0.2 |
| B150 | G (Kg/cm2) | 840000 |
| E237 | Momento torsional generado por viento en gancho: | 0 |
| C268 | Número de pernos | 4 |
| C269 | Diámetro (cm) | 105 |

### Veredictos

- **D207** (cadena con #REF!) `=IF(#REF!<=#REF!,"OK! TRAMO No 1 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
- **D208** (cadena con #REF!) `=IF(V202<=#REF!,"OK! TRAMO No 2 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
  - V202 (Base tramo 2) = `=(S74+S75+C80)/T28` → 6.471654154801967
- **D209** (cadena con #REF!) `=IF(V203<=#REF!,"OK! TRAMO No 3 CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → #REF!
  - V203 (Base tramo 3) = `=(S74+S75+S76+C80)/S32` → 4.023173479240425
- **D210** `=IF(B210<=F205,"OK! TRAMO CUMPLE A LA COMPRESION","POSTE NO CUMPLE A LA COMPRESION. CAMBIAR SECCION")` → OK! TRAMO CUMPLE A LA COMPRESION
  - B210 (Base tramo) = `=0.75*(H84)/B44` → 12.883883000742292
  - F205 (Por lo tanto se tiene que la carga admisible a la ) = `=(G200/E203)/B44` → 69.99068885271406
- **D220** `=IF(B210+D231<=B220,"OK! SECCION CUMPLE","PANDEO LOCAL. CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - B210 (Base tramo) = `=0.75*(H84)/B44` → 12.883883000742292
  - D231 (Tensión máxima en la base) = `=0.75*D106/D44` → 1252.2533203144314
  - B220 () = `=IF(B218<=(240/SQRT(D12/70.35)),D12,IF(AND(B218>=240/SQRT(D12/70.35),B218<=385/SQRT(D12/70.35)),1.45*D12*(1-0.00129*SQRT(D12/70.35)*B218),108000*70.35/B218^2))` → 2400
- **F228** (cadena con #REF!) `=IF(U236<=B227,"OK! SECCION CUMPLE","f < Fy: CAMBIAR SECCION")` → #REF!
  - U236 (Tensiones en la base del primer tramo) = `=S93/V27` → #REF!
  - B227 (Fm) = `=0.66*D12` → 1584
- **F229** (cadena con #REF!) `=IF(U237<=B227,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → #REF!
  - U237 (Tensiones en la base del segundo tramo) = `=S94/V28` → #REF!
  - B227 (Fm) = `=0.66*D12` → 1584
- **F230** (cadena con #REF!) `=IF(U238<=B227,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → #REF!
  - U238 (Tensiones en la base del tercer tramo) = `=S95/U32` → #REF!
  - B227 (Fm) = `=0.66*D12` → 1584
- **F231** `=IF(D231<=B227,"OK! SECCION CUMPLE","fm > Fm: CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - D231 (Tensión máxima en la base) = `=0.75*D106/D44` → 1252.2533203144314
  - B227 (Fm) = `=0.66*D12` → 1584
- **F243** `=IF(C243<=0.4*D12,"OK! SECCION CUMPLE"," CAMBIAR SECCION")` → OK! SECCION CUMPLE
  - C243 (Tension de corte máxima:) = `=(E238+E237)*(B18/2)/B151` → 4.3195892636764854e-05
- **F251** (cadena con #REF!) `=IF(M238>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M238 (Tramo 1) = `=U236/(B227)+((#REF!)/#REF!)` → #REF!
- **F252** (cadena con #REF!) `=IF(M239>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M239 (Tramo 2) = `=U237/(B227)+((V202)/#REF!)` → #REF!
- **F253** (cadena con #REF!) `=IF(M240>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → #REF!
  - M240 (Tramo 3) = `=U238/(B227)+((V203)/#REF!)` → #REF!
- **F254** `=IF(C254>=1,"INTERACCION > 1. NO CUMPLE","OK! SECCION CUMPLE")` → OK! SECCION CUMPLE
  - C254 (Tramo) = `=D231/(B227)+B210/F205` → 0.9746439219354716
- **C274** `=IF(AND(C271>10.4,C271<=12.3),"1 3/4",IF(AND(C271>12.3,C271<=14.3),"1 7/8",IF(AND(C271>14.3,C271<=16.1),"2",IF(AND(C271>16.1,C271<=21),"2 1/4",IF(AND(C271>21,C271<=25.8),"2 1/2",IF(C271>25.8,"Aumente número de pernos"," "))))))` → 1 3/4
  - C271 (Area de tracción) = `=C270/(0.6*D12)` → 12.278271254398952
  - C271 (Area de tracción) = `=C270/(0.6*D12)` → 12.278271254398952
  - C271 (Area de tracción) = `=C270/(0.6*D12)` → 12.278271254398952
  - C271 (Area de tracción) = `=C270/(0.6*D12)` → 12.278271254398952
  - C271 (Area de tracción) = `=C270/(0.6*D12)` → 12.278271254398952
  - C271 (Area de tracción) = `=C270/(0.6*D12)` → 12.278271254398952
  - C271 (Area de tracción) = `=C270/(0.6*D12)` → 12.278271254398952
  - C271 (Area de tracción) = `=C270/(0.6*D12)` → 12.278271254398952
  - C271 (Area de tracción) = `=C270/(0.6*D12)` → 12.278271254398952
  - C271 (Area de tracción) = `=C270/(0.6*D12)` → 12.278271254398952
  - C271 (Area de tracción) = `=C270/(0.6*D12)` → 12.278271254398952

### Constantes escritas dentro de las fórmulas (valor: veces)

`2`: 168, `100`: 53, `4`: 46, `1`: 29, `3`: 22, `3.14159`: 15, `0.5`: 15, `6`: 14, `64`: 6, `32.595`: 5, `70.35`: 5, `10000`: 4, `0.6`: 4, `70`: 4, `3.1415`: 4, `3.91`: 4, `10.4`: 4, `7850`: 3, `126`: 3, `50`: 3, `16`: 3, `0.75`: 3, `6.122`: 2, `3.31`: 2, `0.3772`: 2, `1.57`: 2, `0.00785`: 2, `0.2`: 2, `2.54`: 2, `2100000`: 2, `240`: 2, `0.21`: 2, `0.92`: 2, `1.46`: 2, `2.15`: 2, `2.98`: 2, `4.92`: 2, `6.25`: 2, `7.45`: 2, `9.06`: 2, `12.3`: 2, `14.3`: 2, `16.1`: 2, `21`: 2, `25.8`: 2, `120`: 1, `0.63`: 1, `28.594`: 1, `3.9`: 1, `14.22`: 1, `0.283`: 1, `0.356`: 1, `23`: 1, `12`: 1, `0.3826`: 1, `385`: 1, `1.45`: 1, `0.00129`: 1, `108000`: 1, `0.66`: 1, `0.37`: 1, `0.4`: 1, `5`: 1

## Datos

Fórmulas: 45. Veredictos: 0 (0 con `#REF!` en su cadena). Fórmulas con `#REF!`: 8 (Q3, R3, S3, T3, Q4, R4, S4, T4)

### Entradas de las que dependen los veredictos

| Celda | Rótulo | Valor guardado |
|---|---|---|

### Veredictos


### Constantes escritas dentro de las fórmulas (valor: veces)



## Normas y referencias citadas en el libro

- P.Recto Circ.!A46: =IF(E44="NO","      Nota: Las fuerzas equivalentes horizontales serán calculadas a partir de la Nch 432 of 72","      Nota: Las fuerzas equivalentes horizontale
- P.Recto Circ. 1 gancho!A46: =IF(E44="NO","      Nota: Las fuerzas equivalentes horizontales serán calculadas a partir de la Nch 432 of 72","      Nota: Las fuerzas equivalentes horizontale
- P.Recto Circ. 2 ganchos!A46: =IF(E44="NO","      Nota: Las fuerzas equivalentes horizontales serán calculadas a partir de la Nch 432 of 72","      Nota: Las fuerzas equivalentes horizontale
- P.Recto Cuad.!A48: =IF(E46="NO","      Nota: Las fuerzas equivalentes horizontales serán calculadas a partir de la Nch 432 of 72","      Nota: Las fuerzas equivalentes horizontale
- P.Recto Cuad. 1 gancho!A48: =IF(E46="NO","      Nota: Las fuerzas equivalentes horizontales serán calculadas a partir de la Nch 432 of 72","      Nota: Las fuerzas equivalentes horizontale
- P.Recto Cuad. 2 ganchos!A48: =IF(E46="NO","      Nota: Las fuerzas equivalentes horizontales serán calculadas a partir de la Nch 432 of 72","      Nota: Las fuerzas equivalentes horizontale
- P.Var. 2 Tramos Circ. 1 gancho!A46: =IF(E44="NO","      Nota: Las fuerzas equivalentes horizontales serán calculadas a partir de la Nch 432 of 72","      Nota: Las fuerzas equivalentes horizontale
- P.Var. 2 Tramos Circ. 2 ganchos!A46: =IF(E44="NO","      Nota: Las fuerzas equivalentes horizontales serán calculadas a partir de la Nch 432 of 72","      Nota: Las fuerzas equivalentes horizontale
- P.Var. Octogonal!A46: =IF(E44="NO","      Nota: Las fuerzas equivalentes horizontales serán calculadas a partir de la Nch 432 of 72","      Nota: Las fuerzas equivalentes horizontale
- P.Var. Octogonal 1 gancho!A53: =IF(E51="NO","      Nota: Las fuerzas equivalentes horizontales serán calculadas a partir de la Nch 432 of 72","      Nota: Las fuerzas equivalentes horizontale
- P.Var. Octogonal 2 ganchos!A63: =IF(E61="NO","      Nota: Las fuerzas equivalentes horizontales serán calculadas a partir de la Nch 432 of 72","      Nota: Las fuerzas equivalentes horizontale
- P.Var.2 Tramos Circ.!A46: =IF(E44="NO","      Nota: Las fuerzas equivalentes horizontales serán calculadas a partir de la Nch 432 of 72","      Nota: Las fuerzas equivalentes horizontale
- P.Var.3 Tramos Circ.!A46: =IF(E44="NO","      Nota: Las fuerzas equivalentes horizontales serán calculadas a partir de la Nch 432 of 72","      Nota: Las fuerzas equivalentes horizontale
- P.Var.3 Tramos Circ. 1 gancho!A46: =IF(E44="NO","      Nota: Las fuerzas equivalentes horizontales serán calculadas a partir de la Nch 432 of 72","      Nota: Las fuerzas equivalentes horizontale
- P.Var.3 Tramos Circ. 2 ganchos!A46: =IF(E44="NO","      Nota: Las fuerzas equivalentes horizontales serán calculadas a partir de la Nch 432 of 72","      Nota: Las fuerzas equivalentes horizontale
- P.Var.4 Tramos Circ.!A46: =IF(E44="NO","      Nota: Las fuerzas equivalentes horizontales serán calculadas a partir de la Nch 432 of 72","      Nota: Las fuerzas equivalentes horizontale
- P.Var.4 Tramos Circ. 1 gancho!A46: =IF(E44="NO","      Nota: Las fuerzas equivalentes horizontales serán calculadas a partir de la Nch 432 of 72","      Nota: Las fuerzas equivalentes horizontale
- P.Var.4 Tramos Circ. 2 ganchos!A46: =IF(E44="NO","      Nota: Las fuerzas equivalentes horizontales serán calculadas a partir de la Nch 432 of 72","      Nota: Las fuerzas equivalentes horizontale
