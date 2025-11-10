import streamlit as st

st.write("# UML diagrams:")


# Split into tabs
tab1, tab2 = st.tabs([
	"1 - Use Case diagram",
	"2 - Activity diagram"
])

#Tab 1 
with tab1:
    st.write("#### UML Use Case diagram:")
    ''
    ''
    st.write("###### Function 3: ")
    ''
    st.image("Pictures/Function_3/F3_UML_UseCase.svg")
    ''
    ''
    ''
    st.write("###### Function 4: ")
    ''
    st.image("Pictures/Function_4/F4_UML_UseCase.svg")

with tab2:
    st.write("#### UML Activity diagram:")
    ''
    ''
    st.write("""
    - Related to the **Function 3** - Creation of XML or JSON
    - This Activity diagram describes the process of what **specifically user needs to do**
    - The **application does just 2 steps** here 
        - Validation - if user provided all inputs 
        - Producing XML or JSON - based on user's choice
    """)
    st.write("""    - To avoid failures **the validation process** is put into **"try and except"** python conditions:
        - If an issue with the inputs (some data were not provided by user -> except -> displaying info note)
        - If all good -> try -> the program continues with the next steps""")
    ''
    ''
    # st.image("Pictures/Function_3/F3_UML_ Activity diagram_extended.svg")
    st.image("Pictures/Function_3/F3_UML_ Activity diagram_extended_2.svg")
    ''
    with st.expander(
        "Application context",
        icon= ":material/help_outline:"
        ):
        
        ''
        ''
        st.write("- Filling data:")
        ''
        # st.image("Pictures/Function_3/F3_UML - context act diagram.PNG")
        st.image("Pictures/Function_3/F3_UML - context act diagram.svg", width=500)
        ''
        ''
        st.write(" - Submit button - inputs validation:")
        ''
        # st.image("Pictures/Function_3/F3 - UML - Activity diagram_note.png")
        st.image("Pictures/Function_3/F3 - UML - Activity diagram_note.svg", width=500)
        ''
        ''
        st.write("- Invoice creation:")
        ''
        # st.image("Pictures/Function_3/F3_UML - context act diagram_2.PNG")
        st.image("Pictures/Function_3/F3_UML - context act diagram_2.svg", width=500)
        ''
        ''

        st.page_link(
        label = "Go to: Function 3",
        page="Subpages/F3_FUNCTION_creation_of_XML.py",
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
	page="Subpages/F3_description_archimate.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/east:",
	) 

st.page_link(
	label = "Previous page",
	page="Subpages/F3_F4_description_BPMN.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/west:"
	) 