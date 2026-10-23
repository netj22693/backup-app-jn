import streamlit as st
from Subpages.Resources_ui_objects import render_specific_page
from Subpages.Resources_ui import UiConfigAndIcons
from Subpages.Release_notes.RN_release_notes import display_release_notes_expander_app_specific, display_release_notes_expander_va, display_release_notes_expander_f1_f2, display_release_notes_expander_f3_f4, display_release_notes_expander_f5, display_release_notes_expander_f6, display_release_notes_expander_f7, display_release_notes_expander_f8

st.write("# Release notes")
''
''
''
''
st.image("Pictures/Release_notes_timeline_v1.svg")

render_specific_page(
        page_key= "app_architecture",
        label_customized= f"{UiConfigAndIcons.Pages.architecture['label']} :material/chevron_right:"
    )
''
tab1, tab2, tab3, tab4 = st.tabs([
 "Foundation",
 "Feature expansion",
 "Consolidation & Refactoring",
 "Centralization, Consistency & Reusability"
])

with tab1:
    st.write("""
        - Build and implementation of first Functions
        - Foundation of their core logic
        """)
    ''
    ''
    ''
    ''
    ''

with tab2:
    st.write("""
        - Technical and business logic expansion 
        - Using new components like APIs and DB
        - Need of extension of fallback logic
        """)
    ''
    ''
    ''
    ''
    ''

with tab3:
    st.write("""
        - Modularity as a new approach 
        - Majore code refactoring
        - Aim to get cleaner code and separated bounderies 
        - Must for growth of Functions logic
        """)
    ''
    ''
    ''
    ''
    ''

with tab4:
    st.write("""
        - Architecture concept set 
        - Centralization -> DRY concept 
        - Centralized components -> reusability
        - Separation of concerns
        - Set of conventions
        - Centralized UI config & UI icon unification
        - UI wrappers 
        """)
    ''

''
''
display_release_notes_expander_app_specific()

display_release_notes_expander_va()

display_release_notes_expander_f1_f2()

display_release_notes_expander_f3_f4()

display_release_notes_expander_f5()

display_release_notes_expander_f6()

display_release_notes_expander_f7()

display_release_notes_expander_f8()


# ===== Page navigation at the bottom ======
''
''
st.write("-------")
render_specific_page("app_architecture")