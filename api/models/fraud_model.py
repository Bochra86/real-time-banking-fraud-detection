from sqlalchemy import Column, Integer, Numeric, String, DateTime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class SuspiciousTransaction(Base):

    __tablename__ = "suspicious_transactions"

    id = Column(Integer, primary_key=True)

    transaction_id = Column(Integer, unique=True, nullable=False, index=True)

    user_id = Column(Integer, nullable=False)

    amount = Column(Numeric(12, 2), nullable=False)

    city = Column(String(100), nullable=False, index=True)

    created_at = Column(DateTime, nullable=False, index=True)
