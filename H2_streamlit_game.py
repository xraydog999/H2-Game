import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="H₂ Builder", layout="wide")

st.title("🧪 Build an H₂ Molecule")
st.write("Drag the two **H** atoms and the **–** bond to assemble **H–H**.")

canvas_width = 800
canvas_height = 400

# Initialize positions only once
if "pieces" not in st.session_state:
    st.session_state.pieces = {
        "H1": {"x": 100, "y": 150},
        "H2": {"x": 600, "y": 150},
        "bond": {"x": 350, "y": 150},
    }

# Draw canvas with NO initial objects
canvas_result = st_canvas(
    fill_color="rgba(0, 0, 0, 0)",
    stroke_width=2,
    stroke_color="#000000",
    background_color="#FFFFFF",
    height=canvas_height,
    width=canvas_width,
    drawing_mode="none",  # no transform mode
    key="canvas",
)

# Draw objects using Streamlit, not the canvas engine
st.markdown(
    f"""
    <div style="position:absolute; left:{st.session_state.pieces['H1']['x']}px; top:{st.session_state.pieces['H1']['y']}px; font-size:80px;">H</div>
    <div style="position:absolute; left:{st.session_state.pieces['H2']['x']}px; top:{st.session_state.pieces['H2']['y']}px; font-size:80px;">H</div>
    <div style="position:absolute; left:{st.session_state.pieces['bond']['x']}px; top:{st.session_state.pieces['bond']['y']}px; font-size:80px;">-</div>
    """,
    unsafe_allow_html=True,
)

# Update positions if user clicks
if canvas_result.json_data is not None:
    click = canvas_result.json_data.get("objects", [])
    if click:
        x = click[-1]["left"]
        y = click[-1]["top"]

        # Move whichever piece is closest to the click
        def dist(p): return abs(p["x"] - x) + abs(p["y"] - y)

        closest = min(st.session_state.pieces, key=lambda k: dist(st.session_state.pieces[k]))
        st.session_state.pieces[closest]["x"] = x
        st.session_state.pieces[closest]["y"] = y

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
