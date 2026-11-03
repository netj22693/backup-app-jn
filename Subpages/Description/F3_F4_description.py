import streamlit as st
from Subpages.Resources import Assets
from Subpages.Resources_ui_objects import render_next_page, render_specific_page
from Video.Display_video import display_video_expander

st.write("# Description - Functions 3 & 4")
''
''
st.write("""
- **Function 3**: Invoice creation based on user inputs (CSV, JSON or XML)
- **Function 3B**: Visibility of already created invoices & analytics
- **Function 4**: Data transformation to CSV, JSON or XML
"""
)

''
display_video_expander(Assets.Videos.LogicalDictionaries.f3_f4)

''
''
st.image("Pictures/Architecture/Detail/F3_F3B_F4_architecture_detail_for_function_v2.svg", width=500)


''
''
st.write("##### Business scenario:") 
st.write(
"Creation of invoice based on user input - CSV, JSON or XML. In case that user wants a different file format than was produced, there is an option of mapping/file transformation. The whole process is supported by DB -> invoices, history and analytics can be seen. "
)
''
''
st.write("##### Process:") 
st.write("""
1) User to insert inputs about an order/ a purchase
2) Application to calculate costs
3) User to select which file format the invoice should be produced in
4) Application to produce the invoice 
5) OPTIONAL: In case of need of different format -> mapping/transformation can be used
6) The invoce, other invoices and analytics can be seen
"""
)

''
tab1, tab2, tab3 = st.tabs([
    "BPMN - F3",
    "BPMN - F3B",
    "BPMN - F4"
])


with tab1:

    st.write("""
    - Invoice creation
    """)
    ''
    st.image("Pictures/Function_3/F3_BPMN_process_v8.svg")
    ''

    st.write("""
    Costs:
    - Additional service - **Insurance** - **15% from product price**
    - Additional service - **Extended warranty** - **10% from product price**
    - Transport - depending on **Country, Transporting Company, Size of package**
    """)

with tab2:
    st.write("""
    - Retrospective data visualization & analytics
    """)
    ''
    st.image("Pictures/Function_3/F3B_BPMN_process_v1.svg", width=520)
    ''
    ''

with tab3:

    st.write("""
    - Data Transformation using CDM
    """)
    ''
    ''
    st.image("Pictures/Function_3/F4_BPMN_process_v4.svg")
    ''
    ''
    ''
    ''
    ''
    ''
    ''

''
''
''
st.write("##### Process flow:") 


tab1, tab2, tab3 = st.tabs([
    "F3",
    "F3B",
    "F4"
])

with tab1:
    render_specific_page("code_architecture")
    st.image("Pictures/Function_3/F3_process_flow_v2.svg")

with tab2:
    render_specific_page("code_architecture") 
    st.image("Pictures/Function_3/F3B_process_flow_v2.svg")

with tab3:
    render_specific_page("code_architecture") 
    st.image("Pictures/Function_4/F4_process_flow_v2.svg")


# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

render_next_page(
    page= Assets.Paths.Description.f3_f4_cdm   
)