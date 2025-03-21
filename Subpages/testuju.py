import streamlit as st

st.write("The button can only close the expander the first time! And not after the expander is manually opened.")

if "expander_state" not in st.session_state:
    st.session_state["expander_state"] = True

def toggle_closed():
    # <potentially do other actions>
    st.session_state["expander_state"] = False

st.button("do stuff then close expander",on_click=toggle_closed)

with st.expander("test expander",expanded = st.session_state["expander_state"]):
    st.write("expander is open")