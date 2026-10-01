from Subpages.Data.F3_F4_CDM_config_data import CONFIG_MAPPING_ADDITIONAL_SERVICES_DB

class F3MappingFunctions:

    def mapping_country_to_table(country: str) -> str:

        mapping = {
            "Czech Republic": "country_cz",
            "Slovakia": "country_sk",
        }

        return mapping.get(country) 


    def mapping_category(category: str) -> int:

        mapping = {
            "PC" : 1,
            "TV" : 2,
            "Gaming" : 3,
            "Mobile phones" : 4,
            "Tablets" : 5,
            "Major Appliances" : 6,
            "Households" : 7
        }
        return mapping.get(category) 


    def mapping_extra_service_id(service: str) -> int:
        return CONFIG_MAPPING_ADDITIONAL_SERVICES_DB.get(service)


    def mapping_extra_service_boolean(service: str) -> bool:

        id =  CONFIG_MAPPING_ADDITIONAL_SERVICES_DB.get(service)

        print("tady more", id)
        print(service)

        if id != 1:
            return True
        else:
            return False



    def mapping_country(country: str) -> int:

        mapping = {
            "Czech Republic" : 1,
            "Slovakia" : 2
        }
        return mapping.get(country) 


    def mapping_transport_company(company: str) -> int:

        mapping = {
            "DHL" : 1,
            "Fedex" : 2
        }
        return mapping.get(company) 


    def mapping_size(size: str) -> str:

        mapping = {
            "small" : "s",
            "medium" : "m",
            "large" : "l",
        }
        return mapping.get(size) 

    def mapping_currency(currency: str) -> int:

        mapping = {
            "euro" : 1,
            "US dollar" : 2,
            "Kč" : 3,
        }
        return mapping.get(currency) 


    def mapping_file_format(format: str) -> int:

        mapping = {
            "XML" : 1,
            "JSON" : 2,
            "CSV": 3
        }
        return mapping.get(format) 

    
    def mapping_currency_for_query(currency: str) -> str:

        mapping = {
            "euro": "euro",
            "US dollar": "us_dollar",
            "Kč": "koruna"
        }

        return mapping.get(currency) 

    def mapping_additional_service_into_field(service_name: str) -> str:
    
        if service_name == 'No additional service':
            return 'N'

        else:
            return 'Y'


# Note: this mapping is based on CDM names/keys. This happens before mapping CDM to DB dict
MAPPING_FUNCTIONS = {
    "category": F3MappingFunctions.mapping_category,
    "extra_service": F3MappingFunctions.mapping_extra_service_boolean,
    "service_type": F3MappingFunctions.mapping_extra_service_id,
    "country": F3MappingFunctions.mapping_country,
    "transporter": F3MappingFunctions.mapping_transport_company,
    "size": F3MappingFunctions.mapping_size,
    "currency": F3MappingFunctions.mapping_currency,
}
