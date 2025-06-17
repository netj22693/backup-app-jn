import streamlit as st

st.write("# ArchiMate diagrams:")


# Split into tabs
tab1, tab2 = st.tabs([
    "Simple diagram",
    "Complex diagram"
])


#Tab 1
with tab1:
    ''
    st.write("##### ArchiMate simple:")
    ''
    st.write("""
    - Basic overview of core Layers (Business <- Application <- Technology)
    
    """)
    ''
    st.image("Pictures/Function_2/F2_Archimate_simple.png")
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

#Tab 2
with tab2:
    ''
    st.write("##### ArchiMate complex:")
    ''
    ''
    st.write("""
    - More detailed overview of the 3 core Layers
    """)

    st.write("""
    - Including: 
        - Function 1 - Download
        - Function 2 - Data Parsing, Validation, Visualization and Generating of .txt summary file
    """)


    ''
    ''
    st.write("*For better visibility - put cursor on the picture and click on the icon in the right upper corner")
    ''
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