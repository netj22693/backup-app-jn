from typing import Optional
import logging
from app_logging import inicialization_logging


# ===== Inicialization for logging =====
inicialization_logging()


# ===== Parsing functions =====
def parsing_data_api_kurzy_cz(data_input: str) -> Optional[float | None]:

    try:
        eur_rate= round(data_input['kurzy']['EUR']['dev_stred'], 3)
        usd_rate = round(data_input['kurzy']['USD']['dev_stred'], 3)

        logging.info(f"F5 - Parsing API - kurzy.cz - SUCCESS")

        return eur_rate, usd_rate

    except Exception as e:
        logging.error(f"F5 - Error data parsing API - kurzy.cz: {e}")
        return None, None


def parsing_data_api_freecurrencyapi_com(data_input: str) -> Optional[float | None]:

    try:
        eur_to_usd = round(data_input['data']['USD'], 3)

        logging.info(f"F5 - Parsing API - freecurrencyapi.com - SUCCESS")

        return eur_to_usd

    except Exception as e:
        logging.error(f"F5 - Error data parsing API - freecurrencyapi.com: {e}")
        return None


# =================== Calculating functions ===================

def get_result_division(a: float,b: float) -> float:
    return a / b
    
def get_result_multiply(a: float,b: float) -> float:
    return a * b

# =================== Formatting for UI ===================

def get_value_formated(input: float) -> str:
    return f"{input:,.2f}". replace(",", " ")
