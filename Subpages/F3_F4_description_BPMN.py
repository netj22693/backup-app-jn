import streamlit as st


st.write("# BPMN diagrams:")


# Split into tabs
''
tab0, tab1, tab2 = st.tabs([
    "BPMN - Overview",
	"BPMN - Function 3",
	"BPMN - Function 4"
])

#Tab 0
with tab0:
    st.write("#### Overview:")
    ''
    st.write("""
    - **Simple overview of use-cases** and which **function to use**
        - Create invoice - F3
        - See invoice(s) - F3B
        - Change file format of created invoice - F4
    """)

    ''
    ''    
    st.image("Pictures/Function_3/F3_F3B_F4_BPMN_navigation.svg")


#Tab 1
with tab1:
    st.write("#### Function 3 process flow:")
    ''
    ''
    st.image("Pictures/Function_3/Function_3_BPMN process_6.svg")
    ''
    '''
    - Inputs to be entered by **user** and submited:
    '''
    ''
    st.image("Pictures/Function_3/delivery details.png", width = 200)
    ''
    '''
    - Then application/function makes the calculation. 
    - In case of all inputs are okay, user can push download button for generating of invoice either in XML or JSON format. 
    - In case that user wants to change something in the original inputs, he can rewrite/change the inputs and then push Submit button again...
    '''

    ''
    ''
    st.write("##### Application calculation process:")
    ''
    ''
    st.image("Pictures/Function_3/Function_3_BPMN_calculation process_3.svg")
    ''
    '''
    - If the BPMN diagram would be transferred into the "**application look**", then it would be like this:
    '''
    ''
    ''
    st.image("Pictures/Function_3/Function_3_BPMN_calculation process_tables_2.svg")
    ''
    ''
    ''
    '''
    The predefined values for calculations are:

    - Additional service/extra costs - **Insurance** - **15% from product price**
    - Additional service/extra costs - **Extended warranty** - **10% from product price**

    - And then **specific costs** for transport depending on **Country, Transporting Company, Size of package** - **stored in DB**
    '''
    ''
    st.image("Pictures/Function_3/F3_Price_list.svg")
    ''
    ''

#Tab 2
with tab2:
    st.write("#### Function 4 process flow:")
    ''
    '''
    - If user wants to **change a file format** of the invoice generated in F3, there is a possibility to **use F4**
    - Mapping into the other format than has been selected
    '''
    '''
    - **Reason** - Why to use F4 and not to generate new invoice:
        - When file produced in F3, the data/ivoice was stored in DB under **unique Order number** -> to keep it, mapping in F4
        - Information about the mapping will be put into DB as **a log record with timestamp** -> this record will be visible in F3B when search for the invoice
    '''
    ''
    ''
    ''
    st.image("Pictures/Function_4/Function_4_BPMN_v2.svg")
    ''
    ''
    ''
    ''
    ''
    with st.expander(
        "Unique Order number",
        icon= ":material/help_outline:"
        ):
        
        st.image("Pictures/Function_3/F3_unique_order_id.png")
        ''
        ''
        st.write("If needed to keep the IDs and change the file format, mapping XML <-> JSON:")

        st.page_link(
        label = "Go to: Function 4",
        page="Subpages/F4_FUNCTION_translation_mapping.py",
        help="The button will redirect to the relevant page within this app.",
        use_container_width=True,
        icon=":material/play_circle:",
        ) 

# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
    label = "Next page",
	page="Subpages/F3_description_UML.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/east:",
	) 

st.page_link(
	label = "Previous page",
	page="Subpages/F3_F4_description.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/west:"
	) 

