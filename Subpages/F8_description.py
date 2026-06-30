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
        st.info("This video is not up to date with the actual F8 features -> will be updated")
    except:
        st.warning("Apologies, the video was not loaded.")
''
''


st.write("##### Application environment:")
''
st.write("""
- The **DB** is built and maintained on **cloud** provided by **Neon company**
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
''
st.write("##### DB structure - ERD:")
''
st.write("""
- The DB is designed based on **2 operational** tables and **multiple lookup** tables
- In the ERD there are highlithed mandatory fields for the F8 tu function properly as **'NOT NULL'**
- When **new either company or branch** is inserted, **DB prevents** from saving without mandatory fields -> **F8 will have all the inputs to function properly** (Displaying of data & MAP)
""")
''
''
st.image("Pictures/Function_8/F8_ERD_v4.svg")

''
''
''
''
''
st.write("##### Business logic:")
''
st.write("**TAB 1** - Transport - Simple view of **principle how companies are selected**")
''
''
st.image("Pictures/Function_8/F8_BPMN_query_internal_domestic.svg")

''
''
''
st.write("**TAB 2** - Company - Simple view of **principle how branches are displayed** based on selected company")
''
''
st.image("Pictures/Function_8/F8_BPMN_query_company_info.svg")



# # ===== Page navigation at the bottom ======
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