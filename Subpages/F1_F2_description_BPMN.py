import streamlit as st

st.write("# BPMN diagrams:")
st.write("*For better visibility - put cursor on the picture and click on the icon in the right upper corner")

st.write("-----")
st.write("#### Application process flow:")
''
st.write("- 5 stages of the process - high level")
''
st.image("Pictures/BPMN flow_2.png")


st.write("-----")
st.write("##### Data parsing process:")
''
st.write(" - Principle of the data parsing process from XML")
''
st.image("Pictures/V2_pictures/BPMN data parsing.png")
''
''
with st.expander(
	"The XML message",
	icon= ":material/help_outline:"
	):
    
	''
	st.write("Structure:")
	st.image("Pictures/Function_1/F1_F2_XML_simple_screen.PNG")
	''
	st.write("More details about the XML and data parsing:")

	st.page_link(
		label = "Go to XSD, XML description page",
		page="Subpages/F1_F2_description_XML_XSD.py",
		help="The button will redirect to the relevant page within this app for download.",
		use_container_width=True,
		icon=":material/launch:"
	)

''
st.write("-----")
st.write("##### Data validation process:")
''
st.image("Pictures/Function_2/F2_BPMN - Validation.png")
''
''
st.write("""
- The application includes validation of the data <total_sum> (Invoice summary of price) against price per item/product <price>. 
- The same happens for <total_sum_services> against sum of <serice_price> in detail.""")
''
st.write(" -> If match, application displays green success note.")
st.write(" -> If not match, application displays warrning message and provides correct number (was calculated by the application)")
''
st.write("**In BOTH CASES application ALLOWS to continue to data visualization step.**")

st.write("-----")
st.write("##### Data visualization process:")
''
st.image("Pictures/Function_2/F2_BPMN - Visualization.png")
''
''
st.write("""
    Data visualization:
    - Overview of header and detail information including values which the app. calculated
    - Interactive table including pie chart and bar chart
    """  
    )

# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
    label = "Next page",
	page="Subpages/F2_description_UML.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/east:",
	) 

st.page_link(
	label = "Previous page",
	page="Subpages/F1_F2_description_function.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/west:"
	) 

