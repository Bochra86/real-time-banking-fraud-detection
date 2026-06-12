from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import os

load_dotenv()

db_user = os.getenv("DB_USER", "")
db_password = quote_plus(os.getenv("DB_PASSWORD", ""))
db_host = os.getenv("DB_HOST", "")
db_port = os.getenv("DB_PORT", "")
db_name = os.getenv("DB_NAME", "")

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)

engine = None
SessionLocal = None

if all([db_user, db_host, db_port, db_name]):
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
