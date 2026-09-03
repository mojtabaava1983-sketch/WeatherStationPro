"""M02-06 Provider Settings."""
from __future__ import annotations
from dataclasses import dataclass


class ProviderSettingsError(ValueError):
    pass


@dataclass(frozen=True)
class ProviderSettings:
    name: str
    base_url: str
    api_key_env: str | None = None
    enabled: bool = True
    timeout_seconds: float = 15.0
    retry_count: int = 2
    rate_limit_per_minute: int | None = None

    def validate(self) -> None:
        if not self.name.strip():
            raise ProviderSettingsError("Provider name cannot be empty.")
        if not self.base_url.strip():
            raise ProviderSettingsError("Provider base_url cannot be empty.")
        if self.timeout_seconds <= 0:
            raise ProviderSettingsError("timeout_seconds must be greater than zero.")
        if self.retry_count < 0:
            raise ProviderSettingsError("retry_count cannot be negative.")
        if self.rate_limit_per_minute is not None and self.rate_limit_per_minute <= 0:
            raise ProviderSettingsError("rate_limit_per_minute must be positive.")

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "base_url": self.base_url,
            "api_key_env": self.api_key_env,
            "enabled": self.enabled,
            "timeout_seconds": self.timeout_seconds,
            "retry_count": self.retry_count,
            "rate_limit_per_minute": self.rate_limit_per_minute,
        }
