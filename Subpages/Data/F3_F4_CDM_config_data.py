from Subpages.Services.F3_F4_CDM import transform_data_CDM_to_CSV, transform_data_CDM_to_JSON, transform_data_CDM_to_XML


# ===== Mapping to & from CDM - CONFIG file =====
CDM_FIELDS = {

    "order_number": {
        "type": int,
        "CSV": 0,
        "DB": "order_number",
        "JSON": ("header", "order_number"),
        "XML": "header/order_number",
    },

    "customer": {
        "type": str, 
        "CSV": 1,
        "DB": "customer",
        "JSON": ("header", "customer"),
        "XML": "header/customer",
    },

    "invoice_number": {
        "type": str, 
        "CSV": 2,
        "DB": "invoice_number",  # Tady budu muset invoice number začít ukládat do DB (rozšířit ERD)
        "JSON": ("header", "invoice_number"),
        "XML": "header/invoice_number",
    },

    "date": {
        "type": str, 
        "CSV": 3,
        "DB": "date",
        "JSON": ("header", "date"),
        "XML": "header/date",
    },

    "total_sum": {
        "type": float, 
        "CSV": 4,
        "DB": "total_sum",  # jmenuje se to v DB teď total_price -> přerefaktorovat total_sum
        "JSON": ("header", "price", "total_sum"),
        "XML": "header/price/total_sum",
    },  

    "currency": {
        "type": str, 
        "CSV": 5,
        "DB": "currency",  # tady to vytáhnu přes join, ať nemusím mapovat (v DB je INT)
        "JSON": ("header", "price", "currency"),
        "XML": "header/price/currency",
    },

    "category": {
        "type": str, 
        "CSV": 6,
        "DB": "category",  # tady to vytáhnu přes join, ať nemusím mapovat (v DB je INT)
        "JSON": ("detail", "category"),
        "XML": "detail/category",
    },

    "product_name": {
        "type": str, 
        "CSV": 7,
        "DB": "product_name",
        "JSON": ("detail", "product_name"),
        "XML": "detail/product_name",
    },

    "price_amount": {
        "type": float, 
        "CSV": 8,
        "DB": "product_price",
        "JSON": ("detail", "price_amount"),
        "XML": "detail/price_amount",
    },

    "extra_service": {
        "type": str, 
        "CSV": 9,
        "DB": "extra_service",  # tady to vytáhnu přes CASE, TRUE == Y, FALSE == N, ať nemusím mapovat
        "JSON": ("detail", "additional_service", "service"),
        "XML": "detail/additional_service/service",
    },

    "service_type": {
        "type": str, 
        "CSV": 10,
        "DB": "extra_service_type",  # tady to vytáhnu přes JOIN, ať nemusím mapovat
        "JSON": ("detail", "additional_service", "service_type"),
        "XML": "detail/additional_service/service_type",
    },

    "service_price": {
        "type": float, 
        "CSV": 11,
        "DB": "extra_service_price",
        "JSON": ("detail", "additional_service", "service_price"),
        "XML": "detail/additional_service/service_price",
    },

    "transporter": {
        "type": str, 
        "CSV": 12,
        "DB": "transport_company",  # jmenuje se to v DB teď tr_company -> přerefaktorovat transport_compancy + JOIN, ať nemusím mapovat
        "JSON": ("transportation", "transporter"),
        "XML": "transportation/transporter",
    },

    "country": {
        "type": str, 
        "CSV": 13,
        "DB": "country",  # JOIN, ať nemusím mapovat
        "JSON": ("transportation", "country"),
        "XML": "transportation/country",
    },

    "size": {
        "type": str, 
        "CSV": 14,
        "DB": "parcel_size",  # použiju CASE, jako mapping v SQL
        "JSON": ("transportation", "size"),
        "XML": "transportation/size",
    },

    "transport_price": {
        "type": float, 
        "CSV": 15,
        "DB": "transport_price",  # jmenuje se to v DB teď tr_price -> přerefaktorovat transport_price
        "JSON": ("transportation", "transport_price"),
        "XML": "transportation/transport_price",
    },
}



MAPPING_MATRIX = {
    "CSV": ["JSON","XML"],
    "JSON": ["CSV","XML"],
    "XML": ["CSV","JSON"],
}

LOGIC_CONFIG = {
    "CSV": {
        "function": transform_data_CDM_to_CSV,
        "mapping_to_suffix": ".csv"
    },
    "XML": {
        "function": transform_data_CDM_to_XML,
        "mapping_to_suffix": ".xml"
    },
    "JSON": {
        "function": transform_data_CDM_to_JSON,
        "mapping_to_suffix": ".json"
    }
}

# (!) Important note - for the mapping is used 'mapping_label' names, can be seen in 'extra_service_list' table in DB
CONFIG_MAPPING_ADDITIONAL_SERVICES_DB = {
    "None" : 1,
    "insurance" : 2,
    "extended warranty" : 3
}