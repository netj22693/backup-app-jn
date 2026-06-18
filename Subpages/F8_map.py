import pandas as pd
import streamlit as st
import pydeck as pdk


def get_map(df: pd.DataFrame):

    '''
    Visualize data on map (PINS) based on DF
    '''

    # Create new column based on data from DB (in DB saved -> RGB color scale)
    df["color"] = df[["color_r", "color_g", "color_b"]].values.tolist()

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_fill_color="color",
        get_radius=100,
        radius_min_pixels=8,
        radius_max_pixels=20,
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=49.8,
        longitude=15.5,
        zoom=4.6,
    )

    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            map_style=None,
            tooltip={
                "text": "City: {City}\nCompany: {Name}\nType: {Type}\nStreet: {Street} {No.}\nBranch ID: {Branch ID} "
            }
        )
    )
