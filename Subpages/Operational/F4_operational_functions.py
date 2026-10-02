import logging
from app_logging import inicialization_logging
from app_db_connection import db_connection
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Session
from Subpages.Dialog.F4_dialog import process_done, insert_db_not_complete
from Subpages.Operational.F3_operational_functions import get_utc_time_custom_string
from Subpages.Services.F3_DB_mapping import F3MappingFunctions

# ===== Inicialization for logging =====
inicialization_logging()

# ==== Functions related to DB =====

# Data for DB insert
def create_data_for_log(order_number: str, format_from_mapped: int, format_to_mapped: int) -> dict:
	
    data = {
        "date": get_utc_time_custom_string("F4","change_log"),   
        "order_number_log": order_number,
        "change": "mapping",
		"mapping_from": format_from_mapped,
		"mapping_to" : format_to_mapped
	}
    
    return data

# Insert into DB
def insert_log_into_db(data: dict):
	
    Base = declarative_base()

    class Change_log(Base):
        __tablename__ = "change_log"
        __table_args__ = {"schema": "billing"}

        log_id = Column(Integer, primary_key=True)
        date = Column(String)
        order_number_log = Column(String)
        change = Column(String)
        mapping_from = Column(String)
        mapping_to = Column(String)
	
    db_engine = db_connection("F4", False)

    try:
        with Session(db_engine) as session:
            new_invoice = Change_log(**data)
            session.add(new_invoice)
            session.commit()

        logging.info(f"F4 - DB Insert - SUCCESS")
        process_done()

    except Exception as e:
        logging.warning(f"F4 - DB Insert - FAIL - Exception: {e}")
        insert_db_not_complete()


def insert_log_into_db_orchestration(order_number: int, format_from: str, format_to: str):

    format_from_mapped = F3MappingFunctions.mapping_file_format(format_from)
    format_to_mapped = F3MappingFunctions.mapping_file_format(format_to)

    data = create_data_for_log(order_number, format_from_mapped, format_to_mapped)

    insert_log_into_db(data)