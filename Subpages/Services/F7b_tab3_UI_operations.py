import streamlit as st
import math
from datetime import date, timedelta
from Subpages.Data.F7_input_data import STATES_UI_GROUPS, STATES_CONFIG
from Subpages.Resources_config import FORMAT_CONFIG
from Subpages.Resources_ui_objects import render_warning_info
from Subpages.Expander.APP_shared_expanders import diplay_how_to_use_filters_expander
from Subpages.Services.F7b_UI_functions import display_state_flow_expander
from Subpages.Universal.Universal_functions import format_integer_number


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


def get_slider_step(value: int | float):
    magnitude = 10 ** math.floor(math.log10(value))
    return magnitude / 10


@st.fragment
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
    st.write("")


    # Date picker
    toggle_date = st.toggle("Date", key="key_toggle_date_f7b_tab3")

    if toggle_date:
        
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
        st.write("")

    else:
        date_from = None
        date_to = None


    # Price slider
    toggle_price = st.toggle("Price", key="key_toggle_price_f7b_tab3")

    if toggle_price:

        price_range = {}

        if len(currency) == 0:
            multiselect_validation(currency, "currency")
            st.write("")
            st.write("")

        else:
            count = 1
            for item in currency:
                min_value= int(data["currency_values"][item]["min"])
                max_value = int(data["currency_values"][item]["max"])

                avg_value = data["currency_values"][item]["avg"]
                avg_p = format_integer_number(avg_value )

                median_value = data["currency_values"][item]["median"]
                median_p = format_integer_number(median_value)

                step = int(get_slider_step(avg_value))

                slider_min = math.floor(min_value / step) * step
                if slider_min <= 0:
                    slider_min = math.floor(min_value / step * 10) * 10 

                slider_max = math.ceil(max_value / step) * step

                slider_price = st.slider(
                    f"{item} (avg: {avg_p} ; median: {median_p})",
                    min_value=int(slider_min),
                    max_value=int(slider_max),
                    value=(int(slider_min), int(slider_max)),
                    step=step,
                    key=f"key_sld_price_{item}_f7b_tab3"
                )

                price_range[item] = {
                    "min" : slider_price[0],
                    "max" : slider_price[1],
                }

                # UI space -> in case that Date picker is displayed
                if count == len(currency):
                    st.write("")
                    st.write("")
                else:
                    count += 1

                
    # Filtering based on delivery service
    toggle_delivery_service = st.toggle("Delivery service",key="key_toggle_delivery_service_f7b_tab3")

    if toggle_delivery_service:

        delivery_service = st.multiselect("Delivery service:", options=data["delivery_service"], label_visibility="collapsed", key="key_mlts_delivery_service_f7b_tab3")
        multiselect_validation(delivery_service, "currency")

        # UI space -> in case that Date picker is displayed
        st.write("")
        st.write("")

    # Filtering based on DTD
    toggle_dtd = st.toggle("Door-to-Door", key="key_toggle_dtd_f7b_tab3") 

    if toggle_dtd:

        door_to_door = st.multiselect("Door-to-Door:", options=data["door_to_door"], label_visibility="collapsed", key="key_mlts_dtd_service_f7b_tab3")
        multiselect_validation(door_to_door, "DtD option")
     

    # Slider - number of rows
    st.write("") 
    st.write("")
    number_rows = st.slider("Number of records to display", min_value=5, max_value=50, step=5, label_visibility="visible", key="key_sld_number_rows_f7b_tab3")

    # Ui outcome dict build
    final =  {
        "multiselect": {
            # list
            "country_from": country_from,
            "country_to": country_to,
            "transport": transport,
            "currency": currency,
            "state": state
            },
        "date": {
            "applicable": toggle_date, # bool
            "from": date_from, # datetime.date(2025, 11, 12) | None
            "to": date_to, # datetime.date(2025, 11, 12) | None          
        },
        # int
        "number_rows": number_rows,
        "price": {
            "applicable": False
        },
        "delivery_service": {
            "applicable": False
        },
        "door_to_door": {
            "applicable": False
        }
    }

    if toggle_price:
        final["price"]["applicable"] = True
        final["price"]["range"] = price_range

    # Note: outputs appeneded to the "multiselect" object due to:
    # 1) UI Output validation is designed to interate trhought it
    # 2) Validation DB vs User input also 
    if toggle_delivery_service:
        final["delivery_service"]["applicable"] = True
        final["multiselect"]["delivery_service"] = delivery_service # goes to multiselect 

    if toggle_dtd:
        final["door_to_door"]["applicable"] = True
        final["multiselect"]["door_to_door"] = door_to_door # goes to multiselect 

    return final 


def initiate_session_state_f7b_tab3(data: dict[list | bool | int]):

    '''
    Initiating session states for purpose/possibility of reseting filters
    '''

    # Multiselects
    if "key_mlts_country_from_f7b_tab3" not in st.session_state:
        st.session_state["key_mlts_country_from_f7b_tab3"] = data["country"]

    if "key_mlts_country_to_f7b_tab3" not in st.session_state:
        st.session_state["key_mlts_country_to_f7b_tab3"] = data["country"]

    if "key_mlts_transport_f7b_tab3" not in st.session_state:
        st.session_state["key_mlts_transport_f7b_tab3"] = data["transport"]

    if "key_mlts_currency_f7b_tab3" not in st.session_state:
        st.session_state["key_mlts_currency_f7b_tab3"] = data["currency"]

    if "key_mlts_state_f7b_tab3" not in st.session_state:
        st.session_state["key_mlts_state_f7b_tab3"] = data["state"]

    if "key_mlts_delivery_service_f7b_tab3" not in st.session_state:
        st.session_state["key_mlts_delivery_service_f7b_tab3"] = data["delivery_service"]

    if "key_mlts_dtd_service_f7b_tab3" not in st.session_state:
        st.session_state["key_mlts_dtd_service_f7b_tab3"] = data["door_to_door"]

    # Radios
    if "key_quick_select_state_f7b_tab3" not in st.session_state:
        st.session_state["key_quick_select_state_f7b_tab3"] = data["quick_select_state"]

    # Sliders
    if "key_sld_number_rows_f7b_tab3" not in st.session_state:
        st.session_state["key_sld_number_rows_f7b_tab3"] = data["slider_rows"]

    # Toggles
    if "key_toggle_date_f7b_tab3"  not in st.session_state:
        st.session_state["key_toggle_date_f7b_tab3"] = data["toggle"]["date"]

    if "key_toggle_delivery_service_f7b_tab3"  not in st.session_state:
        st.session_state["key_toggle_delivery_service_f7b_tab3"] = data["toggle"]["delivery_service"]

    if "key_toggle_price_f7b_tab3"  not in st.session_state:
        st.session_state["key_toggle_price_f7b_tab3"] = data["toggle"]["price"]

    if "key_toggle_dtd_f7b_tab3"  not in st.session_state:
        st.session_state["key_toggle_dtd_f7b_tab3"] = data["toggle"]["dtd"]


# ===== Reset button ===== 
def reset_filters_f7b_tab3(data: dict[list | bool | int]):

    '''
    Reset button to clear all applied filters
    '''

    # Multiselects
    st.session_state["key_mlts_country_from_f7b_tab3"] = data["country"]
    st.session_state["key_mlts_country_to_f7b_tab3"] = data["country"]
    st.session_state["key_mlts_transport_f7b_tab3"] = data["transport"]
    st.session_state["key_mlts_currency_f7b_tab3"] = data["currency"]
    st.session_state["key_mlts_state_f7b_tab3"] = data["state"]
    st.session_state["key_mlts_delivery_service_f7b_tab3"] = data["delivery_service"]
    st.session_state["key_mlts_dtd_service_f7b_tab3"] = data["door_to_door"]

    # Radios
    st.session_state["key_quick_select_state_f7b_tab3"] = data["quick_select_state"]

    # Sliders
    st.session_state["key_sld_number_rows_f7b_tab3"] = data["slider_rows"]

    # Toggles
    st.session_state["key_toggle_date_f7b_tab3"] = data["toggle"]["date"]
    st.session_state["key_toggle_delivery_service_f7b_tab3"] = data["toggle"]["delivery_service"]
    st.session_state["key_toggle_price_f7b_tab3"] = data["toggle"]["price"]
    st.session_state["key_toggle_dtd_f7b_tab3"] = data["toggle"]["dtd"]