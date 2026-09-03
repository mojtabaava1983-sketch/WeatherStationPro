"""M02-09 Fault Tolerance & Recovery."""
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

T = TypeVar("T")

class ConfigurationRecoveryError(RuntimeError):
    """Raised when normal loading and fallback loading both fail."""

@dataclass(frozen=True)
class RecoveryResult(Generic[T]):
    value: T
    recovered: bool
    error: str | None = None

class ConfigurationRecovery(Generic[T]):
    """Try normal loading, then a caller-supplied fallback."""
    def __init__(self, loader: Callable[[], T], fallback: Callable[[], T]):
        self.loader = loader
        self.fallback = fallback

    def load(self) -> RecoveryResult[T]:
        try:
            return RecoveryResult(self.loader(), False, None)
        except Exception as exc:
            try:
                return RecoveryResult(self.fallback(), True, str(exc))
            except Exception as fallback_exc:
                raise ConfigurationRecoveryError(
                    "Configuration load and fallback both failed."
                ) from fallback_exc
