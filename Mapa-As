import streamlit as st
import folium
from streamlit_folium import st_folium

# Título en Streamlit
st.set_page_config(layout="wide")
st.title("Detección de Arsénico en Agua Potable – Chihuahua")

# Crear el mapa centrado en Chihuahua
m = folium.Map(location=[28.67, -106.1], zoom_start=11, control_scale=True)

# Puntos de muestreo
puntos = [
    {"nombre": "A-01", "grupo": "A", "lat": 28.7356, "lng": -106.124055, "extra": "En este punto se tomaron 3 muestras más: dos de control y una de verificación después del periodo de lluvias."},
    {"nombre": "A-02", "grupo": "A", "lat": 28.73836, "lng": -106.13267},
    {"nombre": "A-03", "grupo": "A", "lat": 28.74376, "lng": -106.132388},
    {"nombre": "B-04", "grupo": "B", "lat": 28.66911, "lng": -106.112844},
    {"nombre": "B-05", "grupo": "B", "lat": 28.65202, "lng": -106.138525},
    {"nombre": "B-06", "grupo": "B", "lat": 28.66207, "lng": -106.127324},
    {"nombre": "C-07", "grupo": "C", "lat": 28.64531, "lng": -106.02162},
    {"nombre": "C-08", "grupo": "C", "lat": 28.62303, "lng": -106.01914},
    {"nombre": "C-09", "grupo": "C", "lat": 28.62859, "lng": -106.02545}
]

colores = {"A": "red", "B": "blue", "C": "green"}

# Agregar marcadores
for punto in puntos:
    popup = f"<b>{punto['nombre']}</b><br>Lat: {punto['lat']}, Lng: {punto['lng']}<br>{punto.get('extra','')}"
    folium.CircleMarker(
        location=[punto['lat'], punto['lng']],
        radius=8,
        color=colores[punto['grupo']],
        fill=True,
        fill_opacity=0.5,
        popup=popup
    ).add_to(m)

# Zonas circulares
zonas = [
    {"nombre": "Zona A", "lat": 28.7399, "lng": -106.1297, "color": "red"},
    {"nombre": "Zona B", "lat": 28.658611, "lng": -106.125556, "color": "blue"},
    {"nombre": "Zona C", "lat": 28.6323, "lng": -106.0221, "color": "green"}
]

for zona in zonas:
    folium.Circle(
        location=[zona["lat"], zona["lng"]],
        radius=2000,
        color=zona["color"],
        weight=2,
        fill=False,
        dash_array='5,10'
    ).add_to(m)

# Agregar capa WMS de pozos y cuencas INEGI
folium.raster_layers.WmsTileLayer(
    url="https://gaia.inegi.org.mx/NLB/tunnel/wms/wms61?",
    layers="c111servicios",
    name="Pozos INEGI",
    fmt="image/png",
    transparent=True,
    version="1.1.1",
    attribution="INEGI"
).add_to(m)

folium.raster_layers.WmsTileLayer(
    url="https://gaia.inegi.org.mx/NLB/tunnel/wms/wms61?",
    layers="c400",
    name="Cuencas hidrológicas",
    fmt="image/png",
    transparent=True,
    version="1.1.1",
    attribution="INEGI"
).add_to(m)

folium.raster_layers.WmsTileLayer(
    url="https://gaia.inegi.org.mx/NLB/tunnel/wms/wms61?",
    layers="c455",
    name="Área concentración pozos",
    fmt="image/png",
    transparent=True,
    version="1.1.1",
    attribution="INEGI"
).add_to(m)

# Control de capas
folium.LayerControl().add_to(m)

# Mostrar mapa en Streamlit
st_data = st_folium(m, width=1200, height=600)
