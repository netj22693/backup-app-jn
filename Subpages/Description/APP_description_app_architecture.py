import streamlit as st
from Subpages.Resources import Assets

st.write("# Application Architecture")
''
''
''
st.image(f"{Assets.Images.architecture_landscape}")
''
st.write("""
- **Application logic** - Streamlit cloud
- **DB** - PostgreSQL
- **API** - data from external systems
- **Background jobs** - GitHub Actions
""")

''
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
  "VA",
  "F1 & F2",
  "F3, F3B & F4",
  "F5 & F5B",
  "F6",
  "F7 & F7B",
  "F8"
])

with tab1:
  st.image(Assets.Images.architecture_detail_va)

with tab2:
  st.image(Assets.Images.architecture_detail_f1_f2)

with tab3:
  st.image(Assets.Images.architecture_detail_f3_f3b_f4)

with tab4:
  st.image(Assets.Images.architecture_detail_f5_f5b)

with tab5:
  st.image(Assets.Images.architecture_detail_f6)

with tab6:
  st.image(Assets.Images.architecture_detail_f7_f7b)

with tab7:
  st.image(Assets.Images.architecture_detail_f8)


st.write("##### Code architecture:")

''
st.write(f"- Link to [GitHub]({Assets.Links.External.git_hub}) repository")
''

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
  "Overview",
  "Functions - building blocks",
  "Operation functions X Services", 
  "API Layer",
  "DB Layer",
  "Virtual Assistant"
])

with tab1:
  ''
  st.image("Pictures/Architecture/Code_architecture_v2.svg")
  ''
  ''

with tab2:
  ''
  st.image("Pictures/Architecture/Functions_building_blocks_v2.svg")
  ''

with tab3:
  ''
  st.image("Pictures/Architecture/Operational_vs_service_v2.svg")
  ''
with tab4:
  ''
  st.image("Pictures/Architecture/API_layer_v2.svg", width=430)

with tab5:
  ''
  st.image("Pictures/Architecture/DB_layer_v2.svg")
  ''

with tab6:
  ''
  st.image("Pictures/Architecture/Virtual_assistant_v2.svg", width=620)
  ''



''
''
st.write("""
- **Application generic**
  - **Resources** - assets like images, links, paths
  - **Logging** - logging used across the application
  - **API Layer** - API service/function used across the application
  - **DB Layer** - DB connection service/function used across the application
  - **Universal functions** - generic, reusable operations with no Function-specific business logic. They may be used by multiple independent Functions (DRY concept)
""")

st.write("""
- **Function specific**
  - **Main** - Function main logic stream & orchestration + UI
  - **Operational functions** - separate customized code functions. Related to the Function which executes their logic based on the orchestration
  - **Services** - separate customized "bigger" functions can have their own orchestration
  - **Input data** - Data and structures supporting the Function logic. Typically XREF, logic dictionaries, data structures etc.
  - **SQL queries** - Function specific queries for DB
  - **Dialog** - Function specific dialog windows for UI
  - **Expanders** - Wider UI text kept separated to have cleaner and not that heavy code
  - **Schedulers** - Scripts for GitHub Actions
""")

''
''
st.image("Pictures/Architecture/Root_structure_v1.svg", width=280)


''
''
''
st.write("##### More details about the Functions and their architecture:")
''
st.page_link(
  label = "Description about F1 and F2",
  page= Assets.Paths.Description.f1_f2,
  help="The button will redirect to the relevant page within this app.",
  width="stretch",
  icon=":material/code:",
  ) 

st.page_link(
  label = "Description about F3, F3B and F4",
  page= Assets.Paths.Description.f3_f4,
  help="The button will redirect to the relevant page within this app.",
  width="stretch",
  icon=":material/code:",
  ) 

st.page_link(
  label = "Description about F5 and F5B",
  page= Assets.Paths.Description.f5,
  help="The button will redirect to the relevant page within this app.",
  width="stretch",
  icon=":material/code:",
  )

st.page_link(
  label = "Description about F6",
  page= Assets.Paths.Description.f6,
  help="The button will redirect to the relevant page within this app.",
  width="stretch",
  icon=":material/code:",
  )

st.page_link(
  label = "Description about F7 and F7B",
  page= Assets.Paths.Description.f7,
  help="The button will redirect to the relevant page within this app.",
  width="stretch",
  icon=":material/code:",
  )

st.page_link(
  label = "Description about F8",
  page= Assets.Paths.Description.f8,
  help="The button will redirect to the relevant page within this app.",
  width="stretch",
  icon=":material/code:",
  )

# ===== Page navigation at the bottom ======
''
''
st.write("-------")

st.page_link(
  label = "Virtual Assistant (Chatbot)",
  page= Assets.Paths.VirtualAssistant.va,
  help="The button will redirect to the relevant page within this app.",
  width="stretch",
  icon=":material/smart_toy:",
  ) 

st.page_link(
  label = "Home page",
  page= Assets.Paths.App.main_page,
  help="The button will redirect to the relevant page within this app.",
  width="stretch",
  icon=":material/home:",
  )