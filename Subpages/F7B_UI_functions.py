import streamlit as st


# ======= UI =======
def display_state_flow():

    st.write("") # Workaround for space on UI 
    st.image("Pictures/Function_7/F7B_state_flow/F7B_state_flow_v1.svg", width = 680)

def display_state_flow_expander():

    with st.expander("State flow", icon=":material/info:"):
        st.image("Pictures/Function_7/F7B_state_flow/F7B_state_flow_v1.svg", width = 580)
        st.write("") # Workaround for space on UI
        st.write(" - For manual **Approve/Reject** - Go to **Search for specific offer** tab and search for the offer.")
