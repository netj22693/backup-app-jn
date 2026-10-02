
sql_query_data_integrity = """
SELECT 
  a.order_number,
  a.customer,
  a.invoice_number,
  a.date,
  a.total_sum,
  g.name as "currency",
  b.name as "category",
  a.product_name,
  a.product_price,

  CASE
    WHEN c.service_id = 1 THEN 'N'
    ELSE 'Y'
    END as "extra_service", 

  c.mapping_label as "extra_service_type",
  a.extra_service_price,
  e.name as "transport_company",  
  d.name as "country",
  f.name as "parcel_size",
  a.transport_price
                                    

FROM billing.invoice a
  INNER JOIN billing.category_list b ON (a.category = b.category_id)
  INNER JOIN billing.extra_service_list c ON (a.extra_service_type = c.service_id) 
  INNER JOIN billing.country_list d ON (a.country = d.country_id) 
  INNER JOIN shared.transport_company e ON (a.transport_company = e.comp_id) 
  INNER JOIN shared.parcel_size f ON (a.parcel_size = f.size_id) 
  INNER JOIN billing.currency_list g ON (a.currency = g.currency_id) 

WHERE
  a.order_number = :order_number
"""


sql_query_transformation_overview = """
SELECT 
  i.log_id as "Log ID",
  i.order_number_log as "Order no.",
  i.date as "Date & Time (UTC)",
  h_from.name as "From",
  h_to.name as "To"
  
FROM billing.change_log i
  INNER JOIN billing.format_list h_from ON h_from.format_id = i.mapping_from
  INNER JOIN billing.format_list h_to   ON h_to.format_id   = i.mapping_to    

ORDER BY i.log_id DESC
LIMIT 10
"""