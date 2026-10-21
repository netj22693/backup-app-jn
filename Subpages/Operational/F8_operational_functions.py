import pandas as pd
from Subpages.Resources_ui_objects import render_warning_info

def determin_international(country_from: str, country_to: str) -> bool:
    '''
    - Function to determin if the transport will be from country to the same country or to the different country (international)
    - Result BOOLEAN used for SQL query build
    '''

    if country_from == country_to:
        return False

    else:
        return True


def input_validation(value) -> int | None:
    try:
        return int(value)
    
    except (TypeError, ValueError):
        render_warning_info("**Invalid format** - branch ID is a number.")
        return None


def boolean_to_string_for_ui(a: bool) -> str:

    '''
    - Function transfering boolean input into Yes/No text for UI purposes
    '''

    if a == True:
        return "Yes"
    
    else:
        return "No"


def count_rows(df: pd.DataFrame) -> int:

    return df["Name"].count()


def select_country_flag_path(country_code:str) -> str:

    '''
    - Returns image path based on country code
    '''

    mapping = {
            "AT": "Pictures/Function_8/F8_Country_flags/Flag_of_Austria_v3.svg",
            "CZ": "Pictures/Function_8/F8_Country_flags/Flag_of_the_Czech_Republic_v3.svg",
            "DE": "Pictures/Function_8/F8_Country_flags/Flag_of_Germany_v3.svg",
            "PL": "Pictures/Function_8/F8_Country_flags/Flag_of_Poland_v3.svg",
            "SK": "Pictures/Function_8/F8_Country_flags/Flag_of_Slovakia_v3.svg"
        }
    
    return mapping.get(country_code)

