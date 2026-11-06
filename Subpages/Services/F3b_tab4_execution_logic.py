import streamlit as st
import pandas as pd
from sqlalchemy import text, Engine
from Subpages.SQL.F3b_SQL_queries import get_sql_part_where_date, get_sql_query_category, get_sql_query_company, get_sql_query_parcel_size, get_sql_query_currency, get_sql_query_country, get_sql_query_extra_service_type, get_sql_query_extra_service_count, get_mapping_extra_services, get_sql_query_file_format
from Subpages.Operational.F3b_operational_functions import df_styling, create_pie_chart, data_empty_fallback_info
from Subpages.Dialog.APP_universal_dialog import display_input_warning_toast


def execute_f3b_tab4_logic(
    db_engine : Engine,
    selected: dict
    ):

    if selected["date_validation"] == False:
        display_input_warning_toast()
        return


    with db_engine.connect() as conn:

        # shortcut for simplier code
        a = selected["date_applicable"]

        # Function retruning SQL WHERE condition/string, if filtering based on date applicable
        sql_date_query_where_part = get_sql_part_where_date(a)

        # Building of SQL queries
        sql_query_category = get_sql_query_category(a, sql_date_query_where_part)
        sql_query_company = get_sql_query_company(a, sql_date_query_where_part) 
        sql_query_parcel_size = get_sql_query_parcel_size(a, sql_date_query_where_part)
        sql_query_currency = get_sql_query_currency(a, sql_date_query_where_part)
        sql_query_country = get_sql_query_country(a, sql_date_query_where_part)
        sql_query_extra_service_type = get_sql_query_extra_service_type(a, sql_date_query_where_part)
        sql_query_extra_service_count = get_sql_query_extra_service_count(a, sql_date_query_where_part)
        sql_query_file_format = get_sql_query_file_format(a, sql_date_query_where_part)

        
        # Dataframes creation
        with db_engine.connect() as conn:
            df_category_grouped = pd.read_sql_query(sql=text(sql_query_category), con = conn, params=selected)
            df_company_grouped = pd.read_sql_query(sql=text(sql_query_company), con = conn, params=selected)
            df_parcel_size_grouped = pd.read_sql_query(sql=text(sql_query_parcel_size), con = conn, params=selected)
            df_currency_grouped = pd.read_sql_query(sql=text(sql_query_currency), con = conn, params=selected)
            df_country_grouped = pd.read_sql_query(sql=text(sql_query_country), con = conn, params=selected)
            df_extra_service_type_grouped = pd.read_sql_query(sql=text(sql_query_extra_service_type), con = conn, params=selected)
            df_extra_service_count_grouped = pd.read_sql_query(sql=text(sql_query_extra_service_count), con = conn, params=selected)
            df_file_format_grouped = pd.read_sql_query(sql=text(sql_query_file_format), con = conn, params=selected)


        # mapping
        df_extra_service_count_grouped_mapped = get_mapping_extra_services(df_extra_service_count_grouped)

        # DF extract how many records -> for UI purposes
        number_rows_category = df_category_grouped["count"].sum()
        number_rows_extra_service_count = df_extra_service_count_grouped_mapped["count"].sum()
        number_rows_extra_service_type = df_extra_service_type_grouped["count"].sum()
        
        # Styling for UI purposes -> index change + column name change
        df_category_grouped_styled = df_styling(df_category_grouped)
        df_company_grouped_styled = df_styling(df_company_grouped)
        df_parcel_size_grouped_styled = df_styling(df_parcel_size_grouped)
        df_currency_grouped_styled = df_styling(df_currency_grouped)
        df_country_grouped_styled = df_styling(df_country_grouped)
        df_extra_service_count_grouped_mapped_styled = df_styling(df_extra_service_count_grouped_mapped)
        df_extra_service_type_grouped_styled = df_styling(df_extra_service_type_grouped)
        df_file_format_grouped_styled = df_styling(df_file_format_grouped)


        # Charts
        # Note: built based on the DF pulled from DB (column names) not the styled one (in case of change of styling, no need to change the rest of code)
        chart_category = create_pie_chart(df_category_grouped, "name","count")
        chart_company = create_pie_chart(df_company_grouped, "name","count")
        chart_parcel_size = create_pie_chart(df_parcel_size_grouped, "name","count")
        chart_currency = create_pie_chart(df_currency_grouped, "name","count")
        chart_country = create_pie_chart(df_country_grouped, "name","count")
        chart_extra_service_count = create_pie_chart(df_extra_service_count_grouped_mapped, "extra_service","count")
        chart_extra_service_type = create_pie_chart(df_extra_service_type_grouped, "name","count")
        chart_file_format = create_pie_chart(df_file_format_grouped, "name","count")

    
        # ===== UI visualization =====
        st.write("")
        st.write("")

        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Category & Size",
            "Company & Country",
            "Service type",
            "Currency type",
            "File format",
        ])

        col_layout_1 = [1.5,0.3,2]
        

        with tab1:
            fallback = data_empty_fallback_info(df_category_grouped)

            if fallback == False:
                st.write(f"- Split based on **category** type - total: **{number_rows_category}**:")
                col1, col2, col3 = st.columns(col_layout_1)
                col1.dataframe(df_category_grouped_styled, hide_index=True)
                col3.plotly_chart(chart_category, key="chart_category")

                st.write("")
                st.write(f"- Split based on **size** type - total: **{number_rows_category}**:")
                col1, col2, col3 = st.columns(col_layout_1)
                col1.dataframe(df_parcel_size_grouped_styled, hide_index=True)
                col3.plotly_chart(chart_parcel_size, key="chart_parcel_size")

        with tab2:
            fallback = data_empty_fallback_info(df_company_grouped)

            if fallback == False:
                st.write(f"- Split based on **delivery company** - total: **{number_rows_category}**:")
                col1, col2, col3 = st.columns(col_layout_1)
                col1.dataframe(df_company_grouped_styled, hide_index=True)
                col3.plotly_chart(chart_company, key="chart_company")

                st.write("")
                st.write(f"- Split based on **selected country for delivery** - total: **{number_rows_extra_service_type}**:")
                col1, col2, col3 = st.columns(col_layout_1)
                col1.dataframe(df_country_grouped_styled, hide_index=True)
                col3.plotly_chart(chart_country, key="chart_country")


        with tab3:
            fallback = data_empty_fallback_info(df_extra_service_type_grouped)

            if fallback == False:
                st.write(f"- Split based on **extra service purchase** - total: **{number_rows_extra_service_count}**:")
                col1, col2, col3 = st.columns(col_layout_1)
                col1.dataframe(df_extra_service_count_grouped_mapped_styled, hide_index=True)
                col3.plotly_chart(chart_extra_service_count, key="chart_service_count")

                st.write("")
                st.write(f"- Split based on selected **extra service type** - total: **{number_rows_extra_service_type}**:")
                col1, col2, col3 = st.columns(col_layout_1)
                col1.dataframe(df_extra_service_type_grouped_styled, hide_index=True)
                col3.plotly_chart(chart_extra_service_type, key="chart_service_type")

        with tab4:
            fallback = data_empty_fallback_info(df_currency_grouped)

            if fallback == False:
                st.write(f"- Split based on **currency** - total: **{number_rows_extra_service_count}**:")
                col1, col2, col3 = st.columns(col_layout_1)
                col1.dataframe(df_currency_grouped_styled, hide_index=True)
                col3.plotly_chart(chart_currency, key="chart_currency")

        with tab5:
            fallback = data_empty_fallback_info(df_file_format_grouped)

            if fallback == False:
                st.write(f"- Split based on **invoice format** - total: **{number_rows_extra_service_count}**:")
                col1, col2, col3 = st.columns(col_layout_1)
                col1.dataframe(df_file_format_grouped_styled, hide_index=True)
                col3.plotly_chart(chart_file_format, key="chart_file_format")