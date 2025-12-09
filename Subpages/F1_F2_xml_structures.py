

# Description XML & XSD - xsd 
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



# F1 structures 
xml_data_euro = """<?xml version="1.0" encoding="UTF-8"?>
<invoice>
	<header>
		<customer>ABC s.r.o.</customer>
		<invoice_number>INV-123456</invoice_number>
		<date>2025-03-10</date>
		<price>
			<total_sum>3291.00</total_sum>
			<total_sum_services>118.00</total_sum_services>
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
			<service_price>50.00</service_price>
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

# Note: this is not the same invoice as euro upper - there are 2 differences
# <total_sum_services>168.00</total_sum_services>,   in the euro upper is '118'
# <detail id="13"><product_name>GORENJE NRK61CS2XL4</product_name><service_price>100.00</service_price>,   in the euro upper is '50'
xml_data_euro_db_erd = """<?xml version="1.0" encoding="UTF-8"?>
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