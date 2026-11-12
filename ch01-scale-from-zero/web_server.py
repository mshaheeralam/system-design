import uuid

from cache import Cache
from database import Database

NOT_FOUND = object()

class SessionStore:
    """Shared session storage (in real life: Redis or a DB).

    Every web server gets the SAME SessionStore object, so a user who logged in
    on server A is still recognized by server B. That is what makes the web
    tier stateless.
    """

    def __init__(self):
        self.sessions = {}  # session_id -> user_id

    def create(self, user_id):
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = user_id
        return session_id

    def get_user_id(self, session_id):
        return self.sessions.get(session_id)


class WebServer:
    def __init__(self, name, db, cache, session_store):
        self.name = name
        self.db = db
        self.cache = cache
        self.session_store = session_store
        self.requests_handled = 0  # lets simulate.py show how the load balancer spread traffic

    def get_user(self, user_id):
        self.requests_handled += 1

        value = self.cache.get(user_id)
        if value is NOT_FOUND:
            return None
        elif value is not None:
            return value

        value = self.db.get(user_id)
        
        if value is None:
            self.cache.set(user_id, NOT_FOUND, ttl=5)  # cache negative result for a short time
        else:
            self.cache.set(user_id, value)
        return value


    def update_user(self, user_id, data):
        self.requests_handled += 1
        self.db.set(user_id, data)
        self.cache.delete(user_id)  # invalidate cache so next read gets the new value

    def login(self, user_id):
        self.requests_handled += 1
        return self.session_store.create(user_id)

    def whoami(self, session_id):
        self.requests_handled += 1
        return self.session_store.get_user_id(session_id)


if __name__ == "__main__":
    # Self-check: run `python web_server.py`. Every line should print True.
    db, cache, sessions = Database(), Cache(), SessionStore()
    db.set(1, {"name": "Ana"})
    a = WebServer("A", db, cache, sessions)
    b = WebServer("B", db, cache, sessions)

    print(a.get_user(1) == {"name": "Ana"})   # miss -> DB
    print(b.get_user(1) == {"name": "Ana"})   # hit  -> shared cache
    print(db.query_count == 1)                # DB was only queried once

    a.update_user(1, {"name": "Ana Smith"})
    print(b.get_user(1) == {"name": "Ana Smith"})  # no stale read

    sid = a.login(1)
    print(b.whoami(sid) == 1)                 # logged in on A, recognized by B
