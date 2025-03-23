import streamlit as st
import xml.etree.ElementTree as ET
import time
import plotly.express as px
import pandas as pd
import math


st.write("# Upload XML:")

object_from_upload = st.file_uploader("")

if object_from_upload is None:
    st.info("When a file uploaded, application will start")
        

if object_from_upload is not None:
    st.success("Upload complete")

    # Data import 
    tree_element_data = ET.parse(object_from_upload)

    root = tree_element_data.getroot()
    print(f"root identified as {root}")

    # Data parsing from header
    value_customer = root[0][0].text
    value_invoice_num = root[0][1].text
    value_date = root[0][2].text

    currency = []
    for header_currency in root.findall('header'):
        get_currency = header_currency.find('price/currency').text
        currency.append(get_currency)
    
    currency = currency[0]


    value_total_sum = []
    for header_total_sum in root.findall('header'):
        total_sum = header_total_sum.find('price/total_sum').text
        value_total_sum.append(total_sum)

    # - necessary to change type to float
    value_total_sum = value_total_sum[0]
    value_total_sum = float(value_total_sum)

    value_total_sum_services = []
    for header_total_sum_services in root.findall('header'):
        total_sum_services = header_total_sum_services.find('price/total_sum_services').text
        value_total_sum_services.append(total_sum_services)
        

    # - necessary to change type to float
    value_total_sum_services = value_total_sum_services[0]
    value_total_sum_services_fl = float(value_total_sum_services)
    
 
    #  ----- DATA PARSING FROM DETAIL LEVEL XML ------
    value_category_list = []
    for detail_category in root.findall('detail'):
        category = detail_category.find('category').text
        value_category_list.append(category)


    value_product_name_list = []
    for detail_product_name in root.findall('detail'):
        product_name = detail_product_name.find('product_name').text
        value_product_name_list.append(product_name)


    value_price_list = []
    for detail_price in root.findall('detail'):
        product_price = detail_price.find('price_amount').text
        value_price_list.append(product_price)
        
    
    value_attribut = []
    for detail_id in root.findall('detail'):
        ids = detail_id.get('id')
        value_attribut.append(ids)

    value_attribute_int = list(map(int, value_attribut))
    max_value_attribut = max(value_attribute_int)
    

    # extra logic for recognizing whether any extra money for 'extended varanty' or 'insurance' 
    varanty = []
    for service_type in root.findall('detail'):
        condition_service_type = service_type.find('additional_service/service_type').text

        if condition_service_type == 'extended varanty':
            service_price = service_type.find('additional_service/service_price').text
            varanty.append(service_price)
        
    varanty_float = list(map(float, varanty)) 
    sum_price_varanty = math.fsum(varanty_float)
    

    insurance = []
    for service_type in root.findall('detail'):
        condition_service_type = service_type.find('additional_service/service_type').text

        if condition_service_type == 'insurance':
            service_price = service_type.find('additional_service/service_price').text
            insurance.append(service_price)
        
    insurance_float = list(map(float, insurance)) 
    sum_price_insurance = math.fsum(insurance_float)
    

    #Sum of prices - type change string -> float for calculation
    value_price_list_float = list(map(float, value_price_list)) 
    sum_price = math.fsum(value_price_list_float)
    
    # Data validation - total_sum = pri_values Y/N 
    value_total_sum_fl = float(value_total_sum)


    result_validation = []
    def data_validation(value_total_sum, sum_price):
        result = value_total_sum - sum_price
        st.write("---------")
        st.write("#### Validation process")
        st.write("1) ###### Validation process - Invoice sum = sum of items in lines:")
        
        if result < 0 or result > 0:
            st.warning("Validation not passed - summary does not equeal to line values. You can either continue with existing file or adjust the input file and upload it again.")
            st.write(f"** Total sum in the XML invoice is: '{value_total_sum:.2f}' but summary of prices in detail lines / per product is: '{sum_price:.2f}'.")
            outcome = ("Sum total - Not passed")
            result_validation.append(outcome)

        else:
            st.success("Validation passed")
            outcome = ("Sum total - Passed")
            result_validation.append(outcome)

    data_validation(value_total_sum_fl, sum_price)

    result_obj_outcome = result_validation[0]
    

# Data validation - total_sum_services = value_total_sum_services Y/N 
    
    result_validation_services = []
    def data_validation_services(value_total_sum_services_fl, sum_price_varanty , sum_price_insurance):
        result = value_total_sum_services_fl - sum_price_varanty - sum_price_insurance
        sum_varanty_insurance = sum_price_varanty + sum_price_insurance
        st.write("2) ###### Validation process - Invoice sum services = sum of items in lines:")
        
        if result < 0 or result > 0:
            st.warning("Validation not passed - summary does not equeal to line values. You can either continue with existing file or adjust the input file and upload it again.")
            st.write(f"** Total sum of SERVICES in the XML invoice is: '{value_total_sum_services_fl:.2f}' but summary of prices in detail lines is '{sum_varanty_insurance:.2f}'.")
            outcome = ("Services - Not passed")
            result_validation_services.append(outcome)

        else:
            st.success("Validation passed")
            outcome = ("Services - Passed")
            result_validation_services.append(outcome)

    data_validation_services(value_total_sum_services_fl, sum_price_varanty , sum_price_insurance)

    result_obj_outcome_services = result_validation_services[0]
    

    # Button to show values

    value_to_paid = value_total_sum + sum_price_varanty + sum_price_insurance

    st.write("------")
    st.write("#### Data Visualization:")
    ''
    ''
    if st.button("Summary overview"):
        st.write(f"Sumary:")
        st.write(f" - Invoice number: {value_invoice_num}")
        st.write(f" - Receiver of the invoice: {value_customer}")
        st.write(f" - Invoice from day (date): {value_date} - (format YYYY-MM-DD)")

        st.write(f" - Value to be paid: {value_to_paid:.2f} {currency} (*products + services)")
        st.write(f" - Number of products: {max_value_attribut}")
        ''
        ''
        st.write(f"Detail:")
        st.write(f" - Total sum of products: {value_total_sum:.2f} {currency}")

        sum_additional_serv = sum_price_varanty + sum_price_insurance

        st.write(f" - Sum of additional services: {sum_additional_serv:.2f} {currency}")
        st.write(f" - Extended varanty: {sum_price_varanty:.2f} {currency}")
        st.write(f" - Insurance: {sum_price_insurance:.2f} {currency}")
    ''
    ''
    ''
    ''
    st.write("###### Interactive table and charts:")

    # Transformation of Data to table -> not editable
    data_table = pd.DataFrame({
        "Order" : value_attribut,
        "Product" : value_product_name_list,
        "Price" : value_price_list,
        "Category" : value_category_list                            
        })

    unique_value = data_table['Category'].unique()

    filter_multiselect = st.multiselect(
        "Select category",
        unique_value,
        default = unique_value,
        help = "Select category which you want to see. Multiple categories allowed"
    )  
    
    if not len(filter_multiselect):
        st.warning("Select at lease 1 category to see overview table and charts")

    # min_value_price = data_table['Price'].min()
    # max_value_price = data_table['Price'].max()
    
    
    # Slider na price, zatím nefunkcni
    # from_price, to_price = st.slider(
    #     "Filter Price",
    #     min_value = min_value_price,
    #     max_value = max_value_price,
    #     help = "Select range of prices you want to see"
    # )
    
    
    filtered_data = data_table[
    (data_table["Category"].isin(filter_multiselect))
    # & (data_table["Price"] <= max_value_price)
    # & (min_value_price <= data_table["Price"]) 
    ]

    # This is adjusting the table
    data_table_2 = st.dataframe(data=filtered_data, hide_index=True, use_container_width=True)

    

    # Pie chart
    data = pd.DataFrame({
        "Product" : value_product_name_list,
        "Price" : value_price_list
        })


    fig_pie = px.pie(
        filtered_data, 
        names = "Product",
        values = "Price",
        title = "Pie chart - ratio"
        )

    st.plotly_chart(fig_pie)
    

    fig_bar = px.bar(
        filtered_data, 
        x="Product",
        y="Price",
        title= "Bar chart of products"
        )

    st.plotly_chart(fig_bar)

    # final outcome for print - using server time

    st.write("------")
    st.write("#### Download of .txt:")
    st.write('''A short summary of the original XML invoice, including result of validation, date and some of the parsed data.''')

    st.image("Pictures/V2_pictures/txt outcome_3.png")


    # backend part
    time_objects = time.localtime()
    year, month, day, hour, minute, second, weekday, yearday, daylight = time_objects  

    date_custom = str("Date: %02d-%02d-%04d" % (day,month,year))
    time_custom = str("Time: %02d:%02d:%02d" % (hour,minute,second))
    day_custom = str(("Mon","Tue","Wed","Thu","Fri","Sat","Sun") [weekday])
    day_custom_2 = str("Day: "+ day_custom)
    full_date_outcome = str(date_custom +" | " + day_custom_2 +" | " + time_custom )

    final_outcome = (f"{full_date_outcome} | Validation: 1. {result_obj_outcome}, 2. {result_obj_outcome_services} | Receiver: {value_customer} | Price to pay (including extra services): {value_to_paid:.2f} {currency}.")


    file_name_fstring = f"Summary-{value_invoice_num}.txt"

    if st.download_button("Download", data= final_outcome, file_name= file_name_fstring):
            
        # file = open("print.txt","w")

        # file.write(final_outcome)
        # file.close()
        st.info("download will start in few seconds")

    st.write("------")