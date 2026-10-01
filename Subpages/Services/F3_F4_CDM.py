import logging
import pandas as pd
import xml.etree.ElementTree as ET
import json
import numpy as np
from app_logging import inicialization_logging



# ===== Inicialization for logging ===== 
inicialization_logging()

def get_value(source: str, config: dict, data_type: type, data: str | dict | pd.DataFrame):

    if source == "XML":
        root = ET.fromstring(data)
        item = root.find(config).text

    elif source == "JSON":
        item = data
        for key in config:
            item = item[key]

    elif source == "DB":
        item = data[config].iloc[0]

    elif source == "CSV":
        item = data[config]

    return data_type(item)


def transform_data_to_CDM(data: str | dict | pd.DataFrame | list, source: str, FIELDS: dict) -> dict:

    parsed_data = {}

    try: 
        for field, config in FIELDS.items():

            parsed_data[field] = get_value(
                source,
                config[source],
                config["type"],
                data
            )


        logging.info(f"F4 - Transform data to CDM (was: {source}) - SUCCESS")
        return parsed_data

    # Except logic validation created for CSV
    # JSON and XML has schema validation
    except (ValueError, TypeError):
        logging.warning(f"F4 - Transform data to CDM: (was: {source}) - FAIL - ValueError/TypeError")
        return False

    except Exception as e:
        logging.warning(f"F4 - Transform data to CDM: (was: {source}) - FAIL - Exception: {e}")
        return False


def transform_data_CDM_to_CSV(function_id: str, cdm: dict) -> str:

    try: 
        list_values = []

        for value in cdm.values():
            list_values.append(str(value))  

        result = ",".join(list_values)

        logging.info(f"{function_id} - Transform data from CDM to CSV - SUCCESS")
        return result

    except Exception as e:
        logging.warning(f"{function_id} - Transform data from CDM to CSV - FAIL - Exception: {e}")



def get_or_create(parent: str, tag: str):

    element = parent.find(tag)

    if element is None:
        element = ET.SubElement(parent, tag)

    return element

  
def transform_data_CDM_to_XML(function_id: str, cdm: dict, FIELDS: dict) -> str:

    '''
    - XML Builder
    - Returns: XML as str/text
    '''

    try:
        root = ET.Element("invoice")

        for field, config in FIELDS.items():

            path = config["XML"]
            elements = path.split("/")

            current = root

            for element_name in elements:
                current = get_or_create(current, element_name)

            # Note: to have 2 decimal places in the XML
            if config["type"] == float:
                current.text = str(f"{cdm[field]:.2f}")
            else:
                current.text = str(cdm[field])

        # Pretty print
        ET.indent(root, space="   ")
            
        result =  ET.tostring(root, encoding="unicode", xml_declaration=True)

        logging.info(f"{function_id} - Transform data from CDM to XML - SUCCESS")

        return result

    except Exception as e:
        logging.warning(f"{function_id} - Transform data from CDM to XML - FAIL - Exception: {e}")



def transform_data_CDM_to_JSON(function_id: str, cdm: dict, FIELDS: dict) -> dict:

    '''
    - JSON Builder

    - Principle:
        - path is taken from config file -> tuple. E.g.('header', 'price', 'total_sum')
        - nested for loop 'key in path[:-1]' -> iterate throught the tuple except the last item. E.g. 2 iterations ('header', 'price')
            - if key not in current -> create new as empty object -> key : {}
            - if key in current -> do not create anything
        - 'current = current[key]' -> take the existing structure related to the key
        - when iteration is complete 'for key in path[:-1]' -> use the existing structure which is currently under the 'current' variable and append value -> 'current[path[-1]] = value' -> e.g. 'total_sum' : 1000
    
    'path' - ('header', 'price', 'total_sum')
    'value' - value from cdm to be appended to the key
    'data' - main dictionary which is fullfiled using mutable principle of 'current' pointing to the same dictionary
    'current' - is used to navigate trough the existing structure and take the "existing state" of structure based on LOOP 1: cdm field and nested LOOP 2: key in the JSON path -> to build the structure 

    current = data
    ↓
    current = data["header"]
    ↓
    current = data["header"]["price"]
    '''

    try:
        data = {}

        for field, config in FIELDS.items():

            path = config["JSON"]
            value = cdm[field]

            # 'current' and 'data' reference the same mutable dict. Mutations through 'current' therefore modify 'data'
            current = data

            # Do not forget: the path is list of values the loop needs to go through -> movement deeper in the dict/JSON nesting ('header', 'price', 'total_sum') -> 1 header, 2 price -> header/price 
            for key in path[:-1]:
                if key not in current:
                    current[key] = {}

                current = current[key]

            # header/price/total_sum : 1000
            current[path[-1]] = value

        result = json.dumps(data, indent=4) 
    
        logging.info(f"{function_id} - Transform data from CDM to JSON - SUCCESS")
    
        return result

    except Exception as e:
        logging.warning(f"{function_id} - Transform data from CDM to JSON - FAIL - Exception: {e}")


def transform_data_CDM_to_DB(function_id: str, cdm: dict, MAPPING_FUNCTIONS, CDM_FIELDS: dict) -> str:

    # Step 1: Mapping of values based on DB lookup tables (still within CDM structure)
    try:
        for field, mapping_function in MAPPING_FUNCTIONS.items():          
            cdm[field] = mapping_function(cdm[field])

        logging.info(f"{function_id} - Transform data from CDM to DB 1/3: Mapping - SUCCESS")

    except Exception as e:
        logging.warning(f"{function_id} - Transform data from CDM to DB 1/3: Mapping - FAIL - Exception: {e}")
        return

    # Step 2: Replace CDM keys by DB "keys" (column names)
    try:
        for key, config in CDM_FIELDS.items():
            db_field_name = config["DB"]
            cdm[db_field_name] = cdm.pop(key)


        logging.info(f"{function_id} - Transform data from CDM to DB 2/3: Dict for DB - SUCCESS")

    except Exception as e:
        logging.warning(f"{function_id} - Transform data from CDM to DB 2/3: Dict for DB - FAIL - Exception: {e}")
        return

    # Step 3: Convert NumPy types to native Python types
    # Note: This is standard SQLAlchemy/ORM "issue". (psycopg2.errors.InvalidSchemaName) schema "np" does not exist
    try:
        for key, value in cdm.items():
            if isinstance(value, np.generic):
                cdm[key] = value.item()

        logging.info(
            f"{function_id} - Transform data from CDM to DB 3/3: Type normalization - SUCCESS"
        )

    except Exception as e:
        logging.warning(
            f"{function_id} - Transform data from CDM to DB 3/3: Type normalization - FAIL - Exception: {e}"
        )
        return

    return cdm