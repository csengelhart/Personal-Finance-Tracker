import pandas as pd
import pytest

@pytest.fixture
def sample_transactions_df():
    return pd.DataFrame([
        {
            "date": "01-01-2026",
            "amount": 5000.0,
            "category": "Income",
            "subcategory": "Salary",
            "description": "Target",
        },
        {
            "date": "05-01-2026",
            "amount": 1200.0,
            "category": "Expense",
            "subcategory": "Rent",
            "description": "Lakepoint Rent",
        },
        {
            "date": "10-01-2026",
            "amount": 200.0,
            "category": "Expense",
            "subcategory": "Groceries",
            "description": "Costco",
        },
        {
            "date": "15-01-2026",
            "amount": 300.0,
            "category": "Income",
            "subcategory": "Bonus",
            "description": "Quarterly Bonus",
        },
    ])