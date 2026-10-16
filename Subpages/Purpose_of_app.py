import streamlit as st
from Subpages.Description.APP_description_release_notes import display_release_notes_expander
from Subpages.Resources import Assets
from Subpages.Resources_ui import UiConfigAndIcons
from Subpages.Resources_ui_objects import render_specific_page, render_description_page, render_function_page



st.write("# Welcome!")
''
''

st.write(
    "Purpose of this application is to play with **data structures/objects (XML, JSON, dictionary, dataframes)** and implement them into **smaller versions of real business cases**. The application has **8 functions**."
    )
''
with st.expander("Overview of functions", icon= UiConfigAndIcons.Expanders.list):
	st.write("""
		- **Function 1:** Download of few predefined types of XML for Function 2
		- **Function 2:** Parsing of data from XML -> their visualization -> producing of simple .txt file as summary      
		""")
	''
	st.write("""
		- **Function 3**: Creation of invoice based on user inputs (CSV, JSON or XML) - **DB on cloud**
		- **Function 3B:** Invoice Visibility - Visibility & Analytics based on invoices created in F3
		- **Function 4**: Data Transfer of the invoice ; to CSV, JSON or XML 
		""")
	''
	st.write("""
		- **Function 5:** Exchange rate/calculation (CZK, EUR, USD) - **API based** with actual exchange rate
		- **Function 5B:** Exchange rate - Trend - **Background job based**, data continuously collected into DB and visualized via app UI
		""")
	''
	st.write("""
		- **Function 6:** ZIP code - (1) Get ZIP code(s) based on City, (2) Get City based on ZIP code - **API based**
		"""
		)
	''
	st.write("""
		- **Function 7:** Transport calculation - **API** provides input & **DB on cloud** (:green[**my favorit function**])
		- **Function 7B:** Offer Visibility - Visibility & Analytics based on transport offers created in F7
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
    "Architecture landscape",
    "ArchiMate - Overview Functions",
	"UML - Overview Functions"
])

#Tab 1
with tab1:
	render_specific_page(
		page_key= "app_architecture",
		label_customized= f"{UiConfigAndIcons.Pages.architecture['label']} :material/chevron_right:"
	)

	''
	''
	st.image(Assets.Images.architecture_landscape)

with tab2:
	st.image(Assets.Images.archimate_main)
	
with tab3:
	# Border Width: 10
	st.image(Assets.Images.uml_f1_f2)
	''
	st.image(Assets.Images.uml_f3_f3b_f4)
	''
	st.image(Assets.Images.uml_f5)
	''
	st.image(Assets.Images.uml_f6)
	''
	st.image(Assets.Images.uml_f7_f7b)
	''
	st.image(Assets.Images.uml_f8)


# LinkedIn - expander
''
''
''

with st.expander(
	"Contact - LinkedIn",
	icon=":material/id_card:"
):	
	''
	st.image("Pictures/linkedin-logo-2013-1.svg", width=95)
	st.write(f"- Do you like this app? :) LinkedIn profile [Here]({Assets.Links.External.linked_in})")
	st.write("- Author: Jan Netolicka")


# GitHub - expander
with st.expander(
	"Repository - GitHub",
	icon=":material/deployed_code_history:"
):	

	''
	st.write(f"- GitHub code repository link [Here]({Assets.Links.External.git_hub})")
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
display_release_notes_expander()


# Buttons for redirectiong to the relevant Functions
''
''
st.write("### Go to:")
st.write("**Recommendation:** To firstly read the description chapters (the application navigation bar) to understand how the functions/application work.")

''
render_specific_page("virtual_assistant") 
render_specific_page("app_architecture")

''
render_description_page(
	label= "Description about F1 and F2",
	page= Assets.Paths.Description.f1_f2
)
render_function_page(
	label= "Function 1",
	page= Assets.Paths.Function.f1
)

render_function_page(
	label= "Function 2",
	page= Assets.Paths.Function.f2
)

''
render_description_page(
    label= "Description about F3, F3B and F4",
	page= Assets.Paths.Description.f3_f4,
)

render_function_page(
	label= "Function 3",
	page= Assets.Paths.Function.f3,
) 

render_function_page(
	label= "Function 3B",
	page= Assets.Paths.Function.f3b,
) 

render_function_page(
	label = "Function 4",
	page= Assets.Paths.Function.f4,
) 

''
render_description_page(
    label = "Description about F5 and F5B",
	page= Assets.Paths.Description.f5,
) 

render_function_page(
	label = "Function 5",
	page= Assets.Paths.Function.f5,
) 

render_function_page(
	label = "Function 5B",
	page= Assets.Paths.Function.f5b,
) 

''
render_description_page(
    label = "Description about F6",
	page= Assets.Paths.Description.f6,
)

render_function_page(
	label = "Function 6",
	page= Assets.Paths.Function.f6,
) 

''
render_description_page(
    label = "Description about F7 and F7B",
	page= Assets.Paths.Description.f7,
)

render_function_page(
	label = "Function 7",
	page= Assets.Paths.Function.f7,
) 

render_function_page(
	label = "Function 7B",
	page= Assets.Paths.Function.f7b,
) 

''
render_description_page(
    label = "Description about F8",
	page= Assets.Paths.Description.f8,
)

render_function_page(
	label = "Function 8",
	page= Assets.Paths.Function.f8,
)
