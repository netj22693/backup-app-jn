import requests
import streamlit as st
from typing import Optional
import logging
from app_logging import inicialization_logging

# ===== Inicialization for logging =====
inicialization_logging()

# ===== GET request =====
@st.cache_data(ttl=3600, show_spinner=False)
def api_GET_request_with_cashing(
    url_string: str,
    function_id: str,
    api_name: str,
    headers: dict = None, 
    params: tuple = None,
    timeout:int = 5
    ) -> Optional[str | None]: 

    try:
        request = requests.get(
            url_string,
            timeout=timeout,
            headers=headers,
            params=params
        )

        logging.info(f"{function_id} - API: {api_name} - GET SUCCESS")
        return request.json()

    except Exception as e:
        logging.error(f"{function_id} - API: {api_name} - GET failed: {e}")
        return None


# ===== API strings =====

# Zipcodebase.com
def provide_url_string_zipcodebase_com() -> str:
    return f"""https://app.zipcodebase.com/api/v1/code/city?apikey={st.secrets["F6_api_1"]["password_1"]}"""    


# Zipcodestack.com
def provide_url_string_zipcodestack_com() -> str:
    return "https://api.zipcodestack.com/v1/search"




# ===== API parameters =====

# Zipcodebase.com
def provide_paramaters_zipcodebase_com(city:str, country_code: str) -> tuple[dict, tuple]:

    headers = { 
        "apikey": st.secrets["F6_api_1"]["password_1"]
        }

    params = (
        ("city", city),
        ("country", country_code),
        );

    return headers, params


# Zipcodestack.com
def provide_paramaters_zipcodestack_com(zipcode:str, country_code: str) -> tuple[dict, tuple]:

    headers = { 
        "apikey": st.secrets["F6_api_2"]["password_2"]
        }

    params = (
        ("codes", zipcode),
        ("country",country_code),
        );

    return headers, params