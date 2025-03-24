import streamlit as st
import xml.etree.ElementTree as ET
import json

col1, col2 = st.columns(2)


# XML -> JSON
col1.write("# XML -> JSON :")

col1.write("### Upload XML:")

object_upl_xml = col1.file_uploader("")

if object_upl_xml is None:
    col1.info("When a file uploaded, translation to JSON will happen")
        

if object_upl_xml is not None:
    col1.success("Upload complete")

    # Data import 
    tree_element_data = ET.parse(object_upl_xml)

    root = tree_element_data.getroot()
    print(f"root identified as {root}")

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


    # Change of teh data type to be seen as float and not string in JSON
    total_sum_fl = float(total_sum)
    price_amount_fl = float(price_amount)
    service_price_fl = float(service_price)
    transport_price_fl = float(transport_price)




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


    with open("Data/Function_4_XMLtoJSON_do NOT delete - JSON.json", "w") as outfile:
            outfile.write(json_object)
            outfile.close()

    file_name_json_fstring = f"{invoice_number}.json"

    with open('Data/Function_3_do NOT delete - JSON.json') as j:
            if col1.download_button(
                'Download - JSON',
                j, file_name = file_name_json_fstring,
                use_container_width=True,
                icon = ":material/download:"
                ):

                col1.info("download will start in few seconds")





# JSON -> XML

col2.write("# JSON -> XML :")

col2.write("### Upload JSON:")


object_upl_json = col2.file_uploader("",key= "json")

if object_upl_json is None:
    col2.info("When a file uploaded, translation to XML will happen")
        

if object_upl_json is not None:
    col2.success("Upload complete")

    #dumps the json object into an element
    # json_str = json.dumps(object_upl_json)

    #load the json to a string
    resp = json.load(object_upl_json)

   
    
    # extract an element in the response
    order_number = resp['header']['order_number']
    customer = resp['header']['customer']
    invoice_number = resp['header']['invoice_number']
    date = resp['header']['date']


    # #price>total_sum+currency
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



    total_sum_str = str(total_sum)
    price_amount_str = str(price_amount)
    service_price_str = str(service_price)
    transport_price_str = str(transport_price)


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


    prettify(xml_doc)

    tree = ET.ElementTree(xml_doc)
    # xml_declaration=Tru -> generuje XML prolog
    tree.write('Data/Function_4_JSONtoXML_do NOT delete - JSON.xml', encoding='UTF-8', xml_declaration=True)

    
    file_name_xml_fstring = f"{invoice_number}.xml"

    with open('Data/Function_4_JSONtoXML_do NOT delete - JSON.xml') as j:
            if col2.download_button(
                'Download - XML',
                j, file_name = file_name_xml_fstring,
                use_container_width=True,
                icon = ":material/download:"
                ):

                col2.info("download will start in few seconds")