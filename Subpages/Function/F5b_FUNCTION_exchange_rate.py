import streamlit as st
import pandas as pd
from app_db_connection import db_connection
from sqlalchemy import text
from Subpages.SQL.F5b_SQL_queries import sql_query_exchange_rate_data
from Subpages.Services.F5b_charts import create_chart
from Subpages.Operational.F5b_operational_functions import get_date_range, df_split_data_clean_up, df_clean_up_for_ui, extract_variables_from_df

# =================== App UI  ===================
st.write("# Exchange Rate - Trend:")
''
''
options = ["Last 30 days","Current month"]
radio_selected = st.radio("Range", options=options, label_visibility="collapsed")
''
''
tab1, tab2, tab3 = st.tabs([
    "EUR to CZK",
    "USD to CZK",
    "EUR to USD"
])

# Determin date rage for DB query -> parameters
dict_range_date = get_date_range(radio_selected)
start = dict_range_date["start"]
end = dict_range_date["end"]

# Engine creation
db_engine = db_connection(function_id="F5B")

# Creation DF from DB
with db_engine.connect() as conn:
    df_table_full = pd.read_sql_query(sql=text(sql_query_exchange_rate_data), con=conn, params = {
    "start": start,
    "end": end
    })


# Fallback - case: 1st day in month -> user selects 'Current month' (radio button) but no record in DB yet because scheduler has not run yet. 
if df_table_full.empty:
    st.info("""
    - For current month there is **no record in DB yet**
    - The automated scheduler has not run yet today
    - **Should be visible within next few hours**
    """) 

else:
    df_eur_to_czk = df_split_data_clean_up(df_table_full, "eur_to_czk")
    df_usd_to_czk = df_split_data_clean_up(df_table_full, "usd_to_czk")
    df_eur_to_usd = df_split_data_clean_up(df_table_full, "eur_to_usd")

    df_eur_to_czk_ui = df_clean_up_for_ui(df_eur_to_czk, "eur_to_czk", "EUR to CZK")
    df_usd_to_czk_ui = df_clean_up_for_ui(df_usd_to_czk, "usd_to_czk", "USD to CZK")
    df_eur_to_usd_ui = df_clean_up_for_ui(df_eur_to_usd, "eur_to_usd", "EUR to USD")


    # =================== App UI - content -> result ===================
    
    with tab1:
        if df_eur_to_czk.empty:
            st.info("There is no data for EUR to CZK yet")

        else:
            #------ metrics & chart ------
            value_eur_to_czk_last, delta_eur_to_czk, avg_eur_to_czk, min_eur_to_czk, min_date_eur_to_czk, max_eur_to_czk, max_date_eur_to_czk, last_date_str_eur_to_czk, delta_color_eur_to_czk, delta_arrow_eur_to_czk = extract_variables_from_df(df_eur_to_czk)    

            chart_eur_to_czk = create_chart(df_eur_to_czk, "created_at", "eur_to_czk", "#3206F5", "EUR to CZK", "CZK")

            # ------ UI ------
            ''
            st.metric(
                f"Last record ({last_date_str_eur_to_czk})",
                value=f"{value_eur_to_czk_last:.3f}",
                delta=f"{delta_eur_to_czk:.3f}",
                delta_color=delta_color_eur_to_czk,
                delta_arrow=delta_arrow_eur_to_czk
                )
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Average", value=f"{avg_eur_to_czk:.3f}")
            col2.metric(f"Max (on {max_date_eur_to_czk})", value=f"{max_eur_to_czk:.3f}")
            col3.metric(f"Min (on {min_date_eur_to_czk})", value=f"{min_eur_to_czk:.3f}")
            ''
            ''
            st.plotly_chart(chart_eur_to_czk, width="stretch")

            ''
            with st.expander("List of records", icon=":material/table:"):
                st.dataframe(df_eur_to_czk_ui)

    with tab2:
        if df_usd_to_czk.empty:
            st.info("There is no data for USD to CZK yet")

        else:
            #------ metrics & chart ------
            value_usd_to_czk_last, delta_usd_to_czk, avg_usd_to_czk, min_usd_to_czk, min_date_usd_to_czk,max_usd_to_czk, max_date_usd_to_czk, last_date_str_usd_to_czk, delta_color_usd_to_czk, delta_arrow_usd_to_czk = extract_variables_from_df(df_usd_to_czk)

            chart_usd_to_czk = create_chart(df_usd_to_czk, "created_at", "usd_to_czk", "#111111", "USD to CZK", "CZK")

            # ------ UI ------
            ''
            st.metric(
                f"Last record ({last_date_str_usd_to_czk})",
                value=f"{value_usd_to_czk_last:.3f}",
                delta=f"{delta_usd_to_czk:.3f}",
                delta_color=delta_color_usd_to_czk,
                delta_arrow=delta_arrow_usd_to_czk
                )
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Average", value=f"{avg_usd_to_czk:.3f}")
            col2.metric(f"Max (on {max_date_usd_to_czk})", value=f"{max_usd_to_czk:.3f}")
            col3.metric(f"Min (on {min_date_usd_to_czk})", value=f"{min_usd_to_czk:.3f}")
            ''
            ''
            st.plotly_chart(chart_usd_to_czk, width="stretch")

            ''
            with st.expander("List of records", icon=":material/table:"):
                st.dataframe(df_usd_to_czk_ui)

    with tab3:
        if df_eur_to_usd.empty:
            st.info("There is no data for EUR to USD yet")

        else:
            #------ metrics & chart ------
            value_eur_to_usd_last, delta_eur_to_usd, avg_eur_to_usd, min_eur_to_usd, min_date_eur_to_usd, max_eur_to_usd, max_date_eur_to_usd, last_date_str_eur_to_usd, delta_color_eur_to_usd, delta_arrow_eur_to_usd = extract_variables_from_df(df_eur_to_usd)

            chart_eur_to_usd  = create_chart(df_eur_to_usd, "created_at", "eur_to_usd", "#CE6B0E", "EUR to USD", "USD")

            # ------ UI ------
            ''
            st.metric(
                f"Last record ({last_date_str_eur_to_usd})",
                value=f"{value_eur_to_usd_last:.3f}",
                delta=f"{delta_eur_to_usd:.3f}",
                delta_color=delta_color_eur_to_usd,
                delta_arrow=delta_arrow_eur_to_usd
                )
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Average", value=f"{avg_eur_to_usd:.3f}")
            col2.metric(f"Max (on {max_date_eur_to_usd})", value=f"{max_eur_to_usd:.3f}")
            col3.metric(f"Min (on {min_date_eur_to_usd})", value=f"{min_eur_to_usd:.3f}")
            ''
            ''
            st.plotly_chart(chart_eur_to_usd, width="stretch")

            ''
            with st.expander("List of records", icon=":material/table:"):
                st.dataframe(df_eur_to_usd_ui)