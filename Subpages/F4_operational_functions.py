import streamlit as st
import xml.etree.ElementTree as ET
import json
from typing import TextIO
from sqlalchemy import create_engine, Column, Integer, String, Engine
from sqlalchemy.orm import declarative_base, Session
from Subpages.F3_operational_functions import get_utc_time_custom_string, create_json_file, create_xml_file


# ===== Dialogs =====
def final_dialogs_goto():
    ''
    st.write("**Go to:**")

    st.page_link(
    label = "Function F3B - Invoice visibility",
    page="Subpages/F3b_FUNCTION_invoice_visibility.py",
    help="The button will redirect to the relevant page within this app.",
    use_container_width=True,
    icon=":material/play_circle:",
    )

    st.page_link(
    label = "Function F5 - Description",
    page="Subpages/F5_description_API.py",
    help="The button will redirect to the relevant page within this app.",
    use_container_width=True,
    icon=":material/code:",
    )

    st.page_link(
    label = "Function F5 - Exchange Rate",
    page="Subpages/F5_FUNCTION_exchange.py",
    help="The button will redirect to the relevant page within this app.",
    use_container_width=True,
    icon=":material/play_circle:",
    )

    st.page_link(
    label = "Home page",
    page="Subpages/Purpose_of_app.py",
    help="The button will redirect to the relevant page within this app.",
    use_container_width=True,
    icon=":material/home:",
    )




# Final Dialog boxes
@st.dialog("Insert into DB failed") 
def insert_db_not_complete():
	st.write("""
		- Mapping complete -> :green[**Complete**]
		- But log about this change was not inserted into DB -> :red[**Technical issue**]
		""")
	
	final_dialogs_goto()


@st.dialog("Complete!")
def process_done():
	st.write(f"""
		- Mapping complete -> :green[**Complete**]
		- Log about this change was inserted into DB -> :green[**Complete**]
		""")
	
	final_dialogs_goto()


# Go to dialog
@st.dialog("Go to:")
def display_goto_links():

    ''
    st.page_link(
        label = "Function 5 - Description",
        page="Subpages/F5_description_API.py",
        help="The button will redirect to the relevant page within this app.",
        use_container_width=True,
        icon=":material/code:",
        )

    st.page_link(
        label = "Function 5",
        page="Subpages/F5_FUNCTION_exchange.py",
        help="The button will redirect to the relevant page within this app.",
        use_container_width=True,
        icon=":material/play_circle:",
        )
    
    st.page_link(
        label = "Home page",
        page="Subpages/Purpose_of_app.py",
        help="The button will redirect to the relevant page within this app.",
        use_container_width=True,
        icon=":material/home:",
        )



# ===== Mapping for DB purpose =====
def mapping_format_DB_code(input_from: str, input_to: str) -> int:

	mapping = {
		"XML" : 1,
		"JSON" : 2

	}

	result_from = mapping.get(input_from)
	result_to = mapping.get(input_to)

	return result_from, result_to


# ==== Functions related to DB =====

# Data for DB insert
def create_data_for_log(order_number: str, mapping_from: int, mapping_to: int) -> dict:
	
   
    data = {
        "date": get_utc_time_custom_string('change_log'),   
        "order_number_log": order_number,
        "change": "mapping",
		"mapping_from": mapping_from,
		"mapping_to" : mapping_to
	}
    
    return data


# DB connection
def connection_db() -> Engine:

	try:
		# Load secrets
		password = st.secrets["neon"]["password"]
		endpoint = st.secrets["neon"]["endpoint"]

		# connection string
		conn_string = f"postgresql+psycopg2://neondb_owner:{password}@{endpoint}.gwc.azure.neon.tech/neondb?sslmode=require"

		engine = create_engine(conn_string)
		return engine
	
	except Exception as e:
		print(f"DB connection not established: {e}")


# Insert into DB
def write_log_into_db(data: dict):
	
    Base = declarative_base()

    class Change_log(Base):
        __tablename__ = "change_log"
        __table_args__ = {"schema": "billing"}

        log_id = Column(Integer, primary_key=True)
        date = Column(String)
        order_number_log = Column(String)
        change = Column(String)
        mapping_from = Column(String)
        mapping_to = Column(String)
	
    db_engine = connection_db()

    try:
        with Session(db_engine) as session:
            new_invoice = Change_log(**data)
            session.add(new_invoice)
            session.commit()
        process_done()

    except Exception as e:
        print(f"Insert into DB failed: {e}")
        insert_db_not_complete()


# ==== Functions related to parsing =====

#  Parsing XML to JSON
def parsing_xml_mapping_to_json(object_xml: TextIO) -> tuple[str, str, dict]:

    '''
    - Parsing of data from XML to dictionary
    - The dictionary passed to generic JSON Build function
    - Pasing data to the function creating data inputs into DB
    - Returns: data for download as STR (JSON), file name, data for insert into DB
    '''

    # Data import 
    tree = ET.parse(object_xml)

    root = tree.getroot()

    parsed_data_to_dict = {
        "order_number": root.find("header/order_number").text,
        "customer": root.find("header/customer").text,
        "invoice_number": root.find("header/invoice_number").text,
        "date": root.find("header/date").text,
        "total_sum": float(root.find("header/price/total_sum").text),
        "currency": root.find("header/price/currency").text,

        "category": root.find("detail/category").text,
        "product_name": root.find("detail/product_name").text,
        "price_amount": float(root.find("detail/price_amount").text),

        "service": root.find("detail/additional_service/service").text,
        "service_type": root.find("detail/additional_service/service_type").text,
        "service_price": float(root.find("detail/additional_service/service_price").text),

        "transporter": root.find("transportation/transporter").text,
        "country": root.find("transportation/country").text,
        "size": root.find("transportation/size").text,
        "transport_price": float(root.find("transportation/transport_price").text),
    }

    # Using generic function - JSON builder for F3 and F4
    json_object = create_json_file(parsed_data_to_dict)

    file_name = f"{parsed_data_to_dict['invoice_number']}.json"

    mapping_from, mapping_to = mapping_format_DB_code("XML","JSON")

    data_for_log_db = create_data_for_log(parsed_data_to_dict['order_number'], mapping_from, mapping_to)

    return json_object, file_name, data_for_log_db



#  Parsing XML to JSON
def parsing_json_mapping_to_xml(object_json: TextIO) -> tuple[str, str, dict]:

    '''
    - Parsing of data from JSON to dictionary
    - The dictionary passed to generic XML Build function
    - Pasing data to the function creating data inputs into DB
    - Returns: data for download as STR (XML), file name, data for insert into DB
    '''

    # load the json to a string
    resp = json.load(object_json)

    parsed_data_to_dict = {
        # header
        "order_number": resp["header"]["order_number"],
        "customer": resp["header"]["customer"],
        "invoice_number": resp["header"]["invoice_number"],
        "date": resp["header"]["date"],

        # price
        "total_sum": float(resp["header"]["price"]["total_sum"]),
        "currency": resp["header"]["price"]["currency"],

        # detail
        "category": resp["detail"]["category"],
        "product_name": resp["detail"]["product_name"],
        "price_amount": float(resp["detail"]["price_amount"]),

        # additional service
        "service": resp["detail"]["additional_service"]["service"],
        "service_type": resp["detail"]["additional_service"]["service_type"],
        "service_price": float(resp["detail"]["additional_service"]["service_price"]),

        # transportation
        "transporter": resp["transportation"]["transporter"],
        "country": resp["transportation"]["country"],
        "size": resp["transportation"]["size"],
        "transport_price": float(resp["transportation"]["transport_price"])
    }

    # Using generic function - XML builder for F3 and F4
    xml_object = create_xml_file(parsed_data_to_dict)

    file_name_xml_fstring = f"{parsed_data_to_dict['invoice_number']}.xml"

    mapping_from, mapping_to = mapping_format_DB_code("JSON","XML")

    data_for_log_db = create_data_for_log(parsed_data_to_dict['order_number'], mapping_from, mapping_to)

    return xml_object, file_name_xml_fstring, data_for_log_db