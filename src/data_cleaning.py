import pandas as pd
from pathlib import Path


# -----------------------------
# 1. Load the raw dataset
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

raw_file = BASE_DIR / "Data" / "transactions.csv"
clean_file = BASE_DIR / "Data" / "clean_transactions.csv"

df = pd.read_csv(raw_file)

print("Dataset loaded successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\nFirst 5 rows:")
print(df.head())


# -----------------------------
# 2. Check data types
# -----------------------------

print("\nData types:")
print(df.dtypes)


# -----------------------------
# 3. Check missing values
# -----------------------------

print("\nMissing values:")
print(df.isnull().sum())


# -----------------------------
# 4. Check duplicate rows
# -----------------------------

duplicates = df.duplicated().sum()

print(f"\nDuplicate rows: {duplicates}")


# -----------------------------
# 5. Convert Date column
# -----------------------------

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")


# -----------------------------
# 6. Clean Description
# -----------------------------

df["Description"] = df["Description"].fillna("Unknown")


# -----------------------------
# 7. Clean Category
# -----------------------------

df["Category"] = df["Category"].fillna("Uncategorized")


# -----------------------------
# 8. Handle missing Amount
# -----------------------------

df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

df["Amount"] = df["Amount"].fillna(0)


# -----------------------------
# 9. Remove duplicate rows
# -----------------------------

df = df.drop_duplicates()


# -----------------------------
# 10. Validate transaction amounts
# -----------------------------

invalid_amounts = (df["Amount"] < 0).sum()

print(f"\nInvalid negative amounts: {invalid_amounts}")

df = df[df["Amount"] >= 0]


# -----------------------------
# 11. Sort by date
# -----------------------------

df = df.sort_values("Date")


# -----------------------------
# 12. Save cleaned dataset
# -----------------------------

df.to_csv(clean_file, index=False)

print("\nCleaning completed!")
print(f"Clean dataset saved to: {clean_file}")

print("\nFinal dataset:")
print(df.head())