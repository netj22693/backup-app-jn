import streamlit as st
import requests
from fastapi import HTTPException


# https://app.zipcodebase.com/ - 1 api call to pocita jako 6 :(
def get_api():

    try: 
        headers = { 
        "apikey": "7a293f40-56a9-11f0-9c80-b10c7877b63a"}

        params = (
        ("city","Bratislava"),
        ("country","sk"),
        );

        response = requests.get('https://app.zipcodebase.com/api/v1/code/city?apikey=7a293f40-56a9-11f0-9c80-b10c7877b63a', headers=headers, params=params);
        st.write(response.text)

        st.write(response)

        if response == "<Response [200]>":
            pass

        else:
            st.warning("API is not available - either technical issue or API calls limit reached.")
    
    except:
        st.warning("API is not available - either technical issue or API calls limit reached.")

if st.button("Test"):  
    get_api()