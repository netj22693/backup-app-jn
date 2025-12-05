import streamlit as st

# ==================== Application screen ==============
st.write("# Description - Function 8")
''
''
st.write("""
    - **Function 8:** Company Book - provides visibility of transport companies - **DB on cloud**
    """
    )

''
with st.expander("Video guide", icon= ":material/youtube_activity:"):
    try:
        st.video("Video/F8_videoguide_v1.mp4")
    except:
        st.warning("Apologies, the video was not loaded.")
''
''


st.write("##### Application environment:")
''
st.write("""
- **DB** is built and maintained on **cloud** provided by **Neon company**
- The **DB design** and **data** are **our own** - Neon provides just the infrastructure
- Application makes connection with the DB to get data based on request from user
- Used technology: **PostgreSQL**
""")

''
''
st.image("Pictures/Function_8/F8_Archimate.svg")

''
with st.expander("Known limitation - latency", icon=":material/sync_problem:"):
    
    st.write("""
- The **Function 8** can be quite slow, **5-10 seconds**, when loading data - reasons:
    - I use **FREE version** of the Neon DB and Streamlit
    - **Latency** - Neon DB server is in Frankfurt in **DE** and Streamlit in **USA**
    - The Fucntion 8 is built on **multiple queries pulling data** which needs to be performed. So the latency slows this down a little bit
	""")

''
''
''
st.write("##### DB structure - ERD:")
''
st.write("""
- The DB is designed based on **principle of 2 main kinds of tables** to cover the **core of data/information**
	- Table 1 **'company'** stores information about companies providing transport - and what type of transport does - **Truck, Train, Airplane, International/Domestic transport** 
	- Table 2 **'country_XX'** stores information about branches/contact points of the companies per specific country - **adresses** + **branch type code** 
	- This creates a relationship **1 Parent - multiple Children** having **'0 to Many'** relations also when it comes to records
""")
st.write("""
- Then there is **3rd** table '**branch**' which is linked to the **branch type code** in 'country_XX' tables
	- This branch type code is very important for SQL filtering when it comes to Truck, Train, Airplane critria 
    - And also through SQL JOIN helps to provide text information in dataframes visualized on user screens
    - The branch type code, its text and description can be maintained in this 'branch' table
""")
''
st.image("Pictures/Function_8/F8_ERD_v2.svg")

''
st.write("""
- When a **new company onboarded**, it gets created in the **'company'** table and **PostgreSQL will generate 'comp_id'** which is **PK** and **unique identifier** for the company/record in the DB
- Then **branches of the company** can be added to **'country_XX'** table(s), depending in which of the countries there are any of them
	- **'c_comp_id'** - is **FK** and it is the id of the company as was given in 'company' table
	- when new record added, **PostgreSQL will provide next available 'branch_id' to the record**. The benefit of PostgreSQL here - it takes the last number checking all **'country_XX'** tables -> there is not possible to have two times the same 'branch_id' -> **a record gets unique identifier always** across **all** the tables
""")
''
''
st.image("Pictures/Function_8/F8_erd_small_v3.svg")

''
''
st.write("- Example of data:")
st.image("Pictures/Function_8/F8_erd_table_relations_example.svg")

''
''
''
st.write("##### Logic - SQL query:")
''
''
st.write("""
- Based on the DB logic there can be SQL queries set in the code to provide relevant data to the user screen
""")

''
st.write("""
- User is searching for companies available for particular type of transport (Truck, Train, Airplane) and Internation/Domestic transport
""")

''
st.image("Pictures/Function_8/F8_bpmn_query_internal_crossborder.svg")


''
st.write("""
- User is searching for particular company branches 
""")

''
st.image("Pictures/Function_8/F8_bpmn_query_branches.svg")


# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
	label = "Function 8",
	page="Subpages/F8_FUNCTION_company_book.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/play_circle:"
	) 