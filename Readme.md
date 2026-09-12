Personal Finance Analyzer

A Streamlit-based personal finance dashboard that helps users understand spending, monitor savings, plan monthly budgets, and identify important financial patterns from transaction data.

🚀 Live Demo

https://ai-personal-finance-analyzer-stphheztum4pfxpxjevmv7.streamlit.app/

📌 Problem Statement

Many students and early-career professionals have transaction data but do not have a simple way to turn that raw data into useful financial decisions.

Users may know how much money they spent, but it is harder to quickly answer:

Where is most of my money going?

How much am I saving?

Which categories are exceeding my budget?

Which month had the highest spending?

What should I pay attention to?

The product addresses this problem by converting transaction data into a simple, interactive financial dashboard.

🎯 Target Users

Students

Early-career professionals

Young adults who want a simple view of their personal finances


🧩 MVP

The MVP focuses on the core workflow:

Upload transactions → Clean data → Analyze spending → Set budgets → Identify insights

Core MVP Features

Upload a transaction CSV(The uploaded CSV must contain the required columns: Date, Description, Amount, Transaction Type, and Category.)

Validate required CSV columns

Clean missing and invalid data

Calculate income, expenses, net savings, and savings rate

Filter the dashboard by month

Analyze spending by category

View monthly spending trends

Set monthly category budgets

Compare budget vs. actual spending

Identify over-budget categories

Generate rule-based financial insights

View recent transactions

🛠️ Tech Stack

Python

Pandas

Streamlit

Plotly

🔄 How It Works

User uploads a transaction CSV or uses the default dataset.

The application validates the required columns.

Missing values and invalid dates are handled.

Transactions are filtered based on the selected month.

Financial KPIs and spending analysis are calculated.

Users can set category-level monthly budgets.

Budget vs. actual spending is calculated.

Rule-based insights highlight important financial patterns.

Recent transactions are displayed for quick reference.

📊 Dashboard Sections

Financial Overview

Displays:

Total Income

Total Expenses

Net Savings

Savings Rate

Monthly Budget Planner

Allows users to define category-level budgets and compare them with actual spending.

Spending by Category

Shows spending distribution through bar and pie/donut-style visualizations.

Monthly Spending Trend

Shows how expenses change across the year.

Key Financial Insights

Highlights:

Highest spending category

Savings-rate assessment

Budget overruns

Highest-spending month

Recent Transactions

Displays the latest transactions from the selected period.

📁 Project Structure

AI-Personal-Finance-Analyzer/
│
├── data/
│   ├── transactions.csv
│   ├── clean_transactions.csv
│   ├── monthly_spending.csv
│   └── category_spending.csv
│
├── src/
│   ├── generate_data.py
│   ├── data_cleaning.py
│   └── analytics.py
│
├── app.py
├── README.md
└── requirements.txt

▶️ Run Locally

1. Clone the repository

git clone https://github.com/Akhil-710/ai-personal-finance-analyzer.git
cd ai-personal-finance-analyzer

2. Install dependencies

python -m pip install -r requirements.txt

3. Run the application

python -m streamlit run app.py

The application will open in your browser.

🧹 Data Cleaning

The application validates the uploaded CSV and handles common data-quality issues before analysis, including:

Missing descriptions

Missing categories

Missing numeric amounts

Duplicate transactions

Invalid dates

📈 Product Metrics

The product can be evaluated using metrics such as:

Budget creation rate

Savings-goal progress

Insight engagement

Categorization accuracy

Weekly active users

30-day retention

The primary product metric is:

Percentage of active users who make measurable progress toward their monthly savings goal.

🔮 Future Improvements

Possible future iterations include:

Persistent user profiles

Savings-goal tracking

Automatic transaction categorization improvements

Exportable financial reports

More advanced financial recommendations

Authentication and secure cloud storage

👤 Project

Built as a product-oriented data application demonstrating problem definition, MVP design, data processing, analytics, visualization, and deployment.
