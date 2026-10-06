import streamlit as st

def display_video(path: str):

    try:
        st.video(path)
    except:
        st.warning("Aplogies, issue with loading of the video")