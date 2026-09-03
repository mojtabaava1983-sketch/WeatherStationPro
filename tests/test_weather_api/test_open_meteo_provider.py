from weather_api.providers.open_meteo import OpenMeteoProvider
from weather_api.models import ProviderResponse


def test_build_request():
    provider = OpenMeteoProvider()

    request = provider.build_request({
        "latitude": 40.4093,
        "longitude": 49.8671,
    })

    assert request.method == "GET"
    assert request.url == provider.BASE_URL
    assert request.params["latitude"] == 40.4093
    assert request.params["longitude"] == 49.8671
    assert "temperature_2m" in request.params["current"]


def test_build_request_requires_coordinates():
    provider = OpenMeteoProvider()

    try:
        provider.build_request({"latitude": 40.4093})
        assert False
    except ValueError:
        pass


def test_normalize():
    provider = OpenMeteoProvider()

    response = ProviderResponse(
        provider="open-meteo",
        status_code=200,
        url="https://api.open-meteo.com/v1/forecast",
        data={
            "latitude": 40.4093,
            "longitude": 49.8671,
            "timezone": "UTC",
            "current": {
                "time": "2026-08-30T08:00",
                "temperature_2m": 31.5,
                "relative_humidity_2m": 42,
                "apparent_temperature": 33.0,
                "precipitation": 0.0,
                "rain": 0.0,
                "showers": 0.0,
                "snowfall": 0.0,
                "weather_code": 1,
                "cloud_cover": 10,
                "surface_pressure": 1008.2,
                "wind_speed_10m": 14.4,
                "wind_direction_10m": 120,
                "wind_gusts_10m": 21.6,
            },
        },
    )

    observation = provider.normalize(response)

    assert observation.temperature == 31.5
    assert observation.humidity == 42
    assert observation.wind_speed == 14.4
    assert observation.pressure == 1008.2
    assert observation.precipitation == 0.0
    assert observation.observed_utc == "2026-08-30T08:00"
    assert observation.extras["WeatherCode"] == 1
