from typing import Dict, Tuple

def create_parameters_for_sql(input: list, param_letter: str) -> Tuple[Dict[str, str], str]:
    '''
    Context: Parametrized queries using IN() in SQL are horribly slowing down returning result from PostgreSQL back to the code. Thus:

    THIS FUNCTION DOES DYNAMIC MAPPING to avoid SQL injection as the SQL query is built on f-string principle

    1) build of unique parameter e.g. t0, t1, t2 (depends on the param_letter)
    2) Creation of list [":t0", ":t1", ":t2"] -> list_params_keys[] filled with values
    3) Adding "key":"value" into dict params {} -> {"t0":"Airplane", "t1":"Train", "t2":"Truck"}
    4) Creation of string for sql ":t0, :t1, :t2" -> string_for_sql_in
    '''
    list_params_keys = []
    params = {}

    i = 0
    for value in input:
        param_name = param_letter + str(i)
        list_params_keys.append(":" + param_name)
        params[param_name] = value
        i = i + 1
    
    string_for_sql_in = ", ".join(list_params_keys)
    return params, string_for_sql_in