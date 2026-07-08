import streamlit as st
import plotly.express as px
import pandas as pd
from pandas.io.formats.style import Styler
from typing import NamedTuple
from sqlalchemy import create_engine, text, Engine
from Subpages.F3b_SQL_queries import sql_query_extra_service, sql_query_file_format, sql_query_mapping_log, sql_query_overview, sql_query_product, sql_query_transport, sql_query_transport_company, sql_query_order_exist


# ===== Dialog =====
@st.dialog("Error: DB not connected")
def db_connection_fail():

    st.warning("Application is not able to establish connection with DB server -> **This 3B Function is currently not available**")
    st.stop()

# ===== DB connection =====
def connection_db()-> Engine:
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


# ===== TAB 2 validations =====
def input_validation(order_input: str) -> bool:

    '''
    - Simple validation of missing input 
    '''

    if order_input == '':
        st.warning("**Missing input** - Please provide **Order number**")
        return False
    
    return True

# helps to prevent SQL injection to limit inputs to integer only
def input_safety_validation(order_input: str) -> bool:

    '''
    - Simple safety validation to prevent SQL injestion 
    - Order number is INT type (numeric) -> if not possible to change the input (STR) to INT -> except condition
    '''
    
    try: 
        order_input = int(order_input)
        return True

    except:
        st.warning("**Format issue** - The provide Order number is not in correct format")
        return False
    
# 
def input_validation_order_exists(db_engine: Engine, order_input: str) -> bool:

    with db_engine.connect() as conn:
        params = {"order": order_input}
        df_overview = pd.read_sql_query(sql=text(sql_query_order_exist), con=conn, params=params)

    if df_overview.empty:
        st.info(f"**No invoice** found with this **Order number: {order_input}**")
        return False
    
    return True


# Company logo
def get_company_logo_screen_details(input_company: str) -> tuple[str, int]:

    if input_company == 'DHL':
        image = 'Pictures/Function_3/Logo_DHL_v3.svg'
        size = 150
    
    if input_company == 'Fedex':
        image = 'Pictures/Function_3/Logo_Fedex_v3.svg'
        size = 95
    
    return image, size



# TAB 2 main logic
class OrderDetailsResult(NamedTuple):
        file_format: str
        transport_company: str
        df_overview_styled: Styler
        df_product_styled: Styler
        df_extra_service_styled: Styler
        df_transport_styled: Styler
        df_mapping_logs_styled: Styler | pd.DataFrame
        df_mapping_empty_bool: bool



def get_order_details(db_engine: Engine, order_input: str) -> OrderDetailsResult:

    '''
    - Pull data from DB -> DFs
    - DFs styling -> for UI purposes    
    '''
    
    with db_engine.connect() as conn:
        params = {"order": order_input}
        df_file_format = pd.read_sql_query(sql=text(sql_query_file_format), con=conn, params=params)
        df_overview = pd.read_sql_query(sql=text(sql_query_overview), con=conn, params=params)
        df_product = pd.read_sql_query(sql=text(sql_query_product), con=conn, params=params)
        df_extra_service = pd.read_sql_query(sql=text(sql_query_extra_service), con=conn, params=params)
        df_transport = pd.read_sql_query(sql=text(sql_query_transport), con=conn, params=params)
        df_transport_company = pd.read_sql_query(sql=text(sql_query_transport_company), con=conn, params=params)
        df_mapping_logs = pd.read_sql_query(sql=text(sql_query_mapping_log), con=conn, params=params)


 
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
        
        df_mapping_empty_bool = False
    
    else:
        df_mapping_logs_styled = df_mapping_logs
        df_mapping_empty_bool = True


    return OrderDetailsResult(
        file_format,
        transport_company,
        df_overview_styled,
        df_product_styled,
        df_extra_service_styled,
        df_transport_styled,
        df_mapping_logs_styled,
        df_mapping_empty_bool
    )




# ===== TAB 4 validations =====
def df_change_column_name(input_df: pd.DataFrame) -> pd.DataFrame:
    
    dict_names = {
        "extra_service" : "Extra service",
        "count" : "Count",
        "name" : "Label"
    }

    output_df = input_df.rename(columns=dict_names)

    return output_df


def df_styling(input_df: pd.DataFrame) -> pd.DataFrame:
    
    # Need to create a copy of the original DF to do not change existing variable/DF outside of this function
    input_df = input_df.copy()


    input_df[" "] = input_df.index + 1
    input_df = input_df.set_index(" ")

    # Change of column name for UI purposes
    adj_df = df_change_column_name(input_df)

    return adj_df

def create_pie_chart(df_input, x_data, y_data):
                
    chart = px.pie(
    df_input, 
    names = df_input[f"{x_data}"],
    values = df_input[f"{y_data}"]
    )

    # Adjustment to see 2 decimals always in the chart
    chart.update_traces(texttemplate="%{percent:.2%}")

    return chart


# UI fallback - for case when dataframes are empty (no data following search criteria)
def data_empty_fallback_info(input_df: pd.DataFrame) -> bool:

    if input_df.empty:
        st.warning("No data in DB related to the selected date range")
        fallback = True

    else:
        fallback = False

    return fallback