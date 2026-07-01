import pandas as pd
import streamlit as st
import pydeck as pdk
from pandas.io.formats.style import Styler



def get_map(df: pd.DataFrame, map_size: str):

    '''
    - Visualize data on map (PINS) based on DF
    - Variable size/setup of the map

    - "BIG" (else) - used as part of TAB 1 and TAB 2
    - "SMALL" - used as part of TAB 4
    '''
    
    # Merging RGB for map 
    df["color"] = df[["color_r", "color_g", "color_b"]].values.tolist()
 
    if map_size == "SMALL":
        
        # To have the location point in the center
        lat = df["lat"].loc[0]
        lon = df["lon"].loc[0]


        figures = {
            "get_radius": 100,
            "radius_min_pixels": 8,
            "radius_max_pixels": 20,
            "latitude": lat,
            "longtitude": lon,
            "zoom": 15,
            "height": 300,  # Default stremlit value
            "width": "100%" # Default stremlit value
        }
    
    else:
        figures = {
            "get_radius": 100,
            "radius_min_pixels": 8,
            "radius_max_pixels": 20,
            "latitude": 49.8,
            "longtitude": 15.5,
            "zoom": 4.6,
            "height": 500,  # Default stremlit value
            "width": "100%" # Default stremlit value
        }


    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_fill_color="color",
        get_radius=figures["get_radius"],
        radius_min_pixels=figures["radius_min_pixels"],
        radius_max_pixels=figures["radius_max_pixels"],
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=figures["latitude"],
        longitude=figures["longtitude"],
        zoom=figures["zoom"],
    )

    map_fig = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            map_style=None,
            tooltip={
                "text": "City: {City}\nCompany: {Name}\nStreet: {Street} {No.}\nType: {Type}\nBranch ID: {Branch ID}"
            }
        )

    # Note: "height" needs to be set as part of Streamlit component (If set as part of pdk.Deck Streamlit will not apply it)
    st.pydeck_chart(map_fig, height=figures["height"])


def df_styling_colors_per_map(df: pd.DataFrame) -> Styler:

    '''
    - Using predefined (DB) RGB figures to change color of text in DF 
    - Column "Type" (Type of Branch)
    - Has nested function du to the .apply() principle
    '''

    def style_type(row):

        r = row["color_r"]
        g = row["color_g"]
        b = row["color_b"]

        styles = [""] * len(row)
        styles[df.columns.get_loc("Pin")] = f"color: rgb({r}, {g}, {b})"
        return styles

    df_styled = df.style.apply(style_type, axis=1).hide(axis="columns")

    return df_styled