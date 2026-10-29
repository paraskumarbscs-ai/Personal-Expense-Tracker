
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import date

# ---------------- Configuration ----------------
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

DATA_FILE = Path(__file__).parent / "expenses.csv"

CATEGORIES = [
    "Food", "Transport", "Shopping",
    "Bills", "Education", "Health", "Other"
]

COLUMNS = ["Date", "Category", "Description", "Amount"]

# ---------------- Data functions ----------------
def load_expenses():
    if DATA_FILE.exists():
        try:
            df = pd.read_csv(DATA_FILE)
            if list(df.columns) == COLUMNS:
                df["Date"] = pd.to_datetime(
                    df["Date"], errors="coerce"
                )
                df["Amount"] = pd.to_numeric(
                    df["Amount"], errors="coerce"
                )
                df = df.dropna(subset=["Date", "Amount"])
                return df
        except (ValueError, OSError, pd.errors.ParserError):
            pass

    return pd.DataFrame(columns=COLUMNS)


def save_expenses(df):
    df.to_csv(DATA_FILE, index=False, date_format="%Y-%m-%d")


# ---------------- Load application data ----------------
if "expenses" not in st.session_state:
    st.session_state.expenses = load_expenses()

df = st.session_state.expenses

# ---------------- Sidebar ----------------
st.sidebar.title("💰 Expense Tracker")
page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Add Expense", "All Transactions"]
)

st.sidebar.caption("Track your money, one expense at a time.")

# ---------------- Dashboard ----------------
if page == "Dashboard":
    st.title("📊 Financial Dashboard")
    st.write("Understand your spending at a glance.")

    if df.empty:
        st.info("No expenses yet. Open Add Expense to get started.")
    else:
        df["Month"] = df["Date"].dt.to_period("M").astype(str)

        months = sorted(df["Month"].unique(), reverse=True)
        selected_month = st.selectbox("Select month", months)

        monthly = df[df["Month"] == selected_month]
        total = monthly["Amount"].sum()
        count = len(monthly)
        average = monthly["Amount"].mean() if count else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Spending", f"Rs. {total:,.2f}")
        col2.metric("Transactions", count)
        col3.metric("Average Expense", f"Rs. {average:,.2f}")

        st.divider()

        left, right = st.columns(2)

        with left:
            st.subheader("Spending by Category")
            category_totals = (
                monthly.groupby("Category")["Amount"]
                .sum()
                .reset_index()
            )

            if not category_totals.empty:
                fig = px.pie(
                    category_totals,
                    names="Category",
                    values="Amount",
                    hole=0.45
                )
                st.plotly_chart(fig, use_container_width=True)

        with right:
            st.subheader("Daily Spending")
            daily = (
                monthly.assign(
                    Day=monthly["Date"].dt.strftime("%Y-%m-%d")
                )
                .groupby("Day", as_index=False)["Amount"]
                .sum()
            )

            fig = px.bar(
                daily,
                x="Day",
                y="Amount",
                labels={"Amount": "Spending (Rs.)"}
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Recent Transactions")
        st.dataframe(
            monthly.sort_values("Date", ascending=False)
            [COLUMNS].head(10),
            use_container_width=True,
            hide_index=True
        )

# ---------------- Add Expense ----------------
elif page == "Add Expense":
    st.title("➕ Add a New Expense")

    with st.form("expense_form", clear_on_submit=True):
        expense_date = st.date_input("Date", value=date.today())
        category = st.selectbox("Category", CATEGORIES)
        description = st.text_input(
            "Description", placeholder="e.g. Lunch"
        )
        amount = st.number_input(
            "Amount (Rs.)",
            min_value=0.01,
            max_value=100000000.0,
            value=100.0,
            step=50.0
        )

        submitted = st.form_submit_button(
            "Save Expense", use_container_width=True
        )

        if submitted:
            new_expense = pd.DataFrame([{
                "Date": pd.Timestamp(expense_date),
                "Category": category,
                "Description": description.strip() or category,
                "Amount": amount
            }])

            updated = pd.concat(
                [st.session_state.expenses, new_expense],
                ignore_index=True
            )

            save_expenses(updated)
            st.session_state.expenses = updated
            st.success("Expense saved successfully!")
            st.rerun()

# ---------------- All Transactions ----------------
elif page == "All Transactions":
    st.title("📋 All Transactions")

    if df.empty:
        st.info("No transactions available.")
    else:
        categories = ["All"] + sorted(df["Category"].unique())
        selected_category = st.selectbox(
            "Filter by category", categories
        )

        filtered = df.copy()

        if selected_category != "All":
            filtered = filtered[
                filtered["Category"] == selected_category
            ]

        st.dataframe(
            filtered.sort_values("Date", ascending=False)[COLUMNS],
            use_container_width=True,
            hide_index=True
        )

        csv_data = filtered[COLUMNS].to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Transactions as CSV",
            data=csv_data,
            file_name="my_expenses.csv",
            mime="text/csv"
        )

        st.caption(f"Showing {len(filtered)} transactions.")
