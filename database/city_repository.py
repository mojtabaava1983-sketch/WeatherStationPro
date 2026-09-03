"""WeatherStation Pro - M01-Final-08
City/location repository helpers.
"""
from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Any

class CityRepositoryError(RuntimeError):
    """City persistence error."""

class CityRepository:
    def __init__(self,database_path:str|Path):
        self.database_path=Path(database_path)

    def _connect(self)->sqlite3.Connection:
        if not self.database_path.exists():
            raise CityRepositoryError(f"Database not found: {self.database_path}")
        c=sqlite3.connect(self.database_path,timeout=5.0)
        c.row_factory=sqlite3.Row
        c.execute("PRAGMA foreign_keys=ON")
        c.execute("PRAGMA busy_timeout=5000")
        return c

    def create(self,table:str,values:dict[str,Any])->int:
        if not values:
            raise CityRepositoryError("No city values supplied.")
        cols=list(values)
        sql=(f'INSERT INTO "{table}" ({", ".join(f""" "{x}" """.strip() for x in cols)}) '
             f'VALUES ({", ".join("?" for _ in cols)})')
        try:
            with self._connect() as c:
                cur=c.execute(sql,[values[x] for x in cols])
                c.commit()
                return int(cur.lastrowid)
        except sqlite3.Error as exc:
            raise CityRepositoryError(str(exc)) from exc

    def get_by_id(self,table:str,id_column:str,city_id:int):
        try:
            with self._connect() as c:
                return c.execute(
                    f'SELECT * FROM "{table}" WHERE "{id_column}"=?',
                    (city_id,)).fetchone()
        except sqlite3.Error as exc:
            raise CityRepositoryError(str(exc)) from exc

    def list_cities(self,table:str,order_column:str="Name"):
        try:
            with self._connect() as c:
                return c.execute(
                    f'SELECT * FROM "{table}" ORDER BY "{order_column}"'
                ).fetchall()
        except sqlite3.Error as exc:
            raise CityRepositoryError(str(exc)) from exc
