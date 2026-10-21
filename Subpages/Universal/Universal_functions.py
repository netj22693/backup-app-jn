import pandas as pd
import logging
from app_logging import inicialization_logging


'''
Purpose of this .py file
- Simple generic functions which can be reused across Functions FX
- No specific Function/Business domain logic
'''

# ===== Inicialization for logging ===== 
inicialization_logging()


def singular_or_plural(input_value: int | float) -> str:
    """
    Used for determining if day/days, hour/hours, route/routes, etc.
    """
    if input_value == 1:
        return ""
    else:
        return "s"


def adjust_index_in_df(df: pd.DataFrame, operation: str = "PLUS", num: int = 1) -> pd.DataFrame:
    '''
    Moves DF indexes up/down based on parameters 'operation' and 'number'
    - PLUS +
    - MINUS - 

    E.g.: Index +1: 0, 1, 2 -> 1, 2, 3

    (!) Must be used befor df.styling
    '''

    if operation == "PLUS":
        df.index = df.index + num

    elif operation == "MINUS":
        df.index = df.index - num
    else:
        logging.warning("Universal function - adjust_index_in_df() - FAIL - Incorrect operation")

    return df