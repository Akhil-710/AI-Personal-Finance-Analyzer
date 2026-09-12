import pandas as pd
from pathlib import Path


# -----------------------------
# Load Clean Dataset
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Data" / "clean_transactions.csv"

df = pd.read_csv(DATA_PATH)

# Convert date
df["Date"] = pd.to_datetime(df["Date"])


# -----------------------------
# Separate Income & Expenses
# -----------------------------

income = df[df["Transaction Type"] == "Income"]
expenses = df[df["Transaction Type"] == "Expense"]


# -----------------------------
# Basic Financial Metrics
# -----------------------------

total_income = income["Amount"].sum()
total_expenses = expenses["Amount"].sum()

net_savings = total_income - total_expenses

if total_income > 0:
    savings_rate = (net_savings / total_income) * 100
else:
    savings_rate = 0


# -----------------------------
# Monthly Spending
# -----------------------------

expenses = expenses.copy()

expenses["Month"] = expenses["Date"].dt.to_period("M")

monthly_spending = (
    expenses
    .groupby("Month")["Amount"]
    .sum()
    .reset_index()
)

monthly_spending["Month"] = monthly_spending["Month"].astype(str)


# -----------------------------
# Category Spending
# -----------------------------

category_spending = (
    expenses
    .groupby("Category")["Amount"]
    .sum()
    .sort_values(ascending=False)
)


# -----------------------------
# Largest Transaction
# -----------------------------

largest_transaction = expenses.loc[
    expenses["Amount"].idxmax()
]


# -----------------------------
# Average Expense
# -----------------------------

average_expense = expenses["Amount"].mean()


# -----------------------------
# Display Results
# -----------------------------

print("\n========== FINANCIAL SUMMARY ==========")

print(f"Total Income      : ₹{total_income:,.2f}")
print(f"Total Expenses    : ₹{total_expenses:,.2f}")
print(f"Net Savings       : ₹{net_savings:,.2f}")
print(f"Savings Rate      : {savings_rate:.2f}%")
print(f"Average Expense   : ₹{average_expense:,.2f}")

print("\n========== CATEGORY SPENDING ==========")

print(category_spending)

print("\n========== MONTHLY SPENDING ==========")

print(monthly_spending)

print("\n========== LARGEST EXPENSE ==========")

print(largest_transaction)


# -----------------------------
# Save Analytics Data
# -----------------------------

monthly_spending.to_csv(
    BASE_DIR / "data" / "monthly_spending.csv",
    index=False
)

category_spending.reset_index().to_csv(
    BASE_DIR / "data" / "category_spending.csv",
    index=False
)

print("\nAnalytics completed successfully!")