import csv
import os
import pandas as pd
from app.models import CSV_FILE, COLUMNS

def initialize_csv() -> None:
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(CSV_FILE, index=False)

def add_entry(date: str, amount: float, category: str, subcategory:str, description: str) -> None:
    new_entry = {
        "date": date,
        "amount": amount,
        "category": category,
        "subcategory": subcategory,
        "description": description,
    }

    with open(CSV_FILE, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)
        writer.writerow(new_entry)

def load_transactions() -> pd.DataFrame:
    initialize_csv()
    return pd.read_csv(CSV_FILE)