import requests
import json
import streamlit as st


# ========================= API 1 ====================
# API kurzy.cz 
api_kurzy = "https://data.kurzy.cz/json/meny/b[1].json"

# get reguest
@st.cache_data(ttl=3600)
def get_response_api_1(api_kurzy):
    api_1 = requests.get(api_kurzy, verify=False).text
    return api_1

api_1 = get_response_api_1(api_kurzy)

# JSON format creation
api_1_json = json.loads(api_1)

# Search for data in the API defined format - JSON
eur_rate = api_1_json['kurzy']['EUR']['dev_stred']
usd_rate = api_1_json['kurzy']['USD']['dev_stred']

eur_rate = round(eur_rate, 3)
usd_rate = round(usd_rate, 3)


# ========================= API 2 ====================
api_freecurrency_api = "https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_6SzWJxPYa8Co3Xr9ziCTd7Mt7Yavrhpy2M5A0JZ4&currencies=USD&base_currency=EUR"

#get reguest
@st.cache_data(ttl=3600)
def get_response_api_2(api_freecurrency_api):
    api_2 = requests.get(api_freecurrency_api, verify=False).text
    return api_2

api_2 = get_response_api_2(api_freecurrency_api)


# JSON format creation
api_2_json = json.loads(api_2)

# Search for data in the API defined format - JSON
eur_to_usd_rate = api_2_json['data']['USD']
eur_to_usd_rate = round(eur_to_usd_rate, 3)

# ======= Values for testing purposed to do not call/utilize API
# # API 1
# eur_rate = 24
# usd_rate = 21
# # API 2
# eur_to_usd_rate = 1.14


# ============== App screen part ===================
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

    # Functions for calculation

    def f1_czk_to_eur(czk_obj, eur_rate):
        result = czk_obj / eur_rate
        return result


    f1_result = round(f1_czk_to_eur(czk_obj,eur_rate), 2)


    def f2_czk_to_usd(czk_obj, usd_rate):
        result = czk_obj / usd_rate
        return result

    f2_result = round(f2_czk_to_usd(czk_obj, usd_rate), 2)


    def f3_eur_to_czk(eur_obj, eur_rate):
        result = eur_obj * eur_rate
        return result

    f3_result = round(f3_eur_to_czk(eur_obj, eur_rate), 2)

    def f4_usd_to_czk(usd_obj, usd_rate):
        result = usd_obj * usd_rate
        return result

    f4_result = round(f4_usd_to_czk(usd_obj, usd_rate), 2)


    def f5_eur_to_usd(eur_obj, eur_to_usd_rate):
        result = eur_obj * eur_to_usd_rate
        return result

    f5_result = round(f5_eur_to_usd(eur_obj, eur_to_usd_rate), 2)


    def f6_usd_to_eur(usd_obj, eur_to_usd_rate):
        result = usd_obj / eur_to_usd_rate
        return result

    f6_result = round(f6_usd_to_eur(usd_obj, eur_to_usd_rate), 2)
  


# ----- Buttons ------

    # ALL exchanges button 
    ''
    ''
    sub_butt_all = st.form_submit_button(
    label="To show all conversions",
    use_container_width=True,
    icon = ":material/apps:"
    )

    if sub_butt_all:
        st.write(f"{czk_obj:.2f} CZK = {f1_result} EUR")
        st.write(f"{czk_obj} CZK = {f2_result} USD")
        st.write(f"{eur_obj} EUR = {f3_result} CZK")
        st.write(f"{usd_obj} USD = {f4_result} CZK")
        st.write(f"{eur_obj} EUR = {f5_result} USD")
        st.write(f"{usd_obj} USD = {f6_result} EUR")


    # CZK -> EUR
    ''
    ''
    ''
    sub_butt_1 = st.form_submit_button(
    label="CZK -> EUR",
    use_container_width=True
    )

    if sub_butt_1:
        st.write(f"{czk_obj} CZK = {f1_result} EUR")



    # CZK -> USD
    sub_butt_2 = st.form_submit_button(
    label="CZK -> USD",
    use_container_width=True
    )

    if sub_butt_2:
        st.write(f"{czk_obj} CZK = {f2_result} USD")



    # EUR -> CZK
    ''
    ''
    sub_butt_3 = st.form_submit_button(
    label="EUR -> CZK",
    use_container_width=True
    )

    if sub_butt_3:
        st.write(f"{eur_obj} EUR = {f3_result} CZK")


    # USD -> CZK
    sub_butt_4 = st.form_submit_button(
    label="USD -> CZK",
    use_container_width=True
    )

    if sub_butt_4:
        st.write(f"{usd_obj} USD = {f4_result} CZK")

    
    
    # EUR -> USD
    ''
    ''
    sub_butt_5 = st.form_submit_button(
    label="EUR -> USD",
    use_container_width=True
    )

    if sub_butt_5:
        st.write(f"{eur_obj} EUR = {f5_result} USD")

    
    # USD -> EUR

    sub_butt_6 = st.form_submit_button(
    label="USD -> EUR",
    use_container_width=True
    )

    if sub_butt_6:
        st.write(f"{usd_obj} USD = {f6_result} EUR")




