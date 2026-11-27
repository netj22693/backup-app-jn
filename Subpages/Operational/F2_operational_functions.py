import streamlit as st
import time
import pandas as pd
import pandasql as ps
from pandas.io.formats.style import Styler
import plotly.express as px
from xml.etree.ElementTree import Element
from plotly.graph_objects import Figure
from Subpages.Resources_ui_objects import render_success_info, render_warning_info


# ======= SQL to DF ======
def run_sql_query_df(sql_query, df):

    '''
    - SQL to DF
    - Set specifically for F2 using data_table_sql created in F2 code/script
    '''

    result = ps.sqldf(sql_query, {"data_table_sql": df})
    return result


# ======= Data validation -> displays on UI ======
def data_validation(
        total_sum: float,
        sum_product_price: float,
        currency: str
        ) -> tuple[str, bool]:

    result = total_sum - sum_product_price
    
    if result != 0:

        TEXT = f"""
        Not Passed
        - **Total sum** in the XML invoice is: **{total_sum:.2f}** {currency}
        - But **summary of prices** in detail lines is: **{sum_product_price:.2f}** {currency}
        """

        render_warning_info(TEXT)

        # This string is NOT app state but str/text to appear in the .txt doc
        return "Sum total - Not passed ⚠︎", False


    else:
        render_success_info("Passed")

        # This string is NOT app state but str/text to appear in the .txt doc
        return "Sum total - Passed", True


def data_validation_services(
        total_sum_services: float,
        sum_services: float,
        currency: str
        ) -> tuple[str, bool]:

    result = total_sum_services - sum_services

   
    if result != 0:

        TEXT = f"""
        Not Passed
        - **Total sum SERVICES** in the XML invoice is: **{total_sum_services:.2f}** {currency}
        - But **summary of prices** in detail lines is **{sum_services:.2f}** {currency}."""

        render_warning_info(TEXT)
 
        # This string is NOT app state but str/text to appear in the .txt doc
        return ("Services - Not passed ⚠︎"), False

    else:
        render_success_info("Passed")

        # This string is NOT app state but str/text to appear in the .txt doc
        return "Services - Passed", True


# ======= Logic of F2 warning UI info ======

def get_warning_scenario(v1: bool, v2: bool) -> str:

    '''
    True = Validation passed
    False = Validation NOT passed
    ''' 

    if v1 == True and v2 == True:
        scenario = "NONE"

    elif v1 == True and v2 == False:
        scenario = "V2_ONLY"

    elif v1 == False and v2 == True:
        scenario = "V1_ONLY"
   
    elif v1 == False and v2 == False:
        scenario = "BOTH"

    return scenario


def display_warning_f2(
    scenario: str,
    expected_scenario: list[str],
    text_config: dict[str, str] | None = None
    ):


    if text_config is None:
        text_config = {}


    warning_text = {}

    if scenario in (expected_scenario):
        badge = f":orange-badge[:material/warning:]"
        result = True

        if text_config:
            for key, value in text_config.items():
                update = f":orange-badge[:material/warning: {value}]"
                warning_text[key] = update

    else:
        badge = ""
        result = False

    return badge, warning_text, result

# ======= Functions for parsing - SPECIFIC FOR FUNCTION 2 ======
'''
- These parsing functions are specifically tailored for needs of F2
- NOT to be reused anywhere else
'''


def f2_xml_data_parsing_find_including_additional_services(
        root: Element,
        findall_value: str,
        find_value: str,
        condition_type: str,
        find_value_after_condition: str,
        find_value_if_not_none: str
        ) -> float:

    '''
    - Parsing function specifically tailored for needs of F2
    - NOT to be reused anywhere else
    '''

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

def f2_xml_data_parsing_find_conditional_with_none_condition(
        root: Element,
        findall_value: str,
        find_value: str
        ) -> float:

    '''
    - Parsing function specifically tailored for needs of F2
    - NOT to be reused anywhere else
    '''

    c = []
    for a in root.findall(findall_value):
        condition = a.find(find_value).text

        # v5.3 - extended logic
        if condition in ['extended warranty','insurance']:
            b = a.find('additional_service/service_price').text
            c.append(b)
        
        # v5.3 - specifically this part is important to not parse value in case that <service_type> 'None' but <service_price> 999.99 (with value) -> this is the anti-pattern which this mechanism prevents -> 
        # if 'None' it ignors a value but always appends 0.00 to this list
        elif condition == 'None':
            c.append(0.00)
        
        # Note: XSD definition allows only the 'value' from upper conditions, if different, such XML should not pass validation to the parsing step at all
        else:
            print("Data parsing issue: This should have been stopped by XSD")

    return c


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
        "Sum price": decimals,
        "% ratio": decimals,
        "Sum add. services": decimals,
        "Sum price + add. services": decimals,
        "Avg product price": decimals,
        "Avg price WITH add. services": decimals,
        "Δ delta": decimals,
        "Sum": decimals,
        "Avg" : decimals
    }

    new_formats = {}

    # For loop to keep only existing columns
    for k, v in formats.items():
        if k in df.columns:
            new_formats[k] = v
  
    return df.style.format(new_formats)


# ======= UTC time ======
def get_utc_time_custom_string() -> str:

    utc = time.gmtime()

    year = utc.tm_year
    month = utc.tm_mon
    day = utc.tm_mday
    hour = utc.tm_hour
    minute = utc.tm_min
    second = utc.tm_sec  
    weekday = utc.tm_wday

    date_custom = str("Date: %02d-%02d-%04d" % (day,month,year))
    time_custom = str("Time: %02d:%02d:%02d" % (hour,minute,second))
    day_custom = str(("Mon","Tue","Wed","Thu","Fri","Sat","Sun") [weekday])
    day_custom_2 = str("Day: "+ day_custom)
    
    return str(date_custom +" | " + day_custom_2 +" | " + time_custom + " UTC")

