import logging

# ===== Inicialization for logging ===== 
def inicialization_logging():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )

# Rules
'''
Logging rules:
- Naming convention: Fx - Operation name - STATE - Reason/ Exception: {e}
- Key states: SUCCESS / FAIL
- Where to use:
    - API,
    - DB,
    - Try/Except blocks,
    - Validations,
    - Operations which can inpact the Function behavior,
    - Important process milestones, else blocks where 
    - else blocks to catch potential undefined/missed condition

• Happy path 
F3 - DB insert - SUCCESS
F2 - XML validation XSD - PASSED"


• Unhappy path
F3 - DB insert - FAIL: {e}
F2 - XML validation XSD - NOT PASSED - XML does not match XSD"
F2 - XML validation XSD - NOT PASSED - Exception: {e}"

• API operations  API: name
F6 - Parsing API: zipcodebase.com - SUCCESS"

• Else blocks to catch potential undefined/missed condition
F3 - operational function: get_utc_time_custom_string() - Invalid input
F7 - operational function: get_calculation_price_distance() - Undefined condition

• Operations which can inpact the Function behavior
F6 - Remove diacritics - FAIL: {e}
F6 - Validation of missing ZIP codes - SUCCESS
'''



