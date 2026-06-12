from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml import Pipeline
import os

spark = SparkSession.builder\
    .config("spark.local.dir", "/tmp/spark-local")\
    .config("spark.sql.warehouse.dir", "/tmp/spark-warehouse")\
    .config("spark.driver.extraJavaOptions", "-Djava.io.tmpdir=/tmp/spark-temp")\
    .config("spark.executor.extraJavaOptions", "-Djava.io.tmpdir=/tmp/spark-temp")\
    .appName("FraudTraining")\
    .getOrCreate()

spark.conf.set("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2")

df = spark.read.csv(
    "data/all_transactions.csv",
    header=True,
    inferSchema=True
)

df = df.withColumn(
    "label",
    when(
        ((col("amount") > 3500) & (col("user_id") < 10))
        | (col("city") == "Unknown"),
        1
    ).otherwise(0)
)
print(df.columns)
df.printSchema()

city_indexer = StringIndexer(
    inputCol="city",
    outputCol="city_index",
    handleInvalid="keep"
)

assembler = VectorAssembler(
    inputCols=[
        "amount",
        "user_id",
        "city_index"
    ],
    outputCol="features"
)

rf = RandomForestClassifier(
    labelCol="label",
    featuresCol="features"
)

pipeline = Pipeline(
    stages=[
        city_indexer,
        assembler,
        rf
    ]
)

model = pipeline.fit(df)

os.makedirs("ml/models", exist_ok=True)

model.write().overwrite().save(
    "/home/bmay/projects/banking-kafka-project/ml/models/fraud_model"
)

print("Model saved")
