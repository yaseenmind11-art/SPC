import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np

# --- CONFIGURATION ---
st.set_page_config(layout="wide", page_title="SPC 3D Open World")

# --- 1. GAME STATE ---
if 'game' not in st.session_state:
    st.session_state.game = {
        "lat": 30.0444, "lon": 31.2357, # Starting in Cairo
        "alt": 0, "speed": 0, "heading": 0,
        "mode": "Car"
    }

g = st.session_state.game

# --- 2. CONTROLS ---
st.sidebar.title("🎮 SPC 3D Controller")
g["mode"] = st.sidebar.selectbox("Vehicle Type", ["Car", "Plane"])

# Use sliders to control movement
g["speed"] = st.sidebar.slider("Throttle (km/h)", 0, 300, g["speed"])
g["heading"] = st.sidebar.slider("Steering / Heading", 0, 360, g["heading"])

if st.sidebar.button("APPLY MOVEMENT"):
    rad = np.radians(g["heading"])
    # Move the vehicle based on speed and heading
    move_factor = (g["speed"] * 0.00001)
    g["lat"] += move_factor * np.cos(rad)
    g["lon"] += move_factor * np.sin(rad)
    
    # Simple altitude logic for 'Plane' mode
    if g["mode"] == "Plane" and g["speed"] > 150:
        g["alt"] += 10
    elif g["mode"] == "Car":
        g["alt"] = 0

# --- 3. THE 3D ENGINE (GeoFS + GTA Style) ---

# Link to a public 3D car model (GLB format)
# This model represents the 'NFS' car in the world
VEHICLE_MODEL = "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/CesiumMilkTruck/glTF-Binary/CesiumMilkTruck.glb"

# Create a data frame for the 3D model position
df = pd.DataFrame([g])

# ScenegraphLayer renders the actual 3D body of the car/plane
vehicle_layer = pdk.Layer(
    "ScenegraphLayer",
    df,
    get_scene=VEHICLE_MODEL,
    get_position="[lon, lat, alt]",
    get_orientation="[0, -heading, 90]",
    size_scale=15, # Adjust size so the car is visible
    _lighting="pbr",
)

# ViewState creates the 3D perspective
view_state = pdk.ViewState(
    latitude=g["lat"],
    longitude=g["lon"],
    zoom=19,      # High zoom for street-level view
    pitch=60,     # 60-degree tilt for 3D perspective
    bearing=g["heading"] # Camera follows the vehicle direction
)

# Render the 3D Deck
r = pdk.Deck(
    layers=[vehicle_layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/satellite-v9", # Satellite style for GeoFS look
)

st.pydeck_chart(r)

# HUD Display
st.write(f"**Mode:** {g['mode']} | **Speed:** {g['speed']} km/h | **Altitude:** {g['alt']}m")
