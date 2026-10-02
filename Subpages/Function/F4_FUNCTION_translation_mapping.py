import streamlit as st
import csv
import json
import time
import logging
import pandas as pd
from decimal import Decimal
from sqlalchemy import text
from io import StringIO
from pathlib import Path
from app_db_connection import db_connection
from app_logging import inicialization_logging
from Subpages.Data.F4_validation_process import STATE_TEXT
from Subpages.SQL.F4_SQL_queries import sql_query_data_integrity
from Subpages.Operational.F4_operational_functions import insert_log_into_db_orchestration
from Subpages.Data.F3_F4_CDM_config_data import CDM_FIELDS, LOGIC_CONFIG, MAPPING_MATRIX
from Subpages.Universal.Validation_JSON_against_JSON_Schema import validate_json_against_schema
from Subpages.Universal.Validation_XML_against_XML_Schema import validate_xml_against_xsd
from Subpages.Services.F3_F4_CDM import transform_data_to_CDM

# ===== Inicialization for logging ===== 
inicialization_logging()


# ===== Session state -> to remove uploaded file when Download button ===== 
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

# ===== Orchestration & UI ===== 
st.write("# Data Transformation")


# DB connection
db_engine = db_connection("F4", True)

# UI
''
st.write("##### Upload File:")


uploaded_file = st.file_uploader(
    "Upload file",
    label_visibility="collapsed",
    type=[".csv",".json",".xml"],
    accept_multiple_files=False,
    key=f"uploader_{st.session_state.uploader_key}"
    )

''


if uploaded_file is None:
    st.info("Upload the file you want to transform.")

    # Tady bych mohl přidat tabulku posledních 10 Transformacích něco jako v LCL Sailings
        

elif uploaded_file is not None:

    suffix = Path(uploaded_file.name).suffix.upper().lstrip(".")

    if suffix == "XML":

        validation_result = validate_xml_against_xsd(
            "F4",
            uploaded_file,
            Path(__file__).resolve().parent / "/workspaces/backup-app-jn/Subpages/Data/F3_F4_XML_Schema_v1.xsd"
            )

        with st.spinner(STATE_TEXT["schema_validation"]["spinner"]):
            time.sleep(STATE_TEXT["time_sleep"])
    
        if validation_result == False:
            st.warning(STATE_TEXT["schema_validation"]["fail"])
            st.stop()

        st.success(STATE_TEXT["schema_validation"]["success"])


        cdm_format: dict = transform_data_to_CDM(
            # .getvalue() -> changing format from UploadedFelie to bytes. If this step is not present -> TypeError: a bytes-like object is required, not 'UploadedFile'
            uploaded_file.getvalue(),
            suffix,
            CDM_FIELDS
            )

        with st.spinner(STATE_TEXT["canonical_transformation"]["spinner"]):
            time.sleep(STATE_TEXT["time_sleep"])

        if cdm_format == False:
            st.warning(STATE_TEXT["canonical_transformation"]["fail"])
            st.stop()

        st.success(STATE_TEXT["canonical_transformation"]["success"])


    elif suffix == "JSON":

        data_json = json.load(uploaded_file, parse_float=Decimal)

        with st.spinner(STATE_TEXT["schema_validation"]["spinner"]):
            time.sleep(STATE_TEXT["time_sleep"])

        validation_result = validate_json_against_schema(
            "F4",
            data_json,
            "/workspaces/backup-app-jn/Subpages/Data/F3_F4_JSON_Schema_v1.json"
        )

        if validation_result == False:
            st.warning(STATE_TEXT["schema_validation"]["fail"])
            st.stop()

        st.success(STATE_TEXT["schema_validation"]["success"])

        cdm_format: dict = transform_data_to_CDM(
            data_json,
            suffix,
            CDM_FIELDS
            )

        with st.spinner(STATE_TEXT["canonical_transformation"]["spinner"]):
            time.sleep(STATE_TEXT["time_sleep"])

        if cdm_format == False:
            st.warning(STATE_TEXT["canonical_transformation"]["fail"])
            st.stop()

        st.success(STATE_TEXT["canonical_transformation"]["success"])


    elif suffix == "CSV":

        csv_string = uploaded_file.getvalue().decode("utf-8")
        reader = csv.reader(StringIO(csv_string))
        parsed_list = next(reader)

        cdm_format: dict = transform_data_to_CDM(
            parsed_list,
            suffix,
            CDM_FIELDS
            )

        with st.spinner(STATE_TEXT["canonical_transformation"]["spinner"]):
            time.sleep(STATE_TEXT["time_sleep"])

        if len(parsed_list) != len(CDM_FIELDS):
            st.warning("**[X]** - Canonical Transformation - different number of fields")
            st.stop()

        if cdm_format == False:
            st.warning("**[X]** - Canonical Transformation - data fields doesn't correspond with predefined format")
            st.stop()

        st.success(STATE_TEXT["canonical_transformation"]["success"])



    # ===== DB - Data Integrity Check =====
    with db_engine.connect() as conn:
        data_db = pd.read_sql_query(
            sql=text(sql_query_data_integrity),
            con=conn,
            params= {"order_number": cdm_format["order_number"]}
            )

    with st.spinner(STATE_TEXT["db_integrity_check"]["spinner"]):
        time.sleep(STATE_TEXT["time_sleep"])

    if data_db.empty:
        st.warning(STATE_TEXT["db_order_number"]["fail"] + f": {cdm_format['order_number']}")
        st.stop()
       
    cdm_format_db: dict = transform_data_to_CDM(
        data_db,
        "DB",
        CDM_FIELDS
        )

    if cdm_format != cdm_format_db:
        st.warning(STATE_TEXT["db_integrity_check"]["fail"])
        st.stop()

    st.success(STATE_TEXT["db_integrity_check"]["success"])

    # Try/except statement in case that data preparation for download fails -> to catch this fallback on UI and create logs
    try:
        ''
        '' 
        with st.spinner(STATE_TEXT["button"]["spinner"]):
            time.sleep(STATE_TEXT["button"]["time_sleep"])

        matrix = MAPPING_MATRIX.get(suffix)

        for item in matrix:
            config = LOGIC_CONFIG[item]

            # Note: The function/transforms the data CDM to formats already here -> it is calling the function for mapping
            if item == "CSV":
                data = config["function"]("F4", cdm_format)
            else:
                data = config["function"]("F4", cdm_format, CDM_FIELDS)

            st.download_button(
                item,
                data,
                file_name=f"{cdm_format['invoice_number']}{config['mapping_to_suffix']}",
                use_container_width=True,
                icon=":material/download:",
                on_click=lambda item=item: (
                    insert_log_into_db_orchestration(
                        cdm_format["order_number"],
                        suffix,
                        item
                    ),
                    st.session_state.__setitem__(
                        "uploader_key",
                        st.session_state.uploader_key + 1
                    )
                )
            )

        logging.info("F4 - Creation download buttons - SUCCESS")

    except Exception as e:
        logging.warning(f"F4 - Creation download buttons - FAIL - Exception: {e}")
        st.warning(STATE_TEXT["button"]["fail"])
