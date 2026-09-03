"""WeatherStation Pro M01-Final-07 repository layer."""
from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Any, Iterable

class RepositoryError(RuntimeError):
    """Persistence-layer failure."""

class WeatherRepository:
    def __init__(self,database_path:str|Path):
        self.database_path=Path(database_path)

    def _connect(self)->sqlite3.Connection:
        if not self.database_path.exists():
            raise RepositoryError(f"Database not found: {self.database_path}")
        c=sqlite3.connect(self.database_path,timeout=5.0)
        c.row_factory=sqlite3.Row
        c.execute("PRAGMA foreign_keys=ON")
        c.execute("PRAGMA busy_timeout=5000")
        return c

    def insert_observation(self,table:str,values:dict[str,Any],
                           required_fields:Iterable[str]=("Temperature","Humidity"))->int:
        missing=[f for f in required_fields if values.get(f) is None]
        if missing:
            raise RepositoryError("Required weather values are missing: "+", ".join(missing))
        if not values:
            raise RepositoryError("No observation values supplied.")
        cols=list(values)
        quoted=", ".join(f'"{c}"' for c in cols)
        marks=", ".join("?" for _ in cols)
        sql=f'INSERT INTO "{table}" ({quoted}) VALUES ({marks})'
        try:
            with self._connect() as c:
                cur=c.execute(sql,[values[x] for x in cols])
                c.commit()
                return int(cur.lastrowid)
        except sqlite3.Error as exc:
            raise RepositoryError(str(exc)) from exc

    def fetch_latest(self,table:str,time_column:str,limit:int=1)->list[sqlite3.Row]:
        if limit<1: return []
        try:
            with self._connect() as c:
                return c.execute(
                    f'SELECT * FROM "{table}" ORDER BY "{time_column}" DESC LIMIT ?',
                    (limit,)).fetchall()
        except sqlite3.Error as exc:
            raise RepositoryError(str(exc)) from exc

    def count_rows(self,table:str)->int:
        try:
            with self._connect() as c:
                return int(c.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0])
        except sqlite3.Error as exc:
            raise RepositoryError(str(exc)) from exc
