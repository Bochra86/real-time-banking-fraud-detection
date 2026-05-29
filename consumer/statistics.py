total_transactions = 0
suspicious_transactions = 0
total_amount = 0


def update_statistics(transaction, suspicious):

    global total_transactions
    global suspicious_transactions
    global total_amount

    total_transactions += 1
    total_amount += transaction["amount"]

    if suspicious:
        suspicious_transactions += 1


def print_statistics():

    average = 0

    if total_transactions > 0:
        average = total_amount / total_transactions

    print("\n--- Fraud Statistics ---")
    print(f"Total Transactions: {total_transactions}")
    print(f"Suspicious Transactions: {suspicious_transactions}")
    print(f"Average Amount: {average:.2f}")