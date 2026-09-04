import streamlit as st
from app_api import api_GET_cache_10min, get_url_string_for_GET_api
from Subpages.F5_F6_statistics_api_visualization import display_statistics
from Subpages.F5_json_structures import json_api_structure_1, json_api_structure_2
from Subpages.Resources import Assets


# ==================== Application screen + backend functions ==============
st.write("# Description - Functions 5 & 5B")
''
''
st.write("""
- **Function 5:** Exchange rate/calculation (CZK, EUR, USD) - **API based** with actual exchange rate
- **Function 5B:** Exchange rate - Trend - **Background job based**, data continuously collected into DB and visualized via app UI
"""
)

''
''
st.write("##### Business scenario:") 

st.write("""
- For visibility and calculation purposes. **Function 5** offers **a simple calculator** to convert values between currencies.
		 
	- CZK 
	- EUR
	- USD	 
"""
)
''
''

st.write("##### Actual conversion rate:") 

st.write("""
- API based (open API)
- Comes from external system [Kurzy.cz](https://www.kurzy.cz/) ⚫	
- CZK  to EUR and USD	 
"""
)

''

st.caption("""
Kurzy.cz is a Czech portal specializing in the field of finance - investments, business and personal finance. It was founded in 2000 originally at fin.cz and since 2006 at kurzy.cz. According to Netmonitor statistics, the kurzy.cz server was visited by a total of 3,207,000 real users in March 2022, making the server one of the 15 most visited Czech media.
"""
)


''
''
# Expander API 1 JSON 
with st.expander("API JSON structure - Kurzy.cz", icon= ":material/help:"):

	''
	st.write("""
	- API - **HTTP GET** request to retrieve data from external system
	- There is no limit defined
	- This API returns **static response schema** -> not possible to customize 
	""")

	st.write("""
	- These fields are **parsed**:
		- "EUR" : { "dev_stred" : float value }
		- "USD" : { "dev_stred" : float value }
	""")	


	''
	st.write("- The **static** JSON API **Response**")
	st.code(
		json_api_structure_1,
		language= 'json',
		line_numbers=True,
		height=400)

	

''
''
''
st.write("""
- Comes from external system [Freecurrencyapi.com](https://app.freecurrencyapi.com/) 🔵
- EUR to USD	 
"""
)

''
st.caption("""
Free Currency Conversion API
The 100% free solution for handling exchange rate conversions. Our currency API provides live & historical exchange rate data ranging from 1999 until today.
"""
)

''
''
# Expander API 2 JSON 
with st.expander("API JSON structure - Freecurrencyapi.com", icon= ":material/help:"):

	''
	st.write("""
	- API - **HTTP GET** request to retrieve data from external system
	- The function uses **CUSTOMIZED** data from Freecurrencyapi.com 
		- "data" : { "USD" : float value }
		- Base Currency: **EUR**
		- Currency/Rate to: **USD**
	""")

	''
	st.write("- Customized API **response**")
	st.code(
		json_api_structure_2,
		language= 'json',
		line_numbers=True
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
	st.image("Pictures/Function_5/F5_description_api_statistics.png")
	''
	st.image("Pictures/Function_5/F5_description_api_statistics_another.png")
	''
	''
	st.write("- API is **limited to 1k requests per month**")
	if st.button(
		"API Usage",
		use_container_width=True,
		icon=":material/clock_loader_40:"
	):
		# API 
		data_json = api_GET_cache_10min(
			url_string=get_url_string_for_GET_api("freecurrencyapi_com_EUR_to_USD_statistics"),
			function_id="F5 - STATISTICS",
			api_name="freecurrencyapi.com"  
			)      
		
		# Parsing + UI visualization
		display_statistics(
			data_json=data_json,
			function_id="F5 - STATISTICS",
			api_name="freecurrencyapi.com"
			)
              

''
''
''
''
# Archimate
st.write("##### Archimate Diagram:") 
''
st.image("Pictures/Function_5/F5_description_archimate_api.svg")

''
''
''
st.write("""- The **both** APIs are called **at the same time** to get fresh data when UI is open""")


''
st.write("""
- **API Data caching**
	- To do **not** overutilize the API
	- The cache is applied for **1 hour** (3600 seconds)
	- The cache is applicable for **1 session**
    - **Timeout after 5 seconds** in case of connection issue
    """
)

''
st.write("""
- Frequency of data updates from **Kurzy.cz** ⚫ 
	- **They say**: Exchange rates are updated continuously, with a few minutes delay compared to the source.
	- Based on my observing should be 1x per 24 hours
	- History can be seen (Page in Czech language): https://www.kurzy.cz/kurzy-men/kurzovni-listek/csob/
"""
)

''
st.write("""
- Frequency of data updates from **Freecurrencyapi.com** 🔵
	- **They say**: The currency data on freecurrencyapi.com is updated on a daily basis. This means that while the API provides live and historical exchange rates, the data is refreshed once a day with end-of-day figures. 
	- 1x per 24 hours
"""
)


''
''
''
''
# F5B and ERD
st.write("##### Function 5, Function 5B, Background job and ERD:")

st.write("""
- **F5B** is based on the same APIs as **F5**
	- **F5** calls the APIs when the function is **used by user through app UI** only
	- **F5B** uses **background job** to continuously collect data and save it into DB, even if nobody is activelly using the app
""")

''
tab1, tab2, tab3 = st.tabs([
	"F5",
	"F5B job",
	"F5B"
])

tab1.image(Assets.Images.f5_description_uml_seq_f5)
tab2.image(Assets.Images.f5_description_uml_seq_f5b_job)
tab3.image(Assets.Images.f5_description_uml_seq_f5b)

''
''
st.write("""
- **The background job runs multiple times a day** 
- Triggered through **GitHub Actions** cron
- The data are saved into DB and **when F5B is used, the data are visualized** -> Trend of exchange rate in time can be seen 
""")

st.write("""
- The DB includes also **metadata** tables for troubleshooting and monitoring purposes
	- Tables capturing fail reasons of each API
	- Table capturing runs of the background job 
""")

''
st.image("Pictures/Function_5/F5B_ERD_v1.svg")

# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
	label = "Function 5",
	page="Subpages/F5_FUNCTION_exchange.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/play_circle:"
	) 