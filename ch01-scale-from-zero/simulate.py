import random

from cache import Cache
from database import Database
from load_balancer import LoadBalancer
from web_server import SessionStore, WebServer

NUM_USERS = 100
NUM_REQUESTS = 1000

random.seed(42)  # same "random" requests every run, so results are comparable


def build_system():
    # Fast reads so the simulation finishes quickly. 1000 x 0.05s would take 50s.
    db = Database(read_delay=0.001)
    for user_id in range(NUM_USERS):
        db.set(user_id, {"name": f"user{user_id}"})

    cache = Cache(default_ttl=60)
    sessions = SessionStore()
    servers = [WebServer(name, db, cache, sessions) for name in ["A", "B", "C"]]
    lb = LoadBalancer(servers)
    return db, cache, servers, lb


def pick_user():
    """Popular users get far more traffic, like real apps (a few celebrities, many quiet users).

    Weight for user i is 1/(i+1): user 0 is 100x more popular than user 99.
    """
    weights = [1 / (i + 1) for i in range(NUM_USERS)]
    return random.choices(range(NUM_USERS), weights=weights)[0]


def run():
    db, cache, servers, lb = build_system()

    login_server = lb.next_server()
    session_id = login_server.login(pick_user())

    for i in range(NUM_REQUESTS):
        if i == NUM_REQUESTS // 2:
            lb.mark_down(login_server)
            print(f"\nServer {login_server.name} died!")
            new_server = lb.next_server()
            user_id = new_server.whoami(session_id)
            if user_id is not None:
                print(f"User is still logged in on server {new_server.name} (user_id={user_id})")
            else:
                print(f"User is NOT logged in on server {new_server.name} (user_id={user_id})")

        lb.next_server().get_user(pick_user())

    # Report (already written, so you can see the results once the TODOs work)
    reads = cache.hits + cache.misses
    print(f"\nRequests sent:      {NUM_REQUESTS}")
    print(f"DB queries:         {db.query_count}  (without a cache this would be {NUM_REQUESTS})")
    print(f"Cache hit rate:     {cache.hits / reads:.0%}" if reads else "Cache hit rate:     n/a")
    print("Requests per server:")
    for s in servers:
        status = "DOWN" if s in lb.down else "up"
        print(f"  {s.name} ({status}): {s.requests_handled}")


if __name__ == "__main__":
    run()
