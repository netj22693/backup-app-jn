import re
import pandas as pd
import streamlit as st
import logging
from app_logging import inicialization_logging
from app_api import api_GET_cache_1h, get_url_string_for_GET_api, provide_paramaters_zipcodebase_com, provide_paramaters_zipcodestack_com

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
    data_json = api_GET_cache_1h(
        url_string= get_url_string_for_GET_api("zipcodebase_com_code_city"),
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



def validation_request_vs_response_zipcodes(zipcode_user_input: str, zipcode_response: list) -> list | None:

    '''
    - Validation/to show list of ZIP codes for which no data were found in the external system
    - Principle: compere list of ZIP codes which were sent in Request with list of ZIP  codes in Response
    '''

    try:
        not_in_response_list = []
        for item in zipcode_user_input:
            if item not in zipcode_response:
                not_in_response_list.append(item)


        logging.warning(f"F6 - Validation of missing ZIP codes - SUCCESS")

        return not_in_response_list 

    except Exception as e:
        logging.warning(f"F6 - Validation of missing ZIP codes - FAIL: {e}")
        return None

    

def city_search_result_visualization(parsed_data: list, data_json: dict, zipcode_not_in_response: list):

    st.write("##### Results:")
            
    tab1,tab2 = st.tabs(["Table","Raw data"])

    if len(zipcode_not_in_response) > 0:
        tab1.info(f"No result for: {zipcode_not_in_response}")

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


def zipcodes_into_list(zipcode: str) -> list[str]:

    '''
    Input from user: str  "1,2,3"
    .split(",") -> list ["1","2","3"]
    '''
    return zipcode.split(",")


def remove_all_spaces(data_input: str):
    return data_input.replace(" ", "")

def regex_validation_zipcodes_input(zipcode_input: str) -> str:

    '''
    Rule: 
    - CZ/SK ZIP codes need to have 5 characters/numbers 0-9
    - For the external API, there needs to be , as separater when passed as parameters
    - not other characters allowed -> REGEX validation stop it
    '''

    if re.fullmatch(r"[0-9]{5}(,[0-9]{5})*", zipcode_input):
       return "PASSED"

    else: 
       return "NOT_PASSED"



def ui_formatting(zipcode_not_in_response: list[str]) -> list[str]:

    '''
    Formatting from '25163' -> '251 63' for better UI experience
    '''

    a = []
    for item in zipcode_not_in_response:
        new = item[:3] + " " + item[3:]
        a.append(new)


    formatted = ", ".join(a)
    return formatted



def orchestration_city_based_on_zipcode_search(zipcode_requested: str | None, country_code: str):
    
    '''
    Function making orchestration and validation of city search based on zipcode(s)
    In case of not possible to continue -> return
    '''

    # Input formatting - ZIP Codes still as string
    zipcode_requested: str = remove_all_spaces(zipcode_requested)

    # Input validation
    if not zipcode_requested:
        st.warning("Missing input - ZIP code")
        return

    # Regex validation of input - to not call API having incorrect data input(wasting of API call)
    if regex_validation_zipcodes_input(zipcode_requested) == "NOT_PASSED":
        st.warning("This is not valid format of ZIP code(s).")
        return

    # String into list[str]
    zipcode_requested_list = zipcodes_into_list(zipcode_requested)

    # Removing of duplicities in the list, if any (input: '11000','11000' -> output: '11000' )
    # Why: If duplicities not removed, the API Request parameters in URL: 11000,25163,11000,11000,11000,11000,11000,11000  -> not the best to send it although the external syste has a logic of removing duplicities
    zipcode_requested_list = list(dict.fromkeys(zipcode_requested_list))


    # Input validation - limit 10 ZIP codes
    if len(zipcode_requested_list) > 10:
        st.warning("Request is limited to 10 ZIP codes -> there was more provided")
        return     


    # Creation of parametrs for API
    headers, params = provide_paramaters_zipcodestack_com(zipcode_requested, country_code)

    # API request
    data_json = api_GET_cache_1h(
        url_string= get_url_string_for_GET_api("zipcodestack_com"),
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
        zipcode_not_in_response = validation_request_vs_response_zipcodes(zipcode_requested_list, parsed_data)

        city_search_result_visualization(
            parsed_data,
            data_json,
            ui_formatting(zipcode_not_in_response)
        )