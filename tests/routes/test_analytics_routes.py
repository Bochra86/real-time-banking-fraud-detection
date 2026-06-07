from unittest.mock import patch
# Statistics endpoint


@patch("api.routes.fraud_routes.get_statistics")
def test_statistics(mock_statistics, test_client):

    mock_statistics.return_value = {
        "total_frauds": 10,
        "total_amount": 1000,
        "average_amount": 100,
        "highest_amount": 500
    }

    response = test_client.get("/api/statistics")

    assert response.status_code == 200

# By city endpoint


@patch("api.routes.fraud_routes.frauds_by_city")
def test_frauds_by_city(mock_city, test_client):

    mock_city.return_value = [
        {"city": "Sao Paulo", "fraud_count": 5}
    ]

    response = test_client.get("/api/frauds/by-city")

    assert response.status_code == 200

# Daily summary endpoint


@patch("api.routes.fraud_routes.daily_summary")
def test_daily_summary(mock_summary, test_client):

    mock_summary.return_value = [
        {
            "date": "2026-06-07",
            "total_frauds": 5,
            "total_amount": 1000
        }
    ]

    response = test_client.get("/api/frauds/daily-summary")

    assert response.status_code == 200
