import streamlit as st


st.write("# DB & ERD:")

''
tab_erd_1, tab_erd_2, tab_erd_3 = st.tabs([
    "DB ERD - DB landscape",
    "DB ERD - Transport price",
    "DB ERD - Invoice"
    ])  



with tab_erd_1:
    ''
    st.write("""
        - **DB landscape** which is used by **F3, F3B, F4** functions
        """) 

    st.write("""
        - F3 - Transport price segment - READ
        - F3 - Invoice segment - WRITE
        - F3B - Invoice segment - READ & Data visualization
        - F4 - Invoice segment - WRITE
        """) 

    ''
    ''
    st.image("Pictures/Function_3/F3_F3B_F4_ERD_landscape_context_v2.svg")


with tab_erd_2:
    ''
    st.write("""
    - **DB structure** used by **Function 3** - READ
    - To get **transport price** value **based on user inputs**
    """)
    ''
    st.image("Pictures/Function_3/F3_ERD_transport_price_v2.svg")
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

with tab_erd_3:
    ''
    st.write("""
        - **DB structure** for **invoice/data** created based on **user input**
        """) 
    
    st.write("""
        - **Functional intent:**
            - **Function 3** - Inserts data (invoice) - WRITE
            - **Function 3B** - Visualizes data (invoices) - READ
            - **Function 4** - Insert logs if mapping made - WRITE
        """) 

    st.write("""
        - **Process**:
            - User provides inputs about purchase (F3 screen) -> file invoice created - XML or JSON (F3) -> **data inserted into DB** (F3) -> data visualized based on the DB (F3B)
            - User takes the invoice (from F3) -> uploaded for file format change (F4) -> this **change is logged** and **inserted into DB** (F4) -> this change can be visualized based on the DB (F3B)
        """)     

    st.write("""
        - The DB is designed to be **scalable** in case of growth of options in the future
        """)    
    ''
    st.image("Pictures/Function_3/F3_ERD_invoice_v4.svg")

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
    a.tr_price as "Transport price",
    f.name as "Parcel size",
    a.total_price as "Total price", 
    g.name as "Currency",
    h.name as "File format"                                            

FROM billing.invoice a
    INNER JOIN billing.category_list b ON (a.category = b.category_id)
    INNER JOIN billing.extra_service_list c ON (a.extra_service_type = c.service_id) 
    INNER JOIN billing.country_list d ON (a.country = d.country_id) 
    INNER JOIN shared.transport_company e ON (a.tr_company = e.comp_id) 
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




# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
	label = "Go to: Function 3",
	page="Subpages/F3_FUNCTION_creation_of_XML.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/play_circle:",
	) 

st.page_link(
	label = "Previous page",
	page="Subpages/F3_F4_description_json.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/west:"
	) 