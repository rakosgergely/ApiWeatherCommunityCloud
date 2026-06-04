from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd

from models import City, CurrentWeather
from config import DB_PATH
#import os
#from dotenv import load_dotenv

print(DB_PATH)

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS weather_searches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name TEXT NOT NULL,
    temperature REAL NOT NULL,
    humidity REAL NOT NULL,
    wind_speed REAL NOT NULL,
    searched_at TEXT NOT NULL
);
"""


def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True) if Path(db_path).parent != Path(".") else None
    return sqlite3.connect(db_path)


def init_db(db_path: str = DB_PATH) -> None:
    with get_connection(db_path) as conn:
        conn.execute(CREATE_TABLE_SQL)
        conn.commit()


def log_search(city: City, weather: CurrentWeather, db_path: str = DB_PATH) -> None:
    with get_connection(db_path) as conn:
        conn.execute(
            """
            INSERT INTO weather_searches
                (city_name, temperature, humidity, wind_speed, searched_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                f"{city.name}, {city.country}",
                weather.temperature,
                weather.humidity,
                weather.wind_speed,
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        conn.commit()


def load_recent_searches(limit: int = 10, db_path: str = DB_PATH) -> pd.DataFrame:
    with get_connection(db_path) as conn:
        return pd.read_sql_query(
            """
            SELECT city_name, temperature, humidity, wind_speed, searched_at
            FROM weather_searches
            ORDER BY searched_at DESC
            LIMIT ?
            """,
            conn,
            params=(limit,),
        )
