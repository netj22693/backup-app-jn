import streamlit as st
import xml.etree.ElementTree as ET
import json
from Subpages.F4_operational_functions import write_log_into_db, display_goto_links, parsing_xml_mapping_to_json, parsing_json_mapping_to_xml


# ====================== USER SCREEN =============================
# Split of the screen into 2 columns
col1, col2 = st.columns(2)


# ====================== COLUMN 1: XML -> JSON ===================

col1.write("# XML -> JSON :")

col1.write("### Upload XML:")


object_upl_xml = col1.file_uploader("Upload XML", label_visibility="collapsed", type=".xml")


if object_upl_xml is None:
    col1.info("When a file uploaded, translation to JSON will happen")
        

if object_upl_xml is not None:

    try:
        json_object_returned, file_name_json, data_log_json = parsing_xml_mapping_to_json(object_upl_xml)
        col1.success("Upload complete")
  
        # Download button
        col1.download_button(
            'Download - JSON',
            json_object_returned,
            file_name = file_name_json,
            use_container_width=True,
            icon = ":material/download:",
            on_click= lambda: write_log_into_db(data_log_json)
            )

    except Exception as e:
        print(f"Parsing process not complete - {e}")
        col1.error("The uploaded file is not supported by this application")
        json_object_returned = None
    
           
       
# ====================== COLUMN 2: JSON -> XML ===================

col2.write("# JSON -> XML :")

col2.write("### Upload JSON:")


object_upl_json = col2.file_uploader("Upload JSON", label_visibility="collapsed",key= "json", type=".json")

if object_upl_json is None:
    col2.info("When a file uploaded, translation to XML will happen")
        

if object_upl_json is not None:
    
    try:
        xml_object_returned, file_name_xml, data_log_xml = parsing_json_mapping_to_xml(object_upl_json)
        col2.success("Upload complete")

        # Download button
        col2.download_button(
            'Download - XML',
            xml_object_returned, 
            file_name = file_name_xml,
            use_container_width=True,
            icon = ":material/download:",
            on_click= lambda: write_log_into_db(data_log_xml)
            )

    except Exception as e:
        print(f"Parsing process not complete - {e}")
        col2.error("The uploaded file is not supported by this application")


''
with st.expander(
	"How to use this function",
	icon= ":material/help_outline:"		
    ):
	''
	st.write("""
    - It allows file format translation XML <-> JSON
    - It works with files produced by **Function 3**
    """)
	st.page_link(
        label = "Function 3",
        page="Subpages/F3_FUNCTION_creation_of_XML.py",
        help="The button will redirect to the relevant page within this app.",
        use_container_width=True,
        icon=":material/play_circle:",
        )
		

st.write("-------")

#Closing button  
if st.button(
    "Close Function 4",
    use_container_width= True,
    icon=":material/close:"
	):
    display_goto_links()