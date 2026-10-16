import streamlit as st
from Subpages.Resources import Assets
from Subpages.Resources_ui_objects import render_function_page, render_previous_page


st.write("# DB & ERD:")

''
tab1, tab2, tab3, tab4 = st.tabs([
    "DB layout",
    "Transport price",
    "Invoice",
    "Validation"
    ])  



with tab1:
    ''
    st.write("""
    - **DB landscape** which is used by **F3, F3B, F4** functions
    - Split into business logic segments
    """) 

    ''
    ''
    st.image("Pictures/Function_3/ERD/F3_F3B_F4_ERD_landscape_context_v5.svg")


with tab2:
    ''
    st.write("""
    - Used by **F3** to get **transport price** value **based on user inputs**
    """)
    ''
    st.image("Pictures/Function_3/ERD/F3_ERD_transport_price_v3.svg", width=600)
    ''

    currency = 'euro'
    c_code = 'cz'
    company = 'DHL'
    size = 'small'

    query = f"""
SELECT {currency} 

FROM shared.transport_company e
    INNER JOIN transport.country_{c_code} x ON (e.comp_id = x.c_comp_id)
    INNER JOIN shared.parcel_size f ON (x.size = f.size_id)
WHERE
    e.name = '{company}' AND
    f.name = '{size}'"""

    st.write("- Dynamic SQL query:")
    st.code(query, language="sql")

with tab3:
    ''
    st.write("""
    - **DB structure** for **invoice/data** created based on **user input**
    """) 
    
    st.write("""
    - **Functional intent:**
        - **F3** - Insert data (invoice) - WRITE
        - **F3B** - Visualize data (invoices) - READ
        - **F4** - Data validation & Insert log, if data transformation complete - WRITE
    """) 

    st.write("""
    - **F3** requires keeping of **order_id** reserved in DB until the process is finished → **sequence in PostgreSQL** set to **allow concurrency of users**.
    """)   
     
    ''
    st.image("Pictures/Function_3/ERD/F3_ERD_invoice_v7.svg")

    query_2 = """
SELECT 
    a.order_number as "Order no.",
    a.date as "Date",
    a.customer as "Customer",
    b.name as "Category",
    a.product_name as "Product",
    a.product_price as "Price",
    c.name as "Extra service",
    a.extra_service_price as "Extra service price",
    d.name as "Country",
    e.name as "Transport Company",
    a.transport_price as "Transport price",
    f.name as "Parcel size",
    a.total_sum as "Total price", 
    g.name as "Currency",
    h.name as "File format"                                            

FROM billing.invoice a
    INNER JOIN billing.category_list b ON (a.category = b.category_id)
    INNER JOIN billing.extra_service_list c ON (a.extra_service_type = c.service_id) 
    INNER JOIN billing.country_list d ON (a.country = d.country_id) 
    INNER JOIN shared.transport_company e ON (a.transport_company = e.comp_id) 
    INNER JOIN shared.parcel_size f ON (a.parcel_size = f.size_id) 
    INNER JOIN billing.currency_list g ON (a.currency = g.currency_id) 
    INNER JOIN billing.format_list h ON (a.file_format = h.format_id)

/*
-- JOIN for connecting 'change_log' table
    INNER JOIN billing.invoice a ON (a.order_number = i.order_number_log)
*/;"""


    ''
    st.write("- Visibility of relations through INNER JOIN:")
    st.code(query_2, language="sql")


with tab4:
    ''
    st.write("""
    - **Data-driven** logic used by **F3**
    - Identifying **unusual** user inputs -> the app displays **warnings** 
    """)

    ''
    st.image("Pictures/Function_3/ERD/F3_ERD_validations_v1.svg")


    ''
    ''
    tab1, tab2 = st.tabs([
        "Validation - Parcel size",
        "Validation - Product price"
    ])

    with tab1:
        st.image("Pictures/Function_3/ERD/F3_ERD_validation_detail_parcel_size_v1.svg")

    with tab2:
        st.image("Pictures/Function_3/ERD/F3_ERD_validation_detail_product_price_v1.svg")


# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

render_function_page(
	label= "Go to: Function 3",
	page= Assets.Paths.Function.f3,    
)

render_previous_page(
	page= Assets.Paths.Description.f3_f4_xml_json
)