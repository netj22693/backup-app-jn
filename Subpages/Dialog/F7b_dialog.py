import streamlit as st
from Subpages.Resources_ui import UiConfigAndIcons


# ===== Rating function =====
@st.dialog("Complete!")
def rating_complete(rating_result: float | int):
    st.write(f"""
    - Overall rating score: **{rating_result} / 5 ⭐**
    - Rating -> :green[**Complete**]
    """)

@st.dialog("Technical issue") 
def rating_not_saved():
    st.write("""
    - Rating **not** updated -> :red[**Technical issue**]
    """)

@st.dialog("Rating not updated")
def rating_already_submitted():
    st.write("""
    - Rating **not** updated -> :blue[**Another user has already rated this offer**]
    - Please reopen the offer to see the given rating
    """)


# ===== State update =====
@st.dialog("Complete!")
def state_change_complete(offer_id: str, new_status: str):

    rule = {
        "APPROVED": UiConfigAndIcons.UnifiedIcons.approve,
        "REJECTED": UiConfigAndIcons.UnifiedIcons.reject
    }  

    state_icon = rule.get(new_status)

    new_status = new_status.capitalize()

    st.write(f"""
    - The offer **{offer_id}** set as **{new_status}** {state_icon}
    - State update -> :green[**Complete**]
    """)

@st.dialog("Technical issue") 
def state_change_not_complete():
    st.write("""
    - State **not** updated -> :red[**Technical issue**]
    """)

@st.dialog("State not updated") 
def state_change_not_complete_concurrency():
    st.write(f"""
    - State **not** updated -> :blue[**Another user has already changed the state**]
    - Please reopen the offer to see the state
    """)