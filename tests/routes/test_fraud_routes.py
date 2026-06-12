# Test fraud list


def test_get_frauds(test_client):

    response = test_client.get(
        "/api/frauds?page=1&page_size=10"
    )

    assert response.status_code == 200

    data = response.json()

    assert "page" in data
    assert "page_size" in data
    assert "total_records" in data
    assert "data" in data

# Test invalid page


def test_invalid_page(test_client):

    response = test_client.get(
        "/api/frauds?page=0&page_size=10"
    )

    assert response.status_code == 422


# Test latest frauds


def test_latest_frauds(test_client):

    response = test_client.get(
        "/api/latest-frauds"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )

# Test highest frauds


def test_highest_frauds(test_client):

    response = test_client.get(
        "/api/frauds/highest"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


# Test frauds sorted in descending order


def test_frauds_sort_desc(test_client):

    response = test_client.get(
        "/api/frauds?page=1&page_size=10&sort=desc"
    )

    assert response.status_code == 200
