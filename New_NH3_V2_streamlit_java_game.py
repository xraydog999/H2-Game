import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="NH₃ Builder", layout="wide")

st.title("🧪 Build an Ammonia Molecule (NH₃)")
st.write("Drag the atoms, bonds, and lone pair to assemble **H–N–H** with a third H and a lone pair.")

# We still keep positions in session_state in case you want to use them later,
# but the HTML below uses fixed initial positions so we don't need f-strings there.
if "pieces" not in st.session_state:
    st.session_state.pieces = {
        "N": {"x": 350, "y": 150},
        "H1": {"x": 100, "y": 50},
        "H2": {"x": 600, "y": 50},
        "H3": {"x": 350, "y": 300},
        "bond1": {"x": 250, "y": 150},
        "bond2": {"x": 450, "y": 150},
        "bond3": {"x": 350, "y": 225},
        "lone": {"x": 350, "y": 75},
    }

# Pure triple-quoted string: NO f-string, NO Python interpolation here.
components.html(
    """
    <style>
        #drag-area {
            width: 800px;
            height: 450px;
            border: 2px solid #ccc;
            position: relative;
            background: white;
            user-select: none;
            overflow: hidden;
        }

        .piece {
            position: absolute;
            font-size: 70px;
            cursor: grab;
            transition: box-shadow 0.15s ease, transform 0.15s ease;
        }

        .piece:active {
            cursor: grabbing;
        }

        .glow {
            box-shadow: 0 0 18px 4px rgba(0, 150, 255, 0.7);
            transform: scale(1.05);
        }

        .lonepair {
            font-size: 40px;
        }
    </style>

    <div id="drag-area">

        <div id="N" class="piece"
             style
