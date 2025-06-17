import streamlit as st

st.write("# ArchiMate diagram:")

''
''
st.write("""
- Overview of the Function 3 process (file XML or JSON creation) across 3 core Layers
""")

''
''
st.write("*For better visibility - put cursor on the picture and click on the icon in the right upper corner")
''
st.image("Pictures/Function_3/ArchM Function 3.drawio.png")


''
''
st.write("""
- **Business Layer (Yellow)**:
    - Element Event (need for billing) is the business trigger for Invoice creation 
    - **Invoice** is the business object/outcome of the Function 3 process
""")

''
st.write("""
- **Application Layer (Blue)**:
    - The Business process is served by this application giving the possibility to create such invoice in required formats (XML or JSON)
""")

''
st.write("""
- **Technology Layer (Green)**:
    - This is about dedicated Streamlit application server on which this application runs
    - The principle of this **Streamlit Framework & environment** is **IaaS on Cloud**
    - It is **Google Cloud**
    - Codespace: **MS Visual Studio Code**
    - Repository: **GitHub**
    """)

''
''
st.image("Pictures/Function_2/F2_archimate_google cloud.png", width=190)
''
''
st.image("Pictures/Function_2/F2_Archimate_vscode logo.png", width=190)
''
st.image("Pictures/Function_2/F2_Archimate_github logo.png", width=170)
''
st.image("Pictures/Function_2/F2_Archimate_streamlit logo.png", width=210)


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