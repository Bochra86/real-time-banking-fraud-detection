import streamlit as st
import pandas as pd
import time
from dotenv import load_dotenv
import os

from sqlalchemy import create_engine
from urllib.parse import quote_plus

load_dotenv()

#Credentials
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = quote_plus(os.getenv("DB_PASSWORD"))
db_port = os.getenv("DB_PORT")

# PostgreSQL Connection
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

# Streamlit Configuration
st.set_page_config(
    page_title="Banking Fraud Dashboard",
    layout="wide"
)

st.title("🚨 Real-Time Banking Fraud Dashboard")

st.caption("Dashboard refreshes every 5 seconds")


# Dashboard Placeholder
placeholder = st.empty()


while True:

    with placeholder.container():

        try:

            # Read data from PostgreSQL
            df = pd.read_sql(
                "SELECT * FROM suspicious_transactions",
                engine
            )

            if not df.empty:

                # Metrics
                total_suspicious = len(df)

                total_amount = df["amount"].sum()

                average_amount = df["amount"].mean()

                highest_amount = df["amount"].max()

                city_counts = df["city"].value_counts()

                # KPI Metrics
                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "Suspicious Transactions",
                    total_suspicious
                )

                col2.metric(
                    "Total Fraud Amount",
                    f"${total_amount:.2f}"
                )

                col3.metric(
                    "Average Fraud Amount",
                    f"${average_amount:.2f}"
                )

                col4.metric(
                    "Highest Fraud Amount",
                    f"${highest_amount:.2f}"
                )

                # Fraud Amount Distribution
                st.subheader("Fraud Amount Distribution")

                st.line_chart(df["amount"])

                # Fraud by City
                st.subheader("Fraud Transactions by City")

                st.bar_chart(city_counts)

                # Latest Transactions
                st.subheader("Latest Suspicious Transactions")

                st.dataframe(
                    df.sort_values(
                        by="created_at",
                        ascending=False
                    )
                )

            else:

                st.warning("No suspicious transactions found.")

        except Exception as error:

            st.error(f"Database Error: {error}")

    time.sleep(5)