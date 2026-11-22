import streamlit as st
from sqlalchemy import text
import pandas as pd
import logging
from app_logging import inicialization_logging
from app_db_connection import db_connection
from Subpages.Resources_ui import UiConfigAndIcons
from Subpages.Resources_ui_objects import render_info_info
from Subpages.Services.F7_UI_image_generator import provide_ui_image_path, provide_ui_color_coding_image
from Subpages.SQL.F7b_SQL_queries import sql_query_table_overview, sql_offer_exists, sql_table_offer, sql_table_delivery, sql_table_costs, sql_table_extra_steps_time, sql_table_sla, sql_query_logs, sql_query_offer_rating, get_sql_query_offer_state_validation
from Subpages.Data.F7_input_data import DATASET_CITIES, STATES_CONFIG, TRANSPORT_SPEED, CURRENCY_COUNTRY, STATES_UI_GROUPS, DELIVERY_SERVICE
from Subpages.Operational.F7b_operational_functions import change_state_in_db, input_validation, operational_update_of_states, display_state_and_symbol_mapped, display_offer_logs, mapping_states, get_styling_colors, get_list_states, get_min_date_offer, get_currency_db_values
from Subpages.Services.F7b_UI_functions import display_state_flow, display_state_flow_expander, display_offer_visualization_ui
from Subpages.Services.F7b_tab3_UI_operations import initiate_session_state_f7b_tab3, display_filter_options_f7b_tab3, reset_filters_f7b_tab3
from Subpages.Services.F7b_tab3_execution_logic import execute_f7b_tab3_logic
from Subpages.Services.F7b_rating_function import make_rating_validation, display_offer_rating_ui_info, display_offer_rating_ui_tab
from Subpages.Services.F7b_tab4_UI_operations import initiate_session_state_f7b_tab4, display_filter_options_f7b_tab4, reset_filters_f7b_tab4
from Subpages.Services.F7b_tab4_execution_logic import execute_f7b_tab4_logic
from Subpages.Universal.Universal_functions import extract_keys_from_dict_and_adjust


# Inicialization of logging
inicialization_logging()


# ================ Application Screen ========================
st.write("# Find your offer:")
''

st.write("- View into DB. Based on offers created in Function 7...")
''

tab1, tab2, tab3, tab4 = st.tabs([
    "Last 30 offers",
    "Search for specific offer",
    "Customized search",
    "Analytics"
])

# Connection can be used across tabs
db_engine = db_connection("F7B", True)

# ===== Variable used in multiple tabs =====
min_date = get_min_date_offer(db_engine)

quick_select_state = list(STATES_UI_GROUPS.values())
states: list =  get_list_states(STATES_CONFIG)

# ====================== TAB 1 ======================
with tab1:

    ''
    if st.button("Show last 30 offers", width="stretch", icon=UiConfigAndIcons.Expanders.table):

        # Pulling of data from DB - status check
        df_state_check = pd.read_sql(
            sql=text(
                get_sql_query_offer_state_validation(
                    limit=True,
                )
            ),
            con=db_engine,
            params={
                "limit": 30
            }
        )

        operational_update_of_states(df_state_check, db_engine)

        
        # Query into DB + DF column adjustment
        df = pd.read_sql(sql_query_table_overview,db_engine)

        df = mapping_states(df, STATES_CONFIG)


        # UI + Styled DF visualization
        ''
        display_state_flow_expander()
        ''
        st.dataframe(
            get_styling_colors(df),
            column_config={
                "Icon": st.column_config.TextColumn(
                width="small"
                )    
            },
            width = "stretch",
            height=562
        )


# ====================== TAB 2 ======================
with tab2:

    with st.form(key="user_form"):
        offer_input_user = st.text_input(label="Offer number:", help="Insert **Offer number** you would like to see. It is based on offers created in **Function 7**.")
        
        submit_button = st.form_submit_button(label= "Submit", width="stretch", icon=UiConfigAndIcons.Buttons.submit,)


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
                    render_info_info(f"**No result** - offer **{offer_input_validated}** does not exist.")

                else:
                    offer_id = offer_id_exists["offer_id"].iloc[0]

                    # Validation (and change) of state to have it actual
                    df_validation = pd.read_sql_query(
                        sql=text(
                            get_sql_query_offer_state_validation(
                                offer=True, 
                            )
                        ),
                        con=conn,
                        params=params
                    )

                    operational_update_of_states(df_validation, db_engine)

                    # --- a.OFFER --- 
                    df_table_offer = pd.read_sql_query(sql=text(sql_table_offer), con=conn, params=params)

                    # Extracting data from DF -> variables
                    row_offer = df_table_offer.iloc[0]


                    # --- b.DELIVERY --- 
                    df_table_delivery = pd.read_sql_query(sql=text(sql_table_delivery), con=conn, params=params)

                    # Extracting data from DF -> variables
                    row_delivery = df_table_delivery.iloc[0]


                    # --- c.COSTS --- 
                    df_table_costs = pd.read_sql_query(sql=text(sql_table_costs), con=conn, params=params)

                    # Extracting data from DF -> variables
                    row_costs = df_table_costs.iloc[0]


                    # --- e.EXTRA_STEPS_TIME --- 
                    df_table_extra_steps_time = pd.read_sql_query(sql=text(sql_table_extra_steps_time), con=conn, params=params)  

                    # Extracting data from DF -> variables   
                    row_extra_steps_time = df_table_extra_steps_time.iloc[0]
                        

                    # --- h.SLA --- 
                    df_table_sla = pd.read_sql_query(sql=text(sql_table_sla), con=conn, params=params)  

                    # Extracting data from DF -> variables  
                    row_sla = df_table_sla.iloc[0]

                    # --- n.OFFER_RATING ---
                    df_table_offer_rating = pd.read_sql_query(sql=text(sql_query_offer_rating), con=conn, params=params)

                    # Rating functionality - validation
                    rating_end = make_rating_validation(df_table_offer_rating)
                    logging.info(f"F7B - Rating function - SUCCESS - {rating_end}")

                
                    # Get UI image for the particular offer          
                    ui_image_path = provide_ui_image_path(row_offer["transport"], row_delivery["from_dtd"], row_delivery["to_dtd"], row_extra_steps_time["truck_breaks"])

                    ui_color_coding_image_path = provide_ui_color_coding_image(row_offer["transport"], row_delivery["from_dtd"], row_delivery["to_dtd"], row_extra_steps_time["truck_breaks"])


                    # ========== TAB 2 UI ========================================
                    ''
                    ''
                    tab2_tab1, tab2_tab2, tab2_tab3, tab2_tab4 = st.tabs([
                        f"Offer {offer_id}",
                        "State change & logs",
                        "State flow",
                        "Rating ★"
                    ])

                    with tab2_tab1:

                        display_state_and_symbol_mapped(row_offer["offer_state"], STATES_CONFIG)

                        display_offer_rating_ui_info(rating_end, df_table_offer_rating)

                        ''
                        display_offer_visualization_ui(
                            "F7B",
                            ui_image_path,
                            ui_color_coding_image_path,
                            offer_id,
                            row_offer,
                            row_delivery,
                            row_costs,
                            row_extra_steps_time,
                            row_sla
                        )


                    with tab2_tab2:
                        display_state_and_symbol_mapped(row_offer["offer_state"], STATES_CONFIG)

                        if row_offer["offer_state"] == "CREATED":

                            ''
                            if st.button("Approve", 
                                on_click=change_state_in_db,
                                args=(db_engine, offer_id, row_offer["offer_state"], "APPROVED"),
                                width="stretch",
                                icon = UiConfigAndIcons.UnifiedIcons.approve
                                ):
                                    pass
                                

                            if st.button("Reject",
                                on_click = change_state_in_db,
                                args=(db_engine, offer_id, row_offer["offer_state"], "REJECTED"),
                                width="stretch",
                                icon = UiConfigAndIcons.UnifiedIcons.reject
                                ):
                                    pass

                            ''
                            ''

                        # Logs table   
                        display_offer_logs(db_engine, sql_query_logs, offer_id, STATES_CONFIG)

                    # State flow
                    with tab2_tab3:
                        display_state_flow()

                    # Rating function
                    with tab2_tab4:
                        display_offer_rating_ui_tab(offer_id, rating_end, df_table_offer_rating)


# ====================== TAB 3 ======================
with tab3: 

    delivery_service = sorted(
        item["name"].capitalize()
        for item in DELIVERY_SERVICE.values()
    )

    currency = extract_keys_from_dict_and_adjust(
        CURRENCY_COUNTRY,
        sorting=True
        )

    execution_data = {
        "country": extract_keys_from_dict_and_adjust(
            DATASET_CITIES,
            operation="upper",
            sorting=True
            ),

        "transport": extract_keys_from_dict_and_adjust(
            TRANSPORT_SPEED,
            operation="capitalize",
            sorting=True
            ),
        "currency": extract_keys_from_dict_and_adjust(
            CURRENCY_COUNTRY,
            sorting=True
            ),
        "currency_values": get_currency_db_values(db_engine, currency),
        "quick_select_state": quick_select_state,
        "state": states,
        "door_to_door": ["No DtD", "DtD From","DtD To", "DtD From & To"],
        "slider_rows" : 20,
        "min_date": min_date,
        "delivery_service": delivery_service,
        "toggle" : {
            "date" : False,
            "price" : False,
            "delivery_service" : False,
            "dtd" : False,
        }
    }

    initiate_session_state_f7b_tab3(execution_data)

    selected_data: dict = display_filter_options_f7b_tab3(execution_data)

    ''
    submit_button_tab3 = st.button("Apply filters", width= "stretch", icon=UiConfigAndIcons.Buttons.apply_filters, key="submit_button_f7b_tab3")

    if submit_button_tab3:

        execute_f7b_tab3_logic(
            db_engine,
            selected_data
        )
        
    # ===== Reset button =====
    st.write("-" *10)
    st.button(
        "Reset filters",
        on_click=reset_filters_f7b_tab3,
        args=(execution_data,),
        width="stretch",
        icon=UiConfigAndIcons.Buttons.reset,
        key="reset_button_f7b_tab3"
        )

# ====================== TAB 4 ======================
with tab4: 

    execution_data = {
    "min_date": min_date,
    "quick_select_state": quick_select_state,
    "state": states,
    }


    initiate_session_state_f7b_tab4(execution_data)

    selected_data = display_filter_options_f7b_tab4(execution_data)

    ''
    ''
    submit_button_tab4 = st.button("Apply filters", width= "stretch", icon=UiConfigAndIcons.Buttons.apply_filters, key="submit_button_f7b_tab4")

    if submit_button_tab4:

        execute_f7b_tab4_logic(
            db_engine,
            selected_data
        )

    # ===== Reset button =====
    st.write("-" *10)
    st.button(
        "Reset filters",
        on_click=reset_filters_f7b_tab4,
        args=(execution_data,),
        width="stretch",
        icon=UiConfigAndIcons.Buttons.reset,
        key="reset_button_f7b_tab4"
        )
