
class F3InputDataQueries:
    sql_query_category_options = """
    SELECT name
    FROM billing.category_list
    ORDER by name
    """

    sql_query_transport_company_options = """
    SELECT name
    FROM shared.transport_company
    ORDER by name
    """

    sql_query_currency_options = """
    SELECT name
    FROM billing.currency_list
    ORDER by name
    """

    sql_query_additional_service_options = """
    SELECT name
    FROM billing.extra_service_list
    """

    sql_query_country_options = """
    SELECT name
    FROM billing.country_list
    ORDER by name
    """

    sql_query_parcel_size_options = """
    SELECT name
    FROM shared.parcel_size f
    ORDER BY 
      CASE 
        WHEN f.name = 'small' THEN 1
        WHEN f.name = 'medium' THEN 2
        WHEN f.name = 'large' THEN 3
      END 
    """ 

    sql_query_additional_service_table = """
    SELECT *
    FROM billing.extra_service_list
    """ 


query_currency_max_values = """
SELECT 
    name, 
    max_value
FROM billing.currency_list
"""

sql_query_parcel_size = """
SELECT 
  f.name as "Parcel size",
  f.description as "Description"
  
FROM shared.parcel_size f
  
ORDER BY 
  CASE 
    WHEN f.name = 'small' THEN 1
    WHEN f.name = 'medium' THEN 2
    WHEN f.name = 'large' THEN 3
  END 
"""

query_additional_service_price_info = """
SELECT
    name as "Service", 
    description as "Costs",
    service_description,
    icon

FROM billing.extra_service_list

WHERE
    -- option "No additional service" excluded
    service_id != 1

ORDER BY
    name ASC
"""

