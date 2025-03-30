import streamlit as st
import xml.etree.ElementTree as ET

# ========= Firstly - data options/XML structures -> objects ===============

xml_data_euro = """<?xml version="1.0" encoding="UTF-8"?>
<invoice>
	<header>
		<customer>ABC s.r.o.</customer>
		<invoice_number>INV-123456</invoice_number>
		<date>2025-03-10</date>
		<price>
			<total_sum>3291.00</total_sum>
			<total_sum_services>168.00</total_sum_services>
			<currency>euro</currency>
		</price>
	</header>
	<detail id="1">
		<category>PC</category>
		<product_name>HP ProBook</product_name>
		<price_amount>240.00</price_amount>
		<additional_service>
			<service>Y</service>
			<service_type>extended warranty</service_type>
			<service_price>9.00</service_price>
		</additional_service>
	</detail>
	<detail id="2">
		<category>TV</category>
		<product_name>Philips The One</product_name>
		<price_amount>300.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="3">
		<category>Gaming</category>
		<product_name>Playstation 5 Pro</product_name>
		<price_amount>202.00</price_amount>
		<additional_service>
			<service>Y</service>
			<service_type>insurance</service_type>
			<service_price>25.00</service_price>
		</additional_service>
	</detail>
	<detail id="4">
		<category>PC</category>
		<product_name>MacBook Air 13</product_name>
		<price_amount>183.00</price_amount>
		<additional_service>
			<service>Y</service>
			<service_type>insurance</service_type>
			<service_price>15.00</service_price>
		</additional_service>
	</detail>
	<detail id="5">
		<category>Mobile phones</category>
		<product_name>Xiaomi Pad 7</product_name>
		<price_amount>99.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="6">
		<category>Gaming</category>
		<product_name>Playstation 5</product_name>
		<price_amount>132.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="7">
		<category>Mobile phones</category>
		<product_name>Xiaomi 15 Ultra 5G</product_name>
		<price_amount>340.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="8">
		<category>Mobile phones</category>
		<product_name>Xiaomi 15 Ultra </product_name>
		<price_amount>320.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="9">
		<category>Gaming</category>
		<product_name>Xbox Series S</product_name>
		<price_amount>71.00</price_amount>
		<additional_service>
			<service>Y</service>
			<service_type>insurance</service_type>
			<service_price>4.00</service_price>
		</additional_service>
	</detail>
	<detail id="10">
		<category>Gaming</category>
		<product_name>Kingdom Come: Deliverance 2</product_name>
		<price_amount>18.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="11">
		<category>Tablets</category>
		<product_name>iPad 10.9</product_name>
		<price_amount>99.00</price_amount>
		<additional_service>
			<service>Y</service>
			<service_type>extended warranty</service_type>
			<service_price>5.00</service_price>
		</additional_service>
	</detail>
	<detail id="12">
		<category>Tablets</category>
		<product_name>Samsung Galaxy Tab S9</product_name>
		<price_amount>99.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0</service_price>
		</additional_service>
	</detail>
	<detail id="13">
		<category>Major Appliances</category>
		<product_name>GORENJE NRK61CS2XL4</product_name>
		<price_amount>990.00</price_amount>
		<additional_service>
			<service>Y</service>
			<service_type>insurance</service_type>
			<service_price>100.00</service_price>
		</additional_service>
	</detail>
	<detail id="14">
		<category>Households</category>
		<product_name>BOSCH MUM58364</product_name>
		<price_amount>109.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0</service_price>
		</additional_service>
	</detail>
	<detail id="15">
		<category>Gaming</category>
		<product_name>Meta Quest 3S 128GB</product_name>
		<price_amount>89.00</price_amount>
		<additional_service>
			<service>Y</service>
			<service_type>insurance</service_type>
			<service_price>10.00</service_price>
		</additional_service>
	</detail>
</invoice>
"""


xml_data_koruna = """<?xml version="1.0" encoding="UTF-8"?>
<invoice>
	<header>
		<customer>ABC s.r.o.</customer>
		<invoice_number>INV-123456</invoice_number>
		<date>2025-03-10</date>
		<price>
			<total_sum>210930.00</total_sum>
			<total_sum_services>6169.00</total_sum_services>
			<currency>Kč</currency>
		</price>
	</header>
	<detail id="1">
		<category>PC</category>
		<product_name>HP ProBook</product_name>
		<price_amount>24000.00</price_amount>
		<additional_service>
			<service>Y</service>
			<service_type>extended warranty</service_type>
			<service_price>990.00</service_price>
		</additional_service>
	</detail>
	<detail id="2">
		<category>TV</category>
		<product_name>Philips The One</product_name>
		<price_amount>30000.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="3">
		<category>Gaming</category>
		<product_name>Playstation 5 Pro</product_name>
		<price_amount>20290.00</price_amount>
		<additional_service>
			<service>Y</service>
			<service_type>insurance</service_type>
			<service_price>2500.00</service_price>
		</additional_service>
	</detail>
	<detail id="4">
		<category>PC</category>
		<product_name>MacBook Air 13</product_name>
		<price_amount>18390.00</price_amount>
		<additional_service>
			<service>Y</service>
			<service_type>insurance</service_type>
			<service_price>1590.00</service_price>
		</additional_service>
	</detail>
	<detail id="5">
		<category>Mobile phones</category>
		<product_name>Xiaomi Pad 7</product_name>
		<price_amount>9990.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="6">
		<category>Gaming</category>
		<product_name>Playstation 5</product_name>
		<price_amount>13290.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="7">
		<category>Mobile phones</category>
		<product_name>Xiaomi 15 Ultra 5G</product_name>
		<price_amount>34000.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="8">
		<category>Mobile phones</category>
		<product_name>Xiaomi 15 Ultra </product_name>
		<price_amount>32000.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="9">
		<category>Gaming</category>
		<product_name>Xbox Series S</product_name>
		<price_amount>7190.00</price_amount>
		<additional_service>
			<service>Y</service>
			<service_type>insurance</service_type>
			<service_price>499.00</service_price>
		</additional_service>
	</detail>
	<detail id="10">
		<category>Gaming</category>
		<product_name>Kingdom Come: Deliverance 2</product_name>
		<price_amount>1890.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="11">
		<category>Tablets</category>
		<product_name>iPad 10.9</product_name>
		<price_amount>9990.00</price_amount>
		<additional_service>
			<service>Y</service>
			<service_type>extended warranty</service_type>
			<service_price>590.00</service_price>
		</additional_service>
	</detail>
	<detail id="12">
		<category>Tablets</category>
		<product_name>Samsung Galaxy Tab S9</product_name>
		<price_amount>9900.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0</service_price>
		</additional_service>
	</detail>
</invoice>
"""

xml_data_usdollar = """<?xml version="1.0" encoding="UTF-8"?>
<invoice>
	<header>
		<customer>ABC s.r.o.</customer>
		<invoice_number>INV-123456</invoice_number>
		<date>2025-03-10</date>
		<price>
			<total_sum>2000.00</total_sum>
			<total_sum_services>50.00</total_sum_services>
			<currency>US dollar</currency>
		</price>
	</header>
	<detail id="1">
		<category>PC</category>
		<product_name>HP ProBook</product_name>
		<price_amount>240.00</price_amount>
		<additional_service>
			<service>Y</service>
			<service_type>extended warranty</service_type>
			<service_price>9.00</service_price>
		</additional_service>
	</detail>
	<detail id="2">
		<category>TV</category>
		<product_name>Philips The One</product_name>
		<price_amount>300.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="3">
		<category>Gaming</category>
		<product_name>Playstation 5 Pro</product_name>
		<price_amount>202.00</price_amount>
		<additional_service>
			<service>Y</service>
			<service_type>insurance</service_type>
			<service_price>25.00</service_price>
		</additional_service>
	</detail>
	<detail id="4">
		<category>PC</category>
		<product_name>MacBook Air 13</product_name>
		<price_amount>183.00</price_amount>
		<additional_service>
			<service>Y</service>
			<service_type>insurance</service_type>
			<service_price>15.00</service_price>
		</additional_service>
	</detail>
	<detail id="5">
		<category>Mobile phones</category>
		<product_name>Xiaomi Pad 7</product_name>
		<price_amount>99.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="6">
		<category>Gaming</category>
		<product_name>Playstation 5</product_name>
		<price_amount>132.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="7">
		<category>Mobile phones</category>
		<product_name>Xiaomi 15 Ultra 5G</product_name>
		<price_amount>340.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="8">
		<category>Mobile phones</category>
		<product_name>Xiaomi 15 Ultra </product_name>
		<price_amount>320.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="9">
		<category>Gaming</category>
		<product_name>Xbox Series S</product_name>
		<price_amount>71.00</price_amount>
		<additional_service>
			<service>Y</service>
			<service_type>insurance</service_type>
			<service_price>4.00</service_price>
		</additional_service>
	</detail>
	<detail id="10">
		<category>Gaming</category>
		<product_name>Kingdom Come: Deliverance 2</product_name>
		<price_amount>18.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="11">
		<category>Tablets</category>
		<product_name>iPad 10.9</product_name>
		<price_amount>99.00</price_amount>
		<additional_service>
			<service>Y</service>
			<service_type>extended warranty</service_type>
			<service_price>5.00</service_price>
		</additional_service>
	</detail>
	<detail id="12">
		<category>Tablets</category>
		<product_name>Samsung Galaxy Tab S9</product_name>
		<price_amount>99.00</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0</service_price>
		</additional_service>
	</detail>
</invoice>
"""

xml_empty_template = """<?xml version="1.0" encoding="UTF-8"?>
<invoice>
	<header>
		<customer/>
		<invoice_number/>
		<date/>
		<price>
			<total_sum/>
			<total_sum_services/>
			<currency/>
		</price>
	</header>
	<detail id="1">
		<category/>
		<product_name/>
		<price_amount/>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="2">
		<category/>
		<product_name/>
		<price_amount/>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="3">
		<category/>
		<product_name/>
		<price_amount/>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="4">
		<category/>
		<product_name/>
		<price_amount/>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="5">
		<category/>
		<product_name/>
		<price_amount/>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="6">
		<category/>
		<product_name/>
		<price_amount/>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="7">
		<category/>
		<product_name/>
		<price_amount/>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="8">
		<category/>
		<product_name/>
		<price_amount/>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="9">
		<category/>
		<product_name/>
		<price_amount/>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="10">
		<category/>
		<product_name/>
		<price_amount/>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="11">
		<category/>
		<product_name/>
		<price_amount/>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
	<detail id="12">
		<category/>
		<product_name/>
		<price_amount/>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0.00</service_price>
		</additional_service>
	</detail>
</invoice>
"""
# ======================== Screen part ==================================

st.set_page_config(page_title="XML download")
st.write("# XML download")
''
st.write(
    '''
Here you can download XMLs which can be used for parsing:

1) Predefind file - sum matches - currency: euro - € - 15 detail lines
2) Predefind file - sum matches - currency: koruna - Kč - 12 detail lines
3) Predefind file - sum does not match - currency: US dollar - $ - 15 detail lines
4) XML Template

*The number of detail lines is basically not limited as defined in the XSD / XML Schema -> no need to stick 12 or 15 lines :)
'''
)

st.write("------")

# Option 1
st.write("#### 1) Predefined file:")
''
st.write(
    '''
- Currency: euro - €
- Lines in detail segment: 15
- <total_sum> value matches sum of <price_amount> values in detail segment
- <total_sum_services> matches sum of <service_price> in detail segment
''')
''
''
'''
-> Validation step in the application will be passed
'''
''
''
st.image("Pictures/V2_pictures/XML download - scenario 1_3.png")
''
''
with st.expander("Show XML structure - code"):
	st.code(xml_data_euro, language= 'xml', line_numbers=True, height=700)

if st.download_button("Download",data = xml_data_euro  , file_name="XML_euro_sum matches.xml", icon = ":material/download:"):
    st.info("Download will happen in few seconds")
''
st.write("------")


# Option 2
st.write("#### 2) Predefined file:")
''
st.write(
    '''
- Currency: Koruna - Kč
- Lines in detail segment: 12
- <total_sum> value matches sum of <price_amount> values in detail segment
- <total_sum_services> matches sum of <service_price> in detail segment
''')
''
''
'''
-> Validation step in the application will be passed
'''
''
''
st.image("Pictures/V2_pictures/XML download - scenario 2_2.png")
''
''
with st.expander("Show XML structure - code"):
	st.code(xml_data_koruna, language= 'xml', line_numbers=True, height=700)
     
if st.download_button("Download",data = xml_data_koruna  , file_name="XML_koruna_sum matches.xml", icon = ":material/download:"):
    st.info("Download will happen in few seconds")

st.write("------")

# Option 3
st.write("#### 3) Predefined file:")
''
st.write(
    '''
- Currency: US dollar - $
- Lines in detail segment: 15
- <total_sum> value does **NOT** match sum of <price_amount> values in detail segment
- <total_sum_services> does **NOT** match sum of <service_price> in detail segment
''')
''
''
'''
-> Validation step in the application will show this inconsistency of numbers
'''
''
''
st.image("Pictures/V2_pictures/XML download - scenario 3_2.png")
''
''
with st.expander("Show XML structure - code"):
	st.code(xml_data_usdollar, language= 'xml', line_numbers=True, height=700)
      
if st.download_button("Download",data = xml_data_usdollar , file_name="XML_usdollar_sum not match.xml", icon = ":material/download:"):
    st.info("Download will happen in few seconds")

st.write("------")


# Option 4
st.write("#### 4) XML Template:")
''
st.write(
    '''
- Empty template
- Lines in detail segment: 12 
- Data to be fulfilled manually
'''
)
'''
- **(!) It is recommended: Once the XML is fullfiled, pair it and validate it against XSD. It will help to make sure that the XML will be processed throught the application and will not fail due to data quality issue**
'''
'''
- *XSD - can be downloaded from the page Functions 1 and 2 "Description - XSD, XML Schema"*
'''
''
with st.expander(
	"How to pair XML with XSD",
	icon= ":material/help_outline:"
	):
    
	st.write("1) Download XSD Schema from this application:")
	''
	st.page_link(
		label = "Go to XSD page",
		page="Subpages/XML_XSD_schema.py",
		help="The button will redirect to the relevant page within this app for download.",
		use_container_width=True,
		icon=":material/launch:"

		) 
	''
	''
	st.write("2) At the **BOTTOM** of the page - download button .xsd format -> XSD will be downloaded")
	''
	st.image("Pictures/V2_pictures/XSD download button.png", width=130)
	''
	''
	st.write("3) Find location where the XSD is located on your device (probably in Downloads folder)")
	''
	''
	st.write("4) Download XML Template from this section 4), just below :)")
	''
	''
	st.write("5) Open the XML Template file in your data editor (Notepad++ is for free)")
	''
	st.image("Pictures/V2_pictures/Altova notepad.png")
	''
	''
	st.write("6) Extend the XML root element <invoice> by the following:")
	''
	st.image("Pictures/V2_pictures/root extended.png")
	''
	st.write('''
		xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
		xsi:noNamespaceSchemaLocation="*location of your XSD file*">
		'''
	)
	''
	''
	st.write("7) **XML should be paired with XSD now**")
	''
	''
	st.write("8) Depending on data editor tool you use - you can work with the validation and control that you follow predefined rules in the XSD")
	''
	st.image("Pictures/V2_pictures/validation xsd final_2.png")
	''
	''
	st.write("9) Once no error detected in your XML -> you can upload it in the app in Function 2 section")
	''
	st.image("Pictures/V2_pictures/no error.png")
	''
	''
	st.page_link(
		label = "Go to Function 2 - 2. XML - Parsing, Validation, Vizualization",
		page="Subpages/XML_parsing_to_txt_outcome.py",
		help="The button will redirect to the relevant page within this app.",
		use_container_width=True,
		icon=":material/launch:"
		) 
	''
	''

      

''
''
''
st.image("Pictures/V2_pictures/XML download - scenario 4.png")
''
''
with st.expander("Show XML structure - code"):
	st.code(xml_empty_template, language= 'xml', line_numbers=True, height=700)
      
if st.download_button("Download",data = xml_empty_template , file_name="XML_empty_template.xml", icon = ":material/download:"):
    st.info("Download will happen in few seconds")



# ===== Page navigation at the bottom ======
st.write("-------")
''
''
st.page_link(
	label = "Previous page",
	page="Subpages/XML_XSD_schema.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/west:"
	) 

st.page_link(
    label = "Go to: Function 2",
	page="Subpages/XML_parsing_to_txt_outcome.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/play_circle:",
	) 