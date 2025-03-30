import streamlit as st

st.set_page_config(page_title="XSD, XML Schema")




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

st.write("# XSD, XML Schema")
st.write(
    '''
Description of XML structure/XML Schema with which this application works. There is a **download button at the end of this page** to download XML Schema in both .txt and .xsd format.

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
st.write("#### Diagram with element properties:")
st.write("*For better visibility - put cursor on the picture and click on the icon in the right upper corner")
st.write("###### Header:")
''
''  
st.image("Pictures/V2_pictures/header properties_2.png")
''
''  
st.image("Pictures/V2_pictures/xsd_header_2.png")
''
''  
st.write("###### Detail:")
''
''  
st.image("Pictures/V2_pictures/detail properties_2.png")
''
''  
st.image("Pictures/V2_pictures/xsd_detail_2.png")
''
''
with st.expander("Show XSD structure - code", icon= ":material/code:"):
	st.code(xsd_structure, language= 'xml', line_numbers=True, height=700)

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
st.write('''
Additional rules:
- **<service_typ> rule - insurance:** sum all <service_price> values from <detail> when 'insurance' in <service_type>
- **<service_typ> rule - extended warranty:** sum all <service_price> values from <detail> when 'extended warranty' in <service_type>
'''
)
st.write("------")


# Download of XSD

st.write("#### XSD - download as .txt:")
if st.download_button("Download",data = xsd_structure  , file_name="XML Schema.txt", icon = ":material/download:"):
    st.info("Download will happen in few seconds")

st.write("------")

st.write("#### XSD - download as .xsd:")
if st.download_button("Download",data = xsd_structure  , file_name="XML Schema.xsd",icon = ":material/download:"):
    st.info("Download will happen in few seconds")

''
''
# ===== Page navigation at the bottom ======
st.write("-------")
st.page_link(
	label = "Previous page",
	page="Subpages/application_description_archimate.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/west:"
	) 

st.page_link(
    label = "Go to: Function 1",
	page="Subpages/XML_dowload.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/play_circle:",
	) 

