import streamlit.components.v1 as components

components.html(
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
        // JS drag code here...
    </script>
    """,
    height=450,
)
