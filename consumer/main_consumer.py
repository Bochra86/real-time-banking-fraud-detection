from confluent_kafka import Consumer
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession

import json
import logging
import os

from config.settings import (KAFKA_BROKER, TOPIC_NAME, LOG_FILE)
from consumer.fraud_detection import is_suspicious
from consumer.statistics import (update_statistics, print_statistics)
from consumer.storage import save_suspicious_transaction
from consumer.database import save_to_postgresql

# Create folders if they don't exist
os.makedirs("logs", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Spark Session
spark = (
    SparkSession.builder
    .appName("FraudPrediction")
    .getOrCreate()
)

# Load the saved ML model
model = PipelineModel.load(
    "ml/models/fraud_model"
)

# Logging configuration
logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Kafka Consumer
consumer = Consumer({'bootstrap.servers': KAFKA_BROKER,
                     'group.id': 'banking-group',
                     'auto.offset.reset': 'earliest'})

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

    # Create DataFrame
    df = spark.createDataFrame([transaction])

    # ML Prediction
    # ---------------------------------

    prediction_df = model.transform(df)

    prediction = int(prediction_df.collect()[0]["prediction"])

    print(f"ML Prediction: {'FRAUD' if prediction == 1 else 'NORMAL'}")

    # Rule-based Detection
    suspicious = is_suspicious(transaction)  # bool

    # Update statistics
    update_statistics(transaction, suspicious)

    # Handle suspicious transactions
    if suspicious or prediction == 1:

        if prediction == 1 and suspicious:

            print("🚨 ML Fraud Detected!")
            print("⚠️ Rule-Based Suspicious Transaction!")

        elif prediction == 1:

            print("🚨 ML Fraud Detected!")

        elif suspicious:

            print("⚠️ Rule-Based Suspicious Transaction!")

        logging.warning(f"Suspicious transaction: {transaction}")

        save_suspicious_transaction(transaction)

        save_to_postgresql(transaction)

    # Print live statistics
    print_statistics()
