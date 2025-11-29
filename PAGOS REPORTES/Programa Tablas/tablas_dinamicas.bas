Attribute VB_Name = "Módulo1"
Sub CrearTablasDinamicas()

    Dim wsDatos As Worksheet
    Dim wsPivot As Worksheet
    Dim tblRng As Range
    Dim pvtCache As PivotCache
    Dim pvtTbl1 As PivotTable, pvtTbl2 As PivotTable
    Dim ultFila As Long, ultCol As Long
    Dim campoValor As String
    
    ' Nombre limpio del campo
    campoValor = "Recuperación por Gestión"
    
    ' Referencia a la hoja con los datos
    Set wsDatos = ActiveSheet
    
    ' Crear nueva hoja para las tablas dinámicas
    On Error Resume Next
    Application.DisplayAlerts = False
    ThisWorkbook.Sheets("Tablas_Dinamicas").Delete
    Application.DisplayAlerts = True
    On Error GoTo 0
    
    Set wsPivot = ThisWorkbook.Sheets.Add
    wsPivot.Name = "Tablas_Dinamicas"
    
    ' Rango de datos
    ultFila = wsDatos.Cells(wsDatos.Rows.Count, 1).End(xlUp).Row
    ultCol = wsDatos.Cells(1, wsDatos.Columns.Count).End(xlToLeft).Column
    Set tblRng = wsDatos.Range(wsDatos.Cells(1, 1), wsDatos.Cells(ultFila, ultCol))
    
    ' Crear caché para tablas dinámicas
    Set pvtCache = ThisWorkbook.PivotCaches.Create(SourceType:=xlDatabase, SourceData:=tblRng)
    
    ' ==============================
    ' PRIMERA TABLA DINÁMICA
    ' ==============================
    Set pvtTbl1 = pvtCache.CreatePivotTable(TableDestination:=wsPivot.Range("B3"), TableName:="TablaDinamica1")
    
    With pvtTbl1
        .ClearAllFilters
        .PivotFields("Campaña").Orientation = xlPageField
        .PivotFields("Segmento").Orientation = xlRowField
        With .PivotFields(campoValor)
            .Orientation = xlDataField
            .Function = xlSum
            .NumberFormat = "#,##0.00"
        End With
        .TableStyle2 = "PivotStyleMedium6"
    End With
    
    ' ==============================
    ' SEGUNDA TABLA DINÁMICA
    ' ==============================
    ' Colocar la segunda tabla más abajo (20 filas después de la primera para que no se empalme)
    Set pvtTbl2 = pvtCache.CreatePivotTable(TableDestination:=wsPivot.Range("G3"), TableName:="TablaDinamica2")
    
    With pvtTbl2
        .ClearAllFilters
        .PivotFields("Campaña").Orientation = xlPageField
        .PivotFields("Producto").Orientation = xlRowField
        With .PivotFields(campoValor)
            .Orientation = xlDataField
            .Function = xlSum
            .NumberFormat = "#,##0.00"
        End With
        .TableStyle2 = "PivotStyleMedium6"
    End With

End Sub

