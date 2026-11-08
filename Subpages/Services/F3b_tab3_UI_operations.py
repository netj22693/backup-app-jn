import streamlit as st
from datetime import date, timedelta
from Subpages.Data.F3_F3B_UI_config_data import CONFIG_UI_INPUTS
from Subpages.Resources_config import FORMAT_CONFIG
from Subpages.Resources_ui_objects import render_warning_info
from Subpages.Expander.APP_shared_expanders import diplay_how_to_use_filters_expander

def multiselect_validation(values: list, text: str):
        if len(values) == 0:
            render_warning_info(f"At least 1 {text} needs to be selected.")


@st.fragment
def display_filter_options_f3b_tab3(data: dict):     

    diplay_how_to_use_filters_expander() 
    st.write("")

    # Multiselect - category
    selected_category = st.multiselect(
        f"{CONFIG_UI_INPUTS['category']['icon']} {CONFIG_UI_INPUTS['category']['name']}",
        options=data['category_options'],
        key="key_category_options_f3b_tab3"
        )
    multiselect_validation(selected_category, "category")

    # Multiselect - currency
    selected_currency = st.multiselect(
        f"{CONFIG_UI_INPUTS['currency']['icon']} {CONFIG_UI_INPUTS['currency']['name']}",
        options=data['currency_options'],
        key="key_currency_options_f3b_tab3"
        )

    multiselect_validation(selected_currency, "currency")

    # Multiselect - additional service
    selected_additional_service = st.multiselect(
        f"{CONFIG_UI_INPUTS['additional_service']['icon']} {CONFIG_UI_INPUTS['additional_service']['name']}",
        options=data['additional_service_options'],
        key="key_additional_service_options_f3b_tab3"
        )

    multiselect_validation(selected_additional_service, "service option")

    # Multiselect - country
    selected_country = st.multiselect(
        f"{CONFIG_UI_INPUTS['country']['icon']} {CONFIG_UI_INPUTS['country']['name']}",
        options=data['country_options'],
        key="key_country_options_f3b_tab3"
        )

    multiselect_validation(selected_country, "country")

    # Multiselect - transport company
    selected_transport_company = st.multiselect(
        f"{CONFIG_UI_INPUTS['transport_company']['icon']} {CONFIG_UI_INPUTS['transport_company']['name']}",
        options=data['transport_company_options'],
        key="key_transport_company_options_f3b_tab3"
        )

    multiselect_validation(selected_transport_company, "transport company")

    # Multiselect - parcel size
    selected_parcel_size = st.multiselect(
        f"{CONFIG_UI_INPUTS['parcel_size']['icon']} {CONFIG_UI_INPUTS['parcel_size']['name']}",
        options=data['parcel_size_options'],
        key="key_parcel_size_options_f3b_tab3"
        )

    multiselect_validation(selected_parcel_size, "parcel size")

    # Multiselect - file format
    selected_file_format = st.multiselect(
        f"{CONFIG_UI_INPUTS['file_format']['icon']} {CONFIG_UI_INPUTS['file_format']['name']}",
        options=data['file_format_options'],
        key="key_file_format_options_f3b_tab3"
        )

    multiselect_validation(selected_file_format, "file format")


    # Date picker
    st.write("")
    checkbox_date = st.checkbox("Filtering based on date", key="key_checkbox_date_f3b_tab3")

    if checkbox_date == True:
        
        col1, col2 = st.columns(2)

        # Min date allowed
        min_date = data['min_date'] 

        # default = today - 30 days
        default_date = date.today() - timedelta(days=30)
        max_date = date.today()

        
        picked_date_from = col1.date_input(
            "From",
            value=default_date,
            min_value = min_date,
            max_value = max_date,
            format = FORMAT_CONFIG["date"]["streamlit_widget"],
            key = "key_date_input_1"
        )

        picked_date_to = col2.date_input(
            "To",
            value = max_date,
            min_value = min_date,
            max_value = max_date,
            format = FORMAT_CONFIG["date"]["streamlit_widget"],
            key ="key_date_input_2")
        
        # Fallback info 
        if picked_date_from > picked_date_to:
            render_warning_info("**Date issue** - date **To** is farther in the past than **From**.")

        # UI space -> in case that Date picker is displayed
        st.write("")
    else: 
        picked_date_from = None
        picked_date_to = None

    # Text search
    checkbox_text = st.checkbox("Filtering based on text search", key="key_checkbox_text_f3b_tab3")

    if checkbox_text == True:
        customer = st.text_input(
            f"{CONFIG_UI_INPUTS['customer']['icon']} {CONFIG_UI_INPUTS['customer']['name']}",
            max_chars=CONFIG_UI_INPUTS['customer']['limit'],
            help=CONFIG_UI_INPUTS['customer']['help_f3b']
            ).strip()

        product = st.text_input(
            f"{CONFIG_UI_INPUTS['product']['icon']} {CONFIG_UI_INPUTS['product']['name']}",
            max_chars=CONFIG_UI_INPUTS['product']['limit'],
            help=CONFIG_UI_INPUTS['product']['help_f3b']
            ).strip()

    else: 
        customer = None
        product = None

    # Slider - number of rows
    st.write("")
    number_rows = st.slider("Number of records to be shown", min_value=5, max_value=50, step=5, label_visibility="visible", key="key_sld_number_rows_f3b_tab3")


    return {
        "multiselect": {
            # list
            "category": selected_category,
            "currency": selected_currency,
            "additional_service": selected_additional_service,
            "country": selected_country,
            "transport_company": selected_transport_company,
            "parcel_size": selected_parcel_size,
            "file_format": selected_file_format,
            },

        # ** Default value -> will change, if text input passes validation
        "text":{
            "checkbox": checkbox_text,          # bool
            "customer": customer,               # str | None
            "customer_applicable": False,       # **
            "product": product,                 # str | None
            "product_applicable": False,        # ** 
        },
        "date": {
            "checkbox": checkbox_date, # bool
            "from": picked_date_from, # datetime.date(2025, 11, 12) | None
            "to": picked_date_to, # datetime.date(2025, 11, 12) | None          
        },
        # int
        "number_rows": number_rows
    }


def initiate_session_state_f3b_tab3(data: dict[str, list | bool | int]):

    '''
    - Initiating session states for purpose/possibility of reseting filters
    '''

    if "key_category_options_f3b_tab3" not in st.session_state:
        st.session_state["key_category_options_f3b_tab3"] = data["category_options"]

    if "key_transport_company_options_f3b_tab3" not in st.session_state:
        st.session_state["key_transport_company_options_f3b_tab3"] = data["transport_company_options"]

    if "key_currency_options_f3b_tab3" not in st.session_state:
        st.session_state["key_currency_options_f3b_tab3"] = data["currency_options"]

    if "key_additional_service_options_f3b_tab3" not in st.session_state:
        st.session_state["key_additional_service_options_f3b_tab3"] = data["additional_service_options"]

    if "key_country_options_f3b_tab3" not in st.session_state:
        st.session_state["key_country_options_f3b_tab3"] = data["country_options"]

    if "key_parcel_size_options_f3b_tab3"  not in st.session_state:
        st.session_state["key_parcel_size_options_f3b_tab3"] = data["parcel_size_options"]

    if "key_file_format_options_f3b_tab3"  not in st.session_state:
        st.session_state["key_file_format_options_f3b_tab3"] = data["file_format_options"]

    if "key_sld_number_rows_f3b_tab3" not in st.session_state:
        st.session_state["key_sld_number_rows_f3b_tab3"] = data["number_rows"]
    
    if "key_checkbox_date_f3b_tab3"  not in st.session_state:
        st.session_state["key_checkbox_date_f3b_tab3"] = data["checkbox_date"]

    if "key_checkbox_text_f3b_tab3"  not in st.session_state:
        st.session_state["key_checkbox_text_f3b_tab3"] = data["checkbox_text"]


def reset_filters_f3b_tab3(data: dict[str, list | bool | int]):

    '''
    Reset button to clear all applied filters
    '''

    st.session_state["key_category_options_f3b_tab3"] = data["category_options"]
    st.session_state["key_transport_company_options_f3b_tab3"] = data["transport_company_options"]
    st.session_state["key_currency_options_f3b_tab3"] = data["currency_options"]
    st.session_state["key_additional_service_options_f3b_tab3"] = data["additional_service_options"]
    st.session_state["key_country_options_f3b_tab3"] = data["country_options"]
    st.session_state["key_parcel_size_options_f3b_tab3"] = data["parcel_size_options"]
    st.session_state["key_file_format_options_f3b_tab3"] = data["file_format_options"]
    st.session_state["key_sld_number_rows_f3b_tab3"] = data["number_rows"]
    st.session_state["key_checkbox_date_f3b_tab3"] = data["checkbox_date"]
    st.session_state["key_checkbox_text_f3b_tab3"] = data["checkbox_text"]