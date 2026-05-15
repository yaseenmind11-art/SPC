import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="SPC Ultra-Detail")

# Your Verified Cesium Token
CESIUM_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI3MjUwMTRjMC1mZmNjLTRiMGMtOTQ3Zi0zYjdhYTcxZWUyZWUiLCJpZCI6NDMxNjU4LCJpc3MiOiJodHRwczovL2lvbi5jZXNpdW0uY29tIiwiYXVkIjoidW5kZWZpbmVkX2RlZmF1bHQiLCJpYXQiOjE3Nzg3NzkwNzd9.Z6NvuvwPdtghJiUM9fcfIe1SaZXMBNu8tN_pCQTelxw"

st.title("🏙️ SPC: Photorealistic 3D World")
st.info("WASD to Drive | Click map once to start | Real Textures Active")

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
        
        const viewer = new Cesium.Viewer('cesiumContainer', {{
            terrainProvider: Cesium.createWorldTerrain(),
            baseLayerPicker: false, animation: false, timeline: false,
            sceneModePicker: false, infoBox: false
        }});

        // --- THE "PAID" DETAIL FIX ---
        // This adds the Google Photorealistic Tiles (Windows, Balconies, Textures)
        async function addPhotorealism() {{
            try {{
                const tileset = await Cesium.createGooglePhotorealistic3DTileset();
                viewer.scene.primitives.add(tileset);
            }} catch (e) {{
                // Fallback to OSM if Google Tiles are not enabled in your dashboard
                viewer.scene.primitives.add(Cesium.createOsmBuildings());
            }}
        }}
        addPhotorealism();

        // Driving State
        let lon = 31.2357; 
        let lat = 30.0444;
        let heading = 0;
        let velocity = 0;

        // Fixed-Size Sports Car
        const carEntity = viewer.entities.add({{
            position: Cesium.Cartesian3.fromDegrees(lon, lat, 0),
            model: {{ 
                uri: 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/CesiumMilkTruck/glTF-Binary/CesiumMilkTruck.glb',
                scale: 1.5,
                heightReference: Cesium.HeightReference.CLAMP_TO_GROUND
            }}
        }});

        viewer.trackedEntity = carEntity;

        // Physics Loop
        document.addEventListener('keydown', (e) => {{
            if (e.code === 'KeyW') velocity += 0.000005;
            if (e.code === 'KeyS') velocity -= 0.000005;
            if (e.code === 'KeyA') heading -= 0.05;
            if (e.code === 'KeyD') heading += 0.05;
        }});

        viewer.scene.preUpdate.addEventListener(() => {{
            velocity *= 0.95; // Friction
            lat += velocity * Math.cos(heading);
            lon += velocity * Math.sin(heading);
            
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
