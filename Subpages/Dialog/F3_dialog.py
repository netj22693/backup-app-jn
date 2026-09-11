import streamlit as st
from Subpages.Resources import Assets

# ================ DIALOGS - process complete or not complete  =================
def final_dialogs_goto():    
    ''
    st.write("**Go to:**")

    st.page_link(
        label = "Function 3B - Invoice visibility",
        page= Assets.Paths.Function.f3b,
        help="The button will redirect to the relevant page within this app.",
        use_container_width=True,
        icon=":material/play_circle:",
        )
    
    st.page_link(
        label = "Function 4 - Mapping",
        page= Assets.Paths.Function.f4,
        help="The button will redirect to the relevant page within this app.",
        use_container_width=True,
        icon=":material/play_circle:",
        )

    st.page_link(
        label = "Function 5 - Description - API",
        page= Assets.Paths.Description.f5,
        help="The button will redirect to the relevant page within this app.",
        use_container_width=True,
        icon=":material/code:",
        )
    
    st.page_link(
        label = "Home page",
        page= Assets.Paths.App.main_page,
        help="The button will redirect to the relevant page within this app.",
        use_container_width=True,
        icon=":material/home:",
        )

@st.dialog("Complete!")
def process_done(order_number):
    st.write(f"""
        - File was created and downloaded -> :green[**Complete**]
        - Order **{order_number}** was inserted into DB -> :green[**Complete**]
        """)
    ''
    final_dialogs_goto()


@st.dialog("Insert into DB failed") 
def insert_db_not_complete():
    st.write("""
        - File was created and downloaded -> :green[**Complete**]
        - But Order **was not** inserted into DB -> :red[**Technical issue**]
        """)
    ''
    final_dialogs_goto()