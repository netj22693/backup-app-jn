import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd

@st.dialog("Error: DB not connected")
def db_connection_fail():

    st.warning("Application is not able to establish connection with DB server -> **This 3B Function is currently not available**")
    st.stop()


def connection_db():
    # Load secrets
    password = st.secrets["neon"]["password"]
    endpoint = st.secrets["neon"]["endpoint"]

    # connection string
    try: 
        conn_string = f"postgresql+psycopg2://neondb_owner:{password}@{endpoint}.gwc.azure.neon.tech/neondb?sslmode=require"

        engine = create_engine(conn_string)
        return engine

    except:
        db_connection_fail()



# ================ Application Screen - INPUT Buttons ========================
st.write("# Find your invoice:")
''

st.write("- Simple view into DB. Based on invoices created in Function 3...")
''

tab1, tab2 = st.tabs([
    "Last 15 invoices",
    "Search for specific invoice",
])


# =================  Tab 1  ======================
with tab1:
    db_engine = connection_db()

    df = pd.read_sql("""
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
        
        FROM f4b.invoice a
            INNER JOIN f4b.category_list b ON (a.category = b.category_id)
            INNER JOIN f4b.extra_service_list c ON (a.extra_service_type = c.service_id) 
            INNER JOIN f4b.country_list d ON (a.country = d.country_id) 
            INNER JOIN f4b.transport_company e ON (a.tr_company = e.comp_id) 
            INNER JOIN f4b.size_list f ON (a.parcel_size = f.size_id) 
            INNER JOIN f4b.currency_list g ON (a.currency = g.currency_id) 
            INNER JOIN f4b.format_list h ON (a.file_format = h.format_id)

        ORDER BY 
            a.date DESC,
            a.order_number DESC
        LIMIT 15  
            ;""", db_engine)


    # DF styling

    # This makes index + 1 -> by adding new column which is based on index number + 1 (normal df_styled.index = df_styled.index + 1 here doesn't work due to the style. - ing)
    df[" "] = df.index + 1
    df = df.set_index(" ")

    df["Date"] = pd.to_datetime(df["Date"])

    df_styled = df.style.format({
        "Price": "{:,.2f}",
        "Extra service price": "{:,.2f}",
        "Transport price": "{:,.2f}",
        "Total price": "{:,.2f}",
        "Date": lambda d: d.strftime("%d-%m-%Y")
        })
    
    st.dataframe(df_styled, width = "stretch", height=562)

# =================  Tab 2 - main logic put in def ======================

def tab_2_logic_run():
    
    # Queries
    sql_overview = """
    SELECT 
        a.order_number as "Order no.",
        a.date as "Date",
        a.customer as "Customer",
        a.total_price as "Total price",
        g.name as "Currency"                                            
    
    FROM f4b.invoice a
        INNER JOIN f4b.category_list b ON (a.category = b.category_id)
        INNER JOIN f4b.extra_service_list c ON (a.extra_service_type = c.service_id) 
        INNER JOIN f4b.country_list d ON (a.country = d.country_id) 
        INNER JOIN f4b.transport_company e ON (a.tr_company = e.comp_id) 
        INNER JOIN f4b.size_list f ON (a.parcel_size = f.size_id) 
        INNER JOIN f4b.currency_list g ON (a.currency = g.currency_id) 

    WHERE 
        a.order_number = :order
        ;"""

    sql_file_format = """
    SELECT 
        h.name                                        
    
    FROM f4b.invoice a
        INNER JOIN f4b.format_list h ON (a.file_format = h.format_id)

    WHERE 
        a.order_number = :order
        ;"""

    sql_product = """
    SELECT 
        a.product_name as "Product",
        b.name as "Category",
        a.product_price as "Price",
        g.name as "Currency"                                       
    
    FROM f4b.invoice a
        INNER JOIN f4b.category_list b ON (a.category = b.category_id)
        INNER JOIN f4b.extra_service_list c ON (a.extra_service_type = c.service_id) 
        INNER JOIN f4b.country_list d ON (a.country = d.country_id) 
        INNER JOIN f4b.transport_company e ON (a.tr_company = e.comp_id) 
        INNER JOIN f4b.size_list f ON (a.parcel_size = f.size_id) 
        INNER JOIN f4b.currency_list g ON (a.currency = g.currency_id) 
    
    WHERE 
        a.order_number = :order
    ;"""   

    sql_extra_service = """
    SELECT 
        c.name as "Extra service",
        a.extra_service_price as "Extra service price",
        g.name as "Currency"                          
    
    FROM f4b.invoice a
        INNER JOIN f4b.category_list b ON (a.category = b.category_id)
        INNER JOIN f4b.extra_service_list c ON (a.extra_service_type = c.service_id) 
        INNER JOIN f4b.country_list d ON (a.country = d.country_id) 
        INNER JOIN f4b.transport_company e ON (a.tr_company = e.comp_id) 
        INNER JOIN f4b.size_list f ON (a.parcel_size = f.size_id) 
        INNER JOIN f4b.currency_list g ON (a.currency = g.currency_id) 
    
    WHERE 
        a.order_number = :order
    ;"""   

    sql_transport = """
    SELECT 
        e.name as "Transport Company",
        d.name as "Country",
        f.name as "Parcel size",
        a.tr_price as "Transport price",
        g.name as "Currency"                         
    
    FROM f4b.invoice a
        INNER JOIN f4b.category_list b ON (a.category = b.category_id)
        INNER JOIN f4b.extra_service_list c ON (a.extra_service_type = c.service_id) 
        INNER JOIN f4b.country_list d ON (a.country = d.country_id) 
        INNER JOIN f4b.transport_company e ON (a.tr_company = e.comp_id) 
        INNER JOIN f4b.size_list f ON (a.parcel_size = f.size_id) 
        INNER JOIN f4b.currency_list g ON (a.currency = g.currency_id) 
    
    WHERE 
        a.order_number = :order
    ;""" 


    sql_transport_company = """
    SELECT 
        e.name                   
    
    FROM f4b.invoice a
        INNER JOIN f4b.transport_company e ON (a.tr_company = e.comp_id) 
    
    WHERE 
        a.order_number = :order
    ;"""

    sql_mapping_log = """
    SELECT 
        i.date as "Date",
        i.change as "Description",
        f_from.name as "From",
        f_to.name as "To"

    FROM f4b.change_log i
    INNER JOIN f4b.format_list f_from ON f_from.format_id = i.mapping_from
    INNER JOIN f4b.format_list f_to   ON f_to.format_id   = i.mapping_to
    INNER JOIN f4b.invoice a ON (a.order_number = i.order_number_log)

    WHERE 
    a.order_number = :order

    ORDER BY 
    i.date ASC
    ;"""


    # DB connection + +ueries run
    db_engine = connection_db()

    with db_engine.connect() as conn:
        params = {"order": order_input}
        df_file_format = pd.read_sql_query(sql=text(sql_file_format), con=conn, params=params)
        df_overview = pd.read_sql_query(sql=text(sql_overview), con=conn, params=params)
        df_product = pd.read_sql_query(sql=text(sql_product), con=conn, params=params)
        df_extra_service = pd.read_sql_query(sql=text(sql_extra_service), con=conn, params=params)
        df_transport = pd.read_sql_query(sql=text(sql_transport), con=conn, params=params)
        df_transport_company = pd.read_sql_query(sql=text(sql_transport_company), con=conn, params=params)
        df_mapping_logs = pd.read_sql_query(sql=text(sql_mapping_log), con=conn, params=params)


    # Key if/else logic - in case that no match in DB with Order number -> tab_2 logic doesn't continue
    if df_overview.empty or df_file_format.empty:
        st.info(f"**No invoice** found with this **Order number: {order_input}**")
    
    else: 
        # Making variables extracting them from dataframes
        file_format = df_file_format['name'].iloc[0]
        transport_company = df_transport_company['name'].iloc[0]


        #df styling
        df_overview["Date"] = pd.to_datetime(df_overview["Date"])

        df_overview_styled = df_overview.style.format({
            "Total price": "{:,.2f}",
            "Date": lambda d: d.strftime("%d-%m-%Y")
            })

        df_product_styled = df_product.style.format({
            "Price": "{:,.2f}"
            })
        
        df_extra_service_styled = df_extra_service.style.format({
            "Extra service price": "{:,.2f}"
            })

        df_transport_styled = df_transport.style.format({
            "Transport price": "{:,.2f}"
            })

        if not df_mapping_logs.empty:
            # This makes index + 1 -> by adding new column which is based on index number + 1 (normal df_styled.index = df_styled.index + 1 here doesn't work due to the style. - ing)
            df_mapping_logs[" "] = df_mapping_logs.index + 1
            df_mapping_logs = df_mapping_logs.set_index(" ")

            df_mapping_logs["Date"] = pd.to_datetime(df_mapping_logs["Date"])

            df_mapping_logs_styled = df_mapping_logs.style.format({
                "Date": lambda d: d.strftime("%d-%m-%Y - %H:%M:%S")
                })


        def bring_logo_screen(input_company):

            if input_company == 'DHL':
                image = 'Pictures/Function_3/Logo_DHL_v3.svg'
                size = 150
            
            if input_company == 'Fedex':
                image = 'Pictures/Function_3/Logo_Fedex_v3.svg'
                size = 95
            
            return image, size

        logo, size_logo = bring_logo_screen(transport_company)


        # Visualization on user screen
        ''
        ''
        st.write(f"- Invoice was originally produced in **{file_format}** format")
        ''
        st.write("- Invoice overview:")
        st.dataframe(df_overview_styled, hide_index=True)

        ''
        st.write("- Product overview:")
        st.dataframe(df_product_styled, hide_index=True)

        ''
        st.write("- Extra service overview:")
        st.dataframe(df_extra_service_styled, hide_index=True)

        ''
        st.write("- Transport overview:")
        st.image(logo, width= size_logo)
        st.dataframe(df_transport_styled, hide_index=True)

        ''
        if df_mapping_logs.empty:
            st.write("- Logs - Invoice mapped to differnet format: **no mapping**")
            st.dataframe(df_mapping_logs)
        else:
            st.write("- Logs - Invoice mapped to differnet format:")
            st.dataframe(df_mapping_logs_styled)


with tab2: 

    with st.form(key="user_form"):
        order_input = st.text_input(label="Order number:", help="Insert **Order number** of invoice you would like to see. It is based on invoices created in **Function 3**.")

        order_input=order_input.strip()
        
        submit_button = st.form_submit_button(label= "Submit", width="stretch")
    
    if submit_button:

        def input_validation(input):

            if input == '':
                st.warning("**Missing input** - Please provide **Order number**")
                return False
            
            return True
        
        # helps to prevent SQL injection to limit inputs to integer only
        def input_safety_validation(input):
            
            try: 
                input = int(input)
                return True

            except:
                st.warning("**Format issue** - The provide Order number is not in correct format")
                return False
                
                
        
        # if/else logic block - if not preventing for triggering main logic due to wrong input
        if not input_validation(order_input) or not input_safety_validation(order_input):
            pass


        # Tab 2 main being triggered here
        else:
            tab_2_logic_run()
            

# ======================= Tab 2 END ====================

