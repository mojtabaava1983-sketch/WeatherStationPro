Attribute VB_Name = "modM08Startup"
Option Compare Database
Option Explicit

Public Function M08Startup() As Boolean
    On Error GoTo Failed

    If Not M08HealthCheck() Then GoTo Failed

    DoCmd.OpenForm STARTUP_FORM
    M08Startup = True
    Exit Function

Failed:
    MsgBox "M08 startup failed: " & Err.Description, _
           vbCritical, "WeatherStation Pro"
    M08Startup = False
End Function
