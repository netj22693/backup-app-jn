import streamlit as st
import pandas as pd
import time
from datetime import date, timedelta
from sqlalchemy import text
from app_db_connection import db_connection
from Subpages.Resources_ui import UiConfigAndIcons
from Subpages.Resources_ui_objects import render_warning_info, render_info_info
from Subpages.Data.F3_F3B_UI_config_data import CONFIG_UI_INPUTS
from Subpages.Operational.F3b_operational_functions import input_validation, input_safety_validation, get_order_details, get_company_logo_screen_details, input_validation_order_exists, df_styling, create_pie_chart, data_empty_fallback_info, multiselect_validation, get_sql_query_f3b_tab_3, reset_filters_tab3
from Subpages.Services.F3_load_data_from_DB import load_f3_data
from Subpages.SQL.F3b_SQL_queries import sql_query_overview_invoices, sql_query_file_format, get_sql_part_where_date, get_sql_query_category, get_sql_query_company, get_sql_query_parcel_size, get_sql_query_currency, get_sql_query_country, get_sql_query_extra_service_type, get_sql_query_extra_service_count, get_mapping_extra_services, get_sql_query_file_format
from Subpages.Universal.Creation_of_parameters_for_SQL import create_parameters_for_sql
from Subpages.Universal.Universal_functions import adjust_index_in_df, singular_or_plural

start = time.perf_counter()

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
    if st.button("Show last 15 offers", width="stretch", icon=UiConfigAndIcons.Buttons.show_table):

        db_engine = db_connection("F3B", True)

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
        
        submit_button = st.form_submit_button(label= "Submit", width="stretch", icon=UiConfigAndIcons.Buttons.submit)
    

    if submit_button:   


        db_engine = db_connection("F3B", True)            

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

with tab3:
    db_engine = db_connection("F3", True)

    (
    category_options,
    transport_company_options,
    currency_options,
    additional_service_options,
    country_options,
    parcel_size_options,
    file_format_options,
    min_date_db
    ) = load_f3_data(db_engine, "F3B")


    # Validation
    none_values = [
        category_options,
        transport_company_options,
        currency_options,
        additional_service_options,
        country_options,
        parcel_size_options,
        file_format_options,
        min_date_db
    ]

    if any(value is None for value in none_values):
        render_warning_info("**Technical issue** - this part is not available.")
        # UI will not render this tab3 and will continue to tab4

    else:
        # Default state conditions
        submit_disabled = False
        checkbox_date = False
        customer_applicable = False
        product_applicable = False

        # Initiating session states for purpose/possibility of reseting filters
        if "key_category_options" not in st.session_state:
            st.session_state["key_category_options"] = category_options

        if "key_transport_company_options" not in st.session_state:
            st.session_state["key_transport_company_options"] = transport_company_options

        if "key_currency_options" not in st.session_state:
            st.session_state["key_currency_options"] = currency_options

        if "key_additional_service_options" not in st.session_state:
            st.session_state["key_additional_service_options"] = additional_service_options

        if "key_country_options" not in st.session_state:
            st.session_state["key_country_options"] = country_options

        if "key_parcel_size_options"  not in st.session_state:
            st.session_state["key_parcel_size_options"] = parcel_size_options

        if "key_file_format_options"  not in st.session_state:
            st.session_state["key_file_format_options"] = file_format_options

        if "key_sld_number_rows" not in st.session_state:
            st.session_state["key_sld_number_rows"] = 20
        
        if "key_checkbox_date"  not in st.session_state:
            st.session_state["key_checkbox_date"] = False

        if "key_checkbox_text"  not in st.session_state:
            st.session_state["key_checkbox_text"] = False

        st.write("nad blockem")   


        # @st.fragment
        def test_ui(
            submit_disabled,
            checkbox_date,
            category_options,
            transport_company_options,
            currency_options,
            additional_service_options,
            country_options,
            parcel_size_options,
            file_format_options,
            min_date_db          
        ):
            st.write("v bloku")
            start_vnitrek = time.perf_counter()
            # ============ UI filters ============ 
            # Multiselect - category
            ''
            selected_category = st.multiselect(
                f"{CONFIG_UI_INPUTS['category']['icon']} {CONFIG_UI_INPUTS['category']['name']}",
                options=category_options,
                key="key_category_options"
                )
            multiselect_validation(selected_category, "category")

            # Multiselect - currency
            selected_currency = st.multiselect(
                f"{CONFIG_UI_INPUTS['currency']['icon']} {CONFIG_UI_INPUTS['currency']['name']}",
                options=currency_options,
                key="key_currency_options"
                )

            multiselect_validation(selected_currency, "currency")

            # Multiselect - additional service
            selected_additional_service = st.multiselect(
                f"{CONFIG_UI_INPUTS['additional_service']['icon']} {CONFIG_UI_INPUTS['additional_service']['name']}",
                options=additional_service_options,
                key="key_additional_service_options"
                )

            multiselect_validation(selected_additional_service, "service option")

            # Multiselect - country
            selected_country = st.multiselect(
                f"{CONFIG_UI_INPUTS['country']['icon']} {CONFIG_UI_INPUTS['country']['name']}",
                options=country_options,
                key="key_country_options"
                )

            multiselect_validation(selected_country, "country")

            # Multiselect - transport company
            selected_transport_company = st.multiselect(
                f"{CONFIG_UI_INPUTS['transport_company']['icon']} {CONFIG_UI_INPUTS['transport_company']['name']}",
                options=transport_company_options,
                key="key_transport_company_options"
                )

            multiselect_validation(selected_transport_company, "transport company")

            # Multiselect - parcel size
            selected_parcel_size = st.multiselect(
                f"{CONFIG_UI_INPUTS['parcel_size']['icon']} {CONFIG_UI_INPUTS['parcel_size']['name']}",
                options=parcel_size_options,
                key="key_parcel_size_options"
                )

            multiselect_validation(selected_parcel_size, "parcel size")

            # Multiselect - file format
            selected_file_format = st.multiselect(
                f"{CONFIG_UI_INPUTS['file_format']['icon']} {CONFIG_UI_INPUTS['file_format']['name']}",
                options=file_format_options,
                key="key_file_format_options"
                )

            multiselect_validation(selected_file_format, "file format")


            # Date picker
            ''
            checkbox_date = st.checkbox("Filtering based on date", key="key_checkbox_date")

            if checkbox_date == True:
                
                col1, col2 = st.columns(2)

                # Min date allowed
                min_date = min_date_db 

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
                
                # Fallback info 
                if picked_date_from > picked_date_to:
                    render_warning_info("**Date issue** - date **To** is farther in the past than **From**.")
                    submit_disabled = True

                # UI space -> in case that Date picker is displayed
                ''
            else: 
                picked_date_from = None
                picked_date_to = None
        
            # Text search
            checkbox_state_text = st.checkbox("Filtering based on text search", key="key_checkbox_text")

            if checkbox_state_text == True:
                customer = st.text_input(
                    f"{CONFIG_UI_INPUTS['customer']['icon']} {CONFIG_UI_INPUTS['customer']['name']}",
                    max_chars=CONFIG_UI_INPUTS['customer']['limit'],
                    help=CONFIG_UI_INPUTS['customer']['help_f3b']
                    ).strip()

                product = st.text_input(
                    f"{CONFIG_UI_INPUTS['product']['icon']} {CONFIG_UI_INPUTS['product']['name']}",
                    max_chars=CONFIG_UI_INPUTS['product']['limit'],
                    help=CONFIG_UI_INPUTS['product']['help_f3b']
                    ).strip()

            else: 
                customer = None
                product = None

            # Slider - number of rows
            ''
            number_rows = st.slider("Number of records to be shown", min_value=5, max_value=50, step=5, label_visibility="visible", key="key_sld_number_rows")


            end_vnitrek = time.perf_counter()

            st.write("konec bloku")
            st.write(f"Execution time: {end_vnitrek - start_vnitrek:.4f} seconds")

            return (
                selected_category,
                selected_currency,
                selected_additional_service,
                selected_country,
                selected_transport_company,
                selected_parcel_size,
                selected_file_format,
                checkbox_state_text,
                checkbox_date,
                picked_date_from,
                picked_date_to,
                customer,
                product,
                number_rows
            )




        (
        selected_category,
        selected_currency,
        selected_additional_service,
        selected_country,
        selected_transport_company,
        selected_parcel_size,
        selected_file_format,
        checkbox_state_text,
        checkbox_date,
        picked_date_from,
        picked_date_to,
        customer,
        product,
        number_rows
        ) = test_ui(
            submit_disabled,
            checkbox_date,
            category_options,
            transport_company_options,
            currency_options,
            additional_service_options,
            country_options,
            parcel_size_options,
            file_format_options,
            min_date_db
            )

        
        submit_button_tab3 = st.button("Submit", width= "stretch", icon=UiConfigAndIcons.Buttons.submit)

        st.write("pod blokem")
        # ===== Submit button -> triggering query into DB =====
        if submit_button_tab3:

            # ===== Validation =====
            if any(not x for x in [
                selected_category,
                selected_currency,
                selected_additional_service,
                selected_country,
                selected_transport_company,
                selected_parcel_size,
                selected_file_format    
            ]):

                render_warning_info("**Missing input** - please provide.")

            else:
                # Creation of parameter for SQL query
                params_category, str_for_sql_in_category = create_parameters_for_sql(selected_category, "cat")
                params_currency, str_for_sql_in_currency = create_parameters_for_sql(selected_currency, "cur")
                params_additional_service, str_for_sql_in_additional_service = create_parameters_for_sql(selected_additional_service, "as")
                params_country, str_for_sql_in_country = create_parameters_for_sql(selected_country, "c")
                params_transport_company, str_for_sql_in_transport_company = create_parameters_for_sql(selected_transport_company, "tc")
                params_parcel_size, str_for_sql_in_transport_parcel_size = create_parameters_for_sql(selected_parcel_size, "ps")
                params_file_format, str_for_sql_in_transport_file_format = create_parameters_for_sql(selected_file_format, "ff")

                # Marging of the dictionaries to have 1 dictionary with all parameters
                params_full = params_category | params_currency | params_additional_service | params_country | params_transport_company | params_parcel_size | params_file_format

                # If condition to make sure that variables exist
                # len() > 0 not an empty string
                # _applicable - boolean logic for SQL builder function
                # f"%{variable}%" - preperation of wild cards for SQL parameter

                if checkbox_state_text == True:
                    if len(customer) > 0:
                        params_full["customer"] = f"%{customer}%"
                        customer_applicable = True

                    if len(product) > 0:
                        params_full["product"] = f"%{product}%"
                        product_applicable = True

                if checkbox_date == True:
                    params_full["date_from"] = picked_date_from
                    params_full["date_to"] = picked_date_to

                # Limit/number of rows
                params_full["number_rows"] = number_rows

            
                sql_query_tab_3 = get_sql_query_f3b_tab_3(
                    str_for_sql_in_category,
                    str_for_sql_in_currency,
                    str_for_sql_in_additional_service,
                    str_for_sql_in_country,
                    str_for_sql_in_transport_company,
                    str_for_sql_in_transport_parcel_size,
                    str_for_sql_in_transport_file_format,
                    checkbox_date,
                    customer_applicable,
                    product_applicable
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
                    
                    ''
                    if rows_from_db != number_rows:

                        s = singular_or_plural(rows_from_db)

                        render_info_info(f"There is only **{rows_from_db} record{s}** matching the selected criteria.")

                    st.dataframe(df_table_tab_3_styled)


        # ===== Reset button =====
        st.write("-" *10)
        st.button(
            "Reset filters",
            on_click=reset_filters_tab3,
            args=(
                category_options,
                transport_company_options,
                currency_options,
                additional_service_options,
                country_options,
                parcel_size_options,
                file_format_options  
                ),
            width="stretch",
            icon=UiConfigAndIcons.Buttons.reset
            )

# =================  Tab 4  ======================

with tab4:

    # Default state condition
    submit_disabled = False

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
            render_warning_info("**Date issue** - date **To** is farther in the past than **From**.")
            submit_disabled = True
  

    ''
    ''
    submit_button_tab4 = st.button("Submit", width= "stretch", icon=UiConfigAndIcons.Buttons.submit, key="key_submit_button_tab4", disabled=submit_disabled)

    if submit_button_tab4:
        db_engine = db_connection("F3B", True)

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


end = time.perf_counter()

st.write(f"Execution time: {end - start:.4f} seconds")