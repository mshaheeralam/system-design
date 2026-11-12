# Chapter 1 Build Plan: Scale From Zero to Millions of Users

Goal: simulate the chapter's core architecture in plain Python (standard library only).
The parts are a load balancer, stateless web servers, a cache-aside cache, a shared session store and a slow database.

## Files

| File | Responsibility |
|---|---|
| `database.py` | Fake DB: a dict with an artificial `time.sleep(0.05)` on every read, plus a counter of how many queries it handled. |
| `cache.py` | In-memory cache with `get`, `set` (with a TTL) and `delete`. Expired entries count as misses. |
| `web_server.py` | `WebServer(name, db, cache, session_store)`. `get_user(user_id)` uses **cache-aside**. `update_user(...)` writes to the DB **and invalidates the cache**. `login` / `whoami` use the **shared** session store. |
| `load_balancer.py` | Round-robin across servers. `mark_down(server)` makes it skip a dead server. |
| `simulate.py` | Runs ~1,000 requests where some users are requested much more often than others. Prints cache hit rate, DB query count and requests handled per server. Kills a server partway through and shows the logged-in user is **still logged in**. |
| `resharding.py` *(stretch)* | Assigns keys 0–9999 with `% 4`, then with `% 5`. Prints the percentage of keys that moved. Sets up Chapter 5. |
| `notes.md` | Key ideas in your own words, plus the quiz mistakes below. |

## Cache-aside flow (the web server does the work)

```
get_user(id):
    value = cache.get(id)
    if hit: return value
    value = db.get(id)          # slow
    cache.set(id, value, ttl)
    return value

update_user(id, data):
    db.set(id, data)
    cache.delete(id)            # invalidate, or the next read is stale
```

The cache never talks to the DB directly.

## Done when `simulate.py` shows

- [ ] DB query count is much lower with the cache than without it (run both and compare)
- [ ] An update is visible immediately (no stale read after `update_user`)
- [ ] Killing the server that handled `login` doesn't log the user out
- [ ] Requests are spread across servers, and the dead server gets none after `mark_down`
- [ ] *(stretch)* `resharding.py` shows roughly 80% of keys move when going from 4 to 5 shards

## Concepts to review (from the quiz)

- **Resharding:** going from `% 4` to `% 5` remaps most keys, which means mass data movement. Chapter 5's consistent hashing fixes this.
- **Cache invalidation:** updating the DB without deleting or updating the cached copy serves stale data until the TTL expires.
- **Stateless tier:** the main win is that *any server can handle any request*, which allows autoscaling and survives failures. Sticky sessions lose both.
- **Replication failover:** async replication means a promoted slave may lack the latest writes, so data can be lost.

## Workflow

1. Work on branch `ch01-scale-from-zero`.
2. Build in this order: `database.py` → `cache.py` → `web_server.py` → `load_balancer.py` → `simulate.py`.
3. Ask Claude for a review when stuck or finished. Then open a PR so your friend can compare it with their version.
