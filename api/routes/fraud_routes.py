from fastapi import APIRouter, Query, Depends, Request
from sqlalchemy.orm import Session
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address

from api.database.dependencies import get_db

from api.services.fraud_service import (get_frauds,
                                        get_latest_frauds,
                                        highest_frauds as get_highest_frauds)
from api.services.analytics_service import (get_statistics,
                                            frauds_by_city,
                                            daily_summary)

from api.schemas.fraud_schema import (
    DailySummaryResponse,
    FraudByCityResponse,
    FraudPageResponse,
    FraudTransaction,
    StatisticsResponse)


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# -------------------------
# FRAUD ENDPOINTS
# -------------------------

# 1 Route for get_frauds()


@router.get("/frauds",
            response_model=FraudPageResponse,
            tags=["Frauds"],
            summary="Get fraud transactions",
            description="Returns fraud transactions with filtering,"
            "sorting and pagination.")
@limiter.limit("10/minute")
def frauds(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    min_amount: float | None = None,
    city: str | None = None,
    sort: str = Query("desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    return get_frauds(db, page, page_size, min_amount, city, sort)

# 2 Route for get_latest_frauds(db)


@router.get("/latest-frauds",
            response_model=list[FraudTransaction],
            tags=["Frauds"],
            summary="Get latest fraud transactions",
            description="Returns latest fraud transactions with ordering and limiting.")
@limiter.limit("10/minute")
def latest_frauds(request: Request, db: Session = Depends(get_db)):
    return get_latest_frauds(db)

# 3 Route for get_highest_frauds(db)


@router.get("/frauds/highest",
            response_model=list[FraudTransaction],
            tags=["Frauds"],
            summary="Get highest fraud transactions",
            description="Returns the top 10 highest fraud transactions.")
@limiter.limit("10/minute")
def highest_frauds(request: Request, db: Session = Depends(get_db)):
    return get_highest_frauds(db)

# -------------------------
# ANALYTICS
# -------------------------

# 4 Route for get_statistics()


@router.get("/statistics",
            response_model=StatisticsResponse,
            tags=["Analytics"],
            summary="Get fraud statistics",
            description="Returns aggregated statistics about fraud transactions.")
@limiter.limit("2/minute")
def statistics(request: Request):
    return get_statistics()

# 5 Route for frauds_by_city()


@router.get("/frauds/by-city",
            response_model=list[FraudByCityResponse],
            tags=["Analytics"],
            summary="Get frauds by city",
            description="Returns fraud transactions grouped by city.")
@limiter.limit("2/minute")
def frauds_by_city_route(request: Request):
    return frauds_by_city()

# 6 Route for daily_summary()


@router.get("/frauds/daily-summary",
            response_model=list[DailySummaryResponse],
            tags=["Analytics"],
            summary="Get daily fraud summary",
            description="Returns a daily summary of fraud transactions.")
def daily_summary_route():
    return daily_summary()
