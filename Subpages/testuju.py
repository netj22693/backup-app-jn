import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
from typing import Optional
from Subpages.F7b_SQL_queries import sql_query_table_overview, sql_offer_exists, sql_table_offer, sql_table_delivery, sql_table_costs, sql_table_extra_steps_time, sql_table_sla

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

    # Query into DB + DF styling
    df = pd.read_sql(sql_query_table_overview,db_engine)

    df[" "] = df.index + 1
    df = df.set_index(" ")

    df_styled = df.style.format({
        "Final price": "{:,.2f}",
        })
        
    # Styled DF visualization
    st.dataframe(df_styled, width = "stretch", height=562)

# ====================== TAB 2 ======================
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
        offer_input_validated = input_validation(offer_input_user)

        st.write("result validation II:", offer_input_validated)

        if offer_input_validated is not None:
            st.write("ready for query")

            # Queries into DB           
            with db_engine.connect() as conn:
                params = {"offer_id": offer_input_validated}

                offer_id_exists = pd.read_sql_query(sql=text(sql_offer_exists), con=conn, params=params)
                
                # Validation if inserted offer_id by user exists in DB 
                if offer_id_exists.empty:
                    st.warning(f"Offer id **{offer_input_validated}** does not exist.")

                else:
                    offer_id_exists = offer_id_exists["offer_id"].iloc[0]

                    # a.OFFER
                    df_table_offer = pd.read_sql_query(sql=text(sql_table_offer), con=conn, params=params)
                    
                    # Extracting data from DF -> variables
                    offer_created_date = df_table_offer["created_date"].iloc[0]
                    offer_created_time = df_table_offer["created_time"].iloc[0]
                    offer_need_approve_date = df_table_offer["need_approve_date"].iloc[0]
                    offer_need_approve_time = df_table_offer["need_approve_time"].iloc[0]
                    offer_need_approve_days = df_table_offer["need_approve_days"].iloc[0]
                    offer_transport = df_table_offer["transport"].iloc[0]
                    offer_service = df_table_offer["service"].iloc[0]
                    offer_time_zone = df_table_offer["time_zone"].iloc[0]
                    offer_time_overall = df_table_offer["time_overall"].iloc[0]
                    offer_expected_delivery = df_table_offer["expected_delivery"].iloc[0]
                    offer_final_price = df_table_offer["final_price"].iloc[0]
                    offer_currency = df_table_offer["currency"].iloc[0]

                    # b.DELIVERY
                    df_table_delivery = pd.read_sql_query(sql=text(sql_table_delivery), con=conn, params=params)

                    # Extracting data from DF -> variables
                    delivery_from_country = df_table_delivery["from_country"].iloc[0]
                    delivery_from_city = df_table_delivery["from_city"].iloc[0]
                    delivery_from_dtd = df_table_delivery["from_dtd"].iloc[0]
                    delivery_to_country = df_table_delivery["to_country"].iloc[0]
                    delivery_to_city = df_table_delivery["to_city"].iloc[0]
                    delivery_to_dtd = df_table_delivery["to_dtd"].iloc[0]
                    delivery_distance_length = df_table_delivery["distance_length"].iloc[0]
                    delivery_dtd_time = df_table_delivery["dtd_time"].iloc[0]

                    # c.COSTS
                    df_table_costs = pd.read_sql_query(sql=text(sql_table_costs), con=conn, params=params)

                    # Extracting data from DF -> variables
                    costs_distance_cost = df_table_costs["distance_cost"].iloc[0]
                    costs_dtd_from = df_table_costs["dtd_from"].iloc[0]
                    costs_dtd_to = df_table_costs["dtd_to"].iloc[0]
                    costs_shipment_value = df_table_costs["shipment_value"].iloc[0]
                    costs_insurance = df_table_costs["insurance"].iloc[0]
                    costs_fragile = df_table_costs["fragile"].iloc[0]
                    costs_danger = df_table_costs["danger"].iloc[0]

                    # e.EXTRA_STEPS_TIME
                    df_table_extra_steps_time = pd.read_sql_query(sql=text(sql_table_extra_steps_time), con=conn, params=params)  

                    # Extracting data from DF -> variables    
                    extra_steps_time_truck_breaks = df_table_extra_steps_time["truck_breaks"].iloc[0]
                    extra_steps_time_shipment_transfer_dtd_from = df_table_extra_steps_time["shipment_transfer_dtd_from"].iloc[0]
                    extra_steps_time_shipment_transfer_dtd_to = df_table_extra_steps_time["shipment_transfer_dtd_to"].iloc[0]
                    extra_steps_time_dtd_truck_if_not_truck_main = df_table_extra_steps_time["dtd_truck_if_not_truck_main"].iloc[0]

                    # e.SLA
                    df_table_sla = pd.read_sql_query(sql=text(sql_table_sla), con=conn, params=params)  

                    # Extracting data from DF -> variables  
                    sla_distance_cost = df_table_sla["time_sla"].iloc[0]


                    # NEXT STEP: variables to be put into UI visualization -> Offer 
                    # NEXT STEP: Add diagrams/pictures svg per selected transport DTD A B Transport types...

