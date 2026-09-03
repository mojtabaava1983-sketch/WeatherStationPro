"""M02-02 Settings Storage.

Persistence abstraction only; validation and provider-specific semantics belong
to later M02 layers.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Mapping


class SettingsStorageError(RuntimeError):
    pass


class JsonSettingsStorage:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}
        try:
            data=json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise SettingsStorageError(f"Unable to load settings: {self.path}") from exc
        if not isinstance(data, dict):
            raise SettingsStorageError("Settings root must be a JSON object.")
        return data

    def save(self, values: Mapping[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp=self.path.with_suffix(self.path.suffix+".tmp")
        try:
            tmp.write_text(json.dumps(dict(values), ensure_ascii=False, indent=2),
                           encoding="utf-8")
            tmp.replace(self.path)
        except (OSError, TypeError, ValueError) as exc:
            try: tmp.unlink(missing_ok=True)
            except OSError: pass
            raise SettingsStorageError(f"Unable to save settings: {self.path}") from exc

    def exists(self) -> bool:
        return self.path.exists()
