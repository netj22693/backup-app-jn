import streamlit as st
import pandas as pd
from sqlalchemy import Engine



# FOR DEVELOPMENT A TESTING ONLY ---- SMAZAT
# Function for DB connection
from sqlalchemy import create_engine
def db_connection():

    # Load secrets
    password = st.secrets["neon"]["password"]
    endpoint = st.secrets["neon"]["endpoint"]

    # connection string
    try: 
        conn_string = f"postgresql+psycopg2://neondb_owner:{password}@{endpoint}.gwc.azure.neon.tech/neondb?sslmode=require"

        engine = create_engine(conn_string)
        return engine

    except:
        st.warning("DB not connected - the function will not function fully.")
        return None



# Go green calculation

# Connection
db_engine = db_connection()

# Query into DB -> to get emissions from go_green_emissions table -> DF
def create_df_emissions(engine: Engine) -> pd.DataFrame:

    query = """
    SELECT 
        f.label,
        l.emission,
        l.unit
    FROM function7.transport_type f
        INNER JOIN function7.go_green_emissions l ON (f.transport_id = l.transport_id)
    ORDER BY f.transport_id;
    """
    
    return pd.read_sql(query, engine)

df_emissions_db_input = create_df_emissions(db_engine)



# Emission DF parsing function

# Taken from F7 - tohle je ten DF, ze kterýcho já si pak budu brát distance
tab2_distance_truck_r2 = 400
tab2_distance_train_r2 = 500
tab2_distance_air_r2 = 600.58666
from_city_extra_doortdoor = 0
to_city_extra_doortdoor = 0
tranport_types_list = ['Truck','Train','Airplane']

df_tab2_transport = pd.DataFrame({
    "Transport type" : tranport_types_list,
    "Distance (km)" : [tab2_distance_truck_r2, tab2_distance_train_r2, tab2_distance_air_r2],
    # "Time (hours)" : [tab2_time_journey_truck_r2, tab2_time_journey_train_r2, tab2_time_journey_air_r2],
    # f"Price ({selected_currency})" : [tab2_price_truck_r2, tab2_price_train_r2, tab2_price_air_r2],
})

list_transport_from_df = df_emissions_db_input["label"]


emission_dict = pd.DataFrame.to_json(df_emissions_db_input)



def calculate_emission_transfer(df: pd.DataFrame, dtd_from: float, dtd_to: float) -> dict:

    # Loop to get emission value for 'Transfer' - applicable when DTD 
    for index, row in df.iterrows():
        if row['label'] == 'Transfer':
            emission_value = row['emission']

    if dtd_from > 0 and dtd_to > 0:
        result = 2 * emission_value
    
    elif dtd_from > 0 or dtd_to > 0:
        result = emission_value
    
    else:
        result = 0


    # create DF
    result_df = pd.DataFrame({
        'Transport type' : ['Transfer'],
        'CO2' : [result]
    })

    return result_df


def calculate_emissions_main_distance(df_transport: pd.DataFrame, df_emissions: pd.DataFrame) -> dict:

    '''
    - Merging 2 DFs together (like LEFT JOIN in SQL)
    '''

    df_merged = df_transport.merge(
        df_emissions,
        left_on="Transport type",
        right_on="label",
        how="left"
    )

    df_merged["CO2"] = df_merged["Distance (km)"] * df_merged["emission"]

    emissions_distance = df_merged[["Transport type","CO2"]]
   
    return emissions_distance
    


emission_transfer_df = calculate_emission_transfer(df_emissions_db_input, from_city_extra_doortdoor, to_city_extra_doortdoor)

emissions_main_distance_df = calculate_emissions_main_distance(df_tab2_transport, df_emissions_db_input)

st.write(emission_transfer_df)
st.write(emissions_main_distance_df)

emissions_df_full = pd.concat((emission_transfer_df,emissions_main_distance_df), ignore_index=True)

st.write(emissions_df_full)



# Distance + DTD input + Transport -> funkce na kalkulování výsledků -> asi vracet jako DF (tabulku) -> a pak napsat parsovací def funkci pro konkrétně vybraný typ transportu transportu (uvažovat genericky)     -> DF půjde do TAB 3 a variables pro particular transport do TAB 1


# Graf a DF interprtaci, něco pěknýho - nějakou def na to napsat a tu si pak volat z F7 a zobrazit na UI TAB 3 GoGreen -> UI si pak napsat v F7 přímo pod TAB 3 a jenom použít variables a vstupy odsud

