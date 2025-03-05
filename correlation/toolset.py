# Функції для очищення даних
def percent_to_float(value):
    """Перетворює відсоткові значення у десятковий формат."""
    if isinstance(value, str) and '%' in value:
        return float(value.replace('%', '')) / 100
    return value

def comma_to_float(value):
    """Замінює кому на крапку в числових значеннях."""
    if isinstance(value, str):
        return float(value.replace(',', ''))
    return value
