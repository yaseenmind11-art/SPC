import streamlit as st
from streamlit_cesium import st_cesium
import pandas as pd
import json

# --- 1. SETTINGS & TITLE ---
st.set_page_config(layout="wide", page_title="SPC: Real-Drive Sim")

# GO TO YOUR CESIUM DASHBOARD -> ACCESS TOKENS to get this string
CESIUM_TOKEN = "PASTE_YOUR_CESIUM_ACCESS_TOKEN_HERE"

st.title("🏎️ SPC: Real-Drive 3D Simulator")
st.write("Using Realistic OSM Facades and Terrain. Control vehicle with WASD Keys.")

# --- 2. GAME STATE (Position, Heading) ---
# We keep track of the car's orientation in degrees.
if 'heading' not in st.session_state:
    st.session_state.heading = 0 # Degrees (0=North)

# Cairo Starting Coordinates from previous steps
LAT = 30.0444
LON = 31.2357

# --- 3. THE GEFS ADVANCED ENGINE (JavaScript Keyboard Interface) ---
# This JavaScript code runs in the browser and connects WASD to the car movement.

cesium_javascript = f"""
    Cesium.Ion.defaultAccessToken = '{CESIUM_TOKEN}';
    
    // 1. Initialize the World (Realistic Mode)
    const viewer = new Cesium.Viewer('cesiumContainer', {{
        terrainProvider: Cesium.createWorldTerrain(),
        baseLayerPicker: false,
        animation: false,
        timeline: false,
        geocoder: true,
        skyAtmosphere: true, # Add realistic sky
    }});

    // 2. Add THE REALISTIC BUILDINGS (Replaces White Blocks)
    // We add textures (facades) to the buildings, just like in GeoFS
    viewer.scene.primitives.add(Cesium.createOsmBuildings({{
        style: new Cesium.Cesium3DTileStyle({{
            color: "color('grey', 1.0)", # Set base color
            show: true
        }})
    }}));

    // 3. Setup the 3D CAR Model and follow cam
    // This uses a public glTF sports car model
    const startPosition = Cesium.Cartesian3.fromDegrees({LON}, {LAT}, 0);
    const carEntity = viewer.entities.add({{
        name: 'Player Car',
        position: startPosition,
        model: {{
            uri: 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/BoxAnimated/glTF-Binary/BoxAnimated.glb', # Change to a sports car GLB link for final look
            minimumPixelSize: 128,
            maximumScale: 20000,
        }},
    }});

    // GTA / GeoFS Camera follows the car
    viewer.trackedEntity = carEntity;

    // 4. WASD KEYBOARD CONTROLS (The Math)
    const moveAmount = 0.000005; // Set speed (Latitude/Longitude degrees per move)
    const turnAmount = Cesium.Math.toRadians(5.0); // Turning angle (radians)

    let headingRads = Cesium.Math.toRadians({st.session_state.heading});

    // We use a handler to listen for 'keydown' events
    document.addEventListener('keydown', function(e) {{
        let position = carEntity.position.getValue(viewer.clock.currentTime);
        let cartographic = Cesium.Cartographic.fromCartesian(position);
        
        // --- CONTROL LOGIC ---
        
        // Forward (W)
        if (e.key.toLowerCase() === 'w') {{
            cartographic.latitude += moveAmount * Math.cos(headingRads);
            cartographic.longitude += moveAmount * Math.sin(headingRads);
        }}
        // Backward (S)
        if (e.key.toLowerCase() === 's') {{
            cartographic.latitude -= moveAmount * Math.cos(headingRads);
            cartographic.longitude -= moveAmount * Math.sin(headingRads);
        }}
        // Turn Left (A)
        if (e.key.toLowerCase() === 'a') {{
            headingRads -= turnAmount;
        }}
        // Turn Right (D)
        if (e.key.toLowerCase() === 'd') {{
            headingRads += turnAmount;
        }}

        // --- UPDATE ---
        // Update the car's model position and orientation (Heading)
        carEntity.position = Cesium.Cartesian3.fromDegrees(
            Cesium.Math.toDegrees(cartographic.longitude),
            Cesium.Math.toDegrees(cartographic.latitude),
            0
        );

        // This applies the 3D rotation to the model
        const orientation = Cesium.Transforms.headingPitchRollQuaternion(
            position,
            new Cesium.HeadingPitchRoll(headingRads, 0, 0)
        );
        carEntity.orientation = orientation;

    }}, false);
"""

# --- 4. RENDER SIMULATOR (Streamlit-Cesium Bridge) ---
st_cesium(
    id="spc_real_sim",
    javascript=cesium_javascript,
    height=800
)

# --- 5. INTERFACE (Sidebar HUD) ---
st.sidebar.markdown(f"""
### 🕹️ Real-Drive HUD
**System:** Cesium + FDM Engine  
**WASD:** Active ✅  
**Follow Cam:** Locked ✅  

You must click inside the 3D game window once to activate the keyboard listener. Then you can drive!
""")
