import streamlit as st
from Subpages.Resources import Assets
from Subpages.Resources_ui import UiConfigAndIcons


# ============= LOGO - SHARED ON ALL PAGES ==========
st.set_page_config(initial_sidebar_state="auto") 

# ============= LOGO - SHARED ON ALL PAGES ==========
st.logo("Pictures/V2_pictures/Logo_7.png", size='large')


# ============== Pages as objects ====================

# ----- Landing page -----
landing_page = st.Page(
    Assets.Paths.App.main_page,
    title= UiConfigAndIcons.Pages.landing_page["label"],
    icon= UiConfigAndIcons.Pages.landing_page["icon"]
    )

# ----- Application architecture page -----
app_description_architecture = st.Page(
    Assets.Paths.App.app_architecture,
    title= UiConfigAndIcons.Pages.architecture["label"],
    icon= UiConfigAndIcons.Pages.architecture["icon"]
    )

# ----- VA -----
VA_function = st.Page(
    Assets.Paths.VirtualAssistant.va,
    title= UiConfigAndIcons.Pages.virtual_assistant["label"],
    icon= UiConfigAndIcons.Pages.virtual_assistant["icon"]
)

# ----- Bug form -----
BF_function = st.Page(
    Assets.Paths.BugForm.bf,
    title= UiConfigAndIcons.Pages.bug_form["label"],
    icon= UiConfigAndIcons.Pages.bug_form["icon"]
)

# ----- Release notes -----
app_description_release_notes = st.Page(
    Assets.Paths.ReleaseNotes.rn,
    title= UiConfigAndIcons.Pages.release_notes["label"],
    icon= UiConfigAndIcons.Pages.release_notes["icon"]
)

# ----- Test pages -----
test_1 = st.Page(
    "Subpages/Testing/TEST_1.py",
    title="TESTING_1"
    )

test_2 = st.Page(
    "Subpages/Testing/TEST_2.py",
    title="TESTING_2"
)


# ----- F1 & F2 -----
F1_F2_description = st.Page(
    Assets.Paths.Description.f1_f2,
    title="Description - Functions",
    icon= UiConfigAndIcons.Pages.description["icon"]
)

F1_F2_descritpion_xml_xsd = st.Page(
    Assets.Paths.Description.f1_f2_xml_xsd,
    title="Description - XML Schema",
    icon= UiConfigAndIcons.Pages.description["icon"]
    )

F1_function = st.Page(
    Assets.Paths.Function.f1,
    title="1. XML - Download",
    icon = UiConfigAndIcons.Pages.function["icon"]
    )

F2_function = st.Page(
    Assets.Paths.Function.f2,
    title="2. XML - Parsing, Validation, Vizualization",
    icon = UiConfigAndIcons.Pages.function["icon"]
    )


# ----- F3 & F4 -----
F3_F4_description = st.Page(
    Assets.Paths.Description.f3_f4,
    title="Description - Functions",
    icon= UiConfigAndIcons.Pages.description["icon"]
)

F3_F4_description_cdm = st.Page(
    Assets.Paths.Description.f3_f4_cdm,
    title="Description - CDM",
    icon= UiConfigAndIcons.Pages.description["icon"]
)

F3_F4_description_xml_json = st.Page(
    Assets.Paths.Description.f3_f4_xml_json,
    title="Description - JSON & XML Schemas",
    icon= UiConfigAndIcons.Pages.description["icon"]
)

F3_F4_description_erd = st.Page(
    Assets.Paths.Description.f3_f4_erd,
    title="Description - DB & ERD",
    icon= UiConfigAndIcons.Pages.description["icon"]
    )

F3_function = st.Page(
    Assets.Paths.Function.f3,
    title="3. Invoice - Creation",
    icon = UiConfigAndIcons.Pages.function["icon"]
    )

F3B_function = st.Page(
    Assets.Paths.Function.f3b,
    title="3B. Invoice - Visibility",
    icon = UiConfigAndIcons.Pages.function["icon"]
    )

F4_function = st.Page(
    Assets.Paths.Function.f4,
    title="4. Invoice - Data Transformation",
    icon = UiConfigAndIcons.Pages.function["icon"]
)

# ----- F5 -----
F5_description = st.Page(
    Assets.Paths.Description.f5,
    title="Description - API & DB",
    icon= UiConfigAndIcons.Pages.description["icon"]
)

F5_function = st.Page(
    Assets.Paths.Function.f5,
    title="5. Exchange Rate",
    icon= UiConfigAndIcons.Pages.function["icon"]
)

F5B_function = st.Page(
    Assets.Paths.Function.f5b,
    title="5B. Exchange Rate Trend",
    icon= UiConfigAndIcons.Pages.function["icon"]
)

# ----- F6 -----
F6_descritpion = st.Page(
    Assets.Paths.Description.f6,
    title="Description - API",
    icon= UiConfigAndIcons.Pages.description["icon"]
)

F6_function = st.Page(
    Assets.Paths.Function.f6,
    title="6. ZIP code",
    icon= UiConfigAndIcons.Pages.function["icon"]
)

# ----- F7 -----
F7_descritpion = st.Page(
    Assets.Paths.Description.f7,
    title="Description - Function",
    icon= UiConfigAndIcons.Pages.description["icon"]
)

F7_description_architecture = st.Page(
    Assets.Paths.Description.f7_architecture,
    title="Description - Architecture",
    icon= UiConfigAndIcons.Pages.description["icon"]
)

F7_description_db = st.Page(
    Assets.Paths.Description.f7_db,
    title="Description - DB & ERD",
    icon= UiConfigAndIcons.Pages.description["icon"]
)

F7_description_state = st.Page(
    Assets.Paths.Description.f7_state,
    title="Description - State flow",
    icon= UiConfigAndIcons.Pages.description["icon"]
)

F7_description_rating = st.Page(
    Assets.Paths.Description.f7_rating,
    title="Description - Rating",
    icon= UiConfigAndIcons.Pages.description["icon"]
)

F7_description_dtd = st.Page(
    Assets.Paths.Description.f7_dtd,
    title="Description - Door-to-Door",
    icon= UiConfigAndIcons.Pages.description["icon"]
)

F7_description_metrics = st.Page(
    Assets.Paths.Description.f7_metrics,
    title="Description - Use Cases & Metrics",
    icon= UiConfigAndIcons.Pages.description["icon"]
)

F7_function = st.Page(
    Assets.Paths.Function.f7,
    title="7. Transportation",
    icon= UiConfigAndIcons.Pages.function["icon"]
)

F7B_function = st.Page(
    Assets.Paths.Function.f7b,
    title="7B. Offer - Visibility",
    icon= UiConfigAndIcons.Pages.function["icon"]
)

# ----- F8 -----
F8_description = st.Page(
    Assets.Paths.Description.f8,
    title="Description - DB & Function",
    icon= UiConfigAndIcons.Pages.description["icon"]
)

F8_function = st.Page(
    Assets.Paths.Function.f8,
    title="8. Company Book",
    icon= UiConfigAndIcons.Pages.function["icon"]
)


# ===== Navigation: =====
pg = st.navigation(
    {
        "About this application": [
            landing_page,
            VA_function,
            BF_function,
            app_description_release_notes,
            app_description_architecture
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
            F3_F4_description_cdm,
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
    f"Do you like this app? :) LinkedIn [Here]({Assets.Links.External.linked_in})"
)