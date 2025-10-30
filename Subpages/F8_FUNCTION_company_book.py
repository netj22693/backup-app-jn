from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
import streamlit as st



def db_connection():

        # Load secrets
    db = st.secrets["neon"]

    # connection string
    try: 
        conn_string = f"postgresql+psycopg2://neondb_owner:{db['password']}@ep-lucky-bar-a9hww36i-pooler.gwc.azure.neon.tech/neondb?sslmode=require"


        engine = create_engine(conn_string)
        return engine

    except:
        st.warning("DB not connected")
        st.stop()



tab1, tab2, tab3 = st.tabs([
    "Tab_1",
    "Specific Company",
    "Company overview"
])

with tab1:
    country_list = ["AT","CZ","DE","PL","SK"]
    country_list.sort()

    list_transport = ["Truck","Train","Airplane"]

    # Form 
    with st.form(key="user_form"):
        country_from = st.selectbox(label="Country From", options=country_list)
        country_to = st.selectbox(label="Country To", options=country_list)
        transport_type = st.selectbox(label="Transport type", options=list_transport)
        
        submit_button = st.form_submit_button(label= "Submit", width="stretch")

    # lowering letters for SQL purpose - case sensitive
    country_from = country_from.lower()
    country_to = country_to.lower()
    transport_type = transport_type.lower()
    st.write(country_from)
    st.write(country_to)
    st.write(transport_type)


    def determin_international(c_from, c_to):

        if c_from == c_to:
            return 'FALSE'

        else:
            return 'TRUE'


    international = determin_international(country_from, country_to)
    st.write(international)

    if submit_button:

        engine = db_connection()

        df = pd.read_sql("SELECT * FROM customer;", engine)
        st.write(df)

        df = pd.read_sql("SELECT * FROM country_de;", engine)
        st.write(df.head())

        df = pd.read_sql("SELECT * FROM customer INNER JOIN country_cz ON (cus_id = c_cus_id);", engine)
        st.write(df.head())

        # country_from = 'cz'
        # transport_type = 'train'
        country_table = f"country_{country_from}"
        st.write(country_table)

        query_international = f"""
            SELECT
                name,
                city,
                street,
                number,
                district,
                zip_code,
                international_transport

            FROM
                customer INNER JOIN {country_table} ON (cus_id = c_cus_id)

            WHERE
                {transport_type} = TRUE AND 
                international_transport != FALSE

                        
            ORDER BY
                name,
                city, 
                district ASC;
            """

        query_domestic = f"""
            SELECT
                name,
                city,
                street,
                number,
                district,
                zip_code,
                international_transport

            FROM
                customer INNER JOIN {country_table} ON (cus_id = c_cus_id)

            WHERE
                {transport_type} = TRUE
                        
            ORDER BY
                name,
                city, 
                district ASC;
            """

        if international == 'FALSE':
            df = pd.read_sql(query_domestic, engine)

        if international == 'TRUE':
            df = pd.read_sql(query_international, engine)

        st.write(df)


with tab2:

    engine = db_connection()

    company_df = pd.read_sql("SELECT name FROM customer;", engine)
    company_list = company_df['name'].tolist()
    company_list.sort()

    with st.form(key="user_form_2"):

        selected_company = st.selectbox(label="Company", options=company_list)

        submit_button = st.form_submit_button(label= "Submit", width="stretch")

    if submit_button:

        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT cus_id FROM customer WHERE name = :company"),
                {"company": selected_company}
            )
            cus_id = result.scalar()

        st.write(cus_id)

        def return_query_country(country_code, customer):

            query_country = f"""
                SELECT
                    branch_id,
                    name,
                    city,
                    street,
                    number,
                    district,
                    zip_code,
                    international_transport

                FROM
                    customer INNER JOIN country_{country_code} ON (cus_id = c_cus_id)

                WHERE
                    c_cus_id = {customer}
                            
                ORDER BY
                    name,
                    city, 
                    district ASC;
                """
            return query_country
        

        query_country_at = return_query_country('at', cus_id)
        query_country_cz = return_query_country('cz', cus_id)
        query_country_de = return_query_country('de', cus_id)
        query_country_pl = return_query_country('pl', cus_id)
        query_country_sk = return_query_country('sk', cus_id)

        df_at = pd.read_sql(query_country_at, engine)
        df_cz = pd.read_sql(query_country_cz, engine)
        df_de = pd.read_sql(query_country_de, engine)
        df_pl = pd.read_sql(query_country_pl, engine)
        df_sk = pd.read_sql(query_country_sk, engine)

        st.write("Austria - AT")
        st.write(df_at)

        st.write("Czech Republic - CZ")
        st.write(df_cz)

        st.write("Germany - DE")
        st.write(df_de)

        st.write("Poland - PL")
        st.write(df_pl)

        st.write("Slovakia - SK")
        st.write(df_sk)


with tab3:

        engine = db_connection()

        df = pd.read_sql("""
            SELECT 
                name, truck, train, airplane, international_transport, cus_id
            FROM
                customer
            ORDER BY 
                name ASC         
            ;""", engine)
        
        st.write(df)