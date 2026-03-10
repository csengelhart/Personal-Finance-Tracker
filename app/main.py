from data_entry import get_description, get_date, get_amount, get_category
from app.storage import initialize_csv, add_entry
from app.report import get_transactions, print_transactions_summary
from app.plotting import plot_transactions

def add_transaction() -> None:
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or press enter for current date: ",
        allow_default=True
    )
    amount = get_amount()
    category = get_category()
    description = get_description()
    add_entry(date, amount, category, description)
    print("Successfully added entry.")

def main() -> None:
    initialize_csv()

    while True:
        print("\n1. Add transaction")
        print("2. View transactions")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_transaction()

        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")

            df = get_transactions(start_date, end_date)
            print_transactions_summary(df)

            if not df.empty:
                show_chart = input(
                    "Would you like to see a chart of transactions over this time? (y/n): "
                ).lower()

                if show_chart == "y":
                    plot_transactions(df)

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Enter a valid choice. Enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
