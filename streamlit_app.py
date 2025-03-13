import streamlit as st


# --- SHARED ON ALL PAGES ---
# st.logo("Pictures/Logo2.png", size='large')


# Pages as objects
# testing = st.Page(
#     "Subpages/testuju.py",
#     title="TESTING"
#     )

# app_purpose = st.Page(
#     "Subpages/Purpose_of_app.py",
#     title="Purpose of this application"
#     )

# app_description_ArM = st.Page(
#     "Subpages/application_description_archimate.py",
#     title="Description Archimate"
#     )

# app_description_BPMN = st.Page(
#     "Subpages/application_description_BPMN.py",
#     title="Description BPMN"
#     )

# download = st.Page(
#     "Subpages/XML_dowload.py",
#     title="1. XML - Download"
#     )

# xsd = st.Page(
#     "Subpages/XML_XSD_schema.py",
#     title="Description - XSD, XML Schema"
#     )

# parsing = st.Page(
#     "Subpages/XML_parsing_to_txt_outcome.py",
#     title="2. XML - Parsing, Validation, Vizualization"
#     )

function_3 = st.Page(
    "Subpages/Function_3_creation of XML.py",
    title="3. XML - Creation of XML"
    )


# Navigation:
pg = st.navigation(
    {
        #"About this application": [app_purpose , app_description_ArM , app_description_BPMN , xsd],
        #"TESTING": [testing],
        "Application functions": [
            #download,
            #parsing,
            function_3,
            ]
    }
)

pg.run()