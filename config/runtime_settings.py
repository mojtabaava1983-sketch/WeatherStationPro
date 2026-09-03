"""M02-07 Runtime Settings."""
from __future__ import annotations
from dataclasses import dataclass


class RuntimeSettingsError(ValueError):
    pass


@dataclass(frozen=True)
class RuntimeSettings:
    request_timeout_seconds: float = 15.0
    retry_count: int = 2
    retry_backoff_seconds: float = 1.0
    acquisition_interval_seconds: float = 300.0
    logging_level: str = "INFO"
    graceful_shutdown_seconds: float = 10.0

    def validate(self) -> None:
        if self.request_timeout_seconds <= 0:
            raise RuntimeSettingsError("request_timeout_seconds must be > 0.")
        if self.retry_count < 0:
            raise RuntimeSettingsError("retry_count cannot be negative.")
        if self.retry_backoff_seconds < 0:
            raise RuntimeSettingsError("retry_backoff_seconds cannot be negative.")
        if self.acquisition_interval_seconds <= 0:
            raise RuntimeSettingsError("acquisition_interval_seconds must be > 0.")
        if self.graceful_shutdown_seconds < 0:
            raise RuntimeSettingsError("graceful_shutdown_seconds cannot be negative.")
        if self.logging_level.upper() not in {"DEBUG","INFO","WARNING","ERROR","CRITICAL"}:
            raise RuntimeSettingsError("Invalid logging_level.")

    def to_dict(self) -> dict:
        return {
            "request_timeout_seconds": self.request_timeout_seconds,
            "retry_count": self.retry_count,
            "retry_backoff_seconds": self.retry_backoff_seconds,
            "acquisition_interval_seconds": self.acquisition_interval_seconds,
            "logging_level": self.logging_level,
            "graceful_shutdown_seconds": self.graceful_shutdown_seconds,
        }
