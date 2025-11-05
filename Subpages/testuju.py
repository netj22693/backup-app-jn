from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
import streamlit as st

@st.dialog("Error: DB not connected")
def db_connection_fail():

    st.warning("Application is not able to establish connection with DB server -> **Function 8 is currently not available**")
    st.stop()


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
        db_connection_fail()


st.write("# Company Book:")
''
''
''
st.image("Pictures/Function_8/F8_brands.svg", width=450)

''
tab1, tab2, tab3 = st.tabs([
    "Transport From - To",
    "Specific Company",
    "Overview - Companies"
])


#Generic connection when main page loaded

engine_generic = db_connection()


branch_type_info_df = pd.read_sql("""
    SELECT
        branch_text as "Type",
        description as "Description"                  
    FROM 
        branch
    WHERE
        type_code >= 3
    ORDER BY
        type_code 
    ;""", engine_generic)








with tab1:
    country_list = ["AT","CZ","DE","PL","SK"]
    country_list.sort()

    list_transport = ["Truck","Train","Airplane"]


    # Screen
    ''
    st.write("""
    - Provides **companies available** for selected **type of transport** and their **contact points/branches** 
    """)

    ''
    with st.form(key="user_form"):
        country_from = st.selectbox(label="Country From", options=country_list, help="Origin of transport.")
        country_to = st.selectbox(label="Country To", options=country_list, help="Destination of transport. It helps to distinguish if only domestic-transport companies to be included or not (in case that transport will happen in one country).")
        transport_type = st.selectbox(label="Transport type", options=list_transport, help="Select preferred transport type.")
        
        submit_button = st.form_submit_button(label= "Submit", width="stretch")

    # lowering letters for SQL purpose - case sensitive
    country_from = country_from.lower()
    country_to = country_to.lower()
    transport_type = transport_type.lower()


    def determin_international(c_from, c_to):

        if c_from == c_to:
            return 'FALSE'

        else:
            return 'TRUE'

    international = determin_international(country_from, country_to)


    if submit_button:

        engine = db_connection()
        

        def determin_transport_for_db_query(transport):

            mapping = {
                    "truck": 5,
                    "train": 6,
                    "airplane": 7
                }
            return mapping.get(transport, 0)


        # preparation of inputs/for dynamic SQL query
        transport_type_code = determin_transport_for_db_query(transport_type)

        branch_codes_display = f"'1','2','3','4','{transport_type_code}'"

        country_table = f"country_{country_from}"


        query_international = f"""
            SELECT
                name as "Name",
                city as "City",
                branch_text as "Type",
                street as "Street",
                number as "No.",
                district as "District",
                zip_code as "ZIP code",
                international_transport as "International transport"

            FROM
                company INNER JOIN {country_table} ON (comp_id = c_comp_id)
                INNER JOIN branch ON (branch_type = type_code)

            WHERE
                {transport_type} = TRUE AND 
                international_transport != FALSE AND
                type_code IN({branch_codes_display})

            ORDER BY
                name,
                city, 
                district ASC;
            """

        query_domestic = f"""
            SELECT
                name as "Name",
                city as "City",
                branch_text as "Type",
                street as "Street",
                number as "No.",
                district as "District",
                zip_code as "ZIP code",
                international_transport as "International transport"

            FROM
                company INNER JOIN {country_table} ON (comp_id = c_comp_id)
                INNER JOIN branch ON (branch_type = type_code)
            WHERE
                {transport_type} = TRUE AND
                type_code IN({branch_codes_display})
                        
            ORDER BY
                name,
                city, 
                district ASC;
            """

        def read_query_international_domestic(query):

            df = pd.read_sql(query, engine)
            
            return df


        if international == 'FALSE':

            df = read_query_international_domestic(query_domestic)

        if international == 'TRUE':

            df = read_query_international_domestic(query_international)


        df.index = df.index + 1

        #Screen
        ''
        with st.expander("Branch type info:",width= "stretch", icon=":material/help_outline:"):
            st.dataframe(branch_type_info_df, hide_index=True)
        
        ''
        st.dataframe(df, width = "stretch")


with tab2:

    engine = db_connection()

    company_df = pd.read_sql("SELECT name FROM company;", engine)
    company_list = company_df['name'].tolist()
    company_list.sort()

    # Screen
    ''
    st.write("""
    - Provides **visibility** about selected company - **availability and branches in countries**
    """)

    ''
    with st.form(key="user_form_2"):

        selected_company = st.selectbox(label="Company", options=company_list, help="Select or type a company name you are interested in.")

        submit_button = st.form_submit_button(label= "Submit", width="stretch")

    if submit_button:

        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT comp_id FROM company WHERE name = :company"),
                {"company": selected_company}
            )
            cus_id = result.scalar()


        def return_query_country(country_code, customer):

            query_country = f"""
                SELECT
                    name as "Name",
                    city as "City",
                    branch_text as "Type",
                    street as "Street",
                    number as "No.",
                    district as "District",
                    zip_code as "ZIP code",
                    branch_id as "Branch id"

                FROM
                    company 
                    INNER JOIN country_{country_code} ON (comp_id = c_comp_id)
                    INNER JOIN branch ON (branch_type = type_code)

                WHERE
                    c_comp_id = {customer}
                            
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


        df_at.index = df_at.index + 1
        df_cz.index = df_cz.index + 1
        df_de.index = df_de.index + 1
        df_pl.index = df_pl.index + 1
        df_sk.index = df_sk.index + 1

        # Screen 

        ''
        with st.expander("Branch type info:",width= "stretch", icon=":material/help_outline:"):
            st.dataframe(branch_type_info_df, hide_index=True)

        ''
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

        # Number of companies reqistered in DB
        df_company_no = pd.read_sql("""        
                SELECT count(comp_id) as count
                FROM company;
                """, engine)
        
        company_num = df_company_no['count'].iloc[0]


        # Number of branches in DB - accross all country_xx tables
        df_branch_num = pd.read_sql("""        
                        SELECT 
                            (SELECT COUNT(branch_id) FROM country_at) +
                            (SELECT COUNT(branch_id) FROM country_cz) +
                            (SELECT COUNT(branch_id) FROM country_de) +
                            (SELECT COUNT(branch_id) FROM country_pl) +
                            (SELECT COUNT(branch_id) FROM country_sk) as total_count;
                """, engine)
        
        branch_num = df_branch_num['total_count'].iloc[0]


        # Main query -> DF and overview
        df = pd.read_sql("""
                SELECT 
                    name as "Name",
                    truck as "Truck",
                    train as "Train",
                    airplane as "Airplane",
                    international_transport as "International transport"
                FROM
                    company
                ORDER BY 
                    name ASC         
                ;""", engine)


        df.index = df.index + 1

        # Screen
        ''
        st.write(f"""
        - Number of companies: **{company_num}**
        - Number of branches: **{branch_num}**
        """)

        ''
        st.dataframe(df, width = "stretch", height=800)