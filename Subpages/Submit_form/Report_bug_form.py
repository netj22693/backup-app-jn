import streamlit as st

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def display_report_bug_form():

    access_key = st.secrets["web3Forms"]["access_key"]

    # UI
    st.write("Please provide details:")
	
    contact_form =f"""
	<form action="https://api.web3forms.com/submit" method="POST">
		<input type="hidden" name="access_key" value={access_key}>
		<input type="text" name="Subject" required placeholder="Subject" maxlength="100">
		<textarea name="Message" required placeholder="Bug description" maxlength="500"></textarea>
		<button type="submit">Submit</button>
	</form>
    """

    st.markdown(contact_form, unsafe_allow_html = True)

    local_css("Subpages/Submit_form/style.css")

    st.write("")
    st.write("")
    st.caption("Powered by Web3Forms")
    st.image("Pictures/Logo/Logo_Web3Forms.svg", width=150)