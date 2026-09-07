import re
import pandas as pd
import streamlit as st
import logging
import unicodedata
from app_logging import inicialization_logging
from app_api import api_GET_cache_1h, get_url_string_for_GET_api, provide_paramaters_zipcodebase_com, provide_paramaters_zipcodestack_com
from Subpages.F6_input_data import cities_api_aliases, cities_normalized_not_unique, cities_not_unique_name


# ===== Inicialization for logging =====
inicialization_logging()


# ===================================================
# -------- 🟠 Get ZIP code(s) based on City --------
# ===================================================

def regex_validation_city_input(city_input: str, country_code: str) -> tuple[str, int]:

    '''
    Rule: 
    - Allows CZ/SK letters
    - For the external API, there needs to be , as separater when passed as parameters
    - not other characters allowed -> REGEX validation stop it
    '''

    pattern = {
        "CZ": {
            "rule": r"^[A-Za-zÁČĎÉĚÍŇÓŘŠŤÚŮÝŽáčďéěíňóřšťúůýž -]{1,33}$",
            "length": 33
        },
        "SK": {
            "rule": r"^[A-Za-zÁÄČĎÉÍĹĽŇÓÔŔŠŤÚÝŽáäčďéíĺľňóôŕšťúýž -]{1,23}$",
            "length": 23
        }
    }

    country_pattern = pattern.get(country_code)
    allowed_length = country_pattern["length"]


    if len(city_input) > allowed_length:
        return "NOT_PASSED_TOO_LONG", allowed_length

    elif re.fullmatch(country_pattern["rule"], city_input):
        return "PASSED", allowed_length
    
    else:
        return "NOT_PASSED", allowed_length


def remove_diacritic(city: str) -> str:

    ''''
    - unicodedata.normalize("NFKD") splits string by characters
    - character with diacritic is split into two č → c + ˇ
    - for loop again connects the split characters, if not unicode (which ˇ isn't), it will not connect 
    - týnec -> tyˊnec -> tynec
    '''

    try: 
        normalized = unicodedata.normalize("NFKD", city)

        result = ""

        for character in normalized:
            if not unicodedata.combining(character):
                result += character

        logging.info(f"F6 - Remove diacritics - COMPLETE: from: {city} -> to: {result}")
        return result

    except Exception as e:
        logging.warning(f"F6 - Remove diacritics - FAILED: {e}")
        return city


def is_city_in_xref(city: str, country_code: str, data: dict, check_type: str) -> bool:

	'''
	Uses XREF dict
	A) IS_CITY_NAME_UNIQUE
		To recognize city which name is not unique -> the same city name appears in multiple regions	
	
	B) IS_NORMALIZED_CITY_NAME_UNIQUE
		To recognize cities which have unique names before normalization but after normalization the uniqueness is gone	
	'''
	try:	
		for object in data[country_code]:
			normalized = object["normalized"]
			xref_name = object ["name"]

			if normalized == city: 

				logging.info(f"F6 - XREF check: {check_type} - MATCH - {city} | {normalized} | {xref_name} - SUCCESS")

				return True

		else:
			logging.info(f"F6 - XREF check: {check_type} - NO MATCH - SUCCESS")
			return False


	except KeyError:
		logging.warning(f"F6 - XREF check: {check_type} - KEY ERROR - FAIL")
		return False

	except Exception as e:
		logging.warning(f"F6 - XREF check: {check_type} - FAIL: {e}")
		return False


def check_city_multiple_names(city: str, country_code: str, data: dict) -> str:

	'''
	To unifie cities which have both czech and official english name worldwide known
	user: praha -> api: prague
	'''
	try:	
		for object in data[country_code]:
			normalized = object["normalized"]
			api_name = object ["api"]

			if normalized == city: 

				logging.info(f"F6 - XREF check: MULTIPLE NAMES - MATCH - {city} | {normalized} -> {api_name} - SUCCESS")

				return api_name

		else:
			logging.info(f"F6 - XREF check: MULTIPLE NAMES - NO MATCH - SUCCESS")
			return city


	except KeyError:
		logging.warning(f"F6 - XREF check: MULTIPLE NAMES - KEY ERROR - FAIL")
		return city

	except Exception as e:
		logging.warning(f"F6 - XREF check: MULTIPLE NAMES - FAIL: {e}")
		return city


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

    string_zip_codes = [
    ", ".join(data_series[i:i + 10])
    for i in range(0, len(data_series), 10)
    ]   

    return data_series, string_zip_codes


def zipcode_search_result_visualization(data_series: pd.Series, list_of_strings_zipcodes: list[str], city_name_not_unique: bool, city_name_normalized_not_unique: bool, len_zipcodes: int):


    # XREF result info
    text_city_name_not_unique = f"This city **name is shared by multiple cities in multiple regions**. You can use the search box below to verify the correct city and ZIP code."

    text_city_name_normalized_not_unique = "The city **name may correspond to multiple cities** in **multiple regions** because **diacritics**. You can use the search box below to verify the correct ZIP code."


    # String text logic
    num_strings = (len(list_of_strings_zipcodes))

    if num_strings > 1:
        text = "These **strings** can be used in the search box below :green[⬤]. Split by **10 ZIP codes per line** - limit per request." 

        if num_strings >= 2:
            mindfull_text= """
            - **Please use the API responsibly and avoid unnecessary API calls** 😊💚
            """

    else:
        text = "This **string** can be used in the search box below :green[⬤]"


    # UI 
    st.write("")
    st.write(data_series)
    if city_name_not_unique == True and len_zipcodes > 1:
        st.write("")
        st.info(text_city_name_not_unique)

    if city_name_normalized_not_unique == True:
        st.write("")
        st.info(text_city_name_normalized_not_unique)
    
    st.write("")
    st.write(text)
    if num_strings >= 2:
        st.write(mindfull_text)
    st.write("")

    for string in list_of_strings_zipcodes:
        st.write(string)

    st.write("")
    st.caption(r"**\*NOTE:** The below search uses **different external system** -> it is possible that there will not be 100% match.")



def orchestration_zipcode_based_on_city_search(city: str, country_code: str):

    '''
    Function making orchestration and validation of zipcode search based on city and country inputs
    In case of not possible to continue -> return
    '''

    # Input normaliyation
    city = city.strip().casefold()


    # Input validation
    if not city:
        st.warning("**Missing input** - Please provide City")
        return

    # Regex validation
    regex_result, allowed_length = regex_validation_city_input(city, country_code)

    if regex_result == "NOT_PASSED_TOO_LONG":
        st.warning(f"""
        The city input is too long. Max number of characters for {country_code} is **{allowed_length}**.
        """)
        return

    elif regex_result == "NOT_PASSED":
        st.warning(f"""
        Not allowed characters in the city input.
        """)
        return

    # Normalization of latin diacritics 
    city = remove_diacritic(city)

    # Normalization using XREFs
    city_name_not_unique = is_city_in_xref(
		city,
		country_code,
		cities_not_unique_name,
		"IS_CITY_NAME_UNIQUE"
		)
	
    city_name_normalized_not_unique = is_city_in_xref(
        city,
        country_code,
        cities_normalized_not_unique,
        "IS_NORMALIZED_CITY_NAME_UNIQUE"
        )

    city = check_city_multiple_names(
        city,
        country_code,
        cities_api_aliases
    )

    # Creation of parametrs for API
    headers, params = provide_paramaters_zipcodebase_com(city, country_code)

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
        return

    # Happy path:
    else:

        data_series, list_of_strings_zip_codes = adjust_data_for_visualization(parsed_data)

        zipcode_search_result_visualization(
            data_series,
            list_of_strings_zip_codes,
            city_name_not_unique,
            city_name_normalized_not_unique,
            len(parsed_data)
            )



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


        logging.info(f"F6 - Validation of missing ZIP codes - SUCCESS")

        return not_in_response_list 

    except Exception as e:
        logging.warning(f"F6 - Validation of missing ZIP codes - FAIL: {e}")
        return None

    

def city_search_result_visualization(parsed_data: list, data_json: dict, zipcode_not_in_response: list):

    st.write("")
    st.write("##### Results:")
            
    tab1,tab2 = st.tabs(["Table","Raw data"])

    if len(zipcode_not_in_response) > 0:
        tab1.info(f"**No** result returned for: **{zipcode_not_in_response}**")

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
        result_df = pd.DataFrame({
            "ZIP code": postal_code_list,
            "City name": city_list,
            "Region": region_list
        })

        result_df = result_df.sort_values("City name", ascending=True)
        result_df = result_df.reset_index(drop=True)

        result_df.index += 1
        tab1.write(result_df)   


def zipcodes_into_list(zipcode: str) -> list[str]:

    '''
    Input from user: str  "1,2,3"
    .split(",") -> list ["1","2","3"]
    '''
    return zipcode.split(",")


def remove_all_spaces(data_input: str):
    return data_input.replace(" ", "")


def zipcodes_from_list_to_string(data_input: list) -> str:
    return ",".join(data_input)


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
    zipcode_requested_list: list[str] = zipcodes_into_list(zipcode_requested)


    # Input validation - limit 10 ZIP codes
    if len(zipcode_requested_list) > 10:
        st.warning("Request is limited to 10 ZIP codes -> there was more provided")
        return     

    # Removing of duplicities in the list, if any (input: '11000','11000' -> output: '11000' )
    # Why: If duplicities not removed, the API Request parameters in URL: 11000,25163,11000,11000,11000,11000,11000,11000  -> not the best to send it although the external syste has a logic of removing duplicities
    zipcode_requested_list = list(dict.fromkeys(zipcode_requested_list))

    # Back to the string for API parametrs input - without duplicated ZIP codes
    zipcode_requested: str = zipcodes_from_list_to_string(zipcode_requested_list)

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