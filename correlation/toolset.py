# Функції для очищення даних
def percent_to_float(value):
    """Перетворює відсоткові значення у десятковий формат."""
    """Usage:
    columns_to_convert_percent = ['1dep_users_28d_percent', '2dep_users_28d_percent', '3dep_users_28d_percent']

    for col in columns_to_convert_percent:
        df[col] = df[col].apply(percent_to_float)
    """

    if isinstance(value, str) and '%' in value:
        return float(value.replace('%', '')) / 100
    return value

def comma_to_float(value):
    """Замінює кому на крапку в числових значеннях."""
    """Usage:
    columns_to_convert_comma = ['2dep_adpu_28d', '3dep_adpu_28d']
        for col in columns_to_convert_comma:
        df[col] = df[col].apply(comma_to_float)
    """

    if isinstance(value, str):
        return float(value.replace(',', ''))
    return value
