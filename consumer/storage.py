import csv
import os

from config.settings import CSV_OUTPUT_FILE


def save_suspicious_transaction(transaction):

    file_exists = os.path.isfile(CSV_OUTPUT_FILE)

    with open(CSV_OUTPUT_FILE, mode="a", newline="") as file:

        writer = csv.DictWriter(file, fieldnames=transaction.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(transaction)