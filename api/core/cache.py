import json
import redis
import logging

logger = logging.getLogger(__name__)

cache = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


def get_cache(key):

    try:
        value = cache.get(key)

        if value:
            return json.loads(value)

        return None

    except Exception as e:
        logger.warning({
            "event": "redis_read_failed",
            "key": key,
            "error": str(e)
        })

        return None


def set_cache(key, value, ttl=120):

    try:
        cache.set(key,
                  json.dumps(value),
                  ex=ttl)

    except Exception as e:
        logger.warning({"event": "redis_write_failed",
                        "key": key,
                        "error": str(e)})
