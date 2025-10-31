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

st.info("This section is still under build - This is just basic view - more will be provided soon :)")

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
- Table 1 **'company'** stores information about companies providing transport - and what type of transport
- Table 2 **'country_XX**' stores information about branches/contact points of the companies per specific country
- This creates a relationship **1 Parent - multiple Children** having **'1 to Many'** relations also when it comes to records
""")
''
st.image("Pictures/Function_8/F8_ERD.svg")



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