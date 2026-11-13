import pandas as pd
from Subpages.Resources_ui_objects import render_info_info

def validate_criteria_not_in_final_result(df: pd.DataFrame, selected_data: dict, config: dict):

    '''
    - Semi-universal function
    - Applicable for F3B & F7B TAB3 (and will be used in the future adjustment of TAB4 in the Functions)
    - Compares data pulled from DB (DF) and data selected on UI (multiselects) -> displays what is not in the range of result -> UI overview for user
    
    (!) naming convention
    ---------------------
    - config file CONFIG_VALIDATE_CRITERIA_<function_id>_TAB<tab_number>
    - e.g.: CONFIG_VALIDATE_CRITERIA_F7B_TAB3

    - config file to be imported from Data Subfolder

    
    (!) config dict structure
    ---------------------
    "country_from":{
        "df_column":"Country from",
        "selected_data_column": "country_from",
        "ui_text": "Country from",
        "always_available": False
        },

    - df_column - name of column in DF passed into this function
    - selected_data_column - name of config file which has saved the values from UI filters
    - ui_text - part of string to be displayed in the overall notification to the user on UI -> outcome of this function
    - always_available - if the multiselect filter is not set as default (hidden under checkbox)
    '''

    show_info = False

    # Important note: create a new dict. Do not adjust the config one
    # Keep config only as config, not touch
    # Troubleshooting 08-Nov-2026
    missing_values = {}

    for key, value in config.items():
        df_values = set(df[value["df_column"]].drop_duplicates())

        multiselect = selected_data["multiselect"]
        selected_column = value["selected_data_column"]

        if selected_column not in multiselect:
            if value["always_available"]:
                raise KeyError(f"UI filter '{selected_column}' is missing from selected_data.")
            
            continue

        selected_data_values = multiselect[selected_column]

        for item in selected_data_values:
            if item not in df_values:
                missing_values.setdefault(key, {}).setdefault("missing", []).append(item)
                show_info = True


    ui_text_build ="The following selected values **are not covered** by the **current range of results**.\n"

    for key, value in missing_values.items():
        missing = value["missing"]
        missing.sort()
        missing_str = ", ".join(missing)

        ui_text = config[key]["ui_text"]
        line = f"- **{ui_text}**: {missing_str}\n"

        ui_text_build += line


    if show_info:
        render_info_info(ui_text_build)