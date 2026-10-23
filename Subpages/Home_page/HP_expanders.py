import streamlit as st
from Subpages.Resources import Assets
from Subpages.Resources_ui import UiConfigAndIcons


def display_expander_overview_functions():

    with st.expander(
        "Overview of the Functions",
        icon= UiConfigAndIcons.Expanders.list
        ):
        st.write("""
            - **F1:** Download of few predefined XMLs for Function 2
            - **F2:** Data parsing from XML -> data visualization & analytics      
            """)
        ''
        st.write("""
            - **F3**: Creation of invoice based on user input (CSV, JSON or XML)
            - **F3B:** Invoice visibility & analytics
            - **F4**: Data transformation of the invoices created in F3, using **CDM** (:green[**my favorit piece of logic**])
            """)
        ''
        st.write("""
            - **F5:** Actual exchange rate & calculation (CZK, EUR, USD) - **API based**
            - **F5B:** Trend of exchange rate - **Background job based**, data continuously collected into DB and visualized via the Function UI
            """)
        ''
        st.write("""
            - **F6:** ZIP code - (1) Get ZIP codes based on City, (2) Get City based on ZIP code - **API based**
            """
            )
        ''
        st.write("""
            - **F7:** Transport calculation -> transport offer creation (:green[**my favorit Function**])
            - **F7B:** Offer visibility & analytics of transport offers created in F7
            """
            )
        ''
        st.write("""
            - **F8:** Visibility & analytics of transport companies registered in DB
            """
            )

def display_expander_github():
    with st.expander(
        "GitHub - Repository",
        icon=":material/deployed_code_history:"
        ):	
        st.write(f"- Link to [GitHub]({Assets.Links.External.git_hub}) repository")
        st.image("Pictures/Github_archimate_2.svg")


def display_expander_web_app():
    with st.expander(
        "Web app - Recommendation",
        icon=":material/computer:"
        ):	

        st.write("- The **primary** approach is through **web browser**")
        st.write('- :green[**To get the best experience, use the app on laptop or some bigger device**]')
        st.write("- On mobile phones layout of charts and image visibility might be slightly impacted due to screen size")


def display_expander_linkedin():
    with st.expander(
        "Contact - LinkedIn",
        icon=":material/id_card:"
        ):	
        
        st.image("Pictures/Logo/Logo_Linkedin.svg", width=90)
        st.write(f"- [Jan Netolicka]({Assets.Links.External.linked_in})")