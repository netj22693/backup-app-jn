import streamlit as st



st.write("# Use Cases & Metrics:")

''
''

tab_1, tab_2 = st.tabs([
   "Metrics",
   "Use Cases"
])

with tab_1.container(border=True):
    
   st.write("###### Airplane")

   st.write("""
      - Possible combinations - **120** (16 cities)
            """)

   ''
   st.write("Divergence")

   col_m_1, col_m_2, col_m_3 = st.columns(3)

   col_m_1.metric(label="0 - 15 km", value="83.3 %", delta="Great", delta_color="normal")

   col_m_2.metric(label="15 - 20 km", value="13.3 %", delta="Good", delta_color="normal")

   col_m_3.metric(label="20+ km", value="3.3 %", delta="Acceptable", delta_color="off")


   with st.expander("Measurement", icon= ":material/architecture:"):
      

    st.image("Pictures/Function_7/F7_Metrics/Logo_Google_maps.svg", width=120)

    ''
    st.write("- Google My Maps - Measure distances and areas feature")

    st.image("Pictures/Function_7/F7_Metrics/F7_metrics_air_prague_wroclav_2.png")


   with st.expander("Detail", icon= ":material/info:"):
      st.write("- **30** combinations tested")

      st.image("Pictures/Function_7/F7_Metrics/F7_metrics_legend_air_5.svg")
      
      ''
      st.image("Pictures/Function_7/F7_Metrics/F7_metrics_table_air_dr.svg")


with tab_1.container(border=True):
    
   st.write("###### Truck & Train")

   st.write("""
      - **Note**: The **accuracy of result** is influenced by:
         - The coordinate system is based on units - **1 unit ~ 30 km**
         - It is quite hard to mathematically predict the distance because of **infrustructure** in real world and **detours**
      """)
   
   st.write("""
      - **Thus, distance with divergence till +/- 30 km, I take as success result**
      """)
   
   ''
   st.write("""
      - Possible combinations
         - Truck: **1326** (52 cities)
         - Train: **1056** (33 cities)
            """)

   ''
   st.write("Divergence - Distance **till** 450 km:")

   col_m_1, col_m_2, col_m_3 = st.columns(3)

   col_m_1.metric(label="0 - 20 km", value="76.7 %", delta="Great", delta_color="normal")

   col_m_2.metric(label="20 - 30 km", value="13.7 %", delta="Good", delta_color="normal")

   col_m_3.metric(label="30 - 40 km", value="9.6 %", delta="Acceptable", delta_color="off")


   ''
   ''
   st.write("Divergence - Distance **above** 450 km:")

   col_m_1, col_m_2, col_m_3 = st.columns(3)

   col_m_1.metric(label="0 - 30 km", value="74.0 %", delta="Great", delta_color="normal")

   col_m_2.metric(label="30 - 35 km", value="14.0 %", delta="Good", delta_color="normal" )

   col_m_3.metric(label="35 - 40 km", value="12.0 %", delta="Acceptable", delta_color="off")



   with st.expander("Measurement", icon= ":material/architecture:"):
      
      st.image("Pictures/Function_7/F7_Metrics/Logo_Google_maps.svg", width=120)


      st.write("""
         -  The distance is compared against Google maps   
         """)
      
    
      ''
      st.image("Pictures/Function_7/F7_Metrics/F7_metrics_graz_pardubice.png")


   with st.expander("Important note(!) - **Train**", icon= ":material/train:"):
        
        st.write("""
        - Train has **the same distance** as Truck
        - Train has the same calculation method of distance as Truck 
         """)
      
   
   with st.expander("Detail - Distance **till** 450 km", icon= ":material/info:"):
      st.write("- **73** combinations tested")

      st.image("Pictures/Function_7/F7_Metrics/F7_metrics_legend_lessthan450_3.svg")

      ''
      st.image("Pictures/Function_7/F7_Metrics/F7_metrics_table_lessthan450_dr.svg")


   with st.expander("Detail - Distance **above** 450 km", icon= ":material/info:"):
      st.write("- **50** combinations tested")

      st.image("Pictures/Function_7/F7_Metrics/F7_metrics_legend_morethan450_3.svg")

      ''
      st.image("Pictures/Function_7/F7_Metrics/F7_metrics_table_morethan450_dr.svg")


# ============================  Use Cases part  ===================================================

tab_2.write("""""")
tab_2.write("""
- **Few examples** of what is the **Transport difference**
- What results **can be achieved** using the Function 7
- Use Case - UC 
""")

''
tab_2.write("""""")
tab_2.write("""
- **Note(!)**: The costs/price is influenced by actual exchange rate -> **can change in time** (API)
""")


tab_2.write("""""")
tab_2.write("""""")


tab_2_1_1, tab_2_1_2, tab_2_1_3, tab_2_1_4 = tab_2.tabs([
      "UC1",
      "UC2",
      "UC3",
      "UC4"
   ])

# UC1

tab_2_1_1.write("""""")
tab_2_1_1.write("###### UC1 - Speed of Transport")

tab_2_1_1.write("""""")
with tab_2_1_1.container(border= True):

   st.write("**Basic**")

   st.write("""
   - Prague (CZ) - Brno (CZ)
   """)


   ''
   st.image("Pictures/Function_7/F7_Use_Case/F7_metrics_UC1_legend.svg", width=400)
   ''
   st.image("Pictures/Function_7/F7_Use_Case/F7_metrics_UC1_basic.svg")

   ''
   st.write("""
   - Truck is a little bit slower than Train (minimum on such distance)
   - Train is cheaper than Truck (Airplane very expensive)
   """)

   st.write("""
   - But Truck (when **Standard** service) needs less time for administration -> Can be at the end in the destination by **15 hours earlier**
   """)

   st.write("""
   - **Game changer** can be seen if you need **Express** delivery
   - Truck and Train are still for reasonable price and delivery time is getting significantly shorter
   - In case of **real urgency**, **Airplane** wins but the **price is very high**
   """)

   ''
   st.image("Pictures/Function_7/F7_Use_Case/F7_metrics_UC1_basic_express.svg")




with tab_2_1_1.container(border= True):

   st.write("**Advanced**")

   st.write("""
   - The same scenario as Basic, but within **much longer distance**
   """)

   st.write("""
   - Munich (DE) - Wroclav (PL)
   """)

   ''
   st.image("Pictures/Function_7/F7_Use_Case/F7_metrics_UC1_legend.svg", width=400)
   ''
   st.image("Pictures/Function_7/F7_Use_Case/F7_metrics_UC1_advanced.svg")

   ''
   st.write("""
   - Truck needs 32 hours for administration and Train 48 hours -> this time difference is **minimized on longer distances (700+ km)** because **Truck has mandatory breaks**
   - Thus **Train** now reaches basically **the same time for delivery as Truck** and is **still cheaper**
   - Airplane is still not reasonable for such case of **Standard** delivery
   """)

   st.write("""
   - **Game changer** again is **Express** service of delivery
   - The time difference between Truck and Train is getting bigger -> **Train 8 hours earlier**
   - Again Airplane is significantly fastest, but again also the price is very high
   """)

   ''
   st.image("Pictures/Function_7/F7_Use_Case/F7_metrics_UC1_advanced_express.svg")






# UC2

tab_2_1_2.write("""""")
tab_2_1_2.write("###### UC2 - Cost save -> Slow delivery")

tab_2_1_2.write("""""")
with tab_2_1_2.container(border= True):

   ''
   st.write("""
   - **Price can be significantly reduced** in case of **Slow** delivery selected
   - If it is **not time sensitive delivery** and can be planned in advance -> **significant cost amount can be saved**
   """)

   ''
   st.image("Pictures/Function_7/F7_Use_Case/F7_metrics_UC1_legend.svg", width=400)

   ''
   st.write("**Medium distance** - Prague (CZ) - Linz (AT)")
   st.image("Pictures/Function_7/F7_Use_Case/F7_metrics_UC2_medium.svg")

   ''
   ''
   st.write("**Longer distance** - Munich (DE) - Wroclav (PL)")
   st.image("Pictures/Function_7/F7_Use_Case/F7_metrics_UC2_longer.svg")


# UC3

tab_2_1_3.write("""""")
tab_2_1_3.write("###### UC3 - Door-to-Door delivery impact")

tab_2_1_3.write("""""")
with tab_2_1_3.container(border= True):

   st.write("**Basic**")
   st.write("""
   - Graz (AT) - Prague (CZ)
   """)

   ''
   st.image("Pictures/Function_7/F7_Use_Case/F7_metrics_UC3_basic_legend.svg", width= 450)

   ''
   ''
   ''
   st.image("Pictures/Function_7/F7_Use_Case/F7_metrics_UC3_basic.svg")

   ''
   st.write("""
   - To see how **DTD influences the time and price**
   - For **Train** and **Airplane** there needs to be a shipment transfer to Truck to make the DTD -> increases time and price
   """)


with tab_2_1_3.container(border= True):

   st.write("**Advanced**")

   st.write("""
   - Kosice (SK) - Würzburg (DE)
   """)

   ''
   st.image("Pictures/Function_7/F7_Use_Case/F7_metrics_UC3_advanced_legend.svg", width= 510)


   ''
   ''
   ''
   st.image("Pictures/Function_7/F7_Use_Case/F7_metrics_UC3_advanced.svg")


   ''
   st.write("""
   - **Truck** needs to follow mandatory breaks (11.5 hours for that long distance) but still will be **faster** specifically due to shorter time for administration (32 hours)
   - **Train** does not need mandatory breaks but in case of DTD, there is **2x shipment transfer** (Truck -> Train and then Train -> Truck), which **costs more and needs extra time** (2 hours in this case), but the **Train will be at the end significantly cheaper still**. 
   """)

# UC4
tab_2_1_4.write("""""")
tab_2_1_4.write("###### UC4 - Edge case")

tab_2_1_4.write("""""")
with tab_2_1_4.container(border= True):

   st.write("**Door-to-Door causes 10 hours break**")

   st.write("""
   - Most (CZ) - Poprad (SK)
   """)

   ''
   st.image("Pictures/Function_7/F7_Use_Case/F7_metrics_UC4_legend.svg", width= 410)

   ''
   ''
   ''
   st.image("Pictures/Function_7/F7_Use_Case/F7_metrics_UC4.svg")

   ''
   st.write("""
   - Case when **DTD can have a significant impact on delivery**
   - **Why?** Because the distance **Most (CZ) - Poprad (SK) itself** takes **9.46 hours of driving** (which applies an driving exception for distances till 10 hours - can be covered with 2x 45 minutes break). But in case of **DTD 20 km**, it extends the driving time to more than 10 hours -> **the driver needs to take 10 hours break after 9 hours of driving**
   """)


# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
	label = "Function 7",
	page="Subpages/F7_FUNCTION_transport.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/play_circle:"
	) 

st.page_link(
    label = "Previous page",
	page="Subpages/F7_description_dtd.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/west:",
	) 