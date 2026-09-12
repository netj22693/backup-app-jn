import streamlit as st
import pandas as pd
from Subpages.Data.F7_input_data import TRANSPORT_SPEED, UNIT_DISTANCE
from Subpages.Resources import Assets


def display_expander_transport_type_comparison():
    with st.expander("Transport type comparison", icon=":material/info:"):

        st.write("")
        st.write("""
        - There is few factors to consider:
            - Time, Costs
            - Type of Cargo 
            - Infrasture availability  
        
        """)

        st.write("")
        st.image("Pictures/Function_7/F7_transport_comparison_table.svg")


def display_expander_truck():
    with st.expander("Truck / Road", icon=":material/local_shipping:"):

        st.write("")
        st.write(f"""- Average speed: **{TRANSPORT_SPEED['truck']} km/h**""")
        st.write("""- Every city is available -> no restrictions""")
        st.write("""- But the **driver needs mandatory breaks** which can prolong the journey/delivery time""")


        st.write("")
        st.write("###### Mandatory breaks:")

        st.write("""
        - The cargo can be impacted by **mandatory breaks for the driver**
        - This also **influences the time of the delivery**
        """)
        
        st.write("""
        - **Rules/law**:
        - A driver can drive **4.5 hours** and then needs to take a **mandatory 45 minutes break**
        - A driver can drive for **9 hours a day** max.   
        - After the 9 hours mandatory **10 hours break** before continuing to drive 
        - **Exception:** in case that the distance is **within 10 hours** of driving, exception can be made                        
        """)

        st.write("")
        st.write(" -> Distance is **not** longer than **4.5 hours** - no mandatory break")
        st.write(" -> Distance is **longer** than **4.5 hours** - mandatory **45 minutes** break")
        st.write(" -> Distance is **not** longer than **9 hours** - mandatory **45 minutes** break")
        st.write(" -> Distance is **not** longer than **10 hours** (exception) - mandatory **2x  45 minutes** break")
        st.write(" -> In case that the distance is longer than **9 and 10 hours** (10+) - there is **45 minutes** break + **10 hours** break")
        
        ''
        st.caption("""
        * Example of journey between 9 - 10 hours -> the exception: Most (CZ) - Poprad (SK)
        * Example of journey longer than 9 or 10 hours with 10 hours sleep break: Teplice (CZ) - Kosice (SK) or Karlovy Vary (CZ) - Kosice (SK)
        """)


def display_expander_sla(df: pd.DataFrame):
    with st.expander("**SLA** - Service Level Agreement (Express, Standard, Slow)", icon= ":material/contract:"):
        st.write("")
        st.write(" - **Time** - Cargo on its way till this time - **HOURS**")
        st.dataframe(df, hide_index=True)

def display_expander_unit_price():
    with st.expander("Unit price", icon= ":material/info:"):

        st.write("")
        st.write("- Is a price per specific distance")
        st.write("- The function/calculation works based on **coordinate system**")
        st.write("- Unit means specific field in this coordinate system")
        st.write("- **Based on the units, distance and price is calculated**")
        st.write(f"- **1 unit is approximatelly ~ {UNIT_DISTANCE} km** (but not always - there are some variables/coeficients making calculation corrections, depending on case City A to City B)")
        st.write(f"- If the distance is **less than** ~ {UNIT_DISTANCE} km (You travel within 1 unit), the final price is calculated as 1 unit. This also helps to keep profit for the business.  Example: Teplice <-> Most")


def display_expander_extra_services(extra_service_dict: dict):
    with st.expander("Extra services - Overview", icon= ":material/info:"):

        st.write("")
        st.write("""
        - Multiple choices can be selected
        - Note: **Airplane** - Danger goods is **not allowed**
        """)

        st.write("")
        st.write(f"""
        - Costs:
            - Insurance extra -> **{extra_service_dict['insurance']}%** from shipment value
            - Fragile goods -> **{extra_service_dict['fragile']}%** from shipment value
            - Danger goods -> **{extra_service_dict['danger']}%** from shipment value
        """)

        st.image("Pictures/Function_7/F7_table_shipment_value.svg")

def display_expander_fragile_goods():
    with st.expander("Fragile goods", icon= ":material/quick_reference:"):

        ''
        st.write("""
        - Overview of goods and the common type of transport
        """)

        st.image("Pictures/Function_7/F7_table_fragile_truck_train.svg")
        st.image("Pictures/Function_7/F7_table_fragile_airplane.svg")

def display_expander_danger_goods():
    with st.expander("Danger goods", icon= ":material/warning:"):

        ''
        st.write("""
        - Overview of goods and the common type of transport
        - Note: **Airplane** - Danger goods is **not allowed**
        """)

        st.image("Pictures/Function_7/F7_table_danger_truck_train.svg")


def display_expander_door_to_door():
    with st.expander("Door-to-Door", icon= ":material/info:"):

        st.write("")
        st.write("""
        - **The point of Door-to-Door is to define whether:**
            - The transport between cities will be just from City A to City B **configured upper**
            - Or eventually from/to somewhere else within defined areas (City, ~ 10km, ~20km)
        """)

        st.write("")
        st.write(""" 
        - **Truck:**
            - **City** - everywhere within City area **for free**
            - **10 km** radius - **500 koruna** ; **20 euro**
            - **20 km** radius - **1 000 koruna** ; **40 euro**
        """)

        st.write("")
        st.write(""" 
        - **Train and Airplane:**
            - Measured from Train Station or Airport
            - **Higher price** due to need of **Truck** and **Shipment transfer**
                - **No** - pick up/delivery just from/to Train Station/Airport by Train/Airplane
                - **10 km** radius - **1 000 koruna** ; **40 euro** (Truck needed)
                - **20 km** radius - **1 500 koruna** ; **60 euro** (Truck needed)
        """)

        st.write("")
        st.write("- **More details**:")

        st.link_button(
            label = "Go to Door-to-Door page",
            url= Assets.Links.App.f7_description_dtd,
            help="The button will redirect to the relevant page within this app for download.",
            width="stretch",
            icon=":material/launch:"
        )


        st.write("")
        st.write("")
        st.write("###### Simple view/example:")

        st.image("Pictures/Function_7/F7_dtd_legend.svg")

        st.write("")
        st.image("Pictures/Function_7/F7_dtd_abb_air.svg", width= 370)

        st.write("")
        st.write(""" 
        - Selected transport between **A** and **B** - **Airplane**
        - Service **ordered** just from the **A** point ('From city') - **Airport**
        - Delivery to **B** point ('To' city) - **Airport**, but customer pays extra delivery to point **B in the area of 20km**
        """)
        st.write(""" 
        - Result:
            -  Customer will deliver the Shipment to point **A** (Airport) **on his own**
            - **A** to **B** distance (Airport to Airport) will be provided by our company (Airplane)
            - Customer pays for delivery to **B - 20km** -> our company will make a shipment transfer from **Airplane to Truck** for the last **20 km**     
        """)