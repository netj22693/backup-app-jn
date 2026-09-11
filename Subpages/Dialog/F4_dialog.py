import streamlit as st
from Subpages.Resources import Assets

# ===== Dialogs =====
def final_dialogs_goto():
    ''
    st.write("**Go to:**")

    st.page_link(
    label = "Function F3B - Invoice visibility",
    page= Assets.Paths.Function.f3b,
    help="The button will redirect to the relevant page within this app.",
    use_container_width=True,
    icon=":material/play_circle:",
    )

    st.page_link(
    label = "Function F5 - Description",
    page= Assets.Paths.Description.f5,
    help="The button will redirect to the relevant page within this app.",
    use_container_width=True,
    icon=":material/code:",
    )

    st.page_link(
    label = "Function F5 - Exchange Rate",
    page= Assets.Paths.Function.f5,
    help="The button will redirect to the relevant page within this app.",
    use_container_width=True,
    icon=":material/play_circle:",
    )

    st.page_link(
    label = "Home page",
    page= Assets.Paths.App.main_page,
    help="The button will redirect to the relevant page within this app.",
    use_container_width=True,
    icon=":material/home:",
    )


# Final Dialog boxes
@st.dialog("Insert into DB failed") 
def insert_db_not_complete():
	st.write("""
		- Mapping complete -> :green[**Complete**]
		- But log about this change was not inserted into DB -> :red[**Technical issue**]
		""")
	
	final_dialogs_goto()


@st.dialog("Complete!")
def process_done():
	st.write(f"""
		- Mapping complete -> :green[**Complete**]
		- Log about this change was inserted into DB -> :green[**Complete**]
		""")
	
	final_dialogs_goto()


# Go to dialog
@st.dialog("Go to:")
def display_goto_links():

    ''
    st.page_link(
        label = "Function 5 - Description",
        page= Assets.Paths.Description.f5,
        help="The button will redirect to the relevant page within this app.",
        use_container_width=True,
        icon=":material/code:",
        )

    st.page_link(
        label = "Function 5",
        page= Assets.Paths.Function.f5,
        help="The button will redirect to the relevant page within this app.",
        use_container_width=True,
        icon=":material/play_circle:",
        )
    
    st.page_link(
        label = "Home page",
        page= Assets.Paths.App.main_page,
        help="The button will redirect to the relevant page within this app.",
        use_container_width=True,
        icon=":material/home:",
        )