import streamlit as st

st.write("# ArchiMate diagram:")
st.write("*For better visibility - put cursor on the picture and click on the icon in the right upper corner")

st.write("-----")
st.image("Pictures/Function_3/ArchM Function 3.drawio.png")


# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
    label = "Next page",
	page="Subpages/F3_description_XML.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/east:",
	) 

st.page_link(
	label = "Previous page",
	page="Subpages/F3_description_UML.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/west:"
	) 