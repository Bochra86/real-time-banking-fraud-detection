from confluent_kafka import Consumer
import json
import csv
import logging
import os

# Create folders if they don't exist
os.makedirs("logs", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Logging configuration
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Kafka Consumer
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'banking-group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['bank-transactions'])

print("Listening for transactions...")

# Fraud statistics
total_transactions = 0
suspicious_transactions = 0
total_amount = 0

# CSV file setup
csv_file = 'output/suspicious_transactions.csv'

# Create CSV header if file doesn't exist
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['transaction_id', 'user_id', 'amount', 'city'])

while True:

    msg = consumer.poll(1.0)

    if msg is None:
        continue

    if msg.error():
        logging.error(msg.error())
        continue

    transaction = json.loads(msg.value().decode('utf-8'))

    print("Received:", transaction)

    logging.info(f"Transaction received: {transaction}")

    amount = transaction["amount"]

    total_transactions += 1
    total_amount += amount

    average_amount = total_amount / total_transactions

    # Fraud detection
    if amount > 4000:

        suspicious_transactions += 1

        print("⚠️ Suspicious transaction detected!")

        logging.warning(f"Suspicious transaction: {transaction}")

        # Save suspicious transaction to CSV
        with open(csv_file, mode='a', newline='') as file:

            writer = csv.writer(file)

            writer.writerow([
                transaction["transaction_id"],
                transaction["user_id"],
                transaction["amount"],
                transaction["city"]
            ])

    # Print statistics
    print("\n--- Fraud Statistics ---")
    print(f"Total Transactions: {total_transactions}")
    print(f"Suspicious Transactions: {suspicious_transactions}")
    print(f"Average Amount: {average_amount:.2f}")