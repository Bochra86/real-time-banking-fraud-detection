import csv
import os


CSV_FILE = "data/all_transactions.csv"


def save_transaction(transaction: dict):

    os.makedirs("data", exist_ok=True)

    file_exists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="") as f:

        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "transaction_id",
                "user_id",
                "amount",
                "city"
            ])

        writer.writerow([
            transaction["transaction_id"],
            transaction["user_id"],
            transaction["amount"],
            transaction["city"]
        ])
