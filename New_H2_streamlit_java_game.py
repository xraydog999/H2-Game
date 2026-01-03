import streamlit as st
import json

st.set_page_config(page_title="H₂ Builder", layout="wide")

st.title("🧪 Build an H₂ Molecule")
st.write("Drag the two **H** atoms and the **–** bond to assemble **H–H**.")

# Initial positions
if "pieces" not in st.session_state:
    st.session_state.pieces = {
        "H1": {"x": 100, "y": 150},
        "H2": {"x": 600, "y": 150},
        "bond": {"x": 350, "y": 150},
    }

# Container for the draggable area
drag_area = st.empty()

# Inject HTML + JS
drag_area.html(
    f"""
    <style>
        #drag-area {{
            width: 800px;
            height: 400px;
            border: 2px solid #ccc;
            position: relative;
            background: white;
            user-select: none;
        }}
        .piece {{
            position: absolute;
            font-size: 80px;
            cursor: grab;
        }}
        .piece:active {{
            cursor: grabbing;
        }}
    </style>

    <div id="drag-area">
        <div id="H1" class="piece" style="left:{st.session_state.pieces['H1']['x']}px; top:{st.session_state.pieces['H1']['y']}px;">H</div>
        <div id="H2" class="piece" style="left:{st.session_state.pieces['H2']['x']}px; top:{st.session_state.pieces['H2']['y']}px;">H</div>
        <div id="bond" class="piece" style="left:{st.session_state.pieces['bond']['x']}px; top:{st.session_state.pieces['bond']['y']}px;">-</div>
    </div>

    <script>
        const pieces = ["H1", "H2", "bond"];
        let active = null;
        let offsetX = 0;
        let offsetY = 0;

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

                active.style.left = (clientX - offsetX) + "px";
                active.style.top = (clientY - offsetY) + "px";
            }}

            function endDrag() {{
                if (!active) return;

                // Send updated positions to Streamlit
                const rect = active.getBoundingClientRect();
                const parent = document.getElementById("drag-area").getBoundingClientRect();

                const x = rect.left - parent.left;
                const y = rect.top - parent.top;

                const payload = {{
                    id: active.id,
                    x: x,
                    y: y
                }};
                window.parent.postMessage({{"type": "streamlit:setComponentValue", "value": payload}}, "*");

                active = null;

                document.removeEventListener("mousemove", drag);
                document.removeEventListener("mouseup", endDrag);
                document.removeEventListener("touchmove", drag);
                document.removeEventListener("touchend", endDrag);
            }}
        }});
    </script>
    """,
    height=450,
)

# Receive JS → Python updates
event = st.experimental_get_query_params().get("streamlit_component_value")

if event:
    try:
        data = json.loads(event[0])
        st.session_state.pieces[data["id"]]["x"] = data["x"]
        st.session_state.pieces[data["id"]]["y"] = data["y"]
    except:
        pass

# Alignment check
def is_aligned():
    H1 = st.session_state.pieces["H1"]
    H2 = st.session_state.pieces["H2"]
    bond = st.session_state.pieces["bond"]

    y_tol = 40
    if abs(H1["y"] - bond["y"]) > y_tol:
        return False
    if abs(H2["y"] - bond["y"]) > y_tol:
        return False

    return H1["x"] < bond["x"] < H2["x"] or H2["x"] < bond["x"] < H1["x"]

if is_aligned():
    st.success("🎉 You built an H₂ molecule!  **H–H**")
