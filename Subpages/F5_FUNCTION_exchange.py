import streamlit as st
from app_api import api_GET_cache_1h, get_url_string_for_GET_api
from Subpages.F5_operational_functions import get_result_division, get_result_multiply, get_value_formated, parsing_data_api_freecurrencyapi_com, parsing_data_api_kurzy_cz


# =================== App screen ===================
st.write("# Exchange Rate:")
''
''
st.write("""
- The exchange rate is API based 
- The data comes from ⚫[Kurzy.cz](https://www.kurzy.cz/) and 🔵[Freecurrencyapi.com](https://app.freecurrencyapi.com/)
""")



# =================== API call ===================
api_raw_data_kurzy_cz = api_GET_cache_1h(
    url_string = get_url_string_for_GET_api("kurzy_cz"),
    function_id = "F5",
    api_name = "kurzy.cz"
    )

api_raw_data_freecurrencyapi_com = api_GET_cache_1h(
    url_string = get_url_string_for_GET_api("freecurrencyapi_com_EUR_to_USD"),
    function_id = "F5",
    api_name = "freecurrencyapi.com"
    )

# =================== Parsing + Fallbacks ===================
if api_raw_data_kurzy_cz != None:
    eur_rate, usd_rate = parsing_data_api_kurzy_cz(api_raw_data_kurzy_cz)

else:
    st.warning("""
    API Kurzy.cz was not connected - there are temporary values used:
    - CZK to EUR = 24
    - CZK to USD = 21
    """)

    eur_rate = 24
    usd_rate = 21



if api_raw_data_freecurrencyapi_com != None:
    eur_to_usd_rate = parsing_data_api_freecurrencyapi_com(api_raw_data_freecurrencyapi_com)

else:
    st.warning("""
    API Freecurrencyapi.com was not connected - there is temporary value used:
    - EUR to USD = 1.14
    """)

    eur_to_usd_rate = 1.14


# =================== App screen Metrics ===================


''
''
''
st.metric(label="EUR to CZK", value= f"{eur_rate:.3f}")

st.metric(label="USD to CZK", value= f"{usd_rate:.3f}")

st.metric(label="EUR to USD", value= f"{eur_to_usd_rate:.3f}")


''
''
''
''

# =============== Form ==============================

st.write("#### Calculation: ")

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


    # Data formating
    czk_obj_formatted = get_value_formated(czk_obj)
    eur_obj_formatted = get_value_formated(eur_obj)
    usd_obj_formatted = get_value_formated(usd_obj)

    r1_czk_to_eur_formatted = get_value_formated(get_result_division(czk_obj, eur_rate))
    r2_czk_to_usd_formatted = get_value_formated(get_result_division(czk_obj, usd_rate))
    r3_eur_to_czk_formatted = get_value_formated(get_result_multiply(eur_obj, eur_rate))
    r4_usd_to_czk_formatted = get_value_formated(get_result_multiply(usd_obj, usd_rate))
    r5_eur_to_usd_formatted = get_value_formated(get_result_multiply(eur_obj, eur_to_usd_rate))
    r6_usd_to_eur_formatted = get_value_formated(get_result_division(usd_obj, eur_to_usd_rate))

# ===== Buttons =====

    # ALL exchanges button 
    ''
    ''
    sub_butt_all = st.form_submit_button(
    label="To show all conversions",
    use_container_width=True,
    icon = ":material/apps:")

    if sub_butt_all:
        st.write(f"{czk_obj_formatted} CZK = {r1_czk_to_eur_formatted} EUR")
        st.write(f"{czk_obj_formatted} CZK = {r2_czk_to_usd_formatted} USD")
        st.write(f"{eur_obj_formatted} EUR = {r3_eur_to_czk_formatted} CZK")
        st.write(f"{usd_obj_formatted} USD = {r4_usd_to_czk_formatted} CZK")
        st.write(f"{eur_obj_formatted} EUR = {r5_eur_to_usd_formatted} USD")
        st.write(f"{usd_obj_formatted} USD = {r6_usd_to_eur_formatted} EUR")


    # CZK -> EUR
    ''
    ''
    ''
    sub_butt_1 = st.form_submit_button(
    label="CZK -> EUR",
    use_container_width=True
    )

    if sub_butt_1:
        st.write(f"{czk_obj_formatted} CZK = {r1_czk_to_eur_formatted} EUR")

    # CZK -> USD
    sub_butt_2 = st.form_submit_button(
    label="CZK -> USD",
    use_container_width=True
    )

    if sub_butt_2:
        st.write(f"{czk_obj_formatted} CZK = {r2_czk_to_usd_formatted} USD")

    # EUR -> CZK
    ''
    ''
    sub_butt_3 = st.form_submit_button(
    label="EUR -> CZK",
    use_container_width=True
    )

    if sub_butt_3:
        st.write(f"{eur_obj_formatted} EUR = {r3_eur_to_czk_formatted} CZK")


    # USD -> CZK
    sub_butt_4 = st.form_submit_button(
    label="USD -> CZK",
    use_container_width=True
    )

    if sub_butt_4:
        st.write(f"{usd_obj_formatted} USD = {r4_usd_to_czk_formatted} CZK")

    
    
    # EUR -> USD
    ''
    ''
    sub_butt_5 = st.form_submit_button(
    label="EUR -> USD",
    use_container_width=True
    )

    if sub_butt_5:
        st.write(f"{eur_obj_formatted} EUR = {r5_eur_to_usd_formatted} USD")

    
    # USD -> EUR
    sub_butt_6 = st.form_submit_button(
    label="USD -> EUR",
    use_container_width=True
    )

    if sub_butt_6:
        st.write(f"{usd_obj_formatted} USD = {r6_usd_to_eur_formatted} EUR")