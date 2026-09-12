import streamlit as st


# ===== Rating function =====
@st.dialog("Complete!")
def rating_complete(rating_result: float | int):
    st.write(f"""
    - Overall rating score: **{rating_result} / 5 ⭐**
    - Rating saved into DB -> :green[**Complete**]
    """)

@st.dialog("Technical issue") 
def rating_not_saved():
    st.write("""
    - Rating process not complete -> :red[**Technical issue**]
    """)

@st.dialog("Rating not saved")
def rating_already_submitted():
    st.write("""
    - Rating process **not** complete -> :blue[**Rating already given**]
    - There was a **concurrent user who gave the ratting** at the same time
    - **Search/reopen the offer again** to see the rating
    """)


# ===== State update =====
@st.dialog("Complete!")
def state_change_complete(offer_id: str, new_status: str):
    st.write(f"""
        - State change -> :green[**Complete**]
        - The offer **{offer_id}** has been changed to **{new_status}**
        """)

@st.dialog("Technical issue") 
def state_change_not_complete():
    st.write("""
        - State change **was not** complete -> :red[**Technical issue**]
        """)

@st.dialog("Status not updated") 
def state_change_not_concurrency(offer_id: str):
    st.write(f"""
    - Status **not** updated {offer_id} -> :blue[**Already Approved/Rejected**]
    - There was a **concurrent user who updated** at the same time
    - **Search/reopen the offer again** to see the state
    """)