import streamlit as st

# ==================== Application screen ==============
st.write("# Description - Function 8")
''
''
st.write("""
    - **Function 8:** Company Book - provides visibility of transporting companies **DB on cloud**
    """
    )
''
''

st.info("This section si being prepared - will be available soon")


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