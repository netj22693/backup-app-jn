import streamlit as st
from datetime import date, timedelta
from Subpages.Data.F7_input_data import STATES_UI_GROUPS, STATES_CONFIG
from Subpages.Resources_config import FORMAT_CONFIG
from Subpages.Resources_ui_objects import render_warning_info
from Subpages.Expander.APP_shared_expanders import diplay_how_to_use_filters_expander
from Subpages.Services.F7b_UI_functions import display_state_flow_expander


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


def update_state_multiselect(data):
    quick_select = st.session_state["key_quick_select_state_f7b_tab3"]

    st.session_state["key_mlts_state_f7b_tab3"] = provide_quick_select_states(
        quick_select,
        data["state"]
    )

def multiselect_validation(values: list, text: str):
        if len(values) == 0:
            render_warning_info(f"At least 1 {text} needs to be selected.")


# @st.fragment
def display_filter_options_f7b_tab3(data: dict):

    diplay_how_to_use_filters_expander()
    st.write("")

    country_from = st.multiselect("Country from:", options=data["country"], key="key_mlts_country_from_f7b_tab3")
    multiselect_validation(country_from, "country")

    country_to = st.multiselect("Country to:", options=data["country"], key="key_mlts_country_to_f7b_tab3")
    multiselect_validation(country_to, "country")

    transport = st.multiselect("Transport:", options=data["transport"], key="key_mlts_transport_f7b_tab3")
    multiselect_validation(transport, "transport")

    currency = st.multiselect("Currency:", options=data["currency"], key="key_mlts_currency_f7b_tab3")
    multiselect_validation(currency, "currency")

    st.write("")
    quick_select = st.radio(
        "Offer state:",
        options=data["quick_select_state"],
        key="key_quick_select_state_f7b_tab3",
        on_change=update_state_multiselect,
        args=(data,)
)

    state = st.multiselect(
        "Offer state:",
        label_visibility="collapsed",
        options = data["state"],
        key="key_mlts_state_f7b_tab3"
        )
    multiselect_validation(state, "state")
    display_state_flow_expander(additional_text=False)

    # Date picker
    st.write("")
    checkbox_date = st.checkbox("Filtering based on date", key="key_checkbox_date_f7b_tab3")

    if checkbox_date:
        
        col1, col2 = st.columns(2)

        # default = today - 30 days
        default_date = date.today() - timedelta(days=30)
        max_date = date.today()

        
        date_from = col1.date_input(
            "From",
            value=default_date,
            min_value = data["min_date"],
            max_value = max_date,
            format = FORMAT_CONFIG["date"]["streamlit_widget"],
            key = "key_date_input_1"
        )

        date_to = col2.date_input(
            "To",
            value = max_date,
            min_value = data["min_date"],
            max_value = max_date,
            format = FORMAT_CONFIG["date"]["streamlit_widget"],
            key ="key_date_input_2"
            )
        
        # Fallback info 
        if date_from > date_to:
            render_warning_info("**Date issue** - date **To** is farther in the past than **From**.")

        # UI space -> in case that Date picker is displayed
        st.write("")

    else:
        date_from = None
        date_to = None
        

    # Slider - number of rows
    st.write("")
    number_rows = st.slider("Number of records to be shown", min_value=5, max_value=50, step=5, label_visibility="visible", key="key_sld_number_rows_f7b_tab3")

    return {
        "multiselect": {
            # list
            "country_from": country_from,
            "country_to": country_to,
            "transport": transport,
            "currency": currency,
            "state": state
            },
        "date": {
            "checkbox": checkbox_date, # bool
            "from": date_from, # datetime.date(2025, 11, 12) | None
            "to": date_to, # datetime.date(2025, 11, 12) | None          
        },
        # int
        "number_rows": number_rows
    }


def initiate_session_state_f7b_tab3(data: dict[list | bool | int]):

    '''
    Initiating session states for purpose/possibility of reseting filters
    '''

    if "key_mlts_country_from_f7b_tab3" not in st.session_state:
        st.session_state["key_mlts_country_from_f7b_tab3"] = data["country"]

    if "key_mlts_country_to_f7b_tab3" not in st.session_state:
        st.session_state["key_mlts_country_to_f7b_tab3"] = data["country"]

    if "key_mlts_transport_f7b_tab3" not in st.session_state:
        st.session_state["key_mlts_transport_f7b_tab3"] = data["transport"]

    if "key_mlts_currency_f7b_tab3" not in st.session_state:
        st.session_state["key_mlts_currency_f7b_tab3"] = data["currency"]

    if "key_quick_select_state_f7b_tab3" not in st.session_state:
        st.session_state["key_quick_select_state_f7b_tab3"] = data["quick_select_state"] 

    if "key_mlts_state_f7b_tab3" not in st.session_state:
        st.session_state["key_mlts_state_f7b_tab3"] = data["state"]

    if "key_sld_number_rows_f7b_tab3" not in st.session_state:
        st.session_state["key_sld_number_rows_f7b_tab3"] = data["slider_rows"]

    if "key_checkbox_date_f7b_tab3"  not in st.session_state:
        st.session_state["key_checkbox_date_f7b_tab3"] = data["checkbox_date"]


# ===== Reset button ===== 
def reset_filters_f7b_tab3(data: dict[list | bool | int]):

    '''
    Reset button to clear all applied filters
    '''

    st.session_state["key_mlts_country_from_f7b_tab3"] = data["country"]
    st.session_state["key_mlts_country_to_f7b_tab3"] = data["country"]
    st.session_state["key_mlts_transport_f7b_tab3"] = data["transport"]
    st.session_state["key_mlts_currency_f7b_tab3"] = data["currency"]
    st.session_state["key_quick_select_state_f7b_tab3"] = data["quick_select_state"]
    st.session_state["key_mlts_state_f7b_tab3"] = data["state"]
    st.session_state["key_sld_number_rows_f7b_tab3"] = data["slider_rows"]
    st.session_state["key_checkbox_date_f7b_tab3"] = data["checkbox_date"]