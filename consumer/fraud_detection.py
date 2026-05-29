from config.settings import (FRAUD_AMOUNT_THRESHOLD, RISKY_CITIES)

def is_suspicious(transaction):

    amount = transaction["amount"]
    city = transaction["city"]

    if amount > FRAUD_AMOUNT_THRESHOLD:
        return True

    if city in RISKY_CITIES:
        return True

    return False