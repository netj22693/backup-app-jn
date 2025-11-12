import streamlit as st


st.write("# Welcome!")
''
st.write(
    "Purpose of this application is to play with **data structures/objects (XML, JSON, dictionary, dataframes)** and implement them into **smaller versions of real business cases**. The application has **8 functions**:"
    )
''
st.write("""
    - **Function 1:** Download of few predefined types of XML for Function 2
    - **Function 2:** Parsing of data from XML -> their visualization -> producing of simple .txt file as summary      
    """)
''
st.write("""
    - **Function 3:** Creation of XML (slightly different one than used in F1 and F2) or JSON, through the application screen (manual inputs) - **DB on cloud**
    - **Function 4:** Mapping/change of file format XML -> JSON or JSON -> XML 
    """)
''
st.write("""
    - **Function 5:** Exchange rate/calculation (CZK, EUR, USD) - **API based** with actual exchange rate
    """)
''
st.write("""
    - **Function 6:** ZIP code - (1) Get ZIP code(s) based on City, (2) Get City based on ZIP code - **API based**
    """
    )
''
st.write("""
    - **Function 7:** Transport calculation - **API** provides input (:green[**my favorit function**])
    """
    )
''
st.write("""
    - **Function 8:** Company Book - provides visibility of transport companies - **DB on cloud**
    """
    )
''
''
"More details about the functions can be seen in the subpages - what the functions do, what data structures are used, etc."

st.write("enjoy... :)") 

''
''
# split into Tabs 
tab1,tab2, tab3 = st.tabs([
    "ArchiMate - Overview",
    "UML - Activity diagram - Overview",
	"Architecture landscape"
])

#Tab 1
with tab1:
	st.write("###### ArchiMate - Overview of the functions:")
	''
	st.image("Pictures/Archimate_functions_overview_9.svg")
	
with tab2:
	st.write("###### UML - Overview of the functions:")
	''
	st.image("Pictures/Overall_UML_F1 and F2.svg")
	''
	st.image("Pictures/Overall_UML_F3 and F4_v2.svg")
	''
	st.image("Pictures/Overall_UML_F5.svg")
	''
	st.image("Pictures/Overall_UML_F6.svg")
	''
	st.image("Pictures/Overall_UML_F7.svg")
	''
	st.image("Pictures/Overall_UML_F8.svg")

with tab3:
	st.write("###### Architecture landscape:")
	''
	st.image("Pictures/App_landscape_architecture_v3.svg")

''
''
# Buttons for redirectiong to the relevant Functions
st.write("### Go to:")
st.write("**Recommendation:** To firstly read the description chapters (the application navigation bar) to understand how the functions/application work.")
''
st.page_link(
    label = "Description about F1 and F2",
	page="Subpages/F1_F2_description_function.py",
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
    icon=":material/code:",
	) 
st.page_link(
	label = "Function 1",
	page="Subpages/F1_FUNCTION_XML_dowload.py",
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
	icon=":material/play_circle:"
	) 

st.page_link(
	label = "Function 2",
	page="Subpages/F2_FUNCTION_XML_parsing_to_txt_outcome.py",
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
	icon=":material/play_circle:"
	) 
''
st.page_link(
    label = "Description about F3 and F4",
	page="Subpages/F3_F4_description.py",
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
    icon=":material/code:",
	) 

st.page_link(
	label = "Function 3",
	page="Subpages/F3_FUNCTION_creation_of_XML.py",
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
	icon=":material/play_circle:"
	) 

st.page_link(
	label = "Function 3B",
	page="Subpages/F3b_FUNCTION_invoice_visibility.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/play_circle:",
	)

st.page_link(
	label = "Function 4",
	page="Subpages/F4_FUNCTION_translation_mapping.py",
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
	icon=":material/play_circle:"
	) 
''
st.page_link(
    label = "Description about F5",
	page="Subpages/F5_description_API.py",
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
    icon=":material/code:",
	)

st.page_link(
	label = "Function 5",
	page="Subpages/F5_FUNCTION_exchange.py",
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
	icon=":material/play_circle:"
	)
''
st.page_link(
    label = "Description about F6",
	page="Subpages/F6_description_API.py",
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
    icon=":material/code:",
	)

st.page_link(
	label = "Function 6",
	page="Subpages/F6_FUNCTION_zip_code.py",
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
	icon=":material/play_circle:"
	) 

''
st.page_link(
    label = "Description about F7",
	page="Subpages/F7_description.py",
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
    icon=":material/code:",
	)

st.page_link(
	label = "Function 7",
	page="Subpages/F7_FUNCTION_transport.py",
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
	icon=":material/play_circle:"
	) 

''
st.page_link(
    label = "Description about F8",
	page="Subpages/F8_description.py",
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
    icon=":material/code:",
	)

st.page_link(
	label = "Function 8",
	page="Subpages/F8_FUNCTION_company_book.py",
	help="The button will redirect to the relevant page within this app.",
	width="stretch",
	icon=":material/play_circle:"
	) 

# Bug - expander
''
''
''
with st.expander("Have you seen a bug? Report it here.",icon= ":material/pest_control:"):

    ''
    st.write("Please provide details:")

    contact_form ="""
        <form action="https://formsubmit.co/honza.ne@seznam.cz" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="subject" placeholder= "Subject" required>
            <textarea name="message" placeholder="Description..."></textarea>
            <button type="submit">Send</button>
        </form>
    """

    st.markdown(contact_form, unsafe_allow_html = True)

    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css("Subpages/CSS/style.css")

    ''
    ''
    st.caption("Powered by FormSubmit")
    st.image("Pictures/formsubmitlogo.png", width=150)

# LinkedIn - expander

with st.expander(
	"Contact - LinkedIn",
	icon=":material/id_card:"
):	
	''
	st.image("Pictures/linkedin-logo-2013-1.svg", width=95)
	st.write("- Do you like this app? :) LinkedIn profile [Here](https://www.linkedin.com/in/jan-netolicka-12209a221/)")
	st.write("- Author: Jan Netolicka")


# No AI - expander

with st.expander(
	"No AI used in the code",
	icon=":material/block:"
):	

	''
	st.write("""
	- **NO** vibe-coding/AI used in this app 
	- I build this app as a hobby to train my brain
	- The code is written by me with help of Python documentation, Google, Stack Overflow and other forums in case I get stuck :)
	""")
	''

# GitHub - expander

with st.expander(
	"Repository - GitHub",
	icon=":material/deployed_code_history:"
):	

	''
	st.write("- GitHub code repository link [Here](https://github.com/netj22693/backup-app-jn/blob/main/streamlit_app.py)")
	st.image("Pictures/Github_archimate_2.svg")

# Web app - expander

with st.expander(
	"Web app - Recommendation",
	icon=":material/computer:"
):	

	''
	st.write("- The Streamlit Framework helps to build web apps")
	st.write("- The **primary** approach is through **web browser**")
	st.write('- :green[**The best way is to use the app on your laptop or some "bigger" device to get the full experience**]')
	st.write("- It is also working on Mobile phones - but some of the features might be slightly impacted. Specifically charts and images due to screen size")
	''

# Release notes - expander

with st.expander(
	"Release notes",
	icon=":material/event_note:"
):	

	''
	st.write("Key highlights (* **vX.X** -> version of application):")

	''
	st.write("""
	- Function 8:
		- **v36.9** - 'branch' table introduced -> SQL results better customized - 05-Nov-2025
		- **v36.7** - 2 more SQLs - num. of companies & num. of branches - 04-Nov-2025
		- **v36.2** - F8 released - 31-Oct-2025
	""")

	''
	st.write("""
	- Function 7:
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

	''
	st.write("""
	- Function 6:
		- **v12.1** - Better visualization of results (tabs) - 06-July-2025
		- **v12.0** - APIs not called in case of empty forms (missing inputs) - to not waste API calls - 06-July-2025
		- **v10.2** - Additional try-except logic to cover API limit reached situation  - 03-July-2025
		- **v10.0** - F6 released - 02-July-2025
	""")

	''
	st.write("""
	- Function 5:
		- **v11.0** - try-except logic added + timeout 5 secs, to cover unavailability of APIs - 04-July-2025
		- **v4.1** - API 3 added (status/monitoring of API 2 get requests) - 16-Jun-2025
		- **v2.7** - API 2 added - 10-Jun-2025
		- **v2.6** - F5 developed (API 1) - 10-Jun-2025
	""")


	''
	st.write("""
	- Function 4:
		- **v7.2** - Try/Except - Error handling, if wrong file uploaded - 18-Jun-2025	
		- **v0.7** - F4 released - 23-March-2025
	""")
	

	''
	st.write("""
	- Function 3:
		- **v42.7** - F3B - developed (Find your invoice) - 12-Nov-2025
		- **v42.0** - End of process: invoice is inserted into DB - 10-Nov-2025
		- **v41.0** - Connected to DB to get transport price - 10-Nov-2025
		- **v17.2** - End of the process adjusted - info message/box appears - 28-July-2025	
		- **v5.2** - Try/Except - Error handling - 17-Jun-2025	 
		- **v0.7** - Bug fix/fine tuning - 23-March-2025
		- **v0.6** - F3 released - 13-March-2025
	""")


	''
	st.write("""
	- Function 2:
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



	''
	st.write("""
	- Function 1:
		- **v0.1** - F1 released (together with F2) - 20-Feb-2025
	""")

	''
	''


