import streamlit as st
import pandas as pd
import logging
import time
from datetime import datetime, timezone, timedelta
from sqlalchemy import create_engine, text, Engine
from Subpages.Function_5b.F5b_SQL_queries import sql_query_exchange_rate_data
from Subpages.Function_5b.F5b_charts import create_chart

# =================== App UI  ===================
st.write("# Exchange Rate - Trend:")
''
''
options = ["Last 30 days","Current month"]
radio_selected = st.radio("Range", options=options, label_visibility="collapsed")
''
''
tab1, tab2, tab3 = st.tabs([
    "EUR to CZK",
    "USD to CZK",
    "EUR to USD"
])
# -----------------------------------------------


# GLOBAL variable - Value for rounding
round_value = 3
# ------------------------------------

# Inicialization for logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    force=True
)
# ------------------------------------

@st.dialog("Error: DB not connected")
def db_connection_fail():

    st.warning("Application is not able to establish connection with DB server -> **This 5B Function is currently not available**")
    st.stop()


def connection_db() -> Engine:

    try: 
        # Load secrets
        password = st.secrets["neon"]["password"]
        endpoint = st.secrets["neon"]["endpoint"]

        # connection string
        conn_string = f"postgresql+psycopg2://neondb_owner:{password}@{endpoint}.gwc.azure.neon.tech/neondb?sslmode=require"

        engine = create_engine(conn_string)

        with engine.connect() as conn:
            logging.info("DB connection established")

        return engine

    except Exception as e:
        logging.error(f"DB connection failed: {e}")
        db_connection_fail()


   

def get_date_range(radio_input: str) -> dict:
    '''
    - To detrmin date from/to based radio button selection from user
    '''

    now = datetime.now(timezone.utc)

    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    month_range_past =  today_start - timedelta(days=30)

    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)

    mapping = {
        "Last 30 days": {
            "start": month_range_past,
            "end": now
        },
        "Current month": {
            "start": start_of_month,
            "end": now
        }
    }

    return mapping[radio_input]


def get_avg(df:pd.DataFrame) -> float:

    return round(df.iloc[:,1].mean(), round_value)


def get_min_max(df:pd.DataFrame) -> tuple[float, str]:

    min_value = round(df.iloc[:,1].min(), round_value)
    date_min = df.loc[df.iloc[:,1].idxmin(), df.columns[0]]
    date_min = pd.to_datetime(date_min).strftime("%d-%b-%Y")

    max_value = round(df.iloc[:,1].max(), round_value)
    date_max= df.loc[df.iloc[:,1].idxmax(), df.columns[0]]
    date_max = pd.to_datetime(date_max).strftime("%d-%b-%Y")
    
    return min_value, date_min, max_value, date_max



def get_delta(previous: float, last: float) -> float:

    return round(((last - previous)/previous) * 100, 2)   


def get_values_for_metrics(df:pd.DataFrame) -> tuple[float, float, str]:
    '''
    - If there is less than 2 records (can happen on 1st of month) -> elif condition
    - Tail - Takes 2 latest records from DF -> 'last' and 'previous'
    - .iloc - Takes valus from DF -> float 
    - produces date in string format of the last record
    Purpose: 
        - floats for metrics/comparison purposes
        - date_str -> to visualize from which date the last record in DB is
    '''
    number_rows = len(df.index)

    if number_rows >= 2:
        df = df.tail(2)
        previous = round(df.iloc[0,1],round_value)
        last = round(df.iloc[1,1], round_value)
        last_date = df.iloc[1,0]
        last_date_str = last_date.strftime("%d-%b-%Y")
    
    elif number_rows == 1:
        last = round(df.iloc[0,1],round_value)
        previous = last
        last_date = df.iloc[0,0]
        last_date_str = last_date.strftime("%d-%b-%Y")

    else:
        # 0 rows: DF is empty -> this case is supposed to be stoped in main if/else logic and this function should not be called at all
        logging.error(f"Get_values_for_metrics - this condition cannot happen")
        st.write("tu?")
        previous = last = last_date_str = None
        st.write(previous)
        st.write(last)


    return previous, last, last_date_str


def df_split_data_clean_up(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    '''
    Split of full DF pulled from DB into small DFs accordingly to column name -> values for particular currency
    '''

    # Small DF from 3 columns
    column_state = column_name + "_state"
    df = df[["created_at", column_name, column_state]]
    st.write(df)


    # Drop of NULL values
    # df = df.loc[df[column_name].notna()]
    # st.write(df)
    df = df[df[column_state]  == "SUCCESS"]

    # Sorting based on data/time TIMESTAMPZ format form DB still 2026-05-14 07:01:18.101787+00
    df = df.sort_values("created_at")

    # Drop of TIME and Z -> 2026-05-14
    df["created_at"] = pd.to_datetime(df["created_at"]).dt.date

    # Grouping of values based on date 2026-05-14 -> taking just the latest value
    # Note: the scheduler runs multiple time per day, there can be avg 4-5 records of rate per date -> That's why to take the last 
    df = df.groupby("created_at").tail(1)

    return df

def extract_variables_from_df(df: pd.DataFrame):
    # Sorting based on data/time TIMESTAMPZ format form DB still 2026-05-14 07:01:18.101787+00
    df = df.sort_values("created_at")

    # Drop of TIME and Z -> 2026-05-14
    df["created_at"] = pd.to_datetime(df["created_at"]).dt.date

    # Grouping of values based on date 2026-05-14 -> taking just the latest value
    # Note: the scheduler runs multiple time per day, there can be avg 4-5 records of rate per date -> That's why to take the last 
    df = df.groupby("created_at").tail(1)

    # Get values for metrics
    previous, last, last_date_str = get_values_for_metrics(df)

    # Get delta values for metrics
    delta_last_previous = get_delta(previous, last)

    # Get avg
    avg = get_avg(df)

    # Get min and max
    min_value, date_min, max_value, date_max = get_min_max(df)

    return last, delta_last_previous, avg, min_value, date_min, max_value, date_max, last_date_str


# Determin date rage for DB query -> parameters
dict_range_date = get_date_range(radio_selected)
start = dict_range_date["start"]
end = dict_range_date["end"]

# Engine creation
db_engine = connection_db()

# Creation DF from DB
with db_engine.connect() as conn:
    df_table_full = pd.read_sql_query(sql=text(sql_query_exchange_rate_data), con=conn, params = {
    "start": start,
    "end": end
    })

# Fallback - case: 1st day in month -> user selects 'Current month' (radio button) but no record in DB yet because scheduler has not run yet. 
if df_table_full.empty:
    st.info("""
    - For current month there is **no record in DB yet**
    - The automated scheduler has not run yet today
    - **Should be visible within next few hours**
    """) 

else:
    
    df_eur_to_czk = df_split_data_clean_up(df_table_full, "eur_to_czk")
    df_usd_to_czk = df_split_data_clean_up(df_table_full, "usd_to_czk")
    df_eur_to_usd = df_split_data_clean_up(df_table_full, "eur_to_usd")

    
    value_eur_to_czk_last, delta_eur_to_czk, avg_eur_to_czk, min_eur_to_czk, min_date_eur_to_czk, max_eur_to_czk, max_date_eur_to_czk, last_date_str_eur_to_czk = extract_variables_from_df(df_eur_to_czk)
    value_usd_to_czk_last, delta_usd_to_czk, avg_usd_to_czk, min_usd_to_czk, min_date_usd_to_czk,max_usd_to_czk, max_date_usd_to_czk, last_date_str_usd_to_czk = extract_variables_from_df(df_usd_to_czk)
    value_eur_to_usd_last, delta_eur_to_usd, avg_eur_to_usd, min_eur_to_usd, min_date_eur_to_usd, max_eur_to_usd, max_date_eur_to_usd, last_date_str_eur_to_usd = extract_variables_from_df(df_eur_to_usd)

    # Creation of charts
    chart_eur_to_czk = create_chart(df_eur_to_czk, "created_at", "eur_to_czk", "#3206F5", "EUR to CZK", "CZK")
    chart_usd_to_czk = create_chart(df_usd_to_czk, "created_at", "usd_to_czk", "#111111", "USD to CZK", "CZK")
    chart_eur_to_usd  = create_chart(df_eur_to_usd, "created_at", "eur_to_usd", "#CE6B0E", "EUR to USD", "USD")



    # =================== App UI - content -> result ===================

    with tab1:
        ''
        st.metric(f"Last record ({last_date_str_eur_to_czk})", value=f"{value_eur_to_czk_last:.3f}", delta=delta_eur_to_czk)
        col1, col2, col3 = st.columns(3)
        col1.metric("Average", value=f"{avg_eur_to_czk:.3f}")
        col2.metric(f"Max (on {max_date_eur_to_czk})", value=f"{max_eur_to_czk:.3f}")
        col3.metric(f"Min (on {min_date_eur_to_czk})", value=f"{min_eur_to_czk:.3f}")
        ''
        ''
        st.plotly_chart(chart_eur_to_czk, width="stretch")

    with tab2:
        ''
        st.metric(f"Last record ({last_date_str_usd_to_czk})", value=f"{value_usd_to_czk_last:.3f}", delta=delta_usd_to_czk)
        col1, col2, col3 = st.columns(3)
        col1.metric("Average", value=f"{avg_usd_to_czk:.3f}")
        col2.metric(f"Max (on {max_date_usd_to_czk})", value=f"{max_usd_to_czk:.3f}")
        col3.metric(f"Min (on {min_date_usd_to_czk})", value=f"{min_usd_to_czk:.3f}")
        ''
        ''
        st.plotly_chart(chart_usd_to_czk, width="stretch")

    with tab3:
        ''
        st.metric(f"Last record ({last_date_str_eur_to_usd})", value=f"{value_eur_to_usd_last:.3f}", delta=delta_eur_to_usd)
        col1, col2, col3 = st.columns(3)
        col1.metric("Average", value=f"{avg_eur_to_usd:.3f}")
        col2.metric(f"Max (on {max_date_eur_to_usd})", value=f"{max_eur_to_usd:.3f}")
        col3.metric(f"Min (on {min_date_eur_to_usd})", value=f"{min_eur_to_usd:.3f}")
        ''
        ''
        st.plotly_chart(chart_eur_to_usd, width="stretch")