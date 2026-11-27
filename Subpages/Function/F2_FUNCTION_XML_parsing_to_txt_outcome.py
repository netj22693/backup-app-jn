import streamlit as st
import pandas as pd
import math
import time
from Subpages.Resources_ui import UiConfigAndIcons
from Subpages.Resources_ui_objects import render_success_info
from Subpages.Data.F2_input_data import F2_UI_CONFIG
from Subpages.Dialog.F2_dialog import close_function_f2, display_f2_warning_toast
from Subpages.Universal.Universal_functions import display_df_index_hidden
from Subpages.Universal.Charts import create_pie_chart, create_bar_chart
from Subpages.Universal.Validation_XML_against_XML_Schema import validate_xml_against_xsd
from Subpages.Universal.XML_operations import get_xml_root, xml_data_parsing_find, xml_data_parsing_get, xml_data_parsing_find_conditional
from Subpages.Services.F2_UI_operations import initiate_session_state_f2, download_summary, display_interactive_table_and_charts
from Subpages.Expander.F2_expanders import show_expander_help, xsd_not_passed, show_expander_help_validation_process
from Subpages.Operational.F2_operational_functions import f2_xml_data_parsing_find_including_additional_services, df_styling, data_validation, data_validation_services, f2_xml_data_parsing_find_conditional_with_none_condition, get_utc_time_custom_string, get_warning_scenario, display_warning_f2, run_sql_query_df
from Subpages.SQL.F2_SQL_queries import get_sql_query_item_inc_add_service, get_sql_query_percentage_product_prices_category, get_sql_query_percentage_product_prices_category_inc_add_serv, get_sql_query_percentage_add_services, sql_query_no_items_product_category, sql_query_no_items_with_additional_service, sql_query_no_items_without_additional_service, sql_query_expensive_item, sql_query_cheapest_item, sql_query_avg_product_price, sql_query_avg_price_with_add_serv, sql_query_avg_price_of_add_serv



# ==== Session state ====
initiate_session_state_f2()

# ==== UI upload box ====

st.write("# Upload XML:")
''
''
''

upload = st.file_uploader(
    "Upload your XML file",
    type=".xml", 
    label_visibility="collapsed", accept_multiple_files=False,
    key=f"uploader_key_f2_{st.session_state.uploader_key_f2}"
    )


if upload is None:
    show_expander_help()


# ==== Main logic ====
if upload is not None:

    # st.empty used because before upload there is Help expander displayed. 
    # When upload done, st.empty() helps to clean up the UI (the expander) and replace it quickly by the spinner
    st.empty()

    with st.spinner(F2_UI_CONFIG["schema_validation"]["spinner"]):
        time.sleep(F2_UI_CONFIG["time_sleep"])

    # Validation XML against XSD
    validation_result = validate_xml_against_xsd(
        "F2",
        upload,
        "Subpages/Data/F2_XML_Schema_v1.xsd"
        )

    if validation_result == False:
        xsd_not_passed()
    

    root = get_xml_root(upload)

    #  ==== DATA PARSING FROM HEADER LEVEL XML ==== 
    data_header = {
        "customer": xml_data_parsing_find(root,'header','customer', False, False),
        "invoice_number": xml_data_parsing_find(root,'header','invoice_number', False, False),
        "date": xml_data_parsing_find(root,'header','date', False, False),
        "currency": xml_data_parsing_find(root,'header','price/currency', False, False),
        "total_sum": xml_data_parsing_find(root,'header','price/total_sum', True, False),
        "total_sum_services": xml_data_parsing_find(root,'header','price/total_sum_services', True, False)
    }
    
    #  ==== DATA PARSING FROM DETAIL LEVEL XML ====   
    data_detail = {

        "list" : {
            "category": xml_data_parsing_find(root,'detail','category', False, True),
            "product_name": xml_data_parsing_find(root,'detail','product_name', False, True),
            "product_price": xml_data_parsing_find(root,'detail','price_amount', True, True),
            "attribute": list(map(int, xml_data_parsing_get(root,'detail', 'id'))),

            # Type of additional service <additional_service> - Including 'None'
            "additional_service_all": list(map(
                str.capitalize,
                xml_data_parsing_find(root,'detail','additional_service/service_type', False, True)
            )),

            # Price including '0.00' for None values
            "price_including_zero": list(map(
                float,
                f2_xml_data_parsing_find_conditional_with_none_condition(root,'detail','additional_service/service_type')
                )
            )
        },

        "sum": {
            "product_price": math.fsum(
                xml_data_parsing_find(root,'detail','price_amount', True, True)
            ),           

            "additional_services": {
                "warranty": math.fsum(
                    xml_data_parsing_find_conditional(root,'detail','additional_service/service_type', 'extended warranty', 'additional_service/service_price', True)
                ),

                "insurance": math.fsum(
                    xml_data_parsing_find_conditional(root,'detail','additional_service/service_type', 'insurance', 'additional_service/service_price', True) 
                ),
            },

            # SQL 3 expander  - NOT including add.services
            "category": {
                "gaming": sum(
                    xml_data_parsing_find_conditional(root,'detail','category','Gaming','price_amount', True)
                    ),
                "mobile_phones": sum(
                    xml_data_parsing_find_conditional(root,'detail','category','Mobile phones','price_amount', True)
                    ),
                "tablets": sum(
                    xml_data_parsing_find_conditional(root,'detail','category','Tablets','price_amount', True)
                    ),      
                "pc": sum(
                    xml_data_parsing_find_conditional(root,'detail','category','PC','price_amount', True)
                    ),     
                "tv": sum(
                    xml_data_parsing_find_conditional(root,'detail','category','TV','price_amount', True)
                    ),     
                "major_appliances": sum(
                    xml_data_parsing_find_conditional(root,'detail','category','Major Appliances','price_amount', True)
                    ),   
                "households": sum(
                    xml_data_parsing_find_conditional(root,'detail','category','Households','price_amount', True)
                    )
                },

            # SQL 3 expander  - INCLUDING add. services
            "category_having_add_services": {
                "gaming": f2_xml_data_parsing_find_including_additional_services(root,'detail','category','Gaming', 'additional_service/service_type', 'additional_service/service_price'),

                "mobile_phones": f2_xml_data_parsing_find_including_additional_services(root,'detail','category','Mobile phones','additional_service/service_type', 'additional_service/service_price'),

                "tablets": f2_xml_data_parsing_find_including_additional_services(root,'detail','category','Tablets','additional_service/service_type', 'additional_service/service_price'),

                "pc": f2_xml_data_parsing_find_including_additional_services(root,'detail','category','PC','additional_service/service_type', 'additional_service/service_price'),      
                
                "tv": f2_xml_data_parsing_find_including_additional_services(root,'detail','category','TV','additional_service/service_type', 'additional_service/service_price'),    

                "major_appliances": f2_xml_data_parsing_find_including_additional_services(root,'detail','category','Major Appliances','additional_service/service_type', 'additional_service/service_price'),  

                "households": f2_xml_data_parsing_find_including_additional_services(root,'detail','category','Households','additional_service/service_type', 'additional_service/service_price'),  
            },

            # Sum of products having additional service
            "product_having": {
                "insurance": math.fsum(
                xml_data_parsing_find_conditional(root,'detail','additional_service/service_type', 'insurance', 'price_amount', True)
                ),

                "warranty": math.fsum(
                xml_data_parsing_find_conditional(root,'detail','additional_service/service_type', 'extended warranty', 'price_amount', True)           
                )
            }
            
        }
    }

    # ===== Split into variables or smaller objects =====

    # From header
    currency: str = data_header["currency"]

    total_sum: float = data_header["total_sum"]

    total_sum_services: float = data_header["total_sum_services"]

    # From detail
    sum_warranty: float = data_detail["sum"]["additional_services"]["warranty"]

    sum_insurance: float = data_detail["sum"]["additional_services"]["insurance"]

    sum_product_price: float = data_detail["sum"]["product_price"]

    number_products: int  = len(data_detail["list"]["attribute"])

    sum_product_having_insurance: float = data_detail["sum"]["product_having"]["insurance"]

    sum_product_having_warranty: float = data_detail["sum"]["product_having"]["warranty"]

    # Logical objects from detail
    category: dict = data_detail["sum"]["category"]

    category_having_services: dict = data_detail["sum"]["category_having_add_services"]

    detail_list: dict = data_detail["list"]

    # Calculated variable
    to_pay: float = total_sum + total_sum_services

    sum_services: float = sum_warranty + sum_insurance



    # ===== Validations =====

    render_success_info("Upload complete")

    st.write("---------")
    st.write("#### Validation process")
    ''
    st.write("1) ###### Validation process")

    with st.spinner(F2_UI_CONFIG["invoice_validation_total_sum"]["spinner"]):
        time.sleep(F2_UI_CONFIG["time_sleep"])

    validation_price_text, v1 = data_validation(
        total_sum, 
        sum_product_price,
        currency
        )
  
    ''
    st.write("2) ###### Validation process")

    with st.spinner(F2_UI_CONFIG["invoice_validation_total_sum_services"]["spinner"]):
        time.sleep(F2_UI_CONFIG["time_sleep"])

    validation_price_services_text, v2 = data_validation_services(
        total_sum_services,
        sum_services,
        currency
        )


    scenario = get_warning_scenario(v1, v2)

    # to_pay
    w1_badge, w1_warning_text, w1_result = display_warning_f2(
        scenario,
        ["V2_ONLY","V1_ONLY","BOTH"],
        {
            "t1": "the **% ratio** column is impacted"
        }
        )

    # total_sum_services
    w2_badge, w2_warning_text, w2_result = display_warning_f2(
        scenario,
        ["V2_ONLY","BOTH"],
        {
            "t1": "the **% ratio** column is impacted",
            "t2": "The chart is based on incorrect data"
        }
        )

    # total_sum
    w3_badge, w3_warning_text, w3_result = display_warning_f2(
        scenario,
        ["V1_ONLY", "BOTH"],
        {
            "t1": "the **% ratio** column is impacted",
            "t2": "The chart is based on incorrect data"
        }
        )


    # Data to DFs
    # Note: *must be float due to filtring

    # 1) Not editable table
    df = pd.DataFrame({
        "Item id" : detail_list["attribute"],
        "Product" : detail_list["product_name"],
        "Price" : detail_list["product_price"], # *float    
        "Category" : detail_list["category"], 
        "Additional service" : detail_list["additional_service_all"], 
        "Additional service price" : detail_list["price_including_zero"]  # *float           
        })

    # 2) Table for SQL queries
    df_sql = pd.DataFrame({
        "Item_id" : detail_list["attribute"],
        "Product" : detail_list["product_name"],
        "Price" : detail_list["product_price"], # *float    
        "Category" : detail_list["category"], 
        "Additional_service" : detail_list["additional_service_all"], 
        "Additional_service_price" : detail_list["price_including_zero"]  # *float              
        })


    # ==== UI ====
    ''
    ''
    with st.expander("Help",icon=UiConfigAndIcons.Expanders.help_additional_info):
        show_expander_help_validation_process()


    
    st.write("------")
    st.write("#### Data Visualization")
    ''
    ''
    with st.expander("Summary overview - Invoice", icon=UiConfigAndIcons.Expanders.list):
        '' 
        st.write(f"**Sumary:**")
        st.write(f" - Invoice number: **{data_header['invoice_number']}**")
        st.write(f" - Customer: **{data_header['customer']}**")
        st.write(f" - Invoice created (YYYY-MM-DD): **{data_header['date']}**")

        st.write(f" - Overall costs: **{to_pay:,.2f} {currency}** {w1_badge}")
        st.write(f" - Number of products: **{number_products}**")
        ''
        ''
        ''
        st.write(f"**Detail:**")
        st.write(f" - Sum of products: **{sum_product_price:,.2f} {currency}**")

        st.write(f" - Sum of additional services: **{sum_services:,.2f} {currency}**")
        st.write(f" - Extended warranty: **{sum_warranty:,.2f} {currency}**")
        st.write(f" - Insurance: **{sum_insurance:,.2f} {currency}**")
        ''
        ''

    with st.expander("SQL Queries 1 - Overview", icon=UiConfigAndIcons.Expanders.table):
        '' 
        st.write(f"- Items in **each product Category** (Total: {number_products}):")
        display_df_index_hidden(
            run_sql_query_df(
                sql_query_no_items_product_category,
                df_sql
                )
            )

        ''
        st.write("- Items having **additional services**:")
        display_df_index_hidden(
            run_sql_query_df(
                sql_query_no_items_with_additional_service,
                df_sql
                )
            )

        ''
        st.write("- Items **without** additional service:")
        display_df_index_hidden(
            run_sql_query_df(
                sql_query_no_items_without_additional_service,
                df_sql
                )
            )

    with st.expander("SQL Queries 2 - Prices/Costs", icon=UiConfigAndIcons.Expanders.table):

        # DF styling -> 2 decimals       
        df_expensive = df_styling(
            run_sql_query_df(
                sql_query_expensive_item,
                df_sql
                )
            )

        df_expensive_warranty = df_styling(
            run_sql_query_df(
                get_sql_query_item_inc_add_service('Extended warranty', 'DESC'),
                df_sql
                )
            )

        df_expensive_insurance = df_styling(
            run_sql_query_df(
                get_sql_query_item_inc_add_service('Insurance', 'DESC'),
                df_sql
                )
            )

        df_cheapest = df_styling(
            run_sql_query_df(
                sql_query_cheapest_item,
                df_sql
                )
            )

        df_cheapest_warranty = df_styling(
            run_sql_query_df(
                get_sql_query_item_inc_add_service('Extended warranty', 'ASC'),
                df_sql
                )
            )

        df_cheapest_insurance = df_styling(
            run_sql_query_df(
                get_sql_query_item_inc_add_service('Insurance', 'ASC'),
                df_sql
                )
            )

        # === UI - Data visualization ====
        ''
        st.write(f"- Currency: **{currency}**")
        ''  
        st.write("- The **most expensive** item (Price):")
        display_df_index_hidden(df_expensive)
        ''
        st.write("- The **most expensive additional service**:")
        display_df_index_hidden(df_expensive_warranty)
        display_df_index_hidden(df_expensive_insurance)
        ''
        st.write("- The **cheapest** item (Price):")
        display_df_index_hidden(df_cheapest)
        ''
        st.write("- The **cheapest additional service**:")
        display_df_index_hidden(df_cheapest_warranty)
        display_df_index_hidden(df_cheapest_insurance)


    with st.expander("SQL Queries 3 & Pie Charts - % Ratio", icon=UiConfigAndIcons.Expanders.pie_chart):

        # DF styling -> 2 decimals
        df_ratio_category = df_styling(
            run_sql_query_df(
                get_sql_query_percentage_product_prices_category(total_sum),
                df_sql
            )
        )

        df_ratio_category_with_services = df_styling(
            run_sql_query_df(
                get_sql_query_percentage_product_prices_category_inc_add_serv(to_pay),
                df_sql
            )
        )

        df_ratio_services_per_category = df_styling(
            run_sql_query_df(
                get_sql_query_percentage_add_services(total_sum_services),
                df_sql
            )
        )

        # DFs for charts
        df_ratio_category_pie = pd.DataFrame({
            "Costs": [
                category["gaming"],
                category["households"],
                category["major_appliances"],
                category["mobile_phones"],
                category["pc"],
                category["tablets"],
                category["tv"]
            ],
            "Category": [
                "Gaming",
                "Households",
                "Major Appliances",
                "Mobile phones",
                "PC",
                "Tablets",
                "TV"
            ]
        })

        df_ratio_category_with_services_pie = pd.DataFrame({
            "Costs": [
                category_having_services["gaming"],
                category_having_services["households"],
                category_having_services["major_appliances"],
                category_having_services["mobile_phones"],
                category_having_services["pc"],
                category_having_services["tablets"],
                category_having_services["tv"]
            ],
            "Category": [
                "Gaming",
                "Households",
                "Major Appliances",
                "Mobile phones",
                "PC",
                "Tablets",
                "TV"
            ]
        })

        df_ratio_services_per_category_pie = pd.DataFrame({
            "Costs": [
                category["gaming"] + category_having_services["gaming"],
                category["households"] + category_having_services["households"],
                category["major_appliances"] + category_having_services["major_appliances"],
                category["mobile_phones"] + category_having_services["mobile_phones"],
                category["pc"] + category_having_services["pc"],
                category["tablets"] + category_having_services["tablets"],
                category["tv"] + category_having_services["tv"]
            ],
            "Category": [
                "Gaming",
                "Households",
                "Major Appliances",
                "Mobile phones",
                "PC",
                "Tablets",
                "TV"
            ]
        })


        
        # ==== UI - Data visualization ====
        ''
        st.write(f"- Currency: **{currency}**")
        '' 
        st.write(f"- No. of items: **{number_products}**")

        '' 
        st.write(f"- **(1) Percentage % ratio** - product price per **Category**. Sum: **{total_sum:,.2f} {currency}**{w3_badge}")

        # Warning logic
        if w3_result:
            if w3_warning_text:
                st.write(w3_warning_text["t1"])

        display_df_index_hidden(df_ratio_category)

        ''
        st.write(f"- **(2) Percentage % ratio** - product price per **Category**. Sum: **{to_pay:,.2f} {currency}**{w1_badge}, **including** additional services **{total_sum_services:,.2f} {currency}**. {w2_badge}")

        # Warning logic
        if w1_result:
            if w1_warning_text:
                st.write(w1_warning_text["t1"])

        display_df_index_hidden(df_ratio_category_with_services)

        ''
        st.write(f"- **(3) Percentage % ratio** of **additional services** per **Category**. Sum: **{total_sum_services:,.2f} {currency}**{w2_badge}")

        # Warning logic
        if w2_result:
            if w2_warning_text:
                st.write(w2_warning_text["t1"])        

        display_df_index_hidden(df_ratio_services_per_category)   

        ''
        ''
        col1, col2 = st.columns(2, gap="medium")

        col1.plotly_chart(
            create_pie_chart(
                df_ratio_category_pie,
                "Category",
                "Costs",
                "(1) Ratio of product costs per Category:",
                True,
                "Costs"
                )
            )
        
        col2.plotly_chart(
            create_pie_chart(
                df_ratio_services_per_category_pie,
                "Category",
                "Costs",
                "(2) ...including add. services:",
                True,
                "Costs"
                )
            )

        col1.plotly_chart(
            create_pie_chart(
                df_ratio_category_with_services_pie,
                "Category",
                "Costs",
                "(3) Ratio of additional services per Category:",
                True,
                "Costs"
                )
            )


    with st.expander("SQL Queries 4 - Average", icon=UiConfigAndIcons.Expanders.table):

        # DF styling -> 2 decimals
        df_avg_product_price = df_styling(
            run_sql_query_df(
                sql_query_avg_product_price,
                df_sql
                )
            )

        df_avg_price_incl_services = df_styling(
            run_sql_query_df(
                sql_query_avg_price_with_add_serv,
                df_sql
            )
        )
       
        df_avg_price_service = df_styling(
            run_sql_query_df(
                sql_query_avg_price_of_add_serv,
                df_sql
            )
        )

        # ===== UI =====
        ''
        st.write(f"- Currency: **{currency}**")
        '' 
        st.write("- Value visible **only** if there is more than 1 product in category (**no. of products > 1**)")
        '' 
        st.write(f"- **Average product price** per Category:")

        display_df_index_hidden(df_avg_product_price)

        ''
        st.write(f"""
        - **Average product price including additional service** per Category:
            - Δ delta = avg(Price with add. services)  - avg(Price without add. services)   
            - Δ delta **0.00** -> No additional service in the category  
        """)

        display_df_index_hidden(df_avg_price_incl_services)

        ''
        st.write(f"""
        - **Average price of additional services:**
            - Count - items having the service
            - Sum - sum of costs
            - Avg - average cost per item 
        """)
        display_df_index_hidden(df_avg_price_service)
    


    
    # ==== UI ====
    ''
    ''
    ''
    ''
    st.write("##### Interactive table and charts:")

    # The full filtering logic
    display_interactive_table_and_charts(df)


    ''
    ''
    ''
    st.write("##### Static Charts:")

    icon_p = UiConfigAndIcons.UnifiedIcons.pie_chart
    icon_b = UiConfigAndIcons.UnifiedIcons.bar_chart

    tab1, tab2, tab3 = st.tabs([
        f"{icon_b} Cost increase additional services",
        f"{icon_p} Ratio - cost increase additional services",
        f"{icon_p} Ratio - cost increase additional services - split"
    ])

    with tab1:
        st.plotly_chart(
            create_bar_chart(
                df,
                "Product",
                ["Price","Additional service price"],
                )
            )

    cost_ratio_overall = pd.DataFrame({
        "Costs" : [
            total_sum,
            total_sum_services
            ],
        "Costs name" : [
            "Product price",
            "Additional services"
            ]
        })

    cost_ratio_insurance = pd.DataFrame({
        "Costs" : [
            sum_product_having_insurance,
            sum_insurance
            ],
        "Costs name" : [
            "Product price",
            "Insurance"
            ]
        })

    cost_ratio_warranty = pd.DataFrame({
        "Costs" : [
            sum_product_having_warranty,
            sum_warranty
            ],
        "Costs name" : [
            "Product price",
            "Warranty"
            ]
        })

    # ===== UI =====
    with tab2:

        if w2_result and w3_result:
            if w2_warning_text:
                st.write(w2_warning_text["t2"])
        else:
            if w2_result:
                if w2_warning_text:
                    st.write(w2_warning_text["t2"])

            if w3_result:
                if w3_warning_text:
                    st.write(w3_warning_text["t2"])

        st.plotly_chart(
            create_pie_chart(
                cost_ratio_overall,
                "Costs name",
                "Costs"
                )
            )

        st.write(f"- Products costs: **{total_sum:,.2f}** {currency} {w3_badge}")
        st.write(f"- Additional services costs: **{total_sum_services:,.2f}** {currency} {w2_badge}")
        st.write(f"- Sum:  **{to_pay:,.2f}** {currency} {w1_badge}")

    with tab3:

        col1, col2 = st.columns(2)

        col1.plotly_chart(
            create_pie_chart(
                cost_ratio_insurance,
                "Costs name",
                "Costs",
                False
                )
            )
        
        col1.write(f"- Products costs: **{sum_product_having_insurance:,.2f}** {currency}")
        col1.write(f"- Insurance: **{sum_insurance:,.2f}** {currency}")
        col1.write(f"- Sum:  **{(sum_product_having_insurance + sum_insurance):,.2f}** {currency}")


        col2.plotly_chart(
            create_pie_chart(
                cost_ratio_warranty,
                "Costs name",
                "Costs",
                False
                )
            )
        
        col2.write(f"- Products costs: **{sum_product_having_warranty:,.2f}** {currency}")
        col2.write(f"- Warranty: **{sum_warranty:,.2f}** {currency}")
        col2.write(f"- Sum:  **{(sum_product_having_warranty + sum_warranty):,.2f}** {currency}")

    st.write("------")

    
    # ===== Summary file =====

    date_string: str = get_utc_time_custom_string()

    # change to UTF-8 symbol
    if w1_result:
        w1_badge = " ⚠︎"

    summary = (f"{date_string} | Validation: 1. {validation_price_text}, 2. {validation_price_services_text} | Customer: {data_header['customer']} | Overall costs: {to_pay:,.2f} {currency}{w1_badge}.")

    file_name = f"Summary-{data_header['invoice_number']}.txt"

    # Download .txt
    download_summary(
        summary,
        file_name
    )


    # Warning toast based on the validation (at the end of the script for smooth UX feeling)
    if scenario != "NONE":
        display_f2_warning_toast()


    st.write("-------")
    st.button(
        "Close Function 2",
        width="stretch",
        icon=UiConfigAndIcons.Buttons.close,
        on_click = close_function_f2           
        )