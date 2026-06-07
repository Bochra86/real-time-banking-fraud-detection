import logging
import sys
from pythonjsonlogger import jsonlogger


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)

    formatter = jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s %(module)s"    )

    handler.setFormatter(formatter)

    logger.handlers = [handler]

    # -----------------------------
    # MODULE-SPECIFIC LOG LEVELS
    # -----------------------------
    LOG_LEVEL = {"api.services.analytics_service": logging.DEBUG,
                 "api.services.fraud_service": logging.INFO,}
    
    for name, level in LOG_LEVEL.items():
        logging.getLogger(name).setLevel(level)