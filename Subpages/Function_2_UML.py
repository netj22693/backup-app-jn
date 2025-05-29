import streamlit as st

st.write("# UML diagrams:")
st.write("*For better visibility - put cursor on the picture and click on the icon in the right upper corner")


st.write("-----")
st.write("#### UML Use Case diagram:")
''
''
st.write("###### Function 1: ")
''
st.image("Pictures/Function_1/F1_UML - Use case.PNG")
''
''
''
st.write("###### Function 2: ")
''
st.image("Pictures/Function_2/F2_UML - Use case.PNG")

st.write("-----")
st.write("#### UML Activity diagram:")
st.image("Pictures/Function_2/F2 - UML_Activity diagram_2.png")

# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
    label = "Next page",
	page="Subpages/application_description_archimate.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/east:",
	) 

st.page_link(
	label = "Previous page",
	page="Subpages/application_description_BPMN.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/west:"
	) 