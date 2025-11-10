import streamlit as st


st.write("# BPMN diagrams:")
st.write("*For better visibility - put cursor on the picture and click on the icon in the right upper corner")


# Split into tabs
tab1, tab2 = st.tabs([
	"BPMN - Function 3 & DB ERD",
	"BPMN - Function 4"
])


#Tab 1
with tab1:
    st.write("#### Function 3 process flow:")
    ''
    ''
    # st.image("Pictures/Function_3/Function_3_BPMN process_5.png")
    st.image("Pictures/Function_3/Function_3_BPMN process_5.svg")
    ''
    '''
    - Inputs to be entered by **user** and submited:
    '''
    ''
    st.image("Pictures/Function_3/delivery details.png", width = 200)
    ''
    '''
    - Then application/function makes the calculation. 
    - In case of all inputs are okay, user can push download button for generating of an invoice either in XML format or JSON. 
    - In case that user wants to change something in the original inputs, he can rewrite/change the inputs and then push Submit button again...
    '''

    ''
    ''
    st.write("##### Application calculation process:")
    ''
    ''
    # st.image("Pictures/Function_3/Function_3_BPMN_calculation process_2.png")
    st.image("Pictures/Function_3/Function_3_BPMN_calculation process_3.svg")
    ''
    '''
    - If the BPMN diagram would be transferred into the "**application look**", then it would be like this:
    '''
    ''
    ''
    # st.image("Pictures/Function_3/Function_3_BPMN_calculation process_tables_2.png")
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
    st.image("Pictures/Function_3/Price_list.png")
    ''
    ''
    st.write("##### DB & ERD:")
    ''
    st.write("- This shows the **DB structure** to be able to maintain data and get **transport price** value **based on user inputs**")
    ''
    st.image("Pictures/Function_3/F3_ERD_transport_price.svg")
    ''

    currency = 'euro'
    c_code = 'cz'
    company = 'DHL'
    size = 'small'

    query = f"""
    SELECT {currency} 

    FROM f3.company a
        INNER JOIN f3.country_{c_code} b ON (a.comp_id = b.c_comp_id)
        INNER JOIN f3.parcel_size c ON (b.size = c.size_id)
        
    WHERE
        a.name = '{company}' AND
        c.name = '{size}'
    """

    st.write("- Dynamic SQL query:")
    st.code(query, language="sql")
    



#Tab 2
with tab2:
    st.write("#### Function 4 process flow:")
    ''
    ''
    '''
    - In case that user wants to change file format of invoice generated in Function 3 step, there is a possibility to use Function 4
    - Mapping into the other format than has been selected
    - Reason why to do this and not generate new one? The existing invoice file from the Function 3 has **uniquie ID and order number specific for the invoice** and thus this conversion into the other file format will keep these unique IDs.
    '''
    ''
    ''
    ''
    # st.image("Pictures/Function_4/Function_4_BPMN.png")
    st.image("Pictures/Function_4/Function_4_BPMN.svg")
    ''
    ''
    ''
    ''
    ''
    with st.expander(
        "Unique Order number and Invoice ID",
        icon= ":material/help_outline:"
        ):
        
        st.image("Pictures/Function_3/unique IDs_2.png")
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

