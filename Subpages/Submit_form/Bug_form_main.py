import streamlit as st
from Subpages.Submit_form.Report_bug_form import display_report_bug_form

st.write("# :material/pest_control: Report a Bug:")
''
''

with st.container(border=True, width="stretch"):
    display_report_bug_form()