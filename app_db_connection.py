import streamlit as st
import logging
from app_logging import inicialization_logging
from Subpages.Resources_ui_objects import render_warning_info
from sqlalchemy import create_engine, Engine, text


# ===== Inicialization for logging ===== 
inicialization_logging()


# ===== Dialog windows related to DB ===== 
@st.dialog("Error: DB not connected")
def display_dialog_function_not_available(function_id: str):

    render_warning_info(f"**DB connection issue** - the **{function_id}** is currently not available.")
    st.stop()


# ===== DB Engine cache + Health check ===== 

@st.cache_resource(show_spinner=False)
def get_db_engine() -> Engine:

    '''
    - Creation of Engine and immediate database connection test
    (handshake with the database).
    - The successfully initialized Engine is cached using st.cache_resource.
    Engine creation and the initial connection test are then not repeated
    on every app rerun.
    - Reduces unnecessary compute and connection initialization overhead on every app rerun: approximately 1.6 seconds -> 0.0001 seconds (cached Engine)
    - The Engine resources is shared across aplication Functions
    - Note - Neon DB documentation:
        - The first connection may have slightly higher latency than subsequent
        connections to an already-active compute.
        - After 5 minutes of inactivity, Neon Free suspends the compute.
        The next connection triggers a cold start and may have higher latency
        (approximately 2.9 seconds observed in this application).
    '''

    logging.info("DB - get_db_engine(): Engine creation started")

    password = st.secrets["neon"]["password"]
    endpoint = st.secrets["neon"]["endpoint"]
    user = st.secrets["neon"]["user"]

    conn_string = f"postgresql+psycopg2://{user}:{password}@{endpoint}.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

    engine = create_engine(
        conn_string,
        pool_pre_ping=True
    )
    
    # Immediate test of the connection by query into DB
    # Note: To prevent fail of insert into DB in case that there is any credential issue. To find out now when Engine is created and not later. This will immediatelly trigger DB FALLBACK LOGIC
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return engine

    except Exception:
        # .dispose() -> drop not working connection pool (not Engine)
        engine.dispose()
        raise

# ===== DB connection ===== 
def db_connection(function_id: str, dialog_to_display: bool) -> Engine:

    '''
    function_id: FX -> id of the Function which call the db_connection() -> logic of dialog window
    ''' 

    try: 
        engine = get_db_engine()

        logging.info(f"{function_id} - DB connection - SUCCESS")
        return engine


    except Exception as e:
        logging.error(f"{function_id} - DB connection - FAIL - {e}")

        # If dialog/info to be displayed to the user is required 
        if dialog_to_display == True:
            display_dialog_function_not_available(function_id)
