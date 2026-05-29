import streamlit as st
import pandas as pd
import time
import os

st.set_page_config(page_title="Banking Fraud Dashboard", layout="wide")

st.title("🚨 Real-Time Banking Fraud Dashboard")

csv_file = "output/suspicious_transactions.csv"

placeholder = st.empty()

while True:

    with placeholder.container():

        st.subheader("Suspicious Transactions")

        if os.path.exists(csv_file):

            df = pd.read_csv(csv_file)

            total_suspicious = len(df)

            total_amount = df["amount"].sum()

            average_amount = df["amount"].mean()

            col1, col2, col3 = st.columns(3)

            col1.metric("Suspicious Transactions", total_suspicious)

            col2.metric("Total Fraud Amount", f"${total_amount:.2f}")

            col3.metric("Average Fraud Amount", f"${average_amount:.2f}")

            st.dataframe(df)

            st.subheader("Fraud Amount Distribution")

            st.bar_chart(df["amount"])

        else:

            st.warning("No suspicious transactions yet.")

    time.sleep(5)