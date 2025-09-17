import streamlit as st


st.write("# Variables:")

''
st.write("""
        - **Mind map** of the Function 7 code
        - **Simplified overview** to help to understand the **dependencies/relationships in the code** -> which can be beneficial for new development and testing/troubleshooting
        - **Paradigm:** Procedural programming
        """)

st.image("Pictures/Function_7/F7_desc_function_diagram.svg")

''
st.write("""
        - **5 main segments**:
            - Data (split into multiple data sets)  
            - API (dynamic part which influences price)
            - User Input screen (what user sees and what he selects)
            - Processing after Submit button (creating of outputs)
            - User Output screen (visualization of results calculated by the app)
        """)

''
st.write("""
        - The **color-coding** visualizes what influences what -> gives a visibility which parts are impacted -> **helps to recognize the level of testing** which is needed
        """)


''
st.write("""
         - **High level processing**:
            1) API request (or cached data from the API) - actual exchange rate -> influences price
            2) Data from the data sets parsed and visualize on User Input screen 
            3) User can select accordingly their needs. The screen dynamically changes the options for user accordingly to choice (e.g. 'From' and 'To' cities selected -> app provides Transport options, currency, etc. accordigly to where the cities are located and what are the transport options defined in the dataset)
            4) Once the customer's needs reflected in the application -> Submit button can be used
            5) The app then calls relevant functions in the code to calculate and get results
            6) The app also gets actuall time & date CET/CEST to put the results into context of real time
            7) Visualization of the results on the User Output screen 
        """)



# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
	label = "Next page",
	page="Subpages/F7_description_dtd.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/east:"
	) 

st.page_link(
    label = "Previous page",
	page="Subpages/F7_description.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/west:",
	) 



