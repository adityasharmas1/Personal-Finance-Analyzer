# Personal Finance Analyzer
# Python Essentials Course Project
# Author: Aditya Sharma
#
# This program is used to record income and expenses, see where the money
# is going and calculate how much is saved. All data is stored in a JSON
# file so it is not lost when the program is closed.

import json
import os
from datetime import datetime

# ---------------------------------------------------------------
# Global variables (file names, categories, date format)
# ---------------------------------------------------------------
FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(FOLDER, "finance_data.json")
REPORT_FILE = os.path.join(FOLDER, "financial_report.txt")

DATE_FORMAT = "%d-%m-%Y"   # example: 01-09-2026

EXPENSE_CATEGORIES = ["Food", "Transport", "Education", "Shopping",
                      "Hostel/Rent", "Entertainment", "Health", "Bills", "Other"]
INCOME_SOURCES = ["Salary", "Pocket Money", "Freelancing", "Scholarship", "Other"]


# ---------------------------------------------------------------
# Part 1: Small helper functions (printing and taking input)
# ---------------------------------------------------------------
def print_heading(title):
    # prints a title with lines above and below it
    print()
    print("=" * 40)
    print(title.center(40).rstrip())
    print("=" * 40)


def format_money(amount):
    # converts a number to text like ₹30,000 or ₹250.50
    amount = round(amount, 2)
    sign = ""
    if amount < 0:
        sign = "-"
        amount = -amount

    if amount == int(amount):
        return sign + "₹" + f"{int(amount):,}"
    else:
        return sign + "₹" + f"{amount:,.2f}"


def get_amount(prompt, allow_zero=False):
    # keeps asking until the user enters a valid amount
    while True:
        text = input(prompt).strip()

        if text == "":
            print("Error: amount cannot be empty!")
            continue

        try:
            amount = float(text)
        except ValueError:
            print("Error: please enter a number, not letters!")
            continue

        if amount < 0:
            print("Error: amount cannot be negative!")
        elif amount == 0 and not allow_zero:
            print("Error: amount must be greater than 0!")
        elif not (amount < 100000000):
            # this also catches 'nan' and 'inf' which float() accepts
            print("Error: amount is too large or not valid!")
        else:
            return round(amount, 2)


def get_date(prompt):
    # asks for a date in DD-MM-YYYY format, Enter = today's date
    while True:
        text = input(prompt).strip()

        if text == "":
            return datetime.now().strftime(DATE_FORMAT)

        try:
            date = datetime.strptime(text, DATE_FORMAT)
        except ValueError:
            print("Error: invalid date! Use DD-MM-YYYY (example: 15-09-2026)")
            continue

        if date.year < 2000:
            print("Error: year must be 2000 or later!")
        else:
            return date.strftime(DATE_FORMAT)


def get_text(prompt, required=True):
    # asks for some text, empty input is not allowed if required is True
    while True:
        text = input(prompt).strip()
        if text == "" and required:
            print("Error: this cannot be empty!")
        elif len(text) > 50:
            print("Error: please use less than 50 characters!")
        else:
            return text


def get_number(prompt, low, high):
    # asks for a whole number between low and high
    while True:
        text = input(prompt).strip()

        if text == "":
            print("Error: please enter a number!")
            continue

        try:
            number = int(text)
        except ValueError:
            print("Error: please enter a number, not letters!")
            continue

        if number < low or number > high:
            print("Error: please enter a number from", low, "to", high)
        else:
            return number


def pick_from_list(title, options):
    # shows a numbered list and returns the option that the user selects
    print(title)
    for i in range(len(options)):
        print(f"  {i + 1}. {options[i]}")
    choice = get_number(f"Enter choice (1-{len(options)}): ", 1, len(options))
    return options[choice - 1]


def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer == "y" or answer == "yes":
            return True
        elif answer == "n" or answer == "no":
            return False
        else:
            print("Error: please type y or n!")


# ---------------------------------------------------------------
# Part 2: Saving and loading data (JSON file)
# ---------------------------------------------------------------
def is_valid(item):
    # checks if one transaction from the file is correct
    try:
        if item["type"] != "Income" and item["type"] != "Expense":
            return False
        if not isinstance(item["category"], str):
            return False
        if not (item["amount"] > 0):
            return False
        datetime.strptime(item["date"], DATE_FORMAT)
        if "description" not in item:
            item["description"] = ""
        return True
    except (KeyError, TypeError, ValueError):
        return False


def load_data():
    # reads the transactions from finance_data.json
    if not os.path.exists(DATA_FILE):
        print("No data file found, starting with empty data.")
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        transactions = data["transactions"]
        if not isinstance(transactions, list):
            raise ValueError("transactions should be a list")
    except (json.JSONDecodeError, UnicodeDecodeError, KeyError, TypeError, ValueError):
        # file is corrupted, so keep a backup copy and start again
        print("Warning: data file is corrupted! Starting with empty data.")
        try:
            os.replace(DATA_FILE, DATA_FILE + ".bak")
            print("Old file was saved as finance_data.json.bak")
        except OSError:
            pass
        return []
    except OSError:
        print("Warning: could not read the data file.")
        return []

    good_transactions = []
    bad_count = 0
    for item in transactions:
        if is_valid(item):
            good_transactions.append(item)
        else:
            bad_count += 1

    if bad_count > 0:
        print("Warning:", bad_count, "invalid transaction(s) were skipped.")

    return good_transactions


def save_data(transactions):
    # writes all the transactions to finance_data.json
    data = {"transactions": transactions}
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        return True
    except OSError:
        print("Error: could not save the data!")
        return False


def export_report(text):
    # writes the report text to financial_report.txt
    try:
        with open(REPORT_FILE, "w", encoding="utf-8") as file:
            file.write(text)
        return True
    except OSError:
        print("Error: could not write the report file!")
        return False


# ---------------------------------------------------------------
# Part 3: Calculations
# ---------------------------------------------------------------
def get_total(transactions, kind):
    # total of all "Income" or all "Expense" transactions
    total = 0
    for t in transactions:
        if t["type"] == kind:
            total = total + t["amount"]
    return round(total, 2)


def get_savings_rate(income, savings):
    # savings rate = (savings / income) * 100
    if income == 0:
        return 0.0   # cannot divide by zero
    return round(savings / income * 100, 2)


def get_category_totals(transactions):
    # returns a dictionary like {"Food": 5000, "Bills": 1200}
    totals = {}
    for t in transactions:
        if t["type"] == "Expense":
            name = t["category"]
            if name in totals:
                totals[name] = totals[name] + t["amount"]
            else:
                totals[name] = t["amount"]
    return totals


def get_top_category(totals):
    # finds the category with the highest spending
    top_name = "N/A"
    top_amount = 0
    for name in totals:
        if totals[name] > top_amount:
            top_name = name
            top_amount = totals[name]
    return top_name, top_amount


def get_highest_expense(transactions):
    highest = None
    for t in transactions:
        if t["type"] == "Expense":
            if highest is None or t["amount"] > highest["amount"]:
                highest = t
    return highest


def get_lowest_expense(transactions):
    lowest = None
    for t in transactions:
        if t["type"] == "Expense":
            if lowest is None or t["amount"] < lowest["amount"]:
                lowest = t
    return lowest


def get_month_key(date_text):
    # "01-09-2026" -> "2026-09"  (this format is easy to sort)
    date = datetime.strptime(date_text, DATE_FORMAT)
    return date.strftime("%Y-%m")


def get_month_name(month_key):
    # "2026-09" -> "September 2026"
    date = datetime.strptime(month_key, "%Y-%m")
    return date.strftime("%B %Y")


def get_months(transactions):
    # list of all months that have transactions, in order
    months = []
    for t in transactions:
        key = get_month_key(t["date"])
        if key not in months:
            months.append(key)
    months.sort()
    return months


def get_month_transactions(transactions, month_key):
    result = []
    for t in transactions:
        if get_month_key(t["date"]) == month_key:
            result.append(t)
    return result


def get_message(income, expenses):
    # simple message about savings (this is not financial advice)
    if income == 0 and expenses == 0:
        return "No transactions added yet."

    savings = income - expenses
    if savings < 0:
        return "Your expenses are higher than your income."

    rate = get_savings_rate(income, savings)
    if rate >= 30:
        return "Excellent saving!"
    elif rate >= 10:
        return "Your savings are moderate."
    else:
        return "Your savings are low."


def describe_expense(t):
    # short text about one expense, used in the reports
    if t is None:
        return "N/A"
    return f"{format_money(t['amount'])} ({t['category']}, {t['date']})"


def get_date_object(t):
    # used for sorting the transactions by date
    return datetime.strptime(t["date"], DATE_FORMAT)


# ---------------------------------------------------------------
# Part 4: Adding, viewing and searching transactions
# ---------------------------------------------------------------
def add_income(transactions):
    print_heading("ADD INCOME")

    amount = get_amount("Amount (₹): ")
    date = get_date("Date (DD-MM-YYYY, Enter for today): ")
    source = pick_from_list("Income source:", INCOME_SOURCES)

    if source == "Other":
        name = get_text("Enter source name (or press Enter to skip): ", False)
        if name != "":
            source = name

    description = get_text("Description (optional): ", False)

    new_transaction = {
        "date": date,
        "type": "Income",
        "category": source,
        "amount": amount,
        "description": description
    }
    transactions.append(new_transaction)

    if save_data(transactions):
        print()
        print("✓ Income added successfully!")


def add_expense(transactions):
    print_heading("ADD EXPENSE")

    amount = get_amount("Amount (₹): ")
    date = get_date("Date (DD-MM-YYYY, Enter for today): ")
    category = pick_from_list("Category:", EXPENSE_CATEGORIES)
    description = get_text("Description: ")

    new_transaction = {
        "date": date,
        "type": "Expense",
        "category": category,
        "amount": amount,
        "description": description
    }
    transactions.append(new_transaction)

    if save_data(transactions):
        print()
        print("✓ Expense added successfully!")


def print_table(transactions):
    # prints the transactions like a table (oldest first)
    if len(transactions) == 0:
        print("No transactions found.")
        return

    print(f"{'Date':<12}{'Type':<9}{'Category':<15}{'Amount':>12}  Description")
    print("-" * 70)

    for t in sorted(transactions, key=get_date_object):
        category = t["category"][:14]
        description = t["description"][:25]
        print(f"{t['date']:<12}{t['type']:<9}{category:<15}"
              f"{format_money(t['amount']):>12}  {description}")

    print("-" * 70)
    print(len(transactions), "transaction(s) shown.")


def view_transactions(transactions):
    print_heading("TRANSACTION HISTORY")
    print_table(transactions)


def search_transactions(transactions):
    print_heading("SEARCH TRANSACTIONS")

    if len(transactions) == 0:
        print("No transactions added yet.")
        return

    searching = True
    while searching:
        print("Search by:")
        print("  1. Date")
        print("  2. Category")
        print("  3. Type (Income / Expense)")
        print("  4. Amount range")
        choice = get_number("Enter choice (1-4): ", 1, 4)

        results = []

        if choice == 1:
            date = get_date("Enter date (DD-MM-YYYY, Enter for today): ")
            for t in transactions:
                if t["date"] == date:
                    results.append(t)

        elif choice == 2:
            word = get_text("Enter category (or part of it): ").lower()
            for t in transactions:
                if word in t["category"].lower():
                    results.append(t)

        elif choice == 3:
            kind = pick_from_list("Select type:", ["Income", "Expense"])
            for t in transactions:
                if t["type"] == kind:
                    results.append(t)

        else:
            low = get_amount("Minimum amount (₹): ", True)
            high = get_amount("Maximum amount (₹): ")
            while high < low:
                print("Error: maximum cannot be less than minimum!")
                high = get_amount("Maximum amount (₹): ")
            for t in transactions:
                if low <= t["amount"] <= high:
                    results.append(t)

        print()
        print_table(results)
        print()
        searching = ask_yes_no("Do you want to search again? (y/n): ")
        print()


# ---------------------------------------------------------------
# Part 5: Analysis screens and report
# ---------------------------------------------------------------
def category_lines(transactions):
    # makes the lines for the category table (used on screen and in report)
    totals = get_category_totals(transactions)
    lines = []

    if len(totals) == 0:
        lines.append("No expenses added yet.")
        return lines

    total_expenses = get_total(transactions, "Expense")
    lines.append(f"{'Category':<16}{'Amount':>12}{'Percent':>10}")
    lines.append("-" * 38)

    # print from highest to lowest: find the top one, print it, remove it
    remaining = dict(totals)
    while len(remaining) > 0:
        name, amount = get_top_category(remaining)
        percent = amount / total_expenses * 100
        lines.append(f"{name:<16}{format_money(amount):>12}{percent:>9.2f}%")
        del remaining[name]

    lines.append("-" * 38)
    lines.append(f"{'Total':<16}{format_money(total_expenses):>12}{'100.00':>9}%")
    return lines


def monthly_comparison_lines(transactions):
    # compares all the months (only if there is more than one month)
    months = get_months(transactions)
    lines = []
    if len(months) < 2:
        return lines

    lines.append(f"{'Month':<16}{'Income':>12}{'Expenses':>12}{'Savings':>12}{'Rate':>10}")
    lines.append("-" * 62)

    for key in months:
        month_data = get_month_transactions(transactions, key)
        income = get_total(month_data, "Income")
        expenses = get_total(month_data, "Expense")
        savings = income - expenses
        rate = get_savings_rate(income, savings)
        lines.append(f"{get_month_name(key):<16}{format_money(income):>12}"
                     f"{format_money(expenses):>12}{format_money(savings):>12}"
                     f"{rate:>9.2f}%")
    return lines


def summary_lines(transactions):
    # makes the lines for the full financial summary
    income = get_total(transactions, "Income")
    expenses = get_total(transactions, "Expense")
    savings = round(income - expenses, 2)
    rate = get_savings_rate(income, savings)
    top_name, top_amount = get_top_category(get_category_totals(transactions))

    if top_name == "N/A":
        top_text = "N/A"
    else:
        top_text = f"{top_name} ({format_money(top_amount)})"

    lines = []
    lines.append(f"{'Total Income:':<26}{format_money(income)}")
    lines.append(f"{'Total Expenses:':<26}{format_money(expenses)}")
    lines.append(f"{'Total Savings:':<26}{format_money(savings)}")
    lines.append(f"{'Savings Rate:':<26}{rate:.2f}%")
    lines.append(f"{'Transactions:':<26}{len(transactions)}")
    lines.append(f"{'Highest Expense:':<26}{describe_expense(get_highest_expense(transactions))}")
    lines.append(f"{'Lowest Expense:':<26}{describe_expense(get_lowest_expense(transactions))}")
    lines.append(f"{'Most Expensive Category:':<26}{top_text}")
    lines.append("")
    lines.append("Status: " + get_message(income, expenses))

    comparison = monthly_comparison_lines(transactions)
    if len(comparison) > 0:
        lines.append("")
        lines.append("Monthly Comparison")
        lines.extend(comparison)

    return lines


def show_monthly_analysis(transactions):
    print_heading("MONTHLY ANALYSIS")

    months = get_months(transactions)
    if len(months) == 0:
        print("No transactions added yet.")
        return

    names = []
    for key in months:
        names.append(get_month_name(key))

    chosen_name = pick_from_list("Select a month:", names)
    key = months[names.index(chosen_name)]
    month_data = get_month_transactions(transactions, key)

    income = get_total(month_data, "Income")
    expenses = get_total(month_data, "Expense")
    savings = round(income - expenses, 2)
    rate = get_savings_rate(income, savings)
    top_name, top_amount = get_top_category(get_category_totals(month_data))

    print()
    print(chosen_name)
    print("-" * 35)
    print(f"{'Income:':<20}{format_money(income)}")
    print(f"{'Expenses:':<20}{format_money(expenses)}")
    print(f"{'Savings:':<20}{format_money(savings)}")
    print(f"{'Savings Rate:':<20}{rate:.2f}%")
    print(f"{'Transactions:':<20}{len(month_data)}")
    print(f"{'Highest Expense:':<20}{describe_expense(get_highest_expense(month_data))}")
    print(f"{'Top Category:':<20}{top_name}")
    print()
    print(get_message(income, expenses))


def show_categories(transactions):
    print_heading("SPENDING CATEGORIES")
    for line in category_lines(transactions):
        print(line)


def show_savings_analysis(transactions):
    print_heading("SAVINGS ANALYSIS")

    income = get_total(transactions, "Income")
    expenses = get_total(transactions, "Expense")
    savings = round(income - expenses, 2)
    rate = get_savings_rate(income, savings)

    print(f"{'Total Income:':<20}{format_money(income)}")
    print(f"{'Total Expenses:':<20}{format_money(expenses)}")
    print("-" * 35)
    print(f"{'Savings:':<20}{format_money(savings)}")
    print(f"{'Savings Rate:':<20}{rate:.2f}%")
    print()
    print(get_message(income, expenses))
    print("(This is only a simple message, not financial advice.)")


def show_summary(transactions):
    print_heading("FINANCIAL SUMMARY")
    for line in summary_lines(transactions):
        print(line)


def make_report(transactions):
    # creates the full text of the report
    now = datetime.now().strftime("%d-%m-%Y %H:%M")
    lines = []
    lines.append("=" * 54)
    lines.append("PERSONAL FINANCE ANALYZER - REPORT".center(54))
    lines.append("=" * 54)
    lines.append("Generated on: " + now)
    lines.append("")
    lines.append("FINANCIAL SUMMARY")
    lines.append("-" * 54)
    lines.extend(summary_lines(transactions))
    lines.append("")
    lines.append("SPENDING BY CATEGORY")
    lines.append("-" * 54)
    lines.extend(category_lines(transactions))
    lines.append("")
    lines.append("Note: this report is only a record of the data entered by the user.")
    return "\n".join(lines) + "\n"


def export_option(transactions):
    print_heading("EXPORT REPORT")
    if export_report(make_report(transactions)):
        print("✓ Report exported successfully!")
        print("Saved as: financial_report.txt")


# ---------------------------------------------------------------
# Part 6: Dashboard, menu and main program
# ---------------------------------------------------------------
def show_dashboard(transactions):
    income = get_total(transactions, "Income")
    expenses = get_total(transactions, "Expense")
    savings = round(income - expenses, 2)
    rate = get_savings_rate(income, savings)
    top_name, top_amount = get_top_category(get_category_totals(transactions))

    print_heading("PERSONAL FINANCE ANALYZER")
    print()
    print(f"{'Current Month:':<20}{datetime.now().strftime('%B %Y')}")
    print(f"{'Income:':<20}{format_money(income)}")
    print(f"{'Expenses:':<20}{format_money(expenses)}")
    print(f"{'Savings:':<20}{format_money(savings)}")
    print(f"{'Savings Rate:':<20}{rate:.2f}%")
    print(f"{'Transactions:':<20}{len(transactions)}")
    print(f"{'Top Category:':<20}{top_name}")
    print()


def show_menu():
    print("-" * 40)
    print("1.  Add Income")
    print("2.  Add Expense")
    print("3.  View Transactions")
    print("4.  Monthly Analysis")
    print("5.  Spending Categories")
    print("6.  Savings Analysis")
    print("7.  Financial Summary")
    print("8.  Search Transactions")
    print("9.  Export Report")
    print("10. Exit")
    print("-" * 40)


def main():
    transactions = load_data()

    running = True
    while running:
        show_dashboard(transactions)
        show_menu()
        choice = get_number("Enter your choice (1-10): ", 1, 10)

        if choice == 1:
            add_income(transactions)
        elif choice == 2:
            add_expense(transactions)
        elif choice == 3:
            view_transactions(transactions)
        elif choice == 4:
            show_monthly_analysis(transactions)
        elif choice == 5:
            show_categories(transactions)
        elif choice == 6:
            show_savings_analysis(transactions)
        elif choice == 7:
            show_summary(transactions)
        elif choice == 8:
            search_transactions(transactions)
        elif choice == 9:
            export_option(transactions)
        else:
            print()
            print("Thank you for using Personal Finance Analyzer. Goodbye!")
            running = False

        if running:
            input("\nPress Enter to continue...")


# program starts from here
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # if the user presses Ctrl+C the program closes without an error
        print("\n\nProgram closed. Your saved data is safe.")
