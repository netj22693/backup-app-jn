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
''
''
st.write("##### DB structure - ERD:")
''
st.write("""
- The DB is designed based on **principle of 2 kinds of tables**
- Table 1 **'company'** stores information about companies providing transport - and what type of transport does - **Truck, Train, Airplane, International/Domestic transport** 
- Table 2 **'country_XX**' stores information about branches/contact points of the companies per specific country
- This creates a relationship **1 Parent - multiple Children** having **'1 to Many Optional'** relations also when it comes to records
""")
''
st.image("Pictures/Function_8/F8_ERD.svg")

''
st.write("""
- When a **new company onboarded**, it gets created in the **'company'** table and **PostgreSQL will generate 'comp_id'** which is **PK** and **unique identifier** for the company/record in the DB
- Then **branches of the company** can be added to **'country_XX'** table(s), depending in which of the countries there are any of them
	- **'c_comp_id'** - is **FK** and it is the id of the company as was given in 'company' table
	- when new record added, **PostgreSQL will provide next available 'branch_id' to the record**. The benefit of PostgreSQL here - it takes the last number checking all **'country_XX'** tables -> there is not possible to have two times the same 'branch_id' -> **a record gets unique identifier always** across **all** the tables
""")
''
''
st.image("Pictures/Function_8/F8_erd_small.svg")


''
st.write("""
- With this DB logic there can be SQL queries set in the code to provide relevant data to the user screen
""")

''
st.write("""
- User is searching for companies available for particular type of transport (Truck, Train, Airplane) and Internation/Domestic transport
""")

''
st.image("Pictures/Function_8/F8_bpmn_query_internal_crossborder.svg")


''
st.write("""
- User is for particular company branches 
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