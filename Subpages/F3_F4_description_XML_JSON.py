import streamlit as st
from Subpages.F3_F4_xml_json_structures import xml_message_example, xsd_as_string, json_message_example, json_schema, json_structure_rules_header, json_structure_rules_detail, json_structure_rules_transportation, xsd_structure_rules_header, xsd_structure_rules_detail, xsd_structure_rules_transportation

# ============= Variables - text ==========================
DESC_HEADER = """
**Header** includes nested elements providing key information/summary about an order 
"""

DESC_DETAIL = """
**Detail** has few nested elements. It groups information about the product which was purchased and whether any additional service for the product was bought or not (Insurance, Extended warranty).
"""

DESC_TRANSPORTATION = """
**Transportation** has few nested elements grouping data about transportation and delivery. 
"""

# ============= Variables - formatting ====================
CODE_HEIGHT = 400


# ================= Screen ================================

st.write("# JSON & XML Schemas")
''
''

st.write("""
- Description of JSON structure & JSON Schema and XML structure & XML Schema used in Function 3 and Function 4
- **Function 3** - Invoice creation
- **Function 4** - Mapping of files
""")

st.write("----")
st.write("##### Diagram:")
''

st.write("""
- JSON and XML structures are basically **identicall** due to the same data the are supposed to keep
- The structure is split into **3 main segments** - header, detail and transportation.
""")

''
tab1, tab2 = st.tabs([
        "JSON Schema",
        "XML Schema"
])


''
''  
''

with tab1:
    ''
    st.image("Pictures/Function_3/F3_F4_JSON_HLE_v1.svg", width=370)
    ''
    ''
    
    tab1_json, tab2_json, tab3_json = st.tabs([
        "Header",
        "Detail",
        "Transportation"
    ])

    with tab1_json:
            ''
            st.write(DESC_HEADER)

            '' 
            st.image("Pictures/Function_3/F3_F4_JSON_header_v1.svg")
            ''
            ''
            with st.expander("JSON Schema structure rules - **header**", icon= ":material/code:"):
                st.code(
                    json_structure_rules_header,
                    language= 'json',
                    line_numbers=True,
                    height=CODE_HEIGHT
                )


    with tab2_json: 
            ''
            st.write(DESC_DETAIL)

            '' 
            st.image("Pictures/Function_3/F3_F4_JSON_detail_v1.svg")
            ''
            ''
            with st.expander("JSON Schema structure rules - **detail**", icon= ":material/code:"):
                st.code(
                    json_structure_rules_detail,
                    language= 'json',
                    line_numbers=True,
                    height=CODE_HEIGHT
                )


    with tab3_json:
            ''
            st.write(DESC_TRANSPORTATION)
            '' 
            st.image("Pictures/Function_3/F3_F4_JSON_transportation_v1.svg", width=500)
            ''
            ''
            with st.expander("JSON Schema structure rules - **transportation**", icon= ":material/code:"):
                st.code(json_structure_rules_transportation,
                language= 'json',
                line_numbers=True,
                height=CODE_HEIGHT
                )

    with st.expander("JSON Schema - **full**", icon=":material/code:"):
        st.code(
            json_schema,
            language="json",
            line_numbers=True,
            height=CODE_HEIGHT,
        )

    with st.expander("JSON message - **example**", icon=":material/code:"):
        st.code(
            json_message_example,
            language="json",
            line_numbers=True,
            height=CODE_HEIGHT,
        )

with tab2:
    ''
    ''
    ''
    st.image("Pictures/Function_3/F3_F4_XML_HLE_v1.svg", width=320)
    ''
    ''
    
    tab1_xml, tab2_xml, tab3_xml, tab4_xml, tab5_xml = st.tabs([
        "Header",
        "Detail",
        "Transportation",
        "Notation",
        "Message definition"
    ])


    with tab1_xml:
            ''
            st.write(DESC_HEADER)

            '' 
            st.image("Pictures/Function_3/F3_F4_XML_header_v1.svg", width=650)
            ''
            ''
            with st.expander("XML Schema structure rules - **header**", icon= ":material/code:"):
                st.code(
                    xsd_structure_rules_header,
                    language= 'xml',
                    line_numbers=True,
                    height=CODE_HEIGHT
                )


    with tab2_xml: 
            ''
            st.write(DESC_DETAIL)

            '' 
            st.image("Pictures/Function_3/F3_F4_XML_detail_v1.svg")
            ''
            ''
            with st.expander("XML Schema structure rules - **detail**", icon= ":material/code:"):
                st.code(
                    xsd_structure_rules_detail,
                    language= 'xml',
                    line_numbers=True,
                    height=CODE_HEIGHT
                )


    with tab3_xml:
            ''
            st.write(DESC_TRANSPORTATION)
            '' 
            st.image("Pictures/Function_3/F3_F4_XML_transportation_v1.svg", width=540)
            ''
            ''
            with st.expander("XML Schema structure rules - **transportation**", icon= ":material/code:"):
                st.code(
                    xsd_structure_rules_transportation,
                    language= 'xml',
                    line_numbers=True,
                    height=CODE_HEIGHT
                )


    with tab4_xml:
            '' 
            st.image("Pictures/Function_3/F3_F4_XML_notation_v1.svg", width=550)
            ''
            ''

    with tab5_xml:
            ''
            st.image("Pictures/Function_3/F3_XML_layout_table.png")
            ''
            ''

    with st.expander("XML Schema - **full**", icon= ":material/code:"):
        st.code(
            xsd_as_string,
            language= 'xml',
            line_numbers=True,
            height=CODE_HEIGHT
        )

    with st.expander("XML message - **example**", icon=":material/code:"):
        st.code(
            xml_message_example,
            language="xml",
            line_numbers=True,
            height=CODE_HEIGHT,
        )


     
st.write("----") 

# Download of XSD

st.write("##### Download of schemas")
''

tab1, tab2 = st.tabs([
    "JSON Schema",
    "XML Schema"   
])

with tab1:
    ''
    st.write("- Format .json")
    if st.download_button(
        "Download",
        data = json_schema,
        file_name="JSON_Schema_for_functions_3_and_4.json",
        icon = ":material/download:"
    ):
        st.info("Download will happen in few seconds")

    ''
    ''
    st.write("- Format .txt")  
    if st.download_button(
        "Download",
        data = json_schema,
        file_name="JSON_Schema_for_functions_3 and_4.txt",
        icon = ":material/download:"
    ):
        st.info("Download will happen in few seconds")


with tab2:
    ''
    st.write("- Format .xsd")
    if st.download_button(
        "Download",
        data = xsd_as_string,
        file_name="XML_Schema_for_functions_3_and_4.xsd",
        icon = ":material/download:"
    ):
        st.info("Download will happen in few seconds")

    ''
    ''
    st.write("- Format .txt")  
    if st.download_button("Download",
        data = xsd_as_string,
        file_name="XML_Schema_for_functions_3_and_4.txt",
        icon = ":material/download:"
    ):
        st.info("Download will happen in few seconds")

# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
    label = "Next page",
	page="Subpages/F3_description_ERD.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/east:",
	) 

st.page_link(
	label = "Previous page",
	page="Subpages/F3_description_archimate.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/west:"
	) 