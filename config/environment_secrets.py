"""M02-04 Environment & Secrets.

Reads configuration values from the process environment without persisting or
printing secret values.
"""
from __future__ import annotations
import os
from dataclasses import dataclass ,field
from typing import Mapping


class SecretConfigurationError(ValueError):
    pass


@dataclass(frozen=True)
class EnvironmentReader:
    environ: Mapping[str, str] = field(default_factory=lambda:os.environ)

    def get(self, name: str, default: str | None = None) -> str | None:
        return self.environ.get(name, default)

    def require(self, name: str) -> str:
        value=self.environ.get(name)
        if value is None or value == "":
            raise SecretConfigurationError(f"Required environment value is missing: {name}")
        return value

    def secret(self, name: str) -> str:
        return self.require(name)

    @staticmethod
    def masked(value: str | None) -> str | None:
        if value is None:
            return None
        return "***"

    def masked_get(self, name: str) -> str | None:
        return self.masked(self.environ.get(name))
