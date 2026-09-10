
sql_query_exchange_rate_data = """
SELECT *
FROM function5.exchange_rate_data
WHERE created_at >= :start
AND created_at < :end
"""