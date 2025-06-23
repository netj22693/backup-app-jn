import streamlit as st


if 'counter' not in st.session_state:
    st.session_state.counter = 0

st.write(st.session_state.counter)

if st.button("up"):
    st.session_state.counter += 1
    st.write(st.session_state.counter)
