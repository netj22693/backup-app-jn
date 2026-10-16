import streamlit as st
from Subpages.Resources import Assets
from Subpages.Resources_ui_objects import render_function_page, render_description_page, render_specific_page

def final_dialogs_goto():
    ''
    st.write("**Go to:**")

    render_function_page(
        label = "Function F7B - Offer visibility",
        page= Assets.Paths.Function.f7b        
    )

    render_description_page(
        label = "Function F8 - Description",
        page= Assets.Paths.Description.f8        
    )

    render_specific_page("home_page")


@st.dialog("Complete!")
def process_done(offer_number_input):
    st.write(f"""
        - PDF offer was generated -> :green[**Complete**]
        - The offer **{offer_number_input}** was inserted into DB -> :green[**Complete**]
        """)
    ''
    final_dialogs_goto()


@st.dialog("Insert into DB failed") 
def insert_db_not_complete():
    st.write("""
        - PDF offer was generated -> :green[**Complete**]
        - But the offer **was not** inserted into DB -> :red[**Technical issue**]
        """)
    ''
    final_dialogs_goto()