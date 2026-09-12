import streamlit as st
from Subpages.Resources import Assets
from Subpages.Expander.F1_expanders import display_expander_pair_xml_xsd
from Subpages.Data.F1_F2_xml_structures import xml_data_euro, xml_data_koruna, xml_data_usdollar, xml_empty_template


# ======================== Screen part ==================================

st.write("# XML download")
''
''
st.write(
'''
- Here you can **download XMLs** which can be used for parsing in **Function 2**:

    1) Predefind file - **sum matches** - **euro - €** - 15 detail lines
    2) Predefind file - **sum matches** - **koruna - Kč** - 12 detail lines
    3) Predefind file - sum does **not** match - **US dollar - $** - 15 detail lines
    4) XML Template
'''
)
''
st.write("""
- The XMLs **can be customized**
- The XMLs are limited to **30 detail lines** (Set as XSD rule)
- The customization needs to **fit into predefined XML Schema/XSD rules**
""")

''
''
''
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Euro",
	"2. Koruna",
	"3. US dollar",
	"4. XML Template"
])

# Option 1
with tab1:
    ''
    st.write("""
    - Currency: **euro - €**
    - Lines in detail segment: **15**
    - <total_sum> value **matches** sum of <price_amount> values in detail segment
    - <total_sum_services> **matches** sum of <service_price> in detail segment
    """)

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



# Option 2
with tab2:
    ''
    st.write("""
    - Currency: **Koruna - Kč**
    - Lines in detail segment: **12**
    - <total_sum> value **matches** sum of <price_amount> values in detail segment
    - <total_sum_services> **matches** sum of <service_price> in detail segment
    """)

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


# Option 3
with tab3:
    ''
    st.write("""
    - Currency: **US dollar - $**
    - Lines in detail segment: **15**
    - <total_sum> value does **NOT** match sum of <price_amount> values in detail segment
    - <total_sum_services> does **NOT** match sum of <service_price> in detail segment
    """)

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



# Option 4
with tab4:
    ''
    st.write("""
    - Empty template
    - Lines in detail segment: **12** 
    - Data to be fulfilled manually
    """)

    '''
    - **(!) It is recommended: Once the XML is fullfiled, pair it and validate it against XSD. It will help to make sure that the XML will be processed throught the application and will not fail due to data quality issue**
    '''
    '''
    - *XSD - can be downloaded from the page Functions 1 and 2 "Description - XSD, XML Schema"*
    '''
    ''
    display_expander_pair_xml_xsd()

        

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
	page= Assets.Paths.Function.f2,
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
    icon=":material/play_circle:",
	) 

st.page_link(
	label = "Previous page",
	page= Assets.Paths.Description.f1_f2_xml_xsd,
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
	icon=":material/west:"
	) 

