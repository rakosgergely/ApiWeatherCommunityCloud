from __future__ import annotations

import requests
import streamlit as st

from models import geocode_city, get_weather
from ui.charts import humidity_line_chart, temperature_line_chart, wind_line_chart
from ui.streamlit_ui import apply_page_config, inject_css, render_header, render_map, render_metrics
from database import init_db, load_recent_searches, log_search
import os
from dotenv import load_dotenv


@st.cache_data(ttl=900, show_spinner=False)
def cached_geocode_city(city_name: str):
    return geocode_city(city_name)


@st.cache_data(ttl=900, show_spinner=False)
def cached_get_weather(city):
    return get_weather(city)


def main() -> None:
    load_dotenv()
    apply_page_config()
    inject_css()
    init_db()

    render_header("OpenWeather")

    with st.sidebar:
        st.header("Search")
        city_name = st.text_input("Enter city name", value="Budapest")
        search_clicked = st.button("Show weather", use_container_width=True)
        st.divider()
        st.caption("Tipp: próbáld ki például: Budapest, Vienna, London, Tokyo.")

    if not city_name.strip():
        st.warning("Adj meg egy létező városnevet.")
        return

    if search_clicked:
        try:
            city = cached_geocode_city(city_name)
            if city is None:
                st.warning("Nem található ilyen város. Próbálj meg pontosabb nevet megadni.")
                return

            weather, hourly = cached_get_weather(city)
            log_search(city, weather)

        except requests.HTTPError as exc:
            st.warning(f"Az API hívás hibát dobott: {exc}")
            return
        except requests.RequestException as exc:
            st.warning(f"Nem sikerült kapcsolódni az API-hoz: {exc}")
            return
        except KeyError:
            st.warning("Az API válasza nem a várt formátumú volt.")
            return

        st.subheader(f"Current Weather in {city.name}, {city.country}")
        render_metrics(weather)

        left, right = st.columns([1, 1])
        with left:
            render_map(city)
        with right:
            st.subheader("Current search details")
            st.write(f"**City:** {city.name}")
            st.write(f"**Country:** {city.country}")
            st.write(f"**Latitude:** {city.latitude}")
            st.write(f"**Longitude:** {city.longitude}")

        tab1, tab2, tab3, tab4 = st.tabs(["Temperature", "Humidity", "Wind", "Search log"])
        with tab1:
            st.plotly_chart(temperature_line_chart(hourly), use_container_width=True)
        with tab2:
            st.plotly_chart(humidity_line_chart(hourly), use_container_width=True)
        with tab3:
            st.plotly_chart(wind_line_chart(hourly), use_container_width=True)
        with tab4:
            st.dataframe(load_recent_searches(), use_container_width=True)


if __name__ == "__main__":
    main()
