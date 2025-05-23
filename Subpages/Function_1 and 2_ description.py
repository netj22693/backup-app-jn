import streamlit as st

st.write("# Functions 1 and 2")
st.write(
    "Purpose of these functions is to parse data from XML -> validate them -> visualize them -> and produce simple .txt sumary."
    )

st.write("""
    - **Function 1**: Download XML file
    - **Function 2**: Parse data from the XML
    """
    )

st.write(" ")

st.write("##### Business scenario:") 
st.write(
    "Simplified version of case when a company does a purchase from other company/e-shop on frequent bases. That is why there is XML invoice defined for invoicing. This parsing function could be seen like very small ERP system/ERP program :)."
    )

st.write(" ")

st.write("##### Process:") 
st.write("""
    1) Dowload XML (keep existing or you can update it) 
    2) Upload XML
    3) And see what happens... :)
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
	page="Subpages/application_description_BPMN.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/east:",
	) 

