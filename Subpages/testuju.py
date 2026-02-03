import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
from typing import Optional

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

#Connection can be used across tabs
db_engine = connection_db()

with tab1:

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



# ====================== main logic for tab2 + relevant def functions ======================

def input_validation(input: str) -> Optional[str]:
    '''  
    Simple logic to have correct format of 'offer_id' before query to DB

    Covers basic scenarios:
    1) user input is correct F7-number  - e.g. F7-123
    2) user input is "lazy" number format e.g. 123 -> adjustment F7-123
    3) user input is wrong generically - e.g. f123 -> return False

    '''
    if input.startswith("F7-"):
        return input

    if input.isdigit():
        input = "F7-" + input
        return input
    
    if input == "":
        st.warning("**Missing input** - Please provide **Offer number**")
        return None

    else:
        st.error(f"Invalid Offer format inserted - **{input}** is not valid. Valid format: F7-XXX")
        return None


with tab2:
    st.info("This section is under build - to be available soon")

    with st.form(key="user_form"):
            offer_input_user = st.text_input(label="Offer number:", help="Insert **Offer number** of invoice you would like to see. It is based on invoices created in **Function 3**.")
           
            submit_button = st.form_submit_button(label= "Submit", width="stretch")


    if submit_button:
       
        offer_input_user = offer_input_user.strip().upper()
        result_validation = input_validation(offer_input_user)

        st.write("result validation II:", result_validation)

        if result_validation is not None:
            st.write("ready for query")
            # readz to build functions to run queries and visualize data


