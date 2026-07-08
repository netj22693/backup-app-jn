import pandas as pd
import streamlit as st


# ==== Mapping ====
def get_mapping_extra_services(df: pd.DataFrame) -> pd.DataFrame:

    '''
    Replaces BOOLEAN values for UI purposes
    '''
    
    # Need to create a copy of the original DF to do not change existing variable/DF outside of this function
    df_adj = df.copy()

    df_adj["extra_service"] = df_adj["extra_service"].replace({
    True: "Purchased",
    False: "Not purchased"
    })

    return df_adj


# ==== TAB 1 ====
sql_query_overview_invoices = """
SELECT 
    a.order_number as "Order no.",
    a.date as "Date",
    a.customer as "Customer",
    b.name as "Category",
    a.product_name as "Product",
    a.product_price as "Price",
    c.name as "Extra service",
    a.extra_service_price as "Extra service price",
    d.name as "Country",
    e.name as "Transport Company",
    a.tr_price as "Transport price",
    f.name as "Parcel size",
    a.total_price as "Total price", 
    g.name as "Currency",
    h.name as "File format"                                            

FROM billing.invoice a
    INNER JOIN billing.category_list b ON (a.category = b.category_id)
    INNER JOIN billing.extra_service_list c ON (a.extra_service_type = c.service_id) 
    INNER JOIN billing.country_list d ON (a.country = d.country_id) 
    INNER JOIN shared.transport_company e ON (a.tr_company = e.comp_id) 
    INNER JOIN shared.parcel_size f ON (a.parcel_size = f.size_id) 
    INNER JOIN billing.currency_list g ON (a.currency = g.currency_id) 
    INNER JOIN billing.format_list h ON (a.file_format = h.format_id)

ORDER BY 
    a.date DESC,
    a.order_number DESC
LIMIT 15  
    ;"""


# ==== TAB 2 ====
sql_query_order_exist = """
SELECT 
    a.order_number                                        
FROM billing.invoice a
WHERE 
    a.order_number = :order
"""


sql_query_overview = """
SELECT 
    a.order_number as "Order no.",
    a.date as "Date",
    a.customer as "Customer",
    a.total_price as "Total price",
    g.name as "Currency"                                            

FROM billing.invoice a
    INNER JOIN billing.category_list b ON (a.category = b.category_id)
    INNER JOIN billing.extra_service_list c ON (a.extra_service_type = c.service_id) 
    INNER JOIN billing.country_list d ON (a.country = d.country_id) 
    INNER JOIN shared.transport_company e ON (a.tr_company = e.comp_id) 
    INNER JOIN shared.parcel_size f ON (a.parcel_size = f.size_id) 
    INNER JOIN billing.currency_list g ON (a.currency = g.currency_id) 

WHERE 
    a.order_number = :order
    ;"""

sql_query_file_format = """
SELECT 
    h.name                                        

FROM billing.invoice a
    INNER JOIN billing.format_list h ON (a.file_format = h.format_id)

WHERE 
    a.order_number = :order
    ;"""

sql_query_product = """
SELECT 
    a.product_name as "Product",
    b.name as "Category",
    a.product_price as "Price",
    g.name as "Currency"                                       

FROM billing.invoice a
    INNER JOIN billing.category_list b ON (a.category = b.category_id)
    INNER JOIN billing.extra_service_list c ON (a.extra_service_type = c.service_id) 
    INNER JOIN billing.country_list d ON (a.country = d.country_id) 
    INNER JOIN shared.transport_company e ON (a.tr_company = e.comp_id) 
    INNER JOIN shared.parcel_size f ON (a.parcel_size = f.size_id) 
    INNER JOIN billing.currency_list g ON (a.currency = g.currency_id) 

WHERE 
    a.order_number = :order
;"""   

sql_query_extra_service = """
SELECT 
    c.name as "Extra service",
    a.extra_service_price as "Extra service price",
    g.name as "Currency"                          

FROM billing.invoice a
    INNER JOIN billing.category_list b ON (a.category = b.category_id)
    INNER JOIN billing.extra_service_list c ON (a.extra_service_type = c.service_id) 
    INNER JOIN billing.country_list d ON (a.country = d.country_id) 
    INNER JOIN shared.transport_company e ON (a.tr_company = e.comp_id) 
    INNER JOIN shared.parcel_size f ON (a.parcel_size = f.size_id) 
    INNER JOIN billing.currency_list g ON (a.currency = g.currency_id) 

WHERE 
    a.order_number = :order
;"""   

sql_query_transport = """
SELECT 
    e.name as "Transport Company",
    d.name as "Country",
    f.name as "Parcel size",
    a.tr_price as "Transport price",
    g.name as "Currency"                         

FROM billing.invoice a
    INNER JOIN billing.category_list b ON (a.category = b.category_id)
    INNER JOIN billing.extra_service_list c ON (a.extra_service_type = c.service_id) 
    INNER JOIN billing.country_list d ON (a.country = d.country_id) 
    INNER JOIN shared.transport_company e ON (a.tr_company = e.comp_id) 
    INNER JOIN shared.parcel_size f ON (a.parcel_size = f.size_id) 
    INNER JOIN billing.currency_list g ON (a.currency = g.currency_id) 

WHERE 
    a.order_number = :order
;""" 


sql_query_transport_company = """
SELECT 
    e.name                   

FROM billing.invoice a
    INNER JOIN shared.transport_company e ON (a.tr_company = e.comp_id) 

WHERE 
    a.order_number = :order
;"""

sql_query_mapping_log = """
SELECT 
    i.date as "Date",
    i.change as "Description",
    h_from.name as "From",
    h_to.name as "To"

FROM billing.change_log i
    INNER JOIN billing.format_list h_from ON h_from.format_id = i.mapping_from
    INNER JOIN billing.format_list h_to   ON h_to.format_id   = i.mapping_to
    INNER JOIN billing.invoice a ON (a.order_number = i.order_number_log)

WHERE 
    a.order_number = :order

ORDER BY 
    i.date ASC
;"""


# ==== TAB 4 ====

# Function returning WHERE statement, if user filtering based on date
def get_sql_part_where_date(date_filter: bool) -> str | None:

    if date_filter == True:
        query = """
        WHERE
        a.date BETWEEN :date_from AND :date_to"""
    
    else: query = None
    
    return query


def get_sql_query_category(date_filter: bool, where_condition: str | None) -> str:
    query = """
    SELECT b.name, count(a.category)
    FROM billing.invoice a 
    INNER JOIN billing.category_list b ON (a.category = b.category_id)"""

    # User filtering based on date
    if date_filter == True:
        query += where_condition
    
    query +="""
    GROUP BY b.name, a.category
    ORDER BY count(a.category) DESC;"""

    return query

def get_sql_query_company(date_filter: bool, where_condition: str | None) -> str:
    query = """
    SELECT e.name, count(a.tr_company)
    FROM billing.invoice a
    INNER JOIN shared.transport_company e ON (a.tr_company = e.comp_id)"""

    # User filtering based on date
    if date_filter == True:
        query += where_condition
    
    query +="""
    GROUP BY e.name, a.tr_company
    ORDER BY count(a.tr_company) DESC;"""

    return query

def get_sql_query_parcel_size(date_filter: bool, where_condition: str | None) -> str:

    query = """
    SELECT f.name, count(a.parcel_size)
    FROM billing.invoice a
    INNER JOIN shared.parcel_size f ON (a.parcel_size = f.size_id)"""

    # User filtering based on date
    if date_filter == True:
        query += where_condition
    
    query +="""
    GROUP BY f.name, a.parcel_size
    ORDER BY count(a.parcel_size) DESC;"""

    return query

def get_sql_query_currency(date_filter: bool, where_condition: str | None) -> str:

    query = """
    SELECT g.name, count(a.currency)
    FROM billing.invoice a
    INNER JOIN billing.currency_list g ON (a.currency = g.currency_id)"""

    # User filtering based on date
    if date_filter == True:
        query += where_condition
    
    query +="""
    GROUP BY g.name, a.currency
    ORDER BY count(a.currency) DESC;"""

    return query

def get_sql_query_country(date_filter: bool, where_condition: str | None) -> str:

    query = """
    SELECT d.name, count(a.country)
    FROM billing.invoice a
    INNER JOIN billing.country_list d ON (a.country = d.country_id)"""

    # User filtering based on date
    if date_filter == True:
        query += where_condition
    
    query +="""
    GROUP BY d.name, a.country
    ORDER BY count(a.country) DESC;"""

    return query

def get_sql_query_extra_service_type(date_filter: bool, where_condition: str | None) -> str:

    query = """
    SELECT c.name, count(a.extra_service_type)
    FROM billing.invoice a
    INNER JOIN billing.extra_service_list c ON (a.extra_service_type = c.service_id)"""

    # User filtering based on date
    if date_filter == True:
        query += where_condition
    
    query +="""
    GROUP BY c.name, a.extra_service_type
    ORDER BY count(a.extra_service_type) DESC;"""

    return query

def get_sql_query_extra_service_count(date_filter: bool, where_condition: str | None) -> str:

    query = """
    SELECT a.extra_service, count(a.extra_service)
    FROM billing.invoice a"""

    # User filtering based on date
    if date_filter == True:
        query += where_condition
    
    query +="""
    GROUP BY a.extra_service
    ORDER BY count(a.extra_service) DESC;"""

    return query

def get_sql_query_file_format(date_filter: bool, where_condition: str | None) -> str:

    query = """
    SELECT h.name, count(a.file_format)
    FROM billing.invoice a
    INNER JOIN billing.format_list h ON (a.file_format = h.format_id)"""

    # User filtering based on date
    if date_filter == True:
        query += where_condition
    
    query +="""
    GROUP BY h.name, a.file_format
    ORDER BY count(a.file_format) DESC;"""

    return query