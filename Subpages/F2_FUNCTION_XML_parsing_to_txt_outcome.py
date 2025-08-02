import streamlit as st
import xml.etree.ElementTree as ET
import time
import plotly.express as px
import pandas as pd
import math
import pandasql as ps
from lxml import etree



# ======= XSD not passed ======

def xsd_not_passed():

    ''
    ''
    st.error("The uploaded XML doesn't follow XSD rules -> the XML is not valid for this application")

    with st.expander(
        "Help",
        icon= ":material/help_outline:"
        ):

        ''
        st.write("- Please check the uploaded file")
        ''
        st.write("- Data issue/structure issue not following XSD/XML definition for this Function 2")
        ''
        ''
        st.write("**How to fix this?**")
        st.write("- **Either** you can use any of the **predefined files**:")
        ''
        st.link_button(
                    label = "Go to: Function 1",
                    url="https://dataparsing.streamlit.app/F1_FUNCTION_XML_dowload",
                    help="The button will redirect to the relevant page within this app.",
                    use_container_width=True,
                    icon=":material/launch:",
        ) 

        ''
        st.write("- **Or** you can see more about the XSD/XML definition for this Function 2 -> which should help to fix. **XSD** is at the bottom of the page")
        ''

        st.link_button(
                    label = "XML principles for this Function 2",
                    url="https://dataparsing.streamlit.app/F1_F2_description_XML_XSD",
                    help="The button will redirect to the relevant page within this app.",
                    use_container_width=True,
                    icon=":material/launch:",
                    )

    st.stop()



# ======= Function for validation uploaded XML against XSD =========

def validate(xml_path: str, xsd_path: str) -> bool:

        #try-except - for case when uploaded file is RECOGNIZED as XML (has suffux .xml) but the content is NOT XML. (If the try-except not here the script would jump to the very bottom of the script and raise the "something went wrong - report it as a bug" alert. But this is nto bug in the application, but file content issue)
        try:
            xmlschema_doc = etree.parse(xsd_path)
            xmlschema = etree.XMLSchema(xmlschema_doc)

            xml_doc = etree.parse(xml_path)
            result = xmlschema.validate(xml_doc)

            # variable 'result' returns True = valid or False = not valid - defined as 'bool' in the function header
            if result == True:
                pass

            else:
                xsd_not_passed()

        except:
            xsd_not_passed()

        


# //////////////////////////   OPENING SCREEN   //////////////////////////////////////////

# ======== Upload button to trigger the application ======================================

st.write("# Upload XML:")

# type = ".xml" - allows to upload only xml files
object_from_upload = st.file_uploader("", type=".xml")

if object_from_upload is None:
    st.info("When a file uploaded, the application will start")

    # (?) Help expander
    with st.expander(
                "Help",
                icon= ":material/help_outline:"
                ):

                ''
                ''
                st.write("**What file?**")
                st.write("- Only **XML** is allowed to be uploaded")
                st.write("- You can use any of the **predefined files**")

                st.link_button(
                    label = "Go to: Function 1",
                    url="https://dataparsing.streamlit.app/F1_FUNCTION_XML_dowload",
                    help="The button will redirect to the relevant page within this app.",
                    use_container_width=True,
                    icon=":material/launch:",
                    ) 
                ''
                ''
                st.write("-------")
                st.write("**Advanced approach:**")
                st.write("- If you know XML and XSD principles, you can try this")
                st.write("- The XML files can be **customized** or you can create **your own** following a template/structure")

                ''
                ''
                st.write("Steps:")
                st.write("""
                        1) Go to Function 1
                            - **Either** you can **customize** the predefines files 1), 2), 3)
                            - **Or** you can **create your own** from scratch. You can use template 4) for the beginning

                                            
                        """)
                st.link_button(
                    label = "Go to: Function 1",
                    url="https://dataparsing.streamlit.app/F1_FUNCTION_XML_dowload#4-xml-template",
                    help="The button will redirect to the relevant page within this app.",
                    use_container_width=True,
                    icon=":material/launch:",
                    ) 

                st.write("2) Download a XML file")
                st.write("3) Do/change/customize it how you like but **follow rules of XSD**")

                ''
                st.write("The rules of the XML and **XSD file** for download here:")

                st.link_button(
                    label = "XML principles for this Function 2",
                    url="https://dataparsing.streamlit.app/F1_F2_description_XML_XSD",
                    help="The button will redirect to the relevant page within this app.",
                    use_container_width=True,
                    icon=":material/launch:",
                    )


# //////////////////////////   LOGIC / SCRIPT AFTER FILE UPLOAD //////////////////////////////////

# The key logic of this application
if object_from_upload is not None:


    # try - Opening statement for the full parsing and visualization logic
    # Except - prevents the application from crashing
    try:


        validate(xml_path = object_from_upload, xsd_path ="F2_XSD_validation/XML_Schema_for_functions_1_and_2.xsd")
        
        # # Data import 
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
        
        # change of type from string to float
        value_price_list_fl = list(map(float, value_price_list))


        
        value_attribut = []
        for detail_id in root.findall('detail'):
            ids = detail_id.get('id')
            value_attribut.append(ids)

        value_attribute_int = list(map(int, value_attribut))
        max_value_attribut = max(value_attribute_int)
        

        # Logic for recognizing whether any extra money for 'extended warranty' or 'insurance' 
        warranty = []
        for service_type in root.findall('detail'):
            condition_service_type = service_type.find('additional_service/service_type').text

            if condition_service_type == 'extended warranty':
                service_price = service_type.find('additional_service/service_price').text
                warranty.append(service_price)
            
        warranty_float = list(map(float, warranty)) 
        sum_price_warranty = math.fsum(warranty_float)
        

        insurance = []
        for service_type in root.findall('detail'):
            condition_service_type = service_type.find('additional_service/service_type').text

            if condition_service_type == 'insurance':
                service_price = service_type.find('additional_service/service_price').text
                insurance.append(service_price)
            
        insurance_float = list(map(float, insurance)) 
        sum_price_insurance = math.fsum(insurance_float)

        #Extra parsing for charts
        # Type of additional service <additional_service> - Including 'None'
        add_service_full = []
        for add_ser_item in root.findall('detail'):
            add_service = add_ser_item.find('additional_service/service_type').text
            add_service = add_service.capitalize()
            add_service_full.append(add_service)

        # Prices full - including '0.00' for None values
        add_ser_price_full = []
        for service_type in root.findall('detail'):
            condition_service_type = service_type.find('additional_service/service_type').text

            # v5.3 - extended logic
            if condition_service_type == 'extended warranty':
                service_price = service_type.find('additional_service/service_price').text
                add_ser_price_full.append(service_price)

            if condition_service_type == 'insurance':
                service_price = service_type.find('additional_service/service_price').text
                add_ser_price_full.append(service_price)
            
            # v5.3 - specifically this part is important to not parse value in case that <service_type> 'none' but <service_price> 999.99 (with value) -> this is the anti-pattern which this mechanism prevents -> 
            # if 'None' it ignors a value but always appends 0.00 to this list
            if condition_service_type == 'None':
                add_ser_price_full.append(0.00)




        # Extra parsing for charts in SQL 3 expander  - NOT including add.services
        price_gaming = []
        for i_category in root.findall('detail'):
            condition = i_category.find('category').text
            if condition == 'Gaming':
                item = i_category.find('price_amount').text
                price_gaming.append(item)

        
        price_mobile_phone = []
        for i_category in root.findall('detail'):
            condition = i_category.find('category').text
            if condition == 'Mobile phones':
                item = i_category.find('price_amount').text
                price_mobile_phone.append(item)

        price_tablets = []
        for i_category in root.findall('detail'):
            condition = i_category.find('category').text
            if condition == 'Tablets':
                item = i_category.find('price_amount').text
                price_tablets.append(item)

        price_pc = []
        for i_category in root.findall('detail'):
            condition = i_category.find('category').text
            if condition == 'PC':
                item = i_category.find('price_amount').text
                price_pc.append(item)

        price_tv = []
        for i_category in root.findall('detail'):
            condition = i_category.find('category').text
            if condition == 'TV':
                item = i_category.find('price_amount').text
                price_tv.append(item)

        price_majapliances = []
        for i_category in root.findall('detail'):
            condition = i_category.find('category').text
            if condition == 'Major Appliances':
                item = i_category.find('price_amount').text
                price_majapliances.append(item)

        price_househol = []
        for i_category in root.findall('detail'):
            condition = i_category.find('category').text
            if condition == 'Households':
                item = i_category.find('price_amount').text
                price_househol.append(item)


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
        price_gaming_addserv = []
        for i_category in root.findall('detail'):
            condition = i_category.find('category').text
            if condition == 'Gaming':
                # This 'None' condition follows the rule to parse data from <additional_service> element specifically <additional_service>/<service_price> only in case that <additional_service>/<service> is NOT 'None
                item = i_category.find('additional_service/service_type').text
                if item != 'None':
                    item_2 = i_category.find('additional_service/service_price').text
                    price_gaming_addserv.append(item_2)

        
        price_mobphones_addserv = []
        for i_category in root.findall('detail'):
            condition = i_category.find('category').text
            if condition == 'Mobile phones':
                # This 'None' condition follows the rule to parse data from <additional_service> element specifically <additional_service>/<service_price> only in case that <additional_service>/<service> is NOT 'None
                item = i_category.find('additional_service/service_type').text
                if item != 'None':
                    item_2 = i_category.find('additional_service/service_price').text
                    price_mobphones_addserv.append(item_2)

        price_tablets_addserv = []
        for i_category in root.findall('detail'):
            condition = i_category.find('category').text
            if condition == 'Tablets':
                # This 'None' condition follows the rule to parse data from <additional_service> element specifically <additional_service>/<service_price> only in case that <additional_service>/<service> is NOT 'None
                item = i_category.find('additional_service/service_type').text
                if item != 'None':
                    item_2 = i_category.find('additional_service/service_price').text
                    price_tablets_addserv.append(item_2)

        price_pc_addserv = []
        for i_category in root.findall('detail'):
            condition = i_category.find('category').text
            if condition == 'PC':
                # This 'None' condition follows the rule to parse data from <additional_service> element specifically <additional_service>/<service_price> only in case that <additional_service>/<service> is NOT 'None
                item = i_category.find('additional_service/service_type').text
                if item != 'None':
                    item_2 = i_category.find('additional_service/service_price').text
                    price_pc_addserv.append(item_2)

        

        price_tv_addserv = []
        for i_category in root.findall('detail'):
            condition = i_category.find('category').text
            if condition == 'TV':
                # This 'None' condition follows the rule to parse data from <additional_service> element specifically <additional_service>/<service_price> only in case that <additional_service>/<service> is NOT 'None
                item = i_category.find('additional_service/service_type').text
                if item != 'None':
                    item_2 = i_category.find('additional_service/service_price').text
                    price_tv_addserv.append(item_2)


        price_majappl_addserv = []
        for i_category in root.findall('detail'):
            condition = i_category.find('category').text
            if condition == 'Major Appliances':
                # This 'None' condition follows the rule to parse data from <additional_service> element specifically <additional_service>/<service_price> only in case that <additional_service>/<service> is NOT 'None
                item = i_category.find('additional_service/service_type').text
                if item != 'None':
                    item_2 = i_category.find('additional_service/service_price').text
                    price_majappl_addserv.append(item_2)

        
        price_households_addserv = []
        for i_category in root.findall('detail'):
            condition = i_category.find('category').text
            if condition == 'Households':
                # This 'None' condition follows the rule to parse data from <additional_service> element specifically <additional_service>/<service_price> only in case that <additional_service>/<service> is NOT 'None
                item = i_category.find('additional_service/service_type').text
                if item != 'None':
                    item_2 = i_category.find('additional_service/service_price').text
                    price_households_addserv.append(item_2)


        # Type change from string to float
        price_gaming_addserv = list(map(float, price_gaming_addserv))
        price_mobphones_addserv = list(map(float, price_mobphones_addserv))
        price_tablets_addserv = list(map(float, price_tablets_addserv))
        price_pc_addserv = list(map(float, price_pc_addserv))
        price_tv_addserv = list(map(float, price_tv_addserv))
        price_majappl_addserv = list(map(float, price_majappl_addserv))
        price_households_addserv = list(map(float, price_households_addserv))

        # Sum of the list values
        sum_price_gaming_addserv = sum(price_gaming_addserv)
        sum_price_mobphones_addserv = sum(price_mobphones_addserv)
        sum_price_tablets_addserv = sum(price_tablets_addserv)
        sum_price_pc_addserv = sum(price_pc_addserv)
        sum_price_tv_addserv = sum(price_tv_addserv)
        sum_price_majappl_addserv = sum(price_majappl_addserv)
        sum_price_households_addserv = sum(price_households_addserv)

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
        pro_price_where_insurance = []
        for price_amount in root.findall('detail'):
            condition_service_type = price_amount.find('additional_service/service_type').text

            if condition_service_type == 'insurance':
                price_amount = price_amount.find('price_amount').text
                pro_price_where_insurance.append(price_amount)
            
        pro_price_where_insurance = list(map(float, pro_price_where_insurance)) 
        sum_pro_price_where_insurance = math.fsum(pro_price_where_insurance)


        pro_price_where_ewarranty = []
        for price_amount in root.findall('detail'):
            condition_service_type = price_amount.find('additional_service/service_type').text

            if condition_service_type == 'extended warranty':
                price_amount = price_amount.find('price_amount').text
                pro_price_where_ewarranty.append(price_amount)
            
        pro_price_where_ewarranty = list(map(float, pro_price_where_ewarranty)) 
        sum_pro_price_where_ewarranty = math.fsum(pro_price_where_ewarranty)

        # --------------------------------------------------------------------

        # Notification to appear on the screen when all parsing steps successfully done - at this point of teh script we know that the uploaded file is okay. Parsing of data done -> teh app can continue with next steps
        st.success("Upload complete")

        # ======= Application Function for validation of detail line sum matches header values============

        # <total_sum>
        result_validation = []
        def data_validation(value_total_sum, sum_price):
            result = value_total_sum - sum_price
            st.write("---------")
            st.write("#### Validation process")
            ''
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
    

        # Data validation - <total_sum_services> = value_total_sum_services Y/N 
        
        result_validation_services = []
        def data_validation_services(value_total_sum_services_fl, sum_price_warranty , sum_price_insurance):
            result = value_total_sum_services_fl - sum_price_warranty - sum_price_insurance
            sum_warranty_insurance = sum_price_warranty + sum_price_insurance
            st.write("2) ###### Validation process - Invoice sum services = sum of items in lines:")
            
            if result < 0 or result > 0:
                st.warning("Validation not passed - summary does not equeal to line values. You can either continue with existing file or adjust the input file and upload it again.")
                st.write(f"** Total sum of SERVICES in the XML invoice is: '{value_total_sum_services_fl:.2f}' but summary of prices in detail lines is '{sum_warranty_insurance:.2f}'.")
                outcome = ("Services - Not passed")
                result_validation_services.append(outcome)

            else:
                st.success("Validation passed")
                outcome = ("Services - Passed")
                result_validation_services.append(outcome)

        data_validation_services(value_total_sum_services_fl, sum_price_warranty , sum_price_insurance)

        result_obj_outcome_services = result_validation_services[0]


        ''
        ''
        with st.expander(
            "Help",
            icon= ":material/help_outline:"
            ):

            ''
            st.write("""
            - If validation **not passed**, it is because summary of either 1. or 2. (or both) are not matching with values in detail
            - This is an alert that some of the values visualized in the dashbords bellow will **not be correct**
            - More details on the data parsing and validation here:
            """)

            ''
            # st.page_link(
            #     label = "XML princpiles for this Function 2",
            #     page="Subpages/F1_F2_description_XML_XSD.py",
            #     help="The button will redirect to the relevant page within this app.",
            #     use_container_width=True,
            #     icon=":material/launch:",
            #     ) 

            st.link_button(
                label = "Go to XSD, XML description page",
                url="https://dataparsing.streamlit.app/F1_F2_description_XML_XSD",
                help="The button will redirect to the relevant page within this app for download.",
                use_container_width=True,
                icon=":material/launch:"
            )
            ''
            ''
            st.image("Pictures/Function_2/F2_validation_xml.png")


        # ========= Button to show values parsed and calculated ======================

        value_to_paid = value_total_sum + sum_price_warranty + sum_price_insurance

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

            # Number of items in each product category 
            q0a = """SELECT category, count(*) as 'count'
            FROM
                data_table_sql
            GROUP BY
                Category
            ORDER BY 
                count DESC, category ASC
            """


            st.write(f"- Number of items in **each product Category** (No. of items - {max_value_attribut}):")
            st.dataframe(ps.sqldf(q0a, locals()), hide_index=True, use_container_width=True)

            # Number of items with additional service
            q0b = """SELECT 
                Additional_service as 'Additional service',
                count(*) as 'count'
            FROM
                data_table_sql
            
            WHERE 
                Additional_service IS NOT 'None'
                
            GROUP BY
                Additional_service
            ORDER BY 
                count DESC
            """

            ''
            ''
            st.write("- Number of items having **additional services**:")
            st.dataframe(ps.sqldf(q0b, locals()), hide_index=True, use_container_width=True)

            # Number of items with  NO additional service = 'None'
            q0c = """SELECT
                Additional_service as 'Additional service',
                count(*) as 'count'
            FROM
                data_table_sql
            
            WHERE 
                Additional_service = 'None'
                
            GROUP BY
                Additional_service
            ORDER BY 
                count DESC
            """

            ''
            ''
            st.write("- Number of items **without** any additional service:")
            st.dataframe(ps.sqldf(q0c, locals()), hide_index=True, use_container_width=True)


        with st.expander("SQL Queries 2 - Prices/Costs", icon = ":material/view_list:"):
            ''
            ''
            st.write(f"- Currency: **{currency}**")
            ''
            '' 
            # The most expensive item
            q1 = """SELECT
                item_id as 'Item id',
                Product,
                Price, 
                Category, 
                Additional_service as 'Additional service',
                Additional_service_price as 'Additional service price'
            FROM
                data_table_sql
            ORDER BY
                Price DESC
            LIMIT 1"""
            

			# Data styling before visualization  -> 2 decimals
            style_q1 = ps.sqldf(q1, locals())
            style_q1 = style_q1.style.format({
                "Price":"{:,.2f}",
                "Additional service price":"{:,.2f}"  # here it works with the alias (AS) name
                })

			# Q1 visualization	
            st.write("- The **most expensive** item (Price):")
            st.dataframe(data=style_q1, hide_index=True, use_container_width=True)


            # The most expensive item including Additional service
            q2 = """SELECT
                item_id as 'Item id',
                Product,
                Price, 
                Category, 
                Additional_service as 'Additional service',
                Additional_service_price as 'Additional service price'
            FROM
                data_table_sql
            WHERE
                Additional_service = 'Extended warranty'
            ORDER BY
                Additional_service_price DESC
            LIMIT 1"""

            q2b = """SELECT
                item_id as 'Item id',
                Product,
                Price, 
                Category, 
                Additional_service as 'Additional service',
                Additional_service_price as 'Additional service price'
            FROM
                data_table_sql
            WHERE
                Additional_service = 'Insurance'
            ORDER BY
                Additional_service_price DESC
            LIMIT 1"""


			# Data styling before visualization  -> 2 decimals
            style_q2 = ps.sqldf(q2, locals())
            style_q2 = style_q2.style.format({
                "Price":"{:,.2f}",
                "Additional service price":"{:,.2f}"  # here it works with the alias (AS) name
                })

			# Data styling before visualization  -> 2 decimals
            style_q2b = ps.sqldf(q2b, locals())
            style_q2b = style_q2b.style.format({
                "Price":"{:,.2f}",
                "Additional service price":"{:,.2f}"  # here it works with the alias (AS) name
                })


			# Data visualization
            ''
            ''
            st.write("- The **most expensive additional service** (Extended warranty and Insurance):")
            st.dataframe(data=style_q2, hide_index=True, use_container_width=True)
            st.dataframe(data=style_q2b, hide_index=True, use_container_width=True)

            # The cheapest item
            q3 = """SELECT
                item_id as 'Item id',
                Product,
                Price, 
                Category, 
                Additional_service as 'Additional service',
                Additional_service_price as 'Additional service price'
            FROM
                data_table_sql
            ORDER BY
                (Price + 'Additional service price') ASC
            LIMIT 1"""
            
			# Data styling before visualization  -> 2 decimals
            style_q3 = ps.sqldf(q3, locals())
            style_q3 = style_q3.style.format({
                "Price":"{:,.2f}",
                "Additional service price":"{:,.2f}"  # here it works with the alias (AS) name
                })

			# Data visualization
            ''
            ''
            st.write("- The **cheapest** item (lowest Price):")
            st.dataframe(data=style_q3, hide_index=True, use_container_width=True)


            # The cheapest additional services
            q4 = """SELECT
                item_id as 'Item id',
                Product,
                Price, 
                Category, 
                Additional_service as 'Additional service',
                Additional_service_price as 'Additional service price'
            FROM
                data_table_sql
            WHERE
                Additional_service = 'Extended warranty'
            ORDER BY
                Additional_service_price ASC
            LIMIT 1"""

            q4b = """SELECT
                item_id as 'Item id',
                Product,
                Price, 
                Category, 
                Additional_service as 'Additional service',
                Additional_service_price as 'Additional service price'
            FROM
                data_table_sql
            WHERE
                Additional_service = 'Insurance'
            ORDER BY
                Additional_service_price ASC
            LIMIT 1"""
            
			# Data styling before visualization  -> 2 decimals
            style_q4 = ps.sqldf(q4, locals())
            style_q4 = style_q4.style.format({
                "Price":"{:,.2f}",
                "Additional service price":"{:,.2f}"  # here it works with the alias (AS) name
                })       


            style_q4b = ps.sqldf(q4b, locals())
            style_q4b = style_q4b.style.format({
                "Price":"{:,.2f}",
                "Additional service price":"{:,.2f}"  # here it works with the alias (AS) name
                })    

			# Visualization
            ''
            ''
            st.write("- The **cheapest additional service** (Extended warranty and Insurance):")
            st.dataframe(data= style_q4, hide_index=True, use_container_width=True)
            st.dataframe(data= style_q4b, hide_index=True, use_container_width=True)


        # Expander SQL 3 
        with st.expander("SQL Queries 3 & Pie Charts - % Ratio", icon = ":material/clock_loader_60:"):
            ''
            ''
            st.write(f"- Currency: **{currency}**")
            '' 
            st.write(f"- No. of items: **{max_value_attribut}**")
            '' 


            # Percentage % ratio of product prices per Category - NOT including additional services
            q5 = f"""SELECT
            	category,
                count(*) as 'count',
                sum(price) as 'sum price',
                round(((sum(price)/'{value_total_sum}')*100),2) as '% ratio'
            FROM
                data_table_sql
            GROUP BY
                Category
            ORDER BY 
                count DESC, category ASC""".format(value_total_sum)

			
			# Data styling before visualization  -> 2 decimals
            style_q5 = ps.sqldf(q5, locals())
            style_q5 = style_q5.style.format({
                "sum price":"{:,.2f}",
                "% ratio" : "{:.2f}"
                })

			# Data visualization
            st.write(f"- **(1) Percentage % ratio** of product costs per **Category**. From  total sum of products: **{value_total_sum:,.2f} {currency}** ")

            st.dataframe(data=style_q5, hide_index=True, use_container_width=True)
            

            # Data for chart -  Percentage % ratio of product prices per Category - NOT including additional services
            data_variable_dict = {
                "Item id" : value_attribut,
                "Product" : value_product_name_list,
                "Price" : value_price_list_fl, # must be float due to filtring in table    
                "Category" : value_category_list, 
                "Additional service" : add_service_full, 
                "Additional service price" : add_ser_price_full_float  # must be float due to filtring in table                
                }


            # Percentage % ratio of product prices per Category - INCLUDING additional services
            q5b = f"""SELECT
            	category,
				count(*) as 'count',
                sum(price+Additional_service_price) as 'sum price + add. services',
                round(((sum(price+Additional_service_price)/'{value_to_paid}')*100),2) as '% ratio'
            FROM
                data_table_sql
            GROUP BY
                Category
            ORDER BY 
                count DESC, category ASC""".format(value_to_paid)


			# Data styling before visualization  -> 2 decimals
            style_q5b = ps.sqldf(q5b, locals())
            style_q5b = style_q5b.style.format({
                "sum price + add. services":"{:,.2f}",
                "% ratio" : "{:.2f}"
                })


			# Data visualization
            ''
            st.write(f"- **(2) Percentage % ratio** of product prices per **Category**. From  total sum of products: **{value_to_paid:,.2f} {currency}**, **including** additional services **{sum_additional_serv:,.2f} {currency}**.")

            st.dataframe(data = style_q5b, hide_index=True, use_container_width=True)




            # Percentage % ratio of additional services per category
            q6 = f"""SELECT
            	category,
				count(*) as 'count',
                sum(Additional_service_price) as 'sum add. services',
                round(((sum(Additional_service_price)/'{sum_additional_serv}')*100),2) as '% ratio'
            FROM
                data_table_sql
            GROUP BY
                Category
            ORDER BY 
                count DESC, category ASC""".format(sum_additional_serv)
            

			# Data styling before visualization  -> 2 decimals
            style_q6 = ps.sqldf(q6, locals())
            style_q6 = style_q6.style.format({
                "sum add. services":"{:,.2f}",
                "% ratio" : "{:.2f}"
                })


			# Data visualization
            ''
            st.write(f"- **(3) Percentage % ratio** of **additional services** per Category (**{sum_additional_serv:,.2f} {currency}**)")

            st.dataframe(data=style_q6, hide_index=True, use_container_width=True)


         

            # Data frames for Charts in SQL 3 expander
            data_pie_sql3_1 = pd.DataFrame({

                "Costs" : [sum_price_gaming,
                           sum_price_mobile_phone,
                           sum_price_tablets,
                           sum_price_pc,
                           sum_price_tv,
                           sum_price_majapliances,
                           sum_price_househol
                           ],

                "Category" : ["Gaming",
                              "Mobile phones",
                              "Tablets",
                              "PC",
                              "TV",
                              "Major Appliances",
                              "Households"
                              ]

                })
            

            # Important logic, to drop() rows with 0 costs to do not appear in chart 
            index_0 = data_pie_sql3_1[ (data_pie_sql3_1['Costs'] == 0)].index
            data_pie_sql3_1.drop(index_0 , inplace=True)

            fig_pie_sql3_1 = px.pie(
                data_pie_sql3_1, 
                names = "Category",
                values = "Costs",
                title = "(1) Ratio of product costs per Category:"
                )
            
            # Adjustment to see 2 decimals always in the chart
            fig_pie_sql3_1.update_traces(texttemplate="%{percent:.2%}")
            
            data_pie_sql3_2 = pd.DataFrame({

                "Costs" : [sum_price_gaming_addserv,
                           sum_price_mobphones_addserv,
                           sum_price_tablets_addserv,
                           sum_price_pc_addserv,
                           sum_price_tv_addserv,
                           sum_price_majappl_addserv,
                           sum_price_households_addserv
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


            # Important logic, to drop() rows with 0 costs to do not appear in chart 
            index_0_2 = data_pie_sql3_2[ (data_pie_sql3_2['Costs'] == 0)].index
            data_pie_sql3_2.drop(index_0_2 , inplace=True)


            fig_pie_sql3_2 = px.pie(
                data_pie_sql3_2, 
                names = "Category",
                values = "Costs",
                title = "(3) Ratio of additional services per Category:"
                )
            
            # Adjustment to see 2 decimals always in the chart
            fig_pie_sql3_2.update_traces(texttemplate="%{percent:.2%}")


            data_pie_sql3_3 = pd.DataFrame({

                "Costs" : [ss_gaming,
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


            # Important logic, to drop() rows with 0 costs to do not appear in chart 
            index_0_3 = data_pie_sql3_3[ (data_pie_sql3_3['Costs'] == 0)].index
            data_pie_sql3_3.drop(index_0_3 , inplace=True)


            fig_pie_sql3_3 = px.pie(
                data_pie_sql3_3, 
                names = "Category",
                values = "Costs",
                title = "(2) ...including add. services:"
                )

            # Adjustment to see 2 decimals always in the chart
            fig_pie_sql3_3.update_traces(texttemplate="%{percent:.2%}")


            # Charts visualization
            ''
            ''
            col1, col2 = st.columns(2, gap="medium")


            col1.plotly_chart(fig_pie_sql3_1, use_container_width=True)
            col2.plotly_chart(fig_pie_sql3_3, use_container_width=True)
            col1.plotly_chart(fig_pie_sql3_2, use_container_width=True)


        # SQL 4
        with st.expander("SQL Queries 4 - Average", icon = ":material/view_list:"):
            ''
            ''
            st.write(f"- Currency: **{currency}**")
            '' 
            st.write("- Tables show values **only** if there is more than 1 item/product in specific category -> **no. of products > 1**")
            '' 
            ''

            # AVG Price without additional services
            q4_1 = """SELECT category,
                    count(Price) as 'count',
                    round(avg(Price), 2) as 'average price'
                FROM
                    data_table_sql
                GROUP BY
                    Category
                HAVING 
                    count(*) > 1
                ORDER BY 
                    category ASC
            """
            

			# Data styling before visualization  -> 2 decimals
            style_q4_1 = ps.sqldf(q4_1, locals())
            style_q4_1 = style_q4_1.style.format({
                "average price":"{:,.2f}",
                })

			# Data visualization
            st.write(f"- **Average price** in each product Category (Total price **{value_total_sum:,.2f} {currency}** - **without** additional services):")
            st.dataframe(data=style_q4_1, hide_index=True, use_container_width=True)



            # AVG Price WITH additional services
            q4_2 = """SELECT category,
                    count(*) as 'count',
                    round((sum(Price) + sum(Additional_service_price))/count(*), 2) as 'average price WITH add. services',
                    round(((sum(Price) + sum(Additional_service_price))/count(*) - avg(Price)), 2) as 'Δ delta'
                FROM
                    data_table_sql
                GROUP BY
                    Category
                HAVING 
                    count(*) > 1
                ORDER BY 
                    category ASC
            """
            
			# Data styling before visualization  -> 2 decimals
            style_q4_2 = ps.sqldf(q4_2, locals())
            style_q4_2 = style_q4_2.style.format({
                "average price WITH add. services":"{:,.2f}",
                "Δ delta" : "{:,.2f}"
                })

			# Data visualization
            ''
            ''
            st.write(f"""
            - **Average price including additional service price** in each product Category:
                - Total price **{value_to_paid:,.2f} {currency}** - **with** additional services
                - Δ delta = avg(Price with add. services)  - avg(Price without add. services)   
                - if Δ delta is **0** -> there was no additional service purchased in the category  
            
            """)

            st.dataframe(data=style_q4_2, hide_index=True, use_container_width=True)


            # AVG Price of additional services
            q4_3 = """SELECT Additional_service, 
                    count(*) as 'count',
                    sum(Additional_service_price) as 'sum',
                    round(sum(Additional_service_price)/count(*), 2) as 'average'
                FROM
                    data_table_sql
                WHERE 
                    Additional_service != 'None'
                GROUP BY
                    Additional_service
                ORDER BY
                    count(*) DESC
            """
            
			# Data styling before visualization  -> 2 decimals
            style_q4_3 = ps.sqldf(q4_3, locals())
            style_q4_3 = style_q4_3.style.format({
                "sum":"{:,.2f}",
                "average" : "{:,.2f}"
                })

            ''
            ''
            st.write(f"""
            - **Average price of additional services:**
                - count - no. of items having the type of service purchased
                - sum - sum of costs
                - average - average cost per item 
            """)
            st.dataframe(data = style_q4_3, hide_index=True, use_container_width=True)
        
        # ========= Data Visualization ====================
        ''
        ''
        ''
        ''
        st.write("##### Interactive table and charts:")


        # Creation of unique values from lists -> purpose: filters
        unique_value = data_table['Category'].unique()

        unique_add_ser = data_table['Additional service'].unique()

        # Creation of min and max values from lists to have start/end points of filters
        min_value_price = data_table['Price'].min()
        max_value_price = data_table['Price'].max()
        
        min_value_ads = data_table['Additional service price'].min()
        max_value_ads = data_table['Additional service price'].max()


    
        # Multiselect filter - Category
        ''

        filter_multiselect = st.multiselect(
            "Select Category",
            unique_value,
            default = unique_value,
            help = "Select category which you want to see. Multiple categories allowed"
        )  

       
        if not len(filter_multiselect):
            st.warning("Select at lease 1 category to see overview table and charts")


        
		# Slider - price 
        ''
        from_price, to_price = st.slider(
            "Filter Price",
            min_value = min_value_price,
            max_value = max_value_price,
            value= [min_value_price, max_value_price],
            step = 10.00,
            help = "Select range of prices you want to see"
        )



        # Multiselect filter - Additional service
        ''
        ''
        filter_multiselect_2 = st.multiselect(
            "Select Additional service",
			unique_add_ser,
            default= unique_add_ser,
            help = "Select additional service which you want to see. Multiple categories allowed"
            )

	
        if not len(filter_multiselect_2):
            st.warning("Select at lease 1 category to see overview table and charts")
            
		
        
		# Slider - price additional services
        ''
        from_price_ads, to_price_ads = st.slider(
            "Filter Price of Additional Services",
            min_value = min_value_ads,
            max_value = max_value_ads,
            value= [min_value_ads, max_value_ads],
            step = 5.00,
            help = "Select range of prices you want to see"
        )
        

      
        # Set of filters applied into the dataframe/table throught this part of code
        filtered_data = data_table[
        (data_table["Category"].isin(filter_multiselect)) & (data_table["Additional service"].isin(filter_multiselect_2))

        & ((data_table["Price"] <= to_price)
        & (data_table["Price"] >= from_price))

        & ((data_table["Additional service price"] <= to_price_ads)
        & (data_table["Additional service price"] >= from_price_ads))

        ]
        

		# DF style formating prior data visualization - to have 2 decimals
        df_filtered_styled = filtered_data.style.format({
            "Price": "{:,.2f}",
			"Additional service price": "{:,.2f}"
            })



        # Visualization of the table (where filters already applied)
        ''
        ''
        data_table_2 = st.dataframe(data=df_filtered_styled, hide_index=True, use_container_width=True)
        

        # Pie chart
        data = pd.DataFrame({
            "Product" : value_product_name_list,
            "Price" : value_price_list
            })


        fig_pie = px.pie(
            filtered_data, 
            names = "Product",
            values = "Price",
            title = "Costs - ratio of product prices"
            )

        # Adjustment to see 2 decimals always in the chart
        fig_pie.update_traces(texttemplate="%{percent:.2%}")

        with st.container(border=True):
            st.plotly_chart(fig_pie, use_container_width=True)
        

        
        # Bar chart
        fig_bar = px.bar(
            filtered_data, 
            x="Product",
            y="Price",
            title= "Bar chart - Costs - ratio of product prices",
            )

        with st.container(border=True):
            st.plotly_chart(fig_bar, use_container_width=True)


        # 15-June - testuju
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

        fig_bar_2 = px.bar(data_bar_2,
                x="Product",
                y=["Price","Additional service price"],
                title="Bar chart - Ratio of price including extra costs for additional services",
                )

        with st.container(border=True):
            st.plotly_chart(fig_bar_2, use_container_width=True)


        # v4.0 - new charts ---------------------------------------

        data_pie_2 = pd.DataFrame({

        "Costs" : [value_total_sum_fl,sum_adds_fl],
        "Costs name" : ["Sum price","Sum additional services"],

        })


        fig_pie_2 = px.pie(
            data_pie_2, 
            names = "Costs name",
            values = "Costs",
            title = "How much additional services increase the costs"
            )

        # Adjustment to see 2 decimals always in the chart
        fig_pie_2.update_traces(texttemplate="%{percent:.2%}")

        with st.container(border=True):
            st.plotly_chart(fig_pie_2, use_container_width=True)
            st.write(f"- Products costs: **{value_total_sum_fl:,.2f}** {currency}")
            st.write(f"- Additional services costs: **{sum_adds_fl:,.2f}** {currency}")
            st.write(f"- Summary:  **{(sum_adds_fl + value_total_sum_fl):,.2f}** {currency}")



        col1, col2 = st.columns(2)

        data_pie_3 = pd.DataFrame({

        "Costs" : [sum_pro_price_where_insurance,sum_price_insurance],
        "Costs named" : ["Costs products","Costs Insurance"],

        })

        fig_pie_3 = px.pie(
            data_pie_3, 
            names = "Costs named",
            values = "Costs",
            title = "Costs Insurance"
            )
        
        # Adjustment to see 2 decimals always in the chart
        fig_pie_3.update_traces(texttemplate="%{percent:.2%}")


        data_pie_4 = pd.DataFrame({

        "Costs" : [sum_pro_price_where_ewarranty,sum_price_warranty],
        "Costs names" : ["Costs products","Costs warranty"],

        })

        fig_pie_4 = px.pie(
            data_pie_4, 
            names = "Costs names",
            values = "Costs",
            title = "Costs Extended warranty"
            )  

        # Adjustment to see 2 decimals always in the chart
        fig_pie_4.update_traces(texttemplate="%{percent:.2%}")


        with col1.container(border=True):
                st.write(fig_pie_3)
                st.write(f"- Products costs: **{sum_pro_price_where_insurance:,.2f}** {currency}")
                st.write(f"- The insurance: **{sum_price_insurance:,.2f}** {currency}")
                st.write(f"- Summary:  **{(sum_pro_price_where_insurance + sum_price_insurance):,.2f}** {currency}")



        with col2.container(border=True):
            st.write(fig_pie_4)
            st.write(f"- Products costs: **{sum_pro_price_where_ewarranty:,.2f}** {currency}")
            st.write(f"- The warranty: **{sum_price_warranty:,.2f}** {currency}")
            st.write(f"- Summary:  **{(sum_pro_price_where_ewarranty + sum_price_warranty):,.2f}** {currency}")
        
        #----------------------------------------------------------------------------

        # Final outcome for print - using SERVER time
        st.write("------")
        st.write("#### Download of .txt:")
        st.write('''A short summary of the original XML invoice, including result of validation, date and some of the parsed data.''')

        st.image("Pictures/V2_pictures/txt outcome_3.png")


        # Time 
        time_objects = time.localtime()
        year, month, day, hour, minute, second, weekday, yearday, daylight = time_objects  

        date_custom = str("Date: %02d-%02d-%04d" % (day,month,year))
        time_custom = str("Time: %02d:%02d:%02d" % (hour,minute,second))
        day_custom = str(("Mon","Tue","Wed","Thu","Fri","Sat","Sun") [weekday])
        day_custom_2 = str("Day: "+ day_custom)
        full_date_outcome = str(date_custom +" | " + day_custom_2 +" | " + time_custom )

        final_outcome = (f"{full_date_outcome} | Validation: 1. {result_obj_outcome}, 2. {result_obj_outcome_services} | Receiver: {value_customer} | Price to pay (including extra services): {value_to_paid:,.2f} {currency}.")


        file_name_fstring = f"Summary-{value_invoice_num}.txt"

        ''
        ''
        ''
        if st.download_button(
            "Download",
            data= final_outcome,
            file_name= file_name_fstring,
            icon = ":material/download:",
            use_container_width=True):
                
            st.info("download will start in few seconds")
        
        st.write("-------")

        #Closing button/part of the app

        @st.dialog("Go to:")
        def process_done():

            ''
            st.page_link(
                label = "Function 3 - Description",
                page="Subpages/F3_F4_description.py",
                help="The button will redirect to the relevant page within this app.",
                use_container_width=True,
                icon=":material/code:",
                )

            st.page_link(
                label = "Function 3",
                page="Subpages/F3_FUNCTION_creation_of_XML.py",
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
            "Close Function 2",
            use_container_width= True,
            icon=":material/close:"
        ):
            process_done()

    # Except - prevents the application from error + providing extra info/help
    except:
        ''
        ''
        st.error("Something went wrong, please try again. If not working, please report it as a bug (on the main page).")

