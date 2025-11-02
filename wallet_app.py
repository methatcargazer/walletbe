import streamlit as st
import pandas as pd
import walletbe  # our backend file

st.set_page_config(page_title="Digital Wallet", page_icon="💰", layout="centered")
st.title("💰 Digital Wallet Dashboard")

walletbe.init_db()

tab1, tab2, tab3 = st.tabs(["➕ Add Transaction", "📋 View Transactions", "📊 Reports"])

# TAB 1: Add Transaction
with tab1:
    st.subheader("Add a new transaction")
    date = st.date_input("Date")
    t_type = st.selectbox("Type", ["income", "expense"])
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    category = st.text_input("Category (e.g. Rent, Salary, Food)")
    desc = st.text_area("Description")

    if st.button("Add Transaction"):
        walletbe.add_transaction(str(date), t_type, amount, category, desc)
        st.success("✅ Transaction added successfully!")

# TAB 2: View Transactions
with tab2:
    st.subheader("All Transactions")
    df = walletbe.get_transactions()
    if df.empty:
        st.info("No transactions found yet.")
    else:
        st.dataframe(df)

# TAB 3: Monthly Report
with tab3:
    st.subheader("Monthly Summary")
    year = st.number_input("Year", min_value=2020, max_value=2100, value=2025)
    month = st.number_input("Month (1-12)", min_value=1, max_value=12, value=10)

    if st.button("Generate Report"):
        report = walletbe.monthly_report(int(year), int(month))
        if report:
            income, expense, savings = report
            st.write(f"**Income:** ₹{income:.2f}")
            st.write(f"**Expenses:** ₹{expense:.2f}")
            st.write(f"**Savings:** ₹{savings:.2f}")
        else:
            st.warning("No data found for that month.")

    # Optional Chart
    df = walletbe.get_transactions()
    if not df.empty:
        chart_df = df.groupby("type")["amount"].sum()
        st.bar_chart(chart_df)
