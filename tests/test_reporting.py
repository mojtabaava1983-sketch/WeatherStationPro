from reporting import ReportingService, ReportFilter, DEFAULT_REPORTS

def test_catalog_has_core_reports():
    ids = {item.report_id for item in DEFAULT_REPORTS}
    assert {"current_weather", "weather_history", "forecast", "sun_times"} <= ids

def test_current_weather_report():
    service = ReportingService()
    result = service.build(
        "current_weather",
        [{
            "CityID": 1,
            "CityName": "Tehran",
            "ObservationUTC": "2026-08-13T10:00:00+00:00",
            "Temperature": 31.5,
            "Humidity": 40,
            "Pressure": 1012,
            "WindSpeed": 5,
            "CloudCover": 10,
            "Visibility": 10000,
            "DataQuality": 100,
        }],
    )
    assert result.row_count == 1
    assert result.rows[0]["City"] == "Tehran"
    assert result.rows[0]["Temperature"] == 31.5

def test_city_filter():
    service = ReportingService()
    rows = [
        {"CityID": 1, "CityName": "A"},
        {"CityID": 2, "CityName": "B"},
    ]
    result = service.build("current_weather", rows, ReportFilter(city_id=2))
    assert result.row_count == 1
    assert result.rows[0]["City"] == "B"
