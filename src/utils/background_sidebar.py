import base64
import streamlit as st

def background_sidebar(image_file: str):
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        section[data-testid="stSidebar"] {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-position: center;
        }}
        section[data-testid="stSidebar"] {{
        backdrop-filter: blur(20px);
    }}
        </style>
        """,
        unsafe_allow_html=True
    )
