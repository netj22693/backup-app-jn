import requests
import streamlit as st
import logging
from app_logging import inicialization_logging

# ===== Inicialization for logging =====
inicialization_logging()

# ===== GET request =====

def create_api_GET(ttl_time: int):

    '''
    Factory function principle
    '''

    @st.cache_data(ttl=ttl_time, show_spinner=False)
    def api_GET_request(
        url_string: str,
        function_id: str,
        api_name: str,
        headers: dict = None, 
        params: tuple = None,
        timeout:int = 5
        ) -> dict | None: 

        try:
            request = requests.get(
                url_string,
                timeout=timeout,
                headers=headers,
                params=params
            )

            # Note: In case of fail, there will be also HTTP code in the Exception seen
            request.raise_for_status()

            logging.info(f"{function_id} - API: {api_name} - GET SUCCESS")
            return request.json()

        except Exception as e:
            logging.error(f"{function_id} - API: {api_name} - GET failed: {e}")
            return None

    return api_GET_request

# Factory function principle
api_GET_cache_1h = create_api_GET(3600)
api_GET_cache_10min = create_api_GET(600)

# ===== API strings =====

def get_url_string_for_GET_api(key: str) -> str:
    url = {
        # 1) F6 - 🟣 zipcodebase.com - Get ZIP code(s) based on City
        "zipcodebase_com_code_city": f"https://app.zipcodebase.com/api/v1/code/city?apikey={st.secrets['F6_api_1']['password_1']}",

        # 2) F6 - 🟢 zipcodestack.com - Get city based on ZIP code
        "zipcodestack_com": "https://api.zipcodestack.com/v1/search",

        # 3) F6 - 🟢 zipcodestack.com - API statistics of usage of 2)
        "zipcodestack_com_statistics": f"https://api.zipcodestack.com/v1/status?apikey={st.secrets['F6_api_2']['password_2']}",

        # 4) F5 - ⚫ kurzy.cz
        "kurzy_cz" : "https://data.kurzy.cz/json/meny/b[1].json",

        # 5) F5 - 🔵 freecurrencyapi.com - EUR to USD
        "freecurrencyapi_com_EUR_to_USD" : f"https://api.freecurrencyapi.com/v1/latest?apikey={st.secrets['F5_api_2']['password']}&currencies=USD&base_currency=EUR",

        # 6) F5 - 🔵 freecurrencyapi.com - API statistics of usage of 5)
        "freecurrencyapi_com_EUR_to_USD_statistics": f"https://api.freecurrencyapi.com/v1/status?apikey={st.secrets['F5_api_2']['password']}",

        # 7) F7 - freecurrencyapi.com EUR to CZK
        "freecurrencyapi_com_EUR_to_CZK": f"https://api.freecurrencyapi.com/v1/latest?apikey={st.secrets['F7_api']['password_7']}&currencies=EUR%2CCZK"
    }

    return url.get(key)



# ===== API parameters =====

# Zipcodebase.com
def provide_paramaters_zipcodebase_com(city:str, country_code: str) -> tuple[dict, tuple]:

    # Note: this is official snippet of the code from their documentation but if apikey in headers only, they return {"error":"no apikey provided."}. Thus I use APIKEY in URL as well
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