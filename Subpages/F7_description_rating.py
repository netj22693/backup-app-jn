import streamlit as st

st.write("# Rating")
''
''
st.write("""
- Every offer which is in state **Delivered** can be rated
- The rating is possible till **14 days** since the calculated delivery
""")

''
''

st.write("##### Rating process based on offer states")
''
st.write("""
- When **new offer** is created using **F7**, a new row is also created in **offer_rating** table in DB.
- When the specific offer is supposed to be **displayed** as part of **F7B UI**, the F7B already works with this **rating information from DB**, the same as with the **state** in which the offer at the moment is.
- The combination of **offer state**, if the **rating was given (True/False)** and **time (actuall and precalculated)**, gives the **logic of what should be displayed to the user**. If the user should see, rating which was already given, form to be able to give the rating or any of the few info notes.
- In case of **concurrent users** giving the rating to the same offer at the same time, there is also **logic preventing from overwriting**.
""")
''
''
st.image("Pictures/Function_7/F7_rating/F7_rating_BPMN_logic_v3.svg")

''
''
st.image("Pictures/Function_7/F7_rating/F7_rating_DB_context_v1.svg")

''
''
''
''
st.write("##### Principle:")
''
st.write("""
- The process workflow describing the logic
- The **make_rating_validation()** is the **core rating function** using the **BPMN** logic
""")

''
''
st.image("Pictures/Function_7/F7_rating/F7_rating_principle_v1.svg")






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
	page="Subpages/F7_description_state.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/west:",
	) 