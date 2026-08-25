import streamlit as st
import pandas as pd
from Subpages.F7b_operational_functions import singular_or_plural

def display_offer_visualization_ui(
        ui_image_path: str,
        ui_color_coding_image_path: str,
        offer_id: str,
        row_offer: pd.Series,
        row_delivery: pd.Series,
        row_costs: pd.Series,
        row_extra_steps_time: pd.Series,
        row_sla: pd.Series
    ):

    st.write(f"""
        - Offer number: **{offer_id}**
        - Offer created: **{row_offer["created_date"]} - {row_offer["created_time"]} {row_offer["time_zone"]}**
        - Customer to approve till: **{row_offer["need_approve_date"]} {row_offer["need_approve_time"]} - {row_offer["time_zone"]}** ({row_offer["need_approve_days"]} day{singular_or_plural(row_offer["need_approve_days"])})
    """)

    # UI transport workflow image
    st.write("")
    try:
        st.image(ui_image_path)

    except Exception as e:
        print(e)
        st.warning("Failed to load image")
    
    # Expander 
    with st.expander("Transfer process", icon= ":material/help:"):
        try:
            st.image(ui_color_coding_image_path)

        except Exception as e:
            print(e)
            st.warning("Failed to load image")
        

        # To show DTD button or not
        if row_delivery["from_dtd"] > 0 or row_delivery["to_dtd"] > 0:

            st.write("- More info about DTD:")
            
            st.link_button(
                label = "Go to Door-to-Door page",
                url="https://dataparsing.streamlit.app/F7_description_dtd",
                help="The button will redirect to the relevant page within this app for download.",
                width="stretch",
                icon=":material/launch:"
            )                       

    st.write("")
    st.write("")
    st.write(f"""
        - Delivery from **{row_delivery["from_city"]} ({row_delivery["from_country"]})** to **{row_delivery["to_city"]} ({row_delivery["to_country"]}):**
            - Costs: **{row_costs["distance_cost"]:,.2f} {row_offer["currency"]}**
            - Distance: **{row_delivery["distance_length"]:,.2f} km**
            - Time to cover the distance: **{row_delivery["distance_time"]:.2f} hour(s)**
            - Transport type: **{row_offer["transport"]}**
    """)


    # Different UI for Truck and Train or Airplane
    if row_offer["transport"] == 'Truck':

        st.write("")
        st.write(f"""
            - **Door-to-Door**:
                - Additional: **{row_delivery["from_dtd"] + row_delivery["to_dtd"]} km** to the distance
                    - {row_delivery["from_city"]}: {row_delivery["from_dtd"]} km
                    - {row_delivery["to_city"]}: {row_delivery["to_dtd"]} km
                - Time to cover the Door-to-Door: **{row_delivery["dtd_time"]:.2f} hours(s)**
        """)

        st.write("")
        st.write(f"""
        - **{row_offer["transport"]}**:
            - Selected service **{row_offer["service"]}** requires **{row_sla["time_sla"]:.2f} hours** for administration, load, etc. - **the SLA**  
            - If longer distance (including Door-to-Door time), **mandatory breaks** for driver: **{row_extra_steps_time["truck_breaks"]:.2f} hour(s)**
        """)

    if row_offer["transport"] in ("Train", "Airplane"):

        st.write("")
        st.write(f"""
        - **Door-to-Door**:
            - Additional: **{row_delivery["from_dtd"] + row_delivery["to_dtd"]} km** to the distance for which **Truck is needed**
                - {row_delivery["from_city"]}: {row_delivery["from_dtd"]} km
                - {row_delivery["to_city"]}: {row_delivery["to_dtd"]} km
            - Time to cover the Door-to-Door: **{row_delivery["dtd_time"]:.2f} hours(s)**
                - Transfer {row_offer["transport"]} <-> Truck: {(row_extra_steps_time["shipment_transfer_dtd_from"] + row_extra_steps_time["shipment_transfer_dtd_to"]):.2f} hour(s)
                - Time for Truck ride: {row_extra_steps_time["dtd_truck_if_not_truck_main"]} hour(s)
        """)

        st.write("")
        st.write(f"""
        - **{row_offer["transport"]}**:
            - Selected service **{row_offer["service"]}** requires **{row_sla["time_sla"]:.2f} hours** for administration, load, etc. - **the SLA**  
        """)

    # This UI same for all types of transport
    st.write("")
    st.write("- **Overall time end-to-end delivery:**")

    with st.container(border=True):
        st.write(f"""**{row_offer["time_overall"]:.2f} hour{singular_or_plural(row_offer["time_overall"])}**""")


    st.write("- **Expected delivery:**")
    with st.container(border=True):
        st.write(f"""**{row_offer["expected_delivery"]} - {row_offer["time_zone"]}**""")


    st.write("")
    st.write("")
    st.write(f"""
    - **Additional services - costs**:
        - Insurance extra costs: **{row_costs["insurance"]:,.2f} {row_offer["currency"]}**
        - Fregile goods costs: **{row_costs["fragile"]:,.2f} {row_offer["currency"]}**
        - Danger goods costs: **{row_costs["danger"]:,.2f} {row_offer["currency"]}**
        - Door-To-Door - {row_delivery["from_city"]} ({row_delivery["from_country"]}):  **{row_costs["dtd_from"]:,.2f} {row_offer["currency"]}** - ({row_delivery["from_dtd"]} km)
        - Door-To-Door - {row_delivery["to_city"]} ({row_delivery["to_country"]}):  **{row_costs["dtd_to"]:,.2f} {row_offer["currency"]}** - ({row_delivery["to_dtd"]} km)
    """)


    st.write("")
    st.write("")
    st.write("- **Final price:**")
    with st.container(border=True):
        st.write(f"""**{row_offer["final_price"]:,.2f} {row_offer["currency"]}**""")