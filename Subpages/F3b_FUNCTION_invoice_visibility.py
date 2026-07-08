import streamlit as st
import pandas as pd
from datetime import date, timedelta
from sqlalchemy import text
from Subpages.F3b_operational_functions import connection_db, input_validation, input_safety_validation, get_order_details, get_company_logo_screen_details, input_validation_order_exists, df_styling, create_pie_chart, data_empty_fallback_info
from Subpages.F3b_SQL_queries import sql_query_overview_invoices, sql_query_file_format, get_sql_part_where_date, get_sql_query_category, get_sql_query_company, get_sql_query_parcel_size, get_sql_query_currency, get_sql_query_country, get_sql_query_extra_service_type, get_sql_query_extra_service_count, get_mapping_extra_services, get_sql_query_file_format



# ================ Application Screen - INPUT Buttons ========================
st.write("# Find your invoice:")
''

st.write("- View into DB. Based on invoices created in Function 3...")
''

tab1, tab2, tab3, tab4 = st.tabs([
    "Last 15 invoices",
    "Search for specific invoice",
    "Customized search",
    "Analytics"
])


# ================= Tab 1 ======================
with tab1:

    ''
    if st.button("Show last 15 offers", width="stretch", icon=":material/table:"):

        db_engine = connection_db()

        df = pd.read_sql(sql_query_overview_invoices, db_engine)

        # DF styling

        # This makes index + 1 -> by adding new column which is based on index number + 1 (normal df_styled.index = df_styled.index + 1 here doesn't work due to the style. - ing)
        df[" "] = df.index + 1
        df = df.set_index(" ")

        df["Date"] = pd.to_datetime(df["Date"])

        df_styled = df.style.format({
            "Price": "{:,.2f}",
            "Extra service price": "{:,.2f}",
            "Transport price": "{:,.2f}",
            "Total price": "{:,.2f}",
            "Date": lambda d: d.strftime("%d-%b-%Y")
            })
        
        ''
        st.dataframe(df_styled, width = "stretch", height=562)

# ================= Tab 2 ======================

with tab2: 

    with st.form(key="user_form"):
        order_input = st.text_input(label="Order number:", help="Insert **Order number** of invoice you would like to see. It is based on invoices created in **Function 3**.")

        order_input=order_input.strip()
        
        submit_button = st.form_submit_button(label= "Submit", width="stretch")
    

    if submit_button:   


        db_engine = connection_db()            

        # Trigger function 2 only in case that valid and safe input (SQL injestion) and Order number found in DB
        if not input_validation(order_input) or not input_safety_validation(order_input) or not input_validation_order_exists(db_engine, order_input) :
            pass  # pass because of Streamlit script -> to continue with loadign of other TABs


        # Tab 2 main being triggered here
        else:

            result = get_order_details(db_engine, order_input)

            image_company, size = get_company_logo_screen_details(result.transport_company) 

            # ===== UI user screen =====
            ''
            ''
            st.write(f"- Invoice was originally produced in **{result.file_format}** format")
            ''
            st.write("- Invoice overview:")
            st.dataframe(result.df_overview_styled, hide_index=True)

            ''
            st.write("- Product overview:")
            st.dataframe(result.df_product_styled, hide_index=True)

            ''
            st.write("- Extra service overview:")
            st.dataframe(result.df_extra_service_styled, hide_index=True)

            ''
            st.write("- Transport overview:")
            st.image(image_company, width= size)
            st.dataframe(result.df_transport_styled, hide_index=True)

            ''
            if result.df_mapping_empty_bool == True:
                st.write("- Logs - Invoice mapped to differnet format: **no mapping**")
                st.dataframe(result.df_mapping_logs_styled)
            else:
                st.write("- Logs - Invoice mapped to differnet format:")
                st.dataframe(result.df_mapping_logs_styled)  

# =================  Tab 3  ======================

# To be built up
with tab3:
    st.info("This part is currently under build - to be released soon")

# =================  Tab 4  ======================

with tab4:
    # Date picker
    ''
    radio_state_tb4 = st.radio("Filter",options=["All invoices - no specific date","Date range"])

    if radio_state_tb4 == "All invoices - no specific date":

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
        db_engine = connection_db()

        with db_engine.connect() as conn:

            # Function retruning SQL WHERE condition/string, if filtering based on date applicable
            sql_date_query_where_part = get_sql_part_where_date(date_query_applicable)

            # Build of parameters date
            params_date = {
                "date_from" : picked_date_from_tab4,
                "date_to" : picked_date_to_tab4,
            }

            # Build of parameters joining -> full set of parametrs
            params = params_date

            # Building of SQL queries
            sql_query_category = get_sql_query_category(date_query_applicable, sql_date_query_where_part)
            sql_query_company = get_sql_query_company(date_query_applicable, sql_date_query_where_part) 
            sql_query_parcel_size = get_sql_query_parcel_size(date_query_applicable, sql_date_query_where_part)
            sql_query_currency = get_sql_query_currency(date_query_applicable, sql_date_query_where_part)
            sql_query_country = get_sql_query_country(date_query_applicable, sql_date_query_where_part)
            sql_query_extra_service_type = get_sql_query_extra_service_type(date_query_applicable, sql_date_query_where_part)
            sql_query_extra_service_count = get_sql_query_extra_service_count(date_query_applicable, sql_date_query_where_part)
            sql_query_file_format = get_sql_query_file_format(date_query_applicable, sql_date_query_where_part)

            
            # Dataframes creation
            with db_engine.connect() as conn:
                df_category_grouped = pd.read_sql_query(sql=text(sql_query_category), con = conn, params=params)
                df_company_grouped = pd.read_sql_query(sql=text(sql_query_company), con = conn, params=params)
                df_parcel_size_grouped = pd.read_sql_query(sql=text(sql_query_parcel_size), con = conn, params=params)
                df_currency_grouped = pd.read_sql_query(sql=text(sql_query_currency), con = conn, params=params)
                df_country_grouped = pd.read_sql_query(sql=text(sql_query_country), con = conn, params=params)
                df_extra_service_type_grouped = pd.read_sql_query(sql=text(sql_query_extra_service_type), con = conn, params=params)
                df_extra_service_count_grouped = pd.read_sql_query(sql=text(sql_query_extra_service_count), con = conn, params=params)
                df_file_format_grouped = pd.read_sql_query(sql=text(sql_query_file_format), con = conn, params=params)


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
            ''
            ''
            tab4_tab1, tab4_tab2, tab4_tab3, tab4_tab4, tab4_tab5 = st.tabs([
                "Category & Size",
                "Company & Country",
                "Service type",
                "Currency type",
                "File format",
            ])

            col_layout_1 = [1.5,0.3,2]
            col_layout_2 = [1.5,0.3,1.5]
            

            with tab4_tab1:
                fallback = data_empty_fallback_info(df_category_grouped)

                if fallback == False:
                    st.write(f"- Split based on **category** type - total: **{number_rows_category}**:")
                    col_tab4_1, col_tab4_2, col_tab4_3 = st.columns(col_layout_1)
                    col_tab4_1.dataframe(df_category_grouped_styled, hide_index=True)
                    col_tab4_3.plotly_chart(chart_category, key="chart_category")

                    ''
                    st.write(f"- Split based on **size** type - total: **{number_rows_category}**:")
                    col_tab4_1, col_tab4_2, col_tab4_3 = st.columns(col_layout_1)
                    col_tab4_1.dataframe(df_parcel_size_grouped_styled, hide_index=True)
                    col_tab4_3.plotly_chart(chart_parcel_size, key="chart_parcel_size")

            with tab4_tab2:
                fallback = data_empty_fallback_info(df_company_grouped)

                if fallback == False:
                    st.write(f"- Split based on **delivery company** - total: **{number_rows_category}**:")
                    col_tab4_1, col_tab4_2, col_tab4_3 = st.columns(col_layout_1)
                    col_tab4_1.dataframe(df_company_grouped_styled, hide_index=True)
                    col_tab4_3.plotly_chart(chart_company, key="chart_company")
                    ''
                    st.write(f"- Split based on **selected country for delivery** - total: **{number_rows_extra_service_type}**:")
                    col_tab4_1, col_tab4_2, col_tab4_3 = st.columns(col_layout_1)
                    col_tab4_1.dataframe(df_country_grouped_styled, hide_index=True)
                    col_tab4_3.plotly_chart(chart_country, key="chart_country")


            with tab4_tab3:
                fallback = data_empty_fallback_info(df_extra_service_type_grouped)

                if fallback == False:
                    st.write(f"- Split based on **extra service purchase** - total: **{number_rows_extra_service_count}**:")
                    col_tab4_1, col_tab4_2, col_tab4_3 = st.columns(col_layout_1)
                    col_tab4_1.dataframe(df_extra_service_count_grouped_mapped_styled, hide_index=True)
                    col_tab4_3.plotly_chart(chart_extra_service_count, key="chart_service_count")
                    ''
                    st.write(f"- Split based on selected **extra service type** - total: **{number_rows_extra_service_type}**:")
                    col_tab4_1, col_tab4_2, col_tab4_3 = st.columns(col_layout_1)
                    col_tab4_1.dataframe(df_extra_service_type_grouped_styled, hide_index=True)
                    col_tab4_3.plotly_chart(chart_extra_service_type, key="chart_service_type")

            with tab4_tab4:
                fallback = data_empty_fallback_info(df_currency_grouped)

                if fallback == False:
                    st.write(f"- Split based on **currency** - total: **{number_rows_extra_service_count}**:")
                    col_tab4_1, col_tab4_2, col_tab4_3 = st.columns(col_layout_1)
                    col_tab4_1.dataframe(df_currency_grouped_styled, hide_index=True)
                    col_tab4_3.plotly_chart(chart_currency, key="chart_currency")

            with tab4_tab5:
                fallback = data_empty_fallback_info(df_file_format_grouped)

                if fallback == False:
                    st.write(f"- Split based on **invoice format** - total: **{number_rows_extra_service_count}**:")
                    col_tab4_1, col_tab4_2, col_tab4_3 = st.columns(col_layout_1)
                    col_tab4_1.dataframe(df_file_format_grouped_styled, hide_index=True)
                    col_tab4_3.plotly_chart(chart_file_format, key="chart_file_format")