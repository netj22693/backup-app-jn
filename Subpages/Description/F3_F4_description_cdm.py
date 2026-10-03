import streamlit as st
from Subpages.Resources import Assets


st.write("# CDM:")


''
st.write("""
- **Canonical Data Model** shortly known as CDM
- Used both by **F3** and **F4**
- These Functions operates with multiple data formats -> benefical to have unified CDM 
- The main benefit is the possibility to transform the data formats/mapping **without** point-to-point translations
- Also allows to compare data parsed from a file with data saved in DB -> **CDM to CDM data comparison**
""")

''
''
''
st.image("Pictures/Function_3/CDM/F3_F4_CDM_main_v1.svg")


tab1, tab2 = st.tabs([
    "Function 3",
    "Function 4"
])

with tab1:
    st.write("- User input -> File creation -> Data saved into DB")
    ''
    st.image("Pictures/Function_3/CDM/F3_CDM_v1.svg")

with tab2:
    st.write("- File input -> Data validation -> Data transformation -> File output")
    ''
    st.image("Pictures/Function_3/CDM/F4_CDM_v1.svg")


''
''
st.write("##### Validations:") 

st.write("""
- Multiple data validations **preventing** from data transformation -> if the file produced by user using F3 is somehow invalid e.g.: **manually changed either data structure or values**
- **Level 1**: JSON and XML use **Schema validations**, CSV uses **number of fields** separated by comma, before transformed to CDM
- **Level 2**: Check if there is **existing record in DB** based on **Order number** parsed form the uploaded file 
- **Level 3**: If record in DB exists, the data are pulled from DB and translated to CDM format. CDM data (file and DB) are compared, if they match
""")

''
st.image("Pictures/Function_3/CDM/F4_CDM_validations_v1.svg")


''
''
st.write("##### Code architecture:") 

st.write("""
- The CDM is approached as a service consisted of **multiple functions**
- The Parsing/Translation from/to CDM happens based on **CDM config** rules which the functions use
- The CDM config is basically the **middle data structure description** including JSON & XML paths, CSV positions, DB column names
""")

''
st.image("Pictures/Function_3/CDM/F3_F4_CDM_code_context_v1.svg")


# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
    label = "Next page",
	page= Assets.Paths.Description.f3_f4_xml_json,
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
    icon=":material/east:",
	) 

st.page_link(
	label = "Previous page",
	page= Assets.Paths.Description.f3_f4,
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
	icon=":material/west:"
	) 