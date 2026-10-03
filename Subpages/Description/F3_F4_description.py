import streamlit as st
from Subpages.Resources import Assets

st.write("# Description - Functions 3 & 4")
''
''
st.write("""
- **Function 3**: Creation of invoice based on user inputs (CSV, JSON or XML)
- **Function 3B**: Visibility of already created invoices & Analytics
- **Function 4**: Data Transfer of the invoice ; to CSV, JSON or XML
"""
)

''
with st.expander("Video guide", icon= ":material/youtube_activity:"):
    try:
        st.video("Video/F3_videoguide_v1.mp4")
    except:
        st.warning("Apologies, the video was not loaded.")

''
''
st.image("Pictures/Architecture/Detail/F3_F3B_F4_architecture_detail_for_function_v2.svg", width=500)


''
''
st.write("##### Business scenario:") 
st.write(
"Creation of invoice based on user input - CSV, JSON or XML. In case that user wants a different file format than was produced, there is an option of mapping/automatic file translation. The whole process is supported by DB -> invoices, history and analytics can be seen as well. "
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
6) The invoce, other invoices and analytics can be seen
"""
)

''
tab1, tab2 = st.tabs([
    "BPMN - Function 3",
    "BPMN - Function 4"
])


with tab1:
    ''
    st.write("""
    - Invoice creation
    """)
    ''
    st.image("Pictures/Function_3/F3_BPMN_process_v7.svg")
    ''
    ''
    st.image("Pictures/Function_3/F3_BPMN_calculation_process_v4.svg")
    ''
    ''

    st.write("""
    Costs:
    - Additional service - **Insurance** - **15% from product price**
    - Additional service - **Extended warranty** - **10% from product price**
    - Transport - depending on **Country, Transporting Company, Size of package**
    """)

    ''
    ''
    st.image("Pictures/Function_3/F3_Price_list.svg")
    ''
    ''

with tab2:
    ''
    st.write("""
    - Data Transformation using CDM
    """)
    ''
    ''
    ''
    st.image("Pictures/Function_3/F4_BPMN_process_v4.svg")
    ''
    ''
    ''
    ''
    ''
    ''



# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
    label = "Next page",
	page= Assets.Paths.Description.f3_f4_cdm,
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
    icon=":material/east:",
	) 