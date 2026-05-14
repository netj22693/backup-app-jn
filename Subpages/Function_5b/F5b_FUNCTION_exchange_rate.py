import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text, Engine
from Subpages.Function_5b.F5b_SQL_queries import sql_query_exchange_rate_data
from Subpages.Function_5b.F5b_charts import create_chart



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

    # Grouping of values based on date 2026-05-14 -> taking just the ltest value
    # Note: the scheduler runs multiple time per day, there can be avg 4-5 records of rate per date -> That's why to take the last 
    df = df.groupby("created_at").tail(1)

    return  df

# Engine creation
db_engine = connection_db()

# Creation DF from DB
with db_engine.connect() as conn:
    df_table_full = pd.read_sql_query(sql=text(sql_query_exchange_rate_data), con=conn)


df_eur_to_czk = df_split_data_clean_up(df_table_full, "eur_to_czk")
df_usd_to_czk = df_split_data_clean_up(df_table_full, "usd_to_czk")
df_eur_to_usd = df_split_data_clean_up(df_table_full, "eur_to_usd")

# Creation of charts
chart_eur_to_czk = create_chart(df_eur_to_czk, "created_at", "eur_to_czk", "#3206F5", "EUR to CZK", "CZK")
chart_usd_to_czk = create_chart(df_usd_to_czk, "created_at", "usd_to_czk", "#111111", "USD to CZK", "CZK")
chart_eur_to_usd  = create_chart(df_eur_to_usd, "created_at", "eur_to_usd", "#CE6B0E", "EUR to USD", "USD")



# =================== App UI ===================
st.write("# Exchange Rate - Trend:")
''
''
st.write("""- EUR to CZK:""")
st.plotly_chart(chart_eur_to_czk, use_container_width=True)

st.write("""- USD to CZK:""")
st.plotly_chart(chart_usd_to_czk, use_container_width=True)

st.write("""- EUR to USD:""")
st.plotly_chart(chart_eur_to_usd, use_container_width=True)