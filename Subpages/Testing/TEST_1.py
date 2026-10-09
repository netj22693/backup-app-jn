import streamlit as st
import pandas as pd
from sqlalchemy import text
import logging
from app_logging import inicialization_logging
from app_db_connection import db_connection
from Subpages.SQL.F3_SQL_queries import F3InputDataQueries, sql_query_parcel_size, query_additional_service_price_info
from Subpages.Dialog.F3_dialog import dialog_not_possible_to_pull_data, F3ToastsValidations
from Subpages.Data.F3_F4_CDM_config_data import CDM_FIELDS
from Subpages.Services.F3_DB_mapping import MAPPING_FUNCTIONS, F3MappingFunctions
from Subpages.Services.F3_F4_CDM import transform_data_CDM_to_JSON, transform_data_CDM_to_XML, transform_data_CDM_to_CSV, transform_data_CDM_to_DB
from Subpages.Operational.F3_operational_functions import create_invoice_number, get_utc_time_custom_string, reset, get_transport_price, create_order_num, on_download_click, extract_data_additional_services, pull_data_and_transfer_to_list, get_transport_price_table, display_company_logo, F3ValueValidation


# ===== Inicialization for logging ===== 
inicialization_logging()
    

st.write("# Delivery details:")
''

# DB connection -> Engine
db_engine = db_connection("F3", True)

  
try:      
    with db_engine.connect() as conn:

        # Get options for the user form 
        category_options = pull_data_and_transfer_to_list(F3InputDataQueries.sql_query_category_options, conn)
        transport_company_options = pull_data_and_transfer_to_list(F3InputDataQueries.sql_query_transport_company_options, conn)
        currency_options = pull_data_and_transfer_to_list(F3InputDataQueries.sql_query_currency_options, conn)
        additional_service_options = pull_data_and_transfer_to_list(F3InputDataQueries.sql_query_additional_service_options, conn)
        country_options = pull_data_and_transfer_to_list(F3InputDataQueries.sql_query_country_options, conn)
        parcel_size_options = pull_data_and_transfer_to_list(F3InputDataQueries.sql_query_parcel_size_options, conn)

        # Get Price and Parcel size info tables 
        df_cz_dhl = get_transport_price_table(conn, "CZ", "DHL")
        df_cz_fedex = get_transport_price_table(conn, "CZ", "Fedex")
        df_sk_dhl = get_transport_price_table(conn, "SK", "DHL")
        df_sk_fedex = get_transport_price_table(conn, "SK", "Fedex")

        df_parcel_size = pd.read_sql_query(sql=text(sql_query_parcel_size), con=conn)

        # Get service df
        df_additional_service = pd.read_sql_query(sql=text(F3InputDataQueries.sql_query_additional_service_table), con=conn)
        df_additional_service_info = pd.read_sql_query(sql=text(query_additional_service_price_info), con=conn)



    logging.info(f"F3 - Pull data from DB - SUCCESS")

except Exception as e:
    logging.warning(f"F3 - Pull data from DB - FAIL - Exception: {e}")
    dialog_not_possible_to_pull_data()
    st.stop()


# ===== User form UI =====

placeholder_text = "Type..."
placeholder_select = "Select..."


with st.form(key="key_form"):

    st.write("Please provide details about order...")
    ''
    with st.container(border=True, width="stretch"):
        
        customer = st.text_input(
            ":material/tag_faces: Customer/Company name:",
            placeholder=placeholder_text,
            help= "Type a customer or company name",
            key= "key_customer"
            )

    with st.container(border=True, width="stretch"):

        icon=":material/devices:"

        category = st.selectbox(
            f"{icon} Category:" ,
            index = None,
            placeholder= placeholder_select,
            options= category_options,
            help= "Select one from the options",
            key= "key_category"
            )

        product_name = st.text_input(
            f"{icon} Product name:",
            placeholder=placeholder_text,
            help = "Type a product name",
            key= "key_product_name"
            )

    with st.container(border=True, width="stretch"):

        icon = ":material/euro_symbol:"
        currency = st.selectbox(
            f"{icon} Currency:" ,
            index = None,
            placeholder= placeholder_select,
            options= currency_options,
            help = "Select one from the options",
            key= "key_currency"
            )
        
        product_price = st.number_input(
            f"{icon} Product price:",
            min_value=0.00,
            step = 10.00,
            help = "You can either click on the +- icons or type the input using numbers. *The step is step +- 10.00 -> i case of diferent values in decimals type it.",
            key= "key_product_price"
            )

    with st.container(border=True, width="stretch"):

        icon = ":material/exposure_plus_1:"

        additional_service = st.selectbox(
            f"{icon} Additional service:" ,
            options= additional_service_options,
            help = "Select one of the options",
            key= "key_additional_service"
            )

        with st.expander("Service description", icon=":material/help:"):

            ''
            st.dataframe(
                df_additional_service_info,
                hide_index=True,
                column_config={
                    "service_description": None,
                    "icon": None
                },
            )

            # Note: "records" is one of the specific dict type the 'to_dict()' function can do 
            # orient: Literal['records']
            services = df_additional_service_info.to_dict("records")

            tab_names = []

            for s in services:
                tab_names.append(f'{s["icon"]} {s["Service"]}')

            
            tabs = st.tabs(tab_names)

            for tab, service in zip(tabs, services):
                with tab:
                    st.write(f'- {service["service_description"]}')

    with st.container(border=True, width="stretch"):

        icon_transport = ":material/directions_bus:"
        icon_parcel = ":material/box:"
        icon_pin = ":material/location_on:"

        country = st.selectbox(
            f"{icon_pin} Country:" ,
            options= country_options,
            index = None,
            placeholder= placeholder_select,
            help = "Select one of the options - there is different price for service for each country -> see the pricing table below.",
            key= "key_country"
            )
        
        transport_company = st.selectbox(
            f"{icon_transport} Transport company:" ,
            options= transport_company_options,
            index = None,
            placeholder= placeholder_select,
            help = "Select one of the options - there is different price for each company -> see the pricing table below.",
            key= "key_transport_company"
            )
        
        parcel_size = st.selectbox(
            f"{icon_parcel} Parcel size:" ,
            options=parcel_size_options,
            index = None,
            placeholder= placeholder_select,
            help = "Select one of the options",
            key= "key_parcel_size"        
            )
        ''
        ''

        with st.expander("Parcel size", icon=icon_parcel):

            ''
            st.image("Pictures/Function_3/F3_Parcel_sizes_v2.svg")

            ''
            st.dataframe(df_parcel_size, hide_index= True)



        with st.expander("Price list", icon=":material/help:"):

            tab1, tab2 = st.tabs([
                "CZ",
                "SK"
            ])

            FLAG_IMAGE_WIDTH = 40

            with tab1:
                st.image("Pictures/Function_3/Country_flags/Flag_of_the_Czech_Republic_v3.svg", width=FLAG_IMAGE_WIDTH)

                ''
                display_company_logo("DHL")
                st.dataframe(df_cz_dhl, hide_index=True)

                display_company_logo("Fedex")
                st.dataframe(df_cz_fedex, hide_index=True)

            with tab2:
                st.image("Pictures/Function_3/Country_flags/Flag_of_Slovakia_v3.svg", width=FLAG_IMAGE_WIDTH) 

                ''
                display_company_logo("DHL")
                st.dataframe(df_sk_dhl, hide_index=True)

                display_company_logo("Fedex")
                st.dataframe(df_sk_fedex, hide_index=True)


    ''
    ''
    ''
    submit_button = st.form_submit_button(
        "Submit",
        use_container_width=True,
        icon = ":material/apps:",
        )
''
''
if  submit_button:

    # Normalization
    customer = customer.strip()
    product_name = product_name.strip()
    product_price = round(product_price, 2)

    # Validation
    empty_strings = [
    customer,
    product_name,
    additional_service,
    ]

    none_values = [
    category,
    currency,
    country,
    transport_company,
    parcel_size,
    ]

    if (
        any(value == "" for value in empty_strings)
        or any(value is None for value in none_values)
        ):
            st.warning("Missing inputs -> please provide.")
            st.stop()

    if product_price == 0.00:
        st.warning("Missing Product price -> please provide.")
        st.stop()



    additional_service_label, additional_service_cost_percentage  = extract_data_additional_services(additional_service, df_additional_service)

    currency_query = F3MappingFunctions.mapping_currency_for_query(currency)

    country_table = F3MappingFunctions.mapping_country_to_table(country)

    order_number = create_order_num(db_engine)

    invoice_number = create_invoice_number(order_number)

    date = get_utc_time_custom_string("F3", "invoice")

    # Costs calculations
    transport_price = get_transport_price(db_engine, currency_query, country_table, parcel_size, transport_company)

    additional_service_price = round((product_price * (additional_service_cost_percentage/100)), 2)

    final_price = round((product_price + transport_price + additional_service_price), 2)

    # CDM structure creation
    cdm = {
        "order_number": order_number,
        "customer": customer,
        "invoice_number": invoice_number,
        "date": date,
        "total_sum": final_price,
        "currency": currency,
        "category": category,
        "product_name": product_name,
        "price_amount": product_price,
        "extra_service": F3MappingFunctions.mapping_additional_service_into_field(additional_service) ,
        "service_type": additional_service_label,
        "service_price": additional_service_price,
        "transporter": transport_company,
        "country": country,
        "size": parcel_size,
        "transport_price": transport_price,
    }
        # + "file_format": mapped_file_format - by which this is extended bellow, once one of download buttons pushed


    # ===== Validations of user input (in predefined range or not) =====
    validation_product_price = F3ValueValidation.validate_price(db_engine, product_price, category, currency)      

    validation_parcel_size = F3ValueValidation.validate_parcel_size(db_engine, category, parcel_size)    


    if validation_product_price is not None and validation_product_price["level"] != "N":

        F3ToastsValidations.display_product_price_attention_toast(validation_product_price['label'])

        attention_product = f":{validation_product_price['color']}-badge[:material/warning: {validation_product_price['label']}]"

    else:
        attention_product = ""


    if validation_parcel_size is not None:

        F3ToastsValidations.display_parcel_size_attention_toast(validation_parcel_size['label'])

        attention_parcel_size = f":{validation_parcel_size['color']}-badge[:material/warning: {validation_parcel_size['label']}]"

    else:
        attention_parcel_size = ""

    # ================= UI - DOWNLOAD + FINALIZATION OF THE PROCESS ===========
    st.write("#### Summary of your order:")

    ''
    with st.container(border=True):
        st.write(f" - Customer name: **{customer}**")
        st.write(f" - Order number: **{order_number}**")
        st.write(f" - Invoice number: **{invoice_number}**")
    ''
    with st.container(border=True):
        st.write(f" - Product name: **{product_name}**")
        st.write(f" - Category: **{category}**")
        st.markdown(f" - Price: **{product_price:,.2f} {currency}**{attention_product}")
        st.write(f" - Price for the extra service: **{additional_service_price:,.2f} {currency}** - Extra service: **{additional_service}** ")
    ''
    with st.container(border=True):
        display_company_logo(transport_company)
        st.write(f" - Price for transport: **{transport_price:,.2f} {currency}** - Transport company: **{transport_company}** - Country: **{country}**")
        st.markdown(f" - Parcel size: **{parcel_size}**  {attention_parcel_size}")
    
    ''
    with st.container(border=True):
        st.write(f"- Total price to pay: **{final_price:,.2f} {currency}**")


    ''
    ''
    st.info(f"""
    - **Download button**:
        - **CSV, JSON or XML** file will be created
        - Data will be stored into **DB** - Order number: **{order_number}**      
    """)

    st.info(f"""
    - **Change of inputs**:
        - Go up > Change data > Push **Submit button again** > Recalculation will happen
    """)
    
    
    ''
    st.write("###### Download:")  


    st.download_button(
        'Download - XML',
        transform_data_CDM_to_XML("F3", cdm, CDM_FIELDS),
        file_name=f"{invoice_number}.xml",
        use_container_width=True,
        icon=":material/download:",
        on_click=lambda: on_download_click(
            db_engine,
            "XML",
            transform_data_CDM_to_DB("F3", cdm, MAPPING_FUNCTIONS, CDM_FIELDS),
            order_number             
            )
    )

    
    st.download_button(
        'Download - JSON',
        transform_data_CDM_to_JSON("F3", cdm, CDM_FIELDS), 
        file_name = f"{invoice_number}.json",
        use_container_width=True,
        icon = ":material/download:",
        on_click=lambda: on_download_click(
            db_engine,
            "JSON",
            transform_data_CDM_to_DB("F3", cdm, MAPPING_FUNCTIONS, CDM_FIELDS),
            order_number 
            )
    )


    st.download_button(
        'Download - CSV',
        transform_data_CDM_to_CSV("F3", cdm), 
        file_name = f"{invoice_number}.csv",
        use_container_width=True,
        icon = ":material/download:",
        on_click=lambda: on_download_click(
            db_engine,
            "CSV",
            transform_data_CDM_to_DB("F3", cdm, MAPPING_FUNCTIONS, CDM_FIELDS),
            order_number 
            )
    )

                
("---------")
st.button(
    "Reset",
    use_container_width= True,
    on_click = reset,
    help = "It will clear the form",
    icon= ":material/delete:"
    )