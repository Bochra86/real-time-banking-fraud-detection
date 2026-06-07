from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from decimal import Decimal


class FraudTransaction(BaseModel):
    transaction_id: int
    user_id: int
    amount: Decimal
    city: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class FraudPageResponse(BaseModel):
    page: int
    page_size: int
    total_records: int
    data: list[FraudTransaction]


class StatisticsResponse(BaseModel):
    total_frauds: int
    total_amount: Decimal
    average_amount: Decimal
    highest_amount: Decimal


class FraudByCityResponse(BaseModel):
    city: str
    fraud_count: int


class DailySummaryResponse(BaseModel):
    date: date
    total_frauds: int
    total_amount: Decimal
