"""M02-01 Configuration Core."""
from dataclasses import dataclass, field
from typing import Any, Mapping


class ConfigurationError(ValueError):
    """Raised when configuration cannot be represented safely."""


@dataclass(frozen=True)
class SettingDefinition:
    name: str
    default: Any = None
    required: bool = False
    secret: bool = False


DEFAULT_DEFINITIONS = (
    SettingDefinition("app.name", "WeatherStationPro"),
    SettingDefinition("app.environment", "development"),
    SettingDefinition("app.timezone", "UTC"),
    SettingDefinition("logging.level", "INFO"),
    SettingDefinition("runtime.enabled", True),
)


@dataclass
class Configuration:
    """Central configuration container with defaults and overrides."""
    values: dict[str, Any] = field(default_factory=dict)
    definitions: tuple[SettingDefinition, ...] = DEFAULT_DEFINITIONS

    def __post_init__(self):
        merged = {d.name: d.default for d in self.definitions}
        merged.update(self.values)
        self.values = merged

    def get(self, name: str, default: Any = None) -> Any:
        return self.values.get(name, default)

    def require(self, name: str) -> Any:
        value = self.values.get(name)
        if value is None or value == "":
            raise ConfigurationError(f"Required setting is missing: {name}")
        return value

    def set(self, name: str, value: Any) -> None:
        if not name or not name.strip():
            raise ConfigurationError("Setting name cannot be empty.")
        self.values[name] = value

    def update(self, values: Mapping[str, Any]) -> None:
        for name, value in values.items():
            self.set(name, value)

    def as_dict(self) -> dict[str, Any]:
        return dict(self.values)

    def masked_dict(self) -> dict[str, Any]:
        secrets = {d.name for d in self.definitions if d.secret}
        return {k: ("***" if k in secrets and v is not None else v)
                for k, v in self.values.items()}
