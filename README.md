# Personal Finance Analyzer

A command-line program made in Python for my Python Essentials course. It helps a user record income and expenses, see where the money is going, and find out how much is being saved.

## Project Description

Many students do not track their money, so at the end of the month they do not know where it went. This program solves that problem. The user can add income and expenses, and the program calculates the totals, savings, spending by category and a month-by-month comparison. All the data is saved in a JSON file, so it is still there when the program is opened again.

The whole program is in one file (`main.py`) and uses only the Python standard library.

## Features

- Dashboard with income, expenses, savings, savings rate, number of transactions, current month and top spending category
- Add income (Salary, Pocket Money, Freelancing, Scholarship, Other)
- Add expense (Food, Transport, Education, Shopping, Hostel/Rent, Entertainment, Health, Bills, Other)
- View all transactions in a table
- Search transactions by date, category, type or amount range
- Monthly analysis for any month that has data
- Spending category analysis with percentages
- Savings analysis with a simple message
- Financial summary with highest/lowest expense and monthly comparison
- Export a report to `financial_report.txt`
- Data is saved automatically in `finance_data.json`
- Input validation, so the program does not crash on wrong input, a missing file or a corrupted file

## Technologies Used

- Python 3.8 or above
- Standard library modules only: `json`, `os`, `datetime`

## Python Concepts Demonstrated

| Concept | Where it is used in `main.py` |
|---|---|
| Variables, strings, integers, floats | Throughout the program, e.g. `format_money()` |
| Lists | `transactions`, `EXPENSE_CATEGORIES`, `INCOME_SOURCES` |
| Dictionaries | Each transaction, `get_category_totals()` |
| if / elif / else | Menu in `main()`, `get_message()` |
| for loops | `get_total()`, `print_table()` |
| while loops | Main menu loop, input functions like `get_amount()` |
| Functions with parameters and return values | Every part of the program |
| Exception handling (try / except) | `get_amount()`, `get_date()`, `load_data()` |
| File handling | `load_data()`, `save_data()`, `export_report()` |
| JSON | `finance_data.json` |
| datetime | `get_date()`, `get_month_key()` |
| Modular programming | Program is divided into 6 parts using separate functions |

## Project Structure

```
personal_finance_analyzer/
├── main.py                 # the complete program
├── requirements.txt        # no extra packages are needed
├── README.md               # this file
├── finance_data.json       # created automatically when data is saved
└── financial_report.txt    # created automatically when a report is exported
```

`main.py` has 6 parts:

1. **Helper functions** - printing headings, formatting money, taking valid input
2. **Saving and loading** - reading and writing the JSON file and the report
3. **Calculations** - totals, savings rate, category totals, highest/lowest expense
4. **Transactions** - adding, viewing and searching
5. **Analysis screens and report** - monthly analysis, categories, savings, summary, export
6. **Dashboard and main program** - dashboard, menu and the main loop

## How to Run

1. Install Python 3.8 or above from https://www.python.org/downloads/
2. Keep `main.py` in a folder.
3. Open a terminal in that folder and type:

```
python main.py
```

(On some computers the command is `python3 main.py`.)

**In VS Code:** open the folder (File > Open Folder), open `main.py` and click the Run button at the top right.

No packages have to be installed. `requirements.txt` only shows that no extra library is needed.

`finance_data.json` and `financial_report.txt` are created in the same folder as `main.py`. To start again with empty data, delete `finance_data.json`.

## Example Usage

```
========================================
       PERSONAL FINANCE ANALYZER
========================================

Current Month:      September 2026
Income:             ₹30,000
Expenses:           ₹21,500
Savings:            ₹8,500
Savings Rate:       28.33%
Transactions:       7
Top Category:       Hostel/Rent

----------------------------------------
1.  Add Income
2.  Add Expense
3.  View Transactions
4.  Monthly Analysis
5.  Spending Categories
6.  Savings Analysis
7.  Financial Summary
8.  Search Transactions
9.  Export Report
10. Exit
----------------------------------------
Enter your choice (1-10): 2

========================================
               ADD EXPENSE
========================================
Amount (₹): 250
Date (DD-MM-YYYY, Enter for today):
Category:
  1. Food
  2. Transport
  ...
Enter choice (1-9): 1
Description: Lunch

✓ Expense added successfully!
```

## Future Improvements

- Option to edit and delete a transaction
- Set a monthly budget and show a warning when it is crossed
- Recurring transactions such as rent
- Export to CSV to open in Excel
- Graphs using matplotlib
- A GUI using tkinter
- Use classes (OOP) and split the code into multiple files

## Author

**Name:** Aditya Sharma
**Course:** Python Essentials
**Year:** 2026
