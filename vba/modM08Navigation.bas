Attribute VB_Name = "modM08Navigation"
Option Compare Database
Option Explicit

Public Sub OpenWeatherDashboard()
    DoCmd.OpenForm FORM_DASHBOARD
End Sub

Public Sub OpenCityManager()
    DoCmd.OpenForm FORM_CITY
End Sub

Public Sub OpenForecast()
    DoCmd.OpenForm FORM_FORECAST
End Sub

Public Sub OpenSunTimes()
    DoCmd.OpenForm FORM_SUN
End Sub

Public Sub OpenReports()
    DoCmd.OpenForm FORM_REPORTS
End Sub

Public Sub CloseApplication()
    DoCmd.Quit acQuitSaveNone
End Sub
