"""WeatherStation Pro - M01-Final-05: SQLite backup and restore."""
from __future__ import annotations
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

class BackupError(RuntimeError):
    """Raised when a backup or restore operation fails."""

def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

class BackupManager:
    def __init__(self, database_path: str | Path, backup_dir: str | Path):
        self.database_path = Path(database_path)
        self.backup_dir = Path(backup_dir)

    def create_backup(self, prefix: str = "weatherstation") -> Path:
        if not self.database_path.exists():
            raise BackupError(f"Database not found: {self.database_path}")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        target = self.backup_dir / f"{prefix}_{utc_stamp()}.db"
        source = sqlite3.connect(self.database_path)
        destination = sqlite3.connect(target)
        try:
            source.backup(destination)
            destination.commit()
        except sqlite3.Error as exc:
            target.unlink(missing_ok=True)
            raise BackupError(str(exc)) from exc
        finally:
            destination.close()
            source.close()
        return target

    def restore(self, backup_path: str | Path) -> None:
        backup = Path(backup_path)
        if not backup.exists():
            raise BackupError(f"Backup not found: {backup}")
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        source = sqlite3.connect(backup)
        destination = sqlite3.connect(self.database_path)
        try:
            integrity = source.execute("PRAGMA integrity_check").fetchone()[0]
            if integrity != "ok":
                raise BackupError(f"Backup integrity check failed: {integrity}")
            source.backup(destination)
            destination.commit()
        except BackupError:
            destination.rollback()
            raise
        except sqlite3.Error as exc:
            destination.rollback()
            raise BackupError(str(exc)) from exc
        finally:
            destination.close()
            source.close()

    def list_backups(self) -> list[Path]:
        if not self.backup_dir.exists():
            return []
        return sorted(self.backup_dir.glob("*.db"),
                      key=lambda p: p.stat().st_mtime, reverse=True)
