import streamlit as st


st.write("# Welcome!")
''
st.write(
    "Purpose of this application is to play with XML and JSON data. The application has **6 functions**:"
    )
''
st.write("""
    - **Function 1:** Download of few predefined types of XML for Function 2
    - **Function 2:** Parsing of data from XML -> their visualization -> producing of simple .txt file as summary      
    """)
''
st.write("""
    - **Function 3:** Creation of XML (slightly different one than used in F1 and F2) or JSON, through the application screen (manual inputs)
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
''
"More details about the functions can be seen in the subpages - what the functions do, what data structures are used, etc."

st.write("enjoy... :)") 

''
''
# split into Tabs 
tab1,tab2 = st.tabs([
    "ArchiMate - Overview",
    "UML - Activity diagram - Overview "
])

#Tab 1
with tab1:
	st.write("###### ArchiMate - Overview of the functions:")
	''
	# st.image("Pictures/Archimate_functions_overview.svg")
	st.image("Pictures/Archimate_functions_overview_3.svg")
	
with tab2:
	st.write("###### UML - Overview of the functions:")
	''
	st.image("Pictures/Overall_UML_F1 and F2.svg")
	''
	st.image("Pictures/Overall_UML_F3 and F4.svg")
	''
	st.image("Pictures/Overall_UML_F5.svg")
	''
	st.image("Pictures/Overall_UML_F6.svg")
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
	use_container_width=True,
    icon=":material/code:",
	) 
st.page_link(
	label = "Function 1",
	page="Subpages/F1_FUNCTION_XML_dowload.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/play_circle:"
	) 

st.page_link(
	label = "Function 2",
	page="Subpages/F2_FUNCTION_XML_parsing_to_txt_outcome.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/play_circle:"
	) 
''
st.page_link(
    label = "Description about F3 and F4",
	page="Subpages/F3_F4_description.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/code:",
	) 

st.page_link(
	label = "Function 3",
	page="Subpages/F3_FUNCTION_creation_of_XML.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/play_circle:"
	) 

st.page_link(
	label = "Function 4",
	page="Subpages/F4_FUNCTION_translation_mapping.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/play_circle:"
	) 
''
st.page_link(
    label = "Description about F5",
	page="Subpages/F5_description_API.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/code:",
	)

st.page_link(
	label = "Function 5",
	page="Subpages/F5_FUNCTION_exchange.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/play_circle:"
	)
''
st.page_link(
    label = "Description about F6",
	page="Subpages/F6_description_API.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/code:",
	)

st.page_link(
	label = "Function 6",
	page="Subpages/F6_FUNCTION_zip_code.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
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
	''
	st.write("- GitHub code repository link [Here](https://github.com/netj22693/backup-app-jn/blob/main/streamlit_app.py)")
	st.image("Pictures/Github_archimate_2.svg")

# Web app - expander

with st.expander(
	"Web app - Recommendation",
	icon=":material/computer:"
):	

	''
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
	- Function 6:
		- **v12.1** - Better visualization of results (tabs) - 06-July-2025
		- **v12.0** - APIs not called in case of empty forms (missing inputs) - to not waste API calls - 06-July-2025
		- **v10.2** - Additional try-except logic to cover API limit reached situation  - 03-July-2025
		- **v10.0** - F6 released  - 02-July-2025
	""")

	''
	st.write("""
	- Function 5:
		- **11.0** - try-except logic added + timeout 5 secs, to cover unavailability of APIs  - 04-July-2025
		- **v4.1** - API 3 added (status/monitoring of API 2 get requests)  - 16-Jun-2025
		- **v2.7** - API 2 added  - 10-Jun-2025
		- **v2.6** - F5 developed (API 1)  - 10-Jun-2025
	""")


	''
	st.write("""
	- Function 4:
		- **v7.2** - Try/Except - Error handling, if wrong file uploaded  - 18-Jun-2025	
		- **v0.7** - F4 released  - 23-March-2025
	""")
	

	''
	st.write("""
	- Function 3:
		- **v5.2** - Try/Except - Error handling, if wrong file uploaded  - 17-Jun-2025		  
		- **v0.7** - Bug fix/fine tuning  - 23-March-2025
		- **v0.6** - F3 released - 13-March-2025
	""")


	''
	st.write("""
	- Function 2:
		- **v16.2** - New expander (SQL 4 - average values) - 22-July-2025
		- **v15.0** - Input XML validated against XSD (new feature built) - 11-July-2025
		- **v14.0** - New expander (SQL 3) - another SQL queries & Pie charts - 10-July-2025
		- **v8.1** - More filters/Advanced filtering - 23-Jun-2025		
		- **v5.2** - Try/Except - Error handling, if wrong file uploaded  - 17-Jun-2025		  
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


