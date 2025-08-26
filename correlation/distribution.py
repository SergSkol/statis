import pandas as pd
import matplotlib.pyplot as plt

# Завантаження даних
file_path = "G:/My Drive/data-aff.csv"  # шлях до файлу
df = pd.read_csv(file_path)

df["ftd_month"] = pd.to_datetime(df["ftd_month"], errors="coerce")

# Фільтрування GxBet (Greece, Apr–Aug)
gxbet = df[
    (df["operator"].str.lower() == "gxbet") &
    (df["country"].str.lower() == "greece") &
    (df["affiliate_id"] == 151847) &
    (df["ftd_month"].between("2025-04-01", "2025-08-31"))
].copy()

# Фільтрування Instasino (Jul–Aug)
instasino = df[
    (df["operator"].str.lower() == "instasino") &
    (df["affiliate_id"] == 151847) &
    (df["ftd_month"].between("2025-07-01", "2025-08-31"))
].copy()

# Обчислення ROI
for d in [gxbet, instasino]:
    d["roi"] = d["dtp_amount_predicted_360days"] / d["affiliate_cost"]

# --- Функції візуалізації ---

def plot_roi_distribution(df, operator_name):
    """Гістограма ROI"""
    plt.figure(figsize=(10,6))
    
    # Очистка даних
    clean_df = df.copy()
    clean_df["roi"] = clean_df["roi"].replace([float("inf"), float("-inf")], pd.NA)
    clean_df = clean_df.dropna(subset=["roi"])
    
    df_no_cashout = clean_df[clean_df["cashouts_amount"] == 0]["roi"]
    df_cashout = clean_df[clean_df["cashouts_amount"] > 0]["roi"]

    plt.hist(df_no_cashout, bins=40, alpha=0.6, label="Без кешаутів")
    plt.hist(df_cashout, bins=40, alpha=0.6, label="З кешаутами")

    if not df_no_cashout.empty:
        plt.axvline(df_no_cashout.median(), color="blue", linestyle="dashed", linewidth=1)
    if not df_cashout.empty:
        plt.axvline(df_cashout.median(), color="orange", linestyle="dashed", linewidth=1)

    plt.title(f"Розподіл ROI – {operator_name}")
    plt.xlabel("ROI")
    plt.ylabel("Кількість користувачів")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.show()

def plot_roi_boxplot(df, operator_name):
    """Boxplot ROI"""
    plt.figure(figsize=(8,5))
    df["cashout_flag"] = df["cashouts_amount"].apply(lambda x: "З кешаутами" if x > 0 else "Без кешаутів")
    
    df.boxplot(column="roi", by="cashout_flag", grid=False)
    plt.title(f"Boxplot ROI – {operator_name}")
    plt.suptitle("")  # прибрати зайвий заголовок
    plt.ylabel("ROI")
    plt.show()

def summary_table(df, operator_name):
    """Таблиця з метриками + відносна різниця ROI"""
    table = df.groupby(df["cashouts_amount"] > 0).agg(
        users=("user_id", "nunique"),
        avg_cashout=("cashouts_amount", "mean"),
        avg_roi=("roi", "mean"),
        median_roi=("roi", "median")
    )
    table.index = ["Без кешаутів", "З кешаутами"]

    # Обчислення відносної різниці ROI (%)
    if "Без кешаутів" in table.index and "З кешаутами" in table.index:
        avg_no = table.loc["Без кешаутів", "avg_roi"]
        avg_yes = table.loc["З кешаутами", "avg_roi"]
        med_no = table.loc["Без кешаутів", "median_roi"]
        med_yes = table.loc["З кешаутами", "median_roi"]

        table.loc["Δ ROI vs без кешаутів (%)"] = [
            None,
            None,
            (avg_yes - avg_no) / avg_no * 100 if pd.notna(avg_no) and avg_no != 0 else None,
            (med_yes - med_no) / med_no * 100 if pd.notna(med_no) and med_no != 0 else None
        ]

    print(f"\n--- {operator_name} ---")
    print(table.round(3))
    return table

# --- Побудова графіків і таблиць ---
tables = {}
plot_roi_distribution(gxbet, "GxBet (Greece, Apr-Aug)")
plot_roi_boxplot(gxbet, "GxBet (Greece, Apr-Aug)")
tables["GxBet"] = summary_table(gxbet, "GxBet (Greece, Apr-Aug)")

plot_roi_distribution(instasino, "Instasino (Jul–Aug)")
plot_roi_boxplot(instasino, "Instasino (Jul–Aug)")
tables["Instasino"] = summary_table(instasino, "Instasino (Jul–Aug)")

# --- Експорт у Excel ---
output_file = "roi_cashouts_analysis.xlsx"
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    for name, tbl in tables.items():
        tbl.to_excel(writer, sheet_name=name)

print(f"\n✅ Дані збережено у файл: {output_file}")
