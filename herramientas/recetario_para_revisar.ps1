# Fase 6 · copia del recetario PARA REVISAR: no cambia ningún valor ni fórmula.
# Marca en naranja las celdas dudosas, les agrega una nota y crea la hoja "REVISAR" con la lista.
# Uso: pwsh herramientas/recetario_para_revisar.ps1   (necesita Excel). INTERNO: el recetario trae precios y costos.
$ErrorActionPreference = 'Stop'
$raiz = Split-Path $PSScriptRoot -Parent
$origen = Join-Path $raiz 'insumos\recetario_2026-11-11.xlsx'
$dir = Join-Path (Split-Path $raiz -Parent) 'insumos\interno_NO_PUBLICAR\recetario_revision'
New-Item -ItemType Directory -Force $dir | Out-Null
$dest = Join-Path $dir 'RECETARIO_para_revisar_2026-11-11.xlsx'
if (Test-Path $dest) { Set-ItemProperty $dest IsReadOnly $false; Remove-Item $dest -Force }
Copy-Item $origen $dest; Set-ItemProperty $dest IsReadOnly $false

# hoja, celdas a marcar, qué dice, observación, propuesta (HIPÓTESIS)
$H = @(
  @('RECETARIO','D11','ISO R65 1" con Ø26,67','Es el mismo diámetro de la cañería de 3/4" (fila 7). El peso 1,98 kg/m corresponde a Ø33,4, que es lo que trae el catálogo maestro.','Ø33,4'),
  @('RECETARIO','B43:E43','ASTM A53 2" Ø60,32 × 3,91','Fila repetida: es igual a la fila 39.','Eliminar una o corregir el espesor si era otra cañería'),
  @('RECETARIO','D47','ASTM A53 2 1/2" con Ø73,02','El catálogo maestro dice Ø76,1 con el mismo espesor y peso. Ø73,02 es la medida nominal ASTM de 2 1/2".','Definir cuál vale y dejar la misma en ambos archivos'),
  @('RECETARIO','D87,D91,D95,D99','ASTM A53 10" con Ø273,5','El catálogo maestro dice Ø273,05 con los mismos espesores y pesos. La medida nominal ASTM es 273,05.','Ø273,05'),
  @('RECETARIO','N95','ASTM A53 10" × 7,92: 278,94 kg por barra (46,49 kg/m)','El peso teórico de Ø273 × 7,92 es 51,9 kg/m: el del recetario es 10 % menor. El catálogo maestro trae el mismo 46,49.','Revisar el peso con la tabla del proveedor'),
  @('RECETARIO','C159,C163','ASTM A53 "22"" con Ø610','Ø610 mm corresponde a 24". Las filas 151 y 155 ya son 22" (Ø558,8).','24"'),
  @('RECETARIO','N179','Tubo 1" Ø25,4 × 2: 6,09 kg por barra (1,015 kg/m)','El peso teórico de Ø25,4 × 2 es 1,15 kg/m: el del recetario es 12 % menor.','Revisar el peso'),
  @('RECETARIO','D191,E191','Tubo 1 3/4" con Ø1,5 y espesor 2','Diámetro imposible. 1 3/4" son 44,45 mm. El peso 1,59 kg/m calza con Ø44,45 × 1,5: el espesor quedó en la columna del diámetro.','Ø44,45 y espesor 1,5'),
  @('RECETARIO','D195','Tubo 1 3/4" con Ø2,5 y espesor 2','Diámetro imposible. El peso 2,09 kg/m calza con Ø44,45 × 2.','Ø44,45'),
  @('RECETARIO','E211,N211','Tubo 2 1/2" Ø63,5 × 2,5: 18,18 kg por barra (3,03 kg/m)','El peso 3,03 kg/m calza con espesor 2,0. Con espesor 2,5 serían 3,76 kg/m.','Espesor 2,0, o peso 22,6 kg por barra si el espesor es 2,5'),
  @('TUBULARES','C7','TTUB3A: tramo "58,8*2*3000"','El título del bloque dice 2" (50,8*2). No existe tubo de Ø58,8 en la hoja RECETARIO.','50,8*2*3000'),
  @('TUBULARES','H213','Tramo "114.3*3*6000" (bloque 4"(6000) 2"(1200))','Espesor 3: la cañería de 4" de la hoja RECETARIO es de 3,6 (ISO R65) o 6,02 (ASTM A53).','114,3*3,6*6000'),
  @('TUBULARES','R278','Tramo "114,6*3,6*1500"','Ø114,6 no existe: la cañería de 4" es Ø114,3.','114,3*3,6*1500'),
  @('TUBULARES','','336 celdas con error (en rojo)','Las fórmulas apuntan a otro libro que ya no está vinculado. No hay peso ni costo válido en esas recetas. En el archivo original (Google Sheets) estas celdas muestran #ERROR!. Al abrirlo en Excel muestran 0 o un total incompleto, que NO es un dato válido: en esta copia están pintadas de rojo.','Volver a vincular o reemplazar la fórmula'),
  @('BRAZOS RECTOS','','288 celdas con error (en rojo)','Las fórmulas apuntan a otro libro (por ejemplo [1]Hoja1!F27). Ningún brazo tiene peso ni costo válido. En el archivo original (Google Sheets) estas celdas muestran #ERROR!. Al abrirlo en Excel muestran 0 o un total incompleto, que NO es un dato válido: en esta copia están pintadas de rojo.','Volver a vincular o reemplazar la fórmula'),
  @('GANCHOS CURVOS','','68 celdas con error (en rojo)','Dependen de las celdas con error de BRAZOS RECTOS. En el archivo original (Google Sheets) estas celdas muestran #ERROR!. Al abrirlo en Excel muestran 0 o un total incompleto, que NO es un dato válido: en esta copia están pintadas de rojo.','Se corrige al corregir BRAZOS RECTOS'),
  @('TUBULARES','','49 recetas TTUB / ITUB','Los tramos no coinciden con los planos REV. M (3Ma a 12Mb). Ejemplo: 9 m = 3.000 + 2.500 + 2.500 + 1.600 aquí y 3.000 + 2.800 + 2.800 + 400 en el plano 9Ma.','Definir cuál es la receta vigente'),
  @('LUMINARIAS','','Luminarias con código y nombre','No traen peso ni área al viento. Sin esos datos no se puede verificar un poste para una luminaria concreta.','Agregar peso (kg) y área al viento (m²) de cada ficha')
)
$naranja = 42495   # RGB(255,165,0)
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false; $xl.DisplayAlerts = $false; $xl.AutomationSecurity = 3; $xl.EnableEvents = $false
$wb = $null
try {
  $wb = $xl.Workbooks.Open($dest, 0, $false)
  $xl.Calculation = -4135   # manual: no recalcular nada
  $rev = $wb.Worksheets.Add($wb.Worksheets.Item(1))
  $rev.Name = 'REVISAR'
  $rev.Range('A1').Value2 = 'RECETARIO · puntos por revisar (11-11-2026)'
  $rev.Range('A2').Value2 = 'Copia para revisión: no se cambió ningún valor ni fórmula. Las celdas dudosas están en naranja y tienen una nota. Las propuestas son hipótesis: confirmar antes de corregir el recetario original.'
  $enc = 'N°','Hoja','Celda','Qué dice','Observación','Propuesta (hipótesis)','Respuesta ORBE'
  for ($j = 0; $j -lt $enc.Count; $j++) { $rev.Range("$([char](65 + $j))4").Value2 = [string]$enc[$j] }
  $f = 5; $n = 1
  foreach ($item in $H) {
    $hoja, $celdas, $dice, $obs, $prop = $item
    $ws = $wb.Worksheets.Item($hoja)
    $rev.Range("A$f").Value2 = [double]$n; $rev.Range("B$f").Value2 = [string]$hoja
    $rev.Range("D$f").Value2 = [string]$dice; $rev.Range("E$f").Value2 = [string]$obs; $rev.Range("F$f").Value2 = [string]$prop
    if ($celdas) {
      $rg = $ws.Range($celdas.Replace(",", [string]$xl.International(5)))  # separador de lista según la configuración regional
      $rg.Interior.Color = $naranja
      $primera = $rg.Areas.Item(1).Cells.Item(1, 1)
      $nota = "REVISAR N° $n`n$obs`nPropuesta (hipótesis): $prop"
      if ($primera.Comment) { $primera.Comment.Delete() }
      $c = $primera.AddComment($nota); $c.Shape.TextFrame.AutoSize = $true
      $dir1 = $primera.Address($false, $false)
      [void]$rev.Hyperlinks.Add($rev.Range("C$f"), '', "'$hoja'!$dir1", '', $celdas)
    } else { $rev.Range("C$f").Value2 = '(toda la hoja)' }
    $f++; $n++
  }
  $rev.Range('A1').Font.Bold = $true; $rev.Range('A1').Font.Size = 14
  $rev.Range('A4:G4').Font.Bold = $true; $rev.Range('A4:G4').Interior.Color = 14277081
  $rev.Columns.Item([int]1).ColumnWidth = 5; $rev.Columns.Item([int]2).ColumnWidth = 18; $rev.Columns.Item([int]3).ColumnWidth = 16
  $rev.Columns.Item([int]4).ColumnWidth = 42; $rev.Columns.Item([int]5).ColumnWidth = 70; $rev.Columns.Item([int]6).ColumnWidth = 44; $rev.Columns.Item([int]7).ColumnWidth = 30
  $tabla = $rev.Range("A4:G$($f - 1)")
  $tabla.WrapText = $true; $tabla.VerticalAlignment = -4160; $tabla.Borders.LineStyle = 1
  $rev.Range('A2:G2').Merge(); $rev.Range('A2').WrapText = $true; $rev.Rows.Item(2).RowHeight = 32
  # celdas que en el original muestran #ERROR! (lista de trabajo/fase6/celdas_error_recetario.json): en rojo,
  # porque Excel las recalcula como 0 o como totales incompletos y el error deja de verse
  $rojo = 13551615   # RGB(255,199,206)
  $sep = [string]$xl.International(5)
  $errores = Get-Content (Join-Path $raiz 'trabajo/fase6/celdas_error_recetario.json') -Raw | ConvertFrom-Json
  $pintadas = 0
  foreach ($p in $errores.PSObject.Properties) {
    $ws = $wb.Worksheets.Item($p.Name); $lista = @($p.Value)
    for ($i = 0; $i -lt $lista.Count; $i += 25) {
      $grupo = $lista[$i..([Math]::Min($i + 24, $lista.Count - 1))]
      $ws.Range($grupo -join $sep).Interior.Color = $rojo; $pintadas += $grupo.Count
    }
    $ws.Tab.Color = $rojo
  }
  "Celdas con error pintadas: $pintadas"
  $rev.Tab.Color = $naranja
  $rev.Activate(); $rev.Range('A1').Select() | Out-Null
  $wb.Save()
  "Puntos: $($n - 1)"
} finally {
  if ($wb) { $wb.Close($false) }
  $xl.Quit(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($xl)
}
"Guardado: $dest"
