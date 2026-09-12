import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Personal Finance Analyzer",
    page_icon="💰",
    layout="wide"
)

st.markdown("""
<style>
.main-title { font-size: 2.2rem; font-weight: 700; margin-bottom: 0.15rem; }
.subtitle { color: #666; font-size: 1rem; margin-bottom: 1rem; }
div[data-testid="stMetric"] { border: 1px solid rgba(128,128,128,0.20); border-radius: 10px; padding: 14px; background: rgba(128,128,128,0.04); }
.section-note { color: #666; font-size: 0.9rem; margin-top: -0.45rem; margin-bottom: 0.8rem; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("💰 Finance Analyzer")


# ============================================================
# LOAD DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "clean_transactions.csv"


st.sidebar.subheader("📂 Transaction Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload your transaction CSV",
    type=["csv"]
)


if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.sidebar.success(
        f"Using uploaded file: {uploaded_file.name}"
    )

else:

    df = pd.read_csv(DATA_PATH)

    st.sidebar.info(
        "Using default transaction dataset"
    )


# ============================================================
# VALIDATE CSV
# ============================================================

required_columns = [
    "Date",
    "Description",
    "Amount",
    "Transaction Type",
    "Category"
]


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


if missing_columns:

    st.error(
        "Invalid CSV file. Missing columns: "
        + ", ".join(missing_columns)
    )

    st.stop()


# ============================================================
# CLEAN DATA
# ============================================================

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

df["Description"] = df["Description"].fillna(
    "Unknown"
)

df["Category"] = df["Category"].fillna(
    "Uncategorized"
)

df["Amount"] = pd.to_numeric(
    df["Amount"],
    errors="coerce"
).fillna(0)


# Remove duplicate transactions
df = df.drop_duplicates()


# Remove rows with invalid dates
df = df.dropna(
    subset=["Date"]
)


# ============================================================
# DATASET SUMMARY
# ============================================================

st.sidebar.caption(
    f"Transactions loaded: {len(df):,}"
)
st.sidebar.divider()


# ============================================================
# FILTERS
# ============================================================

st.sidebar.subheader("Filters")


months = sorted(
    df["Date"].dt.strftime("%Y-%m").unique()
)


selected_month = st.sidebar.selectbox(
    "Select Month",
    ["All"] + months
)


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df.copy()


if selected_month != "All":

    filtered_df = filtered_df[
        filtered_df["Date"].dt.strftime("%Y-%m")
        == selected_month
    ]


# ============================================================
# INCOME / EXPENSE DATA
# ============================================================

income_df = filtered_df[
    filtered_df["Transaction Type"] == "Income"
]


expense_df = filtered_df[
    filtered_df["Transaction Type"] == "Expense"
]


# ============================================================
# FINANCIAL CALCULATIONS
# ============================================================

total_income = income_df["Amount"].sum()

total_expenses = expense_df["Amount"].sum()

net_savings = total_income - total_expenses


if total_income > 0:

    savings_rate = (
        net_savings / total_income
    ) * 100

else:

    savings_rate = 0


# ============================================================
# HEADER
# ============================================================

st.markdown('<div class="main-title">💰 Personal Finance Analyzer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Track spending, compare budgets, and understand your financial habits from transaction data.</div>',
    unsafe_allow_html=True
)


if selected_month == "All":

    st.caption(
        "Showing data for the full year"
    )

else:

    st.caption(
        f"Showing data for {selected_month}"
    )


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("Financial Overview")
st.markdown('<div class="section-note">A quick view of income, expenses, savings, and savings rate for the selected period.</div>', unsafe_allow_html=True)


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "💵 Total Income",
    f"₹{total_income:,.0f}"
)


col2.metric(
    "💸 Total Expenses",
    f"₹{total_expenses:,.0f}"
)


col3.metric(
    "💰 Net Savings",
    f"₹{net_savings:,.0f}"
)


col4.metric(
    "📈 Savings Rate",
    f"{savings_rate:.1f}%"
)


st.divider()


# ============================================================
# BUDGET PLANNER
# ============================================================

if selected_month != "All":

    st.subheader("🎯 Monthly Budget Planner")


    st.write(
        "Set your spending limits and compare them "
        "with your actual spending."
    )


    budget_categories = [
        "Food",
        "Rent",
        "Shopping",
        "Utilities",
        "Transport",
        "Entertainment",
        "Healthcare",
        "Education"
    ]


    # --------------------------------------------------------
    # DEFAULT MONTHLY BUDGETS
    # --------------------------------------------------------

    default_budgets = {

        "Food": 15000,

        "Rent": 18000,

        "Shopping": 8000,

        "Utilities": 4000,

        "Transport": 5000,

        "Entertainment": 3000,

        "Healthcare": 3000,

        "Education": 3000
    }


    # --------------------------------------------------------
    # BUDGET INPUTS
    # --------------------------------------------------------

    budget_values = {}

    cols = st.columns(4)


    for i, category in enumerate(
        budget_categories
    ):

        with cols[i % 4]:

            budget_values[category] = (
                st.number_input(
                    f"{category} Budget",
                    min_value=0,
                    value=default_budgets[category],
                    step=500,
                    key=f"budget_{category}"
                )
            )


    # ========================================================
    # BUDGET VS ACTUAL CALCULATION
    # ========================================================

    actual_spending = (
        expense_df
        .groupby("Category")["Amount"]
        .sum()
        .to_dict()
    )


    budget_rows = []


    for category in budget_categories:

        budget = budget_values[category]


        actual = actual_spending.get(
            category,
            0
        )


        variance = budget - actual


        if actual > budget:

            status = "Over Budget"

        else:

            status = "Within Budget"


        budget_rows.append({

            "Category": category,

            "Budget": budget,

            "Actual Spending": actual,

            "Variance": variance,

            "Status": status

        })


    budget_df = pd.DataFrame(
        budget_rows
    )


    # ========================================================
    # BUDGET TABLE
    # ========================================================

    st.subheader("📋 Budget vs Actual")


    display_budget = budget_df.copy()


    display_budget["Budget"] = (
        display_budget["Budget"]
        .map(lambda x: f"₹{x:,.0f}")
    )


    display_budget["Actual Spending"] = (
        display_budget["Actual Spending"]
        .map(lambda x: f"₹{x:,.0f}")
    )


    display_budget["Variance"] = (
        display_budget["Variance"]
        .map(lambda x: f"₹{x:,.0f}")
    )


    st.dataframe(
        display_budget,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # BUDGET CHART
    # ========================================================

    budget_chart = budget_df.melt(

        id_vars="Category",

        value_vars=[
            "Budget",
            "Actual Spending"
        ],

        var_name="Type",

        value_name="Amount"
    )


    fig_budget = px.bar(

        budget_chart,

        x="Category",

        y="Amount",

        color="Type",

        barmode="group",

        title="Budget vs Actual Spending",

        labels={
            "Amount": "Amount (₹)"
        }
    )


    fig_budget.update_layout(
        xaxis_tickangle=-45,
        legend_title_text="",
        margin=dict(t=60, l=20, r=20, b=80)
    )
    fig_budget.update_yaxes(tickprefix="₹", separatethousands=True)


    st.plotly_chart(
        fig_budget,
        use_container_width=True
    )


    # ========================================================
    # BUDGET SUMMARY
    # ========================================================

    over_budget = budget_df[
        budget_df["Status"] == "Over Budget"
    ]


    within_budget = budget_df[
        budget_df["Status"] == "Within Budget"
    ]


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Categories Over Budget",
        len(over_budget)
    )


    col2.metric(
        "Categories Within Budget",
        len(within_budget)
    )


    total_budget = budget_df[
        "Budget"
    ].sum()


    total_actual = budget_df[
        "Actual Spending"
    ].sum()


    col3.metric(
        "Total Budget Variance",
        f"₹{total_budget - total_actual:,.0f}"
    )


    # ========================================================
    # BUDGET ALERTS
    # ========================================================

    st.subheader("🚨 Budget Alerts")


    if len(over_budget) == 0:

        st.success(
            "You are within budget across "
            "all tracked categories."
        )


    else:

        for _, row in over_budget.iterrows():

            overspent_amount = (
                row["Actual Spending"]
                - row["Budget"]
            )


            st.warning(

                f"**{row['Category']}** is over budget by "
                f"₹{overspent_amount:,.0f}."

            )


else:

    st.subheader("🎯 Monthly Budget Planner")


    st.info(
        "Select a specific month from the sidebar "
        "to use the Budget Planner."
    )


st.divider()


# ============================================================
# SPENDING BY CATEGORY
# ============================================================

st.subheader("📊 Spending by Category")
st.markdown('<div class="section-note">See where your money is going and which categories contribute most to total spending.</div>', unsafe_allow_html=True)


category_data = (

    expense_df

    .groupby("Category")["Amount"]

    .sum()

    .reset_index()

    .sort_values(
        "Amount",
        ascending=False
    )

)


if category_data.empty:

    st.info(
        "No expense data available for this period."
    )

else:

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # BAR CHART
    # --------------------------------------------------------

    with col1:

        fig_category = px.bar(

            category_data,

            x="Category",

            y="Amount",

            title="Total Spending by Category",

            labels={

                "Amount": "Spending (₹)",

                "Category": "Category"

            }

        )


        fig_category.update_layout(
            xaxis_tickangle=-45,
            margin=dict(t=60, l=20, r=20, b=80)
        )
        fig_category.update_yaxes(tickprefix="₹", separatethousands=True)


        st.plotly_chart(
            fig_category,
            use_container_width=True
        )


    # --------------------------------------------------------
    # PIE CHART
    # --------------------------------------------------------

    with col2:

        fig_pie = px.pie(

            category_data,

            names="Category",

            values="Amount",

            title="Spending Distribution"

        )


        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )


st.divider()


# ============================================================
# MONTHLY SPENDING TREND
# ============================================================

st.subheader("📈 Monthly Spending Trend")
st.markdown('<div class="section-note">Monthly expense trend across the complete dataset.</div>', unsafe_allow_html=True)


# Use complete dataset so the yearly trend
# remains visible even when a month is selected.

all_expenses = df[
    df["Transaction Type"] == "Expense"
].copy()


all_expenses["Month"] = (
    all_expenses["Date"]
    .dt.strftime("%Y-%m")
)


monthly_data = (

    all_expenses

    .groupby("Month")["Amount"]

    .sum()

    .reset_index()

)


if monthly_data.empty:

    st.info(
        "No monthly expense data available."
    )

else:

    fig_monthly = px.line(

        monthly_data,

        x="Month",

        y="Amount",

        markers=True,

        title="Monthly Expenses"

    )


    fig_monthly.update_layout(

        xaxis_title="Month",

        yaxis_title="Expenses (₹)"

    )


    st.plotly_chart(

        fig_monthly,

        use_container_width=True

    )


st.divider()


# ============================================================
# KEY FINANCIAL INSIGHTS
# ============================================================

st.subheader("📌 Key Financial Insights")
st.markdown('<div class="section-note">Rule-based observations generated from your transaction and budget data.</div>', unsafe_allow_html=True)


# ============================================================
# BIGGEST SPENDING CATEGORY
# ============================================================

if not category_data.empty:

    top_category = (
        category_data.iloc[0]["Category"]
    )


    top_category_amount = (
        category_data.iloc[0]["Amount"]
    )


    category_percentage = (

        top_category_amount
        / total_expenses
        * 100

        if total_expenses > 0

        else 0

    )


    st.info(

        f"Your highest spending category is "
        f"**{top_category}**, accounting for "
        f"**₹{top_category_amount:,.0f} "
        f"({category_percentage:.1f}%)** "
        f"of your total expenses."

    )


# ============================================================
# SAVINGS INSIGHT
# ============================================================

if savings_rate >= 20:

    st.success(

        f"Your savings rate is **{savings_rate:.1f}%**, "
        "which indicates strong savings for this period."

    )


elif savings_rate >= 10:

    st.info(

        f"Your savings rate is **{savings_rate:.1f}%**. "
        "There is room to increase your savings further."

    )


else:

    st.warning(

        f"Your savings rate is only "
        f"**{savings_rate:.1f}%**. "
        "Consider reviewing your largest "
        "discretionary expenses."

    )


# ============================================================
# BUDGET INSIGHT
# ============================================================

if selected_month != "All":

    if len(over_budget) > 0:

        worst_budget_category = (

            over_budget

            .assign(

                Overspent=lambda x:
                x["Actual Spending"] - x["Budget"]

            )

            .sort_values(

                "Overspent",

                ascending=False

            )

            .iloc[0]

        )


        st.warning(

            f"**{worst_budget_category['Category']}** "
            f"has the largest budget overrun at "
            f"**₹{worst_budget_category['Overspent']:,.0f}**."

        )


    else:

        st.success(

            "You are within budget across "
            "all tracked categories."

        )


# ============================================================
# HIGHEST-SPENDING MONTH
# ============================================================

if selected_month == "All" and not monthly_data.empty:

    monthly_highest = monthly_data.loc[
        monthly_data["Amount"].idxmax()
    ]


    st.info(

        f"Your highest-spending month was "
        f"**{monthly_highest['Month']}**, "
        f"with expenses of "
        f"**₹{monthly_highest['Amount']:,.0f}**."

    )


st.divider()


# ============================================================
# RECENT TRANSACTIONS
# ============================================================

st.subheader("🧾 Recent Transactions")
st.markdown('<div class="section-note">The 10 most recent transactions in the selected period.</div>', unsafe_allow_html=True)


recent_transactions = (

    filtered_df

    .sort_values(
        "Date",
        ascending=False
    )

    .head(10)

    .copy()

)


recent_transactions["Date"] = (
    recent_transactions["Date"]
    .dt.strftime("%Y-%m-%d")
)


recent_transactions["Amount"] = (

    recent_transactions["Amount"]

    .map(lambda x: f"₹{x:,.0f}")

)


st.dataframe(

    recent_transactions[
        [
            "Date",
            "Description",
            "Category",
            "Transaction Type",
            "Amount"
        ]
    ],

    use_container_width=True,

    hide_index=True

)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Personal Finance Analyzer • "
    "Built with Python, Pandas, Streamlit and Plotly"
)