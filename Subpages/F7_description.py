import streamlit as st

# dictionary:

dataset_test = ({
    "Prague" : {"big" : ["2","3"], "small" : ["6","7"], "train":"y", "air":"y"},
})   



json_api = {
  "data": {
    "CZK": 20.9216533403,
    "EUR": 0.8579601337
  }
}

#//////////



st.write("# Description - Function 7:")

''
''
st.write("""
    - **Function 7:** Transport calculation - API provides input
    """
    )
''
''
st.write("##### Business scenario:") 

st.write("""
- **Configurator** and **calculator** of **transport cost**, **journey distance** and **lasting** of the delivery based on:
    - Transport type:
         - Truck 
         - Train 
         - Airplane 
    - Distance of journey
	- Door-to-Door delivery or not
	- Shipment specifications (Insurance extra, Danger or Fragile goods)	 
"""
)

''
st.image("Pictures/Function_7/F7_desc_bpmn_customer process.svg")
''


''
''
st.write("##### Distance calculation:") 

st.write("""
- It is based on **coordinate system** - **R1C1** type	 
- There are **2 scales/grids** which help to the calculation - **'big'** and **'small'**
"""
)

''
st.image("Pictures/Function_7/F7_map_R1C1.png")
''

st.write("""
- Thus when **city onboarded**, each gets **'big'** and **'small'** R1C1 coordinates
- And information about **availability of infrastructure** -> transport type y/n (* 'Truck' has 'y' as a default for every city -> thus not in the dataset)
"""
)

st.code(dataset_test, language="python", wrap_lines=True, height=80)

st.write("""
- The **calculation happens based on the 'big' and 'small' units**
- **When Submit button used** - There is a logic of distributing the selected cities/their coordinates (From and To) **between 3 levels/functions** -> to get reasonable distance calculation
    - move within 1 unit 
    - move which is only horizontal or vertical
    - move which is diagonal
- **Each has slightly different logic for calculation** (specifically there is a correction coeficient when it comes to diagonal move)
"""
)
''
st.image("Pictures/Function_7/F7_desc_bpmn.svg")
''


''
st.write("##### Price calculation:") 

st.write("""
- **The price to deliver the shipment between selected cities** (From/To) is returned from **the same def/functions together with the distance** - was influenced by:
    - Selected transport type (Truck, Train, Airplane)
    - Type of service (delivery: Express, Standard, Slow)
    - Selected currency (koruna, euro)
    - **Daily currency exchange rate - :green[API based info]**
"""
)
st.write("""
- **The final price** is then **impacted by other selected inputs** from user:
    - **Extra insurance or Fragile goods or Dange goods** (multiple select possible) - calculated based on additional user inpur (Value of the goods/shipment)
    - And whethe there is extra **Door-To-Door delivery** (more details on the next page)
"""
)

''
''
st.image("Pictures/Function_7/F7_desc_uml_inputs.svg")

''
with st.expander("UML diagram - more details", icon= ":material/help:"):

	st.write("""
	- What user selects **influences** what the **application offers** in the other levels - types of **business scenarios & real case logic**
	""")
	
	st.write("""
	- **L1** - API/Currency -> Influences **L4** price for Delivery service
	- **L2** - Selection fo From/To cities -> influences options of Currency in **L3**
	- **L2** - Selection fo From/To cities -> influences options of Transport type **L4** (not every city has all transport types possible) 
	- **L4** - Transport type -> influences options for Door-to-Door delivery in **L5**
	- **L4** - Transport type -> influences options for Extra service (Airplane cannot transfer Danger goods)  in **L5**
	""")


''
''
st.write("##### API - Exchange rate:") 
st.write("""
- **Dynamic element** in the function
- **Actuall** daily exchange rate
- It is **USD** to **EUR** (euro) and **CZK** (koruna) -> **influences the based price per unit distance -> influences the calculation input and results**
"""
)

''
with st.expander("API info", icon= ":material/help:"):

	st.write("""
	- API - **HTTP GET** request to retrieve data from a server
	- This Function 7 receives **CUSTOMIZED** data from https://freecurrencyapi.com/
	""")
	
	st.code(json_api, "json" )

	st.write("""
	- Limit: **5k** requests per month
	""")
	


# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
    label = "Next page",
	page="Subpages/F7_description_dtd.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/east:",
	) 
