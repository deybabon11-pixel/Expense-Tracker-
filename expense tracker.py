import csv
import os
from datetime import datetime

DATA_FILE = "expenses.csv"
BUDGET_LIMIT = 12000.0

def init_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Date", "Category", "Description", "Type", "Amount"])

def get_transactions():
    transactions = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row["Amount"] = float(row["Amount"])
                    transactions.append(row)
                except (ValueError, KeyError):
                    continue
    return transactions

def save_transaction(desc, amount, category, tx_type):
    transactions = get_transactions()
    new_id = str(len(transactions) + 1)
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([new_id, date_str, category, desc, tx_type, amount])
    print(f"\n[+] Successfully added: {desc} (₹{amount:.2f})")

def show_summary():
    transactions = get_transactions()
    income = sum(t["Amount"] for t in transactions if t["Type"].lower() == "income")
    expense = sum(t["Amount"] for t in transactions if t["Type"].lower() == "expense")
    balance = income - expense
    
    spent_pct = (expense / BUDGET_LIMIT) * 100 if BUDGET_LIMIT > 0 else 0

    print("\n" + "=" * 45)
    print("           FINANCIAL OVERVIEW")
    print("=" * 45)
    print(f" Total Income  : ₹{income:,.2f}")
    print(f" Total Expense : ₹{expense:,.2f}")
    print(f" Net Balance   : ₹{balance:,.2f}")
    print("-" * 45)
    print(f" Monthly Budget: ₹{BUDGET_LIMIT:,.0f} | Spent: {spent_pct:.1f}%")
    if spent_pct >= 80:
        print(" [!] WARNING: You have spent over 80% of your budget!")
    print("=" * 45)

def show_history():
    transactions = get_transactions()
    if not transactions:
        print("\nNo transactions recorded yet.")
        return

    print("\n" + "=" * 65)
    print(f"{'ID':<4} {'Date':<12} {'Type':<8} {'Category':<18} {'Amount':<10} {'Description'}")
    print("-" * 65)
    for t in transactions:
        sign = "+" if t["Type"].lower() == "income" else "-"
        amt_str = f"{sign}₹{t['Amount']:.2f}"
        print(f"{t['ID']:<4} {t['Date']:<12} {t['Type']:<8} {t['Category']:<18} {amt_str:<10} {t['Description']}")
    print("=" * 65)

def main():
    init_file()
    
    # Initial seed data for demo
    if not get_transactions():
        save_transaction("Monthly Allowance", 8000.0, "Salary & Freelance", "Income")
        save_transaction("Metro Recharge", 300.0, "Transport", "Expense")
        save_transaction("Campus Cafeteria", 180.0, "Food & Dining", "Expense")

    while True:
        print("\n=== EXPENSE TRACKER (PYTHON SYSTEM) ===")
        print("1. View Financial Summary")
        print("2. View All Transactions")
        print("3. Add New Transaction")
        print("4. Quick Tag Entry")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            show_summary()
        elif choice == "2":
            show_history()
        elif choice == "3":
            desc = input("Description: ").strip()
            try:
                amount = float(input("Amount (₹): ").strip())
                if amount <= 0:
                    print("Amount must be positive.")
                    continue
            except ValueError:
                print("Invalid amount entered.")
                continue

            print("Type: 1. Expense | 2. Income")
            t_choice = input("Select Type (1/2): ").strip()
            tx_type = "Income" if t_choice == "2" else "Expense"

            print("Categories: Food, Transport, Education, Bills, Salary, Others")
            cat = input("Category: ").strip() or "Others"

            save_transaction(desc, amount, cat, tx_type)

        elif choice == "4":
            print("\nQuick Tags:")
            print("1. 🚇 Metro Fare (₹30)")
            print("2. ☕ Chai & Snacks (₹40)")
            print("3. 📚 College Xerox (₹120)")
            print("4. 📶 Data Recharge (₹499)")
            q_choice = input("Select Quick Tag (1-4): ").strip()
            
            tags = {
                "1": ("Metro / Train Fare", 30.0, "Transport", "Expense"),
                "2": ("Chai & Snacks", 40.0, "Food & Dining", "Expense"),
                "3": ("College Xerox / Stationary", 120.0, "Education", "Expense"),
                "4": ("Data / Phone Recharge", 499.0, "Bills", "Expense")
            }
            if q_choice in tags:
                d, a, c, t = tags[q_choice]
                save_transaction(d, a, c, t)
            else:
                print("Invalid quick tag.")

        elif choice == "5":
            print("\nExiting program. All data saved to expenses.csv.")
            break
        else:
            print("Invalid selection. Please choose between 1 and 5.")

if __name__ == "__main__":
    main()
