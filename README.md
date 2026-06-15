# 🎓 Student Expense Tracker Pro

A Python command-line application designed to help students track and manage their daily expenses such as food, travel, recharge, and other categories. The application stores data locally using JSON, making it lightweight, offline-friendly, and easy to use without any external dependencies.

## ✨ Features
* **Add a new expense** with date, amount, and category.
* **View all recorded expenses** in a structured table format.
* **Calculate and display** the total amount spent.
* **Identify** the highest spending category.
* **Set a monthly budget** and receive warnings when spending exceeds the limit.
* **Search expenses** by date or category.
* **Delete expense records** using unique IDs.
* **View advanced analytics** including budget usage, average expense, highest expense, lowest expense, and category-wise spending breakdown.
* **Export expense data** to TXT and CSV reports.
* **Persistent storage** using JSON so data remains available across sessions.

## 🛠️ Technologies Used
* Python 3
* Dataclasses
* JSON
* CSV
* Pathlib
* Type Hints

## 🚀 How to Run
1. Ensure Python 3 is installed on your system.
2. Open a terminal in the project directory.
3. Run the following command:
   ```bash
   python3 expense_tracker.py
