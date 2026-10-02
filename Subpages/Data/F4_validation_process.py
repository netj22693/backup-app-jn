
STATE_TEXT = {
    "time_sleep": 1.4,
    "schema_validation": {   
            "spinner": "Schema Validation",
            "success":"**[✓]** - Schema Validation",
            "fail": "**[X]** - Schema Validation - the uploaded file doesn't correspond to the predefined format"
    },
    "canonical_transformation":{
            "spinner": "Canonical Transformation",
            "success":"**[✓]** - Canonical Transformation",
            "fail": "**[X]** - Canonical Transformation"
    },        
    "db_integrity_check":{ 
            "spinner": "Data Integrity Check",
            "success":"**[✓]** - Data Integrity Check",
            "fail": "**[X]** - Data Integrity Check - uploaded file has different data than saved in DB"
    },  
    "db_order_number":{
            "spinner": "Order number Check",
            "success":"**[✓]** - Data Integrity Check",
            "fail": "**[X]** - Data Integrity Check - not existing Order number in DB"
    },  
    "button":{
           "spinner": "Preparing buttons for download",
           "fail": "**[X]** - Technical issue - Process not complete.", 
           "time_sleep": 2
    }
}