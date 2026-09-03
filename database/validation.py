"""WeatherStation Pro - M01-Final-06
Database validation and safe health diagnostics.
"""
from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Any

class ValidationError(RuntimeError):
    """Raised when database validation cannot be completed."""

class DatabaseValidator:
    def __init__(self, database_path: str | Path):
        self.database_path = Path(database_path)

    def validate(self) -> dict[str, Any]:
        if not self.database_path.exists():
            return {
                "exists": False,
                "healthy": False,
                "integrity": None,
                "foreign_keys": False,
                "tables": [],
                "error": "Database file does not exist.",
            }

        try:
            conn = sqlite3.connect(self.database_path, timeout=5.0)
            try:
                conn.execute("PRAGMA foreign_keys=ON")
                integrity = conn.execute(
                    "PRAGMA integrity_check"
                ).fetchone()[0]
                foreign_keys = bool(
                    conn.execute("PRAGMA foreign_keys").fetchone()[0]
                )
                tables = [
                    row[0]
                    for row in conn.execute(
                        "SELECT name FROM sqlite_master "
                        "WHERE type='table' AND name NOT LIKE 'sqlite_%' "
                        "ORDER BY name"
                    ).fetchall()
                ]
            finally:
                conn.close()

            return {
                "exists": True,
                "healthy": integrity == "ok" and foreign_keys,
                "integrity": integrity,
                "foreign_keys": foreign_keys,
                "tables": tables,
            }
        except sqlite3.Error as exc:
            return {
                "exists": True,
                "healthy": False,
                "integrity": None,
                "foreign_keys": False,
                "tables": [],
                "error": str(exc),
            }

    def assert_healthy(self) -> None:
        result = self.validate()
        if not result["healthy"]:
            raise ValidationError(str(result))

    def table_exists(self, table_name: str) -> bool:
        if not self.database_path.exists():
            return False
        conn = sqlite3.connect(self.database_path, timeout=5.0)
        try:
            return conn.execute(
                "SELECT 1 FROM sqlite_master "
                "WHERE type='table' AND name=? LIMIT 1",
                (table_name,),
            ).fetchone() is not None
        finally:
            conn.close()
