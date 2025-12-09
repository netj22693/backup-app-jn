import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
from Subpages.F5_json_structures import json_api_structure_1, json_api_structure_2


# ==================== Application screen + backend functions ==============
st.write("# Description - Function 5")
''
''
st.write("""
    - **Function 5:** Exchange rate/calculation (CZK, EUR, USD) - **API based** with actual exchange rate
    """
    )
''
''
st.write("##### Business scenario:") 

st.write("""
- For visibility and calculation purposes. This function offers **a simple calculator** to convert values between currencies.
		 
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
- Comes from Kurzy.cz https://www.kurzy.cz/ 	
- CZK  to EUR and USD	 
"""
)

''

st.caption("""
Kurzy.cz is a Czech portal specializing in the field of finance - investments, business and personal finance. It was founded in 2000 originally at fin.cz and since 2006 at kurzy.cz. According to Netmonitor statistics, the kurzy.cz server was visited by a total of 3,207,000 real users in March 2022, making the server one of the 15 most visited Czech media.
https://cs.wikipedia.org/wiki/Kurzy.cz
"""
)


''
''
# Expander API 1 JSON 
with st.expander("API JSON structure - Kurzy.cz", icon= ":material/help:"):

	''
	st.write("""
	- API - **HTTP GET** request to retrieve data from a server
	- There is no limit defined (I didn't find) for get requests (but anyway  data caching set for 1 hour)
	- This Function 5 receives the full predefined API data from Kurzy.cz 
	- There is no possibility to customize the API data
		  
	- So once received, there is a parsing, specifically:
		- "EUR" : { "dev_stred" : float value }
		- "USD" : { "dev_stred" : float value }
		  
		
	""")


	''
	''
	''
	st.write("The full JSON data:")
	st.code(
		json_api_structure_1,
		language= 'json',
		line_numbers=True,
		height=400)

	

''
''
''
st.write("""
- Comes from Freecurrencyapi.com https://app.freecurrencyapi.com/	
- EUR to USD	 
"""
)

''
st.caption("""
Free Currency Conversion API
The 100% free solution for handling exchange rate conversions. Our currency API provides live & historical exchange rate data ranging from 1999 until today.
https://freecurrencyapi.com/
"""
)

''
''
# Expander API 2 JSON 
with st.expander("API JSON structure - Freecurrencyapi.com", icon= ":material/help:"):

	''
	st.write("""
	- API - **HTTP GET** request to retrieve data from a server
	- This Function 5 receives **CUSTOMIZED** data from Freecurrencyapi.com 
	
		- "data" : { "USD" : float value }
		
		- Base Currency: EUR
		- Currency/Rate to: USD
	"""
	)


	''
	''
	''
	st.write("Customized JSON API data:")
	st.code(
		json_api_structure_2,
		language= 'json',
		line_numbers=True
		)

	''
	''
	st.write("The customization allows:")
	st.write("""
	- Make a registration 
	- Monitor the API requests 
	- And see some statistics
	- Also this UI is allowing to troubleshoot and reproduce the request + **retrospectivelly see every JSON data which were sent out** based on every GET the source application got. 
	- Possible to search based on API status, time, date...
	"""
	)
	''
	st.image("Pictures/Function_5/F5_description_api_statistics.png")
	''
	st.image("Pictures/Function_5/F5_description_api_statistics_another.png")
	''
	''
	''
	st.write("- This API is **limited to 5k requests per month**")
	st.write("- So here is also simple GET API to see statistics:")
	if st.button(
		"API Status",
		use_container_width=True,
		icon=":material/monitoring:"
	):
                
		# try-except logic to cover API unavailability
		try:
			# API count/remaining
			api_key = st.secrets["F5_api_2"]["password"]

			api_count = f"https://api.freecurrencyapi.com/v1/status?apikey={api_key}"

			# get reguest - cached for 10 minutes
			@st.cache_data(ttl=600)
			def get_response_api_3(api_count):
				api_3 = requests.get(api_count, verify=False, timeout=5).text
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
			st.warning("""
			- Apologies, the status API is currently NOT available due to:
				- Either the API system refused to establish connection
				- Or limit of 5k requests per month has been reached              
			"""
			)
              

''
''
''
''
# Archimate
st.write("##### Archimate Diagram:") 
''
st.write("*For better visibility - put cursor on the picture and click on the icon in the right upper corner")
st.image("Pictures/Function_5/F5_description_archimate_api.svg")

''
''
''
st.write("""
- The **both** APIs are called **at the same time**
	- The reason is that the **calls for both happen when the function 5 (the page) is opened** -> to get the fresh data (Exchange rates) visible in the application
    """
)

''
''
st.write("""
- **To do not overutilize the API calls, there is a DATA CACHING set on our application**
	- The caching is applied for **1 hour** (3600 seconds)
	- The caching is applicable for **1 session**
    - Also there is a **timeout after 5 seconds** in case that target systems (any of them) will, from some reason, refuse to establish connection with our application
    """
)

''
''
st.write("""
- Frequency of data updates from **Kurzy.cz**
	- **They say**: Exchange rates are updated continuously, with a few minutes delay compared to the source.
	- Based on my observing should be 1x per 24 hours
	- History can be seen (Page in Czech language): https://www.kurzy.cz/kurzy-men/kurzovni-listek/csob/
"""
)

''
''
st.write("""
- Frequency of data updates from **Freecurrencyapi.com**
	- **They say**: The currency data on freecurrencyapi.com is updated on a daily basis. This means that while the API provides live and historical exchange rates, the data is refreshed once a day with end-of-day figures. 
	- 1x per 24 hours
"""
)

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