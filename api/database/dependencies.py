from api.database.connection import SessionLocal


def get_db():
    if SessionLocal is None:
        raise RuntimeError("Database is not configured")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
