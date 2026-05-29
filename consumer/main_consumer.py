from confluent_kafka import Consumer
import json
import logging
import os

from consumer.fraud_detection import is_suspicious

from consumer.statistics import (update_statistics, print_statistics)

from consumer.storage import (save_suspicious_transaction)

from config.settings import (KAFKA_BROKER, TOPIC_NAME, LOG_FILE)

from consumer.database import save_to_postgresql

# Create folders if they don't exist
os.makedirs("logs", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Logging configuration
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Kafka Consumer
consumer = Consumer({'bootstrap.servers': KAFKA_BROKER, 'group.id': 'banking-group', 'auto.offset.reset': 'earliest'})

consumer.subscribe([TOPIC_NAME])

print("Listening for transactions...")

while True:

    msg = consumer.poll(1.0)

    if msg is None:
        continue

    if msg.error():
        logging.error(msg.error())
        continue

    transaction = json.loads(msg.value().decode('utf-8'))

    print("\nReceived:", transaction)

    logging.info(f"Transaction received: {transaction}")

    # Fraud detection
    suspicious = is_suspicious(transaction)

    # Update statistics
    update_statistics(transaction, suspicious)

    # Handle suspicious transactions
    if suspicious:

        print("⚠️ Suspicious transaction detected!")

        logging.warning(f"Suspicious transaction: {transaction}")

        save_suspicious_transaction(transaction)

        save_to_postgresql(transaction) 

    # Print live statistics
    print_statistics()
