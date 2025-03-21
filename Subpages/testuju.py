import streamlit as st

# Define a callback function that updates the greeting
def update_greeting():
    name = st.session_state.name
    st.session_state.greeting = f'Hello, {name}!'

# Create a text input widget that calls the callback function
st.text_input('Enter your name', key='name', on_change=update_greeting)

# Display the greeting
if 'greeting' in st.session_state:
    st.write(st.session_state.greeting)