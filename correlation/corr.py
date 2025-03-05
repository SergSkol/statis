import pandas as pd

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

# Завантаження даних
file_path = "G:/My Drive/corr-source-data.csv"  # Замініть на шлях до файлу
df = pd.read_csv(file_path)

# Очищення даних
columns_to_convert_percent = ['1dep_users_28d_percent', '2dep_users_28d_percent', '3dep_users_28d_percent']
columns_to_convert_comma = ['2dep_adpu_28d', '3dep_adpu_28d']

for col in columns_to_convert_percent:
    df[col] = df[col].apply(percent_to_float)

for col in columns_to_convert_comma:
    df[col] = df[col].apply(comma_to_float)

# Перетворення всіх числових колонок у float
df = df.apply(pd.to_numeric, errors='coerce')

# Кореляція Пірсона
pearson_corr_matrix = df.corr(method='pearson')
pearson_target_corr = pearson_corr_matrix["adpu_a80d_target"].sort_values(ascending=False)

# Кореляція Спірмана
spearman_corr_matrix = df.corr(method='spearman')
spearman_target_corr = spearman_corr_matrix["adpu_a80d_target"].sort_values(ascending=False)

# Вивід кореляцій
print("Pearson correlation with adpu_a80d_target:")
print(pearson_target_corr)
print("\nSpearman correlation with adpu_a80d_target:")
print(spearman_target_corr)
