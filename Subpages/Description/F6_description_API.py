import streamlit as st
from Subpages.Resources import Assets
from app_api import api_GET_cache_10min, get_url_string_for_GET_api
from Subpages.Services.F5_F6_statistics_api_visualization import display_statistics
from Subpages.Data.F6_json_structures import json_api_structure_zipcodebase, json_api_structure_zipcodestack, json_scenario_1_zipcodestack, json_scenario_2_zipcodebase, json_scenario_2_zipcodestack


# ==================== Application screen + backend functions ==============
st.write("# Description - Function 6")
''
''
st.write("""
- **Function 6:** ZIP code - :orange[⬤] Get ZIP code(s) based on City, :green[⬤] Get City based on ZIP code - **API based**
"""
)
''
''
st.write("##### Business scenario:")

st.write("""
- ZIP codes play important role in logistics
  - Validation of ZIP codes
  - Search for ZIP codes
""")

''
''
st.write("##### ZIP codes:")

st.write("""
- API based (open API)
- Comes from external system [Zipcodebase.com](https://app.zipcodebase.com/) :orange[⬤]
- Insert City -> Get ZIP codes
"""
)

''
st.caption("""
Zipcodebase.com is a website that provides a free ZIP code API for accessing worldwide postal code data. It allows users to perform lookups, distance calculations, radius searches, and more. The service is designed to be a simple solution for tasks related to postal code information.
""")


# Expander API 1 JSON
''
''
with st.expander("API JSON structure - Zipcodebase.com", icon=":material/help:"):

  ''
  st.write("""
  - API - **HTTP GET** request to retrieve data from external system
  - Response is **CUSTOMIZED**
  - The customization is based on user inputs -> **parameters** (**Country** CZ/SK and **City**)
  """)

  ''
  st.write("""
  - API **Response**
    - **"query"** object with the parameters which were in GET Request
    - **"results"** as array with the ZIP codes related to the query
  """)

  st.code(
    json_api_structure_zipcodebase,
    language='json',
    line_numbers=True,
  )

  ''
  st.write("""
  - There is **5k requests limit per month**
  """)
  st.image("Pictures/Function_6/F6_api_monitoring_zipcodebase.png")


''
''
''
st.write("""
- API based (open API)
- Comes from external system [Zipcodestack.com](https://app.zipcodestack.com/) :green[⬤]
- Insert ZIP code(s) -> Get City/Cities
"""
)

''
st.caption("""
Zip Code API - Free Postal Code Search & Validation. A completely free Zip Code REST API and the best way to get accurate zip code data for your application.
"""
)


# Expander API 2 JSON
''
''
with st.expander("API JSON structure - Zipcodestack.com", icon=":material/help:"):

  ''
  st.write("""
  - API - **HTTP GET** request to retrieve data from external system
  - Response is **CUSTOMIZED**
  - The customization is based on user inputs -> **parameters** (**Country** CZ/SK and **ZIP code(s)**)
  """)

  ''
  st.write("""
  - API **Response**
    - **"query"** object with the parameters which were in GET Request
    - **"results"** object containing nested arrays of objects
  """)

  st.code(
    json_api_structure_zipcodestack,
    language='json',
    line_numbers=True,
    height=400
  )

  ''
  ''
  st.write("""
  - External API portal:
    - Monitoring of API requests & HTTP codes
    - Statistics
    - Troubleshooting & reproducing of requests
    - Retrospectivelly see every JSON Response
    - Filtering based on date, time, HTTP code/state
  """)


  ''
  st.image("Pictures/Function_6/F6_api_monitoring_zipcodestack_charts.png")
  ''
  st.image("Pictures/Function_6/F6_api_monitoring_zipcodestack_overview.png")


  ''
  ''
  ''
  st.write("- API is **limited to 300 requests per month**")

  if st.button(
    "API Usage",
    use_container_width=True,
    icon=":material/clock_loader_40:"
  ):


    # API
    data_json = api_GET_cache_10min(
      url_string=get_url_string_for_GET_api("zipcodestack_com_statistics"),
      function_id="F6 - STATISTICS",
      api_name="zipcodestack.com"
    )

    # Parsing + UI visualization
    display_statistics(
      data_json=data_json,
      function_id="F6 - STATISTICS",
      api_name="zipcodestack.com"
    )


''
''
''
''
st.write("##### Process flow:")
''
st.write("""
- Input **validation & normalization** as key part of the process
- Helps to **not send messy data** to external systems
- Helps to **not make unnecessary API calls** having invalid inputs
- If normalization, **cache/caching is more effective**
- Few **XREF dictionaries** help to the normalization and better user experience
""")


''
''
''
st.image("Pictures/Function_6/F6_process_flow_v1.svg")

''
''
tab1, tab2 = st.tabs([
  "Insert City → Get ZIP code",
  "Insert ZIP code → Get City"
])


tab1.image("Pictures/Function_6/F6_process_flow_detail_zipcodebase_v2.svg")

tab2.image("Pictures/Function_6/F6_process_flow_detail_zipcodestack_v2.svg")



''
''
''
''
st.write("##### Description of the APIs:")
''
st.image("Pictures/Function_6/F6_description_archimate_api_v2.svg")

''
''
tab1,tab2 = st.tabs([
	"Data providers",
	"Data scenarios"
  
])

with tab1:
	st.write("""
	- The 2 APIs are **independent** -> each is called based on **different use case** 
	""")


	''
	st.write("""
	- Frequency of data updates from **Zipcodebase.com** :orange[⬤]
	- **They say**: We constantly update and verify our data from multiple sources to ensure the accuracy of our data.
	- **They say**: An uptime of 99.9%, calculated on the past 12 months.
	""")

	''
	''
	st.write("""
	- Data quality **Zipcodestack.com** :green[⬤]
	- **They say**: Our postal code database is updated regularly to ensure high accuracy. We source our data from official postal services and government databases, making it reliable for business use, address validation, and shipping calculations.
	- **They say**: We update our postal code database monthly for most countries. For regions with frequent postal code changes, we provide more frequent updates to ensure you always have access to the most current data.
	""")


with tab2:
	st.write("- **Scenario 1**: Limit of API calls exceeded (:green[⬤] Zipcodestack.com:):")

	st.code(json_scenario_1_zipcodestack, language="json", wrap_lines=True)


	''
	''
	st.write("""
	- **Scenario 2**: Valid response but no match -> no data available
	""")

	st.write(":orange[⬤] Zipcodebase.com:")

	st.code(json_scenario_2_zipcodebase, language="json", wrap_lines=True)

	st.write(":green[⬤] Zipcodestack.com:")

	st.code(json_scenario_2_zipcodestack, language="json", wrap_lines=True)


	''
	''
	st.write("""
	- **Scenario 3**: The ideal case: Data match request and external DB -> API returns data (examples provided upper in the expanders)
	""")


# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
  label="Function 6",
  page= Assets.Paths.Function.f6,
  help="The button will redirect to the relevant page within this app.",
  width="stretch",
  icon=":material/play_circle:"
  )