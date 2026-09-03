"""M02-03 Configuration Validation."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class ValidationIssue:
    name: str
    message: str


class ConfigurationValidationError(ValueError):
    def __init__(self, issues: list[ValidationIssue]):
        self.issues = issues
        super().__init__("Configuration validation failed.")


class ConfigurationValidator:
    def __init__(self, definitions: Iterable[Any]):
        self.definitions = tuple(definitions)

    def validate(self, values: Mapping[str, Any]) -> list[ValidationIssue]:
        issues=[]
        for definition in self.definitions:
            value=values.get(definition.name, definition.default)
            if definition.required and (value is None or value == ""):
                issues.append(ValidationIssue(
                    definition.name, "Required setting is missing."
                ))
        return issues

    def validate_or_raise(self, values: Mapping[str, Any]) -> None:
        issues=self.validate(values)
        if issues:
            raise ConfigurationValidationError(issues)
