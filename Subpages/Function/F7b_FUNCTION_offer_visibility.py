import streamlit as st
from sqlalchemy import text
import pandas as pd
from datetime import date, timedelta
import logging
from app_logging import inicialization_logging
from app_db_connection import db_connection
from Subpages.Resources_config import FORMAT_CONFIG
from Subpages.Resources_ui import UiConfigAndIcons
from Subpages.Resources_ui_objects import render_warning_info, render_info_info
from Subpages.Services.F7_UI_image_generator import provide_ui_image_path, provide_ui_color_coding_image
from Subpages.SQL.F7b_SQL_queries import sql_query_table_overview, sql_offer_exists, sql_table_offer, sql_table_delivery, sql_table_costs, sql_table_extra_steps_time, sql_table_sla, sql_query_logs, sql_query_offer_rating, get_sql_query_transport, get_sql_query_service, get_sql_query_from_country, get_sql_query_to_country, get_sql_query_dtd_with_without, get_sql_query_currency, get_sql_query_from_to_country, get_sql_part_where_date, get_sql_query_city, get_sql_query_routes, get_sql_query_offer_state_validation
from Subpages.Data.F7_input_data import DATASET_CITIES, STATES_CONFIG, TRANSPORT_SPEED, CURRENCY_COUNTRY, STATES_UI_GROUPS
from Subpages.Operational.F7b_operational_functions import change_state_in_db, input_validation, operational_update_of_states, display_state_and_symbol_mapped, display_offer_logs, mapping_states, get_styling_colors, df_styling_index_set_1, data_empty_fallback_info, create_pie_chart, df_change_column_name, get_parameters_countries, get_list_states, get_min_date_offer
from Subpages.Services.F7b_UI_functions import display_state_flow, display_state_flow_expander, display_offer_visualization_ui
from Subpages.Services.F7b_tab3_UI_operations import initiate_session_state_f7b_tab3, display_filter_options_f7b_tab3, reset_filters_f7b_tab3
from Subpages.Services.F7b_tab3_execution_logic import execute_f7b_tab3_logic
from Subpages.Services.F7b_rating_function import make_rating_validation, display_offer_rating_ui_info, display_offer_rating_ui_tab
from Subpages.Universal.Universal_functions import singular_or_plural, extract_keys_from_dict_and_adjust


# Diagnostics
import uuid
import logging
from app_logging import inicialization_logging
inicialization_logging()
run_id = uuid.uuid4().hex[:8]
logging.warning(f"F7B SCRIPT START | {run_id}")



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
    "quick_select_state": list(STATES_UI_GROUPS.values()),
    "state": get_list_states(STATES_CONFIG),
    "slider_rows" : 20,
    "checkbox_date" : False,
    "min_date": get_min_date_offer(db_engine)
    }

    initiate_session_state_f7b_tab3(execution_data)

    selected_data: dict = display_filter_options_f7b_tab3(execution_data)

    ''
    submit_button_tab3 = st.button("Apply filters", width= "stretch", icon=UiConfigAndIcons.Buttons.apply_filters)

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
        icon=UiConfigAndIcons.Buttons.reset
        )

# ====================== TAB 4 ======================
with tab4: 

    # Default state condition
    submit_disabled = False
   
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
            format = FORMAT_CONFIG["date"]["streamlit_widget"],
            key = "key_date_input_tab4_1"
        )

        picked_date_to_tab4 = col2_tab4.date_input(
            "To",
            value = max_date,
            min_value = min_date,
            max_value = max_date,
            format = FORMAT_CONFIG["date"]["streamlit_widget"],
            key ="key_date_input_tab4_2"
            )
        
        # Extending SQL query date filter
        date_query_applicable = True


        # Fallback info 
        if picked_date_from_tab4 > picked_date_to_tab4:
            render_warning_info("**Date issue** - date **To** is farther in the past than **From**.")
            submit_disabled = True
  

    ''
    ''
    submit_button_tab4 = st.button("Submit", width= "stretch", icon=UiConfigAndIcons.Buttons.submit, key="key_submit_button_tab4", disabled=submit_disabled)

    if submit_button_tab4:

        # Build of parameters countries
        # Note 08-Nov-2026: It seems that I had some idea here but didn't finish it. These params are not used
        params_countries = get_parameters_countries(
                extract_keys_from_dict_and_adjust(
                DATASET_CITIES,
                operation="upper",
                sorting=True
                )
            )

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
        with db_engine.connect() as conn:
            df_transport_grouped = pd.read_sql_query(sql=text(sql_query_transport), con = conn, params=params)
            df_service_grouped = pd.read_sql_query(sql=text(sql_query_service), con = conn, params=params)
            df_country_from_grouped = pd.read_sql_query(sql=text(sql_query_from_country), con = conn, params=params)
            df_country_to_grouped = pd.read_sql_query(sql=text(sql_query_to_country), con = conn, params=params)
            df_dtd_with_without = pd.read_sql_query(sql=text(sql_query_dtd_with_without), con = conn, params=params)
            df_currency_grouped = pd.read_sql_query(sql=text(sql_query_currency), con = conn, params=params)
            df_routes = pd.read_sql_query(sql=text(sql_query_routes), con = conn, params=params)

            # Note 08-Nov-2026: It seems that I had some idea here but didn't finish it. These variables don't look to be used. 
            # df_at = pd.read_sql_query(sql=text(sql_query_from_to_country_at), con = conn, params=params)
            # df_cz = pd.read_sql_query(sql=text(sql_query_from_to_country_cz), con = conn, params=params)
            # df_de = pd.read_sql_query(sql=text(sql_query_from_to_country_de), con = conn, params=params)
            # df_pl = pd.read_sql_query(sql=text(sql_query_from_to_country_pl), con = conn, params=params)
            # df_sk = pd.read_sql_query(sql=text(sql_query_from_to_country_sk), con = conn, params=params)

            df_top_city_from = pd.read_sql_query(sql=text(sql_query_top_city_from), con = conn, params=params)
            df_top_city_to = pd.read_sql_query(sql=text(sql_query_top_city_to), con = conn, params=params)


        # DF extract how many records -> for UI purposes
        number_rows_transport = df_transport_grouped["count"].sum()


        # DF adjustment 
        dtd_with = df_dtd_with_without["With DTD"].iloc[0]
        dtd_without = df_dtd_with_without["Without DTD"].iloc[0]
        
        df_dtd_with_without_adj = {
            "Label" : ["With DTD","Without DTD"],
            "Count" : [dtd_with, dtd_without]
        }


        df_transport_grouped_renamed = df_change_column_name(df_transport_grouped)
        df_service_grouped_renamed = df_change_column_name(df_service_grouped)
        df_currency_grouped_renamed = df_change_column_name(df_currency_grouped)
        df_country_from_grouped_renamed = df_change_column_name(df_country_from_grouped)
        df_country_to_grouped_renamed = df_change_column_name(df_country_to_grouped)
        df_top_city_from_renamed = df_change_column_name(df_top_city_from)
        df_top_city_to_columns_renamed = df_change_column_name(df_top_city_to)
        df_routes_columns_renamed = df_change_column_name(df_routes)
        
        df_country_from_grouped_styled = df_styling_index_set_1(df_country_from_grouped_renamed)
        df_country_to_grouped_styled = df_styling_index_set_1(df_country_to_grouped_renamed)
        df_top_city_from_styled = df_styling_index_set_1(df_top_city_from_renamed)
        df_top_city_to_styled = df_styling_index_set_1(df_top_city_to_columns_renamed)
        df_routes_styled = df_styling_index_set_1(df_routes_columns_renamed)
            
        # Charts
        chart_transport = create_pie_chart(df_transport_grouped, "label","count")
        chart_service = create_pie_chart(df_service_grouped, "label","count")
        chart_country_from = create_pie_chart(df_country_from_grouped, "from_country","count")
        chart_country_to = create_pie_chart(df_country_to_grouped, "to_country","count")
        chart_currency = create_pie_chart(df_currency_grouped, "label","count")
        chart_dtd = create_pie_chart(df_dtd_with_without_adj, "Label","Count") #This follows column names already assigned when DF created


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
            fallback = data_empty_fallback_info(df_transport_grouped)

            if fallback == False:
                st.write(f"- Split based on selected **transport** type - total: **{number_rows_transport}**:")
                col_tab4_1, col_tab4_2, col_tab4_3 = st.columns(col_layout_1)
                col_tab4_1.dataframe(df_transport_grouped_renamed, hide_index=True)
                col_tab4_3.plotly_chart(chart_transport, key="chart_transport")
        
        with tab4_tab2:
            fallback = data_empty_fallback_info(df_service_grouped)

            if fallback == False:
                st.write(f"- Split based on selected **delivery service** type - total: **{number_rows_transport}**:")
                col_tab4_1, col_tab4_2, col_tab4_3 = st.columns(col_layout_1)
                col_tab4_1.dataframe(df_service_grouped_renamed, hide_index=True)
                col_tab4_3.plotly_chart(chart_service, key="chart_service")
        
        with tab4_tab3:
            # For the fallback I use different DF than df_dtd_with_without_adj. Reason: It doesn't work on .empty principle like other DFs
            fallback = data_empty_fallback_info(df_transport_grouped) 

            if fallback == False:
                st.write(f"- How many times **door-to-door** was ordered - total: **{number_rows_transport}**:")
                col_tab4_1, col_tab4_2, col_tab4_3 = st.columns(col_layout_1)
                col_tab4_1.dataframe(df_dtd_with_without_adj)
                col_tab4_3.plotly_chart(chart_dtd, key="chart_dtd")
        
        with tab4_tab4:
            fallback = data_empty_fallback_info(df_currency_grouped)

            if fallback == False:
                st.write(f"- Split based on **currency** - total: **{number_rows_transport}**:")
                col_tab4_1, col_tab4_2, col_tab4_3 = st.columns(col_layout_1)
                col_tab4_1.dataframe(df_currency_grouped_renamed, hide_index=True)
                col_tab4_3.plotly_chart(chart_currency, key="chart_currency")
        
        with tab4_tab5:
            fallback = data_empty_fallback_info(df_country_from_grouped_styled)

            if fallback == False:
                st.write(f"- Total number: **{number_rows_transport}**:")
                col_tab4_1, col_tab4_2, col_tab4_3 = st.columns(col_layout_2)
                col_tab4_1.write("- Most frequent **origin** country:")
                col_tab4_1.dataframe(df_country_from_grouped_styled)
                col_tab4_1.plotly_chart(chart_country_from, key="chart_country_from")
                
                col_tab4_3.write("- Most frequent **destination** country:")
                col_tab4_3.dataframe(df_country_to_grouped_styled)
                col_tab4_3.plotly_chart(chart_country_to, key="chart_country_to")

        with tab4_tab6:
            fallback = data_empty_fallback_info(df_top_city_from_styled)

            if fallback == False:
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

                    s = singular_or_plural(number_rows_route)

                    render_info_info(f"There is only **{number_rows_route} route{s}** matching the selected criteria.")

                st.dataframe(df_routes_styled)