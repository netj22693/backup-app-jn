import streamlit as st
from sqlalchemy import create_engine
import pandas as pd

@st.dialog("Error: DB not connected")
def db_connection_fail():

    st.warning("Application is not able to establish connection with DB server -> **This 7B Function is currently not available**")
    st.stop()


def connection_db():

    try: 
        # Load secrets
        password = st.secrets["neon"]["password"]
        endpoint = st.secrets["neon"]["endpoint"]

        # connection string
        conn_string = f"postgresql+psycopg2://neondb_owner:{password}@{endpoint}.gwc.azure.neon.tech/neondb?sslmode=require"

        engine = create_engine(conn_string)
        return engine

    except Exception as e:
        print(f"DB connection failed: {e}")
        db_connection_fail()


# ================ Application Screen - INPUT Buttons ========================
st.write("# Find your offer:")
''

st.write("- Simple view into DB. Based on offers created in Function 7...")
''

tab1, tab2 = st.tabs([
    "Last 15 offers",
    "Search for specific offer",
])


with tab1:
    db_engine = connection_db()

    df = pd.read_sql("""
        SELECT 
            a.offer_id as "Offer id",
            f.label as "Transport",
            b.from_city "From",
            b.to_city as "To",
            a.created_date as "Created day",
            a.created_time as "Created time",
            i.label as "Time zone",
            a.expected_delivery as "Expected delivery",
            a.final_price as "Final price",
            j.label as "Currency"                    
                     
        FROM function7.offer a
            INNER JOIN function7.delivery b ON (a.offer_id = b.offer_id)
            INNER JOIN function7.transport_type f ON (a.transport = f.transport_id)
            INNER JOIN function7.time_zone i ON (a.time_zone = i.zone_id)
            INNER JOIN function7.currency_detail j ON (a.currency = j.currency_id)
                     
        ORDER BY a.offer_id DESC
        LIMIT 15
        ;""",db_engine)


    df[" "] = df.index + 1
    df = df.set_index(" ")

    df_styled = df.style.format({
        "Final price": "{:,.2f}",
        })
        
    # Styled DF visualization
    st.dataframe(df_styled, width = "stretch", height=562)


with tab2:
    st.info("This section is under build - to be available soon")