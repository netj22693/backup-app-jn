
'''
- Simple generic functions which can be reused across Functions FX
- No specific Function/Business domain logic
'''


def singular_or_plural(input_value: int | float) -> str:
    """
    Used for determining if day/days, hour/hours, route/routes, etc.
    """
    if input_value == 1:
        return ""
    else:
        return "s"