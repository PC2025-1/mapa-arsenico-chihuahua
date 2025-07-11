import streamlit as st
import folium
from streamlit_folium import folium_static

# Título de la app
st.set_page_config(layout="wide")
st.title("Mapa: Detección de Arsénico en Agua Potable – Chihuahua")

# Crear el mapa centrado en Chihuahua
m = folium.Map(location=[28.67, -106.1], zoom_start=11, tiles=None)

# Capas base
capa1 = folium.TileLayer(
    tiles='https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png',
    attr='Stadia Maps',
    name='Claro Stadia',
    control=True
).add_to(m)

folium.TileLayer(
    tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attr='OSM',
    name='OSM',
    control=True
).add_to(m)

folium.TileLayer(
    tiles='https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png',
    attr='Stadia Maps',
    name='Oscuro Stadia',
    control=True
).add_to(m)

folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Esri Satélite',
    control=True
).add_to(m)

folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Esri Topográfico',
    control=True
).add_to(m)

# Añadir capas WMS del INEGI (validando capas compatibles con folium)
folium.raster_layers.WmsTileLayer(
    url="https://gaia.inegi.org.mx/NLB/tunnel/wms/wms61?",
    name="Cuencas Hidrográficas (INEGI)",
    layers="c400",
    fmt="image/png",
    transparent=True,
    version="1.1.1",
    attribution="INEGI"
).add_to(m)

folium.raster_layers.WmsTileLayer(
    url="https://gaia.inegi.org.mx/NLB/tunnel/wms/wms61?",
    name="Pozos de Agua (INEGI)",
    layers="c111servicios",
    fmt="image/png",
    transparent=True,
    version="1.1.1",
    attribution="INEGI"
).add_to(m)

folium.raster_layers.WmsTileLayer(
    url="https://gaia.inegi.org.mx/NLB/tunnel/wms/wms61?",
    name="Áreas de concentración de pozos (1996-2008)",
    layers="c455",
    fmt="image/png",
    transparent=True,
    version="1.1.1",
    attribution="INEGI"
).add_to(m)

# Puntos de muestreo
puntos = [
    { "nombre": "A-01", "grupo": "A", "lat": 28.7356, "lng": -106.124055, "extra": "Se tomaron 3 muestras más: 2 de control y 1 de verificación después de lluvias." },
    { "nombre": "A-02", "grupo": "A", "lat": 28.73836, "lng": -106.13267 },
    { "nombre": "A-03", "grupo": "A", "lat": 28.74376, "lng": -106.132388 },
    { "nombre": "B-04", "grupo": "B", "lat": 28.66911, "lng": -106.112844 },
    { "nombre": "B-05", "grupo": "B", "lat": 28.65202, "lng": -106.138525 },
    { "nombre": "B-06", "grupo": "B", "lat": 28.66207, "lng": -106.127324 },
    { "nombre": "C-07", "grupo": "C", "lat": 28.64531, "lng": -106.02162 },
    { "nombre": "C-08", "grupo": "C", "lat": 28.62303, "lng": -106.01914 },
    { "nombre": "C-09", "grupo": "C", "lat": 28.62859, "lng": -106.02545 }
]

colores = { "A": "red", "B": "blue", "C": "green" }

for p in puntos:
    texto = f"<b>{p['nombre']}</b><br>Lat: {p['lat']:.5f}, Lng: {p['lng']:.5f}<br>{p.get('extra','')}"
    folium.CircleMarker(
        location=[p["lat"], p["lng"]],
        radius=8,
        color=colores[p["grupo"]],
        fill=True,
        fillColor=colores[p["grupo"]],
        fillOpacity=0.6,
        popup=texto
    ).add_to(m)

# Círculos para zonas A, B, C
zonas = [
    { "nombre": "Zona A", "lat": 28.7399, "lng": -106.1297, "color": "red" },
    { "nombre": "Zona B", "lat": 28.658611, "lng": -106.125556, "color": "blue" },
    { "nombre": "Zona C", "lat": 28.6323, "lng": -106.0221, "color": "green" }
]

for z in zonas:
    folium.Circle(
        location=[z["lat"], z["lng"]],
        radius=2000,
        color=z["color"],
        fill=False,
        dash_array="6,6",
        weight=2
    ).add_to(m)

# Control de capas
folium.LayerControl().add_to(m)

# Mostrar el mapa en Streamlit
folium_static(m)

