from typing import BinaryIO
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element


def get_xml_root(xml: BinaryIO):
    tree = ET.parse(xml)
    return tree.getroot()


def xml_data_parsing_find(
        root: Element,
        findall_value: str,
        find_value: str,
        to_float: bool,
        to_list: bool
        ) -> str | float | list:

    '''
    - Parsing mechanism extracting values from XML element

    - Outcomes:
        - L1 - list[float]
        - L2 - list[str]
        - L3 - value: float
        - L4 - value: str 

    - List - when element multiple times in the structure
    - Value - when element once in the structure
    '''

    c = []
    for a in root.findall(findall_value):
        b = a.find(find_value).text
        c.append(b)

    if to_list:
        if to_float:
            return list(map(float, c))   #L1

        else:
            return c   #L2


    elif not to_list:
        value = c[0]

        if to_float:
            return float(value)   #L3
        
        else:
            return value   #L4


def xml_data_parsing_find_conditional(
        root: Element,
        findall_value: str,
        find_value: str,
        condition_type: str,
        find_value_after_condition: str,
        to_float: bool
        ) -> list:

    '''
    - Parsing mechanism extracting values from XML element
    - Using condition for appending

    - Outcomes:
        - L1 - list[float]
        - L2 - list[str]
    '''

    c = []
    for a in root.findall(findall_value):
        condition = a.find(find_value).text

        if condition == condition_type:
            b = a.find(find_value_after_condition).text
            c.append(b)

    if to_float:
        return list(map(float, c))   #L1
    
    else:
        return c   #L2


def xml_data_parsing_get(root: Element, findall_value: str, get_value: str) -> list:

    '''
    - Parsing mechanism for XML ATTRIBUTES   
    '''

    c = []
    for a in root.findall(findall_value):
        b = a.get(get_value)
        c.append(b)

    return c