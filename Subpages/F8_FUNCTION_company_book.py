import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, Engine
from sqlalchemy import text
from Subpages.F8_map import get_map, df_styling_colors_per_map
from Subpages.F8_operational_functions import boolean_to_string_for_ui, count_rows, select_country_flag_path
from Subpages.F8_SQL_queries import sql_query_number_companies, sql_query_number_branches, sql_query_company_overview, sql_query_branch_info_df, sql_query_branch_df,sql_query_branch_for_map, sql_query_branch_size, sql_query_company_table, get_sql_query_international_domestic, determin_transport_for_db_query, mapping_country, mapping_transport_type, create_df_branches_country, create_pin_column


# ==== Business data - lists the F8 works with ====
country_list = ["AT","CZ","DE","PL","SK"]
country_list.sort()

list_transport = ["Truck","Train","Airplane"]

# ==== Hide columns for UI ====
# Note: there is a layer conflict between pd Styling and Streamlit visualization. This is a workaroud 
HIDDEN_COLUMNS = {
        "color_r": None,
        "color_g": None,
        "color_b": None,
        "lat": None,
        "lon": None,
    }

HIDDEN_COLUMNS_BRANCH_INFO = {
        "color_r": None,
        "color_g": None,
        "color_b": None,
            }

# ==== Predefined UI width variable used across TABs ====
FLAG_IMAGE_WIDTH = 20

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
tab1, tab2, tab3, tab4 = st.tabs([
    "Transport",
    "Company",
    "Branch",
    "Overview Companies"
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
            help="Destination of transport. **Note:** If country **From** and **To** is **the same**,  **also** companies doing **only** domestic transport (within the selected country) will be included."
            )
        
        transport_type = st.selectbox(
            label="Transport type",
            options=list_transport,
            help="Select preferred transport type."
            )
        
        submit_button = st.form_submit_button(label= "Submit", width="stretch", icon = ":material/apps:")


    # Submit button -> main logic TAB 1
    if submit_button:
        
        # DB engine creation
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
        # Branch type info
        branch_type_info_df = pd.read_sql(sql_query_branch_info_df, db_engine)

        # DF creation of new coumn 'PINS'
        df_from = create_pin_column(df_raw_from, 3)
        df_to = create_pin_column(df_raw_to, 3)
        branch_type_info_df = create_pin_column(branch_type_info_df, 0)

        # DF index
        df_from = adjust_index(df_raw_from)
        df_to = adjust_index(df_raw_to)

        # DF styling - colors
        df_from_styled = df_styling_colors_per_map(df_from)
        df_to_styled = df_styling_colors_per_map(df_to)
        branch_type_info_df = df_styling_colors_per_map(branch_type_info_df)


        # ==== UI data visualization ====
        ''
        with st.expander("Branch type info",width= "stretch", icon=":material/help_outline:"):
            st.dataframe(branch_type_info_df, hide_index=True, column_config = HIDDEN_COLUMNS_BRANCH_INFO)

        with st.expander("Map - Locations", icon=":material/location_on:"):

            # Concat of the 2 DF for MAP purposes + drop of duplicates (this can happen if it is domestic transport and the same country)
            df_raw_from_to = pd.concat([df_raw_from, df_raw_to], ignore_index=True).drop_duplicates()

            get_map(df_raw_from_to, "BIG")



        if international == True:
            ''
            st.write(f"From country - **{country_from}**")
            st.image(select_country_flag_path(country_from), width=FLAG_IMAGE_WIDTH)
            st.dataframe(df_from_styled, width = "stretch", column_config=HIDDEN_COLUMNS)

            ''
            st.write(f"To country - **{country_to}**")
            st.image(select_country_flag_path(country_to), width=FLAG_IMAGE_WIDTH)
            st.dataframe(df_to_styled, width = "stretch", column_config=HIDDEN_COLUMNS)
        
        else:
            ''
            st.write(f"Domestic transport - **{country_from}**")
            st.image(select_country_flag_path(country_from), width=FLAG_IMAGE_WIDTH)
            st.dataframe(df_from_styled, width = "stretch", column_config=HIDDEN_COLUMNS)


with tab2:

    # DB engine creation
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

        submit_button = st.form_submit_button(label= "Submit", width="stretch", icon = ":material/apps:")

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

        df_at = df_styling_colors_per_map(df_at)
        df_cz = df_styling_colors_per_map(df_cz)
        df_de = df_styling_colors_per_map(df_de)
        df_pl = df_styling_colors_per_map(df_pl)
        df_sk = df_styling_colors_per_map(df_sk)

        num_rows_at = count_rows(df_at_raw)
        num_rows_cz = count_rows(df_cz_raw)
        num_rows_de = count_rows(df_de_raw)
        num_rows_pl = count_rows(df_pl_raw)
        num_rows_sk = count_rows(df_sk_raw)


        # Branch type info DF
        branch_type_info_df = pd.read_sql(sql_query_branch_info_df, db_engine)

        branch_type_info_df = create_pin_column(branch_type_info_df, 0)
        
        branch_type_info_df = df_styling_colors_per_map(branch_type_info_df)


        # Company info and logo          
        df_company = pd.read_sql(text(sql_query_company_table), db_engine, params={"company_id": company_id})

        company = df_company.iloc[0]
        company_image = company["image_path"]
        company_name = company["name"]
        company_truck = company["truck"]
        company_train = company["train"]
        company_airplane = company["airplane"]
        company_internation_transport = company["international_transport"]
        company_web_url = company["web_url"]
        company_description = company["company_description"]

        company_truck_str = boolean_to_string_for_ui(company_truck)
        company_train_str = boolean_to_string_for_ui(company_train)
        company_airplane_str = boolean_to_string_for_ui(company_airplane)
        company_internation_transport_str = boolean_to_string_for_ui(company_internation_transport)


        # ==== UI ====
        ''
        try:
            st.image(company_image, width=200)
        except:
            pass

        ''
        with st.expander(f"Company info - **{company_name}**",width= "stretch", icon=":material/list:"):
            
            st.write(f"""
            - Company: **{company_name}**
            - Web page: [here]({company_web_url})
            """)
                        
            st.caption(company_description)


            st.write(f"""
            - International transport: **{company_internation_transport_str}**
            """)

            ''
            st.write(f"""
            - Truck: **{company_truck_str}**
            - Train: **{company_train_str}**
            - Airplane: **{company_airplane_str}**
            """)
        
        with st.expander("Branch type",width= "stretch", icon=":material/help_outline:"):
            st.dataframe(branch_type_info_df, hide_index=True, column_config = HIDDEN_COLUMNS_BRANCH_INFO)

        with st.expander("Map - Locations", icon=":material/location_on:"):
            
            # 02-July-2026 - Note: some DFs can be emppty due to no data (expacted behavior). FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation. -> For loop is filtering out the empty ones -> pd.concat() works
            dfs = [df_at_raw, df_cz_raw, df_de_raw, df_pl_raw, df_sk_raw]

            dfs = [df for df in dfs if not df.empty]

            df_raw_concat = pd.concat(dfs, ignore_index=True).drop_duplicates()

            get_map(df_raw_concat, "BIG")


        image_width = 20

        ''
        ''
        st.write(f"Austria - **AT** - Branches: **{num_rows_at}**")
        st.image(select_country_flag_path('AT'), width=FLAG_IMAGE_WIDTH)
        st.dataframe(df_at, width = "stretch", column_config=HIDDEN_COLUMNS)

        ''
        st.write(f"Czech Republic - **CZ** - Branches: **{num_rows_cz}**")
        st.image(select_country_flag_path('CZ'), width=FLAG_IMAGE_WIDTH)
        st.dataframe(df_cz, width = "stretch", column_config=HIDDEN_COLUMNS)

        ''
        st.write(f"Germany - **DE** - Branches: **{num_rows_de}**")
        st.image(select_country_flag_path('DE'), width=FLAG_IMAGE_WIDTH)
        st.dataframe(df_de, width = "stretch", column_config=HIDDEN_COLUMNS)

        ''
        st.write(f"Poland - **PL** - Branches: **{num_rows_pl}**")
        st.image(select_country_flag_path('PL'), width=FLAG_IMAGE_WIDTH)
        st.dataframe(df_pl, width = "stretch", column_config=HIDDEN_COLUMNS)

        ''
        st.write(f"Slovakia - **SK** - Branches: **{num_rows_sk}**")
        st.image(select_country_flag_path('SK'), width=FLAG_IMAGE_WIDTH)
        st.dataframe(df_sk, width = "stretch",column_config=HIDDEN_COLUMNS)




# ==== Function TAB 3 ==== 
def input_validation(value) -> int | None:
    try:
        return int(value)
    
    except (TypeError, ValueError):

        st.warning("This is not supported format. Branch ID is a number")
        return None

 

with tab3:

    # ==== UI ==== 
    ''
    st.write("""
    - Provides **branch detail**
    """)
    ''

    with st.form(key="user_form_branch"):
        branch_id_input = st.text_input(label="Branch ID:", help="The **Branch ID** is available in TAB 1 or TAB 2. When results are displayed, you can find the **Branch ID** either in the **tables** or in the **maps**")
        
        submit_button = st.form_submit_button(label= "Submit", width="stretch", icon = ":material/apps:")

    if submit_button:

        input_valid = input_validation(branch_id_input)
    
        if input_valid is not None:

            # DB engine creation
            db_engine = db_connection()

            df_branch_and_company = pd.read_sql(text(sql_query_branch_df), db_engine, params={"branch_id": input_valid})

            # Empty DF -> no branch in DB
            if df_branch_and_company.empty == True:
                st.info(f"No branch with ID: **{input_valid}**")
            
            else:

                # DF from DB
                df_map = pd.read_sql(text(sql_query_branch_for_map), db_engine, params={"branch_id": input_valid})

                df_branch_size = pd.read_sql(text(sql_query_branch_size), db_engine, params={"branch_id": input_valid})


                # For extracting data from DF
                branch = df_branch_and_company.iloc[0]
                branch_type = df_map.iloc[0]
                branch_size = df_branch_size.iloc[0]

                # Determin country flag
                branch_country = branch["country_code"]
                
                country_flag = select_country_flag_path(branch_country)



                # ==== UI ====

                ''
                ''
                try:
                    st.image({branch.image_path}, width=200)
                except:
                    pass
                ''
                ''
                st.write(f"""
                - Company: **{branch['name']}**
                - Web page: [here]({branch.web_url})
                """)

                st.caption(f"{branch.company_description}")
                
                st.write("---")

                try:
                    st.image(country_flag, width=60)
                except:
                    pass
                
                col1, col2 = st.columns(2)
                ''
                col1.write(f"""
                - Country: **{branch.country_code}**
                - City: **{branch.city}**
                - Street: **{branch.street} {branch.number}**
                - District: **{branch.district}**
                - Zip Code: **{branch.zip_code}**
                """)


                col2.write(f"""
                - Branch ID: **{branch_type['Branch ID']}**
                - Category: **{branch_type.branch_text}**
                - Size: **{branch_size.description}**
                """)
                ''
                get_map(df_map, "SMALL")

            
            # Dat tam obecny company info + loga + web + branch info a mapu 
    

with tab4:
        # ==== UI ====
        ''
        st.write("""
        - Provides **overall summary/visibility** of companies in DB and number of their branches 
        """)
        ''
        submit_button_tab3 = st.button("Companies", width= "stretch", icon=":material/table:", key="key_submit_button_tab3")

        if submit_button_tab3:
            # DB engine creation
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

# Celá funkce F8 -> Rozšířit kód o logování

# Rozšířit DB o pobočky 
# Fedex
# Emirates skycargo
# Lufthansa Cargo
# OBB Rail crago (hroznej shit to hledat)
# Metrans, ty se dobže hledaj
# DB Cargo
