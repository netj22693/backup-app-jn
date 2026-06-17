import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, Engine
from sqlalchemy import text
from Subpages.F8_SQL_queries import sql_query_number_companies, sql_query_number_branches, sql_query_company_overview, sql_query_branch_info_df, get_sql_query_international_domestic, determin_transport_for_db_query, mapping_country_table, mapping_transport_type, create_df_branches_country


# ==== Business data - lists the F8 works with ====
country_list = ["AT","CZ","DE","PL","SK"]
country_list.sort()

country_list_lowered = list(map(lambda x: x.lower(),country_list))

list_transport = ["Truck","Train","Airplane"]


# ==== Generic function - DB connection ====
@st.dialog("Error: DB not connected")
def db_connection_fail():

    st.warning("Application is not able to establish connection with DB server -> **Function 8 is currently not available**")
    st.stop()


def db_connection() -> Engine:

    # Load secrets
    password = st.secrets["neon"]["password"]
    endpoint = st.secrets["neon"]["endpoint"]

    # connection string
    try: 
        conn_string = f"postgresql+psycopg2://neondb_owner:{password}@{endpoint}.gwc.azure.neon.tech/neondb?sslmode=require"


        engine = create_engine(conn_string)
        return engine

    except:
        st.warning("DB not connected")
        db_connection_fail()


# ==== Generic function - index ==== 

def adjust_index(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Index +1 -> First line in DF will have 1 not 0
    '''

    df.index = df.index + 1

    return df



# ==== UI Function 8 ==== 
st.write("# Company Book")
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


with tab1:

    # Function for TAB 1
    def determin_international(c_from: str, c_to: str) -> bool:
        '''
        - Function to determin if the transport will be from country to the same country or to the different country (international)
        - Result BOOLEAN used for SQL query build
        '''

        if c_from == c_to:
            return False

        else:
            return True


    # ==== UI ====
    ''
    st.write("""
    - Provides **companies available** for selected **type of transport** and their **contact points/branches** 
    """)

    ''
    with st.form(key="user_form"):
        country_from = st.selectbox(
            label="Country From",
            options=country_list,
            help="Origin of transport."
            )
        
        country_to = st.selectbox(
            label="Country To",
            options=country_list,
            help="Destination of transport. It helps to distinguish if only domestic-transport companies to be included or not (in case that transport will happen in one country)."
            )
        
        transport_type = st.selectbox(
            label="Transport type",
            options=list_transport,
            help="Select preferred transport type."
            )
        
        submit_button = st.form_submit_button(label= "Submit", width="stretch")


    # lowering letters for SQL purpose - case sensitive
    country_from = country_from.lower()
    country_to = country_to.lower()
    transport_type = transport_type.lower()

    # Submit button -> main logic TAB 1
    if submit_button:
        
        # DB enine creation
        db_engine = db_connection()


        # preparation of inputs/for dynamic SQL query using mapping
        international = determin_international(country_from, country_to)

        transport_type_code = determin_transport_for_db_query(transport_type)

        branch_codes_display = f"'1','2','3','4','{transport_type_code}'"

        country_table = mapping_country_table(country_from)

        transport_type_mapped = mapping_transport_type(transport_type)
        
        # Get SQL query 
        sql_query_international_domestic = get_sql_query_international_domestic(international, country_table, transport_type_mapped, branch_codes_display)

        # Pull data from DB
        df = pd.read_sql(sql_query_international_domestic, db_engine)

        # DF styling - index
        df = adjust_index(df)

        # Branch type info
        branch_type_info_df = pd.read_sql(sql_query_branch_info_df, db_engine)

        # ==== UI data visualization ====
        ''
        with st.expander("Branch type info:",width= "stretch", icon=":material/help_outline:"):
            st.dataframe(branch_type_info_df, hide_index=True)
        
        ''
        st.dataframe(df, width = "stretch")


with tab2:

    # DB enine creation
    db_engine = db_connection()

    company_df = pd.read_sql("SELECT name FROM company;", db_engine)
    company_list = company_df['name'].tolist()
    company_list.sort()

    # ==== UI ====
    ''
    st.write("""
    - Provides **visibility** about selected company - **availability and branches in countries**
    """)

    ''
    with st.form(key="user_form_2"):

        selected_company = st.selectbox(
            label="Company",
            options=company_list,
            help="Select or type a company name you are interested in."
            )

        submit_button = st.form_submit_button(label= "Submit", width="stretch")

    if submit_button:

        # ==== Main logic TAB 2 ====
        with db_engine.connect() as conn:
            result = conn.execute(
                text("SELECT comp_id FROM company WHERE name = :company"),
                {"company": selected_company}
            )
            cus_id = result.scalar()
     

        df_at = create_df_branches_country('at', cus_id, db_engine)
        df_cz = create_df_branches_country('cz', cus_id, db_engine)
        df_de = create_df_branches_country('de', cus_id, db_engine)
        df_pl = create_df_branches_country('pl', cus_id, db_engine)
        df_sk = create_df_branches_country('sk', cus_id, db_engine)
        

        branch_type_info_df = pd.read_sql(sql_query_branch_info_df, db_engine)



        # ==== UI ====

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
        # ==== UI ====
        ''
        submit_button_tab3 = st.button("Companies", width= "stretch", icon=":material/table:", key="key_submit_button_tab3")

        if submit_button_tab3:
            # DB enine creation
            db_engine = db_connection()

            # Number of companies reqistered in DB
            df_company_no = pd.read_sql(sql_query_number_companies, db_engine)
            
            company_num = df_company_no['count'].iloc[0]


            # Number of branches in DB - accross all country_xx tables
            df_branch_num = pd.read_sql(sql_query_number_branches, db_engine)
            
            branch_num = df_branch_num['total_count'].iloc[0]


            # Main query + DF styling
            df = pd.read_sql(sql_query_company_overview, db_engine)

            # Index
            df = adjust_index(df)

            # ==== UI data visualization ====
            ''
            st.write(f"""
            - Number of companies: **{company_num}**
            - Number of branches: **{branch_num}**
            """)

            ''
            st.dataframe(df, width = "stretch", height=800)