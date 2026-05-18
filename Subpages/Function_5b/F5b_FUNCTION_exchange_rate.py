import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text, Engine
from Subpages.Function_5b.F5b_SQL_queries import sql_query_exchange_rate_data
from Subpages.Function_5b.F5b_charts import create_chart

# GLOBAL variable - Value for rounding
round_value = 3
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
        print("DB connection established")
        return engine

    except Exception as e:
        print(f"DB connection failed: {e}")
        db_connection_fail()


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


def get_values_for_metric(df:pd.DataFrame) -> float:

    df = df.tail(2)
    previous = round(df.iloc[0,1],round_value)
    last = round(df.iloc[1,1], round_value)

    return previous, last


def df_split_data_clean_up(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    '''
    Split of full DF pulled from DB into small DFs accordingly to column name -> values for particular currency
    '''

    # Small DF from 2 columns
    df = df[["created_at", column_name]]

    # Drop of NULL values
    df = df.loc[df[column_name].notna()]

    # Sorting based on data/time TIMESTAMPZ format form DB still 2026-05-14 07:01:18.101787+00
    df = df.sort_values("created_at")

    # Drop of TIME and Z -> 2026-05-14
    df["created_at"] = pd.to_datetime(df["created_at"]).dt.date

    # Grouping of values based on date 2026-05-14 -> taking just the latest value
    # Note: the scheduler runs multiple time per day, there can be avg 4-5 records of rate per date -> That's why to take the last 
    df = df.groupby("created_at").tail(1)

    # Get values for metrics
    previous, last = get_values_for_metric(df)

    # Get delta values for metrics
    delta_last_previous = get_delta(previous, last)

    # Get avg
    avg = get_avg(df)

    # Get min and max
    min_value, date_min, max_value, date_max = get_min_max(df)

    return df, last, delta_last_previous, avg, min_value, date_min, max_value, date_max

# Engine creation
db_engine = connection_db()

# Creation DF from DB
with db_engine.connect() as conn:
    df_table_full = pd.read_sql_query(sql=text(sql_query_exchange_rate_data), con=conn)


df_eur_to_czk, value_eur_to_czk_last, delta_eur_to_czk, avg_eur_to_czk, min_eur_to_czk, min_date_eur_to_czk, max_eur_to_czk, max_date_eur_to_czk  = df_split_data_clean_up(df_table_full, "eur_to_czk")
df_usd_to_czk, value_usd_to_czk_last, delta_usd_to_czk, avg_usd_to_czk, min_usd_to_czk, min_date_usd_to_czk,max_usd_to_czk, max_date_usd_to_czk = df_split_data_clean_up(df_table_full, "usd_to_czk")
df_eur_to_usd, value_eur_to_usd_last, delta_eur_to_usd, avg_eur_to_usd, min_eur_to_usd, min_date_eur_to_usd, max_eur_to_usd, max_date_eur_to_usd = df_split_data_clean_up(df_table_full, "eur_to_usd")

# Creation of charts
chart_eur_to_czk = create_chart(df_eur_to_czk, "created_at", "eur_to_czk", "#3206F5", "EUR to CZK", "CZK")
chart_usd_to_czk = create_chart(df_usd_to_czk, "created_at", "usd_to_czk", "#111111", "USD to CZK", "CZK")
chart_eur_to_usd  = create_chart(df_eur_to_usd, "created_at", "eur_to_usd", "#CE6B0E", "EUR to USD", "USD")



# =================== App UI ===================
st.write("# Exchange Rate - Trend:")
''
''
tab1, tab2, tab3 = st.tabs([
    "EUR to CZK",
    "USD to CZK",
    "EUR to USD"
])


with tab1:
    ''
    st.metric("Last record", value=f"{value_eur_to_czk_last:.3f}", delta=delta_eur_to_czk)
    col1, col2, col3 = st.columns(3)
    col1.metric("Average", value=f"{avg_eur_to_czk:.3f}")
    col2.metric(f"Max (on {max_date_eur_to_czk})", value=f"{max_eur_to_czk:.3f}")
    col3.metric(f"Min (on {min_date_eur_to_czk})", value=f"{min_eur_to_czk:.3f}")
    ''
    ''
    st.plotly_chart(chart_eur_to_czk, width="stretch")

with tab2:
    ''
    st.metric("Last record", value=f"{value_usd_to_czk_last:.3f}", delta=delta_usd_to_czk)
    col1, col2, col3 = st.columns(3)
    col1.metric("Average", value=f"{avg_usd_to_czk:.3f}")
    col2.metric(f"Max (on {max_date_usd_to_czk})", value=f"{max_usd_to_czk:.3f}")
    col3.metric(f"Min (on {min_date_usd_to_czk})", value=f"{min_usd_to_czk:.3f}")
    ''
    ''
    st.plotly_chart(chart_usd_to_czk, width="stretch")

with tab3:
    ''
    st.metric("Last record", value=f"{value_eur_to_usd_last:.3f}", delta=delta_eur_to_usd)
    col1, col2, col3 = st.columns(3)
    col1.metric("Average", value=f"{avg_eur_to_usd:.3f}")
    col2.metric(f"Max (on {max_date_eur_to_usd})", value=f"{max_eur_to_usd:.3f}")
    col3.metric(f"Min (on {min_date_eur_to_usd})", value=f"{min_eur_to_usd:.3f}")
    ''
    ''
    st.plotly_chart(chart_eur_to_usd, width="stretch")