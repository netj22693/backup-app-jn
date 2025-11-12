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

st.write("Based on invoices created in Function 3...")
''

tab1, tab2 = st.tabs([
    "Last 15 invoices",
    "Search for specific invoice",
])

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
            g.name as "Currency"                                            
        
        FROM f4b.invoice a
            INNER JOIN f4b.category_list b ON (a.category = b.category_id)
            INNER JOIN f4b.extra_service_list c ON (a.extra_service_type = c.service_id) 
            INNER JOIN f4b.country_list d ON (a.country = d.country_id) 
            INNER JOIN f4b.transport_company e ON (a.tr_company = e.comp_id) 
            INNER JOIN f4b.size_list f ON (a.parcel_size = f.size_id) 
            INNER JOIN f4b.currency_list g ON (a.currency = g.currency_id) 

        ORDER BY 
            a.date DESC
        LIMIT 15  
            ;""", db_engine)


    # DF styling

    # This makes index + 1 -> by adding new column which is based on index number + 1 (normal df_styled.index = df_styled.index + 1 here doesn't work due to the style. - ing)
    df[" "] = df.index + 1
    df = df.set_index(" ")

    df["Date"] = pd.to_datetime(df["Date"])

    df_styled = df.style.format({
        "Price": "{:,.2f}",
        "Price - Extra service": "{:,.2f}",
        "Transport price": "{:,.2f}",
        "Total price": "{:,.2f}",
        "Date": lambda d: d.strftime("%d-%m-%Y")
        })
    
    st.dataframe(df_styled, width = "stretch", height=562)

with tab2: 

    with st.form(key="user_form"):
        order_input = st.text_input(label="Order number:", help="Insert **Order number** of invoice you would like to see. It is based on invoices created in **Function 3**.")

        order_input=order_input.strip()
        
        submit_button = st.form_submit_button(label= "Submit", width="stretch")
    
    if submit_button:

        def input_validation(input):

            if input == '':
                st.warning("**Missing input** - Please provide **Order number**")
                st.stop()
            
            else:
                pass
        
        # helps to prevent SQL injection to limit inputs to integer only
        def input_safety_validation(input):
            
            try: 
                input = int(input)
                pass

            except:
                st.warning("**Format issue** - The provide Order number is not in correct format")
                st.stop()
                
        
        input_validation(order_input)
        input_safety_validation(order_input)



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

        db_engine = connection_db()

        with db_engine.connect() as conn:
            params = {"order": order_input}
            df_overview = pd.read_sql_query(sql=text(sql_overview), con=conn, params=params)
            df_product = pd.read_sql_query(sql=text(sql_product), con=conn, params=params)
            df_extra_service = pd.read_sql_query(sql=text(sql_extra_service), con=conn, params=params)
            df_transport = pd.read_sql_query(sql=text(sql_transport), con=conn, params=params)
            df_transport_company = pd.read_sql_query(sql=text(sql_transport_company), con=conn, params=params)
      

        transport_company = df_transport_company['name'].iloc[0]

        #df styling

        df_overview["Date"] = pd.to_datetime(df_overview["Date"])

        df_overview_styled = df_overview.style.format({
            "Total price": "{:,.2f}",
            "Date": lambda d: d.strftime("%d-%m-%Y")
            })

        df_product_sytled = df_product.style.format({
            "Price": "{:,.2f}"
            })
        
        df_extra_service_styled = df_extra_service.style.format({
            "Extra service price": "{:,.2f}"
            })

        df_transport_styled = df_transport.style.format({
            "Transport price": "{:,.2f}"
            })


        def bring_logo_screen(input_company):

            if input_company == 'DHL':
                image = 'Pictures/Function_3/Logo_DHL_v2.svg'
                size = 280
            
            if input_company == 'Fedex':
                image = 'Pictures/Function_3/Logo_Fedex_v2.svg'
                size = 150
            
            return image, size

        logo, size_logo = bring_logo_screen(transport_company)


        # Visualization on user screen
        if df_overview.empty:
            st.info(f"**No invoice** found with this **Order number: {order_input}**")

        else:
            ''
            ''
            st.image(logo, width= size_logo)
            ''
            st.write("- **Invoice overview:**")
            st.dataframe(df_overview_styled, hide_index=True)

            ''
            st.write("- **Product overview:**")
            st.dataframe(df_product_sytled, hide_index=True)

            ''
            st.write("- **Extra service overview:**")
            st.dataframe(df_extra_service_styled, hide_index=True)

            ''
            st.write("- **Transport overview**")
            st.dataframe(df_transport_styled, hide_index=True)
