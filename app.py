import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np

# --- CONFIGURATION ---
st.set_page_config(layout="wide", page_title="SPC: Open World Sim")

# --- 1. GAME STATE (The 'GTA' Persistence) ---
if 'game' not in st.session_state:
    st.session_state.game = {
        "lat": 30.0444, "lon": 31.2357, # Starting in Cairo, Egypt
        "alt": 0, "speed": 0, "heading": 0,
        "pitch": 0, "mode": "Car"
    }

# --- 2. THE PHYSICS ENGINE (GeoFS & NFS Logic) ---
def update_physics():
    g = st.session_state.game
    
    # Airspeed/Throttle Handling
    speed_ms = g["speed"] * 0.27778 # Convert km/h to m/s
    
    if g["mode"] == "Plane":
        # GeoFS Logic: Lift depends on speed
        if g["speed"] > 150: # Takeoff speed
            g["alt"] += (g["pitch"] * (g["speed"] / 100))
        # Gravity: If you are in the air, you fall slowly
        if g["alt"] > 0:
            g["alt"] -= 1 # Constant downward pull
            if g["alt"] < 0: g["alt"] = 0
            
    else: # NFS Car Mode
        g["alt"] = 0 # Car stays on ground
        g["pitch"] = 0 # No vertical tilting
        
    # Movement Math: Calculate next position based on Heading
    rad = np.radians(g["heading"])
    # 0.00001 is a coordinate scaling factor to make movement feel real
    g["lat"] += (speed_ms * 0.00001) * np.cos(rad)
    g["lon"] += (speed_ms * 0.00001) * np.sin(rad)

# --- 3. CONTROLS (The Dashboard) ---
st.sidebar.title("🎮 SPC Controller")
g = st.session_state.game

# Vehicle Switch
new_mode = st.sidebar.selectbox("Select Vehicle Type", ["Car", "Plane"], index=0 if g["mode"] == "Car" else 1)
g["mode"] = new_mode

# Drive/Flight Controls
g["speed"] = st.sidebar.slider("Throttle (km/h)", 0, 400, g["speed"])
g["heading"] = st.sidebar.slider("Steering / Heading", 0, 360, g["heading"])

if g["mode"] == "Plane":
    g["pitch"] = st.sidebar.slider("Elevator (Pitch)", -15, 15, g["pitch"])

# Trigger update
if st.sidebar.button("APPLY MOVEMENT"):
    update_physics()

# --- 4. RENDER THE 3D WORLD (Pydeck) ---
view_state = pdk.ViewState(
    latitude=g["lat"],
    longitude=g["lon"],
    zoom=16,
    pitch=45,
    bearing=g["heading"]
)

# Using a public drone model from GitHub as the vehicle
# This replaces the need for a login/email download
obj_data = pd.DataFrame([g])
vehicle_layer = pdk.Layer(
    "ScenegraphLayer",
    obj_data,
    get_scene="https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/Drone/glTF-Binary/Drone.glb",
    get_position="[lon, lat, alt]",
    get_orientation="[0, -heading, 90]", # Rotation to align with map
    size_scale=15,
    _lighting="pbr",
)

r = pdk.Deck(
    layers=[vehicle_layer],
    initial_view_state=view_state,
    map_style="light", # CARTO free style
)

st.pydeck_chart(r)

# --- 5. HUD (Heads-Up Display) ---
c1, c2, c3 = st.columns(3)
c1.metric("Altitude", f"{round(g['alt'], 1)} m")
c2.metric("Speed", f"{g['speed']} km/h")
c3.metric("Heading", f"{g['heading']}°")
