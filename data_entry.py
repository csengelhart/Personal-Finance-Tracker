from datetime import datetime
date_format = "%d-%m-%Y"
CATEGORIES = {
    "I": "Income",
    "E": "Expense",
}
from app.models import INCOME_SUBCATEGORIES, EXPENSE_SUBCATEGORIES

def get_date(prompt: str, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)

    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("invalid date format. Please enter date in the dd-mm-yyyy format")
        # recursive call to keep calling function until a valid date is entered
        return get_date(prompt, allow_default)

def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a non-negative non-zero value")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Enter the category ('I' for income or 'E' for Expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]

    print("Invalid category. Please enter 'I' for income or 'E' for Expense")
    return get_category()

def get_description():
    return input("Enter the description (optional): ")

def get_menu_choice(options: dict ,prompt: str):
    print(prompt)
    for key, value in options.items():
        print(f"{key}. {value}")

    choice = input("Select an option: ").strip()

    if choice in options:
        return options[choice]

    print("Invalid option. Please enter a valid option")
    return get_menu_choice(options,prompt)

def get_subcategory(category):
    if category == "Income":
        subcategory = get_menu_choice(INCOME_SUBCATEGORIES,"Select an income subcategory")
    elif category == "Expense":
        subcategory = get_menu_choice(EXPENSE_SUBCATEGORIES,"Select an expense subcategory")
    else:
        print("Invalid subcategory. Please enter a valid option")

    if subcategory == "Other":
        custom_subcategory = input("Enter the custom subcategory: ").strip()
        if custom_subcategory:
            return custom_subcategory.title()
        return "Other"

    return subcategory
