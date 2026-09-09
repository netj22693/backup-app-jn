import streamlit as st
from Subpages.Resources import Assets

st.write("# Description - Functions 3 & 4")
''
''
st.write("""
- **Function 3**: Creation of invoice based on user inputs (either XML or JSON)
- **Function 3B**: Visibility of already created invoices 
- **Function 4**: Mapping of the same invoice ; XML -> JSON or JSON -> XML
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
st.write("##### Business scenario:") 
st.write(
"Creation of invoice based on user input, either XML or JSON. In case that user wants a different file format than was produced, there is an option of mapping/automatic file translation. The whole process is supported by DB -> invoices, history and analytics can be seen as well. "
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
tab1, tab2, tab3 = st.tabs([
    "BPMN - Overview",
    "BPMN - Function 3",
    "BPMN - Function 4"
])


with tab1:
    ''
    st.write("""
    - Create invoice - **F3**
    - See invoice(s) & Analytics - **F3B**
    - Change file format of created invoice - **F4**
    """)

    ''
    ''    
    st.image("Pictures/Function_3/F3_F3B_F4_BPMN_navigation.svg")



with tab2:
    ''
    ''
    st.image("Pictures/Function_3/Function_3_BPMN process_6.svg")
    ''
    ''
    st.image("Pictures/Function_3/Function_3_BPMN_calculation process_3.svg")
    ''
    ''
    st.write("- Application context:")
    st.image("Pictures/Function_3/Function_3_BPMN_calculation process_tables_2.svg")
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

with tab3:
    ''
    st.write("""
    - Mapping XML <-> JSON
    - To keep the original data, specifically order number which is the invoice identifier
    """)
    ''
    ''
    ''
    st.image("Pictures/Function_4/Function_4_BPMN_v2.svg")
    ''
    ''
    with st.expander(
    "Unique Order number",
    icon= ":material/help_outline:"
    ):

        st.image("Pictures/Function_3/F3_unique_order_id.png")


''
''
''
''
st.write("##### Diagrams describing the functions:")

tab1, tab2, tab3, tab4 = st.tabs([
    "File builders",
    "UML - Use Case diagram",
    "UML - Activity diagram ",
    "ArchiMate"
])

with tab1:
    ''
    st.write("""
    - **Modularity** and logical code dependency of **core functions** in **F3** and **F4** -> **simplified view**
    - **Principle**: the F3 and F4 use/share the same core functions -> **working with/re-using the same data model**
    """)
    ''
    ''
    st.image("Pictures/Function_3/F3_F4_functions_file_builders_v1.svg")

with tab2:
    ''
    st.write("- Function 3: ")
    ''
    st.image("Pictures/Function_3/F3_UML_UseCase.svg")
    ''
    ''
    ''
    st.write("- Function 4: ")
    ''
    st.image("Pictures/Function_4/F4_UML_UseCase.svg")

with tab3:
    ''
    st.image("Pictures/Function_3/F3_UML_ Activity_diagram_v2.svg", width=660)

with tab4:
    ''
    st.image("Pictures/Function_3/F3_Archimate_diagram_v2.svg")


# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
    label = "Next page",
	page= Assets.Paths.Description.f3_f4_xml_json,
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
    icon=":material/east:",
	) 