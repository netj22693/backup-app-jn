import streamlit as st

def show_expander_help():

    with st.expander(
                "Help",
                icon= ":material/help_outline:"
                ):

                ''
                ''
                st.write("**What file?**")
                st.write("- Only **XML** is allowed to be uploaded")
                st.write("- You can use any of the **predefined files**")

                st.link_button(
                    label = "Go to: Function 1",
                    url="https://dataparsing.streamlit.app/F1_FUNCTION_XML_dowload",
                    help="The button will redirect to the relevant page within this app.",
                    width="stretch",
                    icon=":material/launch:",
                    ) 
                ''
                ''
                st.write("-------")
                st.write("**Advanced approach:**")
                st.write("- If you know XML and XSD principles, you can try this")
                st.write("- The XML files can be **customized** or you can create **your own** following a template/structure")

                ''
                ''
                st.write("Steps:")
                st.write("""
                        1) Go to Function 1
                            - **Either** you can **customize** the predefines files 1), 2), 3)
                            - **Or** you can **create your own** from scratch. You can use template 4) for the beginning

                                            
                        """)
                st.link_button(
                    label = "Go to: Function 1",
                    url="https://dataparsing.streamlit.app/F1_FUNCTION_XML_dowload#4-xml-template",
                    help="The button will redirect to the relevant page within this app.",
                    width="stretch",
                    icon=":material/launch:",
                    ) 

                st.write("2) Download a XML file")
                st.write("3) Do/change/customize it how you like but **follow rules of XSD**")

                ''
                st.write("The rules of the XML and **XSD file** for download here:")

                st.link_button(
                    label = "XML principles for this Function 2",
                    url="https://dataparsing.streamlit.app/F1_F2_description_XML_XSD",
                    help="The button will redirect to the relevant page within this app.",
                    width="stretch",
                    icon=":material/launch:",
                    )



def show_expander_help_validation_process():
    
    ''
    st.write("""
    - If validation **not passed**, it is because summary of either 1. or 2. (or both) are not matching with values in detail
    - This is an alert that some of the values visualized in the dashbords bellow will **not be correct**
    - More details on the data parsing and validation here:
    """)

    ''
    st.link_button(
        label = "Go to XSD, XML description page",
        url="https://dataparsing.streamlit.app/F1_F2_description_XML_XSD",
        help="The button will redirect to the relevant page within this app for download.",
        width="stretch",
        icon=":material/launch:"
    )
    ''
    ''
    st.image("Pictures/Function_2/F2_validation_xml.png")