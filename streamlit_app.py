import streamlit as st
from Subpages.Resources import Assets


 # ============= LOGO - SHARED ON ALL PAGES ==========
st.set_page_config(initial_sidebar_state="auto") 

 # ============= LOGO - SHARED ON ALL PAGES ==========
st.logo("Pictures/V2_pictures/Logo_7.png", size='large')


# ============== Pages as objects ====================

# ----- Landing page -----
landing_page = st.Page(
    "Subpages/Purpose_of_app.py",
    title="Purpose of this application",
    icon= ":material/home:"
    )

# ----- VA -----
VA_function = st.Page(
    "Subpages/FVA_main_virtual_assistant.py",
    title="Virtual Assistant (Chatbot)",
    icon= ":material/smart_toy:"
)

# ----- Test pages -----
test_1 = st.Page(
    "Subpages/Testing/TEST_1.py",
    title="TESTING"
    )

test_2 = st.Page(
    "Subpages/Testing/TEST_2.py",
    title="session"
)


# ----- F1 & F2 -----
F1_F2_description = st.Page(
    Assets.Paths.Description.f1_f2,
    title="Description - Functions",
    icon= ":material/code:"
)

F1_F2_descritpion_xml_xsd = st.Page(
    Assets.Paths.Description.f1_f2_xml_xsd,
    title="Description - XML Schema",
    icon= ":material/code:"
    )

F1_function = st.Page(
    "Subpages/F1_FUNCTION_XML_dowload.py",
    title="1. XML - Download",
    icon = ":material/play_circle:"
    )

F2_function = st.Page(
    "Subpages/F2_FUNCTION_XML_parsing_to_txt_outcome.py",
    title="2. XML - Parsing, Validation, Vizualization",
    icon = ":material/play_circle:"
    )


# ----- F3 & F4 -----
F3_F4_description = st.Page(
    Assets.Paths.Description.f3_f4,
    title="Description - Functions",
    icon= ":material/code:"
)

F3_F4_description_xml_json = st.Page(
    Assets.Paths.Description.f3_f4_xml_json,
    title="Description - JSON & XML Schemas",
    icon= ":material/code:"
)

F3_F4_description_erd = st.Page(
    Assets.Paths.Description.f3_f4_erd,
    title="Description - DB & ERD",
    icon= ":material/code:"
    )

F3_function = st.Page(
    "Subpages/F3_FUNCTION_creation_of_XML.py",
    title="3. Invoice - Creation - XML/JSON",
    icon = ":material/play_circle:"
    )

F3B_function = st.Page(
    "Subpages/F3b_FUNCTION_invoice_visibility.py",
    title="3B. Invoice - Visibility",
    icon = ":material/play_circle:"
    )

F4_function = st.Page(
    "Subpages/F4_FUNCTION_translation_mapping.py",
    title="4. Invoice - Mapping - XML/JSON",
    icon = ":material/play_circle:"
)

# ----- F5 -----
F5_description = st.Page(
    Assets.Paths.Description.f5,
    title="Description - API & DB",
    icon= ":material/code:"
)

F5_function = st.Page(
    "Subpages/F5_FUNCTION_exchange.py",
    title="5. Exchange Rate",
    icon= ":material/play_circle:"
)

F5B_function = st.Page(
    "Subpages/Function_5b/F5b_FUNCTION_exchange_rate.py",
    title="5B. Exchange Rate Trend",
    icon= ":material/play_circle:"
)

# ----- F6 -----
F6_descritpion = st.Page(
    Assets.Paths.Description.f6,
    title="Description - API",
    icon= ":material/code:"
)

F6_function = st.Page(
    "Subpages/F6_FUNCTION_zip_code.py",
    title="6. ZIP code",
    icon= ":material/play_circle:"
)

# ----- F7 -----
F7_descritpion = st.Page(
    Assets.Paths.Description.f7,
    title="Description - Function",
    icon= ":material/code:"
)

F7_description_architecture = st.Page(
    Assets.Paths.Description.f7_architecture,
    title="Description - Architecture",
    icon= ":material/code:"
)

F7_description_db = st.Page(
    Assets.Paths.Description.f7_db,
    title="Description - DB & ERD",
    icon= ":material/code:"
)

F7_description_state = st.Page(
    Assets.Paths.Description.f7_state,
    title="Description - State flow",
    icon= ":material/code:"
)

F7_description_rating = st.Page(
    Assets.Paths.Description.f7_rating,
    title="Description - Rating",
    icon= ":material/code:"
)

F7_description_dtd = st.Page(
    Assets.Paths.Description.f7_dtd,
    title="Description - Door-to-Door",
    icon= ":material/code:"
)

F7_description_metrics = st.Page(
    Assets.Paths.Description.f7_metrics,
    title="Description - Use Cases & Metrics",
    icon= ":material/code:"
)

F7_function = st.Page(
    "Subpages/F7_FUNCTION_transport.py",
    title="7. Transportation",
    icon= ":material/play_circle:"
)

F7B_function = st.Page(
    "Subpages/F7b_FUNCTION_offer_visibility.py",
    title="7B. Offer - Visibility",
    icon= ":material/play_circle:"
)

# ----- F8 -----
F8_description = st.Page(
    Assets.Paths.Description.f8,
    title="Description - DB & Function",
    icon= ":material/code:"
)

F8_function = st.Page(
    "Subpages/F8_FUNCTION_company_book.py",
    title="8. Company Book",
    icon= ":material/play_circle:"
)


# ===== Navigation: =====
pg = st.navigation(
    {
        "About this application": [
            landing_page,
            VA_function
            ],
            
        # "TESTING": [test_1, test_2],

        "Functions 1 and 2" : [
            F1_F2_description,
            F1_F2_descritpion_xml_xsd,
            F1_function, 
            F2_function
            ],
        "Functions 3 and 4": [
            F3_F4_description,
            F3_F4_description_xml_json,
            F3_F4_description_erd,
            F3_function,
            F3B_function,
            F4_function
            ],
        "Function 5": [
            F5_description,
            F5_function,
            F5B_function
        ],
        "Function 6": [
            F6_descritpion,
            F6_function
        ],
        "Function 7": [
            F7_descritpion,
            F7_description_architecture,
            F7_description_db,
            F7_description_state,
            F7_description_rating,
            F7_description_dtd,
            F7_description_metrics,
            F7_function,
            F7B_function,
        ],
        "Function 8" : [
            F8_description,
            F8_function
        ]

    },
    expanded=True  #23-Jun-2025: since streamlit version 1.46.0, this is needed to have the right menu bar always open as default (possibility to collaps still available)
)

pg.run()

# ============= side bar caption ===================
st.sidebar.caption(
    f"Do you like this app? :) LinkedIn [Here]({Assets.Links.linked_in})"
)