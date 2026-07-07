import streamlit as st
import xml.etree.ElementTree as ET
from Subpages.F3_operational_functions import create_invoice_number, get_utc_time_custom_string,connection_db, mapping_additional_service, mapping_additional_service_into_field, reset, get_transport_price, mapping_country_to_table, mapping_currency_for_query, create_order_num, insert_db_not_complete, process_done, mapping_category, mapping_country, mapping_currency, mapping_extra_service, mapping_file_format, mapping_size, mapping_transport_company, insert_into_db, create_json_file, create_xml_file



# ================ UI input widgets ========================
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

    if customer_input is not None:
        customer_input = customer_input.strip()

with st.expander("Product", icon=":material/devices:"):

    product_name_inp = st.text_input(
        "Product name:",
        help = "Write a product name",
        key= "k_product"
        )

    if product_name_inp is not None:
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
    ''
    st.image("Pictures/Function_3/F3_Parcel_sizes.svg")
    ''
    ''
    st.image("Pictures/Function_3/F3_Price_list.svg")

''
''

# Conversion between formats -> due to later mapping into message structures
# this rounding to 2 decimals avoids bugs in case that the input will be having more than 2 decimals. Case: User MANUALY enters number example 20.7777777 -> automatically gets rounded
price = round(price, 2)
price_fl = float(price)
price_fl = float("{:.2f}".format(price_fl))



# =============== Logic for additional service (selected by user on screen) =======

# creation of objects /change of data types
service_type_fn , service_price_fn = mapping_additional_service(add_service_select, price)
service_price_fn = round(service_price_fn, 2)
service_price_fl = float(service_price_fn)


# def() for transfering user input into field in XML/JSON    
service_fn = mapping_additional_service_into_field(add_service_select)

# ==================== UI Submit button =================================
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
        db_engine = connection_db()

        currency_query = mapping_currency_for_query(currency_selb)

        country_table = mapping_country_to_table(city_selb)

        calc_transport_price = get_transport_price(db_engine, currency_query, country_table, size_selb, transport_co_selb)

        order_num_generated = create_order_num(db_engine)

        invoice_number_generated = create_invoice_number(order_num_generated)

        date_input = get_utc_time_custom_string('invoice')

   
        # Calculation of final price 
        # important to keep the calculation after SUBMIT button, if not TypeError: unsupported operand type(s) for +: 'float' and 'NoneType'
        final_price_fl = price + calc_transport_price + service_price_fn
        final_price_fl = round(final_price_fl, 2)

        
        # ===== XML and JSON creation -> RAW data to be passed builder functions =====

        data_raw = {
            # STR
            "order_number" : order_num_generated,
            # STR
            "customer" : customer_input,
            # STR
            "invoice_number" : invoice_number_generated,
            # STR
            "date" : date_input,
            # FLOAT
            "total_sum" : final_price_fl,
            # STR
            "currency" : currency_selb,
            # STR
            "category" : category_selb,
            # STR
            "product_name" : product_name_inp,
            # FLOAT
            "price_amount" : price_fl,
            # STR
            "service" : service_fn,
            # STR
            "service_type" : service_type_fn,
            # FLOAT
            "service_price" : service_price_fl,
            # STR
            "transporter" : transport_co_selb,
            # STR
            "country" : city_selb,
            # STR
            "size" : size_selb,
            # FLOAT
            "transport_price" : calc_transport_price
        }


        # File names creation
        file_name_xml_fstring = f"{invoice_number_generated}.xml"
        file_name_json_fstring = f"{invoice_number_generated}.json"
 

        # Mapping for DB insert purposes (to follow the ERD / Relation design principle)
        mapped_category = mapping_category(category_selb)
        mapped_extra_service, mapped_extra_service_bool = mapping_extra_service(add_service_select)
        mapped_country = mapping_country(city_selb)
        mapped_tr_company = mapping_transport_company(transport_co_selb)
        mapped_size = mapping_size(size_selb)
        mapped_currency = mapping_currency(currency_selb)


        # Data to be inserted to DB
        data_for_insert = {
        "order_number": order_num_generated,   
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
        "tr_price": float(calc_transport_price),
        "parcel_size": mapped_size,
        "total_price": float(final_price_fl),
        "currency": mapped_currency,
        # + "file_format": mapped_file_format - by which this is extended bellow, once one of download buttons pushed
        }
           
                   
        def on_download_click(file_format):

            mapped_file_format = mapping_file_format(file_format)

            data_for_insert.update({"file_format": mapped_file_format})

            try:
                insert_into_db(db_engine, data_for_insert)
                process_done(order_num_generated)

            except Exception as e:
                print(f"Insert failed: {e}")
                insert_db_not_complete()
        

        # ================= UI - DOWNLOAD + FINALIZTION OF THE PROCESS ===========
        st.write("#### Summary of your order:")

        st.write(f" - Customer name: **{customer_input}**")
        st.write(f" - Order number: **{order_num_generated}**")
        st.write(f" - Invoice number: **{invoice_number_generated}**")
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
                - When **Download button** used:
                    - A file will be created - **XML** or **JSON**
                    - Data will be stored into **DB** - Order number: **{order_num_generated}** 
                - If change of data needed:
                    - Go up > Change data > Push Submit button again""")
        
        ''
        st.write("###### Download:")  


        st.download_button(
            'Download - XML',
            create_xml_file(data_raw),
            file_name=file_name_xml_fstring,
            use_container_width=True,
            icon=":material/download:",
            on_click=lambda: on_download_click("XML")
        )

        
        st.download_button(
            'Download - JSON',
            create_json_file(data_raw), 
            file_name = file_name_json_fstring,
            use_container_width=True,
            icon = ":material/download:",
            on_click=lambda: on_download_click("JSON")
        )

            
                
("---------")
st.button(
    "Reset",
    use_container_width= True,
    on_click = reset,
    help = "It will clear the form")

