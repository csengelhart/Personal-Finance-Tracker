from annotationlib import Format

import pandas as pd
import csv
from datetime import datetime
from data_entry import get_description,get_date,get_amount,get_category

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
    def get_transcation(cls,start_date,end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format = CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date,CSV.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print(f"No transactions found in the given date range")
        else:
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")

            print(
                filtered_df.to_string(index= False,
                                      formatters = {"date": lambda x : x.strftime(CSV.FORMAT)})
            )

        total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
        total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
        print("\nSummary:")
        print(f"Total income: ${total_income:.2f}")
        print(f"Total expense: ${total_expense:.2f}")
        print(f"Net profit: ${total_income - total_expense:.2f}")

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

CSV.get_transcation("01-01-2025","01-01-2027")
add()
