from api.core.cache import set_cache
from api.core.cache import get_cache

#TEST 1 — “cache miss”
def test_get_cache_miss(monkeypatch):
    class FakeRedis:
        def get(self, key):
            return None

    monkeypatch.setattr("api.core.cache.cache", FakeRedis())

    result = get_cache("test_key")

    assert result is None

#TEST 2 — “cache hit”
def test_get_cache_hit(monkeypatch):
    class FakeRedis:
        def get(self, key):
            return '{"name": "bochra"}'

    monkeypatch.setattr("api.core.cache.cache", FakeRedis())

    result = get_cache("test_key")

    assert result == {"name": "bochra"}


#TEST 3 — “set cache with TTL”
def test_set_cache(monkeypatch):
    class FakeRedis:
        def set(self, *args, **kwargs):
            return True

    monkeypatch.setattr("api.core.cache.cache", FakeRedis())

    set_cache("key", "value", ttl=60)

#TEST 4 — “Redis read failure”
def test_get_cache_exception(monkeypatch):

    class FakeRedis:
        def get(self, key):
            raise Exception("Redis down")

    monkeypatch.setattr("api.core.cache.cache", FakeRedis())

    result = get_cache("test_key")

    assert result is None

#TEST 4 — “Redis write failure”
def test_set_cache_exception(monkeypatch):

    class FakeRedis:
        def set(self, *args, **kwargs):
            raise Exception("Redis down")

    monkeypatch.setattr("api.core.cache.cache", FakeRedis())

    set_cache("key", "value", ttl=60)