"""WeatherStation Pro - M01-Final-10
Provider-independent observation mapping and safe field extraction.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Mapping

@dataclass
class MappedObservation:
    """Normalized observation ready for the persistence service."""
    temperature: Any = None
    humidity: Any = None
    wind_speed: Any = None
    pressure: Any = None
    precipitation: Any = None
    cloud_cover: Any = None
    visibility: Any = None
    uv_index: Any = None
    weather_description: Any = None
    sunrise: Any = None
    sunset: Any = None
    observed_utc: Any = None
    extras: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "Temperature": self.temperature,
            "Humidity": self.humidity,
            "WindSpeed": self.wind_speed,
            "Pressure": self.pressure,
            "Precipitation": self.precipitation,
            "CloudCover": self.cloud_cover,
            "Visibility": self.visibility,
            "UVIndex": self.uv_index,
            "WeatherDescription": self.weather_description,
            "Sunrise": self.sunrise,
            "Sunset": self.sunset,
            "ObservedUTC": self.observed_utc,
            **self.extras,
        }

class ObservationMapper:
    """Extracts known fields without failing on missing provider fields."""

    FIELD_ALIASES = {
        "temperature": ("temperature","temp","Temperature"),
        "humidity": ("humidity","Humidity"),
        "wind_speed": ("wind_speed","windSpeed","windspeed","WindSpeed"),
        "pressure": ("pressure","Pressure"),
        "precipitation": ("precipitation","rain","Precipitation"),
        "cloud_cover": ("cloud_cover","cloudCover","CloudCover"),
        "visibility": ("visibility","Visibility"),
        "uv_index": ("uv_index","uvIndex","UVIndex"),
        "weather_description": (
            "weather_description","description","WeatherDescription"
        ),
        "sunrise": ("sunrise","Sunrise"),
        "sunset": ("sunset","Sunset"),
        "observed_utc": ("observed_utc","observedUTC","ObservedUTC"),
    }

    @classmethod
    def _get(cls, data: Mapping[str, Any], aliases: tuple[str,...]) -> Any:
        for key in aliases:
            if key in data:
                return data[key]
        return None

    @classmethod
    def map(cls, data: Mapping[str, Any]) -> MappedObservation:
        known_keys=set()
        kwargs={}
        for target, aliases in cls.FIELD_ALIASES.items():
            kwargs[target]=cls._get(data,aliases)
            known_keys.update(aliases)

        extras={k:v for k,v in data.items() if k not in known_keys}
        return MappedObservation(**kwargs,extras=extras)

    @classmethod
    def required_fields_present(cls, observation: MappedObservation) -> bool:
        return (
            observation.temperature is not None
            and observation.humidity is not None
        )
