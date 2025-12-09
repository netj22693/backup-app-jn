import streamlit as st
from Subpages.F3_F4_xml_json_structures import xml_as_string, xsd_as_string


# ================= Screen ================================

st.write("# XSD, XML Schema")
st.write('''
Description of XML structure/XML Schema with which these **Functions 3 and 4 work**. There is a **download button at the end of this page** to download XML Schema in both .txt and .xsd formats.
'''
)

st.write("----")
st.write("#### Diagram:")
''
'''
Basic principle: The XML is split into 3 main segments - header, detail and transportation. 
'''
''    
st.image("Pictures/Function_3/XSD main elements.png")
''
''  
''

# Split into tabs 1
tab1, tab2, tab3 = st.tabs([
      "Header",
      "Detail",
      "Transportation"
])

# Note(!): I am keeping 2 tabs nesting. If 1 tab only it doesn't function properly
with tab1:
        st.write("###### Header:")
        ''
        '''
        Header element includes nested elements providing key information/summary about an order which is created through the Function 3 in this app. 
        '''
        '' 
        st.image("Pictures/Function_3/XSD header.png")
        ''
        ''  
        st.image("Pictures/Function_3/F3_xsd_header.png")
        ''
        ''  
        ''

with tab2: 
        st.write("###### Detail:")
        ''
        '''
        Detail element includes also nested elements. They are used for information about the product which was purchased and whether any additional service for the product was bought or not (Insurance, Extended warranty).
        '''
        '' 
        st.image("Pictures/Function_3/XSD detail.png")
        ''
        ''  
        st.image("Pictures/Function_3/F3_xsd_detail.png")
        ''
        ''  
        ''

with tab3:
        st.write("###### Transportation:")
        ''
        '''
        Transportation is a different element for this Function 3 (in comparison with Function 1 and 2 in this app). Including few nested elements which keep data about transportation and delivery. 
        '''
        '' 
        st.image("Pictures/Function_3/XSD transportation.png")
        ''
        ''  
        st.image("Pictures/Function_3/F3_xsd_transportation.png")
        ''
        ''

with st.expander("Show XSD structure - code", icon= ":material/code:"):
	st.code(xsd_as_string, language= 'xml', line_numbers=True, height=700)



st.write("-----")
st.write("#### Message definition overview:")
''
''
st.image("Pictures/Function_3/F3_XML_layout_table.png")


st.write("----")

st.write("#### Principle of the XML in context of the Function 3:")
''
'''
In the application user provides key inputs about the product through input fields. Based on the inputs the Function 3 calculates and provides the remaining details (about your order). Then XML with data is produced.  
'''
'' 
''
''
# st.image("Pictures/Function_3/XML produced.png")
st.image("Pictures/Function_3/F3_XML_produced_v2.png")
'' 
''
'''
Some of the fields/options are predefined and then the application makes the calculation based on what you select from drop down lists. More can be seen when you use the Function 3 itself.
'''
'' 
''
st.image("Pictures/Function_3/delivery details.png", width = 200)
'' 
''
'''
Also, the predefined options in drop-down lists are set as xs:restriction in the XSD -> just these values are allowed for the XML.
'''
'' 
''
st.image("Pictures/Function_3/XSD dropdowns.png")




''
''
''
''
with st.expander("Show XSD structure - code", icon= ":material/code:"):
	st.code(xsd_as_string, language= 'xml', line_numbers=True, height=700)
      
with st.expander("Show XML structure - code", icon= ":material/code:"):
	st.code(xml_as_string, language= 'xml', line_numbers=True, height=700)

st.write("----") 

# Download of XSD

st.write("#### Download of the XSD for Functions 3 and 4:")
''
''

st.write("- Format .xsd")
if st.download_button(
            "Download",
            data = xsd_as_string,
            file_name="XML Schema for functions 3 and 4.xsd",
            icon = ":material/download:"
            ):

            st.info("Download will happen in few seconds")

''
''
st.write("- Format .txt")  
if st.download_button("Download",
            data = xsd_as_string,
            file_name="XML Schema for functions 3 and 4.txt",
            icon = ":material/download:"
            ):
        
            st.info("Download will happen in few seconds")

# ===== Page navigation at the bottom ======
''
''
st.write("-------")

st.page_link(
    label = "Next page",
	page="Subpages/F3_F4_description_json.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/east:",
	) 

st.page_link(
	label = "Previous page",
	page="Subpages/F3_description_archimate.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/west:"
	) 


