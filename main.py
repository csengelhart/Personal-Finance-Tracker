
import pandas as pd
import csv
from datetime import datetime
from data_entry import get_description,get_date,get_amount,get_category
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category","description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns= cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)



    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {"date": date,
                     "amount": amount,
                     "category": category,
                     "description": description
                     }
        with open(cls.CSV_FILE, 'a',newline= "") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames= cls.COLUMNS)
            writer.writerow(new_entry)
        print("Successfully added entry")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            print(
                f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )

            total_income = filtered_df[filtered_df["category"] == "Income"][
                "amount"
            ].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"][
                "amount"
            ].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

        return filtered_df




def add():
    CSV.initialize_csv()
    date = get_date(
"Enter the date of the transaction (dd-mm-yyyy) or enter for current date: ",
        allow_default= True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transaction(df):
    if df.empty:
        print("No data to plot.")
        return

    df = df.copy()

    # make sure date is datetime and amount is numeric
    df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # set date as index
    df.set_index("date", inplace=True)
    df.sort_index(inplace=True)

    # create full daily date range for continuous plotting
    full_date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq="D")

    # resample income and expense by day, then fill missing days with 0
    income_df = (
        df[df["category"] == "Income"]["amount"]
        .resample("D")
        .sum()
        .reindex(full_date_range, fill_value=0)
    )

    expense_df = (
        df[df["category"] == "Expense"]["amount"]
        .resample("D")
        .sum()
        .reindex(full_date_range, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df.values, label="Income", color="g")
    plt.plot(expense_df.index, expense_df.values, label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n1. Add transaction")
        print("2. View transactions")
        print("3. Exit")
        choice =input("Enter your choice: ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date of the transaction (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date of the transaction (dd-mm-yyyy): ")
            df= CSV.get_transactions(start_date,end_date)

            if input("Would you like to see a chart of transactions over this time? (y/n): ").lower() == "y":
                plot_transaction(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Enter a valid choice. Enter 1, 2, or 3.")

if __name__ == "__main__":
    main()

