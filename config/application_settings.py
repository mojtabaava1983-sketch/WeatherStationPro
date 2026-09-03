"""M02-05 Application Settings."""
from __future__ import annotations
from dataclasses import dataclass


class ApplicationSettingsError(ValueError):
    pass


@dataclass(frozen=True)
class ApplicationSettings:
    application_name: str = "WeatherStationPro"
    environment: str = "development"
    timezone: str = "UTC"
    language: str = "en"
    logging_level: str = "INFO"
    enabled: bool = True
    data_retention_days: int = 30

    def validate(self) -> None:
        if not self.application_name.strip():
            raise ApplicationSettingsError("application_name cannot be empty.")
        if not self.environment.strip():
            raise ApplicationSettingsError("environment cannot be empty.")
        if not self.timezone.strip():
            raise ApplicationSettingsError("timezone cannot be empty.")
        if self.logging_level.upper() not in {"DEBUG","INFO","WARNING","ERROR","CRITICAL"}:
            raise ApplicationSettingsError("Invalid logging_level.")
        if self.data_retention_days < 0:
            raise ApplicationSettingsError("data_retention_days cannot be negative.")

    def to_dict(self) -> dict:
        return {
            "application_name": self.application_name,
            "environment": self.environment,
            "timezone": self.timezone,
            "language": self.language,
            "logging_level": self.logging_level,
            "enabled": self.enabled,
            "data_retention_days": self.data_retention_days,
        }

    @classmethod
    def from_dict(cls, values: dict) -> "ApplicationSettings":
        allowed = {
            k: values[k] for k in cls.__dataclass_fields__ if k in values
        }
        obj = cls(**allowed)
        obj.validate()
        return obj
