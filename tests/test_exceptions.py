from api.exceptions import DatabaseError


def test_database_error():

    exc = DatabaseError("Test error")

    assert str(exc) == "Test error"
