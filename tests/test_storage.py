import pandas as pd
from app.storage import initialize_csv, add_entry, load_transactions

def test_initialize_csv_creates_file(tmp_path, monkeypatch):
    test_file = tmp_path / "finance_data.csv"

    monkeypatch.setattr("app.storage.CSV_FILE", str(test_file))

    initialize_csv()
    assert test_file.exists()

def test_load_transactions_returns_dataframe(tmp_path, monkeypatch):
    test_file = tmp_path / "finance_data.csv"

    monkeypatch.setattr("app.storage.CSV_FILE", str(test_file))

    initialize_csv()
    df = load_transactions()

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["date", "amount","category","subcategory", "description"]

def test_add_entry_writes_row_to_csv(tmp_path, monkeypatch):
    test_file = tmp_path / "finance_data.csv"

    monkeypatch.setattr("app.storage.CSV_FILE", str(test_file))

    initialize_csv()
    add_entry("01-01-2026", 5400, "Income","Salary","Target")

    df = load_transactions()

    assert len(df) == 1
    assert df.iloc[0]["date"] == "01-01-2026"
    assert df.iloc[0]["amount"] == 5400
    assert df.iloc[0]["category"] == "Income"
    assert df.iloc[0]["subcategory"] == "Salary"
    assert df.iloc[0]["description"] == "Target"

def test_add_entry_appends_multiple_rows(tmp_path, monkeypatch):
    test_file = tmp_path / "finance_data.csv"

    monkeypatch.setattr("app.storage.CSV_FILE", str(test_file))
    initialize_csv()
    add_entry("01-01-2026", 5000.0, "Income", "Salary", "Target")
    add_entry("10-01-2026", 1200.0, "Expense", "Rent", "Lakepoint Rent")

    df = load_transactions()

    assert len(df) == 2
    assert list(df["subcategory"]) == ["Salary", "Rent"]