import streamlit as st
import logging
from app_logging import inicialization_logging
from sqlalchemy import create_engine, Engine


# ===== Inicialization for logging ===== 
inicialization_logging()


# ===== Dialog windows related to DB ===== 
@st.dialog("Error: DB not connected")
def display_dialog_function_not_available(function_id: str):

    st.warning(f"Application is not able to establish connection with DB server -> **This {function_id} is currently not available**")
    st.stop()


# ===== DB connection ===== 
def db_connection(function_id: str) -> Engine:

    '''
    function_id: FX -> id of function which call the db_connect() -> for logic of dialog window
    '''

    # Load secrets
    password = st.secrets["neon"]["password"]
    endpoint = st.secrets["neon"]["endpoint"]
    user = st.secrets["neon"]["user"]

    # connection string
    try: 
        conn_string = f"postgresql+psycopg2://{user}:{password}@{endpoint}.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

        engine = create_engine(conn_string)
        logging.info(f"{function_id} - DB connection established")
        return engine


    except Exception as e:
        logging.error(f"{function_id} - DB connection failed: {e}")

        # Functions which require dialog/info to be displayed to the user
        if function_id in ("F3", "F3B", "F5B", "F7", "F7B", "F8"):
            display_dialog_function_not_available(function_id)
