import streamlit as st
from Subpages.Resources import Assets
from Subpages.Resources_ui_objects import render_function_page, render_description_page, render_specific_page

# ==== Final close dialog ====
@st.dialog("Go to:")
def close_function():

    ''
    render_description_page(
        label = "Function 3 & 4 - Description",
        page= Assets.Paths.Description.f3_f4       
    )

    render_function_page(
        label = "Function 3",
        page= Assets.Paths.Function.f3        
    )

    render_specific_page("home_page")