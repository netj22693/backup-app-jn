import streamlit as st

st.write("# Functions 3 and 4")
''
''
st.write("""
    - **Function 3**: Creation of invoice based on user inputs (either XML or JSON)
    - **Function 4**: Mapping of the same invoice ; XML -> JSON or JSON -> XML
    """
    )
''
''
st.write("##### Business scenario:") 
st.write(
    "Simplified version of case when user is supposed to manually enter details about purchase/order and system to produce an invoice. There is a possibility to produce either XML or JSON - NOT both at the same time due to unique IDs (invoice ID and order ID) generated by the application. In case that user wants a different file format than was produced, there can be mapping/translation to different format used (Function 4)."
    )
''
''
st.write("##### Process:") 
st.write("""
    1) User to insert inputs about an order/ a purchase
    2) Application to calculate costs
    3) User to select which file format the invoice should have 
    4) Application to produce the invoice 
    5) OPTIONAL: In case of need of different format -> mapping/translation function can be used
    """
    )


# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
    label = "Next page",
	page="Subpages/F3_F4_description_BPMN.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/east:",
	) 
