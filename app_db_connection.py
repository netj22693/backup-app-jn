import streamlit as st
import logging
from app_logging import inicialization_logging
from sqlalchemy import create_engine, Engine, text


# ===== Inicialization for logging ===== 
inicialization_logging()


# ===== Dialog windows related to DB ===== 
@st.dialog("Error: DB not connected")
def display_dialog_function_not_available(function_id: str):

    st.warning(f"Application is not able to establish connection with DB server -> **This {function_id} is currently not available**")
    st.stop()


# ===== DB connection ===== 
def db_connection(function_id: str, dialog_to_display: bool) -> Engine:

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

        # Immediate test of the connection by query into DB
        # Note: To prevent fail of insert into DB in case that there is any credential issue. To find out now when Engine is created and not later. This will immediatelly trigger DB FALLBACK LOGIC
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        logging.info(f"{function_id} - DB connection - SUCCESS")
        return engine


    except Exception as e:
        logging.error(f"{function_id} - DB connection - FAIL - {e}")

        # If dialog/info to be displayed to the user is required 
        if dialog_to_display == True:
            display_dialog_function_not_available(function_id)
