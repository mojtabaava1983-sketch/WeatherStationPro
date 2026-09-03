"""WeatherStation Pro - M01-Final-04: controlled SQLite migrations."""
from __future__ import annotations
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

class MigrationError(RuntimeError):
    """Raised when a migration fails."""

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def utc_unix() -> int:
    return int(datetime.now(timezone.utc).timestamp())

class MigrationManager:
    def __init__(self, database_path: str | Path):
        self.database_path = Path(database_path)

    def _connect(self) -> sqlite3.Connection:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.database_path, timeout=5.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA busy_timeout=5000")
        return conn

    def ensure_metadata(self) -> None:
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS DatabaseInfo(
                    DatabaseID INTEGER PRIMARY KEY CHECK(DatabaseID=1),
                    DatabaseVersion TEXT NOT NULL,
                    SchemaVersion INTEGER NOT NULL,
                    ApplicationVersion TEXT NOT NULL,
                    CreatedUTC TEXT NOT NULL,
                    CreatedUnix INTEGER NOT NULL,
                    LastMigrationUTC TEXT,
                    LastMigrationUnix INTEGER,
                    Description TEXT
                )
            """)
            if conn.execute(
                "SELECT 1 FROM DatabaseInfo WHERE DatabaseID=1"
            ).fetchone() is None:
                now = utc_now_iso()
                conn.execute("""
                    INSERT INTO DatabaseInfo(
                        DatabaseID,DatabaseVersion,SchemaVersion,
                        ApplicationVersion,CreatedUTC,CreatedUnix,Description
                    ) VALUES(1,?,?,?,?,?,?)
                """, ("0.1.0", 0, "0.0.0", now, utc_unix(),
                      "WeatherStation Pro database"))
            conn.commit()

    def current_version(self) -> int:
        self.ensure_metadata()
        with self._connect() as conn:
            return int(conn.execute(
                "SELECT SchemaVersion FROM DatabaseInfo WHERE DatabaseID=1"
            ).fetchone()[0])

    def apply(self, migrations_dir: str | Path) -> list[int]:
        self.ensure_metadata()
        current = self.current_version()
        applied = []
        for path in sorted(Path(migrations_dir).glob("*.sql")):
            try:
                version = int(path.stem.split("_", 1)[0])
            except ValueError:
                continue
            if version <= current:
                continue
            with self._connect() as conn:
                try:
                    conn.execute("BEGIN")
                    conn.executescript(path.read_text(encoding="utf-8"))
                    now = utc_now_iso()
                    conn.execute("""
                        UPDATE DatabaseInfo
                        SET SchemaVersion=?,
                            LastMigrationUTC=?,
                            LastMigrationUnix=?
                        WHERE DatabaseID=1
                    """, (version, now, utc_unix()))
                    conn.commit()
                except sqlite3.Error as exc:
                    conn.rollback()
                    raise MigrationError(
                        f"Migration {path.name} failed: {exc}"
                    ) from exc
            current = version
            applied.append(version)
        return applied
