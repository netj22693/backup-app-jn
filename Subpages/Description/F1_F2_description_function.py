import streamlit as st
from Subpages.Resources import Assets
from Subpages.Resources_ui import UiConfigAndIcons
from Subpages.Resources_ui_objects import render_next_page, render_link_button
from Video.Display_video import display_video_expander

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
display_video_expander(Assets.Videos.LogicalDictionaries.f1_f2)


''
''
''
st.write("##### Business scenario:") 
st.write(
"Simplified version of case when a company does a purchase from other company/e-shop on frequent bases -> XML invoice defined for invoicing."
)

''
st.write("##### Process:") 
st.write("""
1) Dowload XML (keep existing or you can update it) 
2) Upload XML
"""
)

''
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
  st.image(Assets.Images.f2_xml_xsd_validation)

with tab2:
  st.image("Pictures/Function_2/F2_BPMN_HL_data_parsing_v3.svg")

with tab3:
  st.image("Pictures/Function_2/F2_BPMN_HL_data_validation_v5.svg")

with tab4:
  st.image("Pictures/Function_2/F2_BPMN_HL_data_visualization_v4.svg")


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
  st.image("Pictures/Function_2/F2_UML_Activity_diagram_2.svg", width=520)
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

render_next_page(page= Assets.Paths.Description.f1_f2_xml_xsd)