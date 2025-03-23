import streamlit as st
import json


# col1, col2 = st.columns(2)

# object_upl_json = col2.file_uploader("",key= "json")

# if object_upl_json is None:
#     col2.info("When a file uploaded, translation to XML will happen")
        

# if object_upl_json is not None:
#     col2.success("Upload complete")


#     resp = json.loads(object_upl_json)





import json
 
# create a sample json
 
a = {
	"header": {
		"order_number": "01428556724953407012",
		"customer": "Jan s.r.o.",
		"invoice_number": "INV-679747",
		"date": "2025-03-23",
		"price": {
			"total_sum": 12.0,
			"currency": "euro"
		}
	},
	"detail": {
		"category": "TV",
		"product_name": "A22",
		"price_amount": 10.0,
		"additional_service": {
			"service": "N",
			"service_type": "None",
			"service_price": 0.0
		}
	},
	"transportation": {
		"transporter": "DHL",
		"country": "Czech Republic",
		"size": "small",
		"transport_price": 2.0
	}
}

 
# Convert JSON to String
 
y = json.dumps(a)
 
st.write(y)
st.write(type(y))