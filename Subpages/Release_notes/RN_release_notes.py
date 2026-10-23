import streamlit as st
from Subpages.Resources_ui import UiConfigAndIcons

def display_release_notes_expander_app_specific():
    with st.expander(
        "Release notes - App specific changes",
        icon= UiConfigAndIcons.Pages.release_notes["icon"]
        ):	

       st.write("""
        - **v71.4** - Unification of info/fallback notifications by wrappers implemented across Functions - 21-Oct-2026
        - **v71.0** - Centralized UI components and introduced reusable rendering wrappers - 16-Oct-2026        
        - **v70.9** - Created a modular function with extended logic for video selection, rendering and display - 13-Oct-2026
        - **v69.9** - Unified logging - 14-Sep-2026
        - **v69.0** - Centralized API handling - build as separate module - 03-Sep-2026
        - **v68.7** - Centralized DB connection handling - build as separate module - 02-Sep-2026
        """)

def display_release_notes_expander_va():
    with st.expander(
        "Release notes - Virtual Assistant (Chatbot)",
        icon= ":material/event_note:"
        ):	

       st.write("""
        - **v68.7** - Centralized DB connection handling & Adjustment of fallback logic if DB not connected - 02-Sep-2026
        - **v61.2** - Thumbs up/down rating added + connected to DB to store the rating - 11-May-2026
        - **v60.5** - Extended: by more questions to App - 04-May-2026
        - **v60.4** - Extended: by more questions to the Chatbot & App - 30-Apr-2026
        - **v60.3** - Extended: questions related to the Chatbot, XML, XSD, JSON - 28-Apr-2026
        - **v60.2** - VA pilot released - 27-Apr-2026
        """)


def display_release_notes_expander_f1_f2():
    with st.expander(
        "Release notes - F1 & F2",
        icon= UiConfigAndIcons.Pages.release_notes["icon"]
        ):	

        st.write("""
        - F1:
            - **v67.8** - XML Schema/XSD validation - limited to 30 detail lines - 13-Aug-2026
            - **v67.7** - UI layout change - 13-Aug-2026
            - **v52.3** - Function description extended by Video Guide - 03-Dec-2025
            - **v0.1** - F1 released (together with F2) - 20-Feb-2025
        """)
        st.write("")
        st.write("""
        - F2:
            - **v67.8** - XML Schema/XSD validation - limited to 30 detail lines - 13-Aug-2026
            - **v64.8** - Widgets/filters - logic rebuilt to be more dynamic - 05-July-2026
            - **v64.7** - Major code refactoring & clean up - 03-July-2026
            - **v52.3** - Function description extended by Video Guide - 03-Dec-2025
            - **v35.4** - Plotly() arguments adjusted, deprication will happen end of 2025  - 20-Oct-2025
            - **v16.4** - Better visualization in dataframes - 2 decimals always - 22-July-2025
            - **v16.2** - New expander (SQL 4 - average values) - 22-July-2025
            - **v15.0** - Input XML validated against XSD (new feature built) - 11-July-2025
            - **v14.0** - New expander (SQL 3) - another SQL queries & Pie charts - 10-July-2025
            - **v8.1** - More filters/Advanced filtering - 23-Jun-2025		
            - **v5.2** - Try/Except - Error handling, if wrong file uploaded - 17-Jun-2025		  
            - **v5.0** - New expanders with SQL queries (Data highlights) - 16-Jun-2025
            - **v0.1** - F2 released (together with F1) - 20-Feb-2025
        """)

def display_release_notes_expander_f3_f4():
    with st.expander(
        "Release notes - F3, F3B & F4",
        icon= UiConfigAndIcons.Pages.release_notes["icon"]
        ):	
       
        st.write("""
        - F3 & F3B:
            - **v70.8** - F3 - Caching of data loaded from DB -> increased speed of processing - 09-Oct-2026
            - **v70.7** - F3 - Logic of warning of unusual user inputs in context of selected category added & Extension of user input validations - 09-Oct-2026
            - **v70.6** - F3 - Info price table and extra services are pulled from DB -> more interactive UI - 08-Oct-2026
            - **v70.2** - F3 - CDM as a core of the function developed, Code refactored, CSV as new file format added - 01-Oct-2026
            - **v68.7** - F3 & F3B - Centralized DB connection handling - 02-Sep-2026
            - **v67.9** - F3 - Sequence in DB set -> allows concurrent users - 16-Aug-2026
            - **v65.1** - F3B - Major code refactoring & clean up - 08-July-2026
            - **v64.9** - F3 - Major code refactoring & clean up - 06-July-2026
            - **v63.1** - F3B - function extended by Analytics + code refactoring - 16-June-2026
            - **v52.3** - Function description extended by Video Guide - 03-Dec-2025
            - **v52.2** - New DB schema - SQL queries refactored - 01-Dec-2025
            - **v51.1** - F3B - Invoice overview now provides logs, if any mapping using F4 function - 16-Nov-2025
            - **v42.9** - F3B - Refactoring into better code blocks, reson: bug - 14-Nov-2025
            - **v42.7** - F3B - developed (Find your invoice) - 12-Nov-2025
            - **v42.0** - End of process: invoice is inserted into DB - 10-Nov-2025
            - **v41.0** - Connected to DB to get transport price - 10-Nov-2025
            - **v17.2** - End of the process adjusted - info message/box appears - 28-July-2025	
            - **v5.2** - Try/Except - Error handling - 17-Jun-2025	 
            - **v0.7** - Bug fix/fine tuning - 23-March-2025
            - **v0.6** - F3 released - 13-March-2025
        """)

        st.write("")
        st.write("""
        - F4:
            - **v70.4** - UI extended by visibility of last 10 Transformations - 02-Oct-2026
            - **v70.3** - Function rebuilt to use CDM and validate file data against DB data - 02-Oct-2026
            - **v68.7** - Centralized DB connection handling - 02-Sep-2026
            - **v65.0** - Major code refactoring & clean up - 07-July-2026
            - **v52.3** - Function description extended by Video Guide - 03-Dec-2025
            - **v52.2** - New DB schema - SQL queries refactored - 01-Dec-2025
            - **v50.1** - Log about mapping put into DB as a record about this activity - 16-Nov-2025	
            - **v7.2** - Try/Except - Error handling, if wrong file uploaded - 18-Jun-2025	
            - **v0.7** - F4 released - 23-March-2025
        """)

def display_release_notes_expander_f5():
    with st.expander(
        "Release notes - F5 & F5B",
        icon= UiConfigAndIcons.Pages.release_notes["icon"]
        ):	
        st.write("""
        - **v68.9** - F5 - Code refactored: def functions moved to operatonal_functions.py - 03-Sep-2026
        - **v68.7** - F5B - Centralized DB connection handling - 02-Sep-2026
        - **v67.3** - F5B Scheduler to DELETE records older than 100 days from DB released - 07-Aug-2026
        - **v63.0** - F5B Radio button (Month data, Last 30 days) + Expander with data - 01-June-2026
        - **v61.9** - F5B rate metrics added - 18-May-2026
        - **v61.8** - F5B release  - 14-May-2026
        - **v55.3** - Adjustment of format of results - 17-Mar-2026
        - **v54.5** - Major code refactoring -> cleaner code & better modularity - 09-Dec-2025
        - **v11.0** - try-except logic added + timeout 5 secs, to cover unavailability of APIs - 04-July-2025
        - **v4.1** - API 3 added (status/monitoring of API 2 get requests) - 16-Jun-2025
        - **v2.7** - API 2 added - 10-Jun-2025
        - **v2.6** - F5 developed (API 1) - 10-Jun-2025
        """)


def display_release_notes_expander_f6():
    with st.expander(
        "Release notes - F6",
        icon= UiConfigAndIcons.Pages.release_notes["icon"]
        ):	
        st.write("""
        - **v69.5** - Extended by validation/normalization using XREF dictionaries - 07-Sep-2026
        - **v69.4** - Reworked normalization & validation of user input to reduce unnecessary API calls - 05-Sep-2026
        - **v69.0** - Code refactored: Centralized API handling, Reworked fallback logic & executing orchestration, better UI visualization - 03-Sep-2026
        - **v50.1** - Code refactored: into blocks - 14-Nov-2025
        - **v12.1** - Better visualization of results (tabs) - 06-July-2025
        - **v12.0** - APIs not called in case of empty forms (missing inputs) - to not waste API calls - 06-July-2025
        - **v10.2** - Additional try-except logic to cover API limit reached situation  - 03-July-2025
        - **v10.0** - F6 released - 02-July-2025
        """)

def display_release_notes_expander_f7():
    with st.expander(
        "Release notes - F7 & F7B",
        icon= UiConfigAndIcons.Pages.release_notes["icon"]
        ):	
        st.write("""
            - **v69.8** - F7 - DB insert service optimized to commit data insert only in case that all database operations succeed - 14-Sep-2026
            - **v69.7** - F7 - Adjusted to use the same UI offer visualization as F7B (now unified cross-function) - 13-Sep-2026
            - **v69.1** - F7 - Centralized API handling - 04-Sep-2026
            - **v68.7** - F7 & F7B - Centralized DB connection handling & F7 adjustment of fallback logic if DB not connected - 02-Sep-2026
            - **v68.5** - F7B - Concurrency rule set for manual state update Approve/Reject (done by user via UI) - 01-Sep-2026
            - **v68.2** - F7B - Offer rating function released - 27-Aug-2026
            - **v68.1** - F7B - Code refactoring -> simplification - 25-Aug-2026
            - **v68.0** - F7 - Sequence in DB set -> allows concurrent users - 16-Aug-2026
            - **v67.5** - F7B upgrade of UI for better visualization of offer states TAB 1, TAB 2 - 09-Aug-2026
            - **v67.2** - F7 refactored time calculation, F7B STATE logic extended - 07-Aug-2026
            - **v67.1** - F7B - GitHub Action cron job for STATE changes - 05-Aug-2026
            - **v67.0** - F7 & F7B - Offer STATES introduced - pilot version - 04-Aug-2026
            - **v66.0** - F7 - Major code refactoring & clean up - 02-Aug-2026
            - **v63.2** - F7B - Adjustment of fallback on UI (if no records in DB) - 16-June-2026
            - **v60.0** - F7 Go Green calculation released - 21-Apr-2026
            - **v55.8** - F7B Analytics tab released - 09-Apr-2026
            - **v55.6** - F7B Customized search - filtering by date released - 28-Mar-2026
            - **v55.5** - F7B Customized search option released - 26-Mar-2026
            - **v55.4** - F7 Input data moved into separate .py to be used by F7B later - 25-Mar-2026
            - **v55.0** - F7 & F7B - Graphical illustration of transport flow - 13-Mar-2026
            - **v54.9** - F7B - Search for specific offer released - 10-Mar-2026
            - **v54.6** - F7B introduced - simple view into DB - 12-Jan-2026
            - **v54.1** - Function now produces also PDF offer - 07-Dec-2025
            - **v54.0** - DB connected - Offers can be stored in DB - 07-Dec-2025
            - **v52.4** - Function description extended by Video Guide - 04-Dec-2025
            - **v35.0** - Plotly() arguments adjusted, deprication will happen end of 2025  - 20-Oct-2025
            - **v33.5** - 'Delivery at' also added to TAB2 -> available in analytics for other transports - 16-Sep-2025
            - **v33.4** - 'Offer to be approved till' option added -> influences 'delivery at' date & time - 15-Sep-2025
            - **v33.0** - 'Delivery at' added (Weekday - DD-Month-YY HH:MM - CET/CEST) & logic for delivery time frames - 13-Sep-2025
            - **v32.9** - TAB2 Charts added -> better visualization - 11-Sep-2025
            - **v32.7** - TAB2 Analytics & Other transport types after Submit button - 10-Sep-2025
            - **v30.8** - Distance correction list introduced (for specific roads not possible to calculate) - 28-Aug-2025
            - **v30.1** - DTD also extends time for delivery; Airplane & Train if DTD, includes time for shipment transfer to Truck - 21-Aug-2025	
            - **v22.3** - Better calculation method for Airplane - 19-Aug-2025	
            - **v22.0** - V2 of R1C1 map & adjustment of distance calculation & AT, DE, PL onboarded - 18-Aug-2025		  
            - **v21.2** - Better data visualization in expanders + Dashboard expander added - 15-Aug-2025
            - **v20.0** - F7 released - 09-Aug-2025
        """)


def display_release_notes_expander_f8():
    with st.expander(
        "Release notes - F8",
        icon= UiConfigAndIcons.Pages.release_notes["icon"]
        ):	
        st.write("""
        - **v68.8** - Code optimization to call DB only 1x per script run (was happening 2x) - 02-Sep-2026
        - **v68.7** - Centralized DB connection handling - 02-Sep-2026
        - **v64.6** - TABs extended by country flags + Company info expander added - 02-July-2026
        - **v64.5** - DFs extended by PINs and colored -> better visualization on UI - 01-July-2026
        - **v64.4** - TAB 4 Branch info released - 28-Jun-2026
        - **v64.2** - DB design changed & TAB 2 extended also by MAP - 18-Jun-2026
        - **v64.1** - TAB 1 extended by MAP to visualize branches - 17-Jun-2026
        - **v64.0** - Code refactoring & clean up - 17-Jun-2026
        - **v52.5** - Function description extended by Video Guide - 05-Dec-2025
        - **v36.9** - 'branch' table introduced -> SQL results better customized - 05-Nov-2025
        - **v36.7** - 2 more SQLs - num. of companies & num. of branches - 04-Nov-2025
        - **v36.2** - F8 released - 31-Oct-2025
        """)