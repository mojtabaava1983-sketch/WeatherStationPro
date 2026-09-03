Attribute VB_Name = "modM08Utilities"
Option Compare Database
Option Explicit

Public Function DisplayValue(ByVal value As Variant, _
                              Optional ByVal unitText As String = "") As String
    If IsNull(value) Or IsEmpty(value) Then
        DisplayValue = "—"
    ElseIf IsNumeric(value) Then
        DisplayValue = Format(CDbl(value), "0.0") & unitText
    Else
        DisplayValue = CStr(value) & unitText
    End If
End Function

Public Function DisplayInteger(ByVal value As Variant) As String
    If IsNull(value) Or IsEmpty(value) Then
        DisplayInteger = "—"
    ElseIf IsNumeric(value) Then
        DisplayInteger = Format(CDbl(value), "0")
    Else
        DisplayInteger = CStr(value)
    End If
End Function

Public Function M08HealthCheck() As Boolean
    On Error GoTo Failed
    CurrentDb.TableDefs.Refresh
    M08HealthCheck = True
    Exit Function
Failed:
    M08HealthCheck = False
End Function
