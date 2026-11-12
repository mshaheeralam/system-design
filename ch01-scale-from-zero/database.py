import time


class Database:
    """A fake database: stores data in a dict, but every read is slow on purpose.

    The delay is what makes the cache worth having. Without it, we couldn't
    see any difference between reading from the cache and reading from the DB.
    """

    def __init__(self, read_delay=0.05):
        self.data = {}                # key -> value, e.g. 1 -> {"name": "Ana"}
        self.read_delay = read_delay  # seconds each read takes
        self.query_count = 0          # how many reads hit the DB (to measure the cache's effect)

    def get(self, key):
        self.query_count += 1
        time.sleep(self.read_delay)   # pretend this is a slow disk/network round trip
        return self.data.get(key)     # returns None if the key doesn't exist

    def set(self, key, value):
        self.data[key] = value


if __name__ == "__main__":
    # Quick self-check: run `python database.py` from inside ch01-scale-from-zero/
    db = Database()
    db.set(1, {"name": "Ana"})

    start = time.time()
    print(db.get(1))
    print(db.get(2))
    print(f"2 reads took {time.time() - start:.2f}s, query_count = {db.query_count}")
