import streamlit as st


with st.expander("Have you seen a bug? Report it here.",icon= ":material/pest_control:"):

    ''
    st.write("Please provide details:")

    contact_form ="""
        <form action="https://formsubmit.co/honza.ne@seznam.cz" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="subject" placeholder= "Subject" required>
            <textarea name="message" placeholder="Description..."></textarea>
            <button type="submit">Send</button>
        </form>
    """

    st.markdown(contact_form, unsafe_allow_html = True)

    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css("Subpages/CSS/style.css")

    ''
    ''
    st.caption("Powered by FormSubmit")
    st.image("Pictures/formsubmitlogo.png", width=150)
