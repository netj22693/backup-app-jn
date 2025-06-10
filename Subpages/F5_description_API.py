import streamlit as st


# For visibility the API structure from kurzy.cz
json_api_structure = """
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


st.write("# Function 5")
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
- For visibility and calculation purposes. This function offers **simple calculator** to convert values between currencies.
		 
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

# Expander API JSON 
with st.expander("API JSON structure - Kurzy.cz", icon= ":material/code:"):

	''
	st.write("""
	- This Function 5 receives the full predefined API data from Kurzy.cz 
		  
	- And parses specifically:
		- "EUR" : { "dev_stred" : float value }
		- "USD" : { "dev_stred" : float value }
		  
		
	""")


	''
	''
	''
	st.write("The full JSON data:")
	st.code(
		json_api_structure,
		language= 'json',
		line_numbers=True,
		height=700)

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