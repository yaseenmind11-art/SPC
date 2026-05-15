import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="SPC 3D World")

# --- 1. SETTINGS ---
# Your integrated Cesium Token
CESIUM_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI3MjUwMTRjMC1mZmNjLTRiMGMtOTQ3Zi0zYjdhYTcxZWUyZWUiLCJpZCI6NDMxNjU4LCJpc3MiOiJodHRwczovL2lvbi5jZXNpdW0uY29tIiwiYXVkIjoidW5kZWZpbmVkX2RlZmF1bHQiLCJpYXQiOjE3Nzg3NzkwNzd9.Z6NvuvwPdtghJiUM9fcfIe1SaZXMBNu8tN_pCQTelxw"

st.title("🎮 SPC: 3D Open World")
st.write("Streaming 3D Buildings & Terrain from Cesium Ion")

# --- 2. THE GEFS ENGINE (Cesium JS) ---
cesium_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <script src="https://cesium.com/downloads/cesiumjs/releases/1.105/Build/Cesium/Cesium.js"></script>
    <link href="https://cesium.com/downloads/cesiumjs/releases/1.105/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
    <style>
        html, body, #cesiumContainer {{ 
            width: 100%; 
            height: 100%; 
            margin: 0; 
            padding: 0; 
            overflow: hidden; 
            background: #000; 
        }}
        .cesium-viewer-bottom {{ display: none !important; }} /* Clean UI */
    </style>
</head>
<body>
    <div id="cesiumContainer"></div>
    <script>
        Cesium.Ion.defaultAccessToken = '{CESIUM_TOKEN}';
        
        // Setup the 3D World with Terrain (Asset ID 1)
        const viewer = new Cesium.Viewer('cesiumContainer', {{
            terrainProvider: Cesium.createWorldTerrain(),
            baseLayerPicker: false,
            animation: false,
            timeline: false,
            geocoder: true,
            sceneModePicker: true,
            navigationHelpButton: false,
            infoBox: false
        }});

        // Add the 3D OSM Buildings (Asset ID 96188)
        const buildings = viewer.scene.primitives.add(Cesium.createOsmBuildings());

        // Fly to Cairo and set the 'GeoFS' camera angle
        viewer.camera.flyTo({{
            destination: Cesium.Cartesian3.fromDegrees(31.2357, 30.0444, 800),
            orientation: {{
                heading: Cesium.Math.toRadians(0.0),
                pitch: Cesium.Math.toRadians(-25.0),
                roll: 0.0
            }}
        }});
    </script>
</body>
</html>
"""

# --- 3. RENDER ---
components.html(cesium_html, height=800)

st.sidebar.success("Cesium Ion Token Active ✅")
st.sidebar.markdown("""
### Controls
- **Left Click + Drag:** Rotate Camera
- **Right Click + Drag:** Zoom In/Out
- **Middle Click:** Change Tilt Angle
""")
