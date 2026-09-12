import streamlit as st
from Subpages.Resources import Assets


def display_expander_pair_xml_xsd():

    with st.expander(
        "How to pair XML with XSD",
        icon= ":material/help_outline:"
        ):
        
        st.write("1) Download XSD Schema from this application:")
        st.write("")
        st.link_button(
            label = "Go to XSD page",
            url= Assets.Links.App.f2_xml_xsd,
            help="The button will redirect to the relevant page within this app for download.",
            width="stretch",
            icon=":material/launch:"

            ) 
        
        st.write("")
        st.write("")
        st.write("2) At the **BOTTOM** of the page - download button .xsd format -> XSD will be downloaded")
        st.write("")
        st.image("Pictures/V2_pictures/XSD download button.png", width=130)
        st.write("")
        st.write("")
        st.write("3) Find location where the XSD is located on your device (probably in Downloads folder)")
        st.write("")
        st.write("")
        st.write("4) Download XML Template from this section 4), just below :)")
        st.write("")
        st.write("")
        st.write("5) Open the XML Template file in your data editor (Notepad++ is for free)")
        st.write("")
        st.image("Pictures/V2_pictures/Altova notepad.png")
        st.write("")
        st.write("")
        st.write("6) Extend the XML root element <invoice> by the following:")
        st.write("")
        st.image("Pictures/V2_pictures/root extended.png")
        st.write("")
        st.write("""
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:noNamespaceSchemaLocation="*location of your XSD file*">
            """)
        st.write("")
        st.write("")
        st.write("7) **XML should be paired with XSD now**")
        st.write("")
        st.write("")
        st.write("8) Depending on data editor tool you use - you can work with the validation and control that you follow predefined rules in the XSD")
        st.write("")
        st.image("Pictures/V2_pictures/validation xsd final_2.png")
        st.write("")
        st.write("")
        st.write("9) Once no error detected in your XML -> you can upload it in the app in Function 2 section")
        st.write("")
        st.image("Pictures/V2_pictures/no error.png")
        st.write("")
        st.write("")
        st.page_link(
            label = "Go to Function 2",
            page= Assets.Paths.Function.f2,
            help="The button will redirect to the relevant page within this app.",
            width="stretch",
            icon=":material/play_circle:"
            ) 
        st.write("")
        st.write("")