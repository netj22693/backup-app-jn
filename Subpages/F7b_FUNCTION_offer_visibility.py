import streamlit as st
from sqlalchemy import create_engine, text, bindparam
import pandas as pd
from datetime import date, timedelta
from typing import Optional,Dict, Tuple
import plotly.express as px
from Subpages.F7_UI_image_generator import provide_ui_image_path, provide_ui_color_coding_image
from Subpages.F7b_SQL_queries import sql_query_table_overview, sql_offer_exists, sql_table_offer, sql_table_delivery, sql_table_costs, sql_table_extra_steps_time, sql_table_sla, get_sql_query_tab_3, get_sql_query_transport, get_sql_query_service, get_sql_query_from_country, get_sql_query_to_country, get_sql_query_dtd_with_without, get_sql_query_currency, get_sql_query_from_to_country, get_sql_part_where_date, get_sql_query_city, get_sql_query_routes
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

tab1, tab2, tab3, tab4 = st.tabs([
    "Last 15 offers",
    "Search for specific offer",
    "Customized search",
    "Analytics"
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
            offer_input_user = st.text_input(label="Offer number:", help="Insert **Offer number** you would like to see. It is based on offers created in **Function 7**.")
           
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
    st.session_state["key_checkbox_date"] = False
    st.session_state["key_sld_number_rows"] = 20



def create_parameters_for_sql(input: list, param_letter: str) -> Tuple[Dict[str, str], str]:
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
    
    if "key_checkbox_date"  not in st.session_state:
        st.session_state["key_checkbox_date"] = False

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

    # Date picker
    ''
    checkbox_state = st.checkbox("Filtering based on date", key="key_checkbox_date")

    if checkbox_state == True:
        
        col1, col2 = st.columns(2)

        # Min date allowed
        min_date = date(2025, 1, 1)

        # default = today - 30 days
        default_date = date.today() - timedelta(days=30)
        max_date = date.today()

        
        picked_date_from = col1.date_input(
            "From",
            value=default_date,
            min_value = min_date,
            max_value = max_date,
            format ="DD/MM/YYYY",
            key = "key_date_input_1"
        )

        picked_date_to = col2.date_input(
            "To",
            value = max_date,
            format = "DD/MM/YYYY",
            min_value = min_date,
            max_value = max_date,
            key ="key_date_input_2")
        
        # Extending SQL query date filter
        date_query_string = f"""
        AND
        TO_DATE(a.created_date, 'DD-Mon-YY') BETWEEN DATE '{picked_date_from}' AND DATE '{picked_date_to}'
        """

        # Fallback info 
        if picked_date_from > picked_date_to:
            st.warning("Date **To** is farther in the past than **From** -> search will not work. Please change it.")

    
    if checkbox_state == False:

        # Extending SQL -> no extension, no additional filter
        date_query_string = ""
        

    # Slider - number of rows
    ''
    number_rows = st.slider("Number of records to be shown", min_value=5, max_value=50, step=5, label_visibility="visible", key="key_sld_number_rows")


    # ===== Submit button -> triggering query into DB =====

    ''
    ''
    if any(not x for x in [
        selected_coutry_from,
        selected_coutry_to,
        selected_transport,
        selected_currency
    ]):
        submit_button_tab3 = st.button("Submit", width= "stretch", icon=":material/apps:", disabled=True)

    else:   
        submit_button_tab3 = st.button("Submit", width= "stretch", icon=":material/apps:")

    # ===== Reset button =====
    st.write("-" *10)
    st.button("Reset filters", on_click=reset_filters, width="stretch", icon= ":material/delete:")


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
        sql_query_tab_3 = get_sql_query_tab_3(number_rows, date_query_string, str_for_sql_in_transport, str_for_sql_in_currency, str_for_sql_in_country_from, str_for_sql_in_country_to)

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


with tab4: 
   
    # Date picker
    ''
    radio_state_tb4 = st.radio("Filter",options=["All offers - no specific date","Date range"])

    if radio_state_tb4 == "All offers - no specific date":

        # Extending SQL -> no extension, no additional filter
        date_query_applicable = False
        picked_date_from_tab4 = None
        picked_date_to_tab4 = None


    if radio_state_tb4 == "Date range":
        
        col1_tab4, col2_tab4 = st.columns(2)

        # Min date allowed
        min_date = date(2025, 1, 1)

        # default = today - 30 days
        default_date = date.today() - timedelta(days=30)
        max_date = date.today()

        
        picked_date_from_tab4 = col1_tab4.date_input(
            "From",
            value=default_date,
            min_value = min_date,
            max_value = max_date,
            format ="DD/MM/YYYY",
            key = "key_date_input_tab4_1"
        )

        picked_date_to_tab4 = col2_tab4.date_input(
            "To",
            value = max_date,
            format = "DD/MM/YYYY",
            min_value = min_date,
            max_value = max_date,
            key ="key_date_input_tab4_2")
        
        # Extending SQL query date filter
        date_query_applicable = True


        # Fallback info 
        if picked_date_from_tab4 > picked_date_to_tab4:
            st.warning("Date **To** is farther in the past than **From** -> search will not work. Please change it.")
  

    ''
    ''
    submit_button_tab4 = st.button("Submit", width= "stretch", icon=":material/apps:", key="key_submit_button_tab4")

    if submit_button_tab4:

        with db_engine.connect() as conn:

            # Parametrization of countries
            def get_parameters_countries(country_list: list) -> dict:
                
                params_list = []
                params_dict = {}

                for item in country_list:
                    param = item.lower()
                    params_list.append(param)
                    params_dict[param] = item

                return params_dict

            # Build of parameters countries
            params_countries = get_parameters_countries(list_countries_upper)

            # Build of parameters date
            params_date = {
                "date_from" : picked_date_from_tab4,
                "date_to" : picked_date_to_tab4,
            }

            # Build of parameters joining -> full set of parametrs
            params = params_date | params_countries


            # Function retruning SQL WHERE condition/string, if filtering based on date applicable
            sql_date_query_where_part = get_sql_part_where_date(date_query_applicable)


            # Building of SQL queries
            sql_query_transport = get_sql_query_transport(date_query_applicable, sql_date_query_where_part)
            sql_query_service = get_sql_query_service(date_query_applicable, sql_date_query_where_part)
            sql_query_from_country = get_sql_query_from_country(date_query_applicable, sql_date_query_where_part)
            sql_query_to_country = get_sql_query_to_country(date_query_applicable, sql_date_query_where_part)
            sql_query_dtd_with_without = get_sql_query_dtd_with_without(date_query_applicable, sql_date_query_where_part)
            sql_query_currency = get_sql_query_currency(date_query_applicable, sql_date_query_where_part)
            sql_query_routes = get_sql_query_routes (date_query_applicable, sql_date_query_where_part)

            sql_query_from_to_country_at = get_sql_query_from_to_country(date_query_applicable, sql_date_query_where_part, "at")
            sql_query_from_to_country_cz = get_sql_query_from_to_country(date_query_applicable, sql_date_query_where_part, "cz")
            sql_query_from_to_country_de = get_sql_query_from_to_country(date_query_applicable, sql_date_query_where_part, "de")
            sql_query_from_to_country_pl = get_sql_query_from_to_country(date_query_applicable, sql_date_query_where_part, "pl")
            sql_query_from_to_country_sk = get_sql_query_from_to_country(date_query_applicable, sql_date_query_where_part, "sk")

            sql_query_top_city_from = get_sql_query_city(date_query_applicable, sql_date_query_where_part, "from_city","from_country")
            sql_query_top_city_to = get_sql_query_city(date_query_applicable, sql_date_query_where_part, "to_city","to_country")


            # Dataframes creation
            df_transport_grouped = pd.read_sql_query(sql=text(sql_query_transport), con = conn, params=params)
            df_service_grouped = pd.read_sql_query(sql=text(sql_query_service), con = conn, params=params)
            df_country_from_grouped = pd.read_sql_query(sql=text(sql_query_from_country), con = conn, params=params)
            df_country_to_grouped = pd.read_sql_query(sql=text(sql_query_to_country), con = conn, params=params)
            df_dtd_with_without = pd.read_sql_query(sql=text(sql_query_dtd_with_without), con = conn, params=params)
            df_currency_grouped = pd.read_sql_query(sql=text(sql_query_currency), con = conn, params=params)
            df_routes = pd.read_sql_query(sql=text(sql_query_routes), con = conn, params=params)

            df_at = pd.read_sql_query(sql=text(sql_query_from_to_country_at), con = conn, params=params)
            df_cz = pd.read_sql_query(sql=text(sql_query_from_to_country_cz), con = conn, params=params)
            df_de = pd.read_sql_query(sql=text(sql_query_from_to_country_de), con = conn, params=params)
            df_pl = pd.read_sql_query(sql=text(sql_query_from_to_country_pl), con = conn, params=params)
            df_sk = pd.read_sql_query(sql=text(sql_query_from_to_country_sk), con = conn, params=params)

            df_top_city_from = pd.read_sql_query(sql=text(sql_query_top_city_from), con = conn, params=params)
            df_top_city_to = pd.read_sql_query(sql=text(sql_query_top_city_to), con = conn, params=params)

            dtd_with = df_dtd_with_without["With DTD"].iloc[0]
            dtd_without = df_dtd_with_without["Without DTD"].iloc[0]

            # DF extract how many records -> for UI purposes
            number_rows_transport = df_transport_grouped["count"].sum()


            # DF adjustment 
            df_dtd_with_without_adj = {
                "Label" : ["With DTD","Without DTD"],
                "Count" : [dtd_with, dtd_without]
            }

            def df_change_column_name(input_df: pd.DataFrame) -> pd.DataFrame:
                
                dict_names = {
                    "from_country" : "From country",
                    "from_city" : "From city",
                    "to_country" : "To country",
                    "to_city" : "To city",
                    "count" : "Count",
                    "label" : "Label"
                }

                output_df = input_df.rename(columns=dict_names)

                return output_df

            df_transport_grouped_renamed = df_change_column_name(df_transport_grouped)
            df_service_grouped_renamed = df_change_column_name(df_service_grouped)
            df_currency_grouped_renamed = df_change_column_name(df_currency_grouped)
            df_country_from_grouped_renamed = df_change_column_name(df_country_from_grouped)
            df_country_to_grouped_renamed = df_change_column_name(df_country_to_grouped)
            df_top_city_from_renamed = df_change_column_name(df_top_city_from)
            df_top_city_to_columns_renamed = df_change_column_name(df_top_city_to)
            df_routes_columns_renamed = df_change_column_name(df_routes)

            def df_styling_index_set_1(input_df: pd.DataFrame) -> pd.DataFrame:

                input_df[" "] = input_df.index + 1
                input_df = input_df.set_index(" ")

                return input_df
            
            df_country_from_grouped_styled = df_styling_index_set_1(df_country_from_grouped_renamed)
            df_country_to_grouped_styled = df_styling_index_set_1(df_country_to_grouped_renamed)
            df_top_city_from_styled = df_styling_index_set_1(df_top_city_from_renamed)
            df_top_city_to_styled = df_styling_index_set_1(df_top_city_to_columns_renamed)
            df_routes_styled = df_styling_index_set_1(df_routes_columns_renamed)


            # Charts def
            def create_pie_chart(df_input, x_data, y_data):
                
                chart = px.pie(
                df_input, 
                names = df_input[f"{x_data}"],
                values = df_input[f"{y_data}"]
                )

                # Adjustment to see 2 decimals always in the chart
                chart.update_traces(texttemplate="%{percent:.2%}")

                return chart
                
            # # Charts
            chart_transport = create_pie_chart(df_transport_grouped, "label","count")
            chart_service = create_pie_chart(df_service_grouped, "label","count")
            chart_country_from = create_pie_chart(df_country_from_grouped, "from_country","count")
            chart_country_to = create_pie_chart(df_country_to_grouped, "to_country","count")
            chart_currency = create_pie_chart(df_currency_grouped, "label","count")
            chart_dtd = create_pie_chart(df_dtd_with_without_adj, "Label","Count") #This follows column names already assigned when DF created


            # UI fallback - for case when dataframes are empty (no data following search criteria)
            def data_empty_fallback_info(input_df: pd.DataFrame):

                if input_df.empty:
                    st.warning("No data in DB related to the select date range")

                else:
                    pass


            # UI visualization
            ''
            ''
            tab4_tab1, tab4_tab2, tab4_tab3, tab4_tab4, tab4_tab5, tab4_tab6 = st.tabs([
                "Transport type",
                "Service type",
                "With/without DTD",
                "Currency type",
                "Country From & To",
                "City From & To",
            ])

            col_layout_1 = [1.5,0.3,2]
            col_layout_2 = [1.5,0.3,1.5]

            with tab4_tab1:
                data_empty_fallback_info(df_transport_grouped)
                st.write(f"- Split based on selected **transport** type - total: **{number_rows_transport}**:")
                col_tab4_1, col_tab4_2, col_tab4_3 = st.columns(col_layout_1)
                col_tab4_1.dataframe(df_transport_grouped_renamed, hide_index=True)
                col_tab4_3.plotly_chart(chart_transport, key="chart_transport")
            
            with tab4_tab2:
                data_empty_fallback_info(df_service_grouped)
                st.write(f"- Split based on selected **delivery service** type - total: **{number_rows_transport}**:")
                col_tab4_1, col_tab4_2, col_tab4_3 = st.columns(col_layout_1)
                col_tab4_1.dataframe(df_service_grouped_renamed, hide_index=True)
                col_tab4_3.plotly_chart(chart_service, key="chart_service")
            
            with tab4_tab3:
                # For the fallback I use different DF than df_dtd_with_without_adj. Reason: It doesn't work on .empty principle like other DFs
                data_empty_fallback_info(df_transport_grouped) 
                st.write(f"- How many times **door-to-door** was ordered - total: **{number_rows_transport}**:")
                col_tab4_1, col_tab4_2, col_tab4_3 = st.columns(col_layout_1)
                col_tab4_1.dataframe(df_dtd_with_without_adj)
                col_tab4_3.plotly_chart(chart_dtd, key="chart_dtd")
            
            with tab4_tab4:
                data_empty_fallback_info(df_currency_grouped)
                st.write(f"- Split based on **currency** - total: **{number_rows_transport}**:")
                col_tab4_1, col_tab4_2, col_tab4_3 = st.columns(col_layout_1)
                col_tab4_1.dataframe(df_currency_grouped_renamed, hide_index=True)
                col_tab4_3.plotly_chart(chart_currency, key="chart_currency")
            
            with tab4_tab5:
                data_empty_fallback_info(df_country_from_grouped_styled)
                st.write(f"- Total number: **{number_rows_transport}**:")
                col_tab4_1, col_tab4_2, col_tab4_3 = st.columns(col_layout_2)
                col_tab4_1.write("- Most frequent **origin** country:")
                col_tab4_1.dataframe(df_country_from_grouped_styled)
                col_tab4_1.plotly_chart(chart_country_from, key="chart_country_from")
                
                col_tab4_3.write("- Most frequent **destination** country:")
                col_tab4_3.dataframe(df_country_to_grouped_styled)
                col_tab4_3.plotly_chart(chart_country_to, key="chart_country_to")

                # with st.expander("Ahojda"):
                #     col_tab4_1, col_tab4_2 = st.columns(2)
                #     col_tab4_1.dataframe(df_at)
                #     col_tab4_1.dataframe(df_cz)
                #     col_tab4_1.dataframe(df_de)
                #     col_tab4_1.dataframe(df_pl)
                #     col_tab4_1.dataframe(df_sk)

            with tab4_tab6:
                data_empty_fallback_info(df_top_city_from_styled)
                st.write(f"- Total number: **{number_rows_transport}**:")
                col_tab4_1, col_tab4_2, col_tab4_3 = st.columns(col_layout_2)
                col_tab4_1.write("- Most frequent **origin** city:")
                col_tab4_1.dataframe(df_top_city_from_styled)
                col_tab4_3.write("- Most frequent **destination** city:")
                col_tab4_3.dataframe(df_top_city_to_styled)

                st.write("- Top 20 routes:")
                
                #Fallback warning - if not enough routes 
                number_rows_route = df_routes.count().iloc[0]

                if 0 < number_rows_route < 20:
                    st.info(f"There has been only **{number_rows_route} routes** following the selected date criteria")

                st.dataframe(df_routes_styled)