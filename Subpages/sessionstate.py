import streamlit as st

st.write('cus')

if 'a_counter' not in st.session_state:
    st.session_state['a_counter'] = 0


if st.button("up"):
    st.session_state['a_counter'] += 1



if st.button("down"):
    st.session_state['a_counter'] -= 1


if st.button("reset"):
    st.session_state['a_counter'] = 0
st.write(st.session_state['a_counter'])