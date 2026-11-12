import time


class Cache:
    """An in-memory cache where every entry expires after a TTL (time to live).

    Unlike the Database, reads here are fast: there is no sleep.
    """

    def __init__(self, default_ttl=60):
        self.store = {}                 # key -> (value, expires_at)
        self.default_ttl = default_ttl  # seconds
        self.hits = 0
        self.misses = 0

    def get(self, key):
        if key not in self.store:
            self.misses += 1
            return None

        value, expires_at = self.store[key]
        
        if time.time() > expires_at:
            del self.store[key]
            self.misses += 1
            return None

        self.hits += 1
        return value

    def set(self, key, value, ttl=None):

        if ttl is None:
            ttl = self.default_ttl

        expires_at = time.time() + ttl
        self.store[key] = (value, expires_at)

    def delete(self, key):
        self.store.pop(key, None)


if __name__ == "__main__":
    # Self-check: run `python cache.py`. Every line should print True.
    c = Cache(default_ttl=60)
    print(c.get("a") is None)          # miss: not there
    c.set("a", 123)
    print(c.get("a") == 123)           # hit
    c.delete("a")
    print(c.get("a") is None)          # miss: deleted
    c.delete("missing")                # must not crash

    c.set("b", "short-lived", ttl=0.1)
    time.sleep(0.2)
    print(c.get("b") is None)          # miss: expired

    print(c.hits == 1, c.misses == 3)  # True True
