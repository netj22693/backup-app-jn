import streamlit as st
import xml.etree.ElementTree as ET
import string
import random
import time
import json
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.orm import declarative_base, Session
import pandas as pd




# ================ Functions defined =========================

# Function for pretty print of XML elements
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



# Function for generating random 6 digits for invoice number
def id_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# a = id_generator()
# invoice_number_generated = 'INV-' + a

# Function for generating random 12 digits for invoice number
# def order_generator(size=5, chars=string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))

# order_num_generated = order_generator()



# Generation of date for <date> element
now = time.localtime()

date_input = time.strftime("%Y-%m-%d", now)


@st.dialog("Error: DB not connected")
def db_connection_fail():

    st.warning("Application is not able to establish connection with DB server -> **This invoice was not saved into DB**")
    st.stop()


def connection_db():
    # Load secrets
    db = st.secrets["neon"]

    # connection string
    try: 
        conn_string = f"postgresql+psycopg2://neondb_owner:{db['password']}@ep-lucky-bar-a9hww36i-pooler.gwc.azure.neon.tech/neondb?sslmode=require"

        engine = create_engine(conn_string)
        return engine

    except:
        db_connection_fail()



# ================ Application Screen - INPUT Buttons ========================
st.write("# Delivery details:")
''

st.write("Please provide details about order...")
''
with st.expander("Buyer", icon=":material/tag_faces:"):
    
    customer_input = st.text_input(
        "Customer/Company name:",
        help = "Write a customer name/company name",
        key= "k_customer"
        )

    customer_input = customer_input.strip()

with st.expander("Product", icon=":material/devices:"):

    product_name_inp = st.text_input(
        "Product name:",
        help = "Write a product name",
        key= "k_product"
        )

    product_name_inp = product_name_inp.strip()

    category_selb = st.selectbox(
        "Category:" ,
        index = None,
        placeholder= "Select...",
        options=["PC","TV","Gaming","Mobile phones","Tablets","Major Appliances","Households"],
        help = "Select category from which the product is",
        key= "k_category"
         )

with st.expander("Price", icon = ":material/euro_symbol:"):
    currency_selb = st.selectbox(
        "Currency:" ,
        index = None,
        placeholder= "Select...",
        options=["euro","US dollar","Kč"],
        help = "Select one from the predefined currencies",
        key= "k_currency"
        )
    
    price = st.number_input(
        "Product price:",
        min_value=0.00,
        step = 10.00,
        help = "You can either click on the +- icons or write the input using numbers. *The step is step +- 10.00 -> i case of diferent values in decimals write it.",
        key= "k_price"
        )
    
    if price == 0.00:
        st.warning("Please change the value to reflect money to be paid (0.00 is not billable)")


with st.expander("Extra purchase", icon = ":material/exposure_plus_1:"):

    add_service_select = st.selectbox(
        "Additional service:" ,
        options=["No additional service","Insurance","Extended warranty"],
        help = "Select one of the options",
        key= "k_add_service"
         )

    if add_service_select == 'Insurance':
        st.info("costs 15% from product price")
        ''
        if price == 0.00 or currency_selb == None:
            pass

        else:
            st.write(f"Product price: {price:,.2f} -> Service costs: **{((price/100)*15):,.2f} {currency_selb}**")
    
    if add_service_select == 'Extended warranty':
        st.info("costs 10% from product price")
        ''
        if price == 0.00 or currency_selb == None:
            pass

        else:
            st.write(f"Product price: {price:,.2f} -> Service costs: **{((price/100)*10):,.2f} {currency_selb}**")



with st.expander("Transportation", icon = ":material/directions_bus:"):

    city_selb = st.selectbox(
        "Country:" ,
        options=["Czech Republic","Slovakia"],
        index = None,
        placeholder="Select...",
        help = "Select one of the options - there is different price for service for each country -> see the pricing table below.",
        key= "k_country"
         )
      
    transport_co_selb = st.selectbox(
        "Transport company:" ,
        options=["DHL","Fedex"],
        index = None,
        placeholder="Select...",
        help = "Select one of the options - there is different price for each company -> see the pricing table below.",
        key= "k_transp"
         )
    
    size_selb = st.selectbox(
        "Size of package:" ,
        options=["small","medium","large"],
        index = None,
        placeholder="Select...",
        help = "Select one of the options - there is different price for each size. Sum of the lengths of all three sides of the parcel max: Small - 50 cm (e.g. 20 cm x 20 cm x 10 cm). Medium 100 cm. Large 200 cm.",
        key= "k_size"        
        )
    ''
    st.image("Pictures/Function_3/Sizes.png")
    ''
    st.write("Pricing table:")
    ''
    st.image("Pictures/Function_3/Price_list.png")

''
''

# Conversion between formats -> due to later mapping into message structures
# this rounding to 2 decimals avoids bugs in case that the input will be having more than 2 decimals. Case: User MANUALY enters number example 20.7777777 -> automatically gets rounded
price = round(price, 2)
price_str = str(price)
price_fl = float(price)
price_fl = float("{:.2f}".format(price_fl))



# =============== Logic for additional service (selected by user on screen) =======

# def() for making a string object
def fun_add_service_1(option):
    
    if option == 'No additional service':
        return 'None'

    elif option == 'Insurance':
        return 'insurance'
    
    elif option == 'Extended warranty':
        return 'extended warranty'

# translation of what was selected from user input into object using def()
service_type_fn = fun_add_service_1(add_service_select)

# def() for calculation of predefined costs based on price and add. service from user inputs
def fun_add_service_2(option, price):
    
    if option == 'No additional service':
        return 0.00

    elif option == 'Insurance':
        ins = price * 0.15
        #ins = str(ins)
        return ins
    
    elif option == 'Extended warranty':
        extv = price * 0.1
        #extv = str(extv)
        return extv

# creation of objects /change of data types
service_price_fn = fun_add_service_2(add_service_select, price)
service_price_fn = round(service_price_fn, 2)
service_price_fn_str = str(service_price_fn)
service_price_fl = float(service_price_fn)


# def() for transfering user input into field in XML/JSON
def fun_add_service_3(option):
    
    if option == 'No additional service':
        return 'N'

    else:
        return 'Y'
       

service_fn = fun_add_service_3(add_service_select)

# ==================== User screen =================================



# Clear of inputs - Reset button
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



# Submit button

''
''
if  st.button(
    "Submit",
    use_container_width=True,
    icon = ":material/apps:",
    help = "Submit runs the application -> provide calculation -> summary of the invoice and option of generating either XML or JSON file"
    ):

    if customer_input == '' or product_name_inp == '' or category_selb == None or currency_selb == None or price == 0.00 or add_service_select == '' or city_selb == None or transport_co_selb == None or size_selb == None :

        # This step is stopping the script it this 'if' condition is met. 
        # Simply, if missing input and Submit button pushed -> the application will nto continue
        st.warning("**Not all inputs provided** - please check, fill in and then push the **Submit** button again.")


    else:
        a = id_generator()
        invoice_number_generated = 'INV-' + a

        def get_transport_price(engine, currency, c_code, size, company):
            
            query = f"""
            SELECT {currency} 
                FROM f3.company a
                INNER JOIN f3.country_{c_code} b ON (a.comp_id = b.c_comp_id)
                INNER JOIN f3.parcel_size c ON (b.size = c.size_id)
                WHERE
                a.name = '{company}' AND
                c.name = '{size}'
            """

            df_query_result = pd.read_sql(query, engine)
            query_result = df_query_result[f'{currency}'].iloc[0]

            return query_result
        
        def make_order_num(engine):

            query = f"""
            SELECT MAX(order_number) AS order_number
            FROM f4b.invoice
            """

            df_query_result = pd.read_sql(query, engine)

            query_result = df_query_result['order_number'].iloc[0]
            
            # Take the last existing in DB (the highest) + 1 -> next available number
            next_order_num = query_result + 1
            next_order_num = str(next_order_num)

            return next_order_num

            
        
        def transform_currency_for_query(currency):

            mapping = {
                "euro": "euro",
                "US dollar": "us_dollar",
                "Kč": "koruna"
            }

            return mapping.get(currency)      



        def transform_country_to_code(country):

            mapping = {
                "Czech Republic": "cz",
                "Slovakia": "sk",
            }

            return mapping.get(country) 



        db_engine = connection_db()

        currency_query = transform_currency_for_query(currency_selb)

        country_code = transform_country_to_code(city_selb)

        calc_transport_price = get_transport_price(db_engine, currency_query, country_code, size_selb, transport_co_selb)

        order_num_generated = make_order_num(db_engine)


        
        # Calculation of final price 
        # important to keep the calculation after SUBMIT button, if not TypeError: unsupported operand type(s) for +: 'float' and 'NoneType'
        final_price_fl = price + calc_transport_price + service_price_fn
        final_price_fl = round(final_price_fl, 2)
        final_price_fl_str = str(final_price_fl)
        
        st.write("#### Summary of your order:")

        st.write(f" - Customer name: **{customer_input}**")
        st.write(f" - Order number: **{order_num_generated}**")
        ''
        st.write(f" - Product name: **{product_name_inp}**")
        st.write(f" - Category: **{category_selb}**")
        st.write(f" - Price: **{price:,.2f} {currency_selb}**")
        ''
        #st.write(f" - Extra service: {add_service_select}")
        st.write(f" - Price for the extra service: **{service_price_fn:,.2f} {currency_selb}** - Extra service: **{add_service_select}** ")
        ''
        st.write(f" - Price for transport: **{calc_transport_price:,.2f} {currency_selb}** - Transport company: **{transport_co_selb}** - Country: **{city_selb}**")
        st.write(f" - Parcel size: **{size_selb}**")
        ''
        st.write(f" - Total price to pay: **{final_price_fl:,.2f} {currency_selb}**")


        ''
        ''
        st.info(f"""
                - When Download button used:
                    - A file will be created - **XML** or **JSON**
                    - Data will be stored into **DB** - Order number: **{order_num_generated}** 
                - If change of data needed:
                    - Go up > Change data > Push Submit button again""")
        
        # Change of data type
        calc_transport_price_str = str(calc_transport_price)
        
        
        # ================ XML and JSON creation =================================
        # XML structure build
        xml_doc = ET.Element("invoice")
        header = ET.SubElement(xml_doc, 'header')
        order_number = ET.SubElement(header, 'order_number').text = order_num_generated
        customer = ET.SubElement(header, 'customer').text = customer_input
        invoice_number = ET.SubElement(header, 'invoice_number').text = invoice_number_generated
        date = ET.SubElement(header, 'date').text = date_input
        price = ET.SubElement(header, 'price')
        total_sum = ET.SubElement(price, 'total_sum').text = final_price_fl_str
        #total_sum_services = ET.SubElement(price, 'total_sum_services').text = service_price_fn
        currency = ET.SubElement(price, 'currency').text = currency_selb

        detail = ET.SubElement(xml_doc, 'detail')
        category= ET.SubElement(detail, 'category').text = category_selb
        product_name = ET.SubElement(detail, 'product_name').text = product_name_inp
        price_amount = ET.SubElement(detail, 'price_amount').text = price_str
        addtional_service = ET.SubElement(detail, 'additional_service')
        service = ET.SubElement(addtional_service, 'service'). text = service_fn
        service_type = ET.SubElement(addtional_service, 'service_type').text = service_type_fn
        service_price = ET.SubElement(addtional_service, 'service_price').text = service_price_fn_str

        transportation = ET.SubElement(xml_doc, 'transportation')
        transporter = ET.SubElement(transportation, 'transporter').text = transport_co_selb
        country = ET.SubElement(transportation, 'country').text = city_selb
        size = ET.SubElement(transportation, 'size').text = size_selb
        transport_price = ET.SubElement(transportation, 'transport_price').text = calc_transport_price_str

        # Calling of the pretty print function to put the XML into nice shape (based on nesting)
        prettify(xml_doc)

        tree = ET.ElementTree(xml_doc)

        # xml_declaration=Tru -> generuje XML prolog
        tree.write('Data/Function_3_do NOT delete.xml', encoding='UTF-8', xml_declaration=True)


        # JSON structure build
        data_json = {
        "header" : {
            "order_number" : order_num_generated,
            "customer": customer_input,
            "invoice_number": invoice_number_generated,
            "date": date_input,
            "price": {
                "total_sum": final_price_fl,
                "currency": currency_selb
            }
        },
        "detail": {
            "category": category_selb,
            "product_name": product_name_inp,
            "price_amount": price_fl,
            "additional_service": {
                "service": service_fn,
                "service_type": service_type_fn,
                "service_price": service_price_fl
            }
        },
        "transportation": {
            "transporter": transport_co_selb,
            "country": city_selb,
            "size": size_selb,
            "transport_price": calc_transport_price
        }
        }

        json_object = json.dumps(data_json, indent=4)

        with open("Data/Function_3_do NOT delete - JSON.json", "w") as outfile:
            outfile.write(json_object)
            outfile.close()


        # File names creation
        file_name_xml_fstring = f"{invoice_number_generated}.xml"
        file_name_json_fstring = f"{invoice_number_generated}.json"


        # ================ Process complete function and not complete =================

        def final_dialogs_goto():    
            ''
            st.write("**Go to:**")

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
                icon=":material/code:",
                )

        @st.dialog("Complete!")
        def process_done():
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


        # ================= DOWNLOAD + FINALIZTION OF THE PROCESS ===========
        ''
        st.write("###### Download:")

        # Functions for mapping
        def mapping_category(input):

            mapping = {
                "PC" : 1,
                "TV" : 2,
                "Gaming" : 3,
                "Mobile phones" : 4,
                "Tablets" : 5,
                "Major Appliances" : 6,
                "Households" : 7
            }

            return mapping.get(input) 

        def mapping_category(input):

            mapping = {
                "PC" : 1,
                "TV" : 2,
                "Gaming" : 3,
                "Mobile phones" : 4,
                "Tablets" : 5,
                "Major Appliances" : 6,
                "Households" : 7
            }
            return mapping.get(input) 


        def mapping_extra_service(input):

            mapping = {
                "No additional service" : 1,
                "Insurance" : 2,
                "Extended warranty" : 3
            }

            result = mapping.get(input)

            if result != 1:
                result_bool = True
            else:
                result_bool = False

            return result, result_bool


        def mapping_country(input):

            mapping = {
                "Czech Republic" : 1,
                "Slovakia" : 2
            }
            return mapping.get(input) 

        def mapping_transport_company(input):

            mapping = {
                "DHL" : 1,
                "Fedex" : 2
            }
            return mapping.get(input) 
        
        def mapping_size(input):

            mapping = {
                "small" : "s",
                "medium" : "m",
                "large" : "l",
            }
            return mapping.get(input) 
        
        def mapping_currency(input):

            mapping = {
                "euro" : 1,
                "US dollar" : 2,
                "Kč" : 3,
            }
            return mapping.get(input) 
        

        # Mapping for DB insert purposes (to follow the ERD / Relation design principle)
        mapped_category = mapping_category(category_selb)
        mapped_extra_service, mapped_extra_service_bool = mapping_extra_service(add_service_select)
        mapped_country = mapping_country(city_selb)
        mapped_tr_company = mapping_transport_company(transport_co_selb)
        mapped_size = mapping_size(size_selb)
        mapped_currency = mapping_currency(currency_selb)


        # Data to be inserted to DB
        data_for_insert = {
        "order_number": order_number,   
        "date": date_input,
        "customer": customer_input,   
        "category": mapped_category,       
        "product_name": product_name_inp,
        "product_price": price_fl,
        "extra_service": mapped_extra_service_bool,           
        "extra_service_type": mapped_extra_service,
        "extra_service_price": service_price_fn,
        "country": mapped_country,
        "tr_company": mapped_tr_company,
        "tr_price": transport_price,
        "parcel_size": mapped_size,
        "total_price": float(final_price_fl),
        "currency": mapped_currency,
        }


        def sql_insert_function(engine, data):
            
            Base = declarative_base()

            class Invoice(Base):
                __tablename__ = "invoice"
                __table_args__ = {"schema": "f4b"}

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

            with Session(engine) as session:
                new_invoice = Invoice(**data)
                session.add(new_invoice)
                session.commit()
            

            
            
        def on_download_click():
            try:
                sql_insert_function(db_engine, data_for_insert)
                process_done()

            except Exception as e:
                print(f"Insert failed: {e}")
                insert_db_not_complete()

        with open('Data/Function_3_do NOT delete.xml', 'rb') as f:

            st.download_button(
                'Download - XML',
                f,
                file_name=file_name_xml_fstring,
                use_container_width=True,
                icon=":material/download:",
                on_click=on_download_click
            )

        
        with open('Data/Function_3_do NOT delete - JSON.json') as j:

            st.download_button(
                'Download - JSON',
                j, file_name = file_name_json_fstring,
                use_container_width=True,
                icon = ":material/download:",
                on_click=on_download_click
            )

            
                
("---------")
st.button(
    "Reset",
    use_container_width= True,
    on_click = reset,
    help = "It will clear the form")

