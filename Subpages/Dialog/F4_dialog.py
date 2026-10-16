import streamlit as st
import time
from Subpages.Resources import Assets
from Subpages.Resources_ui import UiConfigAndIcons
from Subpages.Resources_ui_objects import render_function_page, render_description_page, render_specific_page


# ===== Toast =====
def display_transformation_not_complete_toast():

    time.sleep(1)

    st.toast(
        "Transformation process **not complete** due to **ivalid uploaded file**.",
        duration= UiConfigAndIcons.Toasts.duration["standard_notification"],
        icon= UiConfigAndIcons.Toasts.warning
    )


def display_transformation_complete_toast():

    time.sleep(1)

    st.toast(
        "Transformation process **complete**. You can **download** the file in different format.",
        duration= UiConfigAndIcons.Toasts.duration["standard_notification"],
        icon= UiConfigAndIcons.Toasts.success
    )


# ===== Dialogs =====
def final_dialogs_goto():
    ''
    st.write("**Go to:**")

    render_function_page(
        label = "Function F3B - Invoice visibility",
        page= Assets.Paths.Function.f3b        
    )

    render_description_page(
        label = "Function F5 - Description",
        page= Assets.Paths.Description.f5        
    )

    render_function_page(
        label = "Function F5 - Exchange Rate",
        page= Assets.Paths.Function.f5    
    )

    render_specific_page("home_page")



# Final Dialog boxes
@st.dialog("Insert into DB failed") 
def insert_db_not_complete():
	st.write("""
		- Mapping complete -> :green[**Complete**]
		- But log about this change was not inserted into DB -> :red[**Technical issue**]
		""")
	
	final_dialogs_goto()


@st.dialog("Complete!")
def process_done():
	st.write(f"""
		- Mapping complete -> :green[**Complete**]
		- Log about this change was inserted into DB -> :green[**Complete**]
		""")
	
	final_dialogs_goto()