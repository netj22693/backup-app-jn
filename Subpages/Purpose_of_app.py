import streamlit as st


st.write("# Welcome!")
''
st.write(
    "Purpose of this application is to play with XML data. The application has **4 functions**:"
    )
''
st.write("""
    - **Function 1:** Download of few predefined types of XML for Function 2
    - **Function 2:** Parsing of data from XML -> their visualization -> producing of simple .txt file as summary      
    """)
''
st.write("""
    - **Function 3:** Creation of XML (slightly different one than used in F1 and F2) or JSON, through the application screen (manual inputs)
    - **Function 4:** Mapping/change of file format XML -> JSON or JSON -> XML 
    """)
''
st.write("""
    - **Function 5:** Exchange rate/calculation (CZK, EUR, USD) - API based with actual exchange rate
    """)
''
''
"More details about the functions can be seen in the subpages - what the functions do, what data structures are used, etc."

st.write("enjoy... :)") 

''
''
st.write("###### ArchiMate - Overview of the functions:")
st.image(
    "Pictures/Archimate_functions_overview.png"
    )
''
''
# Buttons for redirectiong to the relevant Functions
st.write("### Go to:")
st.write("**Recommendation:** To firstly read the description chapters (the application navigation bar) to understand how the functions/application work.")
''
st.page_link(
    label = "Description about F1 and F2",
	page="Subpages/F1_F2_description_function.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/code:",
	) 
st.page_link(
	label = "Function 1",
	page="Subpages/F1_FUNCTION_XML_dowload.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/play_circle:"
	) 

st.page_link(
	label = "Function 2",
	page="Subpages/F2_FUNCTION_XML_parsing_to_txt_outcome.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/play_circle:"
	) 
''
st.page_link(
    label = "Description about F3 and F4",
	page="Subpages/F3_F4_description.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/code:",
	) 

st.page_link(
	label = "Function 3",
	page="Subpages/F3_FUNCTION_creation_of_XML.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/play_circle:"
	) 

st.page_link(
	label = "Function 4",
	page="Subpages/F4_FUNCTION_translation_mapping.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/play_circle:"
	) 
''
st.page_link(
    label = "Description about F5",
	page="Subpages/F5_description_API.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/code:",
	)

st.page_link(
	label = "Function 5",
	page="Subpages/F5_FUNCTION_exchange.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/play_circle:"
	) 

# # ===== Page navigation at the bottom ======
# ''
# ''
# ''
# ''
# st.write("-------")

# st.page_link(
#     label = "Next page",
# 	page="Subpages/Function_1 and 2_ description.py",
# 	help="The button will redirect to the relevant page within this app.",
# 	use_container_width=True,
#     icon=":material/east:",
# 	) 