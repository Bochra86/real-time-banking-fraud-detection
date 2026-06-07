from fastapi import FastAPI
from api.routes.fraud_routes import router as fraud_router
from api.exceptions import DatabaseError
from api.core.exception_handlers import database_exception_handler
from api.core.logging import setup_logging
from api.core.middleware import request_logging_middleware


# -------------------------
# LOGGING (MUST BE FIRST)
# -------------------------
setup_logging()

app = FastAPI(
    title="Banking Fraud Detection API",
    description="Real-Time Fraud Analytics API",
    version="1.0"
)

# -------------------------
# MIDDLEWARE
# -------------------------
app.middleware("http")(request_logging_middleware)

# -------------------------
# EXCEPTION HANDLING
# -------------------------
app.add_exception_handler(DatabaseError, database_exception_handler)

# -------------------------
# ROUTES
# -------------------------
app.include_router(fraud_router, prefix="/api")

# -------------------------
# ROOT ENDPOINTS
# -------------------------


@app.get("/")
def home():
    return {"message": "Real-Time Banking Fraud Detection API"}


@app.get("/health")
def health():
    return {"status": "healthy"}
