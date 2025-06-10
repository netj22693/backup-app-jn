import requests
import json
import streamlit as st



# API kurzy.cz 
api_kurzy = "https://data.kurzy.cz/json/meny/b[1].json"


# get reguest
api_1 = requests.get(api_kurzy, verify=False).text


#  JSON format creation
api_1_json = json.loads(api_1)

# Search for data in the API defined format - JSON
eur_rate = api_1_json['kurzy']['EUR']['dev_stred']
usd_rate = api_1_json['kurzy']['USD']['dev_stred']

# ======= Values for testing purposed to do not call/utilize API
# eur_rate = 24
# usd_rate = 21

st.write("# Exchange rate:")
''
''
st.write("""
- The exchange rate is API based 
- The information comes from https://www.kurzy.cz/
""")

''
''
''
st.metric(label="CZK to EUR", value= eur_rate)

st.metric(label="CZK to USD", value= usd_rate)


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


# ----- Buttons 1 calculations ------

    ''
    ''
    ''
    # CZK -> EUR
    sub_butt_1 = st.form_submit_button(label="CZK -> EUR",      use_container_width=True
    )

    def f1_czk_to_eur(czk_obj, eur_rate):
        result = czk_obj / eur_rate
        return result


    f1_result = round(f1_czk_to_eur(czk_obj,eur_rate), 4)

    if sub_butt_1:
        st.write(f"{czk_obj} CZK = {f1_result} EUR")



    # CZK -> USD
    sub_butt_2 = st.form_submit_button(label="CZK -> USD",      use_container_width=True
    )

    def f2_czk_to_usd(czk_obj, usd_rate):
        result = czk_obj / usd_rate
        return result

    f2_result = round(f2_czk_to_usd(czk_obj, usd_rate), 4)

    if sub_butt_2:
        st.write(f"{czk_obj} CZK = {f2_result} USD")



    # EUR -> CZK
    sub_butt_3 = st.form_submit_button(label="EUR -> CZK",      use_container_width=True
    )

    def f3_eur_to_czk(eur_obj, eur_rate):
        result = eur_obj * eur_rate
        return result

    f3_result = round(f3_eur_to_czk(eur_obj, eur_rate), 4)

    if sub_butt_3:
        st.write(f"{eur_obj} EUR = {f3_result} CZK")


    # USD -> CZK
    sub_butt_4 = st.form_submit_button(label="USD -> CZK",      use_container_width=True
    )

    def f4_usd_to_czk(usd_obj, usd_rate):
        result = usd_obj * usd_rate
        return result

    f4_result = round(f4_usd_to_czk(usd_obj, usd_rate), 4)

    if sub_butt_4:
        st.write(f"{usd_obj} USD = {f4_result} CZK")
