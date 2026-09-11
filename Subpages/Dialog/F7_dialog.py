import streamlit as st
from Subpages.Resources import Assets

def final_dialogs_goto():
    ''
    st.write("**Go to:**")

    st.page_link(
    label = "Function F7B - Offer visibility",
    page= Assets.Paths.Function.f7b,
    help="The button will redirect to the relevant page within this app.",
    use_container_width=True,
    icon=":material/play_circle:",
    )

    st.page_link(
    label = "Function F8 - Description",
    page= Assets.Paths.Description.f8,
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
def process_done(offer_number_input):
    st.write(f"""
        - PDF offer was generated -> :green[**Complete**]
        - The offer **{offer_number_input}** was inserted into DB -> :green[**Complete**]
        """)
    ''
    final_dialogs_goto()


@st.dialog("Insert into DB failed") 
def insert_db_not_complete():
    st.write("""
        - PDF offer was generated -> :green[**Complete**]
        - But the offer **was not** inserted into DB -> :red[**Technical issue**]
        """)
    ''
    final_dialogs_goto()