import calendar 
from datetime import datetime
from expense import Expense

def main():
   print(f"🏃‍♂️ Running Expense tracker!!")
   expense_file_path = "expenses.csv"
   budget = 2000
# Get user input for expense. 
   expense = get_user_expense()

# write their expesnse to a file.
  
   save_expense_to_file(expense, expense_file_path)

# read file and summrize expensesclo.
   summarize_expense(expense_file_path, budget)

def get_user_expense():
  print(f"getting user Expense!!")
  expense_name = input("Enter expense name: ")
  expense_amount = float(input("Enter expense amount: "))
  expense_categories = [
    "🍔Food", 
    "🏡Home", 
    "💻Work",
    "🎮Fun", 
    "🌀Misc",
    ]

  while True:
    print("Select a category: ")
    for i, category_name in enumerate(expense_categories):
      print(f"  {i + 1}. {category_name}")

    value_range = f"[1 - {len(expense_categories)}]"
    selected_index = int(input(f"Enter a category number {value_range}: ")) -1


    if selected_index in range(len(expense_categories)):
     selected_category = expense_categories[selected_index]
     new_expense = Expense(name = expense_name, category=selected_category, amount= expense_amount
     )
     return new_expense
    else:
     print("Invalid category. please try againnn..!!!")

def save_expense_to_file(expense, expense_file_path):
      print(f"💾 saving user Expense: {expense} to {expense_file_path}")
      with open(expense_file_path, "a", encoding="utf=8") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n") 

        
      def green(text):
          return f"\033[92m{text}\033[0m"
        
def summarize_expense(expense_file_path, budget):
  print(f"📑 summarizing user Expense...!!")
  expenses: list[Expense] = []

  with open(expense_file_path, "r", encoding= "utf-8") as f:
    lines = f.readlines()
    for line in lines:
      if not line.strip():
        continue
      expense_name, expense_amount, expense_category = line.strip().split(",")
      line_expense = Expense(
        name=expense_name, amount=float(expense_amount), category=expense_category 
      )
      expenses.append(line_expense)

  amount_by_category = {}
  for expense in expenses:
    key = expense.category
    if key in amount_by_category:
      amount_by_category[key] += expense.amount
    else:
      amount_by_category[key] = expense.amount 
      print("Expenses By category📈:")

    for key, amount in amount_by_category.items():
      print(f"     {key}: ${amount:.2f}")

      total_spent = sum([ex.amount for ex in expenses])
      print(f"📤You've spent ${total_spent:.2f} this month!!")

      remaining_budget = budget - total_spent
      print(f"💸Budget Remaining: ${remaining_budget:.2f} this month!!")

      now = datetime.now()
      days_in_month = calendar.monthrange(now.year, now.month)[1]
      remaining_days = days_in_month - now.day
      print("Remaining days in current month:", remaining_days)
      def green(text):
          return f"\033[92m{text}\033[0m"

      daily_budget = remaining_budget / remaining_days
      print(green(f"👉 Budget per Day: ${daily_budget:.2f}"))


if __name__ == "__main__": #__name__ is a special types of variable and it is equal to __main__ when we run as a file and it is only be true when we run it instead of importing it. 
 main()


 