
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
										<xs:pattern value="INV-[0-9]{1,10}"/>
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

xml_message_example ='''<?xml version="1.0" encoding="utf-8"?>
<invoice>
	<header>
		<order_number>215</order_number>
		<customer>Martina Nováková</customer>
		<invoice_number>INV-215</invoice_number>
		<date>2026-08-15</date>
		<price>
			<total_sum>20940.09</total_sum>
			<currency>Kč</currency>
		</price>
	</header>
	<detail>
		<category>Mobile phones</category>
		<product_name>Samsung A55</product_name>
		<price_amount>18990.99</price_amount>
		<additional_service>
			<service>Y</service>
			<service_type>extended warranty</service_type>
			<service_price>1899.10</service_price>
		</additional_service>
	</detail>
	<transportation>
		<transporter>DHL</transporter>
		<country>Czech Republic</country>
		<size>small</size>
		<transport_price>50.00</transport_price>
	</transportation>
</invoice>
'''



# ============= JSON ===================
json_message_example = '''
{
    "header": {
        "order_number": "215",
        "customer": "Martina Nov\u00e1kov\u00e1",
        "invoice_number": "INV-215",
        "date": "2026-08-15",
        "price": {
            "total_sum": 20940.09,
            "currency": "K\u010d"
        }
    },
    "detail": {
        "category": "Mobile phones",
        "product_name": "Samsung A55",
        "price_amount": 18990.99,
        "additional_service": {
            "service": "Y",
            "service_type": "extended warranty",
            "service_price": 1899.1
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

json_schema = '''{
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
					"type": "string",
					"pattern": "^INV-[0-9]{1,10}$"
				},
				"date": {
					"type": "string",
					"pattern": "^(2025-(03-(1[0-9]|[2-9][0-9])|0[4-9]-[0-9]{2}|1[0-2]-[0-9]{2})|202[6-9]-[0-9]{2}-[0-9]{2}|20[3-9][0-9]-[0-9]{2}-[0-9]{2}|2[1-9][0-9]{2}-[0-9]{2}-[0-9]{2})$"
				},
				"price": {
					"type": "object",
					"properties": {
						"total_sum": {
							"type": "number",
							"minimum": 0.01,
							"multipleOf": 0.01,
							"default": 0.01
						},
						"currency": {
							"type": "string",
							"enum": [
								"euro",
								"US dollar",
								"Kč"
							]
						}
					},
					"required": [
						"total_sum",
						"currency"
					],
					"additionalProperties": false
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
					"type": "string",
					"enum": [
						"PC",
						"TV",
						"Gaming",
						"Mobile phones",
						"Tablets",
						"Major Appliances",
						"Households"
					]
				},
				"product_name": {
					"type": "string"
				},
				"price_amount": {
					"type": "number",
					"minimum": 0,
					"multipleOf": 0.01
				},
				"additional_service": {
					"type": "object",
					"properties": {
						"service": {
							"type": "string",
							"minLength": 1,
							"maxLength": 1,
							"enum": [
								"Y",
								"N"
							],
							"default": "N"
						},
						"service_type": {
							"type": "string",
							"enum": [
								"None",
								"extended warranty",
								"insurance"
							],
							"default": "None"
						},
						"service_price": {
							"type": "number",
							"minimum": 0,
							"multipleOf": 0.01,
							"default": 0
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
					"type": "string",
					"enum": [
						"DHL",
						"Fedex"
					]
				},
				"country": {
					"type": "string",
					"enum": [
						"Czech Republic",
						"Slovakia"
					]
				},
				"size": {
					"type": "string",
					"enum": [
						"small",
						"medium",
						"large"
					]
				},
				"transport_price": {
					"type": "number",
					"minimum": 0,
					"multipleOf": 0.01
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

# ======= Highlights for UI =======
xsd_structure_rules_header = """
<!-- Invoice number is limited by REGEX pattern -->
<xs:element name="invoice_number">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:pattern value="INV-[0-9]{1,10}"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<!-- total_sum never can be 0 -->
<xs:element name="total_sum" default="0.01">
    <xs:simpleType>
        <xs:restriction base="xs:decimal">
            <xs:fractionDigits value="2"/>
            <xs:minInclusive value="0.01"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<!-- Currency has list of values to which it is limited euro|US dollar|Kč -->
<!-- It reflects the exact options which can be selected via UI -->
<xs:element name="currency">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:pattern value="euro|US dollar|Kč"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>
"""


xsd_structure_rules_detail = """
<!-- Category has list of values to which it is limited -->
<!-- It reflects the exact options which can be selected via UI -->
<xs:element name="category">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:pattern value="PC|TV|Gaming|Mobile phones|Tablets|Major Appliances|Households"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<!-- Service also limited to values Y|N -->
<!-- Dependent on if extra service was selected or not -->
<xs:element name="service" default="N">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:length value="1"/>
            <xs:pattern value="Y|N"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<!-- service_type has list of values to which it is limited -->
<!-- It reflects the exact options which can be selected via UI -->
<xs:element name="service_type" default="None">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:pattern value="None|extended warranty|insurance"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>
"""

xsd_structure_rules_transportation = """
<!-- Transporter has list of values to which it is limited -->
<!-- It reflects the exact options which can be selected via UI -->
<xs:element name="transporter">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:pattern value="DHL|Fedex"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<!-- Country also limited to values Czech Republic|Slovakia -->
<!-- It reflects the exact options which can be selected via UI -->
<xs:element name="country">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:pattern value="Czech Republic|Slovakia"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>

<!-- Size has list of values to which it is limited -->
<!-- It reflects the exact options which can be selected via UI -->
<xs:element name="size">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:pattern value="small|medium|large"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>
"""

json_structure_rules_header = """
# Invoice_number limited by REGEX pattern
"invoice_number": {
    "type": "string",
    "pattern": "^INV-[0-9]{1,10}$"
}

# Total_sum never can be 0 
"total_sum": {
    "type": "number",
    "minimum": 0.01,
    "multipleOf": 0.01,
    "default": 0.01
}

# Currency has list of values to which it is limited
# It reflects the exact options which can be selected via UI
"currency": {
    "type": "string",
    "enum": [
        "euro",
        "US dollar",
        "Kč"
    ]
}
"""
json_structure_rules_detail = """
# Category has list of values to which it is limited
# It reflects the exact options which can be selected via UI
"category": {
    "type": "string",
    "enum": [
        "PC",
        "TV",
        "Gaming",
        "Mobile phones",
        "Tablets",
        "Major Appliances",
        "Households"
    ]
}

# Service also limited to values Y|N, default N
# Dependent on if extra service was selected or not
"service": {
    "type": "string",
    "minLength": 1,
    "maxLength": 1,
    "enum": [
        "Y",
        "N"
    ],
    "default": "N"
}

# service_type has list of values to which it is limited
# It reflects the exact options which can be selected via UI
"service_type": {
    "type": "string",
    "enum": [
        "None",
        "extended warranty",
        "insurance"
    ],
    "default": "None"
}
"""
json_structure_rules_transportation = """
# Transporter has list of values to which it is limited
# It reflects the exact options which can be selected via UI
"transporter": {
    "type": "string",
    "enum": [
        "DHL",
        "Fedex"
    ]
}

# Country also limited to values Czech Republic|Slovakia
# It reflects the exact options which can be selected via UI
"country": {
    "type": "string",
    "enum": [
        "Czech Republic",
        "Slovakia"
    ]
}

# Size has list of values to which it is limited
# It reflects the exact options which can be selected via UI
"size": {
    "type": "string",
    "enum": [
        "small",
        "medium",
        "large"
    ]
},
"""