"""Why `key % N` sharding hurts when you add a server.

Quiz question 6a: users are sharded by user_id % 4. What happens when we add a 5th shard?
"""

NUM_KEYS = 10_000


def shard_for(key, num_shards):
    return key % num_shards

def percent_moved(old_shards, new_shards):
    moved_count = 0
    for key in range(NUM_KEYS):
        old_shard = shard_for(key, old_shards)
        new_shard = shard_for(key, new_shards)
        if old_shard != new_shard:
            moved_count += 1

    return (moved_count / NUM_KEYS) * 100

if __name__ == "__main__":
    for old, new in [(4, 5), (4, 8), (10, 11), (100, 101)]:
        print(f"{old:>3} -> {new:>3} shards: {percent_moved(old, new):5.1f}% of keys move")
