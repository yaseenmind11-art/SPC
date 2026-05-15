import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="SPC 3D World")

# --- 1. SETTINGS ---
# Go to your Cesium Ion dashboard -> Access Tokens to get this
CESIUM_TOKEN = "PASTE_YOUR_CESIUM_ACCESS_TOKEN_HERE"

st.title("🎮 SPC: 3D Open World (GeoFS + NFS Style)")
st.write("Using Cesium OSM Buildings (96188) and World Terrain (1)")

# --- 2. THE BRIDGE (Python to JavaScript) ---
# This HTML block contains the REAL Cesium engine code
cesium_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <script src="https://cesium.com/downloads/cesiumjs/releases/1.105/Build/Cesium/Cesium.js"></script>
    <link href="https://cesium.com/downloads/cesiumjs/releases/1.105/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
    <style>
        html, body, #cesiumContainer {{ width: 100%; height: 100%; margin: 0; padding: 0; overflow: hidden; }}
    </style>
</head>
<body>
    <div id="cesiumContainer"></div>
    <script>
        Cesium.Ion.defaultAccessToken = '{CESIUM_TOKEN}';
        
        // Initialize the viewer with 3D Terrain (ID 1 from your image)
        const viewer = new Cesium.Viewer('cesiumContainer', {{
            terrainProvider: Cesium.createWorldTerrain(),
            baseLayerPicker: false,
            sceneModePicker: false,
        }});

        // Add 3D Buildings (ID 96188 from your image)
        const buildings = viewer.scene.primitives.add(Cesium.createOsmBuildings());

        // Fly to Cairo (Your starting point)
        viewer.camera.flyTo({{
            destination: Cesium.Cartesian3.fromDegrees(31.2357, 30.0444, 500),
            orientation: {{
                pitch: Cesium.Math.toRadians(-35.0)
            }}
        }});
    </script>
</body>
</html>
"""

# --- 3. DISPLAY ---
# This renders the 3D window in your Streamlit app
components.html(cesium_html, height=700)

st.sidebar.markdown("""
### How to Play
1. Use your mouse to rotate the world.
2. The 3D buildings are streamed live from **Cesium Ion**.
3. This is the same engine used by **GeoFS**.
""")
