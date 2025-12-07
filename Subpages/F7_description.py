import streamlit as st



# Python code TIME for vsibility

python_time_if = """
def adjust_delivery_time(dt):

    hour = dt.hour

    # First condition, TIME/HOURS. 
    # If 22:00 - 23:59 -> move to 07:00 next day
    # If 00:00 - 06:59 -> move to 07:00 same day 

    if hour >= 22:
        adjusted_dt = (dt + timedelta(days=1)).replace(hour=7, minute=0, second=0, microsecond=0)

    elif 0 <= hour < 7:
        adjusted_dt = dt.replace(hour=7, minute=0, second=0, microsecond=0)

    else:
        adjusted_dt = dt

    # Second condition. DAY 
    # If Saturday (5) -> Monday 10:00  
    # If Sunday (6) -> Monday 10:00  

    weekday = adjusted_dt.weekday()
    hour_2 = adjusted_dt.hour

    if weekday == 5:   
        adjusted_dt = (adjusted_dt + timedelta(days=2)).replace(hour=10, minute=0, second=0, microsecond=0)

    elif weekday == 6: 
        adjusted_dt = (adjusted_dt + timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)

    # If Monday (0) 07:00 - 9:59 -> Monday 10:00  
    elif weekday == 0:
            if 6 < hour_2 < 10:
                adjusted_dt = dt.replace(hour=10, minute=0, second=0, microsecond=0)             

    return adjusted_dt
"""

# dictionary:

dataset_test = ({
    "Prague" : {"big" : ["4","10"], "small" : ["10","29"], "train":"y", "air":"y"},
})   



json_api = {
  "data": {
    "CZK": 20.9216533403,
    "EUR": 0.8579601337
  }
}


correction_list_data = [
    {"city1" : "Opole" , "city2" : "Linz", "distance": 623},
]

#//////////



st.write("# Description - Function 7:")

''
''
st.write("""
    - **Function 7:** Transport calculation - API provides input
    """
    )

''
with st.expander("Video guide", icon= ":material/youtube_activity:"):

    st.info("The video will be updated - currently the function offers **also generating of PDF file & inserting values inot DB** - NOT in the video yet.")
    try:
        st.video("Video/F7_videoguide_v1.mp4")
    except:
        st.warning("Apologies, the video was not loaded.")
''
''
st.write("##### Business scenario:") 

st.write("""
- **Configurator** and **calculator** of **transport cost**, **journey distance** and **lasting** of the delivery based on:
    - Transport type:
         - Truck 
         - Train 
         - Airplane 
    - Distance of journey
    - Delivery service (Express, Standard, Slow)
	- **Door-to-Door delivery** or not - more details about **DTD** on the next page
	- Shipment specifications (Insurance extra, Danger or Fragile goods)	 
"""
)

''
st.image("Pictures/Function_7/F7_desc_bpmn_customer process.svg")
''
''

tab1, tab2 = st.tabs([
	"Invoice & Payment",
    "Book the transport",
])

tab1.image("Pictures/Function_7/F7_payment_bpmn_process.svg")
''
''
tab1.image("Pictures/Function_7/F7_payment_bpmn_legend.svg", width=320)


tab2.image("Pictures/Function_7/F7_dtd_bpmn_process.svg")
''
''
tab2.image("Pictures/Function_7/F7_dtd_bpmn_legend.svg", width=520)






st.write("##### Distance calculation:") 

st.write("""
- It is based on **coordinate system** - **R1C1** type	 
- There are **2 scales/grids** which help to the calculation - **'big'** and **'small'**
"""
)

tab_g1, tab_g2 = st.tabs([
	"V2",
	"V1"
])

with tab_g1:
    ''
    st.write("""
    - **Current version** - including extra space for onboarding of more cities in the future
    """)

    ''
    st.image("Pictures/Function_7/F7_map_R1C1_V2.png")
    ''

with tab_g2:
    ''
    st.write("""
    - First version - **not used anymore**
    """)

    ''
    st.image("Pictures/Function_7/F7_map_R1C1.png")
    ''

st.write("""
- Thus when **city onboarded**, each gets **'big'** and **'small'** R1C1 coordinates
- And information about **availability of infrastructure** -> transport type y/n (* 'Truck' has 'y' as a default for every city -> thus not in the dataset)
"""
)

st.code(dataset_test, language="python", wrap_lines=True, height=80)

st.write("""
- The **calculation happens based on the 'big' and 'small' units**
"""
)

st.write("""
- **Truck & Train**:
    -   Use a logic of distributing **between 3 levels/functions** -> to get reasonable distance calculation
        - move within 1 unit 
        - move only horizontal or vertical
        - move diagonal
    - **Each has slightly different logic for calculation** (specifically, correction coeficient when it comes to diagonal move)
"""
)

st.write("""
- **Airplane**:
    -  Uses pythagorean theorem to get mathematically **the shortest distance** between cities
    - When calculated in the **Function 7**, Airplane has **shorter distance** between cities than Truck or Train
"""
)
''
st.image("Pictures/Function_7/F7_desc_bpmn_calculation_2.svg")
''
with st.expander("Correction list", icon=":material/help:"):

    st.image("Pictures/Function_7/F7_desc_bpmn_correction_list_L0.svg")
    st.write("""
    - The **Correction list Function** is used for cases when there is **not possible to calculate the distance mathematically**
    - Case when the **road is having some detours** or going through some specific cities because of **infrustructure is built like that**
    - In such cases the Coordinate system using mainly principle of looking for short distance between cities is not enough -> **this helps to get reasonable result close to the reality**
    """) 

    ''
    st.write("- Example Opole (PL) - Linz (AT):")
    
    st.image("Pictures/Function_7/F7_desc_correction_list_opole_linz.png")

    st.code(correction_list_data, language="python")

    ''
    st.write("""
    - It is of course **bi-directional**
    - This **one record** covers **both directions** Opole (PL) -> Linz (AT), the same as Linz (AT) -> Opole (PL)""")

''
''
''
st.write("##### Time calculation:") 

st.write("- Overview of variables from which the time result is created")

''
st.image("Pictures/Function_7/F7_desc_time_variables.svg")

''
tab_tc1, tab_tc2, tab_tc3, tab_tc4 = st.tabs([
    "End-to-End delivery time",
    "Expected delivery time",
    "DTF - Delivery Time Frame",
    "Agreed time for offer approval"
])

''
with tab_tc1:
    st.write("""
            - **End-to-End delivery time**:
                - Time to cover **administration once offer approved by customer** (Administration)
                - Time to cover **physical move of the shipment** (Transport)
            """)
    
    st.image("Pictures/Function_7/F7_desc_variables_e2e_time_2.svg")

    st.write("""
            - It is a combination of inputs/variables dependent on user case/business scenario
            - DTD stands for Door-To-Door delivery
            """)

    ''
    st.image("Pictures/Function_7/F7_desc_bpmn_time_process.svg")


    ''
    ''
    tab_time1, tab_time2, tab_time3 = st.tabs([
        "Driver's breaks - expanded",
        "Table - Time for administration & load, etc.",
        "Table - DTD variables"
    ])

    with tab_time1:
        st.image("Pictures/Function_7/F7_desc_bpmn_time_driver_breaks.svg", width=600)

    with tab_time2:
        st.image("Pictures/Function_7/F7_desc_variables_admin_time.svg")
        st.image("Pictures/Function_7/F7_desc_bpmn_time_table.svg", width=550)
        ''
        ''
        ''
        ''
        ''

    with tab_time3:
        st.image("Pictures/Function_7/F7_desc_bpmn_time_addTime_table.svg", width=550)
        ''

    ''
    with st.expander("Use Cases/Examples", icon= ":material/help:"):


        st.write("""
        - **Use Case 1**: 
            - Delivery A to B - **Train** or **Airplane**
            - Door-to-Door: **No**     
        """)

        tab_uc_1_1, tab_uc_1_2 = st.tabs([
            "Diagram",
            "Calculation"
        ])
        ''
        tab_uc_1_1.image("Pictures/Function_7/F7_desc_bpmn_time_example_1.svg")


        tab_uc_1_2.write("""
        **Innsbruck (AT)** -> **Prague (CZ)** - **Train**
        """)
        
        tab_uc_1_2.write("""
        - Service - **Standard**: **48 hours** (Train)
        - Time to cover Innsbruck to Prague (A to B): **6.63 hours**
        - **Total time: 54.63 hours**
        """)



        ''
        ''
        st.write("""
        - **Use Case 2**: 
            - Delivery A to B - **Truck**
            - Door-to-Door: **Yes - B destination**     
        """)

        tab_uc_2_1, tab_uc_2_2 = st.tabs([
            "Diagram",
            "Calculation"
        ])

        ''
        tab_uc_2_1.image("Pictures/Function_7/F7_desc_bpmn_time_example_2.svg")

        tab_uc_2_2.write("""
        **Innsbruck (AT)** -> **Prague (CZ)** - **Truck**
        """)

        tab_uc_2_2.write("""
        - Service - **Standard**: **32 hours** (Truck)
        - Time to cover Innsbruck to Prague (A to B): **7.57 hours**
        - Door-to-Door: dtd B 10 km: **0.42 hour**
        - Mandatory breaks: **0.75 hour**
        - **Total time: 40.74 hours**
        """)



        ''
        ''
        st.write("""
        - **Use Case 3**: 
            - Delivery A to B - **Train** or **Airplane**
            - Door-to-Door: **Yes - B destination + need of shipment transfer to Truck**     
        """)


        tab_uc_3_1, tab_uc_3_2 = st.tabs([
            "Diagram",
            "Calculation"
        ])

        ''
        tab_uc_3_1.image("Pictures/Function_7/F7_desc_bpmn_time_example_3.svg")


        tab_uc_3_2.write("""
        **Innsbruck (AT)** -> **Prague (CZ)** - **Train**
        """)

        tab_uc_3_2.write("""
        - Service - **Standard**: **48 hours** (Train)
        - Time to cover Innsbruck to Prague (A to B): **6.63 hours**
        - Door-to-Door: dtd B 10 km
        - Transfer to Truck: **1 hour** + Truck to cover the distance: **0.42 hour**
        - **Total time: 56.05 hours**
        """)



        ''
        ''
        st.write("""
        - **Use Case 4**: 
            - Delivery A to B - **Truck**
            - Door-to-Door: **Yes - A and B destinations**  
        """)

        tab_uc_4_1, tab_uc_4_2 = st.tabs([
            "Diagram",
            "Calculation"
        ])


        ''
        tab_uc_4_1.image("Pictures/Function_7/F7_desc_bpmn_time_example_4.svg")

        tab_uc_4_2.write("""
        **Innsbruck (AT)** -> **Prague (CZ)** - **Truck**
        """)

        tab_uc_4_2.write("""
        - Service - **Standard**: **32 hours** (Truck)
        - Time to cover Innsbruck to Prague (A to B): **7.57 hours**
        - Door-to-Door: dtd A 20 km & dtd B 20 km: **1.50 hour**
        - Mandatory breaks: **1.5 hour**
        - **Total time: 42.57 hours**
        """)

with tab_tc2:

    st.write("""
        - Is calculated as:
             """)

    st.image("Pictures/Function_7/F7_desc_variables_delivery_time_2.svg")

    st.write("""
        - **Expected delivery time** is then checked, if it is in **Delivery Time Frame (DTF)**
             - **If yes**, the calculated date & time **is kept** and displayed to user
             - **If not**, the calculated date & time **is adjusted** to fit to the DTF
             """)
    
    with st.expander("DTF - Delivery Time Frame", icon=":material/info:"):
        st.write(f"""
                    - Monday: **10:00 - 22:00**
                    - Tuesday - Friday : **07:00 - 22:00**
                    - Saturday & Sunday: No delivery ->  **Monday: 10:00**
                """)   
        
        st.write("- In case that **calculated Expected delivery time** is **not** in these time frames -> **the delivery time is adjusted to fit into these**  and displayed to user")

    ''
    st.write("""
        - The application uses time based on **python libraries 'time' and 'datetime'** (actual time and delta principle)
             """)

    ''
    st.image("Pictures/Function_7/F7_desc_uml_time.svg")


with tab_tc3:

    with st.container(border=True):
        st.write(f"""
                    - Monday: **10:00 - 22:00**
                    - Tuesday - Friday : **07:00 - 22:00**
                    - Saturday & Sunday: No delivery ->  **Monday: 10:00**
                """)   

  
    st.write(f"""
                    - If the **calculated Expected delivery time and date**:
                        - **Fits** into the Frame -> it is not changed
                        - **Does not fit** into the Frame -> it is changed accordingly to the logic
                """)  

    st.image("Pictures/Function_7/F7_desc_time_dtf.svg")

    ''
    with st.expander("DTF - Examples", icon= ":material/info:"):

        st.write("""
                 - Example 1:
                    - **Calculated**: Wednesday - 17-Sep-25 by 19:58
                    - **Changed to**: no change
                 """)
        
        st.write("""
                 - Example 2:
                    - **Calculated**: Wednesday 17-Sep-25 - 04:22
                    - **Changed to**: Wednesday - 17-Sep-25 - **07:00**
                    - **Reason**: no delivery by 04:00
                 """)

        st.write("""
                 - Example 3:
                    - **Calculated**: Saturday 20-Sep-25 - 15:48
                    - **Changed to**: **Monday** - 22-Sep-25 - **10:00**
                    - **Reason**: no delivery Saturday and Sunday
                 """)

    with st.expander("Python code", icon=":material/code:"):
        st.code(python_time_if, language="python")

with tab_tc4:

    st.image("Pictures/Function_7/F7_desc_variables_offer_time.svg", width=190)
    
    st.write("""
                - 1 day - 24 hours
                - 2 days - 48 hours
                - 5 days - 120 hours
                - 7 days - 168 hours
            """)

    st.write("- Can be selected based on customer's need")



''
''
''
st.write("##### Price calculation:") 

st.write("""
- **The price to deliver the shipment between selected cities** (From/To) is returned from **the same def/functions together with the distance** - was influenced by:
    - Selected transport type (Truck, Train, Airplane)
    - Type of service (delivery: Express, Standard, Slow)
    - Selected currency (koruna, euro)
    - **Daily currency exchange rate - :green[API based info]**
"""
)
st.write("""
- **The final price** is then **impacted by other selected inputs** from user:
    - **Extra insurance or Fragile goods or Dange goods** (multiple select possible) - calculated based on additional user inpur (Value of the goods/shipment)
    - And whethe there is extra **Door-To-Door delivery** (more details on the next page)
"""
)

''
''
tab_p_1, tab_p_2 = st.tabs([
     "User inputs",
     "App calculation"

])

with tab_p_1:
    st.image("Pictures/Function_7/F7_desc_uml_inputs.svg")  

    ''
    with st.expander("UML diagram - more details", icon= ":material/help:"):

        st.write("""
        - What user selects **influences** what the **application offers** in the other levels - types of **business scenarios & real case logic**
        """)
        
        st.write("""
        - **L1** - API/Currency -> Influences **L4** price for Delivery service
        - **L2** - Selection of From/To cities -> influences options of Currency in **L3**
        - **L2** - Selection of From/To cities -> influences options of Transport type **L4** (not every city has all transport types possible) 
        - **L4** - Transport type -> influences options for Door-to-Door delivery in **L5**
        - **L4** - Transport type -> influences options for Extra service (Airplane cannot transfer Danger goods)  in **L5**
        """)

with tab_p_2:
    st.image("Pictures/Function_7/F7_desc_uml_tab2.svg", width = 600)

''
''
''
st.write("##### API - Exchange rate:") 
st.write("""
- **Dynamic element** in the function
- **Actuall** daily exchange rate
- It is **USD** to **EUR** (euro) and **CZK** (koruna) -> **influences the based price per unit distance -> influences the calculation input and results**
"""
)

''
with st.expander("API info", icon= ":material/help:"):

	st.write("""
	- API - **HTTP GET** request to retrieve data from a server
	- This Function 7 receives **CUSTOMIZED** data from https://freecurrencyapi.com/
	""")
	
	st.code(json_api, "json" )

	st.write("""
	- Limit: **5k** requests per month
	""")

''
''
st.image("Pictures/Function_7/F7_desc_bpmn_api_unit.svg")   


''
''
st.write("##### Currency offer:") 
st.write("""
- Countries: 
    - CZ - **koruna**
    - SK, AT, DE, PL - **euro**
"""
)

st.write("""
- Transport **inside** a country -> **currency of the country** 
"""
)

st.write("""
- Transport to **different** country:
    - **any of**: SK, AT, DE, PL -> **euro** 
    - **CZ** and **any of**: SK, AT, DE, PL -> Customer can choose: **koruna** or **euro**
"""
)

''
st.image("Pictures/Function_7/F7_desc_bpmn_currency.svg")

# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
    label = "Next page",
	page="Subpages/F7_description_variables.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/east:",
	) 
