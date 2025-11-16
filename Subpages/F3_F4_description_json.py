import streamlit as st


json_structure = '''
{
    "header": {
        "order_number": "75714928876285265049",
        "customer": "ABC s.r.o.",
        "invoice_number": "INV-893911",
        "date": "2025-03-23",
        "price": {
            "total_sum": 14423.85,
            "currency": "K\u010d"
        }
    },
    "detail": {
        "category": "Mobile phones",
        "product_name": "Samsung A22",
        "price_amount": 12499.0,
        "additional_service": {
            "service": "Y",
            "service_type": "insurance",
            "service_price": 1874.85
        }
    },
    "transportation": {
        "transporter": "DHL",
        "country": "Czech Republic",
        "size": "small",
        "transport_price": 50.0
    }
}

'''

json_schema = '''
{
	"$schema": "http://json-schema.org/draft-04/schema#",
	"type": "object",
	"properties": {
		"header": {
			"type": "object",
			"properties": {
				"order_number": {
					"type": "string"
				},
				"customer": {
					"type": "string"
				},
				"invoice_number": {
					"type": "string"
				},
				"date": {
					"type": "string"
				},
				"price": {
					"type": "object",
					"properties": {
						"total_sum": {
							"type": "number"
						},
						"currency": {
							"type": "string"
						}
					},
					"required": [
						"total_sum",
						"currency"
					]
				}
			},
			"required": [
				"order_number",
				"customer",
				"invoice_number",
				"date",
				"price"
			],
			"additionalProperties": false
		},
		"detail": {
			"type": "object",
			"properties": {
				"category": {
					"type": "string"
				},
				"product_name": {
					"type": "string"
				},
				"price_amount": {
					"type": "number"
				},
				"additional_service": {
					"type": "object",
					"properties": {
						"service": {
							"type": "string"
						},
						"service_type": {
							"type": "string"
						},
						"service_price": {
							"type": "number"
						}
					},
					"required": [
						"service",
						"service_type",
						"service_price"
					],
					"additionalProperties": false
				}
			},
			"required": [
				"category",
				"product_name",
				"price_amount",
				"additional_service"
			],
			"additionalProperties": false
		},
		"transportation": {
			"type": "object",
			"properties": {
				"transporter": {
					"type": "string"
				},
				"country": {
					"type": "string"
				},
				"size": {
					"type": "string"
				},
				"transport_price": {
					"type": "number"
				}
			},
			"required": [
				"transporter",
				"country",
				"size",
				"transport_price"
			],
			"additionalProperties": false
		}
	},
	"required": [
		"header",
		"detail",
		"transportation"
	],
	"additionalProperties": false
}
'''


st.write("# JSON Schema")
st.write(
    '''
Description of JSON structure with which these Functions 3 and 4 work. There is a download button at the end of this page to download the JSON Schema.

'''
)

st.write("----")
st.write("#### Diagram:")
''
'''
Basic principle: exactly as the XML also the JSON is split into 3 main segments - header, detail and transportation. So it can be said that the JSON structure has identical layout as the XML. Of course using JSON principles and rules. 
'''
''    
''
st.image("Pictures/Function_3/Function_3_json basic_2.png")
''
''
''


# Split into tabs 

tab1,tab2, tab3 = st.tabs([
      "Header",
      "Detail",
      "Transportation"
])

#Tab1
with tab1:
	st.write("###### Header:")
	''
	'''
	Header element includes nested elements providing key information/summary about an order which is created through the Function 3 in this app. 
	'''
	''
	''
	st.image("Pictures/Function_3/Function_3_json header_3.png")
	''
	''

#Tab2
with tab2:
	st.write("###### Detail:")
	''
	'''
	Detail element includes also nested elements. They are used for information about the product which was purchased and whether any additional service for the product was bought or not (Insurance, Extended varanty).
	'''
	''
	''
	st.write("*For better visibility - put cursor on the picture and click on the icon in the right upper corner")
	''
	st.image("Pictures/Function_3/Function_3_json detail_10.png")
	''
	''

#Tab3
with tab3:
	st.write("###### Transportation:")
	''
	'''
	Different element for this Function 3 (in comparison with Function 1 and 2 in this app) is element transportation. Also few nested elements which have information about transportation/delivery. 
	'''
	''
	''
	st.image("Pictures/Function_3/Function_3_json transportation_2.png")
	''
	''


''	
with st.expander("Show JSON structure - code", icon= ":material/code:"):
	st.code(json_structure, language= 'json', line_numbers=True, height=700)

with st.expander("Show JSON Schema structure - code", icon= ":material/code:"):
	st.code(json_schema, language= 'json', line_numbers=True, height=700)
	

st.write("-----")
st.write("#### Principle of the JSON in context of the Function 3:")
''
'''
In the application user provides key inputs about the product through input fields. Based on the inputs, function culculates and provides the remaining details (about your order) necessary/to fulfill this predefined json. 
'''
''
''
st.image("Pictures/Function_3/Function_3_JSON produced.png")


st.write("-----")

# Download of JSON Schema

st.write("#### Download of the JSON Schema for Functions 3 and 4:")
''
''

st.write("- Format .json")
if st.download_button(
            "Download",
            data = json_schema,
            file_name="JSON Schema for functions 3 and 4.json",
            icon = ":material/download:"
            ):

            st.info("Download will happen in few seconds")

''
''
st.write("- Format .txt")  
if st.download_button("Download",
            data = json_schema,
            file_name="JSON Schema for functions 3 and 4.txt",
            icon = ":material/download:"
            ):
        
            st.info("Download will happen in few seconds")


# ===== Page navigation at the bottom ======
''
''
st.write("-------")

st.page_link(
	label = "Next page",
	page="Subpages/F3_ERD.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/east:",
	) 

st.page_link(
	label = "Previous page",
	page="Subpages/F3_description_XML.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/west:"
	) 
