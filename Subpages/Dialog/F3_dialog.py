import streamlit as st
import time
from Subpages.Resources import Assets
from Subpages.Resources_ui import UiConfigAndIcons
from Subpages.Resources_ui_objects import render_function_page, render_description_page, render_specific_page


# ===== Toasts inserted values validations =====

class F3ToastsValidations:
    
    def display_parcel_size_attention_toast(text: str):

        time.sleep(1)

        st.toast(
            f"**Parcel size** is **{text}** for this category. Please double-check but **you may continue, if you like**.",
            duration= UiConfigAndIcons.Toasts.duration["important_notification"],
            icon= UiConfigAndIcons.Toasts.warning
        )

    def display_product_price_attention_toast(text: str):

        time.sleep(1)

        st.toast(
            f"**Product price** is **{text}** for this category. Please double-check but **you may continue, if you like**.",
            duration= UiConfigAndIcons.Toasts.duration["important_notification"],
            icon= UiConfigAndIcons.Toasts.warning
        )

# ===== DIALOGS - process complete or not complete  =====
def final_dialogs_goto():    
    ''
    st.write("**Go to:**")

    render_function_page(
        label = "Function 3B - Invoice visibility",
        page= Assets.Paths.Function.f3b        
    )

    render_function_page(
        label = "Function 4 - Mapping",
        page= Assets.Paths.Function.f4       
    )
    
    render_description_page(
        label = "Function 5 - Description - API",
        page= Assets.Paths.Description.f5       
    )

    render_specific_page("home_page")
    


@st.dialog("Complete!")
def process_done(order_number):
    st.write(f"""
        - File was created and downloaded -> :green[**Complete**]
        - Order **{order_number}** was inserted into DB -> :green[**Complete**]
        """)
    ''
    final_dialogs_goto()


@st.dialog("Insert into DB failed") 
def insert_db_not_complete():
    st.write("""
        - File was created and downloaded -> :green[**Complete**]
        - But Order **was not** inserted into DB -> :red[**Technical issue**]
        """)
    ''
    final_dialogs_goto()


@st.dialog("Technical issue") 
def dialog_not_possible_to_pull_data():
    st.write("""
    - Not possible to pull data from DB. The F3 function is currently not available
    """)