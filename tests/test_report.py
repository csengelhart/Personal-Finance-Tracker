import pandas as pd
from app.report import get_transactions, print_transactions_summary

def test_get_transactions_returns_only_rows_in_range(monkeypatch, sample_transactions_df):
    def fake_load_transactions():
        return sample_transactions_df

    monkeypatch.setattr("app.report.load_transactions", fake_load_transactions)

    result = get_transactions("02-01-2026", "12-01-2026")
    assert len(result) == 2
    assert list(result["subcategory"]) == ["Rent","Groceries"]


def test_get_transactions_returns_empty_if_storage_is_empty(monkeypatch):
    empty_df = pd.DataFrame(columns=["date", "amount", "category", "subcategory", "description"])

    def fake_load_transactions():
        return empty_df

    monkeypatch.setattr("app.report.load_transactions", fake_load_transactions)
    result = get_transactions("01-01-2026", "31-01-2026")

    assert result.empty == True

def test_print_transactions_summary_prints_empty_messsage(capsys):
    df = pd.DataFrame(columns= ["date", "amount", "category", "subcategory", "description"])

    print_transactions_summary(df)
    captured = capsys.readouterr()
    assert "No transactions found in the given date range" in captured.out

def test_print_transactions_summary_prints_correct_totals(capsys):
    df = pd.DataFrame([
        {
            "date": pd.to_datetime("01-01-2026", format="%d-%m-%Y"),
            "amount": 5000.0,
            "category": "Income",
            "subcategory": "Salary",
            "description": "Target",
        },
        {
            "date": pd.to_datetime("05-01-2026", format="%d-%m-%Y"),
            "amount": 1200.0,
            "category": "Expense",
            "subcategory": "Rent",
            "description": "Lakepoint Rent",
        },
        {
            "date": pd.to_datetime("15-01-2026", format="%d-%m-%Y"),
            "amount": 300.0,
            "category": "Income",
            "subcategory": "Bonus",
            "description": "Quarterly Bonus",
        },
    ])

    print_transactions_summary(df)

    captured = capsys.readouterr()
    assert "Total Income: $5300.00" in captured.out
    assert "Total Expense: $1200.00" in captured.out
    assert "Net Savings: $4100.00" in captured.out