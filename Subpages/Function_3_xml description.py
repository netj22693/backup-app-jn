import streamlit as st

st.set_page_config(page_title="XSD, XML Schema")

st.write("# XSD, XML Schema")
st.write(
    '''
Description of XML structure/XML Schema with which this Function 3 works. There is a download button at the end of this page to download XML Schema in both .txt and .xsd format.

'''
)

st.write("----")
st.write("#### Diagram:")
'''
Basic principle: The XML is split into 3 main segments - header, detail and transport. 
'''
''    
st.image("Pictures/Function_3/XSD main elements.png")
''
''  
''
st.write("###### Header:")
'''
Header element includes nested elements providing key information/summary about an order which is created through the Function 3 in this app. 
'''
'' 
st.image("Pictures/Function_3/XSD header.png")
''
''  
''
st.write("###### Detail:")
'''
Detail element includes also nested elements. They are used for information about the product which was purchased and whether any additional service for the product was bought or not (Insurance, Extended varanty).
'''
'' 
st.image("Pictures/Function_3/XSD detail.png")
''
''  
''
st.write("###### Transportation:")
'''
New element for this Function 3 (in comparison with Function 1 and 2 in this app) is element transportation. Also few nested elements which have information about transportation/delivery. 
'''
'' 
st.image("Pictures/Function_3/XSD transportation.png")
st.write("----")

st.write("#### Principle of the XML in context of the Function 3:")
'''
In the application user provides key inputs about the product through input fields.Based on the inputs, function culculates and provides the remaining details (about your order) also necessary/to fulfill this predefined xml. 
'''
'' 
st.image("Pictures/Function_3/XML produced.png")
'' 
'''
Some of the fields/options are predefined and then application makes the calculation based on what you select from drop down lists. More can be seen when you use the function itself :).
'''
'' 
st.image("Pictures/Function_3/delivery details.png", width = 200)
'' 
'''
Also the predefined options in drop-down lists are set as xs:restriction in the XSD -> just these values are allowed for the XML.
'''
'' 
st.image("Pictures/Function_3/XSD dropdowns.png")

st.write("----") 


xsd_as_string ='''<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" elementFormDefault="qualified" attributeFormDefault="unqualified">
	<xs:element name="invoice">
		<xs:complexType>
			<xs:sequence>
				<xs:element name="header">
					<xs:complexType>
						<xs:sequence>
							<xs:element name="order_number" type="xs:string"/>
							<xs:element name="customer" type="xs:string"/>
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
				<xs:element name="detail">
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
													<xs:pattern value="None|extended varanty|insurance"/>
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
					</xs:complexType>
				</xs:element>
				<xs:element name="transportation">
					<xs:complexType>
						<xs:sequence>
							<xs:element name="transporter">
								<xs:simpleType>
									<xs:restriction base="xs:string">
										<xs:pattern value="DHL|Fedex"/>
									</xs:restriction>
								</xs:simpleType>
							</xs:element>
							<xs:element name="country">
								<xs:simpleType>
									<xs:restriction base="xs:string">
										<xs:pattern value="Czech Republic|Slovakia"/>
									</xs:restriction>
								</xs:simpleType>
							</xs:element>
							<xs:element name="size">
								<xs:simpleType>
									<xs:restriction base="xs:string">
										<xs:pattern value="small|medium|large"/>
									</xs:restriction>
								</xs:simpleType>
							</xs:element>
							<xs:element name="transport_price">
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
		</xs:complexType>
	</xs:element>
</xs:schema>
'''

st.write("#### XSD - download as .txt:")
if st.download_button("Download",data = xsd_as_string  , file_name="XML Schema for function 3.txt"):
    st.info("Download will happen in few seconds")

st.write("------")

st.write("#### XSD - download as .xsd:")
if st.download_button("Download",data = xsd_as_string  , file_name="XML Schema for function 3.xsd"):
    st.info("Download will happen in few seconds")

st.write("------")

st.code(xsd_as_string, language= 'xml', line_numbers=True, height=700)