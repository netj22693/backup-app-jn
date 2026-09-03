import pandas as pd
import requests
import streamlit as st
from typing import Optional
import logging
from app_logging import inicialization_logging
from app_api import api_GET_request_with_cashing, provide_url_string_zipcodebase_com, provide_url_string_zipcodestack_com, provide_paramaters_zipcodebase_com, provide_paramaters_zipcodestack_com

# ===== Inicialization for logging =====
inicialization_logging()



# ===================================================
# -------- 🟣 Get ZIP code(s) based on City --------
# ===================================================
def parsing_data_zipcodebase_com(data_json: dict) -> list | str:

    '''
    2 types of Response 
        1) API response - regular response -> try will pass (unless JSON structure changed)
        2) API response - JSON with message note that limit reached -> goes to except KeyError
    '''

    # Happy path - JSON structure follows pattern 
    try:
        ds = list(map(str, data_json["results"]))

        # Happy path - no result based on the user input "results":[] empty ARRAY
        if len(ds) == 0:
            logging.info("F6 - API: zipcodebase.com - Parsing - SUCCESS - PARSING_STATE_NO_DATA")
            return "PARSING_STATE_NO_DATA"


        # Happy path - data returned based on user input
        logging.info("F6 - API: zipcodebase.com - Parsing - SUCCESS")
        return ds

    # External system sends JSON structure {"message":" something "}
    # Use case: subscription limit reached
    except KeyError:
        if "message" in data_json:
            info_message = data_json["message"]

            logging.info(f"F6 - API: zipcodebase.com - Parsing - MESSAGE RECEIVED: {info_message}")

            return "PARSING_STATE_INFO_MESSAGE"

        # In case that JSON structure will be changed by external system
        else:
            logging.info(f"F6 - API: zipcodebase.com - Parsing - FAIL KeyError ELSE")

            return "PARSING_STATE_TECHNICAL_ISSUE"


    # Undefined/Generic except issue
    except Exception as e:
        logging.warning(f"F6 - API: zipcodebase.com - Parsing - FAIL Exceptio: {e}")
        return "PARSING_STATE_TECHNICAL_ISSUE"


def adjust_data_for_visualization(data: list) ->  tuple[pd.Series, str]:

    data_series = pd.Series(data, name="ZIP codes",)
    data_series.index += 1

    string_zip_codes = ", ".join(data_series)

    return data_series, string_zip_codes


def zipcode_search_result_visualization(data_series: pd.Series, string_zip_codes: str):

    ''
    st.write(data_series)
    ''
    st.write("- This string can be used in the search below 🟢:")
    st.write(string_zip_codes)
    ''
    st.caption(r"**\*NOTE:** The below search uses **different external system** -> it is possible that there will not be 100% match.")



def orchestration_zipcode_based_on_city_search(city: str, country: str):

    '''
    Function making orchestration and validation of zipcode search based on city and country inputs
    In case of not possible to continue -> return
    '''

    # Input validation
    if not city:
        st.warning("**Missing input** - Please provide City")
        return

    # Creation of parametrs for API
    headers, params = provide_paramaters_zipcodebase_com(city, country)

    # API request
    data_json = api_GET_request_with_cashing(
        url_string= provide_url_string_zipcodebase_com(),
        function_id="F6",
        api_name="zipcodebase.com",
        headers=headers, 
        params=params,
        timeout=2
        )

    # Validation of response date
    if not data_json:
        st.warning("API **connection issue** - not possible to establish connection now.")
        return

    # Data parsing
    parsed_data = parsing_data_zipcodebase_com(data_json)

    if parsed_data == "PARSING_STATE_NO_DATA":
        st.warning("""
        There was **no result found** - Possible reasons:
        - The city is **not related** to the selected country
        - The city **doesn't exist**
        - **Typo** in the city name
        - The **external system has no data** for the city
        """)
        return

    elif parsed_data == "PARSING_STATE_INFO_MESSAGE":
        st.warning("""
        **API monthy limit** has been reached - this search is **currently not available**.
        """)
        return

    elif parsed_data == "PARSING_STATE_TECHNICAL_ISSUE":
        st.warning("""
        **Technical issue** -> please report it on the main page **Report bug** section.
        """)  

    # Happy path:
    else:
        data_series, string_zip_codes = adjust_data_for_visualization(parsed_data)

        zipcode_search_result_visualization(data_series, string_zip_codes)



# ===================================================
# --------- 🟢 Get city based on ZIP code ----------
# ===================================================

def parsing_data_zipcodestack_com(data_json: dict) -> list | str:

    '''
    2 types of Response 
        1) API response - regular response -> try will pass (unless JSON structure changed)
        2) API response - JSON with message note that limit reached -> goes to except KeyError
    '''

    # Happy path
    try:
        result_list = []
        
        for result in data_json["results"]:
            result = str(result)
            result_list.append(result)


        result_list = list(map(str, result_list))

        # Happy path - but external system has no data releated to user input
        if len(result_list) == 0:
            logging.info(f"F6 - API: zipcodestack.com - Parsing - PARSING_STATE_NO_DATA")
            return "PARSING_STATE_NO_DATA"

        # Happy end
        else:
            logging.info(f"F6 - API: zipcodestack.com - Parsing - SUCCESS")
            return result_list

    # If JSON Response structure is changed
    except KeyError:
        logging.warning(f"F6 - API: zipcodestack.com - Parsing - FAIL: KeyError")
        return "PARSING_STATE_TECHNICAL_ISSUE"

    # Undefined issue
    except Exception as e:
        logging.warning(f"F6 - API: zipcodestack.com - Parsing - FAIL: {e}")
        return "PARSING_STATE_TECHNICAL_ISSUE"
    

def city_search_result_visualization(parsed_data: list, data_json: dict):

    st.write("##### Results:")
            
    tab1,tab2 = st.tabs(["Table","Raw data"])

    for value in parsed_data:

        postal_code_list = []
        city_list = []
        region_list = []

        for result in data_json["results"][value]:
            tab2.write(f"- ZIP code: **{result['postal_code']}**")
            tab2.write(f"- City: **{result['city_en']}**")
            tab2.write(f"- Region: **{result['state_en']}**")
            tab2.write(f"=====================================")

            postal_code_list.append(result['postal_code'])
            city_list.append(result['city_en'])
            region_list.append(result['state_en'])

        # DF creation
        result_dict = pd.DataFrame({
            "ZIP code": postal_code_list,
            "City name": city_list,
            "Region": region_list
        })

        result_dict.index += 1
        tab1.write(result_dict)   


def validation_number_of_zipcodes(zipcode: str) -> list:

    '''
    Input from user: str  "1,2,3"
    .split(",") -> list ["1","2","3"]
    len(), lenght of the list
    '''
    return len(zipcode.split(","))



def orchestration_city_based_on_zipcode_search(zipcode: str | None, country_code: str):

    
    '''
    Function making orchestration and validation of city search based on zipcode(s)
    In case of not possible to continue -> return
    '''

    # Input validation
    if not zipcode:
        st.warning("Missing input - ZIP code")
        return

    # Input validation - limit 10 ZIP codes
    if validation_number_of_zipcodes(zipcode) > 10:
        st.warning("Request is limited to 10 ZIP codes -> there was more provided")
        return     


    # Creation of parametrs for API
    headers, params = provide_paramaters_zipcodestack_com(zipcode, country_code)

    # API request
    data_json = api_GET_request_with_cashing(
        url_string= provide_url_string_zipcodestack_com(),
        function_id="F6",
        api_name="zipcodestack.com",
        headers=headers, 
        params=params,
        timeout=2
        )

    # Validation of response date
    if not data_json:
        st.warning("API **connection issue** - not possible to establish connection now.")
        return

    # Data parsing
    parsed_data = parsing_data_zipcodestack_com(data_json)  

    if parsed_data == "PARSING_STATE_NO_DATA":
        st.warning("""
        There was **no result found** - Possible reasons:
        - The ZIP code is **not related** to the selected country
        - The ZIP code **doesn't exist**
        - The **external system has no data** for the ZIP code
        """)
        return

    elif parsed_data == "PARSING_STATE_TECHNICAL_ISSUE":
        st.warning("""
        **Technical issue** -> please report it on the main page **Report bug** section.
        """)
        return

    else:
        city_search_result_visualization(parsed_data, data_json)