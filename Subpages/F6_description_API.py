import streamlit as st
from app_api import api_GET_cache_10min, get_url_string_for_GET_api
from Subpages.F5_F6_statistics_api_visualization import display_statistics
from Subpages.F6_json_structures import json_api_structure_1, json_api_structure_2


# ==================== Application screen + backend functions ==============
st.write("# Description - Function 6")
''
''
st.write("""
- **Function 6:** ZIP code - 🟣 Get ZIP code(s) based on City, 🟢 Get City based on ZIP code - **API based**
"""
)
''
''
st.write("##### Business scenario:")

st.write("""
- ZIP codes play an important role in logistics
  - Validation of ZIP codes
  - Search for ZIP codes
""")

''
''
st.write("##### ZIP codes:")

st.write("""
- API based (open API)
- Comes from external system [Zipcodebase.com](https://app.zipcodebase.com/) 🟣
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
    json_api_structure_1,
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
- Comes from external system [Zipcodestack.com](https://app.zipcodestack.com/) 🟢
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
    json_api_structure_2,
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

# ========= SPlit into tabs =======

tab1, tab2, tab3 = st.tabs([
  "Archimate Diagram",
  "UML Activity Diagram 1/2",
  "UML Activity Diagram 2/2 - API",
])

# Archimate

with tab1:
  st.write("##### Archimate Diagram:")
  ''
  st.image("Pictures/Function_6/F6_description_archimate_api.svg")


  ''
  st.write("##### Description of the APIs:")
  ''
  st.write("""
  - The 2 APIs are **independent** -> each is called based on **different use case** 
  """)


  ''
  st.write("""
  - Frequency of data updates from **Zipcodebase.com** 🟣
    - **They say**: We constantly update and verify our data from multiple sources to ensure the accuracy of our data.
    - **They say**: An uptime of 99.9%, calculated on the past 12 months.
  """)

  ''
  ''
  st.write("""
  - Data quality **Zipcodestack.com** 🟢
    - **They say**: Our postal code database is updated regularly to ensure high accuracy. We source our data from official postal services and government databases, making it reliable for business use, address validation, and shipping calculations.
    - **They say**: We update our postal code database monthly for most countries. For regions with frequent postal code changes, we provide more frequent updates to ensure you always have access to the most current data.
  """)



with tab2:
  st.write("##### UML Activity Diagram 1/2 - overall process:")
  ''
  st.write("""
  - Description of how the function 6 works
  - The "Receive JSON and Display results" (VIOLET box) part is described in detail in the next diagram
  """)

  ''
  st.image("Pictures/Function_6/F6_uml_description_process.svg")


with tab3:
  st.write("##### UML Activity Diagram 2/2 - Receive JSON and Display results:")

  ''
  st.write("""
  - Visibility of what types of **states** the application can get **based on API response**
  """)


  ''
  st.image("Pictures/Function_6/F6_uml_description_api_detail.svg")
  ''
  ''
  st.write("- **Scenario 1**: Limit of API calls reached (response from the API system Zipcodestack.com 🟢):")

  st.code("""
  {
    "message": "You used all your monthly requests. Please upgrade your plan at https://app.zipcodestack.com/subscription"
  }
  """, language="json", wrap_lines=True)


  ''
  ''
  st.write("""
  - **Scenario 2**: Relevant response but no match what our application asked for(user input) and what the API systems have in DB
    - Either we have asked for nonsense (examples: "city": "Not existing city" or "codes": [
    "0000000000"])
    - Or they do not have data
    - Which means -> "results" : [] element **comes empty**
  """)

  ''
  st.write("🟣 Zipcodebase.com:")

  st.code("""
  {
    "query": {
      "city": "Not existing city",
      "state": "None",
      "country": "cz"
    },
    "results": [
    ]
  }
  """, language="json", wrap_lines=True)

  st.write("🟢 Zipcodestack.com:")

  st.code("""
  {
    "query": {
      "codes": [
        "0000000000"
      ],
      "country": "CZ"
    },
    "results": {
    }
  }
  """, language="json", wrap_lines=True)


  ''
  ''
  st.write("""
  - **Scenario 3**: The ideal case - user request matches API DB:
    - Examples of JSON were provided upper in the expanders "(?) API - JSON structure..."
  """)


# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
    label="Function 6",
    page="Subpages/F6_FUNCTION_zip_code.py",
    help="The button will redirect to the relevant page within this app.",
    use_container_width=True,
    icon=":material/play_circle:"
    )