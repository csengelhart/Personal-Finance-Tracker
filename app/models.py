CSV_FILE = "../data/finance_data.csv"
COLUMNS = ["date", "amount", "category", "subcategory","description"]
DATE_FORMAT = "%d-%m-%Y"
VALID_CATEGORIES = ["Income", "Expense"]
EXPENSE_SUBCATEGORIES = {
    "1": "Rent",
    "2": "Groceries",
    "3": "Gas",
    "4": "Utilities",
    "5": "Dining",
    "6": "Entertainment",
    "7": "Subscriptions",
    "8": "Insurance",
    "9": "Healthcare",
    "10": "Shopping",
    "11": "Transportation",
    "12": "Other",
}

INCOME_SUBCATEGORIES = {
    "1": "Salary",
    "2": "Bonus",
    "3": "Freelance",
    "4": "Investment",
    "5": "Gift",
    "6": "Refund",
    "7": "Other",
}