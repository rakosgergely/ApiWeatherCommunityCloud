from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import pandas as pd
import requests
#import os
#from dotenv import load_dotenv
from config import FORECAST_DAYS, FORECAST_URL, GEOCODING_URL


@dataclass(frozen=True)
class City:
    name: str
    country: str
    latitude: float
    longitude: float


@dataclass(frozen=True)
class CurrentWeather:
    temperature: float
    humidity: float
    wind_speed: float


def _get_json(url: str, params: dict[str, Any]) -> dict[str, Any]:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def geocode_city(city_name: str) -> City | None:
    data = _get_json(
        GEOCODING_URL,
        {
            "name": city_name.strip(),
            "count": 1,
            "language": "en",
            "format": "json",
        },
    )

    results = data.get("results", [])
    if not results:
        return None

    first = results[0]
    return City(
        name=first["name"],
        country=first.get("country", "Unknown country"),
        latitude=float(first["latitude"]),
        longitude=float(first["longitude"]),
    )


def get_weather(city: City) -> tuple[CurrentWeather, pd.DataFrame]:
    data = _get_json(
        FORECAST_URL,
        {
            "latitude": city.latitude,
            "longitude": city.longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "forecast_days": FORECAST_DAYS,
            "timezone": "auto",
        },
    )

    current = data["current"]
    current_weather = CurrentWeather(
        temperature=float(current["temperature_2m"]),
        humidity=float(current["relative_humidity_2m"]),
        wind_speed=float(current["wind_speed_10m"]),
    )

    hourly = pd.DataFrame(data["hourly"])
    hourly["time"] = pd.to_datetime(hourly["time"])

    return current_weather, hourly
