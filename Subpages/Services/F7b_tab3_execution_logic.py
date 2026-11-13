import streamlit as st
import pandas as pd
from sqlalchemy import text, Engine
from Subpages.Data.F7_input_data import STATES_CONFIG, CONFIG_VALIDATE_CRITERIA_F7B_TAB3
from Subpages.Dialog.APP_universal_dialog import display_input_warning_toast
from Subpages.Resources_ui_objects import render_info_info
from Subpages.Operational.F7b_operational_functions import mapping_states_for_db, exclude_terminal_states, operational_update_of_states, mapping_states, get_styling_colors
from Subpages.SQL.F7b_SQL_queries import get_sql_query_offer_state_validation, get_sql_query_f7b_tab3, create_sql_string_price
from Subpages.Universal.Creation_of_parameters_for_SQL import create_parameters_for_sql
from Subpages.Universal.Universal_functions import singular_or_plural
from Subpages.Services.APP_validate_criteria import validate_criteria_not_in_final_result


def execute_f7b_tab3_logic(
    db_engine : Engine,
    selected_data: dict
    ):

    # ===== The selected data split into smaller objects cleaner code =====
    multiselect_obj = selected_data["multiselect"]

    date_from = selected_data["date"]["from"]
    date_to = selected_data["date"]["to"]

    # ===== Validation =====
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
    states_mapped = mapping_states_for_db(STATES_CONFIG, multiselect_obj["state"])
    

    # ----- Validation actuall data needed but scheduler has not run recently -----
    # Exclude states which are terminal 
    states_without_terminal = exclude_terminal_states(states_mapped, STATES_CONFIG)

    if len(states_without_terminal) > 0:

        params_states_without_terminal, str_for_sql_in_states_without_terminal = create_parameters_for_sql(states_without_terminal, "swt")

        params_sanity_check = {"limit": selected_data["number_rows"]} | params_states_without_terminal

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

     # Creation of parameter for SQL query 
    params_transport, str_for_sql_in_transport = create_parameters_for_sql(multiselect_obj["transport"], "t")
    params_currency, str_for_sql_in_currency = create_parameters_for_sql(multiselect_obj["currency"], "c")
    params_country_from, str_for_sql_in_country_from = create_parameters_for_sql(multiselect_obj["country_from"], "cf")
    params_country_to, str_for_sql_in_country_to = create_parameters_for_sql(multiselect_obj["country_to"], "ct")
    params_state, str_for_sql_in_state = create_parameters_for_sql(states_mapped, "st")  
    
    # Marging of the dictionaries to have 1 dictionary with all parameters
    params_full = params_transport | params_currency | params_country_from | params_country_to | params_state

    params_full["number_rows"] = selected_data["number_rows"]

    if selected_data["date"]["applicable"]:
        params_full["date_from"] = date_from
        params_full["date_to"] = date_to


    params_delivery_service, str_for_sql_in_delivery_service = (
        create_parameters_for_sql(multiselect_obj["delivery_service"], "ds")
        if selected_data["delivery_service"]["applicable"]
        else ({}, "")
    )

    params_dtd, str_for_sql_in_dtd = (
        create_parameters_for_sql(multiselect_obj["door_to_door"], "dtd")
        if selected_data["door_to_door"]["applicable"]
        else ({}, "")
    )

    sql_condition_price, params_price = (
        create_sql_string_price(selected_data["price"]["range"])
        if selected_data["price"]["applicable"]
        else (None, {})
    )

    params_full = params_full | params_price | params_delivery_service | params_dtd


    sql_query_tab_3 = get_sql_query_f7b_tab3(
        selected_data,
        str_for_sql_in_transport,
        str_for_sql_in_currency,
        str_for_sql_in_country_from,
        str_for_sql_in_country_to,
        str_for_sql_in_state,
        str_for_sql_in_delivery_service, 
        str_for_sql_in_dtd,
        sql_condition_price,
        )

    with db_engine.connect() as conn:
        df_table_tab_3 = pd.read_sql_query(sql=text(sql_query_tab_3), con=conn, params=params_full)

    if df_table_tab_3.empty:
        render_info_info("**No result** - There is no record found in DB.")

    else:
        # Mapping states DB naming -> UI naming
        df_table_tab_3 = mapping_states(df_table_tab_3, STATES_CONFIG)

        # DF Styling + state icons to get colors
        df_table_tab_3_styled = get_styling_colors(df_table_tab_3)

        # Info message to the user that there is not that many records as expected
        rows_from_db = len(df_table_tab_3)
               
        st.write("")
        if rows_from_db != selected_data["number_rows"]:

            s = singular_or_plural(rows_from_db)

            render_info_info(f"There is only **{rows_from_db} record{s}** matching the selected criteria.")

        # Validation which of the selected options are not part of the result -> info note to the user
        validate_criteria_not_in_final_result(df_table_tab_3, selected_data, CONFIG_VALIDATE_CRITERIA_F7B_TAB3)

        st.dataframe(df_table_tab_3_styled)