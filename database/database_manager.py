"""WeatherStation Pro - M01-Final-03
SQLite database access layer.
"""
from __future__ import annotations
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, Sequence

class DatabaseError(RuntimeError):
    """Base exception for database-layer failures."""

class DatabaseManager:
    def __init__(self, database_path: str | Path):
        self.database_path = Path(database_path)

    def connect(self) -> sqlite3.Connection:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            conn = sqlite3.connect(self.database_path, timeout=5.0,
                                   isolation_level=None)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys=ON")
            conn.execute("PRAGMA busy_timeout=5000")
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            return conn
        except sqlite3.Error as exc:
            raise DatabaseError(str(exc)) from exc

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        conn = self.connect()
        try:
            conn.execute("BEGIN")
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def initialize(self, schema_paths: Sequence[str | Path]) -> None:
        with self.connection() as conn:
            for path in schema_paths:
                conn.executescript(Path(path).read_text(encoding="utf-8"))

    def execute(self, sql: str, parameters: Sequence[Any] = ()) -> int:
        try:
            with self.connection() as conn:
                return conn.execute(sql, parameters).rowcount
        except sqlite3.Error as exc:
            raise DatabaseError(str(exc)) from exc

    def insert(self, table: str, values: dict[str, Any],
               *, ignore_conflict: bool = False) -> int:
        if not values:
            raise ValueError("values cannot be empty")
        columns=list(values)
        quoted=", ".join(f'"{c}"' for c in columns)
        placeholders=", ".join("?" for _ in columns)
        verb="INSERT OR IGNORE" if ignore_conflict else "INSERT"
        sql=f'{verb} INTO "{table}" ({quoted}) VALUES ({placeholders})'
        try:
            with self.connection() as conn:
                cur=conn.execute(sql,[values[c] for c in columns])
                return int(cur.lastrowid or 0)
        except sqlite3.Error as exc:
            raise DatabaseError(str(exc)) from exc

    def fetch_one(self, sql: str, parameters: Sequence[Any] = ()):
        try:
            with self.connection() as conn:
                return conn.execute(sql, parameters).fetchone()
        except sqlite3.Error as exc:
            raise DatabaseError(str(exc)) from exc

    def fetch_all(self, sql: str, parameters: Sequence[Any] = ()):
        try:
            with self.connection() as conn:
                return conn.execute(sql, parameters).fetchall()
        except sqlite3.Error as exc:
            raise DatabaseError(str(exc)) from exc

    def table_exists(self, table_name: str) -> bool:
        return self.fetch_one(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1",
            (table_name,)) is not None

    def health_check(self) -> dict[str, Any]:
        try:
            with self.connection() as conn:
                fk=conn.execute("PRAGMA foreign_keys").fetchone()[0]
                mode=conn.execute("PRAGMA journal_mode").fetchone()[0]
                integrity=conn.execute("PRAGMA integrity_check").fetchone()[0]
            return {
                "database": str(self.database_path),
                "exists": self.database_path.exists(),
                "foreign_keys": bool(fk),
                "journal_mode": str(mode).lower(),
                "integrity_check": integrity,
                "healthy": integrity == "ok" and bool(fk),
            }
        except sqlite3.Error as exc:
            return {
                "database": str(self.database_path),
                "exists": self.database_path.exists(),
                "healthy": False,
                "error": str(exc),
            }
