# Statistics endpoint


def test_statistics(test_client):

    response = test_client.get(
        "/api/statistics"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

# By city endpoint


def test_frauds_by_city(test_client):

    response = test_client.get(
        "/api/frauds/by-city"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )

# Daily summary endpoint


def test_daily_summary(test_client):

    response = test_client.get(
        "/api/frauds/daily-summary"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )
