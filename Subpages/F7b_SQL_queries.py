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

def get_sql_query_tab_3(input_number_rows: int, date_filter: str, input_transport: str, input_currency: str, input_country_from: str, input_country_to: str) -> str:

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


# ==== TAB 4 ====

# Function returning WHERE statement if user filtering based on date
def get_sql_part_where_date(date_filter: bool) -> str | None:

    if date_filter == True:
        query = """
        WHERE
        TO_DATE(a.created_date, 'DD-Mon-YY') BETWEEN DATE :date_from AND DATE :date_to"""
    
    else: query = None
    
    return query


def get_sql_query_transport(date_filter: bool, where_condition: str | None ) -> str:
    
    query = """
    SELECT f.label, count(a.transport)
    FROM function7.offer a
    INNER JOIN function7.transport_type f ON (a.transport = f.transport_id)"""

    # User filtering based on date
    if date_filter == True:
        query += where_condition
    
    query +="""
    GROUP BY a.transport, f.label
    ORDER BY count(a.transport) DESC;"""

    return query

def get_sql_query_service(date_filter: bool, where_condition: str | None ) -> str:

    query = """
    SELECT g.label, count(a.service)
    FROM function7.offer a
    INNER JOIN function7.service g ON (a.service = g.service_id)"""
    
    # User filtering based on date
    if date_filter == True:
        query += where_condition

    query +="""
    GROUP BY a.service, g.label
    ORDER BY count(a.service) DESC;"""
    return query

def get_sql_query_from_country(date_filter: bool, where_condition: str | None ) -> str:
    
    query = """
    SELECT b.from_country, count(b.from_country)
    FROM function7.delivery b
    INNER JOIN function7.offer a ON (a.offer_id = b.offer_id)"""

    # User filtering based on date
    if date_filter == True:
        query += where_condition

    query += """
    GROUP BY b.from_country
    ORDER BY count(b.from_country) DESC;"""
    return query

def get_sql_query_to_country(date_filter: bool, where_condition: str | None ) -> str:

    query = """
    SELECT b.to_country, count(b.to_country)
    FROM function7.delivery b
    INNER JOIN function7.offer a ON (a.offer_id = b.offer_id)"""
    
    # User filtering based on date
    if date_filter == True:
        query += where_condition

    query += """
    GROUP BY b.to_country
    ORDER BY count(b.to_country) DESC;"""

    return query

def get_sql_query_from_to_country(date_filter: bool, where_condition: str | None, country_from: str ) -> str:

    query = """
    SELECT b.from_country, b.to_country, count(b.to_country)
    FROM function7.delivery b
    INNER JOIN function7.offer a ON (a.offer_id = b.offer_id)"""

    # User filtering based on date
    if date_filter == True:
        query += where_condition

        query += f"""
        AND b.from_country = :{country_from}"""
    
    elif date_filter == False:
        query += f"""
        WHERE b.from_country = :{country_from}"""

    query += """
    GROUP BY b.from_country, b.to_country
    ORDER BY count(b.to_country) DESC, from_country ASC"""

    return query

def get_sql_query_dtd_with_without(date_filter: bool, where_condition: str | None ) -> str:

    query = f"""
    SELECT
    COUNT(*) FILTER (WHERE c.dtd_from != 0 OR c.dtd_to != 0) AS "With DTD",
    COUNT(*) FILTER (WHERE c.dtd_from = 0 AND c.dtd_to = 0) AS "Without DTD"
    FROM function7.costs c 
    INNER JOIN function7.offer a ON (a.offer_id = c.offer_id)"""

    # User filtering based on date
    if date_filter == True:
        query += where_condition

    return query


def get_sql_query_currency(date_filter: bool, where_condition: str | None ) -> str:

    query = f"""
    SELECT j.label, count(a.currency)
    FROM function7.offer a
    INNER JOIN function7.currency_detail j ON (a.currency = j.currency_id)"""

    # User filtering based on date
    if date_filter == True:
        query += where_condition

    query += """
    GROUP BY j.label
    ORDER BY count(a.currency) DESC;"""
    
    return query

def get_sql_query_city(date_filter: bool, where_condition: str | None, direction_city: str,direction_country: str) -> str:

    # mapping to prevent injections
    db_columns = {
    "from_city": "b.from_city",
    "to_city": "b.to_city",
    "from_country": "b.from_country",
    "to_country": "b.to_country"
}

    col1 = db_columns[direction_city]
    col2 = db_columns[direction_country]

    query = f"""
    SELECT {col1}, {col2}, count(*)
    FROM function7.offer a
    INNER JOIN function7.delivery b ON (a.offer_id = b.offer_id)"""

    # User filtering based on date
    if date_filter == True:
        query += where_condition

    query += f"""
    GROUP BY {col1}, {col2}
    ORDER BY count(*) DESC
    LIMIT 5;"""
    
    return query

def get_sql_query_routes(date_filter: bool, where_condition: str | None ) -> str:

    query = f"""
    SELECT 
    b.from_city,
    b.from_country,
    b.to_city, 
    b.to_country,
    count(*)
    FROM function7.offer a
    INNER JOIN function7.delivery b ON (a.offer_id = b.offer_id)"""

    # User filtering based on date
    if date_filter == True:
        query += where_condition

    query += """
    GROUP BY 
    b.from_city,
    b.from_country,
    b.to_city,
    b.to_country
    ORDER BY count(*) DESC
    LIMIT 20;"""
    
    return query