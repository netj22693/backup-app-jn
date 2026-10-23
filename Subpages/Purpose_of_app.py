import streamlit as st
from Subpages.Resources import Assets
from Subpages.Resources_ui import UiConfigAndIcons
from Subpages.Resources_ui_objects import render_specific_page, render_description_page, render_function_page
from Subpages.Home_page.HP_expanders import display_expander_github, display_expander_linkedin, display_expander_overview_functions, display_expander_web_app



st.write("# Welcome!")
''
''

st.write(
    "Purpose of this application is to play with **data structures/objects (XML, JSON, dictionaries, dataframes, etc.)** and implement them into **smaller versions of real business cases**. The application has **8 Functions**."
    )
''
display_expander_overview_functions()
''
''
"More details about the Functions can be seen on the subpages - what the Functions do, what data structures are used, etc."

st.write("enjoy... :)") 

''
''
tab1,tab2, tab3 = st.tabs([
    "Architecture landscape",
    "ArchiMate - Overview Functions",
	"UML - Overview Functions"
])

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


''
''
''
display_expander_linkedin()

display_expander_github()

display_expander_web_app()


''
''
st.write("### Go to:")
st.write("**Recommendation:** To firstly read the description to understand how the Functions/application work. The application navigation bar can help to get oriented.")

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
