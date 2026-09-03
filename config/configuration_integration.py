"""M02-08 Configuration Integration."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping

from .configuration import Configuration, SettingDefinition
from .configuration_validation import ConfigurationValidator
from .settings_storage import JsonSettingsStorage


@dataclass
class IntegratedConfiguration:
    configuration: Configuration
    storage: JsonSettingsStorage

    @classmethod
    def load(cls, storage: JsonSettingsStorage,
             definitions: tuple[SettingDefinition, ...] = ()) -> "IntegratedConfiguration":
        values = storage.load()
        cfg = Configuration(values, definitions or Configuration().definitions)
        return cls(cfg, storage)

    def validate(self) -> None:
        ConfigurationValidator(self.configuration.definitions).validate_or_raise(
            self.configuration.as_dict()
        )

    def save(self) -> None:
        self.validate()
        self.storage.save(self.configuration.as_dict())

    def get(self, name: str, default: Any = None) -> Any:
        return self.configuration.get(name, default)

    def set(self, name: str, value: Any) -> None:
        self.configuration.set(name, value)
