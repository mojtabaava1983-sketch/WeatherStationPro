Attribute VB_Name = "modM08Dashboard"
Option Compare Database
Option Explicit

Public Sub RefreshDashboard()
    On Error GoTo Failed

    DoCmd.Hourglass True
    Forms!frmWeatherDashboard.Requery
    DoCmd.Hourglass False

    MsgBox "Weather dashboard refreshed.", _
           vbInformation, "WeatherStation Pro"
    Exit Sub

Failed:
    DoCmd.Hourglass False
    MsgBox "Dashboard refresh failed: " & Err.Description, _
           vbExclamation, "WeatherStation Pro"
End Sub

Public Sub ClearDashboardSelection()
    On Error Resume Next
    Forms!frmWeatherDashboard!cboCity = Null
    Forms!frmWeatherDashboard!txtTemperature = "—"
    Forms!frmWeatherDashboard!txtHumidity = "—"
    Forms!frmWeatherDashboard!txtPressure = "—"
    Forms!frmWeatherDashboard!txtWindSpeed = "—"
End Sub
