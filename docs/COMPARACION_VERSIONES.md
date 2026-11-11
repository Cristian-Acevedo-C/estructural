# Comparación volcado_A_2026-10-16 → volcado_B_2026-10-21

## Hojas

- Solo en A: ['Precios']
- Solo en B: ['CAÑERIAS']
- Orden A: ['INICIO', 'CUBICACIONES', 'P.Recto Circ.', 'P.Recto Cuad.', 'P.Var.2 Tramos Circ.', 'P.Var.3 Tramos Circ.', 'P.Var.4 Tramos Circ.', 'P.Recto Circ. 1 gancho', 'P.Recto Cuad. 1 gancho', 'P.Var. 2 Tramos Circ. 1 gancho', 'P.Var.3 Tramos Circ. 1 gancho', 'P.Var.4 Tramos Circ. 1 gancho', 'P.Recto Circ. 2 ganchos', 'P.Recto Cuad. 2 ganchos', 'P.Var. 2 Tramos Circ. 2 ganchos', 'P.Var.3 Tramos Circ. 2 ganchos', 'P.Var.4 Tramos Circ. 2 ganchos', 'P.Var. Octogonal', 'P.Var. Octogonal 1 gancho', 'P.Var. Octogonal 2 ganchos', 'Precios', 'Datos']
- Orden B: ['INICIO', 'CUBICACIONES', 'CAÑERIAS', 'P.Recto Circ.', 'P.Var.2 Tramos Circ.', 'P.Var.3 Tramos Circ.', 'P.Var.4 Tramos Circ.', 'P.Recto Circ. 1 gancho', 'P.Var. 2 Tramos Circ. 1 gancho', 'P.Var.3 Tramos Circ. 1 gancho', 'P.Var.4 Tramos Circ. 1 gancho', 'P.Recto Cuad.', 'P.Recto Circ. 2 ganchos', 'P.Recto Cuad. 1 gancho', 'P.Recto Cuad. 2 ganchos', 'P.Var. 2 Tramos Circ. 2 ganchos', 'P.Var.3 Tramos Circ. 2 ganchos', 'P.Var.4 Tramos Circ. 2 ganchos', 'P.Var. Octogonal', 'P.Var. Octogonal 1 gancho', 'P.Var. Octogonal 2 ganchos', 'Datos']

## Fórmulas distintas (hojas comunes)

- `Datos`!Q3: A `=INDEX(Precios!C4:C12,Q2)` → B `=INDEX(#REF!,Q2)`
- `Datos`!Q4: A `=INDEX(Precios!C18:C29,Q2)` → B `=INDEX(#REF!,Q2)`
- `Datos`!R3: A `=INDEX(Precios!D4:D12,Q2)` → B `=INDEX(#REF!,Q2)`
- `Datos`!R4: A `=INDEX(Precios!D18:D29,Q2)` → B `=INDEX(#REF!,Q2)`
- `Datos`!S3: A `=INDEX(Precios!F4:F12,Q2)` → B `=INDEX(#REF!,Q2)`
- `Datos`!S4: A `=INDEX(Precios!F18:F29,Q2)` → B `=INDEX(#REF!,Q2)`
- `Datos`!T3: A `=INDEX(Precios!G4:G12,Q2)` → B `=INDEX(#REF!,Q2)`
- `Datos`!T4: A `=INDEX(Precios!G18:G29,Q2)` → B `=INDEX(#REF!,Q2)`

## Constantes distintas (hojas comunes): en su mayoría, los datos de la última configuración que quedó cargada

- `P.Recto Circ.` (8): A15: 6 → 4; A18: 8.9 → 11.4; A21: 0.3 → 0.36; A24: 0.5 → 70; A27: 20 → 80; C278: 700 → 2000; D146: 10 → 530; D147: 26 → 110
- `P.Var.3 Tramos Circ.` (12): A15: 0.6 → 1.5; A18: 11.4 → 32.3; A21: 0.305 → 0.635; B15: 5.4 → 6; B18: 16.83 → 27.305; B21: 0.34 → 0.5; C18: 21.9 → 32.3; C21: 0.478 → 0.635; C24: 110 → 250; C27: 133 → 120; D146: 228 → 150; D147: 472 → 200
- `P.Var.4 Tramos Circ.` (15): A18: 11.4 → 11.43; A21: 0.602 → 0.36; B15: 2.7 → 3.3; B21: 0.655 → 0.5; C15: 2.7 → 6; C21: 0.635 → 0.5; C291: 800 → 750; C297: 6 → 4; D147: 100 → 15; D148: 150 → 5; D18: 21.907 → 21.9; D21: 0.635 → 0.478; D24: 75 → 25; D27: 105 → 50; H44: 140 → 120
- `P.Recto Circ. 1 gancho` (11): A15: 6 → 5.89; A18: 25 → 114.3; A21: 0.952 → 3.05; A24: 50 → 15; C275: 500 → 800; C281: 10 → 6; D15: 20 → 88.9; D18: 1 → 4; D21: 130 → 150; D24: 130 → 400; H44: 130 → 150
- `P.Var. 2 Tramos Circ. 1 gancho` (10): A15: 6 → 1.8; A18: 11.53 → 14.13; A21: 0.534 → 6.35; A24: 50 → 100; B18: 16.8 → 127; B21: 0.5 → 4; D18: 20 → 11.4; D21: 1 → 4; D24: 130 → 150; D27: 100 → 400
- `P.Var. Octogonal` (8): A15: 9 → 20; A18: 6.2 → 20; A21: 3 → 0.5; A24: 150 → 300; A27: 70 → 1120; B18: 16.8 → 50; C259: 4 → 16; D144: 100 → 200
- `Datos` (7): E24: 0.6 → 1.5; E25: 5.4 → 6; F25: 2.7 → 3.3; F26: 2.7 → 6; G24: 6 → 5.89; I24: 6 → 1.8; Q24: 9 → 20

## VBA: 127 líneas de diferencia (diff unificado)

```diff
--- A/vba.txt
+++ B/vba.txt
@@ -589,28 +589,40 @@
 
-' ===== módulo: Hoja21.cls =====
-Attribute VB_Name = "Hoja21"
-
-Attribute VB_Base = "0{00020820-0000-0000-C000-000000000046}"
-
-Attribute VB_GlobalNameSpace = False
-
-Attribute VB_Creatable = False
-
-Attribute VB_PredeclaredId = True
-
-Attribute VB_Exposed = True
-
-Attribute VB_TemplateDerived = False
-
-Attribute VB_Customizable = True
-
-
-
-
-
-
-
-
-
-
+' ===== módulo: ABOUT1.frm =====
+Attribute VB_Name = "ABOUT1"
+
+Attribute VB_Base = "0{C9F93791-A81A-47DC-A1FB-09D9AA5F051E}{DBF09258-40B1-4884-96D7-6441F466BD44}"
+
+Attribute VB_GlobalNameSpace = False
+
+Attribute VB_Creatable = False
+
+Attribute VB_PredeclaredId = True
+
+Attribute VB_Exposed = False
+
+Attribute VB_TemplateDerived = False
+
+Attribute VB_Customizable = False
+
+
+
+
+
+
+
+
+
+
+
+Private Sub OK_Click()
+
+Unload ABOUT1
+
+Load UserForm1
+
+UserForm1.Show
+
+
+
+End Sub
 
@@ -621,3 +633,3 @@
 
-Attribute VB_Base = "0{E4E4D2A9-9A23-471E-82A6-06863D92761B}{771930B4-2D55-4976-A119-6D535EA05313}"
+Attribute VB_Base = "0{F35092B9-A858-4812-B302-BC3272AE16AF}{628604D9-F089-49A2-8140-F054DCCAD7FC}"
 
@@ -1180,3 +1192,3 @@
 
-Attribute VB_Base = "0{1B496EB7-FD53-4B72-8976-B3B7E51EDC9A}{6A75B2D4-ECFE-4A8F-87DF-FA4584DD0B2F}"
+Attribute VB_Base = "0{8F1DAC2C-4511-4BCE-84B7-11788F463C6C}{47EEA6EB-7DE1-4CC7-A4E6-46D2A5602D31}"
 
@@ -1379,3 +1391,3 @@
 
-Attribute VB_Base = "0{50B12F0B-60D5-4CFF-BF1D-74C774EC88DC}{23ED9126-58E9-4C9C-999D-F8E754CD7F2B}"
+Attribute VB_Base = "0{C2C6CF5E-F610-4834-9FE5-EB5048ECBB10}{3B99C236-9C60-4B3E-95E9-27037835F775}"
 
@@ -1856,42 +1868 @@
 
-
-' ===== módulo: ABOUT1.frm =====
-Attribute VB_Name = "ABOUT1"
-
-Attribute VB_Base = "0{C3DBCC0B-07A9-4AE0-B576-1CEC457F8DDD}{EBC3D010-8C1D-467E-8E85-B4563A3C29E5}"
-
-Attribute VB_GlobalNameSpace = False
-
-Attribute VB_Creatable = False
-
-Attribute VB_PredeclaredId = True
-
-Attribute VB_Exposed = False
-
-Attribute VB_TemplateDerived = False
-
-Attribute VB_Customizable = False
-
-
-
-
-
-
-
-
-
-
-
-Private Sub OK_Click()
-
-Unload ABOUT1
-
-Load UserForm1
-
-UserForm1.Show
-
-
-
-End Sub
-
-
```
