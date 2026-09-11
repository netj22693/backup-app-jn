import streamlit as st
from Subpages.Resources import Assets

# ==== Final close dialog ====
@st.dialog("Go to:")
def close_function():

    ''
    st.page_link(
        label = "Function 3 & 4 - Description",
        page= Assets.Paths.Description.f3_f4,
        help="The button will redirect to the relevant page within this app.",
        width="stretch",
        icon=":material/code:",
        )

    st.page_link(
        label = "Function 3",
        page= Assets.Paths.Function.f3,
        help="The button will redirect to the relevant page within this app.",
        width="stretch",
        icon=":material/play_circle:",
        )
    
    st.page_link(
        label = "Home page",
        page= Assets.Paths.App.main_page,
        help="The button will redirect to the relevant page within this app.",
        width="stretch",
        icon=":material/home:",
        )