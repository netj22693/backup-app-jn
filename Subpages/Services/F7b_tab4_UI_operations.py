import streamlit as st
from datetime import date, timedelta
from Subpages.Data.F7_input_data import STATES_UI_GROUPS, STATES_CONFIG
from Subpages.Resources_ui_objects import render_warning_info
from Subpages.Resources_config import FORMAT_CONFIG
from Subpages.Expander.APP_shared_expanders import diplay_how_to_use_filters_expander

def provide_quick_select_states(quick_select: str, all_options: list[str]):
    for key, value in STATES_UI_GROUPS.items():
        if value == quick_select:
            option_number = key

    if option_number == 0:
        return all_options

    else: 
        options = []
        for value in STATES_CONFIG.values():
            ui_group = value["ui_group"]

            if ui_group == option_number:
                state = value["name"]
                options.append(state)

        options.sort()

        return options


def update_state_multiselect(data: dict):
    quick_select = st.session_state["key_quick_select_state_f7b_tab4"]

    st.session_state["key_mlts_state_f7b_tab4"] = provide_quick_select_states(
        quick_select,
        data["state"]
    )


def multiselect_validation(values: list, text: str):
        if len(values) == 0:
            render_warning_info(f"At least 1 {text} needs to be selected.")


@st.fragment()
def display_filter_options_f7b_tab4(data: dict) -> dict:

    diplay_how_to_use_filters_expander() 
    st.write("")

    date_selected = st.radio(
        "Date filter",
        options=[
            "All offers - no specific date",
            "Date range"
            ], 
        label_visibility="collapsed",
        key="key_radio_date_f7b_tab4"
        )


    if date_selected == "Date range":

        date_applicable = True
        
        col1, col2 = st.columns(2)

        # Min date allowed
        min_date = data["min_date"]

        # default = today - 30 days
        default_date = date.today() - timedelta(days=30)
        max_date = date.today()

        
        date_from = col1.date_input(
            "From",
            value=default_date,
            min_value = min_date,
            max_value = max_date,
            format = FORMAT_CONFIG["date"]["streamlit_widget"],
            key = "key_date_input_from_f7b_tab4"
        )

        date_to = col2.date_input(
            "To",
            value = max_date,
            min_value = min_date,
            max_value = max_date,
            format = FORMAT_CONFIG["date"]["streamlit_widget"],
            key = "key_date_input_to_f7b_tab4"
        )
        
        # Fallback info 
        if date_from > date_to:
            render_warning_info("**Date issue** - date **To** is farther in the past than **From**.")

    else:
        date_applicable = False
        date_from = None
        date_to = None


    st.write("")
    quick_select = st.radio(
        "Offer state:",
        options=data["quick_select_state"],
        key="key_quick_select_state_f7b_tab4",
        on_change=update_state_multiselect,
        args=(data,)
    )

    state = st.multiselect(
        "Offer state:",
        label_visibility="collapsed",
        options = data["state"],
        key="key_mlts_state_f7b_tab4"
        )
    multiselect_validation(state, "state")


    # Ui outcome dict build
    final =  {
        "multiselect": {
            "state": state # list
            },
        "date": {
            "applicable": date_applicable,      # bool
            "from": date_from,                  # datetime.date(2025, 11, 12) | None
            "to": date_to,                      # datetime.date(2025, 11, 12) | None          
        }
    }

    return final
          
           


def initiate_session_state_f7b_tab4(data: dict):

    '''
    - Initiating session states for purpose/possibility of reseting filters
    '''

    # Multiselects
    if "key_mlts_state_f7b_tab4" not in st.session_state:
        st.session_state["key_mlts_state_f7b_tab4"] = data["state"]

    # Radios
    if "key_radio_date_f7b_tab4" not in st.session_state:
        st.session_state["key_radio_date_f7b_tab4"] = "All invoices - no specific date"

    if "key_quick_select_state_f7b_tab4" not in st.session_state:
        st.session_state["key_quick_select_state_f7b_tab4"] = data["quick_select_state"]


# ===== Reset button ===== 
def reset_filters_f7b_tab4(data: dict[list | bool | int]):

    '''
    Reset button to clear all applied filters
    '''

    # Multiselects
    st.session_state["key_mlts_state_f7b_tab4"] = data["state"]

    # Radios
    st.session_state["key_radio_date_f7b_tab4"] = "All invoices - no specific date"
    st.session_state["key_quick_select_state_f7b_tab4"] = data["quick_select_state"]