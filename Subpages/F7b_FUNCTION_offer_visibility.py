import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
from typing import Optional
from Subpages.F7_UI_image_generator import provide_ui_image_path, provide_ui_color_coding_image
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

    with st.form(key="user_form"):
            offer_input_user = st.text_input(label="Offer number:", help="Insert **Offer number** of invoice you would like to see. It is based on invoices created in **Function 3**.")
           
            submit_button = st.form_submit_button(label= "Submit", width="stretch")


    if submit_button:
       
        offer_input_user = offer_input_user.strip().upper()
        offer_input_validated = input_validation(offer_input_user)

        if offer_input_validated is not None:

            # Queries into DB           
            with db_engine.connect() as conn:
                params = {"offer_id": offer_input_validated}

                offer_id_exists = pd.read_sql_query(sql=text(sql_offer_exists), con=conn, params=params)
                
                # Validation if inserted offer_id by user exists in DB to trigger the main logic 
                if offer_id_exists.empty:
                    st.warning(f"Offer id **{offer_input_validated}** does not exist.")

                else:
                    offer_id = offer_id_exists["offer_id"].iloc[0]

                    # a.OFFER
                    df_table_offer = pd.read_sql_query(sql=text(sql_table_offer), con=conn, params=params)
                    
                    # Extracting data from DF -> variables
                    row_offer = df_table_offer.iloc[0]

                    offer_created_date = row_offer["created_date"]
                    offer_created_time = row_offer["created_time"]
                    offer_need_approve_date = row_offer["need_approve_date"]
                    offer_need_approve_time = row_offer["need_approve_time"]
                    offer_need_approve_days = row_offer["need_approve_days"]
                    offer_transport = row_offer["transport"]
                    offer_service = row_offer["service"]
                    offer_time_zone = row_offer["time_zone"]
                    offer_time_overall = row_offer["time_overall"]
                    offer_expected_delivery = row_offer["expected_delivery"]
                    offer_final_price = row_offer["final_price"]
                    offer_currency = row_offer["currency"]

                    # b.DELIVERY
                    df_table_delivery = pd.read_sql_query(sql=text(sql_table_delivery), con=conn, params=params)

                    # Extracting data from DF -> variables
                    row_delivery = df_table_delivery.iloc[0]

                    delivery_from_country = row_delivery["from_country"]
                    delivery_from_city = row_delivery["from_city"]
                    delivery_from_dtd = row_delivery["from_dtd"]
                    delivery_to_country = row_delivery["to_country"]
                    delivery_to_city = row_delivery["to_city"]
                    delivery_to_dtd = row_delivery["to_dtd"]
                    delivery_distance_length = row_delivery["distance_length"]
                    delivery_distance_time = row_delivery["distance_time"]
                    delivery_dtd_time = row_delivery["dtd_time"]

                    # c.COSTS
                    df_table_costs = pd.read_sql_query(sql=text(sql_table_costs), con=conn, params=params)

                    # Extracting data from DF -> variables
                    row_costs = df_table_costs.iloc[0]

                    costs_distance_cost = row_costs["distance_cost"]
                    costs_dtd_from = row_costs["dtd_from"]
                    costs_dtd_to = row_costs["dtd_to"]
                    costs_shipment_value = row_costs["shipment_value"]
                    costs_insurance = row_costs["insurance"]
                    costs_fragile = row_costs["fragile"]
                    costs_danger = row_costs["danger"]

                    # e.EXTRA_STEPS_TIME
                    df_table_extra_steps_time = pd.read_sql_query(sql=text(sql_table_extra_steps_time), con=conn, params=params)  

                    # Extracting data from DF -> variables   
                    row_extra_steps_time = df_table_extra_steps_time.iloc[0]
                      
                    extra_steps_time_truck_breaks = row_extra_steps_time["truck_breaks"]
                    extra_steps_time_shipment_transfer_dtd_from = row_extra_steps_time["shipment_transfer_dtd_from"]
                    extra_steps_time_shipment_transfer_dtd_to = row_extra_steps_time["shipment_transfer_dtd_to"]
                    extra_steps_time_dtd_truck_if_not_truck_main = row_extra_steps_time["dtd_truck_if_not_truck_main"]

                    # e.SLA
                    df_table_sla = pd.read_sql_query(sql=text(sql_table_sla), con=conn, params=params)  

                    # Extracting data from DF -> variables  
                    row_sla = df_table_sla.iloc[0]

                    sla_time_sla = row_sla["time_sla"]


                    # ========== TAB 2 UI ========================================


                    # Function to determin day/days and hour/hoursfor UI purposes
                    def singular_or_plural(input: int) -> str:
                        if input <= 1:
                            return ""
                        
                        else:
                            return "s"
                    
                    # Determin singular or plural for UI
                    day_days_str = singular_or_plural(offer_need_approve_days)
                    hour_hours_str = singular_or_plural(offer_time_overall)

                    # Get UI image for the particular offer 
                    ui_image_path = provide_ui_image_path(offer_transport, delivery_from_dtd, delivery_to_dtd, extra_steps_time_truck_breaks)

                    ui_color_coding_image_path = provide_ui_color_coding_image(offer_transport, delivery_from_dtd, delivery_to_dtd, extra_steps_time_truck_breaks)


                    # UI
                    ''
                    ''
                    st.write(f"""
                        - Offer number: **{offer_id}**
                        - Offer created: **{offer_created_date} - {offer_created_time} {offer_time_zone}**
                        - Customer to approve till: **{offer_need_approve_date} {offer_need_approve_time} - {offer_time_zone}** ({offer_need_approve_days} day{day_days_str})
                    """)

                    # UI transport workflow image
                    ''
                    try:
                        st.image(ui_image_path)

                    except Exception as e:
                        print(e)
                        st.warning("Failed to load image")
                    
                    # Expander 
                    with st.expander("Transfer process", icon= ":material/help:"):
                        try:
                            st.image(ui_color_coding_image_path)

                        except Exception as e:
                            print(e)
                            st.warning("Failed to load image")
                        

                        # To show DTD button or not
                        if delivery_from_dtd > 0 or delivery_to_dtd > 0:

                            st.write("- More info about DTD:")
                            
                            st.link_button(
                                label = "Go to Door-to-Door page",
                                url="https://dataparsing.streamlit.app/F7_description_dtd",
                                help="The button will redirect to the relevant page within this app for download.",
                                width="stretch",
                                icon=":material/launch:"
                            )                       

                    ''
                    ''
                    st.write(f"""
                        - Delivery from **{delivery_from_city} ({delivery_from_country})** to **{delivery_to_city} ({delivery_to_country}):**
                            - Costs: **{costs_distance_cost:,.2f} {offer_currency}**
                            - Distance: **{delivery_distance_length:,.2f} km**
                            - Time to cover the distance: **{delivery_distance_time:.2f} hour(s)**
                            - Transport type: **{offer_transport}**
                    """)


                    # Different UI for Truck and Train or Airplane
                    if offer_transport == 'Truck':

                        ''
                        st.write(f"""
                            - **Door-to-Door**:
                                - Additional: **{delivery_from_dtd + delivery_to_dtd} km** to the distance
                                    - {delivery_from_city}: {delivery_from_dtd} km
                                    - {delivery_to_city}: {delivery_to_dtd} km
                                - Time to cover the Door-to-Door: **{delivery_dtd_time:.2f} hours(s)**
                        """)

                        ''
                        st.write(f"""
                        - **{offer_transport}**:
                            - Selected service **{offer_service}** requires **{sla_time_sla:.2f} hours** for administration, load, etc. - **the SLA**  
                            - If longer distance (including Door-to-Door time), **mandatory breaks** for driver: **{extra_steps_time_truck_breaks} hour(s)**
                        """)

                    if offer_transport in ('Train','Airplane'):
                        ''
                        st.write(f"""
                            - **Door-to-Door**:
                                - Additional: **{delivery_from_dtd + delivery_to_dtd} km** to the distance for which **Truck is needed**
                                    - {delivery_from_city}: {delivery_from_dtd} km
                                    - {delivery_to_city}: {delivery_to_dtd} km
                                - Time to cover the Door-to-Door: **{delivery_dtd_time:.2f} hours(s)**
                                    - Transfer {offer_transport} <-> Truck: {extra_steps_time_shipment_transfer_dtd_from + extra_steps_time_shipment_transfer_dtd_to} hour(s)
                                    - Time for Truck ride: {extra_steps_time_dtd_truck_if_not_truck_main} hour(s)
                        """)

                        ''
                        st.write(f"""
                            - **{offer_transport}**:
                                - Selected service **{offer_service}** requires **{sla_time_sla:.2f} hours** for administration, load, etc. - **the SLA**  
                        """)

                    # This UI same for all types of transport
                    ''
                    st.write("- **Overall time end-to-end delivery:**")

                    with st.container(border=True):
                        st.write(f"**{offer_time_overall:.2f} hour{hour_hours_str}**")
                

                    st.write("- **Expected delivery:**")
                    with st.container(border=True):
                        st.write(f"**{offer_expected_delivery} - {offer_time_zone}**")


                    ''
                    ''
                    st.write(f"""
                    - **Additional services - costs**:
                        - Insurance extra costs: **{costs_insurance:,.2f} {offer_currency}**
                        - Fregile goods costs: **{costs_fragile:,.2f} {offer_currency}**
                        - Danger goods costs: **{costs_danger:,.2f} {offer_currency}**
                        - Door-To-Door - {delivery_from_city} ({delivery_from_country}):  **{costs_dtd_from:,.2f} {offer_currency}** - ({delivery_from_dtd} km)
                        - Door-To-Door - {delivery_to_city} ({delivery_to_country}):  **{costs_dtd_to:,.2f} {offer_currency}** - ({delivery_to_dtd} km)
                    """)


                    ''
                    ''
                    st.write("- **Final price:**")
                    with st.container(border=True):
                        st.write(f"**{offer_final_price:,.2f} {offer_currency}**")

