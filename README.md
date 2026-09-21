# Expense Tracker

Welcome to the Expense Tracker, a robust Python command-line application designed to empower you to log, manage, and track your daily personal expenses with maximum efficiency and simplicity.

## Key Features

*   **Categorized Logging:** Effortlessly record your daily expenditures with comprehensive details, including the expense name, amount, and category, keeping your finances thoroughly organized.
*   **Data Persistence:** Your expense records are automatically exported and appended into a localized `expenses.csv` file using UTF-8 encoding for reliable, long-term local storage.
*   **Budget Insights:** Gain meaningful insights into your financial habits by monitoring and analyzing your total expenditure over time.

## Installation

Ensure you have Python installed on your system. You can then install the required dependencies by running:

```bash
pip install -r requirements.txt
```

## Quick Start

1.  Clone this repository to your local machine.
2.  Ensure your `requirements.txt` is installed.
3.  Execute the main script to start logging your expenses:

```bash
python expense_tracker.py
```

Follow the on-screen prompts to input the expense details, and the data will be securely saved into your `expenses.csv` file.

## Repository & File Structure

To help you and others navigate the codebase, here is a quick overview of the repository layout:

```text
├── expense.py          # Defines the Expense class and data model
├── expense_tracker.py  # Main script executing user interaction and CLI logic
├── expenses.csv        # Data file storing saved expense records
├── requirements.txt    # Python package dependencies
└── README.md           # Project documentation
```

## License

This project is open-source and available under the MIT License.

