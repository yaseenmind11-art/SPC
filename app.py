import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import time

# --- 1. PAGE SETUP ---
st.set_page_config(layout="wide", page_title="SPC 3D World")

# --- 2. GAME STATE (The Memory) ---
if 'game' not in st.session_state:
    st.session_state.game = {
        "lat": 30.0444, "lon": 31.2357, 
        "alt": 0, "speed": 0, "heading": 180,
        "mode": "Car"
    }

g = st.session_state.game

# --- 3. CONTROLLER SIDEBAR ---
st.sidebar.title("🎮 SPC 3D Controller")
g["mode"] = st.sidebar.selectbox("Vehicle Type", ["Car", "Plane"])
g["speed"] = st.sidebar.slider("Throttle (km/h)", 0, 300, g["speed"])
g["heading"] = st.sidebar.slider("Steering", 0, 360, g["heading"])

# Real-time Movement Toggle
run_engine = st.sidebar.checkbox("Start Engine (Auto-Move)")

# --- 4. PHYSICS ENGINE ---
def update_position():
    rad = np.radians(g["heading"])
    # Adjusting coordinates based on speed
    move_dist = (g["speed"] * 0.000005) 
    g["lat"] += move_dist * np.cos(rad)
    g["lon"] += move_dist * np.sin(rad)
    
    # Plane Lift Logic
    if g["mode"] == "Plane" and g["speed"] > 150:
        g["alt"] += 2
    elif g["mode"] == "Car":
        g["alt"] = 0

if run_engine:
    update_position()

# --- 5. THE 3D WORLD (Pydeck) ---

# 3D Model Link (A stable 3D Milk Truck for testing)
VEHICLE_MODEL = "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/CesiumMilkTruck/glTF-Binary/CesiumMilkTruck.glb"

# Create the 3D Vehicle Layer
vehicle_layer = pdk.Layer(
    "ScenegraphLayer",
    pd.DataFrame([g]),
    get_scene=VEHICLE_MODEL,
    get_position="[lon, lat, alt]",
    get_orientation="[0, -heading, 90]", # Rotate to face forward
    size_scale=20, # Scale it up to be visible
    _lighting="pbr",
)

# Set the 3D Camera (Tilt and Zoom)
view_state = pdk.ViewState(
    latitude=g["lat"],
    longitude=g["lon"],
    zoom=18,
    pitch=65, # Tilt to see 3D
    bearing=g["heading"] # Camera follows the car's direction
)

# Render the Map
r = pdk.Deck(
    layers=[vehicle_layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/satellite-v9", # True Satellite Imagery
)

st.pydeck_chart(r)

# --- 6. INTERFACE & LOOP ---
st.write(f"**Status:** {g['mode']} | **Speed:** {g['speed']} km/h | **Altitude:** {round(g['alt'])}m")

# This makes the app refresh itself if the engine is running
if run_engine:
    time.sleep(0.05)
    st.rerun()
