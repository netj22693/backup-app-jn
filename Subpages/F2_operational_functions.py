import streamlit as st
import pandas as pd
from pandas.io.formats.style import Styler
import plotly.express as px
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from lxml import etree
from plotly.graph_objects import Figure


# ==== Final close dialog ====
@st.dialog("Go to:")
def close_function():

    ''
    st.page_link(
        label = "Function 3 - Description",
        page="Subpages/F3_F4_description.py",
        help="The button will redirect to the relevant page within this app.",
        width="stretch",
        icon=":material/code:",
        )

    st.page_link(
        label = "Function 3",
        page="Subpages/F3_FUNCTION_creation_of_XML.py",
        help="The button will redirect to the relevant page within this app.",
        width="stretch",
        icon=":material/play_circle:",
        )
    
    st.page_link(
        label = "Home page",
        page="Subpages/Purpose_of_app.py",
        help="The button will redirect to the relevant page within this app.",
        width="stretch",
        icon=":material/home:",
        )

# ==== XSD not passed ====
def xsd_not_passed():

    ''
    ''
    st.error("The uploaded XML doesn't follow XSD rules -> the XML is not valid for this application")

    with st.expander(
        "Help",
        icon= ":material/help_outline:"
        ):

        ''
        st.write("- Please check the uploaded file")
        ''
        st.write("- Data issue/structure issue not following XSD/XML definition for this Function 2")
        ''
        ''
        st.write("**How to fix this?**")
        st.write("- **Either** you can use any of the **predefined files**:")
        ''
        st.link_button(
                    label = "Go to: Function 1",
                    url="https://dataparsing.streamlit.app/F1_FUNCTION_XML_dowload",
                    help="The button will redirect to the relevant page within this app.",
                    width="stretch",
                    icon=":material/launch:",
        ) 

        ''
        st.write("- **Or** you can see more about the XSD/XML definition for this Function 2 -> which should help to fix. **XSD** is at the bottom of the page")
        ''

        st.link_button(
                    label = "XML principles for this Function 2",
                    url="https://dataparsing.streamlit.app/F1_F2_description_XML_XSD",
                    help="The button will redirect to the relevant page within this app.",
                    width="stretch",
                    icon=":material/launch:",
                    )

    st.stop()

# ======= Function for validation uploaded XML against XSD =========

def validate_xml_against_xsd(xml_path: str, xsd_path: str):

        #try-except - for case when uploaded file is RECOGNIZED as XML (has suffix .xml) but the content is NOT XML.
        try:
            xmlschema_doc = etree.parse(xsd_path)
            xmlschema = etree.XMLSchema(xmlschema_doc)

            xml_doc = etree.parse(xml_path)
            result = xmlschema.validate(xml_doc)

            # If validation passes -> F2 logic can continue 
            if result == True:
                pass

            else:
                xsd_not_passed()

        except:
            xsd_not_passed()

# ======= Data validation -> displays on UI ======
def data_validation(total_sum: float, sum_price: float, currency: str) -> str:

    result = total_sum - sum_price
    
    if result != 0:

        st.warning(f"""
        **NOT PASSED**
        - **Invoice summary** does **not** equal to **line values**
        - You can either continue with existing file or adjust the input file and upload it again.""")

        st.warning(f"""
        - **Total sum** in the XML invoice is: **{total_sum:.2f}** {currency}
        - But **summary of prices** in detail lines is: **{sum_price:.2f}** {currency}""")

        return "Sum total - Not passed"


    else:
        st.success("**PASSED**")
        return "Sum total - Passed"


def data_validation_services(value_total_sum_services_fl: float, sum_price_warranty: float, sum_price_insurance: float, currency: str) -> str:

    result = value_total_sum_services_fl - sum_price_warranty - sum_price_insurance
    sum_warranty_insurance = sum_price_warranty + sum_price_insurance

    
    if result != 0:
        st.warning("""
        **NOT PASSED**
        - **Summary** does **not** equal to **line values**
        - You can either continue with existing file or adjust the input file and upload it again.""")


        st.warning(f"""
        - **Total sum of SERVICES** in the XML invoice is: **{value_total_sum_services_fl:.2f}** {currency}
        - But **summary of prices** in detail lines is **{sum_warranty_insurance:.2f}** {currency}.""")

        return ("Services - Not passed")

    else:
        st.success("**PASSED**")
        return "Services - Passed"



# ======= Functions for parsing ======
def data_parsing_find(root: Element, findall_value: str, find_value: str, to_float: bool, to_list: bool) -> str | float | list:

    c = []
    for a in root.findall(findall_value):
        b = a.find(find_value).text
        c.append(b)
    
    value = c[0]

    if to_list == False:
        if to_float == True:
            return float(value)

        else:
            return value
    
    else:
        return c



def data_parsing_get(root: Element, findall_value: str, get_value: str) -> list:

    c = []
    for a in root.findall(findall_value):
        b = a.get(get_value)
        c.append(b)

    return c


def data_parsing_find_conditional(root: Element, findall_value: str, find_value: str, condition_type: str, find_value_after_condition: str) -> list :

    c = []
    for a in root.findall(findall_value):
        condition = a.find(find_value).text

        if condition == condition_type:
            d = a.find(find_value_after_condition).text
            c.append(d)

    return c


def data_parsing_including_additional_services(root: Element, findall_value: str,find_value: str, condition_type: str, find_value_after_condition: str, find_value_if_not_none: str) -> float:

    b = []
    for a in root.findall(findall_value):
        condition = a.find(find_value).text
        if condition == condition_type:
            # This 'None' condition follows the rule to parse data from <additional_service> element specifically <additional_service>/<service_price> only in case that <additional_service>/<service> is NOT 'None
            item = a.find(find_value_after_condition).text
            if item != 'None':
                item_2 = a.find(find_value_if_not_none).text
                b.append(item_2)

    # Change of type from STR to FLOAT (xml has STR)
    b = list(map(float, b))

    # Sum of the values in the list - Note: '0.0' is start value for case that there is None returned like [] empty list
    b = sum(b, 0.0)

    return b


# ======= Charts ======

def create_pie_chart(df: pd.DataFrame, chart_names:str, chart_values: str, chart_title:str, drop: bool) -> Figure:

    # Drop rows with 0 costs to do not appear in the chart
    if drop == True:
        index = df[(df['Costs'] == 0)].index
        df.drop(index, inplace=True)

    fig_pie = px.pie(
        df, 
        names = chart_names,
        values = chart_values,
        title = chart_title
        )
    
    # To see 2 decimals always in the chart
    fig_pie.update_traces(texttemplate="%{percent:.2%}")

    return fig_pie


def create_bar_chart(df: pd.DataFrame, x_values:str | list, y_values:str | list, title: str) -> Figure:

    fig_bar = px.bar(
        df, 
        x= x_values,
        y= y_values,
        title= title,
        )

    return fig_bar

# ======= DF styling ======

def df_styling(df: pd.DataFrame) -> Styler:

    '''
    - Formating of decimals 
    - Function unified for mutliple DFs with different column names
    - Principle 
        - dictionary of columns
        - df -> if any column name in this dictionary -> apply predefined format
        - df -> if no column in this list, continue
    '''

    decimals = "{:,.2f}"

    formats = {
        "Price": decimals,
        "Additional service price": decimals,
        "sum price": decimals,
        "% ratio": decimals,
        "sum add. services": decimals,
        "sum price + add. services": decimals,
        "average price": decimals,
        "average price WITH add. services": decimals,
        "Δ delta": decimals,
        "sum": decimals,
        "average" : decimals
    }

    new_formats = {}

    # For loop to keep only existing columns
    for k, v in formats.items():
        if k in df.columns:
            new_formats[k] = v
  
    return df.style.format(new_formats)


# ======= Warnign multiselect ======
def display_warning_multiselect():

    st.warning("Select at lease 1 category to see overview table and charts")