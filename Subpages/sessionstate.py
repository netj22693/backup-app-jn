import requests
import json
import streamlit as st
from typing import Optional

# =================== API functions ===================
@st.cache_data(ttl=3600)
def api_GET_request(url_string: str) -> Optional[str]: 

    try:
        api_response = requests.get(url_string, verify=False, timeout=5).text
        return api_response

    except Exception as e:
        print(f"Error GET request: {e}")
        return None


def api_1_kurzy_parsing(data_input: str) -> Optional[float]:

    try:
        data_json = json.loads(data_input)

        # Search for data in the API defined format - JSON
        eur_rate_parsed = data_json['kurzy']['EUR']['dev_stred']
        usd_rate_parsed = data_json['kurzy']['USD']['dev_stred']

        eur_rate_parsed = round(eur_rate_parsed, 3)
        usd_rate_parsed = round(usd_rate_parsed, 3)

        return eur_rate_parsed, usd_rate_parsed

    except Exception as e:
        print(f"Error parsing API 1: {e}")

        eur_rate_parsed = None
        usd_rate_parsed = None
        return eur_rate_parsed, usd_rate_parsed


def api_2_freecurrency_parsing(data_input: str) -> Optional[float]:

    try:
        data_json = json.loads(data_input)

        # Search for data in the API defined format - JSON
        eur_to_usd_rate_parsed = data_json['data']['USD']
        eur_to_usd_rate_parsed = round(eur_to_usd_rate_parsed, 3)

        return eur_to_usd_rate_parsed

    except Exception as e:
        print(f"Error parsing API 2: {e}")

        eur_to_usd_rate_parsed = None
        return eur_to_usd_rate_parsed

# =================== Connection string build ===================
api_1_kurzy_url_string = "https://data.kurzy.cz/json/meny/b[1].json"

secrets_api_2 = st.secrets["F5_api_2"]["password"]
api_2_freecurrency_url_string = f"https://api.freecurrencyapi.com/v1/latest?apikey={secrets_api_2}&currencies=USD&base_currency=EUR"


# =================== API call ===================
api_1_kurzy = api_GET_request(api_1_kurzy_url_string)
api_2_freecurrency = api_GET_request(api_2_freecurrency_url_string)


# =================== Parsing ===================
if api_1_kurzy != None:
    eur_rate, usd_rate = api_1_kurzy_parsing(api_1_kurzy)

if api_1_kurzy == None  or eur_rate == None or usd_rate == None:

    st.warning("""
    API Kurzy.cz was not connected - there are temporary values used:
    - CZK to EUR = 24
    - CZK to USD = 21
    """)

    eur_rate = 24
    usd_rate = 21


if api_2_freecurrency != None:
    eur_to_usd_rate = api_2_freecurrency_parsing(api_2_freecurrency)

if api_2_freecurrency == None or eur_to_usd_rate == None:

    st.warning("""
    API Freecurrency.com was not connected - there is temporary value used:
    - EUR to USD = 1.14
    """)

    eur_to_usd_rate = 1.14


# =================== Calculating functions ===================

def get_result_division(a: float,b: float) -> float:
    result = a / b
    return result
    
def get_result_multiply(a: float,b: float) -> float:
    result = a * b
    return result


# =================== App screen part ===================
st.write("# Exchange rate:")
''
''
st.write("""
- The exchange rate is API based 
- The information comes from https://www.kurzy.cz/ and https://app.freecurrencyapi.com/
""")


''
''
''
st.metric(label="CZK to EUR", value= eur_rate)

st.metric(label="CZK to USD", value= usd_rate)

st.metric(label="EUR to USD", value= eur_to_usd_rate)


''
''
''
''

# =============== Form ==============================

st.write("#### Calculation: ")
# User inputs
with st.form(key="calculation form"):
    czk_obj = st.number_input(
        "CZK",
        step=10.00,
        min_value=0.00,
        help = "You can either click on the +- icons or write the input using numbers. *The step is step +- 10.00 -> i case of diferent values in decimals write it manualy."
        )
    

    eur_obj = st.number_input(
        "EUR",
        step=10.00,
        min_value=0.00,
        help = "You can either click on the +- icons or write the input using numbers. *The step is step +- 10.00 -> i case of diferent values in decimals write it manualy."
        )
    

    usd_obj = st.number_input(
        "USD",
        step=10.00,
        min_value=0.00,
        help = "You can either click on the +- icons or write the input using numbers. *The step is step +- 10.00 -> i case of diferent values in decimals write it manualy."
        )

    r1_czk_to_eur = get_result_division(czk_obj, eur_rate)
    r2_czk_to_usd = get_result_division(czk_obj, usd_rate)
    r3_eur_to_czk = get_result_multiply(eur_obj, eur_rate)
    r4_usd_to_czk = get_result_multiply(usd_obj, usd_rate)
    r5_eur_to_usd = get_result_multiply(eur_obj, eur_to_usd_rate)
    r6_usd_to_eur = get_result_division(usd_obj, eur_to_usd_rate)

# ----- Buttons ------

    # ALL exchanges button 
    ''
    ''
    sub_butt_all = st.form_submit_button(
    label="To show all conversions",
    use_container_width=True,
    icon = ":material/apps:")

    if sub_butt_all:
        st.write(f"{czk_obj:.2f} CZK = {r1_czk_to_eur:.2f} EUR")
        st.write(f"{czk_obj:.2f} CZK = {r2_czk_to_usd:.2f} USD")
        st.write(f"{eur_obj:.2f} EUR = {r3_eur_to_czk:.2f} CZK")
        st.write(f"{usd_obj:.2f} USD = {r4_usd_to_czk:.2f} CZK")
        st.write(f"{eur_obj:.2f} EUR = {r5_eur_to_usd:.2f} USD")
        st.write(f"{usd_obj:.2f} USD = {r6_usd_to_eur:.2f} EUR")

    # CZK -> EUR
    ''
    ''
    ''
    sub_butt_1 = st.form_submit_button(
    label="CZK -> EUR",
    use_container_width=True
    )

    if sub_butt_1:
        st.write(f"{czk_obj:.2f} CZK = {r1_czk_to_eur:.2f} EUR")

    # CZK -> USD
    sub_butt_2 = st.form_submit_button(
    label="CZK -> USD",
    use_container_width=True
    )

    if sub_butt_2:
        st.write(f"{czk_obj:.2f} CZK = {r2_czk_to_usd:.2f} USD")

    # EUR -> CZK
    ''
    ''
    sub_butt_3 = st.form_submit_button(
    label="EUR -> CZK",
    use_container_width=True
    )

    if sub_butt_3:
        st.write(f"{eur_obj:.2f} EUR = {r3_eur_to_czk:.2f} CZK")


    # USD -> CZK
    sub_butt_4 = st.form_submit_button(
    label="USD -> CZK",
    use_container_width=True
    )

    if sub_butt_4:
        st.write(f"{usd_obj:.2f} USD = {r4_usd_to_czk:.2f} CZK")

    
    
    # EUR -> USD
    ''
    ''
    sub_butt_5 = st.form_submit_button(
    label="EUR -> USD",
    use_container_width=True
    )

    if sub_butt_5:
        st.write(f"{eur_obj:.2f} EUR = {r5_eur_to_usd:.2f} USD")

    
    # USD -> EUR
    sub_butt_6 = st.form_submit_button(
    label="USD -> EUR",
    use_container_width=True
    )

    if sub_butt_6:
        st.write(f"{usd_obj:.2f} USD = {r6_usd_to_eur:.2f} EUR")