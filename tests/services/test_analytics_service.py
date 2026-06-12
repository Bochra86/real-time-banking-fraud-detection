import pandas as pd
from unittest.mock import patch
import pytest

from api.exceptions import DatabaseError
from api.services.analytics_service import daily_summary, frauds_by_city, get_statistics

# get_statistics()
# Test 1: Cache hit for get_statistics()


@patch("api.services.analytics_service.get_cache")
def test_get_statistics_cache_hit(mock_cache):

    mock_cache.return_value = {
        "total_frauds": 10,
        "total_amount": 1000
    }

    result = get_statistics()

    assert result["total_frauds"] == 10


# Test 2: Cache miss


@patch("api.services.analytics_service.set_cache")
@patch("api.services.analytics_service.get_cache")
@patch("api.services.analytics_service.pd.read_sql")
def test_get_statistics_cache_miss(
    mock_read_sql,
    mock_get_cache,
    mock_set_cache
):

    mock_get_cache.return_value = None

    mock_read_sql.return_value = pd.DataFrame([
        {
            "total_frauds": 5,
            "total_amount": 500,
            "average_amount": 100,
            "highest_amount": 200
        }
    ])

    result = get_statistics()

    assert result["total_frauds"] == 5


# Test 3: Database exception


@patch("api.services.analytics_service.get_cache")
@patch("api.services.analytics_service.pd.read_sql")
def test_get_statistics_db_error(
    mock_read_sql,
    mock_get_cache
):

    mock_get_cache.return_value = None

    mock_read_sql.side_effect = Exception("DB failure")

    with pytest.raises(DatabaseError):
        get_statistics()

# frauds_by_city()
# Test 1: Cache hit


@patch("api.services.analytics_service.get_cache")
def test_frauds_by_city_cache_hit(mock_cache):

    mock_cache.return_value = [
        {
            "city": "Sao Paulo",
            "fraud_count": 61
        }
    ]

    result = frauds_by_city()

    assert result[0].city == "Sao Paulo"

# Test 2: Cache miss


@patch("api.services.analytics_service.set_cache")
@patch("api.services.analytics_service.get_cache")
@patch("api.services.analytics_service.pd.read_sql")
def test_frauds_by_city_cache_miss(
    mock_read_sql,
    mock_get_cache,
    mock_set_cache
):

    mock_get_cache.return_value = None

    mock_read_sql.return_value = pd.DataFrame([
        {
            "city": "Sao Paulo",
            "fraud_count": 61
        }
    ])

    result = frauds_by_city()

    assert result[0].fraud_count == 61

# Test 3: Database exception


@patch("api.services.analytics_service.get_cache")
@patch("api.services.analytics_service.pd.read_sql")
def test_frauds_by_city_db_error(
    mock_read_sql,
    mock_get_cache
):

    mock_get_cache.return_value = None

    mock_read_sql.side_effect = Exception("DB failure")

    with pytest.raises(DatabaseError):
        frauds_by_city()

# # daily_summary()
# Test 1: Cache hit


@patch("api.services.analytics_service.get_cache")
def test_daily_summary_cache_hit(mock_cache):

    mock_cache.return_value = [
        {
            "date": "2026-06-01",
            "total_frauds": 10,
            "total_amount": 5000
        }
    ]

    result = daily_summary()

    assert result[0].total_frauds == 10

# Test 2: Cache miss


@patch("api.services.analytics_service.set_cache")
@patch("api.services.analytics_service.get_cache")
@patch("api.services.analytics_service.pd.read_sql")
def test_daily_summary_cache_miss(
    mock_read_sql,
    mock_get_cache,
    mock_set_cache
):

    mock_get_cache.return_value = None

    mock_read_sql.return_value = pd.DataFrame([
        {
            "date": "2026-06-01",
            "total_frauds": 10,
            "total_amount": 5000
        }
    ])

    result = daily_summary()

    assert result[0].total_frauds == 10

# Test 3: Database exception


@patch("api.services.analytics_service.get_cache")
@patch("api.services.analytics_service.pd.read_sql")
def test_daily_summary_db_error(
    mock_read_sql,
    mock_get_cache
):

    mock_get_cache.return_value = None

    mock_read_sql.side_effect = Exception("DB failure")

    with pytest.raises(DatabaseError):
        daily_summary()
