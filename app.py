import streamlit as st
from streamlit_cesium import st_cesium

st.set_page_config(layout="wide", page_title="SPC 3D Pro")

# --- 1. ACCESS TOKEN ---
CESIUM_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI3MjUwMTRjMC1mZmNjLTRiMGMtOTQ3Zi0zYjdhYTcxZWUyZWUiLCJpZCI6NDMxNjU4LCJpc3MiOiJodHRwczovL2lvbi5jZXNpdW0uY29tIiwiYXVkIjoidW5kZWZpbmVkX2RlZmF1bHQiLCJpYXQiOjE3Nzg3NzkwNzd9.Z6NvuvwPdtghJiUM9fcfIe1SaZXMBNu8tN_pCQTelxw"

st.title("🏎️ SPC: Advanced 3D Simulator")
st.write("Click on the map once, then use **WASD** to drive through the city!")

# --- 2. THE GEFS ENGINE (JavaScript WASD + Textures) ---
cesium_js = f"""
    Cesium.Ion.defaultAccessToken = '{CESIUM_TOKEN}';
    
    // Setup Viewer
    const viewer = new Cesium.Viewer('cesiumContainer', {{
        terrainProvider: Cesium.createWorldTerrain(),
        baseLayerPicker: false,
        animation: false,
        timeline: false
    }});

    // Add Realistic Textured Buildings (GeoFS Style)
    const buildings = viewer.scene.primitives.add(Cesium.createOsmBuildings({{
        style: new Cesium.Cesium3DTileStyle({{
            color: "color('grey', 1.0)",
            show: true
        }})
    }}));

    // Add 3D Car Model
    const carPos = Cesium.Cartesian3.fromDegrees(31.2357, 30.0444, 0);
    const carEntity = viewer.entities.add({{
        position: carPos,
        model: {{
            uri: 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/CesiumMilkTruck/glTF-Binary/CesiumMilkTruck.glb',
            minimumPixelSize: 128
        }}
    }});

    viewer.trackedEntity = carEntity;

    // WASD Logic
    let heading = 0;
    const speed = 0.00001;

    document.addEventListener('keydown', (e) => {{
        const pos = carEntity.position.getValue(viewer.clock.currentTime);
        const cart = Cesium.Cartographic.fromCartesian(pos);
        
        if (e.code === 'KeyW') {{
            cart.latitude += speed * Math.cos(heading);
            cart.longitude += speed * Math.sin(heading);
        }}
        if (e.code === 'KeyS') {{
            cart.latitude -= speed * Math.cos(heading);
            cart.longitude -= speed * Math.sin(heading);
        }}
        if (e.code === 'KeyA') heading -= 0.1;
        if (e.code === 'KeyD') heading += 0.1;

        carEntity.position = Cesium.Cartesian3.fromDegrees(
            Cesium.Math.toDegrees(cart.longitude),
            Cesium.Math.toDegrees(cart.latitude),
            0
        );
        carEntity.orientation = Cesium.Transforms.headingPitchRollQuaternion(
            carEntity.position.getValue(viewer.clock.currentTime),
            new Cesium.HeadingPitchRoll(heading, 0, 0)
        );
    }});
"""

# --- 3. RENDER ---
st_cesium(id="spc_game", javascript=cesium_js, height=750)

st.sidebar.markdown("### Controls\\n**W** - Forward\\n**S** - Reverse\\n**A/D** - Steer")
