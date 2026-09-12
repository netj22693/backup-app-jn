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
''
''
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
  st.image("Pictures/Architecture/Code_architecture_v1.svg")
  ''
  ''

with tab2:
  st.image("Pictures/Architecture/Functions_building_blocks_v1.svg")
  ''

with tab3:
  st.image("Pictures/Architecture/Operational_vs_service_v1.svg")
  ''
with tab4:
  st.image("Pictures/Architecture/API_layer_v1.svg", width=400)

with tab5:
  st.image("Pictures/Architecture/DB_layer_v1.svg")
  ''

with tab6:
  st.image("Pictures/Architecture/Virtual_assistant_v1.svg", width=620)
  ''



''
''
st.write("""
- **Application generic**
  - **Resources** - assets like images, links, paths
  - **Logging** - logging used across the application
  - **API Layer** - API service/function used across the application
  - **DB Layer** - DB connection service/function used across the application
""")

st.write("""
- **Function specific**
  - **Main** - Function main logic stream & orchestration + UI
  - **Operational functions** - separate customized code functions. Related to the Function which executes their logic based on the orchestration
  - **Services** - separate customized "bigger" functions can have their own orchestration
  - **Input data** - Data and structures supporting the Function logic. Typically XREF, logic dictionaries, data structures etc.
  - **SQL queries** - Function specific queries for DB
  - **Dialog** - Function specific dialog windows for UI
  - **Expanders** - Wider UI text kept separated to have cleaner code
  - **Schedulers** - Scripts for GitHub Actions
""")

''
''
st.image("Pictures/Architecture/Root_structure_v1.svg", width=280)