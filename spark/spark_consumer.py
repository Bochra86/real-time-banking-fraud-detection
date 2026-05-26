import os
os.environ["HADOOP_HOME"] = "C:\\hadoop"
os.environ["hadoop.home.dir"] = "C:\\hadoop"

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Create Spark session
spark = SparkSession.builder \
    .appName("BankingFraudDetection") \
    .config("spark.local.dir", "C:/spark-local") \
    .config("spark.sql.warehouse.dir", "C:/spark-warehouse") \
    .config("spark.driver.extraJavaOptions", "-Djava.io.tmpdir=C:/spark-temp") \
    .config("spark.executor.extraJavaOptions", "-Djava.io.tmpdir=C:/spark-temp") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Transaction schema
schema = StructType([
    StructField("transaction_id", IntegerType()),
    StructField("user_id", IntegerType()),
    StructField("amount", DoubleType()),
    StructField("city", StringType())
])

# Read stream from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "bank-transactions") \
    .option("startingOffsets", "earliest") \
    .load()

# Convert Kafka value to string
json_df = df.selectExpr("CAST(value AS STRING)")

# Parse JSON
transactions = json_df.select(
    from_json(col("value"), schema).alias("data")
).select("data.*")

# Fraud detection
fraud_df = transactions.withColumn(
    "is_suspicious",
    when(col("amount") > 4000, "YES").otherwise("NO")
)

# Show live stream
query = fraud_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .option("checkpointLocation", "C:/tmp/spark-checkpoints") \
    .start()

query.awaitTermination()