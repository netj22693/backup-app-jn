import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, Engine
from sqlalchemy import text
from Subpages.F8_map import get_map
from Subpages.F8_SQL_queries import sql_query_number_companies, sql_query_number_branches, sql_query_company_overview, sql_query_branch_info_df, get_sql_query_international_domestic, determin_transport_for_db_query, mapping_country, mapping_transport_type, create_df_branches_country, drop_columns


# ==== Business data - lists the F8 works with ====
country_list = ["AT","CZ","DE","PL","SK"]
country_list.sort()

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


    # Submit button -> main logic TAB 1
    if submit_button:
        
        # DB enine creation
        db_engine = db_connection()


        # preparation of inputs/for dynamic SQL query using mapping
        international = determin_international(country_from, country_to)

        transport_type_code = determin_transport_for_db_query(transport_type)

        branch_codes_display = f"'1','2','3','4','{transport_type_code}'"

        country_from_mapped = mapping_country(country_from)
        country_to_mapped = mapping_country(country_to)

        transport_type_mapped = mapping_transport_type(transport_type)
        
        # Get SQL query 
        sql_query_international_domestic_from = get_sql_query_international_domestic(international,  country_from_mapped, transport_type_mapped, branch_codes_display)
        sql_query_international_domestic_to = get_sql_query_international_domestic(international,  country_to_mapped, transport_type_mapped, branch_codes_display)

        # Pull data from DB
        df_raw_from = pd.read_sql(sql_query_international_domestic_from, db_engine)
        df_raw_to = pd.read_sql(sql_query_international_domestic_to, db_engine)

        # DF drop of columns not to be visible UI
        df_from = drop_columns(df_raw_from)
        df_to = drop_columns(df_raw_to)

        # DF styling - index
        df_from = adjust_index(df_from)
        df_to = adjust_index(df_to)

        # Branch type info
        branch_type_info_df = pd.read_sql(sql_query_branch_info_df, db_engine)

        # ==== UI data visualization ====
        ''
        with st.expander("Map - Locations", icon=":material/location_on:"):

            # Concat of the 2 DF for MAP purposes + drop of duplicates (this can happen if it is domestic transport and the same country)
            df_raw_from_to = pd.concat([df_raw_from, df_raw_to], ignore_index=True).drop_duplicates()

            get_map(df_raw_from_to)


        with st.expander("Branch type info",width= "stretch", icon=":material/help_outline:"):
            st.dataframe(branch_type_info_df, hide_index=True)
        

        if international == True:
            ''
            st.write(f"From country - **{country_from}**")
            st.dataframe(df_from, width = "stretch")

            ''
            st.write(f"To country - **{country_to}**")
            st.dataframe(df_to, width = "stretch")
        
        else:
            ''
            st.write(f"Domestic transport - **{country_from}**")
            st.dataframe(df_from, width = "stretch")


with tab2:

    # DB enine creation
    db_engine = db_connection()

    company_df = pd.read_sql("SELECT name FROM function8.company;", db_engine)
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
                text("SELECT company_id FROM function8.company WHERE name = :company"),
                {"company": selected_company}
            )
            company_id = result.scalar()
     

        df_at_raw, df_at = create_df_branches_country('AT', company_id, db_engine)
        df_cz_raw, df_cz = create_df_branches_country('CZ', company_id, db_engine)
        df_de_raw, df_de = create_df_branches_country('DE', company_id, db_engine)
        df_pl_raw, df_pl = create_df_branches_country('PL', company_id, db_engine)
        df_sk_raw, df_sk = create_df_branches_country('SK', company_id, db_engine)

        branch_type_info_df = pd.read_sql(sql_query_branch_info_df, db_engine)



        # ==== UI ====

        ''
        with st.expander("Map - Locations", icon=":material/location_on:"):

            df_raw_concat = pd.concat([df_at_raw, df_cz_raw, df_de_raw, df_pl_raw, df_sk_raw], ignore_index=True).drop_duplicates()

            get_map(df_raw_concat)


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



# Pokracovat s:
# Doplnit PL and DE lokace v DB -> čeknout to proti googlu
# Projit lokace CY, AT, SK, a ykontrolovat na mapě, že to nejde někam do pole

# TAB 2 - zakomponovat taky maps expander do výsledků -> složit jeden DF ze 5 malých DF -> passnout MAP funkci A NEBO MOŽNÁÁÁÁÁ :) DÁT POD KAŽDOU ZEMI SEPARÁTNÍ MAPU - S JINÝM DEFAULT SETAUPEM LAN LONG A TEN EXPANDER ZOBRAZIT POUZE IF DF NOT EMPTY :)))

# Pak jsem ještě jsem přemýšlel TAB 4 -> search for Branch Based on ID, že bych ke každě firmě našel logo, udělal nějaké stručné summary o té firmě, stručné summary o té pobočce zobrazil ji na mapě