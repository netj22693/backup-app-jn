import streamlit as st


# Predefined XML used as an example (can be downloaded also in Function_1)
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

# ========== DB and ERD description ===========================
st.write("# DB & ERD")
st.write("(!) Currently, this application is **NOT** connected to any DB. Maybe one day in the future :).")
st.write("This is for visibility how DB tables could look like.")

st.write("-----")
st.write("#### Entity Relationship Diagram:")
''
''
st.image("Pictures/Function_2/F2_2_DB ERD_3.PNG")
''
st.write("Joining using keys:")
st.code('''
SELECT *
FROM sum_inv
    INNER JOIN detail_inv ON (sinv_num = inv_num)
    INNER JOIN cust ON (c_id = cust_id)
''',
language="sql"
)
''
''
''
st.write("##### Description of the tables:")
''
st.write("1) Customer details - cust")
''
st.image("Pictures/Function_2/F2_cust.PNG")
''
st.write("""
- cust -> means customer
- Principle of this table is to maintain details about companies/customers with whom the XML comunication is established
- Data coming in XML is 'name' which is <customer> XML element
- The rest is purelly DB information providing details about the customer
- Can be companies or enterpreneurs (name and surname)
""")
''
st.image("Pictures/Function_2/F2_DB_screen_cust.PNG")
''
with st.expander(
	"Detailed description",
	icon= ":material/help_outline:"
	):
    
    st.write("""
    **c_id** 
    - customer id  - internal company id    
    - is **Primary Key** for this table
    - And the type of the key is Surrogate key as it system-generated identifier for a database object, not derived from the data itself
    - **INTEGER** - limited to 7 characters - each customer will get unique id.
    - Example: 14, 100, 333, 1892030
    - **Type**: system-generated identifier
    """
    )
    ''
    ''
    st.write("""
    **name**
    - Customer/Company name
    - **VARCHAR** - due to possibility of '.-_,&', numbers and letters
    - limited to 100 characters
    - example: ABC & Partners s.r.o, Jan Novak
    - **Type**: DB information about a customer - not comming in the data/XML
    """
    )
    ''
    ''
    st.write("""       
    **city**
    - Customer/Company name
    - **TEXT** - limited to 50 characters
    - example: Prague, Berlin, London
    - **Type**: DB information about a customer - not comming in the data/XML
    """
    )
    ''
    ''
    st.write("""     
    **street**
    - Street name, including number
    - **VARCHAR** - limited to 70 characters
    - Example: Narodni trida 25
    - **Type**: DB information about a customer - not comming in the data/XML
    """
    )
    ''
    ''
    st.write("""     
    **state**
    - Name of state where customer is based
    - **TEXT** - limited to 30 characters
    - Example: Czech republic, Germany, Austria
    - **Type**: DB information about a customer - not comming in the data/XML
    """
    )
    ''
    ''
    st.write("""        
    **phone**
    - Phone number including country preffix
    - **VARCHAR** - limited to 20 characters - can include '+_-'
    - Example: +420123456
    - **Type**: DB information about a customer - not comming in the data/XML
    """
    )
    ''
    ''
    st.write("""       
    **vip**
    - Means special customer
    - **BOOLEAN** 
    - Example: TRUE, FALSE
    - **Type**: DB information about a customer - not comming in the data/XML       
    """
    )
''
''
st.write("2) Invoice summary - sum_inv")
''
st.image("Pictures/Function_2/F2_sum.PNG")
''
st.write("""
- This table reflects data coming in XML header
- sum_inv -> summary of an invoice
"""
)
''
st.image("Pictures/Function_2/F2_DB_screen_sum_inv.PNG")
''
with st.expander(
	"Detailed description",
	icon= ":material/help_outline:"
	):

    st.write("""       
        **sinv_num**
        - Invoice number - 's' used for making the column name unique 
        - **Primary Key** for this table
        - **VARCHAR** - due to invoice ID format 'INV-123456' 
        - **Type**: parsed from XML     
        """
        )
    ''
    ''
    st.write("""       
        **cust_id**
        - Customer id  - internal company id    
        - **INTEGER** - limited to 7 characters - each customer will get unique id. Example: 0000014   
        - is **Foreign Key** for this table  - relation ship with Primary key in 'cust' table
        - **Type**: system-generated identifier 
        """
        )
    st.code('''
    SELECT *
    FROM sum_inv INNER JOIN cust ON (cust_id = c_id)
    ''', language="sql")

    st.image("Pictures/Function_2/F2_DB_sum_inv join cust.png")
    ''
    ''
    st.write("""       
        **date**
        - Date    
        - **DATE** - format YYYY-MM-DD   
        - Example: 2025-05-19
        - **Type**: parsed from XML
        """
        )
    ''
    ''
    st.write("""       
        **ttl_sum**
        - Total sumary of price from all products in XML message  
        - **FLOAT** - defined in XML 2 decimals  
        - Example: 3291.00
        - **Type**: parsed from XML
        """
        )
    ''
    ''
    st.write("""       
        **ttl_sum_serv**
        - Total sumary of price from all products in XML message, If any extra service purchased 
        - **FLOAT** - defined in XML 2 decimals  
        - Example: 168.00
        - **Type**: parsed from XML
        """
        )
    ''
    ''
    st.write("""       
        **cur**
        - Currency - used in the XML
        - **TEXT**
        - XML/XSD is defined to have euro|US dollar|Kč -> in DB euro, koruna, us dollar
        - **Type**: parsed from XML. But characters lowered and Kč insert to DB as 'koruna'
        """
        )
    ''
    st.code('''
	<xs:pattern value="euro|US dollar|Kč"/>
    ''',
    language="xml"
    )
    
    ''
    st.image("Pictures/Function_2/F2_DB_curency small.PNG")
''
''
st.write("3) Invoice detail - detail_inv")
''
st.image("Pictures/Function_2/F2_detail.PNG")
''
st.write("""
- This table reflects data coming in XML detail
- Stores data about the purchased items
- detail_inv -> details of products/items in an invoice
"""
)
''
st.image("Pictures/Function_2/F2_DB_screen_detail_inv.PNG")
''
with st.expander(
	"Detailed description",
	icon= ":material/help_outline:"
	):

    st.write("""       
        **inv_num**
        - Invoice number
        - **VARCHAR** - due to invoice ID format 'INV-123456'      
        - **Foreign Key** for this table to - relation ship with Primary key in sum_inv table
        - **Type**: parsed from XML
        """
        )
    st.code('''
    SELECT *
    FROM sum_inv INNER JOIN detail_inv ON (sinv_id = inv_num)
    ''', language="sql")
    st.image("Pictures/Function_2/F2_DB_sum_inv join detail_inv.png")
    ''
    ''
    st.write("""       
        **product**
        - Product name
        - **VARCHAR** - can include also numbers and special characters      
        - Example: Playstation 5 Pro
        - **Type**: parsed from XML
        """
    )
    ''
    ''
    st.write("""       
    **category**
    - Product category
    - **TEXT** - it is defined in XML/XSD as PC|TV|Gaming|Mobile phones|Tablets|Major Appliances|Households
    - In DB: pc, tv, gaming, mobile phones, tablets, major appliances,households
    - **Type**: parsed from XML. But characters lowered  
    """
    )
    ''
    st.code('''
	<xs:pattern value="PC|TV|Gaming|Mobile phones|Tablets|Major Appliances|Households"/>
    ''',
    language="xml"
    )
    
    ''
    st.image("Pictures/Function_2/F2_DB_category distinct.PNG")
    ''
    ''
    st.write("""       
    **s_type**
    - Special service type
    - **TEXT** - it is defined in XML/XSD as None|extended warranty|insurance
    - In DB: none, extended warranty, insurance   
    - **Type**: parsed from XML. But characters lowered. 
    """
    )
    ''
    st.code('''
	<xs:pattern value="None|extended warranty|insurance"/>
    ''',
    language="xml"
    )
    
    ''
    st.image("Pictures/Function_2/F2_DB_service type distinct.PNG")
    ''
    ''
    st.write("""       
    **s_price**
    - Special service type
    - **FLOAT** - price for extra service - 2 decimals 
    - Example: 9.00, 9.45 ; in case of 'none' no service then 0 in DB 
    - **Type**: parsed from XML
    """
    )
    ''
    ''
    st.write("""       
    **record_id**
    - Table specific id which makes a record unique -> to make it recognizable
    - Is **Primary Key** for this table
    - And the type of the key is **Surrogate key** as it system-generated identifier for a database object, not derived from the data itself
    - Having **Auto-increment** set
    - **BIGINT** - Unsigned range is from 0 to 18446744073709551615
    - Example: 1, 2, .... 39293990, ...
    - **Type**: system-generated identifier, in this case Auto-increment
    """
    )
''
''
''
st.write("##### More details about the cardinality:")
''
st.image("Pictures/Function_2/F2_DB_cardinality.PNG", width= 180)
''
with st.expander(
	"Detailed description - ERD cardinality",
	icon= ":material/help_outline:"
	):
    
    ''
    ''
    st.write("###### 1 - One (and only one) to 0..* Zero or many:")
    ''
    ''
    st.image("Pictures/Function_2/F2_2_DB ERD zero to many_2.PNG")
    ''
    st.write("""
    - Has been chosen based on a **business logic**. 
    
    - **1 - One (and only one)** - In the **'cust'** table there is expected to have all customers registered and each record is unique (one unique customer = one record in 'cust' table) -> that is why **1 and Only one** 
             
    - **0..*** **- Zero or many** - On the other side the table **'sum_inv'** works on principle giving a visibility of how many invoices each customer has. So there is expected to be **many** invoices per customer (the more business you do, the more invoices you should have in DB). And why **0 (Zero)**? Because there can be also registered customers but **NO** invoice received yet. 
    """
    )

    ''
    ''
    st.write("**Example**: How many invoices in 'sum_inv' table registered per customer -> Can be also 0 (Zero)")
    st.image("Pictures/Function_2/F2_2_DB registered customer with 0 invoices.PNG")
    ''
    st.code('''
    SELECT
        name,
        count(cust_id) as "How many invoices registered in 'sum_inv' table"
    
    FROM sum_inv
        RIGHT JOIN cust ON (cust_id = c_id)
    
    GROUP BY
        cust_id
            
    ORDER BY
        count(cust_id) ASC
    ''', language="sql")
    ''
    ''
    ''
    ''
    ''
    st.write("###### 1 - One (and only one) to 1..* One or many:")
    ''
    ''
    st.image("Pictures/Function_2/F2_2_DB ERD one to many.PNG")
    ''
    st.write("""
    - Has been chosen based on logix of the **XML**/XSD definition. 
             
    - **Below**, there is explained the relationship between the tables and XML. 
    
    - If it is simplified then:
        - **'sum_inv'** table coresponds to **XML <header>**
        - **'detail_inv'** coresponds to **XML <detail>**
        - The XML is defined as 1 (and only one) <header> and 1 or many <detail> lines 
        - *Anti-pattern (cannot happen): 0 <detail> line in the XML would mean no product/no transaction 
    """
    )
    ''
    st.image("Pictures/V2_pictures/Simple level.png")
    ''
    ''
    st.write("**Example**: How many <detail> lines/product were in one invoice. 1 to many.")
    st.image("Pictures/Function_2/F2_2_DB number of lines in invoices.PNG")
    ''
    st.code('''
    SELECT 
        sinv_num,
        count(inv_num) as 'Number of detail lines/products in invoice'
        
    FROM sum_inv
        INNER JOIN detail_inv ON (sinv_num = inv_num)
        
    GROUP BY
        sinv_num

    ORDER BY
        count(inv_num) DESC
    ''', language="sql")
''
''
st.write("-----")
st.write("#### The DB tables in context of the data parsing from XML")
''
''
st.write("""       
    - Visualization of relationship between DB tables and data in XML message
    """
)
''
''
st.image("Pictures/Function_2/F2_DB_XML.png")
''
''
st.write("Example:")

st.write("""
- INV-123456
"""
)

with st.expander(
    "Show XML structure - code",
    icon= ":material/code:"
    ):
    
        st.code(
        xml_data_euro,
        language= 'xml',
        line_numbers=True,
        height=700,
        )

''
''
st.write("Details about customer 'ABC s.r.o.'")
st.code('''
    SELECT *
    FROM cust
    WHERE name = 'ABC s.r.o.'
    ''', language="sql")
st.image("Pictures/Function_2/F2_SQL_name.PNG")
''
''
st.write("Info about invoice 'INV-123456' - header")
st.code('''
    SELECT *
    FROM sum_inv
    WHERE sinv_num = 'INV-123456'
    ''', language="sql")
st.image("Pictures/Function_2/F2_SQL_INV-123456.PNG")
''
''
st.write("Info about invoice 'INV-123456' - detail")
st.code('''
    SELECT *
    FROM detail_inv
    WHERE inv_num = 'INV-123456'
    ''', language="sql")
st.image("Pictures/Function_2/F2_SQL_INV-123456_detail.PNG")
''
''
st.write("Info about invoice 'INV-123456' - to show all items where additional service was bought -> what is the extra price for that and calculated value of total sum (price for the product + price for the service)")
st.code('''
SELECT 
	category,
	product, 
	price,
	s_type,
	s_price,
	(price + s_price) as 'Total for product',
	cur

FROM sum_inv 
	INNER JOIN detail_inv di  ON (sinv_num = inv_num) 

WHERE 
	sinv_num = 'INV-123456'
	AND 
	s_type IS NOT 'none'

ORDER BY
	category, product, s_type
    ''', language="sql")
st.image("Pictures/Function_2/F2_DB_SQL_2_result.PNG")
''
''
st.write("-----")
st.write("#### Example of possible Data Science")
''
''
st.write("Example:")

st.write("""
- Search for Invoices received in **January 2025**
- Where currency was '**koruna**' 
- Total sum of the prices in every invoice (Total sum price + Total sum services)
- Percentage **% ratio** - how much every invoice has from the **January revenue**
- **Result:** 3 invoices in January 2025 -> ratio: ~ 46.3%, 0.7%, 53%
"""
)

st.code('''
SELECT 
	sinv_num,
	date,
	ttl_sum + ttl_sum_serv as 'Total sum per invoice',
	cur,
	round(
        ((ttl_sum + ttl_sum_serv)
            /
	    (
		SELECT sum((ttl_sum + ttl_sum_serv))
			FROM sum_inv si
				WHERE 
					date LIKE '2025-01-%'
					AND 
					cur = 'koruna'
	    )
        *100), 3) as 'Percentage ratio % from January revenue'

FROM sum_inv si 
	WHERE 
		date LIKE '2025-01-%'
		AND 
		cur = 'koruna'
    ''',
    language="sql"
    )

st.image("Pictures/Function_2/F2_DB_data science_ revenue.PNG")


# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
    label = "Go to: Function 1",
	page="Subpages/XML_dowload.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/play_circle:",
	) 

st.page_link(
	label = "Previous page",
	page="Subpages/XML_XSD_schema.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/west:"
	) 