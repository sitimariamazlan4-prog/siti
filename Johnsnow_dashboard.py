import streamlit as st
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
from branca.element import Template, MacroElement
from streamlit_folium import st_folium

# ------------------------------
# 1. STREAMLIT PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="Cholera Death Map", layout="wide")
st.title("Cholera Death Dashboard")

# ------------------------------
# 2. LOAD DATA (EPSG:27700)
# ------------------------------
gdf_deaths = gpd.read_file(r"C:\Users\nhani\Desktop\GES_723_Streamlit\Cholera\Cholera_Deaths.shp")
gdf_pumps = gpd.read_file(r"C:\Users\nhani\Desktop\GES_723_Streamlit\Cholera\Pumps.shp")

# ------------------------------
# 3. REPROJECT FOR FOLIUM (EPSG:4326)
# ------------------------------
gdf_deaths_wgs = gdf_deaths.to_crs(epsg=4326)
gdf_pumps_wgs = gdf_pumps.to_crs(epsg=4326)

# ------------------------------
# 4. CREATE BASE MAP
# ------------------------------
center_lat = gdf_deaths_wgs.geometry.y.mean()
center_lon = gdf_deaths_wgs.geometry.x.mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=16)

# ------------------------------
# 5. ADD CHOLERA DEATHS
# ------------------------------
deaths_layer = folium.FeatureGroup(name="Cholera Deaths")
for _, row in gdf_deaths_wgs.iterrows():
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=3,
        color="red",
        fill=True,
        fill_opacity=0.8
    ).add_to(deaths_layer)
deaths_layer.add_to(m)

# ------------------------------
# 6. ADD WATER PUMPS (Font Awesome tint)
# ------------------------------
pumps_layer = folium.FeatureGroup(name="Water Pumps")
for _, row in gdf_pumps_wgs.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup="Water Pump",
        icon=folium.Icon(color="blue", icon="tint", prefix="fa")
    ).add_to(pumps_layer)
pumps_layer.add_to(m)

# ------------------------------
# 7. ADD LAYER CONTROL
# ------------------------------
folium.LayerControl().add_to(m)

# ------------------------------
# 8. ADD TITLE AND LEGEND
# ------------------------------
template = """
{% macro html(this, kwargs) %}

<!-- TITLE -->
<div style="
    position: fixed;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    z-index:9999;
    background-color:white;
    padding:10px;
    border:2px solid grey;
    border-radius:5px;
    font-size:16px;
    font-weight:bold;
    ">
    CHOLERA DEATH MAP
</div>

<!-- LEGEND -->
<div style="
    position: fixed;
    bottom: 50px;
    left: 10px;
    z-index:9999;
    background-color:white;
    padding:10px;
    border:2px solid grey;
    border-radius:5px;
    font-size:14px;
    ">
    <i class="fa fa-circle" style="color:red;"></i> Cholera Deaths<br>
    <i class="fa fa-tint" style="color:blue;"></i> Water Pumps
</div>

{% endmacro %}
"""

macro = MacroElement()
macro._template = Template(template)
m.get_root().add_child(macro)

# ------------------------------
# 9. DISPLAY MAP IN STREAMLIT
# ------------------------------
st.subheader("Interactive Cholera Map")
st_folium(m, width=1000, height=600)