import pandas as pd
import matplotlib.pyplot as plt

def plot_transactions(df: pd.DataFrame) -> None:
    if df.empty:
        print("No transactions to plot")
        return

    df = df.copy()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df.set_index("date", inplace=True)
    df.sort_index(inplace=True)

    full_date_range = pd.date_range(
        start = df.index.min(),
        end = df.index.max(),
        freq = "D"
    )

    income_series = (
        df.loc[df["category"] == "Income", "amount"]
        .resample("D")
        .sum()
        .reindex(full_date_range, fill_value=0)
    )

    expense_series = (
        df.loc[df["category"] == "Expense", "amount"]
        .resample("D")
        .sum()
        .reindex(full_date_range, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_series.index, income_series.values, label="Income")
    plt.plot(expense_series.index, expense_series.values, label="Expense")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income vs Expense Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()