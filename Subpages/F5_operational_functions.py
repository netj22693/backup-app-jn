import requests
import json
import streamlit as st
from typing import Optional
import logging
from app_logging import inicialization_logging

# ===== Tohle pak půjde do unifikováneho API.oy souboru =====
@st.cache_data(ttl=3600)
def api_GET_request(url_string: str, function_id: str, api_name: str) -> Optional[str | None]: 

    try:
        return requests.get(url_string, verify=False, timeout=5).text

    except Exception as e:
        logging.error(f"{function_id} - API: {api_name} - GET failed: {e}")
        return None



# API strings

def provide_url_string_kurzy_cz() -> str:
    return "https://data.kurzy.cz/json/meny/b[1].json"

def provide_url_string_freecurrencyapi_com() -> str:
    return f"""https://api.freecurrencyapi.com/v1/latest?apikey={st.secrets["F5_api_2"]["password"]}&currencies=USD&base_currency=EUR"""





# Tohle zůstane v operational functions

# ===== Inicialization for logging =====
inicialization_logging()


# ===== Parsing functions =====
def parsing_data_api_kurzy_cz(data_input: str) -> Optional[float | None]:

    try:
        data_json = json.loads(data_input)

        eur_rate= round(data_json['kurzy']['EUR']['dev_stred'], 3)
        usd_rate = round(data_json['kurzy']['USD']['dev_stred'], 3)

        logging.info(f"F5 - Parsing API - kurzy.cz - SUCCESS")

        return eur_rate, usd_rate

    except Exception as e:
        logging.error(f"F5 - Error data parsing API - kurzy.cz: {e}")
        return None, None


def parsing_data_api_freecurrency_com(data_input: str) -> Optional[float | None]:

    try:
        data_json = json.loads(data_input)

        eur_to_usd = round(data_json['data']['USD'], 3)

        logging.info(f"F5 - Parsing API - Freecurrency.com - SUCCESS")

        return eur_to_usd

    except Exception as e:
        logging.error(f"F5 - Error data parsing API - freecurrency.com: {e}")
        return None


# =================== Calculating functions ===================

def get_result_division(a: float,b: float) -> float:
    return a / b
    
def get_result_multiply(a: float,b: float) -> float:
    return a * b

# =================== Formatting for UI ===================

def get_value_formated(input: float) -> str:
    return f"{input:,.2f}". replace(",", " ")
