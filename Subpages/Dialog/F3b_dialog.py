import streamlit as st
from Subpages.Resources_ui import UiConfigAndIcons

def display_input_warning_toast():

    st.toast(
        f"**Incorrect input** - Fix it and use the **Apply filters button** again.",
        duration= UiConfigAndIcons.Toasts.duration["standard_notification"],
        icon= UiConfigAndIcons.Toasts.warning
    )