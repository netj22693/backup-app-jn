from lxml import etree
import logging
from app_logging import inicialization_logging

# ===== Inicialization for logging =====
inicialization_logging()


def validate_xml_against_xsd(function_id: str, xml: str, xsd_path: str) -> bool:

    #try-except - for case when uploaded file is RECOGNIZED as XML (has suffix .xml) but the content is NOT XML.
    try:
        xmlschema_doc = etree.parse(xsd_path)
        xmlschema = etree.XMLSchema(xmlschema_doc)

        xml_doc = etree.parse(xml)
        result = xmlschema.validate(xml_doc)

        # If validation passes -> F2 logic can continue 
        if result == True:
            logging.info(f"{function_id} - XML validation XSD - SUCCESS")
            return True

        else:
            logging.warning(f"{function_id} - XML validation XSD - FAIL - XML does not match XSD")
            return False

    except Exception as e:
        logging.warning(f"{function_id} - XML validation XSD - FAIL - Exception: {e}")
        return False
