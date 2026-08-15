import streamlit as st
from Subpages.Resources import Assets

st.write("# BPMN diagrams")


''
''
''
''
st.image("Pictures/Function_2/F2_BPMN_HL_v5.svg")
''
''
''

# Split of the screen to tabs
tab1, tab2, tab3, tab4 = st.tabs([
    ""
    "Validation XML & XML Schema",
    "Data parsing",
	"Data validation",
	"Data visualization"

])


with tab1:

    ''
    st.image(Assets.Images.f2_xml_xsd_validation, width=620)
    ''
    ''
    st.write("""
    - Important step when Function 2 is executed -> **prevents from crash**
    - Helps to keep uploaded data (XML invoice) **consistent**
    - The XML Schema validation **catches data issues** 
    """)

with tab2:

    ''
    st.image("Pictures/Function_2/F2_BPMN_HL_data_parsing_v2.svg", width=550)
    ''
    ''
    with st.expander(
        "XML message structure",
        icon= ":material/help_outline:"
        ):
        
        ''
        st.image("Pictures/Function_1/F1_F2_XML_simple_screen.PNG")
        ''
        st.write("More details about the XML and data parsing:")

        st.link_button(
            label = "Go to XSD, XML description page",
            url="https://dataparsing.streamlit.app/F1_F2_description_XML_XSD",
            help="The button will redirect to the relevant page within this app for download.",
            width="stretch",
            icon=":material/launch:"
        )


with tab3:

    ''
    st.image("Pictures/Function_2/F2_BPMN_HL_data_validation_v4.svg")
    ''
    ''
    st.write("""
    Validation:
    - Summary of prices in **detail level <price>** needs to equal to **<total_sum> in header** 
    - Summary of prices per extra services in **detail level <service_price>** needs to equal to **<total_sum_services> in header**
    """)


    ''
    ''
    st.write(" -> **If match**, application displays green success note.")
    st.success("Passed")

    ''
    st.write(" -> **If not match**, application displays warrning message and provides visibility of what is not matching.")

    st.warning(f"""
    Not passed
    - **Invoice summary** does **not** equal to **line values**
    - You can either continue with existing file or adjust the input file and upload it again.""")

    st.warning(f"""
    - **Total sum** in the XML invoice is: **2000.00** US dollar
    - But **summary of prices** in detail lines is: **2103.00** US dollar""")

    ''
    ''
    st.write("**In BOTH CASES, the application ALLOWS to continue to data visualization step.**")


with tab4:

    ''
    st.image("Pictures/Function_2/F2_BPMN_HL_data_visualization_v3.svg")
    ''
    ''
    st.write("""
    Data visualization:
    - Data analytics & statistics based on the uploaded XML invoice
    - Interactive table connected including pie chart and bar chart
    - Static charts
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
	width="stretch",
    icon=":material/east:",
	) 

st.page_link(
	label = "Previous page",
	page="Subpages/F1_F2_description_function.py",
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
	icon=":material/west:"
	) 

