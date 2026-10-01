
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
    FROM shared.parcel_size
    """ 

    sql_query_additional_service_table = """
    SELECT *
    FROM billing.extra_service_list
    """ 