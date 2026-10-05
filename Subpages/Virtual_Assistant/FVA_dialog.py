import streamlit as st
import time


# ===== Toast =====
def display_feedback_not_saved_toast():

    time.sleep(1)

    st.toast(
        "Technical issue. Your feedback was **not saved** into DB",
        duration= 10,
        icon=":material/warning:"
    )


def display_feedback_saved_toast():

    time.sleep(1)

    st.toast(
        "Your feedback was **saved**. Thank you!",
        duration= 10,
        icon=":material/check:"
    )