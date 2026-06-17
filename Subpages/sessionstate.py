import pandas as pd
import streamlit as st
import pydeck as pdk

# ==== Generic function - DB connection ====
from sqlalchemy import create_engine, Engine

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


def get_map():
    df = pd.DataFrame({
        "name": ["Lannach - Industriestraße"],
        "lat": [48.2119],
        "lon": [16.4156],
        "type": ["retail"]
    })

    color_map = {
        "retail": [255, 0, 0],
        "service": [0, 0, 255]
    }

    df["color"] = df["type"].map(color_map)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_fill_color="color",
        get_radius=50,
        radius_min_pixels=6,
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
                "text": "{name}\nTyp: {type}"
            }
        )
    )


# with st.expander("Map - Locations", icon=":material/location_on:"):
#     get_map()

get_map()