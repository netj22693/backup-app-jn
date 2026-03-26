import streamlit as st
from sqlalchemy import create_engine, text, bindparam
import pandas as pd
from typing import Optional
from Subpages.F7_UI_image_generator import provide_ui_image_path, provide_ui_color_coding_image
from Subpages.F7b_SQL_queries import sql_query_table_overview, sql_offer_exists, sql_table_offer, sql_table_delivery, sql_table_costs, sql_table_extra_steps_time, sql_table_sla, get_sql_query_tab_3
from Subpages.F7_input_data import tranport_types_list, dataset_test

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

st.write("- View into DB. Based on offers created in Function 7...")
''

tab1, tab2, tab3 = st.tabs([
    "Last 15 offers",
    "Search for specific offer",
    "Customized search"
])

#Connection can be used across tabs
db_engine = connection_db()

with tab1:

    ''
    if st.button("Show last 15 offers", width="stretch", icon=":material/table:"):
        ''
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
           
            submit_button = st.form_submit_button(label= "Submit", width="stretch", icon = ":material/apps:",)


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


# ====================== TAB 3 ======================
# ====================== main logic for tab3 + relevant def functions ======================

def reset_filters():
    st.session_state["key_mlts_country_from"] = list_countries_upper
    st.session_state["key_mlts_country_to"] = list_countries_upper
    st.session_state["key_mlts_transport"] = tranport_types_list
    st.session_state["key_mlts_currency"] = currency_list
    st.session_state["key_sld_number_rows"] = 20



def create_parameters_for_sql(input, param_letter):
    '''
    Context: Parametrized queries using IN() in SQL are horribly slowing down returning result from PostgreSQL back to the code. Thus:

    THIS FUNCTION DOES DYNAMIC MAPPING to avoid SQL injection as the SQL query is built on f-string principle

    1) build of unique parameter e.g. t0, t1, t2 (depends on the param_letter)
    2) Creation of list [":t0", ":t1", ":t2"] -> list_params_keys[] filled with values
    3) Adding "key":"value" into dict params {} -> {"t0":"Airplane", "t1":"Train", "t2":"Truck"}
    4) Creation of string for sql ":t0, :t1, :t2" -> string_for_sql_in
    '''
    list_params_keys = []
    params = {}

    i = 0
    for value in input:
        param_name = param_letter + str(i)
        list_params_keys.append(":" + param_name)
        params[param_name] = value
        i = i + 1
    
    string_for_sql_in = ", ".join(list_params_keys)
    return params, string_for_sql_in



with tab3: 

    #From the dataset -> parse keys -> create list of countries for multiselect
    list_countries = dataset_test.keys()

    list_countries_upper = []
    for country in list_countries:
        upper = country.upper()
        list_countries_upper.append(upper)

    # Preparation of lists for multiselects
    list_countries_upper.sort()
    tranport_types_list.sort()

    currency_list = ['euro','koruna']
    currency_list.sort()

    # Initiating session states for purpose/possibility of reseting filters
    if "key_mlts_country_from" not in st.session_state:
        st.session_state["key_mlts_country_from"] = list_countries_upper

    if "key_mlts_country_to" not in st.session_state:
        st.session_state["key_mlts_country_to"] = list_countries_upper

    if "key_mlts_transport" not in st.session_state:
        st.session_state["key_mlts_transport"] = tranport_types_list

    if "key_mlts_currency" not in st.session_state:
        st.session_state["key_mlts_currency"] = currency_list

    if "key_sld_number_rows" not in st.session_state:
        st.session_state["key_sld_number_rows"] = 20

    # Multiselect - Country from
    ''
    selected_coutry_from = st.multiselect("Country from", options=list_countries_upper, key="key_mlts_country_from")

    if len(selected_coutry_from) == 0:
        st.warning("At least 1 country needs to be selected")

    # Multiselect - Country to
    selected_coutry_to = st.multiselect("Country to", options=list_countries_upper, key="key_mlts_country_to")

    if len(selected_coutry_to) == 0:
        st.warning("At least 1 country needs to be selected")
    
    # Multiselect - Transport type
    selected_transport = st.multiselect("Transport", options=tranport_types_list, key="key_mlts_transport")

    if len(selected_transport) == 0:
        st.warning("At least 1 transport needs to be selected")

    # Multiselect - Currency
    selected_currency = st.multiselect("Currency", options=currency_list, key="key_mlts_currency")

    if len(selected_currency) == 0:
        st.warning("At least 1 currency needs to be selected")

    # Slider - number of rows
    number_rows = st.slider("Number of records to be shown", min_value=5, max_value=50, step=5, label_visibility="visible", key="key_sld_number_rows")


    # ===== Reset button =====
    ''
    st.button("Reset filters", on_click=reset_filters, width="stretch", icon= ":material/delete:")
    ''
    st.write("-" *10)


    # ===== Submit button -> triggering query into DB =====

    if any(not x for x in [
        selected_coutry_from,
        selected_coutry_to,
        selected_transport,
        selected_currency
    ]):
        submit_button_tab3 = st.button("Submit", width= "stretch", icon=":material/apps:", disabled=True)

    else:   
        submit_button_tab3 = st.button("Submit", width= "stretch", icon=":material/apps:")


    if submit_button_tab3:
        
        # Creation of parameter for SQL query 
        # The query uses IN() and stadard parametrization approach horribly slowed the query down -> this approach with f-string in query works better (parametrization like this prevents from SQL injestion)
        params_transport, str_for_sql_in_transport = create_parameters_for_sql(selected_transport, "t")
        params_currency, str_for_sql_in_currency = create_parameters_for_sql(selected_currency, "c")
        params_country_from, str_for_sql_in_country_from = create_parameters_for_sql(selected_coutry_from, "cf")
        params_country_to, str_for_sql_in_country_to = create_parameters_for_sql(selected_coutry_to, "ct")

        # Marging of the dictionaries to have 1 dictionary with all parameters
        params_full = params_transport | params_currency | params_country_from | params_country_to

        # Gettign SQL query with inserted variables (variables = keys in paramters to be able to match "key" : "value" when query into DB triggered)
        sql_query_tab_3 = get_sql_query_tab_3(number_rows, str_for_sql_in_transport, str_for_sql_in_currency, str_for_sql_in_country_from, str_for_sql_in_country_to)

        with db_engine.connect() as conn:
            df_table_tab_3 = pd.read_sql_query(sql=text(sql_query_tab_3), con=conn, params=params_full)

            if df_table_tab_3.empty == True:
                st.info("There was no record found in DB.")

            else:
                # Dataframe styling 
                df_table_tab_3[" "] = df_table_tab_3.index + 1
                df_table_tab_3 = df_table_tab_3.set_index(" ")

                df_table_tab_3_styled = df_table_tab_3.style.format({
                "Final price": "{:,.2f}",
                })

                # Info message to the user that there is not that many records as expected
                rows_from_db = df_table_tab_3.index
                rows_from_db = rows_from_db[-1]
                
                ''
                if rows_from_db != number_rows:
                    st.info(f"There is only **{rows_from_db} records** matching the selected criteria")

                st.dataframe(df_table_tab_3_styled)