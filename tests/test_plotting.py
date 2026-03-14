import pandas as pd
from app.plotting import plot_transactions, plot_transactions_subcategories

def test_plot_transactions_handles_empty_dataframe(capsys):
    df = pd.DataFrame(columns=["date", "amount", "category", "subcategory", "description"])

    plot_transactions(df)

    captured = capsys.readouterr()
    assert "No transactions found to display" in captured.out


def test_plot_transactions_runs_without_error(monkeypatch, sample_transactions_df):
    df = sample_transactions_df.copy()
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")

    monkeypatch.setattr("matplotlib.pyplot.show", lambda: None)

    plot_transactions(df)


def test_plot_transactions_subcategories_handles_empty_dataframe(capsys):
    df = pd.DataFrame(columns=["date", "amount", "category", "subcategory", "description"])

    plot_transactions_subcategories(df)

    captured = capsys.readouterr()
    assert "No transactions found to display." in captured.out


def test_plot_transactions_subcategories_runs_without_error(monkeypatch, sample_transactions_df):
    monkeypatch.setattr("matplotlib.pyplot.show", lambda: None)

    plot_transactions_subcategories(sample_transactions_df)