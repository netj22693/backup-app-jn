import logging

# ===== Inicialization for logging ===== 
def inicialization_logging():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )

# Rules
'''

Logging conventions
-------------------

Naming convention:
    F<Function> - <Operation> - <STATE> - <Reason / Exception>

Key states:
    SUCCESS / FAIL

Use logging for:
    - API operations
    - Database operations
    - Try/Except blocks
    - Validations
    - Operations that may affect function behavior
    - Important process milestones
    - Else blocks used to detect unexpected or undefined conditions


• Happy path
    F3 - DB insert - SUCCESS
    F2 - XML validation XSD - SUCCESS


• Unhappy path
    F3 - DB insert - FAIL: {e}
    F2 - XML validation XSD - FAIL - XML does not match XSD
    F2 - XML validation XSD - FAIL - Exception: {e}


• API operations   API: <api_name>
    F6 - API: zipcodebase.com - SUCCESS


• Else blocks / unexpected conditions
    F3 - Operational function: get_utc_time_custom_string() - FAIL - Invalid input
    F7 - Operational function: get_calculation_price_distance() - FAIL - Undefined condition


• Operations that may affect Function behavior
    F6 - Remove diacritics - FAIL - Exception: {e}
    F6 - Validation of missing ZIP codes - SUCCESS
'''



