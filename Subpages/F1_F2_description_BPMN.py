import streamlit as st

st.write("# BPMN diagrams:")
st.write("*For better visibility - put cursor on the picture and click on the icon in the right upper corner")

st.write("-----")
st.write("#### Application process flow:")
''
st.write("- 5 stages of the process - high level")
''
# st.image("Pictures/BPMN flow_2.png")
st.image("Pictures/Function_2/F2_BPMN_5stages HLE_2.svg")
''
''
''

# Split of the screen to tabs
tab1, tab2, tab3 = st.tabs([
    "Data Parsing",
	"Data Validation",
	"Data Visualization"

])


# Tab 1
with tab1:

    ''
    st.write("##### Data parsing process:")
    ''
    st.write(" - Principle of the data parsing process from XML")
    ''
    # st.image("Pictures/V2_pictures/BPMN data parsing.png")
    st.image("Pictures/Function_2/F2_BPMN_data parsing.svg")
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

# Tab 2
with tab2:

    ''
    st.write("##### Data validation process:")
    ''
    # st.image("Pictures/Function_2/F2_BPMN - Validation.png")
    st.image("Pictures/Function_2/F2_BPMN - Validation.svg")
    ''
    ''
    st.write("""
    - The application includes validation of the data <total_sum> (Invoice summary of price) against price per item/product <price>. 
    - The same happens for <total_sum_services> against sum of <serice_price> in detail.""")
    ''
    st.write(" -> **If match**, application displays green success note.")
    st.write(" -> **If not match**, application displays warrning message and provides  suggestion of correct numbers (was calculated by the application)")
    ''
    st.write("**In BOTH CASES, the application ALLOWS to continue to data visualization step.**")


    ''
    ''
    with st.expander(
        "Validation",
        icon= ":material/help_outline:"
        ):
        
        st.write("Example of validation in the Function 2:")
        st.image("Pictures/V2_pictures/validation.png")
        ''
        ''


# Tab 3
with tab3:

    ''
    st.write("##### Data visualization process:")
    ''
    # st.image("Pictures/Function_2/F2_BPMN - Visualization.png")
    st.image("Pictures/Function_2/F2_BPMN - Visualization_2.svg")
    ''
    ''
    st.write("""
        Data visualization:
        - Overview of header and detail information including values which the app. calculated
        - Interactive table  connected including pie chart and bar chart
        - Static charts 
        - And some highlights of the invoice - based on SQL query
        """  
        )

    ''
    ''
    with st.expander(
         "Visualization",
        icon= ":material/help_outline:"
        ):
        
        ''
        st.write("**Few Examples:**")
        ''
        ''
        st.write("- Invoice Overview & SQL highlights expanders:")
        ''
        st.image("Pictures/Function_2/F2_BPMN_visualization_highlight.png",width=420)
        ''
        ''
        ''
        st.write("- Interactive table")
        ''
        st.image("Pictures/Function_2/F2_BPMN_visualization_inttable.png",width=420)
        ''
        ''
        ''
        st.write("- Static charts")
        ''
        st.image("Pictures/Function_2/F2_BPMN_visualization_static charts.png",width=420)
        ''
        ''

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

