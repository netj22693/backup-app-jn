import streamlit as st
import requests
import json
import streamlit as st

# API count/remaining
api_count = "https://api.freecurrencyapi.com/v1/status?apikey=fca_live_6SzWJxPYa8Co3Xr9ziCTd7Mt7Yavrhpy2M5A0JZ4"

# get reguest
@st.cache_data(ttl=600)
def get_response_api_3(api_count):
    api_3 = requests.get(api_count, verify=False).text
    return api_3

api_3 = get_response_api_3(api_count)

# JSON format creation
api_3_json = json.loads(api_3)

# Search for data in the API defined format - JSON


used = api_3_json['quotas']['month']['used']
remaining = api_3_json['quotas']['month']['remaining']

st.write(used)
st.write(remaining)