def singular_or_plural(input_value: int | float) -> str:
    '''
    Used for determining if day/days, hour/hours, route/routes, etc.
    '''
    if input_value < 2:
        return ""
    
    else:
        return "s"