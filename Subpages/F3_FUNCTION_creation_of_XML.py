import streamlit as st
import xml.etree.ElementTree as ET
import string
import random
import time
import json



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
def order_generator(size=20, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

order_num_generated = order_generator()



# Generation of date for <date> element
now = time.localtime()
print(now)
date_input = time.strftime("%Y-%m-%d", now)

# ================ Application Screen - INPUT Buttons ========================
st.write("# Delivery details:")
''

st.write("Please provide details about order...")
''
with st. expander("Buyer", icon=":material/tag_faces:"):
    customer_input = st.text_input(
        "Customer/Company name:",
        help = "Write a customer name/company name",
        key= "k_customer"
        )

with st. expander("Product", icon=":material/devices:"):

    product_name_inp = st.text_input(
        "Product name:",
        help = "Write a product name",
        key= "k_product"
        )

    category_selb = st.selectbox(
        "Category:" ,
        index = None,
        placeholder= "Select...",
        options=["PC","TV","Gaming","Mobile phones","Tablets","Major Appliances","Households"],
        help = "Select category from which the product is",
        key= "k_category"
         )

with st. expander("Price", icon = ":material/euro_symbol:"):
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
    
    if add_service_select == 'Extended warranty':
        st.info("costs 10% from product price")

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
        "Transporting company:" ,
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




# ============ Logic for Transport values based on user inputs ==============

def calculation_transport(city_selb,size_selb,transport_co_selb, currency_selb):   
    # Czech Republic, DHL, small
    if city_selb == 'Czech Republic' and transport_co_selb == 'DHL' and size_selb == 'small' and currency_selb == 'euro':
        return 2.00
    
    if city_selb == 'Czech Republic' and transport_co_selb == 'DHL' and size_selb == 'small' and currency_selb == 'US dollar':
        return 2.17
    
    if city_selb == 'Czech Republic' and transport_co_selb == 'DHL' and size_selb == 'small' and currency_selb == 'Kč':
        return 50.00

    # Czech Republic, DHL, medium
    if city_selb == 'Czech Republic' and transport_co_selb == 'DHL' and size_selb == 'medium' and currency_selb == 'euro':
        return 3.20
    
    if city_selb == 'Czech Republic' and transport_co_selb == 'DHL' and size_selb == 'medium' and currency_selb == 'US dollar':
        return 3.48
    
    if city_selb == 'Czech Republic' and transport_co_selb == 'DHL' and size_selb == 'medium' and currency_selb == 'Kč':
        return 80.00

    # Czech Republic, DHL, large
    if city_selb == 'Czech Republic' and transport_co_selb == 'DHL' and size_selb == 'large' and currency_selb == 'euro':
        return 4.00
    
    if city_selb == 'Czech Republic' and transport_co_selb == 'DHL' and size_selb == 'large' and currency_selb == 'US dollar':
        return 4.35
    
    if city_selb == 'Czech Republic' and transport_co_selb == 'DHL' and size_selb == 'large' and currency_selb == 'Kč':
        return 100.00
    
    # Czech Republic, Fedex, small
    if city_selb == 'Czech Republic' and transport_co_selb == 'Fedex' and size_selb == 'small' and currency_selb == 'euro':
        return 2.40
    
    if city_selb == 'Czech Republic' and transport_co_selb == 'Fedex' and size_selb == 'small' and currency_selb == 'US dollar':
        return 2.61
    
    if city_selb == 'Czech Republic' and transport_co_selb == 'Fedex' and size_selb == 'small' and currency_selb == 'Kč':
        return 60.00
    
    # Czech Republic, Fedex, medium
    if city_selb == 'Czech Republic' and transport_co_selb == 'Fedex' and size_selb == 'medium' and currency_selb == 'euro':
        return 3.20
    
    if city_selb == 'Czech Republic' and transport_co_selb == 'Fedex' and size_selb == 'medium' and currency_selb == 'US dollar':
        return 3.48
    
    if city_selb == 'Czech Republic' and transport_co_selb == 'Fedex' and size_selb == 'medium' and currency_selb == 'Kč':
        return 80.00
    
    # Czech Republic, Fedex, large
    if city_selb == 'Czech Republic' and transport_co_selb == 'Fedex' and size_selb == 'large' and currency_selb == 'euro':
        return 4.40
    
    if city_selb == 'Czech Republic' and transport_co_selb == 'Fedex' and size_selb == 'large' and currency_selb == 'US dollar':
        return 4.78
    
    if city_selb == 'Czech Republic' and transport_co_selb == 'Fedex' and size_selb == 'large' and currency_selb == 'Kč':
        return 110.00
    
    # Slovakia, DHL, small
    if city_selb == 'Slovakia' and transport_co_selb == 'DHL' and size_selb == 'small' and currency_selb == 'euro':
        return 2.80
    
    if city_selb == 'Slovakia' and transport_co_selb == 'DHL' and size_selb == 'small' and currency_selb == 'US dollar':
        return 3.04
    
    if city_selb == 'Slovakia' and transport_co_selb == 'DHL' and size_selb == 'small' and currency_selb == 'Kč':
        return 70.00
    
    # Slovakia, DHL, medium
    if city_selb == 'Slovakia' and transport_co_selb == 'DHL' and size_selb == 'medium' and currency_selb == 'euro':
        return 4.00
    
    if city_selb == 'Slovakia' and transport_co_selb == 'DHL' and size_selb == 'medium' and currency_selb == 'US dollar':
        return 4.35
    
    if city_selb == 'Slovakia' and transport_co_selb == 'DHL' and size_selb == 'medium' and currency_selb == 'Kč':
        return 100.00
    
    # Slovakia, DHL, small
    if city_selb == 'Slovakia' and transport_co_selb == 'DHL' and size_selb == 'small' and currency_selb == 'euro':
        return 2.80
    
    if city_selb == 'Slovakia' and transport_co_selb == 'DHL' and size_selb == 'small' and currency_selb == 'US dollar':
        return 3.04
    
    if city_selb == 'Slovakia' and transport_co_selb == 'DHL' and size_selb == 'small' and currency_selb == 'Kč':
        return 70.00
    
    # Slovakia, DHL, large
    if city_selb == 'Slovakia' and transport_co_selb == 'DHL' and size_selb == 'large' and currency_selb == 'euro':
        return 6.00
    
    if city_selb == 'Slovakia' and transport_co_selb == 'DHL' and size_selb == 'large' and currency_selb == 'US dollar':
        return 6.52
    
    if city_selb == 'Slovakia' and transport_co_selb == 'DHL' and size_selb == 'large' and currency_selb == 'Kč':
        return 150.00

    # Slovakia, Fedex, small
    if city_selb == 'Slovakia' and transport_co_selb == 'Fedex' and size_selb == 'small' and currency_selb == 'euro':
        return 2.60
    
    if city_selb == 'Slovakia' and transport_co_selb == 'Fedex' and size_selb == 'small' and currency_selb == 'US dollar':
        return 2.83
    
    if city_selb == 'Slovakia' and transport_co_selb == 'Fedex' and size_selb == 'small' and currency_selb == 'Kč':
        return 65.00
    
    # Slovakia, Fedex, medium
    if city_selb == 'Slovakia' and transport_co_selb == 'Fedex' and size_selb == 'medium' and currency_selb == 'euro':
        return 4.80
    
    if city_selb == 'Slovakia' and transport_co_selb == 'Fedex' and size_selb == 'medium' and currency_selb == 'US dollar':
        return 5.22
    
    if city_selb == 'Slovakia' and transport_co_selb == 'Fedex' and size_selb == 'medium' and currency_selb == 'Kč':
        return 120.00
    
    # Slovakia, Fedex, large
    if city_selb == 'Slovakia' and transport_co_selb == 'Fedex' and size_selb == 'large' and currency_selb == 'euro':
        return 6.00
    
    if city_selb == 'Slovakia' and transport_co_selb == 'Fedex' and size_selb == 'large' and currency_selb == 'US dollar':
        return 6.52
    
    if city_selb == 'Slovakia' and transport_co_selb == 'Fedex' and size_selb == 'large' and currency_selb == 'Kč':
        return 150.00

calc_transport_price = calculation_transport(city_selb,size_selb,transport_co_selb, currency_selb)


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

# Logic / notification guidence when fullfiled properly
if customer_input == '' or product_name_inp == '' or category_selb == None or currency_selb == None or price == 0.00 or add_service_select == '' or city_selb == None or transport_co_selb == None or size_selb == None :
    st.warning("**One/Some of the inputs still not entered.** Please check and make sure that you have correctly fullfiled all.")

else:
    st.success("Fulfiled properly - Submit button can be used.")


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
if st.button(
    "Submit",
    use_container_width=True,
    icon = ":material/apps:",
    help = "Submit runs the application -> provide calculation -> summary of the invoice and option of generating either XML or JSON file"
    ):

    if customer_input == '' or product_name_inp == '' or category_selb == None or currency_selb == None or price == 0.00 or add_service_select == '' or city_selb == None or transport_co_selb == None or size_selb == None :

        # This step is stopping the script it this 'if' condition is met. 
        # Simply, if missing input and Submit button pushed -> the application will nto continue
        st.error("**Not all inputs provided** - please check, fill in and then push the **Submit** button again.")

        # This Reset button is specific for this nested condition 
        ("---------")
        st.button(
        "Reset",
        use_container_width= True,
        on_click = reset,
        help = "Clear all text/number inputs from the form")

        # This is what completelly stopping the script
        st.stop()


    else:

        a = id_generator()
        invoice_number_generated = 'INV-' + a
        
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
        ''
        st.write(f" - Total price to pay: **{final_price_fl:,.2f} {currency_selb}**")

        st.info("If this is what you expect, you can proceed with Download button which will create a file (XML or JSON). If not, you can go up and change your inputs and then use the Submit button again.")
        
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

        ''
        st.write("###### Download:")
            
            
        with open('Data/Function_3_do NOT delete.xml') as f:
            if st.download_button(
                'Download - XML',
                f, file_name = file_name_xml_fstring,
                use_container_width=True,
                icon = ":material/download:"
                ):

                st.session_state["Submit"]



        
        
        with open('Data/Function_3_do NOT delete - JSON.json') as j:
            if st.download_button(
                'Download - JSON',
                j, file_name = file_name_json_fstring,
                use_container_width=True,
                icon = ":material/download:"
                ):

                st.info("download will start in few seconds")
        
            
("---------")
st.button(
    "Reset",
    use_container_width= True,
    on_click = reset,
    help = "Clear all text/number inputs from the form")

