import streamlit as st


 # ============= LOGO - SHARED ON ALL PAGES ==========
st.set_page_config(initial_sidebar_state="auto") 

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
    "Subpages/F1_F2_description_archimate.py",
    title="Description - ArchiMate",
    icon= ":material/code:"
    )

app_description_BPMN = st.Page(
    "Subpages/F1_F2_description_BPMN.py",
    title="Description - BPMN",
    icon= ":material/code:"
    )

download = st.Page(
    "Subpages/F1_FUNCTION_XML_dowload.py",
    title="1. XML - Download",
    icon = ":material/play_circle:"
    )

xsd = st.Page(
    "Subpages/F1_F2_description_XML_XSD.py",
    title="Description - XSD, XML Schema",
    icon= ":material/code:"
    )

parsing = st.Page(
    "Subpages/F2_FUNCTION_XML_parsing_to_txt_outcome.py",
    title="2. XML - Parsing, Validation, Vizualization",
    icon = ":material/play_circle:"
    )

function_3 = st.Page(
    "Subpages/F3_FUNCTION_creation_of_XML.py",
    title="3. Invoice - Creation - XML/JSON",
    icon = ":material/play_circle:"
    )

function_3b = st.Page(
    "Subpages/F3b_FUNCTION_invoice_visibility.py",
    title="3B. Invoice - Visibility",
    icon = ":material/play_circle:"
    )

function_3_xml = st.Page(
    "Subpages/F3_description_XML.py",
    title="Description - XSD, XML Schema",
    icon= ":material/code:"
    )

function_3_BPMN = st.Page(
    "Subpages/F3_F4_description_BPMN.py",
    title="Description - BPMN",
    icon= ":material/code:"
    )

function_3_erd = st.Page(
    "Subpages/F3_ERD.py",
    title="Description - DB & ERD",
    icon= ":material/code:"
    )

testuju_stsession = st.Page(
    "Subpages/F7_DB_insert.py",
    title="F7_DB_TEST"
)

fun_1and2_descrip = st.Page(
    "Subpages/F1_F2_description_function.py",
    title="Description - Functions",
    icon= ":material/code:"
)

fun_3_archm = st.Page(
    "Subpages/F3_description_archimate.py",
    title="Description - ArchiMate",
    icon= ":material/code:"
)

fun_4 = st.Page(
    "Subpages/F4_FUNCTION_translation_mapping.py",
    title="4. Invoice - Mapping - XML/JSON",
    icon = ":material/play_circle:"
)

fun_3_json = st.Page(
    "Subpages/F3_F4_description_json.py",
    title="Description - JSON Schema",
    icon= ":material/code:"
)

fun_3and4_descrip = st.Page(
    "Subpages/F3_F4_description.py",
    title="Description - Functions",
    icon= ":material/code:"
)

fun_2_DB_ERT = st.Page(
    "Subpages/F2_description_DB_ERT.py",
    title="Description - DB & ERD",
    icon= ":material/code:"
)

fun_2_UML = st.Page(
    "Subpages/F2_description_UML.py",
    title="Description - UML",
    icon= ":material/code:"
)

fun_3_UML = st.Page(
    "Subpages/F3_description_UML.py",
    title="Description - UML",
    icon= ":material/code:"
)

function_5 = st.Page(
    "Subpages/F5_FUNCTION_exchange.py",
    title="5. Exchange Rate",
    icon= ":material/play_circle:"
)

function_5_desc_api = st.Page(
    "Subpages/F5_description_API.py",
    title="Description - API",
    icon= ":material/code:"
)


function_6_zipcode = st.Page(
    "Subpages/F6_FUNCTION_zip_code.py",
    title="6. ZIP code",
    icon= ":material/play_circle:"
)

function_6_desc_api = st.Page(
    "Subpages/F6_description_API.py",
    title="Description - API",
    icon= ":material/code:"
)

function_7_transport = st.Page(
    "Subpages/F7_FUNCTION_transport.py",
    title="7. Transportation",
    icon= ":material/play_circle:"
)

function_7_desc = st.Page(
    "Subpages/F7_description.py",
    title="Description - Function",
    icon= ":material/code:"
)


function_7_desc_dtd = st.Page(
    "Subpages/F7_description_dtd.py",
    title="Description - Door-to-Door",
    icon= ":material/code:"
)

function_7_desc_metrics = st.Page(
    "Subpages/F7_description_metrics.py",
    title="Description - Use Cases & Metrics",
    icon= ":material/code:"
)


function_7_desc_variables = st.Page(
    "Subpages/F7_description_variables.py",
    title="Description - Variables",
    icon= ":material/code:"
)

function_8_company_book = st.Page(
    "Subpages/F8_FUNCTION_company_book.py",
    title="8. Company Book",
    icon= ":material/play_circle:"
)

function_8_desc = st.Page(
    "Subpages/F8_description.py",
    title="Description - DB & Function",
    icon= ":material/code:"
)




# For dev/test purposes - on 31-Dec-2025 use_container_width= will be depricated in context of plotly 
test_7 = st.Page(
    "Subpages/Dev_deprication_Dec_2025/F7_Function_dev_test.py",
    title="TEST_F7_deprication",
    icon= ":material/code:"
)

# Navigation:
pg = st.navigation(
    {
        "About this application": [
            app_purpose,
            ],
            
        # "TESTING": [testing, testuju_stsession, test_7],

        "Functions 1 and 2" : [
            fun_1and2_descrip,
            app_description_BPMN,
            fun_2_UML,
            app_description_ArM,
            xsd,
            fun_2_DB_ERT,
            download, 
            parsing
            ],
        "Functions 3 and 4": [
            fun_3and4_descrip,
            function_3_BPMN,
            fun_3_UML,
            fun_3_archm,
            function_3_xml,
            fun_3_json,
            function_3_erd,
            function_3,
            function_3b,
            fun_4
            ],
        "Function 5": [
            function_5_desc_api,
            function_5
        ],
        "Function 6": [
            function_6_desc_api,
            function_6_zipcode
        ],
        "Function 7": [
            function_7_desc,
            function_7_desc_variables,
            function_7_desc_dtd,
            function_7_desc_metrics,
            function_7_transport,
        ],
        "Function 8" : [
            function_8_desc,
            function_8_company_book
        ]

    },
    expanded=True  #23-Jun-2025: since streamlit version 1.46.0, this is needed to have the right menu bar always open as default (possibility to collaps still available)
)

pg.run()

# ============= side bar caption ===================
st.sidebar.caption(
    "Do you like this app? :) LinkedIn [Here](https://www.linkedin.com/in/jan-netolicka-12209a221/)"
)