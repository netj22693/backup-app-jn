# ==== TAB 1 ======

sql_query_table_overview = """
SELECT 
    a.offer_id as "Offer id",
    f.label as "Transport",
    b.from_city "From",
    b.to_city as "To",
    a.created_date as "Created day",
    a.created_time as "Created time",
    i.label as "Time zone",
    a.expected_delivery as "Expected delivery",
    a.final_price as "Final price",
    j.label as "Currency"                    
                
FROM function7.offer a
    INNER JOIN function7.delivery b ON (a.offer_id = b.offer_id)
    INNER JOIN function7.transport_type f ON (a.transport = f.transport_id)
    INNER JOIN function7.time_zone i ON (a.time_zone = i.zone_id)
    INNER JOIN function7.currency_detail j ON (a.currency = j.currency_id)
                
ORDER BY a.offer_id DESC
LIMIT 15
;"""


# ==== TAB 2 ====

sql_offer_exists = """
SELECT a.offer_id
FROM function7.offer a
WHERE a.offer_id = :offer_id

;"""

sql_table_offer = """
SELECT 
    a.offer_id,
    a.created_date,
    a.created_time,
    a.need_approve_date,
    a.need_approve_time,
    a.need_approve_days,
    f.label as "transport",
    g.label as "service",
    i.label as "time_zone",
    a.time_overall,
    a.expected_delivery,
    a.final_price,
    j.label as "currency"         
            
FROM function7.offer a
    INNER JOIN function7.transport_type f ON (a.transport = f.transport_id)
    INNER JOIN function7.service g ON (a.service = g.service_id)
    INNER JOIN function7.time_zone i ON (a.time_zone = i.zone_id)
    INNER JOIN function7.currency_detail j ON (a.currency = j.currency_id)

WHERE a.offer_id = :offer_id

;"""

sql_table_delivery = """
SELECT
    b.offer_id,
    b.from_country,
    b.from_city,
    b.from_dtd,
    b.to_country,
    b.to_city,
    b.to_dtd,
    b.distance_length,
    b.distance_time,
    b.dtd_time

FROM 
    function7.delivery b

WHERE b.offer_id = :offer_id
;"""

sql_table_costs = """
SELECT *
FROM function7.costs c
WHERE c.offer_id = :offer_id
;"""

sql_table_extra_steps_time = """
SELECT *
FROM function7.extra_steps_time e
WHERE e.offer_id = :offer_id
;"""


sql_table_sla = """
SELECT
    h.time_sla
    
FROM function7.offer a
    INNER JOIN function7.sla h ON  (a.transport = h.transport_id_sla)
        -- 2nd key condition is a must - AND
        AND (a.service   = h.service_id_sla)

    INNER JOIN function7.transport_type f ON (a.transport = f.transport_id)
    INNER JOIN function7.service g ON (a.service = g.service_id)

WHERE a.offer_id = :offer_id
;"""


# ==== TAB 3 ====

def get_sql_query_tab_3(input_number_rows, date_filter, input_transport, input_currency, input_country_from, input_country_to):

    sql_query_tab_3 = f"""
    SELECT 
        a.offer_id as "Offer id",
        f.label as "Transport",
        b.from_country "Country from",
        b.from_city "From",
        b.to_country "Country to",
        b.to_city as "To",
        a.created_date as "Created day",
        a.created_time as "Created time",
        i.label as "Time zone",
        a.expected_delivery as "Expected delivery",
        a.final_price as "Final price",
        j.label as "Currency"                    
                    
    FROM function7.offer a
        INNER JOIN function7.delivery b ON (a.offer_id = b.offer_id)
        INNER JOIN function7.transport_type f ON (a.transport = f.transport_id)
        INNER JOIN function7.time_zone i ON (a.time_zone = i.zone_id)
        INNER JOIN function7.currency_detail j ON (a.currency = j.currency_id)

    WHERE 
        f.label IN({input_transport}) AND
        j.label IN({input_currency}) AND
        b.from_country IN ({input_country_from}) AND
        b.to_country IN ({input_country_to})

        -- part of the query built in the code based on if conditions
        {date_filter} 
                    
    ORDER BY a.offer_id DESC
    LIMIT {input_number_rows}
"""
    
    return sql_query_tab_3