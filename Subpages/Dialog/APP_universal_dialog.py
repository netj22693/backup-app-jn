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



def display_input_warning_toast():

    '''
    - Warning toast tight to multiselects (0 options selected)
    - Triggered after Apply filters button
    - Currently used in: F3B (TAB3, TAB4) and F7B (TAB3, TAB4)
    '''

    st.toast(
        f"**Incorrect input** - Fix it and use the **Apply filters** button again.",
        duration= UiConfigAndIcons.Toasts.duration["standard_notification"],
        icon= UiConfigAndIcons.Toasts.warning
    )