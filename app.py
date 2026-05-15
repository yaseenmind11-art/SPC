import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="SPC Pro Drive")

# Your verified Cesium Ion Token
CESIUM_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI3MjUwMTRjMC1mZmNjLTRiMGMtOTQ3Zi0zYjdhYTcxZWUyZWUiLCJpZCI6NDMxNjU4LCJpc3MiOiJodHRwczovL2lvbi5jZXNpdW0uY29tIiwiYXVkIjoidW5kZWZpbmVkX2RlZmF1bHQiLCJpYXQiOjE3Nzg3NzkwNzd9.Z6NvuvwPdtghJiUM9fcfIe1SaZXMBNu8tN_pCQTelxw"

st.title("🏎️ SPC: Real-Physics Simulator")
st.write("Click the map, then use **W, A, S, D** to drive. The car size is fixed to the ground.")

# The Engine: HTML + JavaScript Bridge
cesium_html = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cesium.com/downloads/cesiumjs/releases/1.105/Build/Cesium/Cesium.js"></script>
    <link href="https://cesium.com/downloads/cesiumjs/releases/1.105/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
    <style>
        html, body, #cesiumContainer {{ width: 100%; height: 100%; margin: 0; padding: 0; overflow: hidden; background: #000; }}
        .cesium-viewer-bottom {{ display: none !important; }}
    </style>
</head>
<body>
    <div id="cesiumContainer"></div>
    <script>
        Cesium.Ion.defaultAccessToken = '{CESIUM_TOKEN}';
        
        // 1. Setup World with Terrain (Asset ID 1)
        const viewer = new Cesium.Viewer('cesiumContainer', {{
            terrainProvider: Cesium.createWorldTerrain(),
            baseLayerPicker: false, animation: false, timeline: false,
            sceneModePicker: false, infoBox: false
        }});

        // 2. Add 3D Buildings with shading (Asset ID 96188)
        viewer.scene.primitives.add(Cesium.createOsmBuildings({{
            style: new Cesium.Cesium3DTileStyle({{ color: "color('grey', 1.0)" }})
        }}));

        // 3. Setup Physics State
        let lon = 31.2357; 
        let lat = 30.0444;
        let heading = 0;
        const speed = 0.00002;

        // 4. Create the Fixed-Size Car (NFS/GeoFS Style)
        const carEntity = viewer.entities.add({{
            position: Cesium.Cartesian3.fromDegrees(lon, lat, 0),
            model: {{ 
                uri: 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/CesiumMilkTruck/glTF-Binary/CesiumMilkTruck.glb',
                minimumPixelSize: 0, // This makes it NOT resize when zooming
                scale: 1.0,           // Fixed real-world size
                heightReference: Cesium.HeightReference.RELATIVE_TO_GROUND
            }}
        }});

        // 5. Follow Camera (Locked View)
        viewer.trackedEntity = carEntity;

        // 6. WASD Controller Logic
        document.addEventListener('keydown', (e) => {{
            if (e.code === 'KeyW') {{
                lat += speed * Math.cos(heading);
                lon += speed * Math.sin(heading);
            }}
            if (e.code === 'KeyS') {{
                lat -= speed * Math.cos(heading);
                lon -= speed * Math.sin(heading);
            }}
            if (e.code === 'KeyA') heading -= 0.05;
            if (e.code === 'KeyD') heading += 0.05;

            const newPos = Cesium.Cartesian3.fromDegrees(lon, lat, 0);
            carEntity.position = newPos;
            carEntity.orientation = Cesium.Transforms.headingPitchRollQuaternion(
                newPos, new Cesium.HeadingPitchRoll(heading, 0, 0)
            );
        }});
    </script>
</body>
</html>
"""

components.html(cesium_html, height=800)

st.sidebar.markdown("### 🎮 Controls\\n- **W/S:** Drive\\n- **A/D:** Steer\\n- Click map to focus.")
