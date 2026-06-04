from __future__ import annotations

import pandas as pd
import plotly.express as px


def temperature_line_chart(hourly: pd.DataFrame):
    fig = px.line(
        hourly,
        x="time",
        y="temperature_2m",
        markers=False,
        title="Hourly Temperature Forecast (Next 5 Days)",
        labels={"time": "Time", "temperature_2m": "Temperature (°C)"},
    )
    fig.update_layout(template="plotly_dark", height=430)
    return fig


def humidity_line_chart(hourly: pd.DataFrame):
    fig = px.area(
        hourly,
        x="time",
        y="relative_humidity_2m",
        title="Hourly Humidity Forecast (Next 5 Days)",
        labels={"time": "Time", "relative_humidity_2m": "Humidity (%)"},
    )
    fig.update_layout(template="plotly_dark", height=430)
    return fig


def wind_line_chart(hourly: pd.DataFrame):
    fig = px.line(
        hourly,
        x="time",
        y="wind_speed_10m",
        title="Hourly Wind Speed Forecast (Next 5 Days)",
        labels={"time": "Time", "wind_speed_10m": "Wind speed (km/h)"},
    )
    fig.update_layout(template="plotly_dark", height=430)
    return fig
