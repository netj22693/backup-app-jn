import streamlit as st
import time
from Subpages.Resources_ui import UiConfigAndIcons

# ===== Toast =====
def display_download_complete_toast():

    time.sleep(1)

    st.toast(
        "File download complete.",
        duration= UiConfigAndIcons.Toasts.duration["standard_notification"],
        icon= UiConfigAndIcons.Toasts.success
    )