import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def plot_transactions(df: pd.DataFrame) -> None:
    if df.empty:
        print("No transactions found to display")
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

def plot_transactions_subcategories(df: pd.DataFrame) -> None:
    if df.empty:
        print("No transactions found to display.")
        return

    df = df.copy()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount", "category", "subcategory"])

    pivot_df = df.pivot_table(
        index="category",
        columns="subcategory",
        values="amount",
        aggfunc="sum",
        fill_value=0
    )

    desired_order = [cat for cat in ["Income", "Expense"] if cat in pivot_df.index]
    pivot_df = pivot_df.loc[desired_order]

    ax = pivot_df.plot(
        kind="bar",
        stacked=True,
        figsize=(10, 5),
        rot=0,
        title="Income vs Expense Breakdown by Subcategory",
        legend=False
    )

    ax.set_xlabel("Category")
    ax.set_ylabel("Amount ($)")
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("${x:,.0f}"))

    # Get which subcategories actually appear in each category
    income_subcats = []
    expense_subcats = []

    if "Income" in pivot_df.index:
        income_subcats = pivot_df.columns[pivot_df.loc["Income"] > 0].tolist()

    if "Expense" in pivot_df.index:
        expense_subcats = pivot_df.columns[pivot_df.loc["Expense"] > 0].tolist()

    # Map legend labels to handles
    handles, labels = ax.get_legend_handles_labels()
    handle_map = dict(zip(labels, handles))

    income_handles = [handle_map[label] for label in income_subcats if label in handle_map]
    expense_handles = [handle_map[label] for label in expense_subcats if label in handle_map]

    # First legend: Income
    if income_handles:
        income_legend = ax.legend(
            income_handles,
            income_subcats,
            title="Income Subcategories",
            bbox_to_anchor=(1.05, 1),
            loc="upper left"
        )
        ax.add_artist(income_legend)

    # Second legend: Expense
    if expense_handles:
        ax.legend(
            expense_handles,
            expense_subcats,
            title="Expense Subcategories",
            bbox_to_anchor=(1.05, 0.45),
            loc="upper left"
        )

    plt.tight_layout()
    plt.show()



