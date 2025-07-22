import streamlit as st





xsd_structure = '''<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" elementFormDefault="qualified" attributeFormDefault="unqualified">
	<xs:element name="invoice">
		<xs:complexType>
			<xs:sequence>
				<xs:element name="header">
					<xs:complexType>
						<xs:sequence>
							<xs:element name="customer">
								<xs:simpleType>
									<xs:restriction base="xs:string">
										<xs:minLength value="1"/>
									</xs:restriction>
								</xs:simpleType>
							</xs:element>
							<xs:element name="invoice_number">
								<xs:simpleType>
									<xs:restriction base="xs:string">
										<xs:minLength value="10"/>
										<xs:maxLength value="10"/>
										<xs:pattern value="[I]{1}[N]{1}[V]{1}[-]{1}[0-9]{6}"/>
									</xs:restriction>
								</xs:simpleType>
							</xs:element>
							<xs:element name="date">
								<xs:simpleType>
									<xs:restriction base="xs:date">
										<xs:minInclusive value="2025-03-10"/>
									</xs:restriction>
								</xs:simpleType>
							</xs:element>
							<xs:element name="price">
								<xs:complexType>
									<xs:sequence>
										<xs:element name="total_sum" default="0.01">
											<xs:simpleType>
												<xs:restriction base="xs:decimal">
													<xs:fractionDigits value="2"/>
													<xs:minInclusive value="0.01"/>
												</xs:restriction>
											</xs:simpleType>
										</xs:element>
										<xs:element name="total_sum_services">
											<xs:simpleType>
												<xs:restriction base="xs:decimal">
													<xs:minInclusive value="0.00"/>
													<xs:fractionDigits value="2"/>
												</xs:restriction>
											</xs:simpleType>
										</xs:element>
										<xs:element name="currency">
											<xs:simpleType>
												<xs:restriction base="xs:string">
													<xs:pattern value="euro|US dollar|Kč"/>
												</xs:restriction>
											</xs:simpleType>
										</xs:element>
									</xs:sequence>
								</xs:complexType>
							</xs:element>
						</xs:sequence>
					</xs:complexType>
				</xs:element>
				<xs:element name="detail" maxOccurs="unbounded">
					<xs:complexType>
						<xs:sequence>
							<xs:element name="category">
								<xs:simpleType>
									<xs:restriction base="xs:string">
										<xs:pattern value="PC|TV|Gaming|Mobile phones|Tablets|Major Appliances|Households"/>
									</xs:restriction>
								</xs:simpleType>
							</xs:element>
							<xs:element name="product_name" type="xs:string"/>
							<xs:element name="price_amount">
								<xs:simpleType>
									<xs:restriction base="xs:decimal">
										<xs:minInclusive value="0.00"/>
										<xs:fractionDigits value="2"/>
									</xs:restriction>
								</xs:simpleType>
							</xs:element>
							<xs:element name="additional_service">
								<xs:complexType>
									<xs:sequence>
										<xs:element name="service" default="N">
											<xs:simpleType>
												<xs:restriction base="xs:string">
													<xs:length value="1"/>
													<xs:pattern value="Y|N"/>
												</xs:restriction>
											</xs:simpleType>
										</xs:element>
										<xs:element name="service_type" default="None">
											<xs:simpleType>
												<xs:restriction base="xs:string">
													<xs:pattern value="None|extended warranty|insurance"/>
												</xs:restriction>
											</xs:simpleType>
										</xs:element>
										<xs:element name="service_price" default="0.00">
											<xs:simpleType>
												<xs:restriction base="xs:decimal">
													<xs:minInclusive value="0.00"/>
													<xs:fractionDigits value="2"/>
												</xs:restriction>
											</xs:simpleType>
										</xs:element>
									</xs:sequence>
								</xs:complexType>
							</xs:element>
						</xs:sequence>
						<xs:attribute name="id" type="xs:integer" use="required" id="yes"/>
					</xs:complexType>
				</xs:element>
			</xs:sequence>
		</xs:complexType>
	</xs:element>
</xs:schema>
'''

# ========================== Screen ============================
st.write("# XSD, XML Schema")
st.write(
    '''
Description of XML structure/XML Schema with which this application, **Function 1 produces (Download) and Function 2 (Parsing and Visualization), works**. There is a **download button at the end of this page** to download the **XML Schema**.

'''
)

st.write("----")
st.write("#### Diagram:")
'''
Basic principle: The XML is split into 2 main segments - header and detail. 
'''
''
''' - header - can be only one time in the message -> it is a summary of the invoice'''
''' - detail - is unbounded -> reflecting line/purchased product information (the more products you buy, the more lines/details will be in)'''
''
''        
st.image("Pictures/V2_pictures/Simple level.png")
''
''
''  
# Split into tabs 1

tab1, tab2 = st.tabs([
	"Header",
	"Detail"
])


#tab1 
with tab1:

        st.write("###### Header:")
        ''
        st.write("- Diagram with element properties")
        ''
        ''  
        st.write("*For better visibility - put cursor on the picture and click on the icon in the right upper corner")
        ''
        st.image("Pictures/V2_pictures/header properties_2.png")
        ''
        ''  
        st.image("Pictures/V2_pictures/xsd_header_2.png")
        ''
        ''  

#tab2 
with tab2:
         
        st.write("###### Detail:")
        ''
        st.write("- Diagram with element properties")
        ''
        ''  
        st.write("*For better visibility - put cursor on the picture and click on the icon in the right upper corner")
        '' 
        st.image("Pictures/V2_pictures/detail properties_2.png")
        ''
        ''  
        st.image("Pictures/V2_pictures/xsd_detail_2.png")
        ''
        ''


with st.expander("Show XSD structure - code", icon= ":material/code:"):
	st.code(xsd_structure, language= 'xml', line_numbers=True, height=700)


st.write("------")
''
st.write("#### Message definition overview:")
''
''
st.image("Pictures/Function_2/F2_XML_layout_table.png")

st.write("----")

st.write("#### Principle of the XML:")
''
''  
st.image("Pictures/V2_pictures/Principle_3.png")
''
''  
st.write('''
As explained upper, there are 2 main segments (header and detail). Each of them has its own specific nested elements -> sub-elements. They provide more detail view on the invoice. 
'''
)
''
''  
st.write("###### In context of data parsing:")
''
st.write('''
The application does the following, when XML uploaded:
- Parsing of data from all the elements (except <service>)
- Calculation and validation of the data (if header matches detail -> visible in the application)
-  Take the parsed data to get the relevant information visible and visualized in the application
'''
)
''
st.image("Pictures/V2_pictures/Principle in context of parsing8.png")
''
st.write('''
- **<customer>** - parsed as is ; data visualization
- **<invoice_number>** - parsed as is ; data visualization
- **<date>** - parsed as is - YYYY-MM-DD ; data visualization
- **<total_sum>** - parsed as is ; for validation & data visualization
- **<total_sum_services>** - parsed as is ; for validation & data visualization 
- **<currency>** - parsed as is ; reflects the currency in the application - euro|US dollar|Kč
- attribute **id=** - parsed as is ; for purposes of no. of products and visualization 
- **<category>** - parsed as is ; for purposes of filtering in application - PC|TV|Gaming|Mobile phones|Tablets|Major Appliances|Households
- **<product_name>** - parsed as is ; for visualization
- **<price_amount>** - parsed as is ; for validation & data visualization
- **<service>** - not parsed 
- **<service_type>** - parsed as is ; important for logic of calculation which application does - None|extended warranty|insurance
- **<service_price>** - parsed as is ; important for logic of calculation which application does + for validation & data visualization
'''
)
''  
st.write("###### Rules in the application from XML point of view:")
''
st.write('''
Validation:
- **<total_sum> rule:** sum all <price_amount> values from <detail> and compare with <total_sum>
- **<total_sum_services> rule:** sum all <service_price> values from <detail> and compare with <total_sum_services>
'''
)
''
with st.expander(
    "Validation",
    icon= ":material/help_outline:"
	):
    
	st.write("Example of validation in the Function 2:")
	st.image("Pictures/V2_pictures/validation.png")
	
''
''
st.write('''
Additional rules:
- **<service_typ> rule - insurance:** sum all <service_price> values from <detail> when 'insurance' in <service_type>
- **<service_typ> rule - extended warranty:** sum all <service_price> values from <detail> when 'extended warranty' in <service_type>
'''
)
''
with st.expander(
    "Example of data parsing - insurance and extended warranty",
    icon= ":material/help_outline:"
	):
    
	st.write("Data parsing based on service type:")
	''
	st.image("Pictures/V2_pictures/Parsing help_2.png")
	''
	''
	st.write("Anti-pattern:")
	st.write(" - In case that there will be any price value but service type as 'None', the parsing mechanism will ignore the value")
	''
	st.image("Pictures/V2_pictures/None-not parsed.png")
	
''
st.write("------")

st.write("#### XML against XSD validation:")
''
st.write("""
- Why the **XSD/XML Schema** is important?
	- Because it is **main function** programmed in the **Function 2**
	- It helps to **keep the expected data quality** and helps to **reduce 99% of failures** (my estimate) during processing of the XML invoice
    - The **XSD is stored in repository** and whenever XML invoice uploaded by user -> the XSD is called by the programmed function to make a validation:
		- If data **okay** -> Function 2 executes next steps
        - If data **not** okay -> User will see an alert on screen -> Function 2 stopped
""")

''
''
st.image("Pictures/Function_2/F2_diagram_xml_xsd_validation.svg")

''
st.write("------")


# Download of XSD

st.write("#### Download of the XSD for Functions 1 and 2:")
''
''

st.write("- Format .xsd")
if st.download_button(
            "Download",
            data = xsd_structure,
            file_name="XML_Schema_for_functions_1_and_2.xsd",
            icon = ":material/download:"
            ):

            st.info("Download will happen in few seconds")

''
''
st.write("- Format .txt")  
if st.download_button("Download",
            data = xsd_structure,
            file_name="XML_Schema_for_functions_1_and_2.txt",
            icon = ":material/download:"
            ):
        
            st.info("Download will happen in few seconds")


# How to pair XSD 1 XML

''
''
''
''
st.write("*In case you want to troubleshoot your XML message:")
with st.expander(
	"How to pair XML with XSD",
	icon= ":material/help_outline:"
	):

        ''
        ''
        st.write("1) Download XSD Schema **.xsd**")
        ''
        st.write("2) Find location where the XSD is located on your device (probably in Downloads folder)")
        ''
        st.write("3) Open the XML file, you want to check, in your data editor (Notepad++ is for free)")
        ''
        st.image("Pictures/V2_pictures/Altova notepad.png")
        ''
        ''
        st.write("4) Extend the XML root element <invoice> by the following:")
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
        st.write("5) **XML should be paired with XSD now**")
        ''
        ''
        st.write("6) Depending on data editor tool you use - you can work with the validation and control that you follow predefined rules in the XSD")
        ''
        st.image("Pictures/V2_pictures/validation xsd final_2.png")
        ''
        ''
        st.write("7) Once no error detected in your XML -> you can upload it in the app in Function 2 section")
        ''
        st.image("Pictures/V2_pictures/no error.png")








''
''
# ===== Page navigation at the bottom ======
st.write("-------")

st.page_link(
    label = "Next page",
	page="Subpages/F2_description_DB_ERT.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/east:",
	) 

st.page_link(
	label = "Previous page",
	page="Subpages/F1_F2_description_archimate.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/west:"
	) 


