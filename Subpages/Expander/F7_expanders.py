import streamlit as st
import pandas as pd
from Subpages.Data.F7_input_data import TRANSPORT_SPEED, UNIT_DISTANCE
from Subpages.Resources import Assets


def display_expander_city_overview(
  at: pd.DataFrame,
  cz: pd.DataFrame,
  de: pd.DataFrame,
  sk: pd.DataFrame,
  pl: pd.DataFrame     
):
    with st.expander("City overview", icon = ":material/pin_drop:"):

        st.write("")

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "CZ",
            "SK",
            "AT",
            "DE",
            "PL"
        ])

        with tab1:
            st.write("- **Czech Republic:**")
            st.write("")
            st.image("Pictures/Function_7/F7_cities_cz.svg")
            st.write("")
            st.dataframe(cz)
        
        with tab2:
            st.write("- **Slovakia:**")
            st.write("")
            st.image("Pictures/Function_7/F7_cities_sk.svg", width= 520)
            st.write("")        
            st.dataframe(sk)

        with tab3:
            st.write("- **Austria:**")
            st.write("")
            st.image("Pictures/Function_7/F7_cities_at.svg", width= 520)
            st.write("")
            st.dataframe(at)

        with tab4:
            st.write("- **Germany:**")
            st.write("")
            st.image("Pictures/Function_7/F7_cities_de.svg", width= 420)
            st.write("")
            st.dataframe(de)

        with tab5:
            st.write("- **Poland:**")
            st.write("")
            st.image("Pictures/Function_7/F7_cities_pl.svg", width= 420)
            st.write("")
            st.dataframe(pl)

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

def display_expander_train(
  at: pd.DataFrame,
  cz: pd.DataFrame,
  de: pd.DataFrame,
  sk: pd.DataFrame,
  pl: pd.DataFrame,       
):
  with st.expander("Train / Rails", icon=":material/train:"):

      st.write("")
      st.write(f"""- Average speed: **{TRANSPORT_SPEED['train']} km/h**""")
      st.write("""
      -   Train does **not need breaks** for the driver (in comparison with Truck)
          - The transport planning includes also **change of the drivers**, if it is that long
          - Train jurney is **not** interrupted by mandatory breaks  
      """)

      st.write("""- But is **less flexible** - Only some cities connected by rails""")


      tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "CZ",
            "SK", 
            "AT",
            "DE",
            "PL"
      ])

      with tab1:
            st.write("")
            st.image("Pictures/Function_7/F7_train_cityname_cz.svg", width = 580)
            st.write("")
            st.dataframe(cz)

      with tab2:
            st.write("")
            st.image("Pictures/Function_7/F7_train_cityname_sk.svg", width = 460)
            st.write("")
            st.dataframe(sk)

      with tab3:
            st.write("")
            st.image("Pictures/Function_7/F7_train_cityname_at.svg", width = 430)
            st.write("")
            st.dataframe(at)

      with tab4:
            st.write("")
            st.image("Pictures/Function_7/F7_train_cityname_de.svg", width = 360)
            st.write("")
            st.dataframe(de)

      with tab5:
            st.write("")
            st.image("Pictures/Function_7/F7_train_cityname_pl.svg", width = 410)
            st.write("")
            st.dataframe(pl)


def display_expander_air(
  at: pd.DataFrame,
  cz: pd.DataFrame,
  de: pd.DataFrame,
  sk: pd.DataFrame,
  pl: pd.DataFrame,       
):

  with st.expander("Airplane", icon=":material/travel:"):
      st.write("")
      st.write(f"""- Average speed: **{TRANSPORT_SPEED['airplane']} km/h**""")
      st.write("""- Very expensive but fast -> Beneficial for time critical goods/transports""")
      st.write("""- Only some cities connected""")
      ''

      tab1, tab2, tab3, tab4, tab5 = st.tabs([
          "CZ",
          "SK",
          "AT",
          "DE",
          "PL"        
      ])

      with tab1:       
            st.write("")
            st.image("Pictures/Function_7/F7_air_cityname_cz.svg", width = 580)
            ''
            st.dataframe(cz)

      with tab2:
            st.write("")
            st.image("Pictures/Function_7/F7_air_cityname_sk.svg", width = 460)
            st.write("")
            st.dataframe(sk)

      with tab3:
          st.write("")
          st.image("Pictures/Function_7/F7_air_cityname_at.svg", width = 430)
          st.write("")
          st.dataframe(at)

      with tab4:
            st.write("")
            st.image("Pictures/Function_7/F7_air_cityname_de.svg", width = 360)
            st.write("")
            st.dataframe(de)

      with tab5:
            st.write("")
            st.image("Pictures/Function_7/F7_air_cityname_pl.svg", width = 410)
            st.write("")
            st.dataframe(pl)

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

def display_expander_currency_and_rate(
    usd_to_czk_rate: float,
    usd_to_eur_rate: float,
    criteria_dataset_kc: pd.DataFrame,
    criteria_dataset_eur: pd.DataFrame,
    default_costs_kc: pd.DataFrame,
    default_costs_eur: pd.DataFrame 
):
    with st.expander("Currency and rate - API", icon = ":material/payments:"):
        st.write("")
        st.write("")
        col_r1,col_r2 = st.columns(2)

        col_r1.metric(label="USD to CZK", value= usd_to_czk_rate)

        col_r2.metric(label="USD to EUR", value= usd_to_eur_rate)

        st.write("")
        st.write("- This is a **dynamic part** - API based")
        st.write("- **Exchange rate of the day** influences the costs/price within calculations")


        st.write("")
        tab1, tab2 = st.tabs([
            "Koruna",
            "Euro"
        ])

        with tab1:
            st.write("###### CZ - koruna:")
            st.dataframe(criteria_dataset_kc, hide_index=True)
            st.write("")

            st.write("Overview:")
            st.write("""
                - These **1-unit** costs per transport type have been set for **default** rate ( 21 <= x < 22 ) for **Standard** delivery service
                """)
            st.caption(f"**1 unit is approximatelly ~ {UNIT_DISTANCE} km** (but not always - there are some variables/coeficients making calculation corrections, depending on case City A to City B)")

            col1,col2 = st.columns(2)
            col1.dataframe(default_costs_kc, hide_index=True, width='stretch')

            st.write("""
                - In case that the **rate is in** this range the application calculates with these **default** values
                - In case that the **rate is different** the relevant % increas/decrease is calculated **from the default values**
                """)


        with tab2:
            st.write("###### SK, AT, DE, PL - euro:")
            st.dataframe(criteria_dataset_eur, hide_index=True)
            st.write("")

            st.write("Overview:")
            st.write("""
                - These **1-unit** costs per transport type have been set for **default** rate ( 0.82 <= x < 0.87 ) for **Standard** delivery service
                """)
            st.caption(f"**1 unit is approximatelly ~ {UNIT_DISTANCE} km** (but not always - there are some variables/coeficients making calculation corrections, depending on case City A to City B)")


            col1,col2 = st.columns(2)
            col1.dataframe(default_costs_eur, hide_index=True, width='stretch')

            st.write("""
                - In case that the **rate is in** this range the application calculates with these **default** values
                - In case that the **rate is different** the relevant % increas/decrease is calculated **from the default values**
                """)