import pandas as pd
from datetime import datetime
from app.models import DATE_FORMAT
from app.storage import load_transactions

def get_transactions(start_date: str, end_date: str) -> pd.DataFrame:
    df = load_transactions()

    if df.empty:
        return df

    df["date"] = pd.to_datetime(df["date"], format=DATE_FORMAT)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    start = datetime.strptime(start_date, DATE_FORMAT)
    end = datetime.strptime(end_date, DATE_FORMAT)

    mask = (df["date"] >= start) & (df["date"] <= end)
    return df.loc[mask].copy()

def print_transactions_summary(df: pd.DataFrame) -> None:
    if df.empty:
        print("No transactions found in the given date range.")
        return

    print(
        df.to_string(
            index=False,
            formatters={"date": lambda x: x.strftime(DATE_FORMAT)}
        )
    )

    total_income = df.loc[df["category"] == "Income", "amount"].sum()
    total_expense = df.loc[df["category"] == "Expense", "amount"].sum()

    print("\nSummary:")
    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expense: ${total_expense:.2f}")
    print(f"Net Savings: ${(total_income - total_expense):.2f}")