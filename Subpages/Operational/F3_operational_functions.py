import time
import streamlit as st
import pandas as pd
from sqlalchemy import Column, Integer, String, Boolean, Float, Engine, text, Connection
from sqlalchemy.orm import declarative_base, Session
import logging
from app_logging import inicialization_logging
from Subpages.Dialog.F3_dialog import process_done, insert_db_not_complete
from Subpages.Services.F3_DB_mapping import F3MappingFunctions

# ===== Inicialization for logging =====
inicialization_logging()

# ===== FUnction to create INV number =====
def create_invoice_number(order_num: int) -> str:

    return 'INV-' + str(order_num)


# ===== Generating of date for <date> element =====
def get_utc_time_custom_string(purpose: str) -> str:

    '''
    - Function to generate UTC time and format based on DB table and function F3 or F4 
    - 'invoice' - DB table 'invoice' used by F3
    - 'change_log' - DB table 'change_log' used by F4
    
    '''

    now = time.gmtime()

    if purpose == 'invoice':
        return time.strftime("%Y-%m-%d", now)

    elif purpose == 'change_log':
        return time.strftime("%Y-%m-%d %H:%M:%S", now)
    
    else:
        logging.warning("F3 - Operational function: get_utc_time_custom_string() - FAIL - Invalid input")


def pull_data_and_transfer_to_list(query: str, conn: Connection):

    df = pd.read_sql_query(sql=text(query), con=conn)
    return df["name"].tolist()


def extract_data_additional_services(service: str, df: pd.DataFrame)->str:

    df = df[df["name"] == service]

    label = df["mapping_label"].iloc[0]
    percentage = df["cost"].iloc[0]

    return label, percentage


def get_transport_price(engine: Engine, currency: str, table: str, size:str, company: str) -> float:

    '''
    - COLUMN and TABLE inserted as variables into f-string are mapped values (prevents SQL injection) -> save input
    '''
    
    query = f"""
    SELECT {currency} 
        FROM shared.transport_company e
        INNER JOIN transport.{table} x ON (e.comp_id = x.c_comp_id)
        INNER JOIN shared.parcel_size f ON (x.size = f.size_id)
        WHERE
        e.name = :company AND
        f.name = :size
    ;"""

    params = {
        "company" : company,
        "size" : size        
        }

    df_query_result = pd.read_sql(text(query), engine, params=params)
    query_result = df_query_result[f'{currency}'].iloc[0]

    return query_result


def create_order_num(engine) -> int:

    # Using sequence principle
    query = f"""
    SELECT nextval('billing.invoice_order_number_sequence')
    """

    df_query_result = pd.read_sql(query, engine)

    # 'nextval' is the name of column
    query_result = df_query_result['nextval'].iloc[0]
    
    # INT for DB - is important to explicitly change the type to int() due to pandas it is np.int64() which ORM when save to DB has an issue with 
    return int(query_result)


# ===== DEF insert into DB =====
def insert_into_db(engine: Engine, data: dict):
            
    Base = declarative_base()

    class Invoice(Base):
        __tablename__ = "invoice"
        __table_args__ = {"schema": "billing"}

        record_id = Column(Integer, primary_key=True)
        order_number = Column(Integer)
        date = Column(String)
        customer = Column(String)
        category = Column(String)
        product_name = Column(String)
        product_price = Column(Float)
        extra_service = Column(Boolean)
        extra_service_type = Column(String)
        extra_service_price = Column(String)
        country = Column(String)
        transport_company = Column(String)
        transport_price = Column(Float)
        parcel_size = Column(String)
        total_sum = Column(Float)
        currency = Column(String)
        file_format = Column(String)
        invoice_number = Column(String)

    with Session(engine) as session:
        new_invoice = Invoice(**data)
        session.add(new_invoice)
        session.commit()


def on_download_click(db_engine: Engine, file_format: str, data: dict, order_number: str):

    mapped_fileformat = F3MappingFunctions.mapping_file_format(file_format)

    data.update({"file_format": mapped_fileformat})

    try:
        insert_into_db(db_engine, data)
        logging.info("F3 - DB insert - SUCCESS")
        process_done(order_number)

    except Exception as e:
        logging.warning(f"F3 - DB insert - FAIL - Exception: {e}")
        insert_db_not_complete()


# ===== Clear of inputs - Reset button =====
def reset():
    st.session_state["key_customer"] = None
    st.session_state["key_product_name"] = None
    st.session_state["key_category"] = None
    st.session_state["key_currency"] = None
    st.session_state["key_product_price"] = 0.00
    st.session_state["key_additional_service"] = "No additional service"
    st.session_state["key_country"] = None
    st.session_state["key_transport_company"] = None
    st.session_state["key_parcel_size"] = None
