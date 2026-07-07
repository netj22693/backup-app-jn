import time
import json
import xml.etree.ElementTree as ET
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, Engine, text
from sqlalchemy.orm import declarative_base, Session


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
        print("Function: get utc time: Invalid input")


# ===== DB =====

@st.dialog("Error: DB not connected")
def db_connection_fail():

    st.warning("Application is not able to establish connection with DB server -> **This invoice was not saved into DB**")
    st.stop()


def connection_db() -> Engine:
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


# ===== Mapping =====


def mapping_additional_service(service_name: str, price_input: float) -> tuple[str, float]:
    
    mapping = {
        'No additional service': ('None', 0.00),
        'Insurance': ('insurance', 0.15),
        'Extended warranty': ('extended warranty', 0.1)
    }
    
    service, rate = mapping[service_name]
    return service, price_input * rate


# def() for transfering user input into field in XML/JSON
def mapping_additional_service_into_field(service_name: str) -> str:
    
    if service_name == 'No additional service':
        return 'N'

    else:
        return 'Y'


# Mapping
def mapping_currency_for_query(currency: str) -> str:

    mapping = {
        "euro": "euro",
        "US dollar": "us_dollar",
        "Kč": "koruna"
    }

    return mapping.get(currency)      


# Mapping
def mapping_country_to_table(country: str) -> str:

    mapping = {
        "Czech Republic": "country_cz",
        "Slovakia": "country_sk",
    }

    return mapping.get(country) 


def mapping_category(category: str) -> int:

    mapping = {
        "PC" : 1,
        "TV" : 2,
        "Gaming" : 3,
        "Mobile phones" : 4,
        "Tablets" : 5,
        "Major Appliances" : 6,
        "Households" : 7
    }
    return mapping.get(category) 


def mapping_extra_service(service: str) -> int:

    mapping = {
        "No additional service" : 1,
        "Insurance" : 2,
        "Extended warranty" : 3
    }

    result = mapping.get(service)

    if result != 1:
        result_bool = True
    else:
        result_bool = False

    return result, result_bool


def mapping_country(country: str) -> int:

    mapping = {
        "Czech Republic" : 1,
        "Slovakia" : 2
    }
    return mapping.get(country) 


def mapping_transport_company(company: str) -> int:

    mapping = {
        "DHL" : 1,
        "Fedex" : 2
    }
    return mapping.get(company) 


def mapping_size(size: str) -> str:

    mapping = {
        "small" : "s",
        "medium" : "m",
        "large" : "l",
    }
    return mapping.get(size) 

def mapping_currency(currency: str) -> int:

    mapping = {
        "euro" : 1,
        "US dollar" : 2,
        "Kč" : 3,
    }
    return mapping.get(currency) 


def mapping_file_format(format: str) -> int:

    mapping = {
        "XML" : 1,
        "JSON" : 2,
    }
    return mapping.get(format) 


# ===== DEF SQL Query =====
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

# ===== DEF SQL Query =====
def create_order_num(engine) -> str:

    query = f"""
    SELECT MAX(order_number) AS order_number
    FROM billing.invoice
    """

    df_query_result = pd.read_sql(query, engine)

    query_result = df_query_result['order_number'].iloc[0]
    
    # Take the last existing in DB (the highest) + 1 -> next available number
    return str(query_result + 1)


# ===== JSON Builder =====
def create_json_file(data: dict) -> str:

    '''
    - JSON Builder
    - Returns: JSON as str/text
    '''

    data_json = {
        "header" : {
            "order_number" : data["order_number"],
            "customer":  data["customer"],
            "invoice_number": data["invoice_number"],
            "date": data["date"],
            "price": {
                "total_sum": data["total_sum"],
                "currency": data["currency"]
            }
        },
        "detail": {
            "category": data["category"],
            "product_name": data["product_name"],
            "price_amount": data["price_amount"],
            "additional_service": {
                "service": data["service"],
                "service_type": data["service_type"],
                "service_price": data["service_price"]
            }
        },
        "transportation": {
            "transporter": data["transporter"],
            "country": data["country"],
            "size": data["size"],
            "transport_price": data["transport_price"]
        }
    }

    return json.dumps(data_json, indent=4) 


# ==== XML Builder =====
def create_xml_file(data: dict) -> str:
    
    '''
    - XML Builder
    - Returns: XML as str/text
    '''

    xml_doc = ET.Element("invoice")

    header = ET.SubElement(xml_doc, "header")

    ET.SubElement(header, "order_number").text = data["order_number"]
    ET.SubElement(header, "customer").text = data["customer"]
    ET.SubElement(header, "invoice_number").text = data["invoice_number"]
    ET.SubElement(header, "date").text = data["date"]

    price = ET.SubElement(header, "price")
    ET.SubElement(price, "total_sum").text = f'{data["total_sum"]:.2f}'
    ET.SubElement(price, "currency").text = data["currency"]


    detail = ET.SubElement(xml_doc, "detail")
    ET.SubElement(detail, "category").text = data["category"]
    ET.SubElement(detail, "product_name").text = data["product_name"]
    ET.SubElement(detail, "price_amount").text = f'{data["price_amount"]:.2f}'

    add = ET.SubElement(detail, "additional_service")
    ET.SubElement(add, "service").text = data["service"]
    ET.SubElement(add, "service_type").text = data["service_type"]
    ET.SubElement(add, "service_price").text = f'{data["service_price"]:.2f}'

    transport = ET.SubElement(xml_doc, "transportation")
    ET.SubElement(transport, "transporter").text = data["transporter"]
    ET.SubElement(transport, "country").text = data["country"]
    ET.SubElement(transport, "size").text = data["size"]
    ET.SubElement(transport, "transport_price").text = f'{data["transport_price"]:.2f}'

    # Pretty print
    ET.indent(xml_doc, space="   ")

    return ET.tostring(xml_doc, encoding="unicode", xml_declaration=True)


# ===== DEF insert into DB =====
def insert_into_db(engine: Engine, data: dict):
            
    Base = declarative_base()

    class Invoice(Base):
        __tablename__ = "invoice"
        __table_args__ = {"schema": "billing"}

        record_id = Column(Integer, primary_key=True)
        order_number = Column(String)
        date = Column(String)
        customer = Column(String)
        category = Column(String)
        product_name = Column(String)
        product_price = Column(Float)
        extra_service = Column(Boolean)
        extra_service_type = Column(String)
        extra_service_price = Column(String)
        country = Column(String)
        tr_company = Column(String)
        tr_price = Column(Float)
        parcel_size = Column(String)
        total_price = Column(Float)
        currency = Column(String)
        file_format = Column(String)

    with Session(engine) as session:
        new_invoice = Invoice(**data)
        session.add(new_invoice)
        session.commit()


# ===== Clear of inputs - Reset button =====
def reset():
    st.session_state["k_customer"] = None
    st.session_state["k_product"] = None
    st.session_state["k_category"] = None
    st.session_state["k_currency"] = None
    st.session_state["k_price"] = 0.00
    st.session_state["k_add_service"] = "No additional service"
    st.session_state["k_country"] = None
    st.session_state["k_transp"] = None
    st.session_state["k_size"] = None



# ================ DIALOGS - process complete or not complete  =================
def final_dialogs_goto():    
    ''
    st.write("**Go to:**")

    st.page_link(
        label = "Function 3B - Invoice visibility",
        page="Subpages/F3b_FUNCTION_invoice_visibility.py",
        help="The button will redirect to the relevant page within this app.",
        use_container_width=True,
        icon=":material/play_circle:",
        )
    
    st.page_link(
        label = "Function 4 - Mapping",
        page="Subpages/F4_FUNCTION_translation_mapping.py",
        help="The button will redirect to the relevant page within this app.",
        use_container_width=True,
        icon=":material/play_circle:",
        )

    st.page_link(
        label = "Function 5 - Description - API",
        page="Subpages/F5_description_API.py",
        help="The button will redirect to the relevant page within this app.",
        use_container_width=True,
        icon=":material/code:",
        )
    
    st.page_link(
        label = "Home page",
        page="Subpages/Purpose_of_app.py",
        help="The button will redirect to the relevant page within this app.",
        use_container_width=True,
        icon=":material/home:",
        )

@st.dialog("Complete!")
def process_done(order_number):
    st.write(f"""
        - File was created and downloaded -> :green[**Complete**]
        - Order **{order_number}** was inserted into DB -> :green[**Complete**]
        """)
    ''
    final_dialogs_goto()


@st.dialog("Insert into DB failed") 
def insert_db_not_complete():
    st.write("""
        - File was created and downloaded -> :green[**Complete**]
        - But Order **was not** inserted into DB -> :red[**Technical issue**]
        """)
    ''
    final_dialogs_goto()