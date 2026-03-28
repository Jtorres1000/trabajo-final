import streamlit as st
import json

@st.cache_data

def load_map_data():
    # Asegúrate de cambiar "world.geojson" por el nombre exacto de tu archivo
    # y la ruta correcta si lo guardaste en una subcarpeta (ej. "data/world.geojson")
    with open("geojson/countries.geo.json", "r", encoding="utf-8") as f:
        return json.load(f)