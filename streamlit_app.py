import streamlit as st


 # ============= LOGO - SHARED ON ALL PAGES ==========
st.logo("Pictures/V2_pictures/Logo_7.png", size='large')


# ============== Pages as objects ====================
testing = st.Page(
    "Subpages/testuju.py",
    title="TESTING"
    )

app_purpose = st.Page(
    "Subpages/Purpose_of_app.py",
    title="Purpose of this application",
    icon= ":material/code:"
    )

app_description_ArM = st.Page(
    "Subpages/application_description_archimate.py",
    title="Description - Archimate",
    icon= ":material/code:"
    )

app_description_BPMN = st.Page(
    "Subpages/application_description_BPMN.py",
    title="Description - BPMN",
    icon= ":material/code:"
    )

download = st.Page(
    "Subpages/XML_dowload.py",
    title="1. XML - Download",
    icon = ":material/play_circle:"
    )

xsd = st.Page(
    "Subpages/XML_XSD_schema.py",
    title="Description - XSD, XML Schema",
    icon= ":material/code:"
    )

parsing = st.Page(
    "Subpages/XML_parsing_to_txt_outcome.py",
    title="2. XML - Parsing, Validation, Vizualization",
    icon = ":material/play_circle:"
    )

function_3 = st.Page(
    "Subpages/Function_3_creation of XML.py",
    title="3. XML - Creation of XML or JSON",
    icon = ":material/play_circle:"
    )

function_3_xml = st.Page(
    "Subpages/Function_3_xml description.py",
    title="Description - XSD, XML Schema",
    icon= ":material/code:"
    )

function_3_BPMN = st.Page(
    "Subpages/Function_3_BPMN.py",
    title="Description - BPMN",
    icon= ":material/code:"
    )

testuju_stsession = st.Page(
    "Subpages/sessionstate.py",
    title="Session state"
)

fun_1and2_descrip = st.Page(
    "Subpages/Function_1 and 2_ description.py",
    title="Description - Functions",
    icon= ":material/code:"
)

fun_3_archm = st.Page(
    "Subpages/Function_3_Archimate.py",
    title="Description - Archimate",
    icon= ":material/code:"
)

fun_4 = st.Page(
    "Subpages/Function_4_xml to json json to xml.py",
    title="4. Mapping XML to JSON, JSON to XML",
    icon = ":material/play_circle:"
)

fun_3_json = st.Page(
    "Subpages/Function_3 and 4_json description.py",
    title="Description - JSON Schema",
    icon= ":material/code:"
)

fun_3and4_descrip = st.Page(
    "Subpages/Function_3 and 4_description.py",
    title="Description - Functions",
    icon= ":material/code:"
)


# Navigation:
pg = st.navigation(
    {
        "About this application": [
            app_purpose,
            ],
        # "TESTING": [testing, testuju_stsession],

        "Functions 1 and 2" : [
            fun_1and2_descrip,
            app_description_BPMN,
            app_description_ArM,
            xsd,
            download, 
            parsing
            ],
        "Functions 3 and 4": [
            fun_3and4_descrip,
            function_3_BPMN,
            fun_3_archm,
            function_3_xml,
            fun_3_json,
            function_3,
            fun_4
            ]
    }
)

pg.run()

# ============= side bar caption ===================
st.sidebar.caption(
    "Do you like this app? :) LinkedIn [Here](https://www.linkedin.com/in/jan-netolicka-12209a221/)"
)