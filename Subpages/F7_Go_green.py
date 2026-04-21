import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import Engine

def call_go_green(db_engine: Engine, from_city_extra_doortdoor: float, to_city_extra_doortdoor: float, df_tab2_transport: pd.DataFrame, selected_transport: str):


    def create_df_emissions(engine: Engine) -> pd.DataFrame:

        query = """
        SELECT 
            f.label,
            l.emission,
            l.unit
        FROM function7.transport_type f
            INNER JOIN function7.go_green_emissions l ON (f.transport_id = l.transport_id)
        ORDER BY f.label IN ('Transfer'), f.label ASC;
        """
        
        return pd.read_sql(query, engine)

    def get_emission_unit_value_truck(df: pd.DataFrame) -> float:

        for index, row in df.iterrows():
            if row["label"] == "Truck":
                emission_value = row["emission"]

        return emission_value

    def calculate_emission_transfer(df: pd.DataFrame, dtd_from: float, dtd_to: float) -> pd.DataFrame | float | bool:

        # Loop to get emission value for 'Transfer' - applicable when DTD 
        for index, row in df.iterrows():
            if row["label"] == "Transfer":
                emission_value = row["emission"]

        if dtd_from > 0 and dtd_to > 0:
            result = 2 * emission_value
        
        elif dtd_from > 0 or dtd_to > 0:
            result = emission_value
        
        else:
            result = 0

        return result, emission_value
    

    def calculate_dtd_emissions(distance: float, emission: float) -> float:

        return distance * emission

        
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
    

    def extend_emissions_dtd_transfer_df(df: pd.DataFrame, transfer_value: float, truck_value: float,dtd_from: float, dtd_to:float):
        
        '''
        - Extension of DF
        - Adding DTD columns
        - Adding Transfer column + where logic
        - Adding Total column + where logic
        - Returns full df with all these columns (if DTD 0 -> values 0)
        '''

        df["DTD From"] = dtd_from * truck_value
        df["DTD To"] = dtd_to * truck_value

        rule_truck = df["Transport type"] == "Truck"
        variable = df["DTD From"] + df["DTD To"]

        # If 'Truck' -> nan, Else transfer_value
        df["Transfer"] = np.where(
            rule_truck,
            0, # np.nan
            transfer_value
        )
        # If 'Truck' -> keep CO2 value, else CO2 value + variable + transfer_value
        df["Total"] = np.where(
            rule_truck,
            df["CO2"]+ variable,
            df["CO2"]+ variable + transfer_value
        )

        return df
    
    def df_rounding(df: pd.DataFrame) -> pd.DataFrame:

        cols = ["CO2", "DTD From", "DTD To", "Transfer", "Total"]
        return df.round({col: 2 for col in cols})
    

    def styling_df(df: pd.DataFrame) -> pd.DataFrame:

        df = df.rename(columns={
            "label": "Transport type",
            "emission": "Emission",
            "unit": "Unit",
            "CO2":"Calculated CO₂",
            "Total" : "Total kg CO₂ / km"
        })

        df = df.style.format({
            "Emission": "{:,.2f}",
            "Transfer": "{:,.2f}",
            "Total kg CO₂ / km": "{:,.2f}",
            "Calculated CO₂": "{:,.2f}",
            "DTD From": "{:,.2f}",
            "DTD To": "{:,.2f}"
        })

        return df

    def create_dict_for_db(df: pd.DataFrame, transport: str) -> dict:

        row = df.loc[df["Transport type"] == transport].iloc[0]

        result = {
            "main_route": float(row["CO2"]),
            "from_dtd": float(row["DTD From"]),
            "to_dtd": float(row["DTD To"]),
            "transfer": float(row["Transfer"]),
            "total": float(row["Total"])
        }

        return result

    # ======== FUNCTION EXECUTION ========

    # Query into DB -> to get emissions from go_green_emissions table -> DF
    df_emissions_db = create_df_emissions(db_engine)

    # Get emission value truck -> for DTD purposes
    emission_unit_truck = get_emission_unit_value_truck(df_emissions_db)

    # Styled version for UI purposes
    df_emissions_db_styled = styling_df(df_emissions_db)

    # To get emission value for 'Transfer'
    emission_transfer, emission_value = calculate_emission_transfer(df_emissions_db, from_city_extra_doortdoor, to_city_extra_doortdoor)

    # To get emission values for selected distances per transport types + DTD 
    emission_dtd_from = calculate_dtd_emissions(from_city_extra_doortdoor, emission_value)
    emission_dtd_to = calculate_dtd_emissions(to_city_extra_doortdoor, emission_value)
    
    emissions_main_distance_df = calculate_emissions_main_distance(df_tab2_transport, df_emissions_db)

    # Extending by DTD and Transfere values
    emissions_all_df  = extend_emissions_dtd_transfer_df( emissions_main_distance_df, emission_transfer, emission_unit_truck, emission_dtd_from, emission_dtd_to)

    emissions_all_df_rounded = df_rounding(emissions_all_df)

    # Styled version for UI purposes
    emissions_main_distance_df_styled = styling_df(emissions_all_df_rounded)

    # Creation of dictionary from the final DF (not styled one) for DB save
    dict_variables_for_db = create_dict_for_db(emissions_all_df_rounded, selected_transport)

    return emissions_all_df_rounded, emissions_main_distance_df_styled, df_emissions_db, df_emissions_db_styled, dict_variables_for_db

