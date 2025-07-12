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
            
    """)
    ''

    st.image("Pictures/Function_2/F2_UML_error_handling_2.drawio.svg")


    ''
    with st.expander(
        "Application context - **(1) Display alert**",
        icon= ":material/help_outline:"
        ):
        
        ''
        ''
        st.write("##### Display alert:")
        ''
        st.image("Pictures/Function_2/F2_uml_display_alert.svg", width= 180)
        ''
        ''
        st.write("- This happens when there is a different file type than XML uploaded")
        ''
        st.image("Pictures/Function_2/F2_uml_alert.png")
        ''
        ''
        st.write("- This alert is displayed even if not a single line of code executed")
        ''
        st.image("Pictures/Function_2/F2_uml_error_handling_annotation_1.svg")
        ''
        st.write("""
                 - The reason is that the upload box element is specific streamlit API reference
                 - So this element can be limited in the code using a specific parameter
                 """)
        ''


    with st.expander(
        "Application context - **(2) Validation of XML against XSD**",
        icon= ":material/help_outline:"
        ):
        ''
        st.write("##### Validation of XML using XSD:")
        ''
        st.image("Pictures/Function_2/F2_uml_error_handling_annotation_2.svg", width= 400)

        st.write("""
                 - **Key** step for the whole Function 2
                 - This prevents from data quality issue, when XML file uploaded -> which would impact the processing and visualization part
                 - The check of XML against XSD makes sure that the Function 2 will get:
                    - All necessary data in the XML
                    - At the possitions they should be
                    - Correct data types 
                    - Correct inputs will be used in case there are predefined paterns -> which is also how the Function 2 is designed
                """)

        st.code("""
<!-- DATA TYPES -->
<xs:restriction base="xs:string">
<xs:restriction base="xs:decimal">


<!-- PATTERNS -->
<!-- Category -->
<xs:pattern value="PC|TV|Gaming|Mobile phones|Tablets|Major Appliances|Households"/>

<!-- Currency -->
<xs:pattern value="euro|US dollar|Kč"/>

<!-- Service type -->
<xs:pattern value="None|extended warranty|insurance"/>

<!-- Invoice number -->
<xs:pattern value="[I]{1}[N]{1}[V]{1}[-]{1}[0-9]{6}"/>

<!-- ... and other stuff possible to define in XSD -->
""",language= "xml", wrap_lines=True)



        ''
        ''
        st.write("- Which in case of **issue -> XML does not pass the validation** looks like this:")
        st.image("Pictures/Function_2/F2_uml_display_issue_note.svg", width= 180)
        st.image("Pictures/Function_2/F2_uml_upload_invalid.png")

        ''
        ''
        st.write("- And in case that **ALL IS OKAY** looks like this:")

        st.image("Pictures/Function_2/F2_uml_continue_with_next_steps.svg", width= 180)
        st.image("Pictures/Function_2/F2_uml_upload_valid.png")


    with st.expander(
        "Application context - **(3) Error note**",
        icon= ":material/help_outline:"
        ):

        ''
        st.write("##### Error note:")
        ''
        st.image("Pictures/Function_2/F2_uml_error_handling_annotation_3.svg", width=460)
        ''
        st.write("""
        - This is an error handling which exists **only** for purpose of **catching bugs** or better to say **prevent the application Function 2 from crashing** in case that some bug appears
        - I believe the probability is **very ver low** here to fall into this error
        - Why? Because the (2) step of XML validation against XSD should catch all data issue -> the python script then should be fully functional because it will get the data which it expects. And because the Function 2 is built "around" the data the processing then should be alright.        
        """)
        ''





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