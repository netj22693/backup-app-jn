import streamlit as st
from Subpages.Resources import Assets

st.write("# Description - Functions 1 & 2")
''
''

st.write(
"Purpose of these functions is to parse data from XML -> validate them -> visualize them -> and produce simple .txt sumary."
)

st.write("""
- **Function 1**: Download XML file
- **Function 2**: Parse data from the XML
"""
)

''
with st.expander("Video guide", icon= ":material/youtube_activity:"):
  try:
    st.video("Video/F2_videoguide_v2.mp4")
  except:
    st.warning("Apologies, the video was not loaded.")


''
''
st.write("##### Business scenario:") 
st.write(
"Simplified version of case when a company does a purchase from other company/e-shop on frequent bases -> XML invoice defined for invoicing."
)

st.write(" ")

st.write("##### Process:") 
st.write("""
1) Dowload XML (keep existing or you can update it) 
2) Upload XML
"""
)

''
''
st.write("##### Upload XML process:")


''
''
''
''
st.image("Pictures/Function_2/F2_BPMN_HL_v5.svg")
''
''
''


tab1, tab2, tab3, tab4 = st.tabs([
  "Validation XML & XML Schema",
  "Data parsing",
	"Data validation",
	"Data visualization"
])


with tab1:
  ''
  st.image(Assets.Images.f2_xml_xsd_validation, width=620)
  ''
  ''
  st.write("""
  - Important step when Function 2 is executed -> **prevents from crash**
  - Helps to keep uploaded data (XML invoice) **consistent**
  - The XML Schema validation **catches data issues** 
  """)

with tab2:
  ''
  st.image("Pictures/Function_2/F2_BPMN_HL_data_parsing_v2.svg", width=550)
  ''
  ''
  with st.expander(
    "XML message structure",
    icon= ":material/help_outline:"
    ):
    
    ''
    st.image("Pictures/Function_1/F1_F2_XML_simple_screen.PNG")
    ''
    st.write("More details about the XML and data parsing:")

    st.link_button(
        label = "Go to XSD, XML description page",
        url="https://dataparsing.streamlit.app/F1_F2_description_XML_XSD",
        help="The button will redirect to the relevant page within this app for download.",
        width="stretch",
        icon=":material/launch:"
    )


with tab3:

  ''
  st.image("Pictures/Function_2/F2_BPMN_HL_data_validation_v4.svg")
  ''
  ''
  st.write("""
  Validation:
  - Summary of prices in **detail level <price>** needs to equal to **<total_sum> in header** 
  - Summary of prices per extra services in **detail level <service_price>** needs to equal to **<total_sum_services> in header**
  """)


  ''
  ''
  st.write(" -> **If match**, application displays green success note.")
  st.success("Passed")

  ''
  st.write(" -> **If not match**, application displays warrning message and provides visibility of what is not matching.")

  st.warning(f"""
  Not passed
  - **Invoice summary** does **not** equal to **line values**
  - You can either continue with existing file or adjust the input file and upload it again.""")

  st.warning(f"""
  - **Total sum** in the XML invoice is: **2000.00** US dollar
  - But **summary of prices** in detail lines is: **2103.00** US dollar""")

  ''
  ''
  st.write("**In BOTH CASES, the application ALLOWS to continue to data visualization step.**")


with tab4:

  ''
  st.image("Pictures/Function_2/F2_BPMN_HL_data_visualization_v3.svg")
  ''
  ''
  st.write("""
  Data visualization:
  - Data analytics & statistics based on the uploaded XML invoice
  - Interactive table connected including pie chart and bar chart
  - Static charts
  """
  )


''
''
''
''
st.write("##### Diagrams describing the functions:")

tab1, tab2, tab3, tab4 = st.tabs([
	"UML - Use Case diagram",
	"UML - Activity diagram",
  "ArchiMate - Simple",
  "ArchiMate - Detailed"
])



with tab1:
  ''
  st.write("- Function 1: ")
  ''
  st.image("Pictures/Function_1/F1_UML_UseCase.svg")
  ''
  ''
  ''
  st.write("- Function 2: ")
  ''
  st.image("Pictures/Function_2/F2_UML_UseCase.svg")


with tab2:
  ''
  st.image("Pictures/Function_2/F2 - UML_Activity diagram_2.svg", width=520)
  ''

with tab3:
  ''
  st.write("""
  - Simple overview of core Layers (Business <- Application <- Technology)
  """)

  ''
  st.image("Pictures/Function_2/F2_Archimate_simple.svg", width=280)
  ''
  ''
  st.write("""
  - **Business Layer (Yellow)**:
    - The Business Process element captures 3 steps which Function 2 does 
  """)

  ''
  st.write("""
  - **Application Layer (Blue)**:
    - Simply visualizes this application as one piece 
  """)

  ''
  st.write("""
  - **Technology Layer (Green)**:
    - Dedicated Streamlit application server on which this application runs
    - **Streamlit Framework & environment** is **IaaS on Cloud** - **Google Cloud**
    - Repository: **GitHub**
  """)

  ''
  ''
  st.image("Pictures/Logo/Logo_GoogleCloud.svg", width=180)
  ''
  st.image("Pictures/Logo/Logo_GitHub.svg", width=140)
  ''
  st.image("Pictures/Logo/Logo_python.svg", width=140)

with tab4:
  ''
  ''
  st.image("Pictures/Function_2/F2_Archimate_diagram_complex.svg")



# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
    label = "Next page",
	page="Subpages/F1_F2_description_XML_XSD.py",
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
    icon=":material/east:",
	) 