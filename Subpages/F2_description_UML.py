import streamlit as st

st.write("# UML diagrams:")


# Split into tabs
tab1, tab2, tab3 = st.tabs([
	"1 - Use Case diagram",
	"2 - Activity diagram",
	"3 - Activity diagram - Error handling"
])


# Tab 1
with tab1:

    ''
    ''
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


# Tab 2
with tab2:

    ''
    ''
    st.write("#### UML Activity diagram:")
    ''
    st.write("""
    - Provides a visibility of:
        - Steps and decisions which user makes to support end-to-end process throught the application
        - Showing the sequence of processing inside the application
    """)

    ''
    ''
    st.image("Pictures/Function_2/F2 - UML_Activity diagram_2.svg")
    ''
    with st.expander(
        "Application context",
        icon= ":material/help_outline:"
        ):
        
        ''
        ''
        st.write("Application process:")
        ''
        # st.image("Pictures/Function_2/F2_UML - app context .png", width= 500)
        st.image("Pictures/Function_2/F2_UML _app_context.svg", width=390)
        

        ''
        st.page_link(
        label = "Go to: Function 2",
        page="Subpages/F2_FUNCTION_XML_parsing_to_txt_outcome.py",
        help="The button will redirect to the relevant page within this app.",
        use_container_width=True,
        icon=":material/play_circle:",
        ) 


# Tab 3
with tab3:

    ''
    ''
    st.write("#### UML Activity diagram - Error handling:")
    ''
    st.write("""
    - The application/Function 2 works with **specific XML file**
    - Based on the definition of the XML (structure/data types) the Function 2 is programmed to be able to parse the data and continue with next steps
    - This Activity diagram **describes the programmed mechanism when a file uploaded**
    - The process is put into "**try and except**" python conditions which **prevents from failuer of the program**
        - If any of these answers is 'No' -> the except condition is met 
        - If all answers are 'Yes' -> try -> file is okay and end-to-end steps can happen
             
    """)
    ''
    ''
    st.image("Pictures/Function_2/F2_UML_error handling parsing.svg")
    ''
    with st.expander(
        "Application context",
        icon= ":material/help_outline:"
        ):
        
        ''
        ''
        st.write("Application process:")
        ''
        # st.image("Pictures/Function_2/F2_UML_error handling parsing_detail.png")
        st.image("Pictures/Function_2/F2_UML_error handling parsing_detail.svg", width= 600)
        

        ''
        st.page_link(
        label = "Go to: Function 2",
        page="Subpages/F2_FUNCTION_XML_parsing_to_txt_outcome.py",
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
	page="Subpages/F1_F2_description_archimate.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/east:",
	) 

st.page_link(
	label = "Previous page",
	page="Subpages/F1_F2_description_BPMN.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/west:"
	) 