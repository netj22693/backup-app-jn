import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import Engine

def call_go_green(db_engine: Engine, from_city_extra_doortdoor: float, to_city_extra_doortdoor: float, df_tab2_transport: pd.DataFrame):


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


    def calculate_emission_transfer(df: pd.DataFrame, dtd_from: float, dtd_to: float) -> pd.DataFrame | float | bool:

        # Loop to get emission value for 'Transfer' - applicable when DTD 
        for index, row in df.iterrows():
            if row["label"] == "Transfer":
                emission_value = row["emission"]

        if dtd_from > 0 and dtd_to > 0:
            result = 2 * emission_value
            flag = True
        
        elif dtd_from > 0 or dtd_to > 0:
            result = emission_value
            flag = True
        
        else:
            result = 0
            flag = False


        # create DF
        result_df = pd.DataFrame({
            'Transport type' : ["Transfer"],
            'CO2' : [result]
        })

        return result_df, result, flag


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
    

    def extend_emissions_df(df: pd.DataFrame, value: float):
        
        '''
        - If transfer emissions applicable
        - Extension of original DF 2 columns -> 4 columns 
        - Rule for 'Truck' defined (there is no transfer)
        '''
     
        rule_truck = df["Transport type"] == "Truck"

        # If 'Truck' -> nan, Else value
        df["Transfer"] = np.where(
            rule_truck,
            np.nan,
            value
        )

        # If 'Truck' -> keep CO2 value, else CO2 value + value
        df["Total"] = np.where(
            rule_truck,
            df["CO2"],
            df["CO2"] + value
        )

        return df


    # ======== FUNCTION EXECUTION ========

    # Query into DB -> to get emissions from go_green_emissions table -> DF
    df_emissions_db_input = create_df_emissions(db_engine)

    # To get emission value for 'Transfer'
    emission_transfer_df, emission_transfer, emission_transfer_flag = calculate_emission_transfer(df_emissions_db_input, from_city_extra_doortdoor, to_city_extra_doortdoor)

    # To get emission values for selected distances per transport tzpes
    emissions_main_distance_df = calculate_emissions_main_distance(df_tab2_transport, df_emissions_db_input)

    # In case of DTD (Emissions for Transfere between Trai/Air <-> Truck) DF/table to be extended
    if emission_transfer_flag == True:
        emissions_main_distance_df  = extend_emissions_df(emissions_main_distance_df, emission_transfer)

    # In case that 
    if emission_transfer_df is not None:
        st.write("None condition?")
        emission_transfer_df.drop(emission_transfer_df.loc[emission_transfer_df['CO2']== 0].index, inplace=True)
    

    return emissions_main_distance_df

