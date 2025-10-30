from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
import streamlit as st







# Load secrets
db = st.secrets["neon"]

# connection string
try: 
    conn_string = f"postgresql+psycopg2://neondb_owner:{db['password']}@ep-lucky-bar-a9hww36i-pooler.gwc.azure.neon.tech/neondb?sslmode=require"


    engine = create_engine(conn_string)

except:
    st.warning("DB not connected")
    st.stop()

df = pd.read_sql("SELECT * FROM test_table LIMIT 5;", engine)
st.write(df.head())