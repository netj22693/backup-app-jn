import streamlit as st

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