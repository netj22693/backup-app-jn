# Purpose: to store image paths and links as variables -> for images used both in APP and Virtual Assistant


HELLO_STATEMENT = """👋 Hi! I'm your FAQ chatbot. You can ask me:

- Questions about the application 
- Questions releated to specific functions  
- Questions related to me (chatbot) :sunglasses:
- :question: For examples of questions / how to ask -> write **What do you do**
- :bulb: **Please note:** The chatbot may occasionally provide incomplete or inaccurate answers, try reformulating your question to help the chatbot understand better.
"""

class Assets:
    class Images:
        va_variables = "Pictures/Virtual_asistant/VA_principle_variables_v2.svg"
        architecture_landscape = "Pictures/App_landscape_architecture_v7.svg"
        archimate_main = "Pictures/Archimate_functions_overview_v14.svg"
        # UML
        uml_f1_f2 = "Pictures/Overall_UML_F1 and F2_v2.svg"
        uml_f3_f3b_f4 = "Pictures/Overall_UML_F3 and F4_v3.svg"
        uml_f5 = "Pictures/Overall_UML_F5.svg"
        uml_f6 = "Pictures/Overall_UML_F6.svg"
        uml_f7_f7b = "Pictures/Overall_UML_F7_v3.svg"
        uml_f8 = "Pictures/Overall_UML_F8_v3.svg"
        # Function desc related images
        f2_xml_xsd_validation ="Pictures/Function_2/F2_diagram_xml_xsd_validation.svg"


    class Links:
        linked_in = "https://www.linkedin.com/in/jan-netolicka-12209a221/"
        sklearn_library = "https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html"
        # Functions
        f1_function = "https://dataparsing.streamlit.app/F1_FUNCTION_XML_dowload"
        #Description
        f2_xml_xsd = "https://dataparsing.streamlit.app/~/+/F1_F2_description_XML_XSD#xsd-xml-schema"
        f2_xml_xsd_validation = "https://dataparsing.streamlit.app/~/+/F1_F2_description_XML_XSD#xml-against-xsd-validation"
        f3_f4_xml_xsd = "https://dataparsing.streamlit.app/~/+/F3_description_XML#xsd-xml-schema"
        f3_f4_json = "https://dataparsing.streamlit.app/F3_F4_description_json#json-schema"
        f3_description = "https://dataparsing.streamlit.app/F3_F4_description#functions-3-and-4"
        f5_description = "https://dataparsing.streamlit.app/F5_description_API"
        f6_description = "https://dataparsing.streamlit.app/F6_description_API"
        f7_description = "https://dataparsing.streamlit.app/F7_description"
        f8_description = "https://dataparsing.streamlit.app/F8_description"
        # ERD
        f3_f4_description_erd = "https://dataparsing.streamlit.app/F3_ERD"
        f7_description_erd = "https://dataparsing.streamlit.app/F7_description_ERD_DB"
        f8_descriptin_erd = "https://dataparsing.streamlit.app/F8_description#db-structure-erd"