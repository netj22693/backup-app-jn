import streamlit as st

st.write("# UML diagrams:")
st.write("*For better visibility - put cursor on the picture and click on the icon in the right upper corner")


st.write("-----")
st.write("#### UML Use Case diagram:")
''
''
st.write("###### Function 3: ")
''
st.image("Pictures/Function_3/F3_UML - Use case.PNG")
''
''
''
st.write("###### Function 4: ")
''
st.image("Pictures/Function_4/F4_UML - Use case.PNG")

st.write("-----")
st.write("#### UML Activity diagram:")
st.image("Pictures/Function_3/F3 - UML - Activity diagram.drawio.png")
''
with st.expander(
    "Application context",
    icon= ":material/help_outline:"
	):
    
	''
	''
	st.write("Filling data:")
	''
	st.image("Pictures/Function_3/F3_UML - context act diagram.PNG", width=500)
	''
	''
	st.write("Invoice creation:")
	''
	st.image("Pictures/Function_3/F3_UML - context act diagram_2.PNG", width=500)
	''
	''
	st.page_link(
	label = "Go to: Function 3",
	page="Subpages/F3_FUNCTION_creation_of_XML.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/play_circle:",
	) 


# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
    label = "Next page",
	page="Subpages/F3_description_archimate.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/east:",
	) 

st.page_link(
	label = "Previous page",
	page="Subpages/F3_F4_description_BPMN.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/west:"
	) 