from dotenv import load_dotenv
import psycopg2
import os


# Load environment variables
load_dotenv()


# Database credentials
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_port = os.getenv("DB_PORT")


# PostgreSQL connection
connection = psycopg2.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password,
    port=db_port
)

cursor = connection.cursor()


# Save suspicious transaction
def save_to_postgresql(transaction):

    query = """
    INSERT INTO suspicious_transactions
    (transaction_id, user_id, amount, city)
    VALUES (%s, %s, %s, %s)
    """

    values = (
        transaction["transaction_id"],
        transaction["user_id"],
        transaction["amount"],
        transaction["city"]
    )

    cursor.execute(query, values)

    connection.commit()