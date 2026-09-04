import streamlit as st
import logging
import plotly.express as px
import pandas as pd
from app_logging import inicialization_logging


# ===== Inicialization for logging =====
inicialization_logging()


# ===== Functions =====
def data_parsing(data_json: dict, function_id: str, api_name: str) -> tuple[int, int] | tuple[None, None]:

    try:
        used = data_json['quotas']['month']['used']
        remaining = data_json['quotas']['month']['remaining']

        logging.info(f"{function_id} - STATISTICS - Parsing API - {api_name} - SUCCESS")

        return used, remaining


    except KeyError:
        logging.warning(f"{function_id} - STATISTICS - Parsing API - {api_name} - KeyError")


    except Exception as e:
        logging.warning(f"{function_id} - STATISTICS - Parsing API - {api_name} - FAIL: {e}")


    return None, None


def create_pie_chart(df: pd.DataFrame):

     return px.pie(
        df, 
        names = "Topics",
        values = "Figures",
        title = "GET Requests This Month"
        )  


# ===== Orchestration function + UI visualization =====
def display_statistics(data_json: dict, function_id: str, api_name: str):

    used, remaining = data_parsing(data_json, function_id, api_name)

    if used == None or remaining == None:
        st.warning("The status API is currently not available.")
        return

    df = pd.DataFrame({
        "Figures" : [used,remaining],
        "Topics" : [f"Used:  {used}",f"Remaining:  {remaining}"],
    })


    # UI
    st.write("")
    st.write(f"""
    - This month **used: {used}** and **remaining: {remaining}** requests
    - The data will be **cached** here for **next 10 minutes**
    """)

    st.write(create_pie_chart(df))
