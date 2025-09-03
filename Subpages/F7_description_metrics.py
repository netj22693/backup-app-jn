import streamlit as st



st.write("# Use Cases & Metrics")

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


   with st.expander("Measurment", icon= ":material/architecture:"):
      

    st.image("Pictures/Function_7/F7_Metrics/Logo_Google_maps.svg", width=120)

    ''
    st.write("- Google My Maps - Measure distances and areas feature")

    st.image("Pictures/Function_7/F7_Metrics/F7_metrics_air_prague_wroclav_2.png")


   with st.expander("Detail", icon= ":material/info:"):
      st.write("- **30** combinations tested")

      st.image("Pictures/Function_7/F7_Metrics/F7_metrics_legend_air.svg")
      ''
      st.image("Pictures/Function_7/F7_Metrics/F7_metrics_air.png")



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



   with st.expander("Measurment", icon= ":material/architecture:"):
      
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

      st.image("Pictures/Function_7/F7_Metrics/F7_metrics_legend_lessthan450_2.svg")

      ''
      st.image("Pictures/Function_7/F7_Metrics/F7_metrics_lessthan450.png")
   


   with st.expander("Detail - Distance **above** 450 km", icon= ":material/info:"):
      st.write("- **50** combinations tested")

      st.image("Pictures/Function_7/F7_Metrics/F7_metrics_legend_morethan450_2.svg")

      ''
      st.image("Pictures/Function_7/F7_Metrics/F7_metrics_morethan450.png")



tab_2.info("This section is under build - to be available soon :)")



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