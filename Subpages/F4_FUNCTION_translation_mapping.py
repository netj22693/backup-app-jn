import streamlit as st
import xml.etree.ElementTree as ET
import json
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime
import pytz

# Final Dialog boxes
@st.dialog("Insert into DB failed") 
def insert_db_not_complete():
	st.write("""
		- Mapping complete -> :green[**Complete**]
		- But log about this change was not inserted into DB -> :red[**Technical issue**]
		""")

@st.dialog("Complete!")
def process_done():
	st.write(f"""
		- Mapping complete -> :green[**Complete**]
		- Log about this change was inserted into DB -> :green[**Complete**]
		""")
	

# Creation of Class based on Base - SQLAlchemy/PostgreSQL 
Base = declarative_base()

class Change_log(Base):
	__tablename__ = "change_log"
	__table_args__ = {"schema": "f4b"}

	log_id = Column(Integer, primary_key=True)
	date = Column(String)
	order_number_log = Column(String)
	change = Column(String)
	mapping_from = Column(String)
	mapping_to = Column(String)


# ======================= Functions ========================
def actual_time_cet_cest():
	cet = pytz.timezone("Europe/Prague")
	now_cet = datetime.now(cet)

	# PostgreSQL format (TIMESTAMP in Postgre)
	postgres_timestamp = now_cet.strftime("%Y-%m-%d %H:%M:%S")

	return postgres_timestamp


# Mapping for DB purpose 
def mapping_format_DB_code(input_from, input_to):

	mapping = {
		"XML" : 1,
		"JSON" : 2

	}

	result_from = mapping.get(input_from)
	result_to = mapping.get(input_to)

	return result_from, result_to

def create_data_for_log(order_number, mapping_from, mapping_to):

	data = {
        "date": actual_time_cet_cest(),   
        "order_number_log": order_number,
        "change": "mapping",
		"mapping_from": mapping_from,
		"mapping_to" : mapping_to
		}

	return data

# DB connection
def connection_db():

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
def write_log_into_db(data):
	
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



#  Parsing XML to JSON
def parsing_xml_mapping_to_json(object_xml):

	# Data import 
	tree_element_data = ET.parse(object_xml)

	root = tree_element_data.getroot()
	#print(f"root identified as {root}")

	# Data parsing from header
	order_number = root[0][0].text
	customer = root[0][1].text
	invoice_number = root[0][2].text
	date = root[0][3].text
	#price>total_sum+currency
	total_sum = root[0][4][0].text
	currency = root[0][4][1].text

	# Data parsing from detail
	category = root[1][0].text
	product_name = root[1][1].text
	price_amount = root[1][2].text
	service = root[1][3][0].text
	service_type = root[1][3][1].text
	service_price = root[1][3][2].text

	# Data parsing from transportation
	transporter = root[2][0].text
	country = root[2][1].text
	size = root[2][2].text
	transport_price = root[2][3].text


	# Change of the data type to be seen as float and not string in JSON
	total_sum_fl = float(total_sum)
	price_amount_fl = float(price_amount)
	service_price_fl = float(service_price)
	transport_price_fl = float(transport_price)


	# JSON structure for build
	data_json = {
		"header" : {
			"order_number" : order_number,
			"customer": customer,
			"invoice_number": invoice_number,
			"date": date,
			"price": {
				"total_sum": total_sum_fl,
				"currency": currency
			}
		},
		"detail": {
			"category": category,
			"product_name": product_name,
			"price_amount": price_amount_fl,
			"additional_service": {
				"service": service,
				"service_type": service_type,
				"service_price": service_price_fl
			}
		},
		"transportation": {
			"transporter": transporter,
			"country": country,
			"size": size,
			"transport_price": transport_price_fl
		}
		}

	json_object = json.dumps(data_json, indent=4)

	file_name = f"{invoice_number}.json"

	mapping_from, mapping_to = mapping_format_DB_code("XML","JSON")

	data_for_log_db = create_data_for_log(order_number, mapping_from, mapping_to)

	return json_object, file_name, data_for_log_db


# def for pretty print of the XML structure to see nesting
def prettify(element, indent='  '):
	queue = [(0, element)]  # (level, element)
	while queue:
		level, element = queue.pop(0)
		children = [(level + 1, child) for child in list(element)]
		if children:
			element.text = '\n' + indent * (level+1)  # for child open
		if queue:
			element.tail = '\n' + indent * queue[0][0]  # for sibling open
		else:
			element.tail = '\n' + indent * (level-1)  # for parent close
		queue[0:0] = children  # prepend so children come before siblings


#  Parsing XML to JSON
def parsing_json_mapping_to_xml(object_json):

	#load the json to a string
	resp = json.load(object_json)

	# extract an element in the response
	order_number = resp['header']['order_number']
	customer = resp['header']['customer']
	invoice_number = resp['header']['invoice_number']
	date = resp['header']['date']

	# price>total_sum+currency
	total_sum = resp['header']['price']['total_sum']
	currency = resp['header']['price']['currency']

	category = resp['detail']['category']
	product_name = resp['detail']['product_name']
	price_amount = resp['detail']['price_amount']
	service = resp['detail']['additional_service']['service']
	service_type = resp['detail']['additional_service']['service_type']
	service_price = resp['detail']['additional_service']['service_price']

	transporter = resp['transportation']['transporter']
	country = resp['transportation']['country']
	size = resp['transportation']['size']
	transport_price = resp['transportation']['transport_price']

	# Change of data type as XML needs them as tring not float when writing into the structure
	total_sum_str = str(total_sum)
	price_amount_str = str(price_amount)
	service_price_str = str(service_price)
	transport_price_str = str(transport_price)

	# Build of XML structure
	xml_doc = ET.Element("invoice")
	header = ET.SubElement(xml_doc, 'header')
	order_number = ET.SubElement(header, 'order_number').text = order_number
	customer = ET.SubElement(header, 'customer').text = customer
	invoice_number = ET.SubElement(header, 'invoice_number').text = invoice_number
	date = ET.SubElement(header, 'date').text = date

	price = ET.SubElement(header, 'price')
	total_sum = ET.SubElement(price, 'total_sum').text = total_sum_str
	currency = ET.SubElement(price, 'currency').text = currency

	detail = ET.SubElement(xml_doc, 'detail')
	category = ET.SubElement(detail, 'category').text = category
	product_name = ET.SubElement(detail, 'product_name').text = product_name
	price_amount = ET.SubElement(detail, 'price_amount').text = price_amount_str
	additional_service = ET.SubElement(detail, 'additional_service')
	service = ET.SubElement(additional_service, 'service').text = service
	service_type = ET.SubElement(additional_service, 'service_type').text = service_type
	service_price = ET.SubElement(additional_service, 'service_price').text = service_price_str

	transportation = ET.SubElement(xml_doc, 'transportation')
	transporter = ET.SubElement(transportation, 'transporter').text = transporter
	country = ET.SubElement(transportation, 'country').text = country
	size = ET.SubElement(transportation, 'size').text = size
	transport_price = ET.SubElement(transportation, 'transport_price').text = transport_price_str

	# Calling the pretty print function
	prettify(xml_doc)

	xml_object = ET.ElementTree(xml_doc)


	# xml_declaration=Tru -> generuje XML prolog
	xml_object.write('Data/Function_4_JSON_to_XML_do_NOT_delete.xml', encoding='UTF-8', xml_declaration=True)

	file_name_xml_fstring = f"{invoice_number}.xml"

	mapping_from, mapping_to = mapping_format_DB_code("JSON","XML")

	data_for_log_db = create_data_for_log(order_number, mapping_from, mapping_to)

	return xml_object, file_name_xml_fstring, data_for_log_db



# ====================== USER SCREEN =============================
# Split of the screen into 2 columns
col1, col2 = st.columns(2)


# ====================== COLUMN 1: XML -> JSON ===================

col1.write("# XML -> JSON :")

col1.write("### Upload XML:")


object_upl_xml = col1.file_uploader("Upload XML", label_visibility="collapsed", type=".xml")


if object_upl_xml is None:
    col1.info("When a file uploaded, translation to JSON will happen")
        

if object_upl_xml is not None:

	try: 
		json_object_returned, file_name_json, data_log_json = parsing_xml_mapping_to_json(object_upl_xml)
		col1.success("Upload complete")

	except Exception as e:
		print(f"Parsing process not complete - {e}")
		col1.error("The uploaded file is not supported by this application")
		json_object_returned = None


	if json_object_returned is not None:

		# Writing of the JSON structure into a file 
		with open("Data/Function_4_XMLtoJSON_do_NOT_delete.json", "w") as outfile:
				outfile.write(json_object_returned)
				outfile.close()

		# Download 
		with open('Data/Function_4_XMLtoJSON_do_NOT_delete.json') as j:
			col1.download_button(
				'Download - JSON',
				j, file_name = file_name_json,
				use_container_width=True,
				icon = ":material/download:",
				on_click= lambda: write_log_into_db(data_log_json)
				)
                                
       
# ====================== COLUMN 2: JSON -> XML ===================

col2.write("# JSON -> XML :")

col2.write("### Upload JSON:")


object_upl_json = col2.file_uploader("Upload JSON", label_visibility="collapsed",key= "json", type=".json")

if object_upl_json is None:
    col2.info("When a file uploaded, translation to XML will happen")
        

if object_upl_json is not None:
    
	try:
		xml_object_returned, file_name_xml, data_log_xml = parsing_json_mapping_to_xml(object_upl_json)
		col2.success("Upload complete")
	
	except Exception as e:
		print(f"Parsing process not complete - {e}")
		col2.error("The uploaded file is not supported by this application")
		xml_object_returned = None


	if xml_object_returned is not None:

		# Download
		with open('Data/Function_4_JSON_to_XML_do_NOT_delete.xml') as j:
			col2.download_button(
				'Download - XML',
				j, file_name = file_name_xml,
				use_container_width=True,
				icon = ":material/download:",
				on_click= lambda: write_log_into_db(data_log_xml)
				)


''
with st.expander(
	"How to use this function",
	icon= ":material/help_outline:"		
    ):
	''
	st.write("""
    - It allows file format translation XML <-> JSON
    - It works with files produced by **Function 3**
    """)
	st.page_link(
        label = "Function 3",
        page="Subpages/F3_FUNCTION_creation_of_XML.py",
        help="The button will redirect to the relevant page within this app.",
        use_container_width=True,
        icon=":material/play_circle:",
        )
		

st.write("-------")

#Closing button/part of the app

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
        icon=":material/code:",
        )
    

if st.button(
    "Close Function 4",
    use_container_width= True,
    icon=":material/close:"
	):
    display_goto_links()