import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta
from sqlalchemy import create_engine, text
from Subpages.F3b_SQL_queries import sql_query_overview_invoices, sql_query_extra_service, sql_query_file_format, sql_query_mapping_log, sql_query_overview, sql_query_product, sql_query_transport, sql_query_transport_company, get_sql_part_where_date, get_sql_query_category, get_sql_query_company, get_sql_query_parcel_size, get_sql_query_currency, get_sql_query_country, get_sql_query_extra_service_type, get_sql_query_extra_service_count, get_mapping_extra_services, get_sql_query_file_format

@st.dialog("Error: DB not connected")
def db_connection_fail():

    st.warning("Application is not able to establish connection with DB server -> **This 3B Function is currently not available**")
    st.stop()


def connection_db():
    # Load secrets
    password = st.secrets["neon"]["password"]
    endpoint = st.secrets["neon"]["endpoint"]

    # connection string
    try: 
        conn_string = f"postgresql+psycopg2://neondb_owner:{password}@{endpoint}.gwc.azure.neon.tech/neondb?sslmode=require"

        engine = create_engine(conn_string)
        return engine

    except:
        db_connection_fail()



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


# =================  Tab 1  ======================
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

# =================  Tab 2 - main logic put in def ======================

def tab_2_logic_run():
    
    # DB connection + queries run
    db_engine = connection_db()

    with db_engine.connect() as conn:
        params = {"order": order_input}
        df_file_format = pd.read_sql_query(sql=text(sql_query_file_format), con=conn, params=params)
        df_overview = pd.read_sql_query(sql=text(sql_query_overview), con=conn, params=params)
        df_product = pd.read_sql_query(sql=text(sql_query_product), con=conn, params=params)
        df_extra_service = pd.read_sql_query(sql=text(sql_query_extra_service), con=conn, params=params)
        df_transport = pd.read_sql_query(sql=text(sql_query_transport), con=conn, params=params)
        df_transport_company = pd.read_sql_query(sql=text(sql_query_transport_company), con=conn, params=params)
        df_mapping_logs = pd.read_sql_query(sql=text(sql_query_mapping_log), con=conn, params=params)


    # Key if/else logic - in case that no match in DB with Order number -> tab_2 logic doesn't continue
    if df_overview.empty or df_file_format.empty:
        st.info(f"**No invoice** found with this **Order number: {order_input}**")
    
    else: 
        # Making variables extracting them from dataframes
        file_format = df_file_format['name'].iloc[0]
        transport_company = df_transport_company['name'].iloc[0]


        #df styling
        df_overview["Date"] = pd.to_datetime(df_overview["Date"])

        df_overview_styled = df_overview.style.format({
            "Total price": "{:,.2f}",
            "Date": lambda d: d.strftime("%d-%m-%Y")
            })

        df_product_styled = df_product.style.format({
            "Price": "{:,.2f}"
            })
        
        df_extra_service_styled = df_extra_service.style.format({
            "Extra service price": "{:,.2f}"
            })

        df_transport_styled = df_transport.style.format({
            "Transport price": "{:,.2f}"
            })

        if not df_mapping_logs.empty:
            # This makes index + 1 -> by adding new column which is based on index number + 1 (normal df_styled.index = df_styled.index + 1 here doesn't work due to the style. - ing)
            df_mapping_logs[" "] = df_mapping_logs.index + 1
            df_mapping_logs = df_mapping_logs.set_index(" ")

            df_mapping_logs["Date"] = pd.to_datetime(df_mapping_logs["Date"])

            df_mapping_logs_styled = df_mapping_logs.style.format({
                "Date": lambda d: d.strftime("%d-%m-%Y - %H:%M:%S")
                })


        def bring_logo_screen(input_company):

            if input_company == 'DHL':
                image = 'Pictures/Function_3/Logo_DHL_v3.svg'
                size = 150
            
            if input_company == 'Fedex':
                image = 'Pictures/Function_3/Logo_Fedex_v3.svg'
                size = 95
            
            return image, size

        logo, size_logo = bring_logo_screen(transport_company)


        # Visualization on user screen
        ''
        ''
        st.write(f"- Invoice was originally produced in **{file_format}** format")
        ''
        st.write("- Invoice overview:")
        st.dataframe(df_overview_styled, hide_index=True)

        ''
        st.write("- Product overview:")
        st.dataframe(df_product_styled, hide_index=True)

        ''
        st.write("- Extra service overview:")
        st.dataframe(df_extra_service_styled, hide_index=True)

        ''
        st.write("- Transport overview:")
        st.image(logo, width= size_logo)
        st.dataframe(df_transport_styled, hide_index=True)

        ''
        if df_mapping_logs.empty:
            st.write("- Logs - Invoice mapped to differnet format: **no mapping**")
            st.dataframe(df_mapping_logs)
        else:
            st.write("- Logs - Invoice mapped to differnet format:")
            st.dataframe(df_mapping_logs_styled)


with tab2: 

    with st.form(key="user_form"):
        order_input = st.text_input(label="Order number:", help="Insert **Order number** of invoice you would like to see. It is based on invoices created in **Function 3**.")

        order_input=order_input.strip()
        
        submit_button = st.form_submit_button(label= "Submit", width="stretch")
    
    if submit_button:

        def input_validation(input):

            if input == '':
                st.warning("**Missing input** - Please provide **Order number**")
                return False
            
            return True
        
        # helps to prevent SQL injection to limit inputs to integer only
        def input_safety_validation(input):
            
            try: 
                input = int(input)
                return True

            except:
                st.warning("**Format issue** - The provide Order number is not in correct format")
                return False
                
                
        
        # if/else logic block - if not preventing for triggering main logic due to wrong input
        if not input_validation(order_input) or not input_safety_validation(order_input):
            pass


        # Tab 2 main being triggered here
        else:
            tab_2_logic_run()
            

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



            def df_change_column_name(input_df: pd.DataFrame) -> pd.DataFrame:
                
                dict_names = {
                    "extra_service" : "Extra service",
                    "count" : "Count",
                    "name" : "Label"
                }

                output_df = input_df.rename(columns=dict_names)

                return output_df
            

            def df_styling_index_set_1(input_df: pd.DataFrame) -> pd.DataFrame:
                
                # Need to create a copy of the original DF to do not change existing variable/DF outside of this function
                input_df = input_df.copy()


                input_df[" "] = input_df.index + 1
                input_df = input_df.set_index(" ")

                # Change of column name for UI purposes
                adj_df = df_change_column_name(input_df)

                return adj_df
            

            # Styling for UI purposes -> index change + column name change
            df_category_grouped_styled = df_styling_index_set_1(df_category_grouped)
            df_company_grouped_styled = df_styling_index_set_1(df_company_grouped)
            df_parcel_size_grouped_styled = df_styling_index_set_1(df_parcel_size_grouped)
            df_currency_grouped_styled = df_styling_index_set_1(df_currency_grouped)
            df_country_grouped_styled = df_styling_index_set_1(df_country_grouped)
            df_extra_service_count_grouped_mapped_styled = df_styling_index_set_1(df_extra_service_count_grouped_mapped)
            df_extra_service_type_grouped_styled = df_styling_index_set_1(df_extra_service_type_grouped)
            df_file_format_grouped_styled = df_styling_index_set_1(df_file_format_grouped)


            # Charts def
            def create_pie_chart(df_input, x_data, y_data):
                
                chart = px.pie(
                df_input, 
                names = df_input[f"{x_data}"],
                values = df_input[f"{y_data}"]
                )

                # Adjustment to see 2 decimals always in the chart
                chart.update_traces(texttemplate="%{percent:.2%}")

                return chart


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


        
            # UI fallback - for case when dataframes are empty (no data following search criteria)
            def data_empty_fallback_info(input_df: pd.DataFrame) -> bool:

                if input_df.empty:
                    st.warning("No data in DB related to the selected date range")
                    fallback = True

                else:
                    fallback = False

                return fallback

            # UI visualization
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