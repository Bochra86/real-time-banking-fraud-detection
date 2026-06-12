import pandas as pd
import logging
from api.database.connection import engine
from api.schemas.fraud_schema import DailySummaryResponse, FraudByCityResponse
from api.exceptions import DatabaseError
from api.core.cache import get_cache, set_cache

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

CACHE_TTL_SECONDS = 120

# 1.Get fraud statistics


def get_statistics() -> dict:
    try:
        cache_key = "fraud_stats"

        cached = get_cache(cache_key)

        if cached:
            logger.info({"event": "cache_hit",
                         "key": cache_key})
            return cached

        logger.info({"event": "cache_miss",
                     "key": cache_key})

        query = """
        SELECT
            COUNT(*) AS total_frauds,
            COALESCE(SUM(amount), 0) AS total_amount,
            COALESCE(AVG(amount), 0) AS average_amount,
            COALESCE(MAX(amount), 0) AS highest_amount
        FROM suspicious_transactions
        """

        df = pd.read_sql(query, engine)

        result = df.iloc[0].to_dict()

        set_cache(cache_key,
                  result,
                  ttl=CACHE_TTL_SECONDS)

        logger.info({"event": "fraud_statistics_generated",
                     "total_frauds": result["total_frauds"],
                     "total_amount": float(result["total_amount"])})

        return result

    except Exception as e:
        logger.exception({"event": "fraud_statistics_failed",
                          "error": str(e)})

        raise DatabaseError("Unable to retrieve statistics") from e

# 2.Fraud count by city


def frauds_by_city() -> list[FraudByCityResponse]:
    try:
        cache_key = "frauds_by_city"
        cached = get_cache(cache_key)

        if cached:
            logger.info({"event": "cache_hit",
                         "key": cache_key})
            return [FraudByCityResponse(**row) for row in cached]

        logger.info({"event": "cache_miss",
                     "key": cache_key})

        query = """
        SELECT city, COUNT(*) AS fraud_count
        FROM suspicious_transactions
        GROUP BY city
        ORDER BY fraud_count DESC
        """

        df = pd.read_sql(query, engine)
        cache_data = df.to_dict(orient="records")

        set_cache(cache_key,
                  cache_data,
                  ttl=CACHE_TTL_SECONDS)

        logger.info({"event": "fraud_count_by_city_retrieved",
                     "cities_returned": len(cache_data),
                     "top_city": cache_data[0]["city"] if cache_data else None,
                     "top_fraud_count": cache_data[0]["fraud_count"]
                     if cache_data else 0})

        return [FraudByCityResponse(**row) for row in cache_data]

    except Exception as e:
        logger.exception({"event": "Retrieving fraud count by city_failed",
                          "error": str(e)})
        raise DatabaseError("Unable to retrieve fraud count by city") from e

# 3.Daily fraud summary


def daily_summary() -> list[DailySummaryResponse]:
    try:
        cache_key = "daily_summary"
        cached = get_cache(cache_key)
        if cached:
            logger.info({"event": "cache_hit",
                         "key": cache_key})

            return [DailySummaryResponse(**row) for row in cached]

        logger.info({"event": "cache_miss",
                     "key": cache_key})

        query = """
        SELECT
            DATE(created_at) AS date,
            COUNT(*) AS total_frauds,
            COALESCE(SUM(amount), 0) AS total_amount
        FROM suspicious_transactions
        GROUP BY DATE(created_at::timestamp)
        ORDER BY date DESC
        """

        df = pd.read_sql(query, engine)
        df["date"] = df["date"].astype(str)
        df["total_amount"] = df["total_amount"].astype(float)

        cache_data = df.to_dict(orient="records")

        set_cache(cache_key,
                  cache_data,
                  ttl=CACHE_TTL_SECONDS)

        logger.info({"event": "daily_fraud_summary_retrieved",
                     "days_returned": len(cache_data),
                     "latest_date": cache_data[0]["date"] if cache_data else None})
        return [DailySummaryResponse(**row) for row in cache_data]

    except Exception as e:
        logger.exception({"event": "Retrieving daily fraud summary failed",
                          "error": str(e)})
        raise DatabaseError("Unable to retrieve daily fraud summary") from e
