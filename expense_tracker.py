import json
import csv
import uuid
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

# --- Configuration ---
DATA_FILE = Path("expenses.json")

# --- Data Models ---
@dataclass
class Expense:
    id: str
    date: str
    amount: float
    category: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Expense':
        return cls(**data)

# --- Main Application ---
class ExpenseTrackerPro:
    DEFAULT_DATA = [
        {"id": "A1B2C3", "date": "2026-06-10", "amount": 450.0, "category": "Food"},
        {"id": "X9Y8Z7", "date": "2026-06-12", "amount": 1200.0, "category": "Travel"},
        {"id": "M4N5P6", "date": "2026-06-15", "amount": 399.0, "category": "Recharge"}
    ]

    def __init__(self) -> None:
        self.expenses: List[Expense] = []
        self.budget: float = 5000.0
        self.load_data()

    def load_data(self) -> None:
        if DATA_FILE.exists():
            try:
                with DATA_FILE.open("r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.expenses = [Expense.from_dict(exp) for exp in data.get("expenses", [])]
                    self.budget = data.get("budget", 5000.0)
            except (json.JSONDecodeError, KeyError):
                # Fix: Save defaults immediately to overwrite corrupted file
                self._load_defaults()
                self.save_data()
        else:
            self._load_defaults()
            self.save_data()

    def _load_defaults(self) -> None:
        self.expenses = [Expense.from_dict(exp) for exp in self.DEFAULT_DATA]

    def save_data(self) -> None:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump({
                "expenses": [exp.to_dict() for exp in self.expenses],
                "budget": self.budget
            }, file, indent=4)

    def add_expense(self) -> None:
        print("\n--- ADD EXPENSE ---")
        date_input = input("Date (YYYY-MM-DD) [Press Enter for Today]: ").strip()
        date_str = date_input if date_input else datetime.today().strftime("%Y-%m-%d")
        
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("❌ Invalid date format.")
            return

        try:
            amount = float(input("Amount (₹): "))
            if amount <= 0:
                print("❌ Amount must be positive.")
                return
        except ValueError:
            print("❌ Invalid amount.")
            return

        valid_categories = ["Food", "Travel", "Recharge", "Other"]
        category = input(f"Category ({'/'.join(valid_categories)}): ").strip().capitalize()
        if category not in valid_categories:
            category = "Other"

        new_expense = Expense(id=uuid.uuid4().hex[:6].upper(), date=date_str, amount=amount, category=category)
        self.expenses.append(new_expense)
        self.save_data()
        
        print("✅ Expense added successfully.")
        self.check_budget()

    def view_expenses(self, expenses_to_show: List[Expense] = None) -> None:
        display_list = expenses_to_show if expenses_to_show is not None else self.expenses
        
        print("\n--- EXPENSE RECORD ---")
        if not display_list:
            print("No expenses found.")
            return

        print("-" * 60)
        print(f"{'ID':<10}{'Date':<15}{'Category':<15}{'Amount (₹)':<15}")
        print("-" * 60)

        for exp in sorted(display_list, key=lambda x: x.date, reverse=True):
            print(f"{exp.id:<10}{exp.date:<15}{exp.category:<15}₹{exp.amount:<15.2f}")
        print("-" * 60)

    def view_total_spent(self) -> None:
        total = sum(exp.amount for exp in self.expenses)
        print(f"\n💰 Total Amount Spent: ₹{total:.2f}")
        self.check_budget()

    def view_highest_category(self) -> None:
        if not self.expenses:
            print("\nNo data available.")
            return
            
        category_totals: Dict[str, float] = {}
        for exp in self.expenses:
            category_totals[exp.category] = category_totals.get(exp.category, 0) + exp.amount
            
        top_cat = max(category_totals, key=category_totals.get)
        print(f"\n🏆 Highest Spending Category: {top_cat} (₹{category_totals[top_cat]:.2f})")

    def manage_expenses(self) -> None:
        """Sub-menu for searching and deleting to keep main menu clean."""
        print("\n--- MANAGE EXPENSES ---")
        print("1. Search Expenses")
        print("2. Delete an Expense")
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            query = input("\nSearch by Category or Date (e.g., 'Food' or '2026-06'): ").strip().lower()
            results = [exp for exp in self.expenses if query in exp.category.lower() or query in exp.date]
            self.view_expenses(results)
        elif choice == "2":
            self.view_expenses()
            if not self.expenses: return
            
            # Fix: Graceful exit on empty ID
            exp_id = input("\nEnter the ID of the expense to delete (or press Enter to cancel): ").strip().upper()
            if not exp_id:
                return
                
            original_count = len(self.expenses)
            self.expenses = [exp for exp in self.expenses if exp.id != exp_id]
            if len(self.expenses) < original_count:
                self.save_data()
                print(f"✅ Expense {exp_id} deleted successfully.")
            else:
                print(f"❌ No expense found with ID '{exp_id}'.")
        else:
            print("❌ Invalid option.")

    def view_analytics(self) -> None:
        print("\n--- ADVANCED ANALYTICS ---")
        if not self.expenses:
            print("Not enough data for analytics.")
            return

        amounts = [exp.amount for exp in self.expenses]
        total = sum(amounts)
        
        remaining = self.budget - total
        usage_pct = (total / self.budget) * 100 if self.budget > 0 else 0

        print(f"\n📊 Monthly Budget Usage:")
        print(f"  Budget:    ₹{self.budget:.2f}")
        print(f"  Spent:     ₹{total:.2f}")
        if remaining >= 0:
            print(f"  Remaining: ₹{remaining:.2f}")
        else:
            print(f"  Overspent: ₹{abs(remaining):.2f} ⚠️")
        print(f"  Usage:     {usage_pct:.1f}%")

        print(f"\n📉 Overall Statistics:")
        print(f"  Total Entries:    {len(self.expenses)}")
        print(f"  Average Expense:  ₹{(total / len(self.expenses)):.2f}")
        # Fix: Re-added Highest Expense
        print(f"  Highest Expense:  ₹{max(amounts):.2f}")
        print(f"  Lowest Expense:   ₹{min(amounts):.2f}")

        category_totals: Dict[str, float] = {}
        for exp in self.expenses:
            category_totals[exp.category] = category_totals.get(exp.category, 0) + exp.amount

        print(f"\n🥧 Category Breakdown:")
        for cat, amt in sorted(category_totals.items(), key=lambda item: item[1], reverse=True):
            print(f"  {cat:<15} ₹{amt:<10.2f} ({(amt/total)*100:.1f}%)")

    def set_budget(self) -> None:
        print("\n--- SET BUDGET ---")
        try:
            new_budget = float(input(f"Enter Monthly Budget (Current: ₹{self.budget:.2f}): "))
            if new_budget <= 0:
                print("❌ Budget must be positive.")
                return
            self.budget = new_budget
            self.save_data()
            print(f"✅ Budget updated to ₹{self.budget:.2f}")
        except ValueError:
            print("❌ Invalid budget format.")

    def check_budget(self) -> None:
        total = sum(exp.amount for exp in self.expenses)
        if total > self.budget:
            print(f"\n⚠️ WARNING: BUDGET EXCEEDED")
            print(f"You are over budget by ₹{total - self.budget:.2f}!")

    def export_reports(self) -> None:
        if not self.expenses:
            print("No data to export.")
            return

        txt_file = Path("expense_report.txt")
        with txt_file.open("w", encoding="utf-8") as f:
            f.write("STUDENT EXPENSE REPORT\n" + "=" * 40 + "\n\n")
            for exp in sorted(self.expenses, key=lambda x: x.date):
                f.write(f"{exp.date} | {exp.category:<10} | ₹{exp.amount:.2f}\n")
            total = sum(exp.amount for exp in self.expenses)
            f.write("\n" + "=" * 40 + f"\nTotal Spent: ₹{total:.2f}\nMonthly Budget: ₹{self.budget:.2f}\n")

        csv_file = Path("expenses_export.csv")
        with csv_file.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "date", "amount", "category"])
            writer.writeheader()
            writer.writerows([exp.to_dict() for exp in self.expenses])

        print("\n✅ Reports successfully exported!")
        print(f"  📄 Text: {txt_file.absolute()}")
        print(f"  📊 CSV:  {csv_file.absolute()}")

    def menu(self) -> None:
        while True:
            print("\n===== 🎓 EXPENSE TRACKER PRO =====")
            print("1. Add Expense")
            print("2. View All Expenses")
            print("3. Total Amount Spent")
            print("4. Highest Spending Category")
            print("5. Search & Manage Data")
            print("6. Advanced Analytics & Budget")
            print("7. Set Monthly Budget")
            print("8. Export Reports (TXT & CSV)")
            print("9. Exit")

            choice = input("\nEnter choice (1-9): ").strip()

            if choice == "1": self.add_expense()
            elif choice == "2": self.view_expenses()
            elif choice == "3": self.view_total_spent()
            elif choice == "4": self.view_highest_category()
            elif choice == "5": self.manage_expenses()
            elif choice == "6": self.view_analytics()
            elif choice == "7": self.set_budget()
            elif choice == "8": self.export_reports()
            elif choice == "9":
                print("Goodbye! Keep your finances in check! 👋")
                break
            else:
                print("❌ Invalid choice. Please select 1-9.")

if __name__ == "__main__":
    try:
        app = ExpenseTrackerPro()
        app.menu()
    except KeyboardInterrupt:
        print("\n\nApplication exited safely. 👋")