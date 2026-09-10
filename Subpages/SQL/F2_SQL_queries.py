# ==== SQL 1 ==== 

# Number of items in each product category 
sql_query_no_items_product_category = """
SELECT
    category,
    count(*) as 'count' 
FROM
    data_table_sql
GROUP BY
    Category
ORDER BY 
    count DESC, category ASC
"""

# Number of items with additional service
sql_query_no_items_with_additional_service = """
SELECT 
    Additional_service as 'Additional service',
    count(*) as 'count'
FROM
    data_table_sql
WHERE 
    Additional_service IS NOT 'None'   
GROUP BY
    Additional_service
ORDER BY 
    count DESC
"""

# Number of items with  NO additional service = 'None'
sql_query_no_items_without_additional_service = """
SELECT
    Additional_service as 'Additional service',
    count(*) as 'count'
FROM
    data_table_sql
WHERE 
    Additional_service = 'None' 
GROUP BY
    Additional_service
ORDER BY 
    count DESC
"""

# ==== SQL 2 ==== 
# The most expensive item
sql_query_expensive_item = """
SELECT
    item_id as 'Item id',
    Product,
    Price, 
    Category, 
    Additional_service as 'Additional service',
    Additional_service_price as 'Additional service price'
FROM
    data_table_sql
ORDER BY
    Price DESC
LIMIT 1
"""

# The cheapest item
sql_query_cheapest_item = """
SELECT
    item_id as 'Item id',
    Product,
    Price, 
    Category, 
    Additional_service as 'Additional service',
    Additional_service_price as 'Additional service price'
FROM
    data_table_sql
ORDER BY
    (Price + 'Additional service price') ASC
LIMIT 1
"""

# The most expensive item including Additional service
# The cheapest item including Additional service
def get_sql_query_item_inc_add_service(service_type: str, sort: str) -> str:

    query = f"""
    SELECT
        item_id as 'Item id',
        Product,
        Price, 
        Category, 
        Additional_service as 'Additional service',
        Additional_service_price as 'Additional service price'
    FROM
        data_table_sql
    WHERE
        Additional_service = '{service_type}'
    ORDER BY
        Additional_service_price {sort}
    LIMIT 1
    """

    return query


# ==== SQL 3 ==== 
# Percentage % ratio of product prices per Category - NOT including additional services
def get_sql_query_percentage_product_prices_category(value: str) -> str:

    query = f"""
    SELECT
        category,
        count(*) as 'count',
        sum(price) as 'sum price',
        round(((sum(price)/'{value}')*100),2) as '% ratio'
    FROM
        data_table_sql
    GROUP BY
        Category
    ORDER BY 
        count DESC,
        category ASC
    """
    
    return query

# Percentage % ratio of product prices per Category - INCLUDING additional services
def get_sql_query_percentage_product_prices_category_inc_add_serv(value: str) -> str:

    query = f"""
    SELECT
        category,
        count(*) as 'count',
        sum(price+Additional_service_price) as 'sum price + add. services',
        round(((sum(price+Additional_service_price)/'{value}')*100),2) as '% ratio'
    FROM
        data_table_sql
    GROUP BY
        Category
    ORDER BY 
        count DESC, 
        category ASC
    """

    return query

# Percentage % ratio of additional services per category
def get_sql_query_percentage_add_services(value: str) -> str:

    query = f"""
    SELECT
        category,
        count(*) as 'count',
        sum(Additional_service_price) as 'sum add. services',
        round(((sum(Additional_service_price)/'{value}')*100),2) as '% ratio'
    FROM
        data_table_sql
    GROUP BY
        Category
    ORDER BY 
        count DESC, 
        category ASC
    """

    return query


# ==== SQL 4 ==== 
# AVG Price without additional services
sql_query_avg_price = """
SELECT 
    category,
    count(Price) as 'count',
    round(avg(Price), 2) as 'average price'
FROM
    data_table_sql
GROUP BY
    Category
HAVING 
    count(*) > 1
ORDER BY 
    category ASC
"""

# AVG Price WITH additional services
sql_query_avg_price_with_add_serv = """
SELECT 
    category,
    count(*) as 'count',
    round((sum(Price) + sum(Additional_service_price))/count(*), 2) as 'average price WITH add. services',
    round(((sum(Price) + sum(Additional_service_price))/count(*) - avg(Price)), 2) as 'Δ delta'
FROM
    data_table_sql
GROUP BY
    Category
HAVING 
    count(*) > 1
ORDER BY 
    category ASC
"""

# AVG Price of additional services
sql_query_avg_price_of_add_serv = """
SELECT 
    Additional_service, 
    count(*) as 'count',
    sum(Additional_service_price) as 'sum',
    round(sum(Additional_service_price)/count(*), 2) as 'average'
FROM
    data_table_sql
WHERE 
    Additional_service != 'None'
GROUP BY
    Additional_service
ORDER BY
    count(*) DESC
"""