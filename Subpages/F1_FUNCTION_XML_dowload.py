import streamlit as st
import xml.etree.ElementTree as ET
from Subpages.F1_F2_xml_structures import xml_data_euro, xml_data_koruna, xml_data_usdollar, xml_empty_template


# ======================== Screen part ==================================

st.write("# XML download")
''
st.write(
    '''
Here you can download XMLs which can be used for parsing:

1) Predefind file - sum matches - currency: euro - € - 15 detail lines
2) Predefind file - sum matches - currency: koruna - Kč - 12 detail lines
3) Predefind file - sum does not match - currency: US dollar - $ - 15 detail lines
4) XML Template

*The number of detail lines is basically not limited as defined in the XSD / XML Schema -> no need to stick to 12 or 15 lines :)
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
with st.expander("Show XML structure - code", icon= ":material/code:"):
	st.code(xml_data_euro, language= 'xml', line_numbers=True, height=700)

if st.download_button("Download",data = xml_data_euro  , file_name="XML_euro_sum_matching.xml", icon = ":material/download:"):
    st.info("Download will happen in few seconds")

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
with st.expander("Show XML structure - code", icon= ":material/code:"):
	st.code(xml_data_koruna, language= 'xml', line_numbers=True, height=700)
     
if st.download_button("Download",data = xml_data_koruna  , file_name="XML_koruna_sum_matching.xml", icon = ":material/download:"):
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
with st.expander("Show XML structure - code", icon= ":material/code:"):
	st.code(xml_data_usdollar, language= 'xml', line_numbers=True, height=700)
      
if st.download_button("Download",data = xml_data_usdollar , file_name="XML_usdollar_sum_not matching.xml", icon = ":material/download:"):
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
	st.link_button(
		label = "Go to XSD page",
		url="https://dataparsing.streamlit.app/F1_F2_description_XML_XSD",
		help="The button will redirect to the relevant page within this app for download.",
		width="stretch",
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
		label = "Go to Function 2",
		page="Subpages/F2_FUNCTION_XML_parsing_to_txt_outcome.py",
		help="The button will redirect to the relevant page within this app.",
		width="stretch",
		icon=":material/play_circle:"
		) 
	''
	''

      

''
''
''
st.image("Pictures/V2_pictures/XML download - scenario 4.png")
''
''
with st.expander("Show XML structure - code", icon= ":material/code:"):
	st.code(xml_empty_template, language= 'xml', line_numbers=True, height=700)
      
if st.download_button("Download",data = xml_empty_template , file_name="XML_empty_template.xml", icon = ":material/download:"):
    st.info("Download will happen in few seconds")



# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
    label = "Go to: Function 2",
	page="Subpages/F2_FUNCTION_XML_parsing_to_txt_outcome.py",
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
    icon=":material/play_circle:",
	) 

st.page_link(
	label = "Previous page",
	page="Subpages/F2_description_DB_ERT.py",
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
	icon=":material/west:"
	) 

