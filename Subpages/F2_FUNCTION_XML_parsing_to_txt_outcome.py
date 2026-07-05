import streamlit as st
import xml.etree.ElementTree as ET
import time
import pandas as pd
import math
import pandasql as ps
from Subpages.F2_expanders import show_expander_help, show_expander_help_validation_process
from Subpages.F2_operational_functions import validate_xml_against_xsd, data_parsing_find, data_parsing_get, data_parsing_find_conditional, data_parsing_including_additional_services, create_pie_chart, df_styling, close_function, display_warning_multiselect, create_bar_chart, data_validation, data_validation_services, data_parsing_find_conditional_with_none_condition, get_utc_time_custom_string, get_filtered_df_including_ui_filters
from Subpages.F2_SQL_queries import get_sql_query_item_inc_add_service, get_sql_query_percentage_product_prices_category, get_sql_query_percentage_product_prices_category_inc_add_serv, get_sql_query_percentage_add_services, sql_query_no_items_product_category, sql_query_no_items_with_additional_service, sql_query_no_items_without_additional_service, sql_query_expensive_item, sql_query_cheapest_item, sql_query_avg_price, sql_query_avg_price_with_add_serv, sql_query_avg_price_of_add_serv



# ==== UI upload box ====

st.write("# Upload XML:")
''

# type = ".xml" - allows to upload only xml files
object_from_upload = st.file_uploader("Upload your XML file", type=".xml", label_visibility="collapsed", accept_multiple_files=False)

if object_from_upload is None:
    st.info("When a file uploaded, the application will start")

    show_expander_help()


# ==== F2 logic when file uploaded ====

if object_from_upload is not None:

    # Validation XML against XSD
    validate_xml_against_xsd(xml_path = object_from_upload, xsd_path ="F2_XSD_validation/XML_Schema_for_functions_1_and_2.xsd")
    
    tree_element_data = ET.parse(object_from_upload)

    root = tree_element_data.getroot()


    #  ==== DATA PARSING FROM HEADER LEVEL XML ====
    value_customer = root[0][0].text
    value_invoice_num = root[0][1].text
    value_date = root[0][2].text


    currency = data_parsing_find(root,'header','price/currency', False, False)
    value_total_sum = data_parsing_find(root,'header','price/total_sum', True, False) 
    value_total_sum_services_fl = data_parsing_find(root,'header','price/total_sum_services', True, False)   

    

    #  ==== DATA PARSING FROM DETAIL LEVEL XML ====   
    value_category_list = data_parsing_find(root,'detail','category', False, True)   
    value_product_name_list = data_parsing_find(root,'detail','product_name', False, True)
    value_price_list = data_parsing_find(root,'detail','price_amount', False, True)

    value_attribut = data_parsing_get(root,'detail', 'id')
    
    # Change of types
    value_price_list_fl = list(map(float, value_price_list))

    value_attribute_int = list(map(int, value_attribut))
    max_value_attribut = max(value_attribute_int)

    
    # Logic for recognizing whether any extra money for 'extended warranty' or 'insurance'   
    warranty = data_parsing_find_conditional(root,'detail','additional_service/service_type', 'extended warranty', 'additional_service/service_price')
    
    warranty_float = list(map(float, warranty)) 
    sum_price_warranty = math.fsum(warranty_float)

    insurance = data_parsing_find_conditional(root,'detail','additional_service/service_type', 'insurance', 'additional_service/service_price')   
       
    insurance_float = list(map(float, insurance)) 
    sum_price_insurance = math.fsum(insurance_float)

    #Extra parsing for charts
    # Type of additional service <additional_service> - Including 'None'
    add_service_full = data_parsing_find(root,'detail','additional_service/service_type', False, True )

    add_service_full = list(map(str.capitalize, add_service_full))


    # Prices full - including '0.00' for None values
    add_ser_price_full = data_parsing_find_conditional_with_none_condition(root,'detail','additional_service/service_type')


    # Extra parsing for charts in SQL 3 expander  - NOT including add.services
    price_gaming = data_parsing_find_conditional(root,'detail','category','Gaming','price_amount')
    price_mobile_phone = data_parsing_find_conditional(root,'detail','category','Mobile phones','price_amount')
    price_tablets = data_parsing_find_conditional(root,'detail','category','Tablets','price_amount')
    price_pc = data_parsing_find_conditional(root,'detail','category','PC','price_amount')
    price_tv = data_parsing_find_conditional(root,'detail','category','TV','price_amount')
    price_majapliances = data_parsing_find_conditional(root,'detail','category','Major Appliances','price_amount')
    price_majapliances = data_parsing_find_conditional(root,'detail','category','Major Appliances','price_amount')
    price_househol = data_parsing_find_conditional(root,'detail','category','Households','price_amount')


    # Type change from string to float
    price_gaming = list(map(float, price_gaming))
    price_mobile_phone = list(map(float, price_mobile_phone))
    price_tablets = list(map(float, price_tablets))
    price_pc = list(map(float, price_pc))
    price_tv = list(map(float, price_tv))
    price_majapliances = list(map(float, price_majapliances))
    price_househol = list(map(float, price_househol))

    # Sum of the list values
    sum_price_gaming = sum(price_gaming)
    sum_price_mobile_phone = sum(price_mobile_phone)
    sum_price_tablets = sum(price_tablets)
    sum_price_pc = sum(price_pc)
    sum_price_tv = sum(price_tv)
    sum_price_majapliances = sum(price_majapliances)
    sum_price_househol = sum(price_househol)


    # 10-July-2025 Extra parsing for charts in SQL 3 expander  - INCLUDING add services
    sum_price_gaming_addserv = data_parsing_including_additional_services(root,'detail','category','Gaming', 'additional_service/service_type', 'additional_service/service_price')

    sum_price_mobphones_addserv = data_parsing_including_additional_services(root,'detail','category','Mobile phones','additional_service/service_type', 'additional_service/service_price')

    sum_price_tablets_addserv = data_parsing_including_additional_services(root,'detail','category','Tablets','additional_service/service_type', 'additional_service/service_price')

    sum_price_pc_addserv = data_parsing_including_additional_services(root,'detail','category','PC','additional_service/service_type', 'additional_service/service_price')

    sum_price_tv_addserv = data_parsing_including_additional_services(root,'detail','category','TV','additional_service/service_type', 'additional_service/service_price')

    sum_price_majappl_addserv = data_parsing_including_additional_services(root,'detail','category','Major Appliances','additional_service/service_type', 'additional_service/service_price')

    sum_price_households_addserv = data_parsing_including_additional_services(root,'detail','category','Households','additional_service/service_type', 'additional_service/service_price')



    # sum of sum - price + additional service price -> for chart in SQL 3 expander
    ss_gaming = sum_price_gaming + sum_price_gaming_addserv
    ss_mobile = sum_price_mobile_phone + sum_price_mobphones_addserv
    ss_tablets = sum_price_tablets + sum_price_tablets_addserv
    ss_pc = sum_price_pc + sum_price_pc_addserv
    ss_tv = sum_price_tv + sum_price_tv_addserv
    ss_majapp = sum_price_majapliances + sum_price_majappl_addserv
    ss_househlds = sum_price_househol + sum_price_households_addserv


    # Sum of prices - type change string -> float for calculation
    value_price_list_float = list(map(float, value_price_list)) 
    sum_price = math.fsum(value_price_list_float)
    
    # Data validation - total_sum = pri_values Y/N 
    value_total_sum_fl = float(value_total_sum)

    # Data type change for purpose of charts
    add_ser_price_full_float = list(map(float, add_ser_price_full)) 
    sum_adds_fl = math.fsum(add_ser_price_full_float)


    # v 3.2.X and higher - additional parsing for charts ---------------

    pro_price_where_insurance = data_parsing_find_conditional(root,'detail','additional_service/service_type', 'insurance', 'price_amount')

    pro_price_where_ewarranty = data_parsing_find_conditional(root,'detail','additional_service/service_type', 'extended warranty', 'price_amount')

       
    pro_price_where_insurance = list(map(float, pro_price_where_insurance)) 
    sum_pro_price_where_insurance = math.fsum(pro_price_where_insurance)

    pro_price_where_ewarranty = list(map(float, pro_price_where_ewarranty)) 
    sum_pro_price_where_ewarranty = math.fsum(pro_price_where_ewarranty)

    # ==== UI ====

    # Notification to appear on the screen when all parsing steps successfully done
    st.success("Upload complete")

    # Validation if DETAIL line sum matches HEADER value 
    # <total_sum>

    st.write("---------")
    st.write("#### Validation process")
    ''
    st.write("1) ###### Validation process")

    result_obj_outcome = data_validation(value_total_sum_fl, sum_price, currency)


    # Data validation - <total_sum_services> = value_total_sum_services Y/N 
    
    ''
    st.write("2) ###### Validation process")

    result_obj_outcome_services = data_validation_services(value_total_sum_services_fl, sum_price_warranty , sum_price_insurance, currency)

    value_to_paid = value_total_sum + sum_price_warranty + sum_price_insurance

    # ==== UI ====
    ''
    ''
    with st.expander("Help",icon= ":material/help_outline:"):
        show_expander_help_validation_process()

    st.write("------")
    st.write("#### Data Visualization:")
    ''
    ''
    with st.expander("Summary overview - Invoice", icon = ":material/apps:"):
        ''
        '' 
        st.write(f"**Sumary:**")
        st.write(f" - Invoice number: **{value_invoice_num}**")
        st.write(f" - Receiver of the invoice: **{value_customer}**")
        st.write(f" - Invoice from date (YYYY-MM-DD): **{value_date}**")

        st.write(f" - Price to be paid: **{value_to_paid:,.2f} {currency}** (*products + services)")
        st.write(f" - Number of products: **{max_value_attribut}**")
        ''
        ''
        ''
        st.write(f"**Detail:**")
        st.write(f" - Total sum of products: **{value_total_sum:,.2f} {currency}**")

        sum_additional_serv = sum_price_warranty + sum_price_insurance

        st.write(f" - Sum of additional services: **{sum_additional_serv:,.2f} {currency}**")
        st.write(f" - Extended warranty: **{sum_price_warranty:,.2f} {currency}**")
        st.write(f" - Insurance: **{sum_price_insurance:,.2f} {currency}**")
        ''
        ''

    # Transformation of Data to table -> not editable table
    data_table = pd.DataFrame({
        "Item id" : value_attribut,
        "Product" : value_product_name_list,
        "Price" : value_price_list_fl, # must be float due to filtring in table    
        "Category" : value_category_list, 
        "Additional service" : add_service_full, 
        "Additional service price" : add_ser_price_full_float  # must be float due to filtring in table                
        })

    
    data_table_sql = pd.DataFrame({
        "Item_id" : value_attribut,
        "Product" : value_product_name_list,
        "Price" : value_price_list_fl, # must be float due to filtring in table    
        "Category" : value_category_list, 
        "Additional_service" : add_service_full, 
        "Additional_service_price" : add_ser_price_full_float  # must be float due to filtring in table                
        })


    # SQL 1
    with st.expander("SQL Queries 1 - Overview", icon = ":material/view_list:"):
        ''
        '' 
        st.write(f"- Number of items in **each product Category** (No. of items - {max_value_attribut}):")
        st.dataframe(ps.sqldf(sql_query_no_items_product_category, locals()), hide_index=True, width="stretch")

        ''
        ''
        st.write("- Number of items having **additional services**:")
        st.dataframe(ps.sqldf(sql_query_no_items_with_additional_service, locals()), hide_index=True, width="stretch")

        ''
        ''
        st.write("- Number of items **without** any additional service:")
        st.dataframe(ps.sqldf(sql_query_no_items_without_additional_service, locals()), hide_index=True, width="stretch")

    # SQL 2
    with st.expander("SQL Queries 2 - Prices/Costs", icon = ":material/view_list:"):

        # Get SQL queries
        sql_query_warranty_expensive_inc_add_serv = get_sql_query_item_inc_add_service('Extended warranty', 'DESC')
        sql_query_insurance_expensive_inc_add_serv = get_sql_query_item_inc_add_service('Insurance', 'DESC')
        sql_query_warranty_cheapest_inc_add_serv = get_sql_query_item_inc_add_service('Extended warranty', 'ASC')
        sql_query_insurance_cheapest_inc_add_serv = get_sql_query_item_inc_add_service('Insurance', 'ASC')


        # Extract data
        df_q1 = ps.sqldf(sql_query_expensive_item, locals())
        df_q2 = ps.sqldf(sql_query_warranty_expensive_inc_add_serv, locals())
        df_q2b = ps.sqldf(sql_query_insurance_expensive_inc_add_serv, locals())
        df_q3 = ps.sqldf(sql_query_cheapest_item, locals())
        df_q4 = ps.sqldf(sql_query_warranty_cheapest_inc_add_serv, locals())
        df_q4b = ps.sqldf(sql_query_insurance_cheapest_inc_add_serv, locals())


        # Data styling before visualization  -> 2 decimals
        df_q1_styled = df_styling(df_q1)
        df_q2_styled = df_styling(df_q2)
        df_q2b_styled = df_styling(df_q2b)
        df_q3_styled = df_styling(df_q3)
        df_q4_styled = df_styling(df_q4)
        df_q4b_styled = df_styling(df_q4b)

        # === UI - Data visualization ====
        ''
        ''
        st.write(f"- Currency: **{currency}**")
        ''
        ''  
        st.write("- The **most expensive** item (Price):")
        st.dataframe(data=df_q1_styled, hide_index=True, width="stretch")
        ''
        ''
        st.write("- The **most expensive additional service** (Extended warranty and Insurance):")
        st.dataframe(df_q2_styled, hide_index=True, width="stretch")
        st.dataframe(df_q2b_styled, hide_index=True, width="stretch")
        ''
        ''
        st.write("- The **cheapest** item (lowest Price):")
        st.dataframe(data=df_q3_styled, hide_index=True, width="stretch")
        ''
        ''
        st.write("- The **cheapest additional service** (Extended warranty and Insurance):")
        st.dataframe(df_q4_styled, hide_index=True, width="stretch")
        st.dataframe(df_q4b_styled, hide_index=True, width="stretch")


    # SQL 3 
    with st.expander("SQL Queries 3 & Pie Charts - % Ratio", icon = ":material/clock_loader_60:"):

        sql_query_percentage_category = get_sql_query_percentage_product_prices_category(value_total_sum)

        sql_query_percentage_category_inc_add_serv = get_sql_query_percentage_product_prices_category_inc_add_serv(value_to_paid)

        sql_query_percentage_add_services = get_sql_query_percentage_add_services(sum_additional_serv)


        df_q5 = ps.sqldf(sql_query_percentage_category, locals())
        df_q5b = ps.sqldf(sql_query_percentage_category_inc_add_serv, locals())
        df_q6 = ps.sqldf(sql_query_percentage_add_services, locals())

        # Data styling before visualization  -> 2 decimals
        df_q5_styled = df_styling(df_q5)
        df_q5b_styled = df_styling(df_q5b)
        df_q6_styled = df_styling(df_q6)


        # Data frames for Charts in SQL 3 expander
        df_pie_sql3_1 = pd.DataFrame({

            "Costs" : [
                sum_price_gaming,
                sum_price_mobile_phone,
                sum_price_tablets,
                sum_price_pc,
                sum_price_tv,
                sum_price_majapliances,
                sum_price_househol
                ],

            "Category" : [
                "Gaming",
                "Mobile phones",
                "Tablets",
                "PC",
                "TV",
                "Major Appliances",
                "Households"
                ]
            })
        
       
        df_pie_sql3_2 = pd.DataFrame({

            "Costs" : [
                sum_price_gaming_addserv,
                sum_price_mobphones_addserv,
                sum_price_tablets_addserv,
                sum_price_pc_addserv,
                sum_price_tv_addserv,
                sum_price_majappl_addserv,
                sum_price_households_addserv
                ],

            "Category" : [
                "Gaming",
                "Mobile phones",
                "Tablets",
                "PC",
                "TV"
                ,"Major Appliances"
                ,"Households"
                ]
            })

      
        df_pie_sql3_3 = pd.DataFrame({

            "Costs" : [
                ss_gaming,
                ss_mobile,
                ss_tablets,
                ss_pc,
                ss_tv,
                ss_majapp,
                ss_househlds
                ],

            "Category" : ["Gaming",
                "Mobile phones",
                "Tablets",
                "PC",
                "TV"
                ,"Major Appliances"
                ,"Households"
                ]
            })


        
        # ==== UI - Data visualization ====
        ''
        ''
        st.write(f"- Currency: **{currency}**")
        '' 
        st.write(f"- No. of items: **{max_value_attribut}**")

        '' 
        st.write(f"- **(1) Percentage % ratio** of product costs per **Category**. From  total sum of products: **{value_total_sum:,.2f} {currency}** ")

        st.dataframe(df_q5_styled, hide_index=True, width="stretch")
        
        ''
        st.write(f"- **(2) Percentage % ratio** of product prices per **Category**. From  total sum of products: **{value_to_paid:,.2f} {currency}**, **including** additional services **{sum_additional_serv:,.2f} {currency}**.")

        st.dataframe(df_q5b_styled, hide_index=True, width="stretch")

        ''
        st.write(f"- **(3) Percentage % ratio** of **additional services** per Category (**{sum_additional_serv:,.2f} {currency}**)")

        st.dataframe(df_q6_styled, hide_index=True, width="stretch")   

        # ==== UI - Charts visualization ====
        ''
        ''
        col1, col2 = st.columns(2, gap="medium")


        col1.plotly_chart(create_pie_chart(df_pie_sql3_1,"Category","Costs","(1) Ratio of product costs per Category:", True))
        col2.plotly_chart(create_pie_chart(df_pie_sql3_3,"Category","Costs","(2) ...including add. services:", True))
        col1.plotly_chart(create_pie_chart(df_pie_sql3_2,"Category","Costs","(3) Ratio of additional services per Category:", True))




    # SQL 4
    with st.expander("SQL Queries 4 - Average", icon = ":material/view_list:"):


        df_q4 = ps.sqldf(sql_query_avg_price, locals())
        df_q4b = ps.sqldf(sql_query_avg_price_with_add_serv, locals())
        df_q4c = ps.sqldf(sql_query_avg_price_of_add_serv, locals())

        # Data styling before visualization  -> 2 decimals
        df_q4_styled = df_styling(df_q4)
        df_q4b_styled = df_styling(df_q4b)
        df_q4c_styled = df_styling(df_q4c)

        # ==== UI Visualization ====
        ''
        ''
        st.write(f"- Currency: **{currency}**")
        '' 
        st.write("- Tables show values **only** if there is more than 1 item/product in specific category -> **no. of products > 1**")
        '' 
        ''

        st.write(f"- **Average price** in each product Category (Total price **{value_total_sum:,.2f} {currency}** - **without** additional services):")

        st.dataframe(df_q4_styled, hide_index=True, width="stretch")

        ''
        ''
        st.write(f"""
        - **Average price including additional service price** in each product Category:
            - Total price **{value_to_paid:,.2f} {currency}** - **with** additional services
            - Δ delta = avg(Price with add. services)  - avg(Price without add. services)   
            - if Δ delta is **0** -> there was no additional service purchased in the category  
        """)

        st.dataframe(df_q4b_styled, hide_index=True, width="stretch")

        ''
        ''
        st.write(f"""
        - **Average price of additional services:**
            - count - no. of items having the type of service purchased
            - sum - sum of costs
            - average - average cost per item 
        """)
        st.dataframe(df_q4c_styled, hide_index=True, width="stretch")
    


    
    # ==== UI - Data Visualization ====
    ''
    ''
    ''
    ''
    st.write("##### Interactive table and charts:")

    # MAIN logic of filtering - Multiselects, Sliders, Filtering, Fallbacks. Including UI visualization
    df_filtered = get_filtered_df_including_ui_filters(data_table)

    # DF style formating prior data visualization - to have 2 decimals
    df_filtered_styled = df_styling(df_filtered)

    # Visualization of the table (where filters already applied)
    ''
    ''
    data_table_2 = st.dataframe(df_filtered_styled, hide_index=True, width="stretch")
    
    # Plotly chart
    with st.container(border=True):
        st.plotly_chart(create_pie_chart(df_filtered,"Product","Price", "Costs - ratio of product prices", False ))
     
    # Bar chart
    with st.container(border=True):
        st.plotly_chart(create_bar_chart(df_filtered,"Product","Price", "Bar chart - Costs - ratio of product prices"))


    # 15-June-25 - testuju
    # Bar chart 2 -  Price + Additional service price
    # It is important to have values in float!!! to be able to 'sum' them as part of visualizing in the chart
    data_bar_2 = ({
        "Product" : value_product_name_list,
        "Price" : value_price_list_float,  #float is must 
        "Category" : value_category_list, 
        "Additional service" : add_service_full, 
        "Additional service price" : add_ser_price_full_float #float is must 
    })

    ''
    ''
    ''
    st.write("##### Static Charts:")

    with st.container(border=True):
        st.plotly_chart(create_bar_chart(data_bar_2,"Product",["Price","Additional service price"], "Bar chart - Ratio of price including extra costs for additional services"))


    # v4.0 - new charts ---------------------------------------

    data_pie_2 = pd.DataFrame({
        "Costs" : [value_total_sum_fl,sum_adds_fl],
        "Costs name" : ["Sum price","Sum additional services"],
    })


    data_pie_3 = pd.DataFrame({
    "Costs" : [sum_pro_price_where_insurance,sum_price_insurance],
    "Costs named" : ["Costs products","Costs Insurance"],
    })


    data_pie_4 = pd.DataFrame({
    "Costs" : [sum_pro_price_where_ewarranty,sum_price_warranty],
    "Costs names" : ["Costs products","Costs warranty"],
    })

    # ==== UI - Data Visualization ====
    with st.container(border=True):
        st.plotly_chart(create_pie_chart(data_pie_2,"Costs name","Costs","How much additional services increase the costs", False))
        st.write(f"- Products costs: **{value_total_sum_fl:,.2f}** {currency}")
        st.write(f"- Additional services costs: **{sum_adds_fl:,.2f}** {currency}")
        st.write(f"- Summary:  **{(sum_adds_fl + value_total_sum_fl):,.2f}** {currency}")

    col1, col2 = st.columns(2)

    with col1.container(border=True):
        st.write(create_pie_chart(data_pie_3,"Costs named","Costs","Costs Extended warranty", False))
        st.write(f"- Products costs: **{sum_pro_price_where_insurance:,.2f}** {currency}")
        st.write(f"- The insurance: **{sum_price_insurance:,.2f}** {currency}")
        st.write(f"- Summary:  **{(sum_pro_price_where_insurance + sum_price_insurance):,.2f}** {currency}")


    with col2.container(border=True):
        st.write(create_pie_chart(data_pie_4, "Costs names", "Costs","Costs Extended warranty", False))
        st.write(f"- Products costs: **{sum_pro_price_where_ewarranty:,.2f}** {currency}")
        st.write(f"- The warranty: **{sum_price_warranty:,.2f}** {currency}")
        st.write(f"- Summary:  **{(sum_pro_price_where_ewarranty + sum_price_warranty):,.2f}** {currency}")
    
    #----------------------------------------------------------------------------

    # Time + creation of strings for .txt file
    full_date_outcome = get_utc_time_custom_string()

    final_outcome = (f"{full_date_outcome} | Validation: 1. {result_obj_outcome}, 2. {result_obj_outcome_services} | Receiver: {value_customer} | Price to pay (including extra services): {value_to_paid:,.2f} {currency}.")

    file_name_fstring = f"Summary-{value_invoice_num}.txt"



    # ===== UI Download txt file =====
    st.write("------")
    st.write("#### Download of .txt:")
    st.write('''A short summary of the original XML invoice, including result of validation, date and some of the parsed data.''')

    st.image("Pictures/V2_pictures/txt outcome_3.png")

    ''
    ''
    ''
    if st.download_button(
        "Download",
        data= final_outcome,
        file_name= file_name_fstring,
        icon = ":material/download:",
        width="stretch"):
            
        st.info("Download complete")
    
    st.write("-------")

    #Closing button   
    if st.button("Close Function 2", width="stretch", icon=":material/close:"):
        close_function()




