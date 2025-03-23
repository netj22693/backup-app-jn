import streamlit as st

st.write("# Welcome!")
''
st.write(
    "Purpose of this application is to play with XML data. It offers **4 functions**:"
    )
''
st.write("""
    - **Function 1:** Download of few predefined types of XML for Function 2
    - **Function 2:** Parsing of data from XML -> their visualization -> producing of simple .txt file as summary      
    """)
''
st.write("""
    - **Function 3:** Creation of XML (slightly different one than used in F1 and F2) or JSON through the application screen (manual inputs)
    - **Function 4:** Mapping/change of file format XML -> JSON or JSON -> XML 
    """)
''
''
"More details about the functions can be seen in the subpages - what the functions do, what data structures are used, etc."

st.write("enjoy... :)") 

''
''
st.image(
    "Pictures/ArchM Functions overview_3.drawio.png.drawio.png",
    caption= "ArchiMate - Overview of functions"
    )