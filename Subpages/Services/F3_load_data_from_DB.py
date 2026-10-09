import pandas as pd
import streamlit as st
import logging
from app_logging import inicialization_logging
from sqlalchemy import text, Engine
from Subpages.Dialog.F3_dialog import dialog_not_possible_to_pull_data
from Subpages.SQL.F3_SQL_queries import F3InputDataQueries, sql_query_parcel_size, query_additional_service_price_info, query_currency_max_values
from Subpages.Operational.F3_operational_functions import pull_data_and_transfer_to_list, get_transport_price_table


# ===== Inicialization for logging ===== 
inicialization_logging()


# ===== Data load from DB or from cache ===== 
@st.cache_data(ttl=3600, show_spinner=False)
def load_f3_data(_db_engine: Engine):

    '''
    - Created as separate service to have possibility of data caching when re-run
    - the 'db_engine' paramater has _ underscore  due to the cache component/decorator -> this argument will be ignored when chacing. This SQLAchemy component is not meant to be cached and streamlit has an issue with it
    - Rule: for caching there must be pure pandas DFs not sytled one (Styler is not accepted as part of caching)
    '''

    try:
        with _db_engine.connect() as conn:

            # Get options for the user form 
            category_options = pull_data_and_transfer_to_list(F3InputDataQueries.sql_query_category_options, conn)
            transport_company_options = pull_data_and_transfer_to_list(F3InputDataQueries.sql_query_transport_company_options, conn)
            currency_options = pull_data_and_transfer_to_list(F3InputDataQueries.sql_query_currency_options, conn)
            additional_service_options = pull_data_and_transfer_to_list(F3InputDataQueries.sql_query_additional_service_options, conn)
            country_options = pull_data_and_transfer_to_list(F3InputDataQueries.sql_query_country_options, conn)
            parcel_size_options = pull_data_and_transfer_to_list(F3InputDataQueries.sql_query_parcel_size_options, conn)

            # Get Price and Parcel size info tables 
            df_cz_dhl = get_transport_price_table(conn, "CZ", "DHL")
            df_cz_fedex = get_transport_price_table(conn, "CZ", "Fedex")
            df_sk_dhl = get_transport_price_table(conn, "SK", "DHL")
            df_sk_fedex = get_transport_price_table(conn, "SK", "Fedex")

            df_parcel_size = pd.read_sql_query(sql=text(sql_query_parcel_size), con=conn)

            # Get service df
            df_additional_service = pd.read_sql_query(sql=text(F3InputDataQueries.sql_query_additional_service_table), con=conn)
            df_additional_service_info = pd.read_sql_query(sql=text(query_additional_service_price_info), con=conn)

            # Get data for validation
            currency_max_values = (pd.read_sql_query(sql=text(query_currency_max_values), con=conn)).set_index("name")["max_value"].to_dict()

            logging.info(f"F3 - Pull data from DB - SUCCESS")

            return (
                category_options,
                transport_company_options,
                currency_options,
                additional_service_options,
                country_options,
                parcel_size_options,
                df_cz_dhl,
                df_cz_fedex,
                df_sk_dhl,
                df_sk_fedex,
                df_parcel_size,
                df_additional_service,
                df_additional_service_info,
                currency_max_values
            )

    except Exception as e:
        logging.warning(f"F3 - Pull data from DB - FAIL - Exception: {e}")
        dialog_not_possible_to_pull_data()
        st.stop()