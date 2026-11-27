import streamlit as st
from Subpages.Resources_ui import UiConfigAndIcons
from Subpages.Resources import Assets
from Subpages.Resources_ui_objects import render_function_page, render_description_page, render_specific_page


# ==== Warning ====
def display_f2_warning_toast():

    '''
    - Related to F2 XML data validations
    '''

    st.toast(
        f"Invoice data validation not passed. Affected visualizations are marked.",
        duration= UiConfigAndIcons.Toasts.duration["important_notification"],
        icon= UiConfigAndIcons.Toasts.warning
    )


# ==== Final close dialog ====
@st.dialog("Go to:")
def close_function_f2():

    st.session_state.uploader_key_f2 += 1

    render_description_page(
        label = "Function 3 & 4 - Description",
        page= Assets.Paths.Description.f3_f4       
    )

    render_function_page(
        label = "Function 3",
        page= Assets.Paths.Function.f3        
    )

    render_specific_page("home_page")