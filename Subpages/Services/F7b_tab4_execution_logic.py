import streamlit as st
import pandas as pd
from sqlalchemy import Engine, text
from Subpages.Resources_ui_objects import render_info_info
from Subpages.Dialog.APP_universal_dialog import display_input_warning_toast
from Subpages.Operational.F7b_operational_functions import mapping_states_for_db, mapping_state_db_to_ui,exclude_terminal_states, operational_update_of_states, df_change_column_name, data_empty_fallback_info, sum_values_in_df
from Subpages.Data.F7_input_data import STATES_CONFIG, CONFIG_VALIDATE_CRITERIA_F7B_TAB4
from Subpages.SQL.F7b_SQL_queries import get_sql_query_offer_state_validation, get_sql_part_where_date, get_sql_query_state,get_sql_query_transport, get_sql_query_service, get_sql_query_from_country, get_sql_query_to_country, get_sql_query_dtd_with_without, get_sql_query_currency, get_sql_query_city, get_sql_query_routes
from Subpages.Services.APP_validate_criteria import validate_criteria_not_in_final_result
from Subpages.Universal.Creation_of_parameters_for_SQL import create_parameters_for_sql
from Subpages.Universal.Universal_functions import adjust_index_in_df, singular_or_plural
from Subpages.Universal.Charts import create_pie_chart


def execute_f7b_tab4_logic(
    db_engine : Engine,
    selected_data: dict
    ):

    # ===== The selected data split into smaller objects cleaner code =====
    date_from = selected_data["date"]["from"]
    date_to = selected_data["date"]["to"]


    if any(value is None or value == [] for value in selected_data["multiselect"].values()):
        display_input_warning_toast()
        return

    if (
        date_from is not None
        and date_to is not None
        and date_from > date_to
        ):  
        display_input_warning_toast()
        return


    # Data mapping from UI to DB format
    states_mapped = mapping_states_for_db(STATES_CONFIG, selected_data["multiselect"]["state"])


    # ----- Validation actuall data needed but scheduler has not run recently -----
    # Exclude states which are terminal 
    states_without_terminal = exclude_terminal_states(states_mapped, STATES_CONFIG)

    if len(states_without_terminal) > 0:

        params_states_without_terminal, str_for_sql_in_states_without_terminal = create_parameters_for_sql(states_without_terminal, "swt")

        params_sanity_check = {"limit": 100} | params_states_without_terminal

        # Pulling of data from DB - status check
        df_sanity_check = pd.read_sql(
            sql=text(
                get_sql_query_offer_state_validation(
                    limit=True,
                    offer=False,
                    states=str_for_sql_in_states_without_terminal
                    ),
                ),
            con=db_engine,
            params=params_sanity_check
        )

        operational_update_of_states(df_sanity_check, db_engine)
    # -------------------------------------------------------------------------

    # Build of parameters
    params_state, str_for_sql_in_state = create_parameters_for_sql(states_mapped, "st")

    params_full = params_state
     
    if selected_data["date"]["applicable"]:
        params_full["date_from"] = date_from
        params_full["date_to"] = date_to  
    

    # Function returning SQL string, if applicable
    sql_date_condition: str = get_sql_part_where_date(selected_data["date"]["applicable"])


    # Building of SQL queries
    sql_query_transport = get_sql_query_transport(str_for_sql_in_state, sql_date_condition)
    sql_query_service = get_sql_query_service(str_for_sql_in_state, sql_date_condition)
    sql_query_from_country = get_sql_query_from_country(str_for_sql_in_state, sql_date_condition)
    sql_query_to_country = get_sql_query_to_country(str_for_sql_in_state, sql_date_condition)
    sql_query_dtd_with_without = get_sql_query_dtd_with_without(str_for_sql_in_state, sql_date_condition)
    sql_query_currency = get_sql_query_currency(str_for_sql_in_state, sql_date_condition)
    sql_query_routes = get_sql_query_routes (str_for_sql_in_state, sql_date_condition)

    sql_query_top_city_from = get_sql_query_city(str_for_sql_in_state, sql_date_condition, "from_city","from_country")
    sql_query_top_city_to = get_sql_query_city(str_for_sql_in_state, sql_date_condition, "to_city","to_country")

    sql_query_distinct_state = get_sql_query_state(str_for_sql_in_state, sql_date_condition)

    # DFs creation
    with db_engine.connect() as conn:
        df_transport_grouped = pd.read_sql_query(sql=text(sql_query_transport), con = conn, params=params_full)
        df_service_grouped = pd.read_sql_query(sql=text(sql_query_service), con = conn, params=params_full)
        df_country_from_grouped = pd.read_sql_query(sql=text(sql_query_from_country), con = conn, params=params_full)
        df_country_to_grouped = pd.read_sql_query(sql=text(sql_query_to_country), con = conn, params=params_full)
        df_dtd_with_without = pd.read_sql_query(sql=text(sql_query_dtd_with_without), con = conn, params=params_full)
        df_currency_grouped = pd.read_sql_query(sql=text(sql_query_currency), con = conn, params=params_full)
        df_routes = pd.read_sql_query(sql=text(sql_query_routes), con = conn, params=params_full)

        df_top_city_from = pd.read_sql_query(sql=text(sql_query_top_city_from), con = conn, params=params_full)
        df_top_city_to = pd.read_sql_query(sql=text(sql_query_top_city_to), con = conn, params=params_full)

        df_distinct_states = pd.read_sql_query(sql=text(sql_query_distinct_state), con = conn, params=params_full)
        

    # DF adjustment 
    df_transport_grouped_renamed = df_change_column_name(df_transport_grouped)
    df_service_grouped_renamed = df_change_column_name(df_service_grouped)
    df_currency_grouped_renamed = df_change_column_name(df_currency_grouped)
    df_country_from_grouped_renamed = df_change_column_name(df_country_from_grouped)
    df_country_to_grouped_renamed = df_change_column_name(df_country_to_grouped)
    df_top_city_from_renamed = df_change_column_name(df_top_city_from)
    df_top_city_to_columns_renamed = df_change_column_name(df_top_city_to)
    df_routes_columns_renamed = df_change_column_name(df_routes)
    
    df_country_from_grouped_styled = adjust_index_in_df(df_country_from_grouped_renamed)
    df_country_to_grouped_styled = adjust_index_in_df(df_country_to_grouped_renamed)
    df_top_city_from_styled = adjust_index_in_df(df_top_city_from_renamed)
    df_top_city_to_styled = adjust_index_in_df(df_top_city_to_columns_renamed)
    df_routes_styled = adjust_index_in_df(df_routes_columns_renamed)
        
    # Charts
    chart_transport = create_pie_chart(df_transport_grouped, "label","count")
    chart_service = create_pie_chart(df_service_grouped, "label","count")
    chart_country_from = create_pie_chart(df_country_from_grouped, "from_country","count")
    chart_country_to = create_pie_chart(df_country_to_grouped, "to_country","count")
    chart_currency = create_pie_chart(df_currency_grouped, "label","count")
    chart_dtd = create_pie_chart(df_dtd_with_without, "Label","Count") #This follows column names already assigned when DF created

    # Validation which of the selected options are not part of the result -> info note to the user
    if not df_distinct_states.empty:
        st.write("")
        
        df_states_mapped = mapping_state_db_to_ui(df_distinct_states, STATES_CONFIG)
        validate_criteria_not_in_final_result(df_states_mapped, selected_data, CONFIG_VALIDATE_CRITERIA_F7B_TAB4)


    # UI visualization
    st.write("")
    st.write("")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Transport type",
        "Service type",
        "With/without DTD",
        "Currency type",
        "Country From & To",
        "City From & To",
    ])

    layout_1 = [1.5,0.3,2]
    layout_2 = [1.5,0.3,1.5]

    with tab1:
        fallback = data_empty_fallback_info(df_transport_grouped)

        if not fallback:

            count_rows = sum_values_in_df(df_transport_grouped_renamed)

            st.write(f"- Split based on selected **transport** type - sum: **{count_rows}**:")
            col1, col2, col3 = st.columns(layout_1)
            col1.dataframe(df_transport_grouped_renamed, hide_index=True)
            col3.plotly_chart(chart_transport, key="chart_transport")
    
    with tab2:
        fallback = data_empty_fallback_info(df_service_grouped)

        if not fallback:

            count_rows = sum_values_in_df(df_service_grouped_renamed)

            st.write(f"- Split based on selected **delivery service** type - sum: **{count_rows}**:")
            col1, col2, col3 = st.columns(layout_1)
            col1.dataframe(df_service_grouped_renamed, hide_index=True)
            col3.plotly_chart(chart_service, key="chart_service")
    
    with tab3:
        fallback = data_empty_fallback_info(df_dtd_with_without) 

        if not fallback:

            count_rows = sum_values_in_df(df_dtd_with_without)

            st.write(f"- How many times **door-to-door** was ordered - sum: **{count_rows}**:")
            col1, col2, col3 = st.columns(layout_1)
            col1.dataframe(df_dtd_with_without, hide_index=True)
            col3.plotly_chart(chart_dtd, key="chart_dtd")
    
    with tab4:
        fallback = data_empty_fallback_info(df_currency_grouped)

        if not fallback:

            count_rows = sum_values_in_df(df_currency_grouped_renamed)

            st.write(f"- Split based on **currency** - sum: **{count_rows}**:")
            col1, col2, col3 = st.columns(layout_1)
            col1.dataframe(df_currency_grouped_renamed, hide_index=True)
            col3.plotly_chart(chart_currency, key="chart_currency")
    
    with tab5:
        fallback = data_empty_fallback_info(df_country_from_grouped_styled)

        if not fallback:

            count_rows_origin = sum_values_in_df(df_country_from_grouped_styled)
            count_rows_destination = sum_values_in_df(df_country_to_grouped_styled)

            col1, col2, col3 = st.columns(layout_2)
            col1.write(f"- Most frequent **origin** country - sum: **{count_rows_origin}**:")
            col1.dataframe(df_country_from_grouped_styled)
            col1.plotly_chart(chart_country_from, key="chart_country_from")
            
            col3.write(f"- Most frequent **destination** country - sum: **{count_rows_destination}**:")
            col3.dataframe(df_country_to_grouped_styled)
            col3.plotly_chart(chart_country_to, key="chart_country_to")

    with tab6:
        fallback = data_empty_fallback_info(df_top_city_from_styled)

        if not fallback:

            count_rows_city_to = sum_values_in_df(df_top_city_from_styled)
            count_rows_city_from = sum_values_in_df(df_top_city_to_styled)
            
            col1, col2, col3 = st.columns(layout_2)
            col1.write(f"- Most frequent **origin** city - sum: **{count_rows_city_to}**:")
            col1.dataframe(df_top_city_from_styled)
            col3.write(f"- Most frequent **destination** city - sum: **{count_rows_city_from}**:")
            col3.dataframe(df_top_city_to_styled)


            count_rows = sum_values_in_df(df_routes_styled)

            st.write(f"- Top 20 routes - sum: **{count_rows}**:")
            
            #Fallback warning - if not enough routes 
            number_rows_route = df_routes.count().iloc[0]

            if 0 < number_rows_route < 20:

                s = singular_or_plural(number_rows_route)

                render_info_info(f"There is only **{number_rows_route} route{s}** matching the selected criteria.")

            st.dataframe(df_routes_styled)