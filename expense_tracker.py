import calendar
from datetime import datetime
import os

import streamlit as st
from expense import Expense


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Kharcha Paani",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Kharcha Paani")
st.subheader("Personal Expense Tracker")
# ==========================================
# USER IDENTIFICATION & AUTHENTICATION
# ==========================================
USER_FILE = "users.txt"

# 1. Helper function to read saved users
def load_users():
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    user, pwd = line.strip().split(",")
                    users[user] = pwd
    return users

# 2. Helper function to save a new user
def save_user(username, password):
    with open(USER_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username},{password}\n")

st.sidebar.header("🔐 Authentication")

# 3. Add a radio button to switch between Login and Sign Up
auth_mode = st.sidebar.radio("Select Mode", ["Login", "Sign Up"])

# Load existing users from the file
users_db = load_users()

if auth_mode == "Sign Up":
    st.sidebar.subheader("Create a New Account")
    new_user = st.sidebar.text_input("Choose a Username").strip().lower()
    new_pwd = st.sidebar.text_input("Choose a Password", type="password")
    
    if st.sidebar.button("Register"):
        if not new_user or not new_pwd:
            st.sidebar.warning("⚠️ Please fill in both fields.")
        elif new_user in users_db:
            st.sidebar.error("❌ Username already exists. Try another.")
        else:
            save_user(new_user, new_pwd)
            st.sidebar.success("✅ Account created! Please switch to 'Login' above.")
    
    # Stop the app here so the expense tracker doesn't load during sign up
    st.stop() 

elif auth_mode == "Login":
    username = st.sidebar.text_input("Username").strip().lower()
    password = st.sidebar.text_input("Password", type="password")
    
    # Stop the app if fields are empty
    if not username or not password:
        st.info("👈 Please login or sign up in the sidebar to continue.")
        st.stop()
        
    # Verify the credentials against the saved users
    if username not in users_db or users_db[username] != password:
        st.sidebar.error("❌ Incorrect username or password.")
        st.stop()
        
    st.sidebar.success(f"✅ Logged in as {username.capitalize()}")
    
    # Dynamically set the file path based on the authenticated username
    EXPENSE_FILE_PATH = f"{username}_expenses.csv"



# ==========================================
# SETTINGS
# ==========================================


EXPENSE_CATEGORIES = [
    "🍔 Food",
    "🏡 Home",
    "💻 Work",
    "🎮 Fun",
    "🌀 Misc",
]


# ==========================================
# MONTHLY BUDGET
# ==========================================

st.subheader("💰 Monthly Budget")

budget = st.number_input(
    "Enter your monthly budget (₹)",
    min_value=0.0,
    step=500.0,
    format="%.2f"
)


# ==========================================
# SAVE EXPENSE TO CSV
# ==========================================

def save_expense_to_file(expense, expense_file_path):

    with open(
        expense_file_path,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"{expense.name},{expense.amount},{expense.category}\n"
        )


# ==========================================
# READ ALL EXPENSES FROM CSV
# ==========================================

def get_all_expenses(expense_file_path):

    expenses = []

    if not os.path.exists(expense_file_path):
        return expenses

    with open(
        expense_file_path,
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:

            if not line.strip():
                continue

            try:

                expense_name, expense_amount, expense_category = (
                    line.strip().split(",")
                )

                expense = Expense(
                    name=expense_name,
                    amount=float(expense_amount),
                    category=expense_category
                )

                expenses.append(expense)

            except ValueError:
                continue

    return expenses


# ==========================================
# EXPENSE SUMMARY
# ==========================================

def summarize_expense(expense_file_path, budget):

    expenses = get_all_expenses(expense_file_path)

    # No expenses yet
    if not expenses:

        st.info("📝 No expenses added yet.")

        return

    # --------------------------------------
    # TOTAL SPENT
    # --------------------------------------

    total_spent = sum(
        expense.amount
        for expense in expenses
    )

    # --------------------------------------
    # EXPENSES BY CATEGORY
    # --------------------------------------

    amount_by_category = {}

    for expense in expenses:

        category = expense.category

        if category in amount_by_category:

            amount_by_category[category] += expense.amount

        else:

            amount_by_category[category] = expense.amount

    # --------------------------------------
    # REMAINING BUDGET
    # --------------------------------------

    remaining_budget = budget - total_spent

    # --------------------------------------
    # DAYS REMAINING
    # --------------------------------------

    now = datetime.now()

    days_in_month = calendar.monthrange(
        now.year,
        now.month
    )[1]

    remaining_days = days_in_month - now.day

    # --------------------------------------
    # DAILY BUDGET
    # --------------------------------------

    if remaining_days > 0:

        daily_budget = (
            remaining_budget / remaining_days
        )

    else:

        daily_budget = remaining_budget

    # ======================================
    # DISPLAY SUMMARY
    # ======================================

    st.subheader("📊 Expense Summary")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "💸 Total Spent",
            f"₹{total_spent:,.2f}"
        )

    with col2:

        st.metric(
            "💰 Budget Remaining",
            f"₹{remaining_budget:,.2f}"
        )

    # ======================================
    # CATEGORY SUMMARY
    # ======================================

    st.subheader("📈 Expenses by Category")

    for category, amount in amount_by_category.items():

        st.write(
            f"**{category}:** ₹{amount:,.2f}"
        )

    # ======================================
    # DAILY BUDGET
    # ======================================

    st.write(
        f"📅 **Remaining days this month:** "
        f"{remaining_days}"
    )

    if remaining_budget > 0:

        st.success(
            f"👉 You can spend approximately "
            f"**₹{daily_budget:,.2f} per day**."
        )

    elif remaining_budget == 0:

        st.warning(
            "⚠️ You have used your entire budget."
        )

    else:

        st.error(
            f"⚠️ You are "
            f"**₹{abs(remaining_budget):,.2f} "
            f"over budget!**"
        )


# ==========================================
# ADD NEW EXPENSE
# ==========================================

st.subheader("➕ Add New Expense")


expense_name = st.text_input(
    "Expense name",
    placeholder="e.g. Lunch, Rent, Netflix..."
)


expense_amount = st.number_input(
    "Expense amount (₹)",
    min_value=0.0,
    step=10.0,
    format="%.2f"
)


expense_category = st.selectbox(
    "Select category",
    EXPENSE_CATEGORIES
)


if st.button(
    "💾 Add Expense",
    use_container_width=True
):

    # Check expense name
    if not expense_name.strip():

        st.warning(
            "⚠️ Please enter an expense name."
        )

    # Check expense amount
    elif expense_amount <= 0:

        st.warning(
            "⚠️ Please enter an amount greater than ₹0."
        )

    else:

        # Create Expense object
        new_expense = Expense(
            name=expense_name.strip(),
            amount=expense_amount,
            category=expense_category
        )

        # Save to CSV
        save_expense_to_file(
            new_expense,
            EXPENSE_FILE_PATH
        )

        st.success(
            f"✅ Added **{expense_name}** "
            f"— ₹{expense_amount:,.2f}"
        )

        st.rerun()


summarize_expense(
    EXPENSE_FILE_PATH,
    budget
)

expenses = get_all_expenses(
    EXPENSE_FILE_PATH
)


if expenses:

    st.subheader("📋 All Expenses")

    for expense in reversed(expenses):

        st.write(
            f"**{expense.name}** — "
            f"₹{expense.amount:,.2f} — "
            f"{expense.category}"
        )
