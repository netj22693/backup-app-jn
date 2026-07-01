import pandas as pd
from sqlalchemy import Engine


#  ==== Functions for mapping ====

def mapping_country(input_country: str) -> str:

    mapping = {
            "AT": "AT",
            "CZ": "CZ",
            "DE": "DE",
            "PL": "PL",
            "SK" : "SK"
        }
    return mapping.get(input_country)     
   

def determin_transport_for_db_query(transport: str) -> str:

    mapping = {
            "Truck": 5,
            "Train": 6,
            "Airplane": 7
        }
    return mapping.get(transport, 0)


def mapping_transport_type(transport: str) -> str:

    mapping = {
            "Truck": "truck",
            "Train": "train",
            "Airplane": "airplane"
        }
    return mapping.get(transport)


#  ==== Function - extension of DF for map purposes ====
def create_pin_column(df: pd.DataFrame, position:int) -> pd.DataFrame:
    
    '''
    - Creation of Pin columns -> for visualization purpuses
    - position - index of column
    '''

    df.insert(position, "Pin", "⬤")

    return df


#  ==== Function - dynamic SQL query ====

def get_sql_query_international_domestic(international: bool, country_from: str, transport_type: str, branch_codes: str) -> str:

    '''
    Building SQL query based on dynamic inputs
    '''

    if international == True:
        extra_where = "AND international_transport != FALSE"
    else:
        extra_where = ""


    query = f"""
    SELECT
        a.name as "Name",
        b.city as "City",
        d.branch_text as "Type",
        b.street as "Street",
        b.number as "No.",
        b.district as "District",
        b.zip_code as "ZIP code",
        a.international_transport as "International transport",
        b.lat, 
        b.lon,
        d.color_r,
        d.color_g,
        d.color_b,
        b.branch_id as "Branch ID"

    FROM
        function8.company a
        INNER JOIN function8.branch b ON(a.company_id = b.company_id)
        INNER JOIN function8.branch_type d ON (b.branch_type = d.type_code)
    WHERE
        {transport_type} = TRUE
        {extra_where}
        AND b.country_code = '{country_from}'
        AND d.type_code IN ({branch_codes})
    ORDER BY
        a.name,
        b.city,
        b.district ASC
    """

    return query

# ==== Function - TAB 2 ====
def create_df_branches_country(country_code: str, company_id, engine: Engine) -> pd.DataFrame:
    '''
    - Main logic for TAB 2 -> getting DF/data from DB
    '''

    # Provide name of table for dynamic SQL query
    country_code_mapped = mapping_country(country_code)

    query_country = f"""
        SELECT
            a.name as "Name",
            b.city as "City",
            d.branch_text as "Type",
            b.street as "Street",
            b.number as "No.",
            b.district as "District",
            b.zip_code as "ZIP code",
            b.lat, 
            b.lon,
            d.color_r,
            d.color_g,
            d.color_b,
            b.branch_id as "Branch ID"

        FROM
            function8.company a
            INNER JOIN function8.branch b ON (a.company_id = b.company_id)
            INNER JOIN function8.branch_type d ON (b.branch_type = d.type_code)

        WHERE
            a.company_id = {company_id} AND
            b.country_code = '{country_code_mapped}'
                    
        ORDER BY
            a.name,
            b.city, 
            b.district ASC;
        """

    # Get DF from DB
    df = pd.read_sql(query_country, engine)

    df_ui = create_pin_column(df, 2)

    # Index change for UI purposes
    df_ui.index = df_ui.index + 1
    
    return df, df_ui


# ============= SQL QUERIES =============
# ==== TAB 1 and 2 ====

sql_query_branch_info_df = """
SELECT
    branch_text as "Type",
    description as "Description",
    color_r,
    color_g,
    color_b                 
FROM 
    function8.branch_type
WHERE
    type_code >= 3
ORDER BY
    type_code;"""


# ==== TAB 3 ====

sql_query_number_companies = """        
SELECT count(company_id) as count
FROM function8.company;"""


sql_query_number_branches = """        
SELECT count(branch_id) as total_count
FROM function8.branch
;"""


sql_query_company_overview = """
SELECT 
    a.name as "Name",
    a.truck as "Truck",
    a.train as "Train",
    a.airplane as "Airplane",
    a.international_transport as "International transport",
    count(b.branch_id) as "No. branches"
FROM
    function8.company a 
    LEFT JOIN function8.branch b ON (a.company_id = b.company_id)

GROUP BY
    a.name,
    a.truck,
    a.train,
    a.airplane,
    a.international_transport

ORDER BY 
    a.name ASC;"""

# ==== TAB 4 ====

sql_query_branch_df = """
SELECT *
FROM function8.branch b
INNER JOIN function8.company a ON (b.company_id = a.company_id)
WHERE b.branch_id = :branch_id
;"""

sql_query_branch_for_map = """
SELECT
    a.name as "Name",
    b.branch_id as "Branch ID",
    b.city as "City",
    b.street as "Street",
    b.number as "No.",
    b.lat,
    b.lon,
    d.branch_text,
    d.color_r,
    d.color_g,
    d.color_b,
    d.branch_text as "Type"

FROM function8.branch b
    INNER JOIN function8.branch_type d ON (b.branch_type = d.type_code)
    INNER JOIN function8.company a ON (b.company_id = a.company_id)

WHERE b.branch_id = :branch_id
;"""


sql_query_branch_size = """
SELECT 
    e.description

FROM function8.branch_size e
    INNER JOIN function8.branch b ON (b.branch_size = e.branch_size)

WHERE b.branch_id = :branch_id
;"""


