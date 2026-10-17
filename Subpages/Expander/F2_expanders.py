import streamlit as st
from Subpages.Resources import Assets
from Subpages.Resources_ui import UiConfigAndIcons
from Subpages.Resources_ui_objects import render_error_info
from Subpages.Resources_ui_objects import render_link_button

def show_expander_help():

    with st.expander(
        "Help",
        icon= UiConfigAndIcons.Expanders.help_additional_info
        ):

        st.write("**What file?**")
        st.write("- Only **XML** is allowed to be uploaded")
        st.write("- You can use any of the **predefined files**")

        render_link_button(
            label= "Function 1",
            url= Assets.Links.App.f1_function            
        )

        st.write("-------")
        st.write("**Advanced approach:**")
        st.write("- If you know XML and XSD principles, you can try this")
        st.write("- The XML files can be **customized** or you can create **your own** following a template/structure")

        st.write("")
        st.write("")
        st.write("Steps:")
        st.write("""
            1) Go to Function 1
                - **Either** you can **customize** the predefines files 1), 2), 3)
                - **Or** you can **create your own** from scratch. You can use template 4) for the beginning
                                
            """)
        
        render_link_button(
            label = "Function 1",
            url= Assets.Links.App.f1_function           
        )

        st.write("2) Download a XML file")
        st.write("3) Do/change/customize it how you like but **follow rules of XML Schema**")

        render_link_button(
            label = "XML Schema",
            url= Assets.Links.App.f2_xml_xsd          
        )



def show_expander_help_validation_process():
    
    st.write("""
    - If validation **not passed**
    - Not matching **sum of values** in detail
    - The dashbords bellow are **impacted**
    - More info:
    """)

    st.write("")
    render_link_button(
        label = "XML Schema description",
        url= Assets.Links.App.f2_xml_xsd          
    )

    st.image("Pictures/Function_2/F2_validation_xml.png")


# ==== XSD not passed ====
def xsd_not_passed():

    render_error_info("XML is not valid")

    with st.expander(
        "Help - XML is not valid",
        icon=UiConfigAndIcons.Expanders.help_additional_info
        ):


        st.write("- Please check the uploaded file")

        st.write("- Data  or structure is not line with XML Schema")

        st.write("")
        st.write("**How to fix this?**")
        st.write("- **Either** you can use any of the **predefined files**:")

        render_link_button(
            label="Function 1",
            url= Assets.Links.App.f1_function
        )

        st.write("")
        st.write("- **Or** you can see more about the XSD/XML definition for this Function 2 -> which should help to fix. **XSD** is at the bottom of the page")

        render_link_button(
            label = "XML Schema description",
            url= Assets.Links.App.f2_xml_xsd          
        )

    st.stop()