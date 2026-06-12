import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import SQLAlchemyError

from api.services.fraud_service import get_frauds, get_latest_frauds, highest_frauds
from api.exceptions import DatabaseError

# get_frauds()
# test1  city_filter


def test_get_frauds_city_filter():

    mock_db = MagicMock()

    query = MagicMock()

    mock_db.query.return_value = query

    query.filter.return_value = query
    query.order_by.return_value = query
    query.offset.return_value = query
    query.limit.return_value = query

    query.count.return_value = 1
    query.all.return_value = [MagicMock(city="Sao Paulo")]

    result = get_frauds(
        db=mock_db,
        page=1,
        page_size=20,
        city="Sao Paulo"
    )

    assert result["total_records"] == 1

# test2 min_amount_filter


def test_get_frauds_min_amount_filter():

    mock_db = MagicMock()

    query = MagicMock()

    mock_db.query.return_value = query

    query.filter.return_value = query
    query.order_by.return_value = query
    query.offset.return_value = query
    query.limit.return_value = query

    query.count.return_value = 1
    query.all.return_value = [MagicMock(amount=5000)]

    result = get_frauds(
        db=mock_db,
        page=1,
        page_size=20,
        min_amount=1000
    )

    assert result["total_records"] == 1

# test3 sort_asc


def test_get_frauds_sort_asc():

    mock_db = MagicMock()

    query = MagicMock()

    mock_db.query.return_value = query

    query.order_by.return_value = query
    query.offset.return_value = query
    query.limit.return_value = query

    query.count.return_value = 0
    query.all.return_value = []

    get_frauds(
        db=mock_db,
        page=1,
        page_size=20,
        sort="asc"
    )

    query.order_by.assert_called_once()

# test4 pagination


def test_frauds_pagination(test_client):

    response = test_client.get("/api/frauds?page=999")

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 999
    assert len(data["data"]) == 0

# test5 db_error


def test_get_frauds_db_error():

    mock_db = MagicMock()

    mock_db.query.side_effect = SQLAlchemyError("DB failure")

    with pytest.raises(DatabaseError):
        get_frauds(
            db=mock_db,
            page=1,
            page_size=20
        )


# get_latest_frauds()
# test1 cache miss


@patch("api.services.fraud_service.set_cache")
@patch("api.services.fraud_service.get_cache")
def test_get_latest_frauds_cache_miss(
    mock_get_cache,
    mock_set_cache
):

    mock_get_cache.return_value = None

    mock_row = MagicMock()

    mock_row.transaction_id = 1
    mock_row.user_id = 10
    mock_row.amount = 100.0
    mock_row.city = "Rio"

    from datetime import datetime
    mock_row.created_at = datetime.now()

    query = MagicMock()

    query.order_by.return_value = query
    query.limit.return_value = query
    query.all.return_value = [mock_row]

    mock_db = MagicMock()
    mock_db.query.return_value = query

    result = get_latest_frauds(mock_db)

    assert len(result) == 1

# test2 cache hit


@patch("api.services.fraud_service.get_cache")
def test_get_latest_frauds_cache_hit(mock_cache):

    mock_cache.return_value = [
        {
            "transaction_id": 1,
            "user_id": 10,
            "amount": 100.0,
            "city": "Rio",
            "created_at": "2026-06-01T10:00:00"
        }
    ]

    result = get_latest_frauds(MagicMock())

    assert len(result) == 1

# test3 db_error


@patch("api.services.fraud_service.get_cache")
def test_get_latest_frauds_db_error(mock_cache):

    mock_cache.return_value = None

    mock_db = MagicMock()
    mock_db.query.side_effect = SQLAlchemyError("DB failure")

    with pytest.raises(DatabaseError):
        get_latest_frauds(mock_db)


# highest_fraud()
# test1 cache_miss


@patch("api.services.fraud_service.set_cache")
@patch("api.services.fraud_service.get_cache")
def test_highest_frauds_cache_miss(
    mock_get_cache,
    mock_set_cache
):

    mock_get_cache.return_value = None

    row = MagicMock()

    row.id = 1
    row.transaction_id = "TX123"
    row.user_id = 10
    row.amount = 5000.0
    row.city = "Sao Paulo"

    from datetime import datetime
    row.created_at = datetime.now()

    query = MagicMock()

    query.order_by.return_value = query
    query.limit.return_value = query
    query.all.return_value = [row]

    mock_db = MagicMock()
    mock_db.query.return_value = query

    result = highest_frauds(mock_db)

    assert len(result) == 1

# test2 cache_hit


@patch("api.services.fraud_service.get_cache")
def test_highest_frauds_cache_hit(mock_cache):

    mock_cache.return_value = [
        {
            "id": 1,
            "transaction_id": "TX123",
            "user_id": 10,
            "amount": 5000.0,
            "city": "Sao Paulo",
            "created_at": "2026-06-01T10:00:00"
        }
    ]

    result = highest_frauds(MagicMock())

    assert len(result) == 1
    assert result[0]["amount"] == 5000.0

# test3 db_error


@patch("api.services.fraud_service.get_cache")
def test_highest_frauds_db_error(mock_cache):

    mock_cache.return_value = None

    mock_db = MagicMock()
    mock_db.query.side_effect = SQLAlchemyError("DB failure")

    with pytest.raises(DatabaseError):
        highest_frauds(mock_db)
