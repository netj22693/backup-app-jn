import pandas as pd
from sqlalchemy import Engine


#  ==== Functions for mapping ====

def mapping_country_table(input_country: str) -> str:

    mapping = {
            "at": "country_at",
            "cz": "country_cz",
            "de": "country_de",
            "pl": "country_pl",
            "sk" : "country_sk"
        }
    return mapping.get(input_country)     
   

def determin_transport_for_db_query(transport: str) -> str:

    mapping = {
            "truck": 5,
            "train": 6,
            "airplane": 7
        }
    return mapping.get(transport, 0)


def mapping_transport_type(transport: str) -> str:

    mapping = {
            "truck": "truck",
            "train": "train",
            "airplane": "airplane"
        }
    return mapping.get(transport)



#  ==== Function - dynamic SQL query ====

def get_sql_query_international_domestic(international: bool, country_table: str, transport_type: str, branch_codes: str):

    '''
    Building SQL query based on dynamic inputs
    '''

    if international == True:
        extra_where = "AND international_transport != FALSE"
    else:
        extra_where = ""


    query = f"""
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
        company
        INNER JOIN {country_table} ON (comp_id = c_comp_id)
        INNER JOIN branch ON (branch_type = type_code)
    WHERE
        {transport_type} = TRUE
        {extra_where}
        AND type_code IN ({branch_codes})
    ORDER BY
        name,
        city,
        district ASC
    """

    return query

# ==== Function - TAB 2 ====
def create_df_branches_country(country_code: str, customer, engine: Engine) -> pd.DataFrame:
    '''
    - Main logic for TAB 2 -> getting DF/data from DB
    '''

    # Provide name of table for dynamic SQL query
    country_table = mapping_country_table(country_code)

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
            INNER JOIN {country_table} ON (comp_id = c_comp_id)
            INNER JOIN branch ON (branch_type = type_code)

        WHERE
            c_comp_id = {customer}
                    
        ORDER BY
            name,
            city, 
            district ASC;
        """

    # Get DF from DB
    df = pd.read_sql(query_country, engine)

    # Index change for UI purposes
    df.index = df.index + 1
    
    return df


# ============= SQL QUERIES =============
# ==== TAB 1 and 2 ====

sql_query_branch_info_df = """
SELECT
    branch_text as "Type",
    description as "Description"                  
FROM 
    branch
WHERE
    type_code >= 3
ORDER BY
    type_code;"""


# ==== TAB 3 ====

sql_query_number_companies = """        
SELECT count(comp_id) as count
FROM company;"""


sql_query_number_branches = """        
SELECT 
    (SELECT COUNT(branch_id) FROM country_at) +
    (SELECT COUNT(branch_id) FROM country_cz) +
    (SELECT COUNT(branch_id) FROM country_de) +
    (SELECT COUNT(branch_id) FROM country_pl) +
    (SELECT COUNT(branch_id) FROM country_sk) as total_count;"""


sql_query_company_overview = """
SELECT 
    name as "Name",
    truck as "Truck",
    train as "Train",
    airplane as "Airplane",
    international_transport as "International transport"
FROM
    company
ORDER BY 
    name ASC;"""


