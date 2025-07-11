import streamlit as st
import folium
from streamlit_folium import folium_static

# Título de la app
st.set_page_config(layout="wide")
st.title("Mapa: Detección de Arsénico en Agua Potable – Chihuahua")

# Crear mapa principal
m = folium.Map(location=[28.67, -106.1], zoom_start=11, control_scale=True, tiles=None)

# Capas base
tiles = {
    "Claro Stadia": 'https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png',
    "OSM": 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    "Oscuro Stadia": 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png',
    "Esri Satélite": 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    "Esri Topográfico": 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
    "Carto Light": 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
    "Carto Dark": 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
}

base_layers = {}
for name, url in tiles.items():
    tile = folium.TileLayer(
        tiles=url,
        name=name,
        attr='&copy; OpenStreetMap contributors',
        control=True
    )
    tile.add_to(m)
    base_layers[name] = tile

# WMS capas del INEGI
folium.raster_layers.WmsTileLayer(
    url='https://gaia.inegi.org.mx/NLB/tunnel/wms/wms61?',
    layers='c455',
    name='Áreas de concentración pozos INEGI (1996–2008)',
    fmt='image/png',
    transparent=True,
    version='1.1.1',
    attr='INEGI'
).add_to(m)

# Zonas
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
        dash_array='6,6'
    ).add_to(m)

    folium.map.Marker(
        [zona["lat"] + 0.015, zona["lng"]],
        icon=folium.DivIcon(html=f"""
            <div style="font-size: 14px; background: rgba(255,255,255,0.8);
                        padding:2px 5px; border-radius:4px;">
                <b>{zona['nombre']}</b>
            </div>
        """)
    ).add_to(m)

# Puntos de muestreo
puntos = [
    { "nombre": "A-01", "grupo": "A", "lat": 28.7356, "lng": -106.124055,
      "extra": "Se tomaron 3 muestras más: dos de control y una de verificación después del periodo de lluvias." },
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

for punto in puntos:
    popup = f"<b>{punto['nombre']}</b>"
    if 'extra' in punto:
        popup += f"<br>{punto['extra']}"
    popup += f"<br>Lat: {punto['lat']:.5f}<br>Lng: {punto['lng']:.5f}"

    folium.CircleMarker(
        location=[punto['lat'], punto['lng']],
        radius=8,
        color=colores[punto["grupo"]],
        fill=True,
        fill_color=colores[punto["grupo"]],
        fill_opacity=0.6,
        popup=popup
    ).add_to(m)

# Minimapa
osm_minimap = folium.TileLayer(
    tiles=tiles["OSM"],
    attr='&copy; OpenStreetMap contributors'
)
MiniMap(tile_layer=osm_minimap, position="bottomleft", toggle_display=True).add_to(m)


# Leyenda personalizada + logos + título
template = """
{% macro html(this, kwargs) %}
<div style="
    position: fixed;
    bottom: 60px;
    left: 10px;
    width: 160px;
    background-color: white;
    z-index:9999;
    font-size:14px;
    padding:10px;
    border-radius:5px;
    box-shadow:0 0 6px rgba(0,0,0,0.3);">
    <b>Leyenda</b><br>
    <i style='background:red;width:12px;height:12px;display:inline-block;border-radius:50%;margin-right:4px;'></i> Zona A (Norte)<br>
    <i style='background:blue;width:12px;height:12px;display:inline-block;border-radius:50%;margin-right:4px;'></i> Zona B (Centro)<br>
    <i style='background:green;width:12px;height:12px;display:inline-block;border-radius:50%;margin-right:4px;'></i> Zona C (Sur)<br>
</div>

<div style="
    position: fixed;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(255,255,255,0.85);
    padding: 8px 15px;
    border-radius: 6px;
    box-shadow: 0 0 5px rgba(0,0,0,0.3);
    z-index: 9999;
    font-size: 16px;
    font-weight: bold;
    text-align: center;">
    Detección de Arsénico en Agua Potable – Chihuahua
</div>

<div style="
    position: fixed;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(255,255,255,0.8);
    padding: 5px 12px;
    font-size: 12px;
    border-radius: 4px;
    font-family: sans-serif;
    display: none;
    z-index: 9999;"
    class="pie-pagina">
    Proyecto académico – 20va Edición del Verano de Investigación Científica · Créditos: CIMAV, UACH · Datos: INEGI, StadiaMaps
</div>

<div style="
    position: fixed;
    bottom: 200px;
    left: 10px;
    background: rgba(255,255,255,0.85);
    padding: 4px 8px;
    border-radius: 5px;
    display: flex;
    gap: 8px;
    align-items: center;
    box-shadow: 0 0 4px rgba(0,0,0,0.3);
    z-index: 9999;">
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQNnAS26nhdsMEyTqi1ccXa-kG_eiqIwBGcSg&s" height="40">
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuQUMI6FVsjhpfo4kR4pnQy1eG0HTLlgyviA&s" height="40">
</div>

<style>
@media (min-width: 600px) {
  .pie-pagina { display: block !important; }
}
</style>

{% endmacro %}
"""
macro = MacroElement()
macro._template = Template(template)
m.get_root().add_child(macro)

# Mostrar el mapa en Streamlit
folium_static(m)

