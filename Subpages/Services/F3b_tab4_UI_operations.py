import streamlit as st
from datetime import date, timedelta
from sqlalchemy import Engine
from Subpages.Resources_config import FORMAT_CONFIG
from Subpages.Resources_ui_objects import render_warning_info
from Subpages.Expander.APP_shared_expanders import diplay_how_to_use_filters_expander

@st.fragment()
def display_filter_options_f3b_tab4(min_date: date) -> dict:

    diplay_how_to_use_filters_expander() 
    st.write("")

    selected_option = st.radio(
        "Filter",
        label_visibility="collapsed",
        options=[
            "All invoices - no specific date",
            "Date range"
            ],
        key="key_radio_date_f3b_tab4"
        )
    

    result = {
        "date_applicable": False, 
        "date_from": None, 
        "date_to": None,
        "date_validation": None
    }

    if selected_option == "Date range":

        col1, col2 = st.columns(2)

        # default = today - 30 days
        default_date = date.today() - timedelta(days=30)
        max_date = date.today()

        
        date_from = col1.date_input(
            "From",
            value = default_date,
            min_value = min_date,
            max_value = max_date,
            format = FORMAT_CONFIG["date"]["streamlit_widget"],
            key = "key_date_input_tab4_1"
        )

        date_to = col2.date_input(
            "To",
            value = max_date,
            min_value = min_date,
            max_value = max_date,
            format = FORMAT_CONFIG["date"]["streamlit_widget"],
            key ="key_date_input_tab4_2"
            )
        
        # Extending SQL query date filter
        result.update({"date_applicable": True})

        # Fallback info 
        if date_from > date_to:
            render_warning_info("**Date issue** - date **To** is farther in the past than **From**.")
            result.update({"date_validation": False})

        else:
            result.update({
                "date_validation": True,
                "date_from": date_from,
                "date_to": date_to
                })


    return result


def initiate_session_state_f3b_tab4():

    '''
    - Initiating session states for purpose/possibility of reseting filters
    '''
    
    if "key_radio_date_f3b_tab4" not in st.session_state:
        st.session_state["key_radio_date_f3b_tab4"] = "All invoices - no specific date"


def reset_filters_f3b_tab4():

    '''
    Reset button to clear all applied filters
    '''

    st.session_state["key_radio_date_f3b_tab4"] = "All invoices - no specific date"