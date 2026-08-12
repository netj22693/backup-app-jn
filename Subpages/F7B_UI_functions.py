import streamlit as st
from Subpages.Resources import Assets


# ======= UI =======
def display_state_flow():

    st.write("") # Workaround for space on UI 
    st.image(Assets.Images.f7_state_flow, width = 680)

def display_state_flow_expander():

    with st.expander("State flow", icon=":material/info:"):
        st.image(Assets.Images.f7_state_flow, width = 580)
        st.write("") # Workaround for space on UI
        st.write(" - For manual **Approve/Reject** - Go to **Search for specific offer** tab and search for the offer.")
