from __future__ import annotations

import streamlit as st
import pandas as pd
from models import City, CurrentWeather


def apply_page_config() -> None:
    st.set_page_config(
        page_title="Weather Dashboard",
        page_icon="🌦️",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def inject_css() -> None:
    st.markdown(
        """
        <style>
        .main { background: #0b1117; }
        h1, h2, h3 { font-weight: 800; }
        .stMetric {
            background: #111827;
            border: 1px solid #243244;
            padding: 18px;
            border-radius: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(title: str) -> None:
    st.title(title)
    st.caption("Open-Meteo API alapú időjárás dashboard KPI-okkal, térképpel, előrejelzéssel.")


def render_metrics(weather: CurrentWeather) -> None:
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature (°C)", f"{weather.temperature:.1f}°C")
    col2.metric("Humidity (%)", f"{weather.humidity:.0f}%")
    col3.metric("Wind Speed (km/h)", f"{weather.wind_speed:.1f} km/h")


def render_map(city: City) -> None:
    st.subheader("Weather Map")
    map_df = pd.DataFrame({"lat": [city.latitude], "lon": [city.longitude]})
    st.map(map_df, latitude="lat", longitude="lon", zoom=10)
