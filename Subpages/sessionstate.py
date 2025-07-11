import streamlit as st
from lxml import etree


upload = st.file_uploader("Upload")
if upload == None:
    st.write("none")

else: 
    st.write("uploaded")

if st.button("cau"):

    def validate(xml_path: str, xsd_path: str) -> bool:

        st.write("tu som")

        xmlschema_doc = etree.parse(xsd_path)

        st.write("zde som")
        xmlschema = etree.XMLSchema(xmlschema_doc)

        st.write("tu")
        xml_doc = etree.parse(xml_path)
        st.write("tady")
        result = xmlschema.validate(xml_doc)

        st.write("tamhle")
        return result


    if validate(xml_path = upload, xsd_path ="F2_XSD_validation/XML_Schema_for_functions_1_and_2.xsd"):
        st.write('Valid! :)')
    else:
        st.write('Not valid! :(')