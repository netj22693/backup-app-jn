import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px

# For visibility the API structure from kurzy.cz
json_api_structure_1 = """
{
	"den": "20250610",
	"denc": "10.6.2025",
	"banka": "ČSOB",
	"url": "https://www.kurzy.cz/kurzy-men/kurzovni-listek/csob/",
	"kurzy": {
		"AUD": {
			"jednotka": 1,
			"dev_stred": 14.189,
			"dev_nakup": 13.811,
			"dev_prodej": 14.567,
			"val_stred": null,
			"val_nakup": null,
			"val_prodej": null,
			"nazev": "Australský dolar",
			"url": "https://www.kurzy.cz/aud"
		},
		"GBP": {
			"jednotka": 1,
			"dev_stred": 29.447,
			"dev_nakup": 28.663,
			"dev_prodej": 30.23,
			"val_stred": 29.447,
			"val_nakup": 28.663,
			"val_prodej": 30.23,
			"nazev": "Britská libra",
			"url": "https://www.kurzy.cz/gbp"
		},
		"CNY": {
			"jednotka": 1,
			"dev_stred": 3.026,
			"dev_nakup": 2.844,
			"dev_prodej": 3.208,
			"val_stred": null,
			"val_nakup": null,
			"val_prodej": null,
			"nazev": "Čínský juan",
			"url": "https://www.kurzy.cz/cny"
		},
		"DKK": {
			"jednotka": 1,
			"dev_stred": 3.324,
			"dev_nakup": 3.236,
			"dev_prodej": 3.412,
			"val_stred": null,
			"val_nakup": null,
			"val_prodej": null,
			"nazev": "Dánská koruna",
			"url": "https://www.kurzy.cz/dkk"
		},
		"EUR": {
			"jednotka": 1,
			"dev_stred": 24.796,
			"dev_nakup": 24.139,
			"dev_prodej": 25.454,
			"val_stred": 24.796,
			"val_nakup": 24.139,
			"val_prodej": 25.454,
			"nazev": "Euro",
			"url": "https://www.kurzy.cz/eur"
		},
		"JPY": {
			"jednotka": 100,
			"dev_stred": 15.014,
			"dev_nakup": 14.615,
			"dev_prodej": 15.413,
			"val_stred": null,
			"val_nakup": null,
			"val_prodej": null,
			"nazev": "Japonský jen",
			"url": "https://www.kurzy.cz/jpy"
		},
		"CAD": {
			"jednotka": 1,
			"dev_stred": 15.865,
			"dev_nakup": 15.442,
			"dev_prodej": 16.287,
			"val_stred": null,
			"val_nakup": null,
			"val_prodej": null,
			"nazev": "Kanadský dolar",
			"url": "https://www.kurzy.cz/cad"
		},
		"HUF": {
			"jednotka": 100,
			"dev_stred": 6.169,
			"dev_nakup": 5.999,
			"dev_prodej": 6.339,
			"val_stred": null,
			"val_nakup": null,
			"val_prodej": null,
			"nazev": "Maďarský forint",
			"url": "https://www.kurzy.cz/huf"
		},
		"NOK": {
			"jednotka": 1,
			"dev_stred": 2.158,
			"dev_nakup": 2.1,
			"dev_prodej": 2.216,
			"val_stred": null,
			"val_nakup": null,
			"val_prodej": null,
			"nazev": "Norská koruna",
			"url": "https://www.kurzy.cz/nok"
		},
		"PLN": {
			"jednotka": 1,
			"dev_stred": 5.805,
			"dev_nakup": 5.648,
			"dev_prodej": 5.963,
			"val_stred": null,
			"val_nakup": null,
			"val_prodej": null,
			"nazev": "Polský zlotý",
			"url": "https://www.kurzy.cz/pln"
		},
		"RON": {
			"jednotka": 1,
			"dev_stred": 4.918,
			"dev_nakup": 4.778,
			"dev_prodej": 5.057,
			"val_stred": null,
			"val_nakup": null,
			"val_prodej": null,
			"nazev": "Rumunský lei",
			"url": "https://www.kurzy.cz/ron"
		},
		"SEK": {
			"jednotka": 1,
			"dev_stred": 2.264,
			"dev_nakup": 2.202,
			"dev_prodej": 2.325,
			"val_stred": null,
			"val_nakup": null,
			"val_prodej": null,
			"nazev": "Švédská koruna",
			"url": "https://www.kurzy.cz/sek"
		},
		"CHF": {
			"jednotka": 1,
			"dev_stred": 26.437,
			"dev_nakup": 25.741,
			"dev_prodej": 27.132,
			"val_stred": 26.437,
			"val_nakup": 25.741,
			"val_prodej": 27.132,
			"nazev": "Švýcarský frank",
			"url": "https://www.kurzy.cz/chf"
		},
		"TRY": {
			"jednotka": 100,
			"dev_stred": 55.284,
			"dev_nakup": 51.849,
			"dev_prodej": 58.72,
			"val_stred": null,
			"val_nakup": null,
			"val_prodej": null,
			"nazev": "Turecká lira",
			"url": "https://www.kurzy.cz/try"
		},
		"USD": {
			"jednotka": 1,
			"dev_stred": 21.743,
			"dev_nakup": 21.165,
			"dev_prodej": 22.321,
			"val_stred": 21.743,
			"val_nakup": 21.165,
			"val_prodej": 22.321,
			"nazev": "Americký dolar",
			"url": "https://www.kurzy.cz/usd"
		}
	}
}
"""

# For visibility the API structure from freecurrencyapi.com
json_api_structure_2 = """
{
  "data": {
    "USD": 1.1430007052
  }
}
"""



# ==================== Application scree + backend functions ==============
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
                    api_count = "https://api.freecurrencyapi.com/v1/status?apikey=fca_live_6SzWJxPYa8Co3Xr9ziCTd7Mt7Yavrhpy2M5A0JZ4"

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