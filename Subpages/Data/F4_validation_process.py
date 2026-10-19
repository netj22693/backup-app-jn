# Note: the text is displayed using wrapper with relevant icon set in the wrapper
STATE_TEXT = {
    "time_sleep": 1.4,
    "schema_validation": {   
            "spinner": "Schema Validation",
            "success":"Schema Validation",
            "fail": "Schema Validation - the uploaded file does not correspond to the predefined format."
    },
    "canonical_transformation":{
            "spinner": "Canonical Transformation",
            "success":"Canonical Transformation",
            "fail": "Canonical Transformation",

            # Specific fails CSV
            "fail_csv_len": "Canonical Transformation - different number of fields.",
            "fail_csv_data": "Canonical Transformation - data fields do not correspond with predefined format.",

    },        
    "db_integrity_check":{ 
            "spinner": "Data Integrity Check",
            "success":"Data Integrity Check",
            "fail": "Data Integrity Check - uploaded file has different data than saved in DB."
    },  
    "db_order_number":{
            "spinner": "Order number Check",
            "success":"Data Integrity Check",
            "fail": "Data Integrity Check - not existing order number in DB" # No dot '.' at the end of the sentense. It is in the code when string is built.
    },  
    "button":{
           "spinner": "Preparing buttons for download",
           "fail": "Technical issue - process not complete.", 
           "time_sleep": 2
    }
}