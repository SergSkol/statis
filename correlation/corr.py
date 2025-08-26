import pandas as pd
from toolset import percent_to_float, comma_to_float

# Завантаження даних
file_path = "G:/My Drive/data-source-corr.csv"  # Замініть на шлях до файлу
df = pd.read_csv(file_path)

# Перетворення всіх числових колонок у float
df = df.apply(pd.to_numeric, errors='coerce')

# Target
target_field_name = "adpu 180d"
# target_field_name = "adpu multiplier 180d vs 28d"

# Кореляція Пірсона
pearson_corr_matrix = df.corr(method='pearson')
pearson_target_corr = pearson_corr_matrix[target_field_name].sort_values(ascending=False) 

# Кореляція Спірмана
spearman_corr_matrix = df.corr(method='spearman')
spearman_target_corr = spearman_corr_matrix[target_field_name].sort_values(ascending=False)

# Вивід кореляцій
print("Pearson correlation with " + target_field_name)
print(pearson_target_corr)
print("\nSpearman correlation with " + target_field_name)
print(spearman_target_corr)
