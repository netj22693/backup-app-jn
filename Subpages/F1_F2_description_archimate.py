import streamlit as st

st.write("# ArchiMate diagrams:")
st.write("*For better visibility - put cursor on the picture and click on the icon in the right upper corner")

st.write("-----")
st.write("#### ArchiMate simple:")
st.image("Pictures/Function_2/F2_Archimate_simple.png")

st.write("-----")
st.write("#### ArchiMate complex:")
st.image("Pictures/Parsing-archimate-diagram_2.png")

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
	use_container_width=True,
    icon=":material/east:",
	) 

st.page_link(
	label = "Previous page",
	page="Subpages/F2_description_UML.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/west:"
	) 