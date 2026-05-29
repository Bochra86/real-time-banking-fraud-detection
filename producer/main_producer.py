from confluent_kafka import Producer
import json
import random
import time

producer = Producer({'bootstrap.servers': 'localhost:9092'})

cities = ["Sao Paulo", "Rio", "Lisbon", "Madrid"]

transaction_id = 1

while True:

    transaction = {
        "transaction_id": transaction_id,
        "user_id": random.randint(1, 100),
        "amount": round(random.uniform(10, 5000), 2),
        "city": random.choice(cities)
    }

    producer.produce('bank-transactions', json.dumps(transaction).encode('utf-8'))

    producer.flush()

    print(f"Sent: {transaction}")

    transaction_id += 1

    time.sleep(2)