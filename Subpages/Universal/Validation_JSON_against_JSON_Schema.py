import logging
import json
from decimal import Decimal
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from app_logging import inicialization_logging


# ===== Inicialization for logging ===== 
inicialization_logging()


def validate_json_against_schema(function_id: str, data_json: dict, schema_path: str):

    '''
    (!) Important note:
        - I use in JSON Schema "multipleOf": 0.01 condition -> 2 decimals maximum 
        - The classical python float issue can happen also when JSON is translated to python  -> 16094.999999999998
        - Fix: parse_float=Decimal -> needs to be used:
            1) json.load() schema - HERE in this FUNCTION
            2) json.load() the JSON message/file which is supposed to be validated

        - Example of log:
            2026-10-02 12:56:09,146 WARNING: F4 - JSON validation JSON Schema - FAIL - ValidationError: 160.95 is not a multiple of 0.01   
    '''

    with open(schema_path, "r", encoding="utf-8") as file:
        
        # 1) json.load() schema - HERE in this FUNCTION -> parse_float=Decimal
        schema = json.load(file, parse_float=Decimal)

    try:
        validate(instance=data_json, schema=schema)
        logging.info(f"{function_id} - JSON validation JSON Schema - SUCCESS")
        return True

    except ValidationError as e:
        logging.warning(f"{function_id} - JSON validation JSON Schema - FAIL - ValidationError: {e.message}")
        return False