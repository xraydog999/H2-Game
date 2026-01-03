import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="NH₃ Builder", layout="wide")

st.title("🧪 Build an Ammonia Molecule (NH₃)")
st.write("Drag the atoms, bonds, and lone pair to assemble **H–N–H** with a third H and a lone pair.")

# Initialize positions only once
if "pieces" not in st.session_state:
    st.session_state.pieces = {
        "N": {"x": 350, "y": 150},
        "H1": {"x": 100, "y": 50},
        "H2": {"x": 600, "y": 50},
        "H3": {"x": 350, "y": 300},
        "bond1": {"x": 250, "y": 150},
        "bond2": {"x": 450, "y": 150},
        "bond3": {"x": 350, "y": 225},  # vertical bond
        "lone": {"x": 350, "y": 75},    # lone pair
    }

components.html(
    f"""
    <style>
        #drag-area {{
            width: 800px;
            height: 450px;
            border: 2px solid #ccc;
            position: relative;
            background: white;
            user-select: none;
            overflow: hidden;
        }}

        .piece {{
            position: absolute;
            font-size: 70px;
            cursor: grab;
            transition: box-shadow 0.15s ease, transform 0.15s ease;
        }}

        .piece:active {{
            cursor: grabbing;
        }}

        .glow {{
            box-shadow: 0 0 18px 4px rgba(0, 150, 255, 0.7);
            transform: scale(1.05);
        }}

        .lonepair {{
            font-size: 40px;
        }}
    </style>

    <div id="drag-area">

        <div id="N" class="piece"
            style="left:{st.session_state.pieces['N']['x']}px;
                   top:{st.session_state.pieces['N']['y']}px;">N</div>

        <div id="H1" class="piece"
            style="left:{st.session_state.pieces['H1']['x']}px;
                   top:{st.session_state.pieces['H1']['y']}px;">H</div>

        <div id="H2" class="piece"
            style="left:{st.session_state.pieces['H2']['x']}px;
                   top:{st.session_state.pieces['H2']['y']}px;">H</div>

        <div id="H3" class="piece"
            style="left:{st.session_state.pieces['H3']['x']}px;
                   top:{st.session_state.pieces['H3']['y']}px;">H</div>

        <div id="bond1" class="piece"
            style="left:{st.session_state.pieces['bond1']['x']}px;
                   top:{st.session_state.pieces['bond1']['y']}px;">-</div>

        <div id="bond2" class="piece"
            style="left:{st.session_state.pieces['bond2']['x']}px;
                   top:{st.session_state.pieces['bond2']['y']}px;">-</div>

        <div id="bond3" class="piece"
            style="left:{st.session_state.pieces['bond3']['x']}px;
                   top:{st.session_state.pieces['bond3']['y']}px;
                   font-size: 90px;">|</div>

        <div id="lone" class="piece lonepair"
            style="left:{st.session_state.pieces['lone']['x']}px;
                   top:{st.session_state.pieces['lone']['y']}px;">••</div>

    </div>

    <script>
        const pieces = ["N", "H1", "H2", "H3", "bond1", "bond2", "bond3", "lone"];
        let active = null;
        let offsetX = 0;
        let offsetY = 0;

        const targets = {{
            "N": {{x: {st.session_state.pieces['N']['x']}, y: {st.session_state.pieces['N']['y']}}},
            "H1": {{x: 250, y: 150}},
            "H2": {{x: 450, y: 150}},
            "H3": {{x: 350, y: 260}},
            "bond1": {{x: 300, y: 150}},
            "bond2": {{x: 400, y: 150}},
            "bond3": {{x: 350, y: 200}},
            "lone": {{x: 350, y: 80}}
        }};

        const snapDistance = 40;

        pieces.forEach(id => {{
            const el = document.getElementById(id);

            el.addEventListener("mousedown", startDrag);
            el.addEventListener("touchstart", startDrag);

            function startDrag(e) {{
                active = el;
                const rect = el.getBoundingClientRect();
                const clientX = e.touches ? e.touches[0].clientX : e.clientX;
                const clientY = e.touches ? e.touches[0].clientY : e.clientY;
                offsetX = clientX - rect.left;
                offsetY = clientY - rect.top;

                document.addEventListener("mousemove", drag);
                document.addEventListener("mouseup", endDrag);
                document.addEventListener("touchmove", drag);
                document.addEventListener("touchend", endDrag);
            }}

            function drag(e) {{
                if (!active) return;

                const clientX = e.touches ? e.touches[0].clientX : e.clientX;
                const clientY = e.touches ? e.touches[0].clientY : e.clientY;

                const x = clientX - offsetX;
                const y = clientY - offsetY;

                active.style.left = x + "px";
                active.style.top = y + "px";

                const t = targets[active.id];
                const dx = t.x - x;
                const dy = t.y - y;
                const dist = Math.sqrt(dx*dx + dy*dy);

                if (dist < snapDistance * 1.5) {{
                    active.classList.add("glow");
                }} else {{
                    active.classList.remove("glow");
                }}
            }}

            function endDrag() {{
                if (!active) return;

                const rect = active.getBoundingClientRect();
                const parent = document.getElementById("drag-area").getBoundingClientRect();

                let x = rect.left - parent.left;
                let y = rect.top - parent.top;

                const t = targets[active.id];
                const dx = t.x - x;
                const dy = t.y - y;
                const dist = Math.sqrt(dx*dx + dy*dy);

                if (dist < snapDistance) {{
                    x = t.x;
                    y = t.y;
                    active.style.left = x + "px";
                    active.style.top = y + "px";
                }}

                active.classList.remove("glow");

                const payload = {{
                    id: active.id,
                    x: x,
                    y: y
                }};

                window.parent.postMessage(
                    {{
                        "type": "streamlit:setComponentValue",
                        "value": payload
                    }},
                    "*"
                );

                active = null;

                document.removeEventListener("mousemove", drag);
                document.removeEventListener("mouseup", endDrag);
                document.removeEventListener("touchmove", drag);
                document.removeEventListener("touchend", endDrag);
            }}
        }});
    </script>
    """,
    height=500,
)

event = st.experimental_get_query_params().get("streamlit_component_value")

if event:
    try:
        data = json.loads(event[0])
        st.session_state.pieces[data["id"]]["x"] = data["x"]
        st.session_state.pieces[data["id"]]["y"] = data["y"]
    except Exception:
        pass

def is_ammonia():
    N = st.session_state.pieces["N"]
    H1 = st.session_state.pieces["H1"]
    H2 = st.session_state.pieces["H2"]
    H3 = st.session_state.pieces["H3"]
    lone = st.session_state.pieces["lone"]

    y_tol = 60
    x_tol = 120

    lone_ok = abs(lone["x"] - N["x"]) < x_tol and lone["y"] < N["y"]
    h1_ok = abs(H1["y"] - N["y"]) < y_tol
    h2_ok = abs(H2["y"] - N["y"]) < y_tol
    h3_ok = H3["y"] > N["y"] and abs(H3["x"] - N["x"]) < x_tol

    return lone_ok and h1_ok and h2_ok and h3_ok

if is_ammonia():
    st.success("🎉 You built an ammonia molecule!  **NH₃**")
