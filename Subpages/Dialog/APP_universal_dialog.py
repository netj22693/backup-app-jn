import streamlit as st
import time

# ===== Toast =====
def display_download_complete_toast():

    time.sleep(1)

    st.toast(
        "File download complete.",
        duration= 10,
        icon=":material/check:"
    )