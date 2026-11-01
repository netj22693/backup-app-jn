import streamlit as st
import pandas as pd
from sqlalchemy import text, Engine
from Subpages.Resources_ui_objects import render_info_info
from Subpages.Dialog.F3b_dialog import display_input_warning_toast
from Subpages.Universal.Creation_of_parameters_for_SQL import create_parameters_for_sql
from Subpages.SQL.F3b_SQL_queries import get_sql_query_f3b_tab_3
from Subpages.Universal.Universal_functions import adjust_index_in_df, singular_or_plural

def execute_f3b_tab3_logic(
    db_engine : Engine,
    selected_data: dict
    ):

    # ===== The selected data split into smaller objects cleaner code =====
    multiselect_obj = selected_data["multiselect"]

    customer = selected_data["text"]["customer"]
    product = selected_data["text"]["product"]

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

    # Creation of parameter for SQL query
    params_category, str_for_sql_in_category = create_parameters_for_sql(multiselect_obj["category"], "cat")
    params_currency, str_for_sql_in_currency = create_parameters_for_sql(multiselect_obj["currency"], "cur")
    params_additional_service, str_for_sql_in_additional_service = create_parameters_for_sql(multiselect_obj["additional_service"], "as")
    params_country, str_for_sql_in_country = create_parameters_for_sql(multiselect_obj["country"], "c")
    params_transport_company, str_for_sql_in_transport_company = create_parameters_for_sql(multiselect_obj["transport_company"], "tc")
    params_parcel_size, str_for_sql_in_transport_parcel_size = create_parameters_for_sql(multiselect_obj["parcel_size"], "ps")
    params_file_format, str_for_sql_in_transport_file_format = create_parameters_for_sql(multiselect_obj["file_format"], "ff")

    # Marging of the dictionaries to have 1 dictionary with all parameters
    params_full = params_category | params_currency | params_additional_service | params_country | params_transport_company | params_parcel_size | params_file_format

    # If condition to make sure that variables exist
    # len() > 0 not an empty string
    # _applicable - boolean logic for SQL builder function
    # f"%{variable}%" - preperation of wild cards for SQL parameter


    if selected_data["text"]["checkbox"] == True:
        if len(customer) > 0:
            params_full["customer"] = f"%{customer}%"
            selected_data["text"]["customer_applicable"] = True

        if len(product) > 0:
            params_full["product"] = f"%{product}%"
            selected_data["text"]["product_applicable"] = True


    if selected_data["date"]["checkbox"] == True:
        params_full["date_from"] = date_from
        params_full["date_to"] = date_to

    # Limit/number of rows
    params_full["number_rows"] = selected_data["number_rows"]


    sql_query_tab_3 = get_sql_query_f3b_tab_3(
        str_for_sql_in_category,
        str_for_sql_in_currency,
        str_for_sql_in_additional_service,
        str_for_sql_in_country,
        str_for_sql_in_transport_company,
        str_for_sql_in_transport_parcel_size,
        str_for_sql_in_transport_file_format,
        selected_data["date"]["checkbox"],
        selected_data["text"]["customer_applicable"],
        selected_data["text"]["product_applicable"]
        )

    with db_engine.connect() as conn:
        df_table_tab_3 = pd.read_sql_query(sql=text(sql_query_tab_3), con=conn, params=params_full)

    if df_table_tab_3.empty == True:
        render_info_info("**No result** - There is no record found in DB.")

    else: 
        # Dataframe styling 
        df_table_tab_3 = adjust_index_in_df(df_table_tab_3)

        df_table_tab_3_styled = df_table_tab_3.style.format({
        "Product price": "{:,.2f}",
        "Extra service price": "{:,.2f}",
        "Transport price": "{:,.2f}",
        "Total sum": "{:,.2f}",
        })

        # Info message to the user that there is not that many records as expected
        rows_from_db = df_table_tab_3.index
        rows_from_db = rows_from_db[-1]
        
        st.write("")
        if rows_from_db != selected_data["number_rows"]:

            s = singular_or_plural(rows_from_db)

            render_info_info(f"There is only **{rows_from_db} record{s}** matching the selected criteria.")

        st.dataframe(df_table_tab_3_styled)