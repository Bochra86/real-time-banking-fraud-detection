from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from api.core.cache import get_cache, set_cache
from api.models.fraud_model import SuspiciousTransaction
from api.exceptions import DatabaseError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

TOP_FRAUD_LIMIT = 10
CACHE_TTL_SECONDS = 60

# 1.Get all frauds with filters

def get_frauds(db: Session,   
               page: int,
               page_size: int,
               min_amount: float | None = None,
               city: str | None = None,
               sort: str = "desc") -> dict[str, Any]:
   try:

    query = db.query(SuspiciousTransaction)
    if min_amount is not None:
            query = query.filter(SuspiciousTransaction.amount >= min_amount)

    if city:
            query = query.filter(SuspiciousTransaction.city == city)

    query = query.order_by(SuspiciousTransaction.amount.desc() if sort == "desc" else SuspiciousTransaction.amount.asc())

    offset = (page - 1) * page_size
    total_records = query.count()
    results = (query.offset(offset).limit(page_size).all())

    logger.info({"event": "fraud_fetched",
                 "page": page,
                 "page_size": page_size,
                 "city": city,
                 "count": len(results)})
    
    return {"page": page, 
            "page_size": page_size, 
            "total_records": total_records, 
            "data": results}
   
   except SQLAlchemyError as e:
    logger.exception({"event": "Database retrieving fraud records failed",
                      "error": str(e)})
    raise DatabaseError( "Unable to retrieve fraud records") from e


# 2.Get latest frauds
def get_latest_frauds(db: Session)->  list[dict[str, Any]]:

    try:   
        cache_key = "latest_frauds"    
        cached = get_cache(cache_key)    
        if cached:
            logger.info({"event": "cache_hit",
                         "key": cache_key})
            return cached 
        
        logger.info({"event": "cache_miss",
                     "key": cache_key})

        
        results = db.query(SuspiciousTransaction).order_by(SuspiciousTransaction.created_at.desc()).limit(10).all()
        cache_data = [{
            "transaction_id": row.transaction_id,
            "user_id": row.user_id,
            "amount": float(row.amount),
            "city": row.city,
            "created_at": row.created_at.isoformat()}for row in results]

        set_cache(cache_key, cache_data, ttl=CACHE_TTL_SECONDS)

        logger.info({"event": "latest_frauds_retrieved", 
                     "count": len(results)})
        return cache_data  
    
    except SQLAlchemyError as e:

        logger.exception({"event": "Retrieving latest fraud records failed",
                          "error": str(e)})

        raise DatabaseError("Unable to retrieve latest fraud records") from e


# 3.Highest fraud transactions
def highest_frauds(db: Session)-> list[dict[str, Any]]:

    try:
        cache_key = "highest_frauds"
        cached = get_cache(cache_key)

        if cached:
            logger.info({"event": "cache_hit",
                         "key": cache_key})
            return cached
        
        logger.info({"event": "cache_miss",
                     "key": cache_key})

        results = (db.query(SuspiciousTransaction).order_by(SuspiciousTransaction.amount.desc()).limit(10).all())
       
        cache_data = [{
            "id": row.id,
            "transaction_id": row.transaction_id,
            "user_id": row.user_id,
            "amount": float(row.amount),
            "city": row.city,
            "created_at": row.created_at.isoformat()
            if row.created_at else None}for row in results]

        set_cache(cache_key, cache_data, ttl=CACHE_TTL_SECONDS,)
   
        logger.info({"event": "highest_frauds_retrieved", "count": len(results)})
        return cache_data
    
    except SQLAlchemyError as e:
        
        logger.exception({"event": "Retrieving highest fraud records failed",
                          "error": str(e)})

        raise DatabaseError("Unable to retrieve highest fraud records") from e