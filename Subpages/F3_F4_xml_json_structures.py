
# ============= XML & XSD ===================
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

xml_as_string ='''<?xml version="1.0" encoding="UTF-8"?>
<invoice>
	<header>
		<order_number>String</order_number>
		<customer>String</customer>
		<invoice_number>INV-000000</invoice_number>
		<date>2025-03-10</date>
		<price>
			<total_sum>0.01</total_sum>
			<currency>Kč</currency>
		</price>
	</header>
	<detail>
		<category>PC</category>
		<product_name>String</product_name>
		<price_amount>0</price_amount>
		<additional_service>
			<service>N</service>
			<service_type>None</service_type>
			<service_price>0</service_price>
		</additional_service>
	</detail>
	<transportation>
		<transporter>DHL</transporter>
		<country>Slovakia</country>
		<size>large</size>
		<transport_price>0</transport_price>
	</transportation>
</invoice>
'''



# ============= JSON ===================
json_structure = '''
{
    "header": {
        "order_number": "157",
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