import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px

# For visibility the API structure from kurzy.cz
json_api_structure_1 = """
{
	"query": {
		"city": "Zlin",
		"state": null,
		"country": "cz"
	},
	"results": [
		"760 01",
		"760 07",
	]
}
"""

# For visibility the API structure from freecurrencyapi.com
json_api_structure_2 = """
{
  "query": {
    "codes": [
      "251 63",
      "110 00",
      "140 21"
    ],
    "country": "CZ"
  },
  "results": {
    "251 63": [
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.9333,
        "longitude": 14.6667,
        "city": "Vidovice",
        "state": "Středočeský kraj",
        "city_en": "Vidovice",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      },
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.95,
        "longitude": 14.7,
        "city": "Menčice",
        "state": "Středočeský kraj",
        "city_en": "Menčice",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      },
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.95,
        "longitude": 14.6667,
        "city": "Svojšovice",
        "state": "Středočeský kraj",
        "city_en": "Svojšovice",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      },
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.9667,
        "longitude": 14.65,
        "city": "Otice",
        "state": "Středočeský kraj",
        "city_en": "Otice",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      },
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.9667,
        "longitude": 14.6833,
        "city": "Všestary",
        "state": "Středočeský kraj",
        "city_en": "Všestary",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      },
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.95,
        "longitude": 14.65,
        "city": "Všechromy",
        "state": "Středočeský kraj",
        "city_en": "Všechromy",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      },
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.95,
        "longitude": 14.6833,
        "city": "Strančice",
        "state": "Středočeský kraj",
        "city_en": "Strančice",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      },
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.95,
        "longitude": 14.6333,
        "city": "Předboř",
        "state": "Středočeský kraj",
        "city_en": "Předboř",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      },
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.9333,
        "longitude": 14.6667,
        "city": "Kunice",
        "state": "Středočeský kraj",
        "city_en": "Kunice",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      },
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.95,
        "longitude": 14.6667,
        "city": "Sklenka",
        "state": "Středočeský kraj",
        "city_en": "Sklenka",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      },
      {
        "postal_code": "251 63",
        "country_code": "CZ",
        "latitude": 49.95,
        "longitude": 14.6667,
        "city": "Kašovice",
        "state": "Středočeský kraj",
        "city_en": "Kašovice",
        "state_en": "Středočeský kraj",
        "state_code": "88"
      }
    ],
    "110 00": [
      {
        "postal_code": "110 00",
        "country_code": "CZ",
        "latitude": 50.3667,
        "longitude": 16.0417,
        "city": "Praha 1-Josefov",
        "state": "Hlavní město Praha",
        "city_en": "Praha 1-Josefov",
        "state_en": "Hlavní město Praha",
        "state_code": "52"
      },
      {
        "postal_code": "110 00",
        "country_code": "CZ",
        "latitude": 50.3333,
        "longitude": 15.9167,
        "city": "Josefov",
        "state": "Hlavní město Praha",
        "city_en": "Josefov",
        "state_en": "Hlavní město Praha",
        "state_code": "52"
      },
      {
        "postal_code": "110 00",
        "country_code": "CZ",
        "latitude": 50.4,
        "longitude": 16.1667,
        "city": "Staré Město",
        "state": "Hlavní město Praha",
        "city_en": "Staré Město",
        "state_en": "Hlavní město Praha",
        "state_code": "52"
      },
      {
        "postal_code": "110 00",
        "country_code": "CZ",
        "latitude": 50.3667,
        "longitude": 16.0417,
        "city": "Praha 1-Nové Město",
        "state": "Hlavní město Praha",
        "city_en": "Praha 1-Nové Město",
        "state_en": "Hlavní město Praha",
        "state_code": "52"
      },
      {
        "postal_code": "110 00",
        "country_code": "CZ",
        "latitude": 50.3667,
        "longitude": 16.0417,
        "city": "Vinohrady",
        "state": "Hlavní město Praha",
        "city_en": "Vinohrady",
        "state_en": "Hlavní město Praha",
        "state_code": "52"
      },
      {
        "postal_code": "110 00",
        "country_code": "CZ",
        "latitude": 50.3667,
        "longitude": 16.0417,
        "city": "Praha 1-Vinohrady",
        "state": "Hlavní město Praha",
        "city_en": "Praha 1-Vinohrady",
        "state_en": "Hlavní město Praha",
        "state_code": "52"
      },
      {
        "postal_code": "110 00",
        "country_code": "CZ",
        "latitude": 50.3667,
        "longitude": 16.0417,
        "city": "Nové Město",
        "state": "Hlavní město Praha",
        "city_en": "Nové Město",
        "state_en": "Hlavní město Praha",
        "state_code": "52"
      },
      {
        "postal_code": "110 00",
        "country_code": "CZ",
        "latitude": 50.3667,
        "longitude": 16.0417,
        "city": "Praha 1-Staré Město",
        "state": "Hlavní město Praha",
        "city_en": "Praha 1-Staré Město",
        "state_en": "Hlavní město Praha",
        "state_code": "52"
      }
    ]
  }
}
"""



# ==================== Application scree + backend functions ==============
st.write("# Description - Function 6")
''
''
st.write("""
    - **Function 6:** ZIP code - (1) Get ZIP code(s) based on City, (2) Get City based on ZIP code - **API based**
    """
    )
''
''
st.write("##### Business scenario:") 

st.write("""
- ZIP codes are important part of logistic, this function can be used for
		 
	- Validation of ZIP codes
	- Search for ZIP codes
	 
"""
)
''
''

st.write("##### ZIP codes:") 

st.write("""
- API based (open API)
- Comes from Zipcodebase.com https://app.zipcodebase.com/
- Insert City -> Get ZIP codes 
"""
)

''

st.caption("""
Zipcodebase.com is a website that provides a free ZIP code API for accessing worldwide postal code data. It allows users to perform lookups, distance calculations, radius searches, and more. The service is designed to be a simple solution for tasks related to postal code information. 
"""
)


''
''
# Expander API 1 JSON 
with st.expander("API JSON structure - Zipcodebase.com", icon= ":material/help:"):

	''
	st.write("""
	- API - **HTTP GET** request to retrieve data from a server
	- There is **5k requests limit per month**
	- This Function 6 receives **CUSTOMIZED** data from the API
	- The customization is based on the user inputs (Country CZ/SK and City)		
	""")


	''
	''
	''
	st.write("The full JSON data:")
	st.code(
		json_api_structure_1,
		language= 'json',
		line_numbers=True,
	)
	
	
	st.write("""
	- There is a possibility to monitor the requests in their portal		
	""")
	st.image("Pictures/Function_6/F6_api_monitoring_zipcodebase.png")
	

''
''
''
st.write("""
- Comes from Zipcodestack.com https://app.zipcodestack.com/
- Insert ZIP code(s) -> Get City/Cities
"""
)

''
st.caption("""
Zip Code API - Free Postal Code Search & Validation. A completely free Zip Code REST API and the best way to get accurate zip code data for your application.
https://zipcodestack.com/
"""
)

''
''
# Expander API 2 JSON 
with st.expander("API JSON structure - Freecurrencyapi.com", icon= ":material/help:"):


	''
	st.write("""
	- API - **HTTP GET** request to retrieve data from a server
	- This Function 6 receives **CUSTOMIZED** data from Zipcodestack.com
	- The customization is based on the user inputs (Country CZ/SK and ZIP code(s))
	"""
	)


	''
	''
	''
	st.write("- Customized JSON API data:")
	st.write('- This is what an user input via application screen {"query": {"codes": **["251 63","110 00","140 21"]**,"country": **"CZ"**} and customized the query.')
	st.code(
		json_api_structure_2,
		language= 'json',
		line_numbers=True,
		height=400
		)

	''
	''
	st.write("The API portal allows:")
	st.write("""
	- Make a registration 
	- Monitor the API requests 
	- And see some statistics
	- Also this UI is allowing to troubleshoot and reproduce the request + **retrospectivelly see every JSON data which were sent out** based on every GET the source application got. 
	- Possible to search based on API status, time, date...
	"""
	)
	''
	st.image("Pictures/Function_6/F6_api_monitoring_zipcodestack_charts.png")
	''
	st.image("Pictures/Function_6/F6_api_monitoring_zipcodestack_overview.png")
	''
	''
	''
	st.write("- This API is **limited to 300 requests per month**")
	st.write("- So here is also simple GET API to see statistics:")
	if st.button(
		"API Status",
		use_container_width=True,
		icon=":material/monitoring:"
	):
            try:

                # API count/remaining
                api_count = "https://api.zipcodestack.com/v1/status?apikey=zip_live_pWsWrXrfbOBJpOjUwXuVT8RDRkWCtUj44M2RKzLd"

                # get reguest - cached for 10 minutes
                @st.cache_data(ttl=600)
                def get_response_api_3(api_count):
                    api_3 = requests.get(api_count, verify=False).text
                    return api_3

                api_3 = get_response_api_3(api_count)

                # JSON format creation
                api_3_json = json.loads(api_3)

                # Search for data in the API defined format - JSON
                used = api_3_json['quotas']['month']['used']
                remaining = api_3_json['quotas']['month']['remaining']

                # Description on the screen
                st.write(f"- In this month subscription period - **used: {used}** and **remaining: {remaining}** requests")
                st.write("- This data will be **cached** here for **next 10 minutes**")

                # Simple pie chart
                data_pie_api = pd.DataFrame({
                "Figures" : [used,remaining],
                "Topics" : [f"Used:  {used}",f"Remaining:  {remaining}"],

                })

                fig_api = px.pie(
                    data_pie_api, 
                    names = "Topics",
                    values = "Figures",
                    title = "API status of GET requests from this application - month period"
                )  


                st.write(fig_api)

            except:
                  st.warning("The limit of the API calls per month has been reached 300/300 calls. It will be **renewed by 1st next month**.")
                  

''
''
''
''

# ========= SPlit into tabs =======

tab1, tab2, tab3 = st.tabs([
"Archimate Diagram",
"UML Activity Diagram 1/2",
"UML Activity Diagram 2/2 - API"
])

# Archimate

with tab1:
  st.write("##### Archimate Diagram:") 
  ''
  st.write("*For better visibility - put cursor on the picture and click on the icon in the right upper corner")
  st.image("Pictures/Function_6/F6_description_archimate_api.svg")


  ''
  st.write("##### Description of the APIs:")
  ''
  st.write("""
      - The 2 APIs are **independent** on each other -> each one is called separatelly
          - Depending what part of the Function 6 you use
          - Not possible to call both **at the exactly same moment** as part of 1 user session. 
          - Each is **called based on different user button** (that is why - you never push 2 buttons at the same time)
  """)
  ''
  st.write("""
  - Data quality **Zipcodestack.com**
    - **They say**: Our postal code database is updated regularly to ensure high accuracy. We source our data from official postal services and government databases, making it reliable for business use, address validation, and shipping calculations.
    - **They say**: We update our postal code database monthly for most countries. For regions with frequent postal code changes, we provide more frequent updates to ensure you always have access to the most current data.

  """
  )

  ''
  ''
  st.write("""
  - Frequency of data updates from **Zipcodebase.com**
    - **They say**: We constantly update and verify our data from multiple sources to ensure the accuracy of our data.
    - **They say**: An uptime of 99.9%, calculated on the past 12 months.
  """
  )


#UML 

with tab2:
    st.write("##### UML Activity Diagram 1/2 - overall process:") 
    ''
    st.write("""
            - Description of how the function 6 works
            - The "Receive JSON and Display results" (VIOLET box) part is described in detail in the next diagram
            """
            )
    

    ''
    st.image("Pictures/Function_6/F6_uml_description_process.svg")


with tab3:
    st.write("##### UML Activity Diagram 2/2 - Receive JSON and Display results:") 

    ''
    st.write("""
            - Visibility of what types of **states** the application can get **based on API response**
            """
            )
    

    ''
    st.image("Pictures/Function_6/F6_uml_description_api_detail.svg")
    ''
    ''
    st.write("- **Scenario 1**: Limit of API calls reached (response from the API system Zipcodestack.com):")

    st.code("""
      {
        "message": "You used all your monthly requests. Please upgrade your plan at https://app.zipcodestack.com/subscription"
      }

      """, language="json", wrap_lines=True  
    )


    ''
    ''
    st.write("""
    - **Scenario 2**: Relevant response but no match what our application asked for(user input) and what the API systems have in DB
      - Either we have asked for nonsense (examples: "city": "Not existing city" or "codes": [
      "0000000000"])
      - Or they do not have data
      - Which means -> "results" : [] element **comes empty**
    """)

    st.write("Zipcodebase.com:")

    st.code("""
      {		
        "query": {	
          "city": "Not existing city",
          "state" : "None",
          "country": "cz"
        },	
        "results": [	
        ]	
      }
    """, language="json", wrap_lines=True  
    )

    st.write("Zipcodestack.com:")

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
    """, language="json", wrap_lines=True  
    )


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
	label = "Function 6",
	page="Subpages/F6_FUNCTION_zip_code.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/play_circle:"
	) 