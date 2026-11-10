# System Design: Learning Alex Xu's *System Design Interview*

Two people work through the book together, one chapter at a time:

- **Chapters 1–3:** both of us read them and implement code on our own, then compare.
- **Chapters 4–15:** we take turns. One person implements the chapter and the other reviews it,
  asking "why X and not Y?" questions in a PR plus one live mock-interview session. Both of us read every chapter.
  - Me: odd chapters (5, 7, 9, 11, 13, 15)
  - Friend: even chapters (4, 6, 8, 10, 12, 14). Ch 6 (KV store) reuses the ch 5 hash ring.
- **Chapter 16:** joint review.

Before each chapter, agree on its scope (core mechanism only for big systems like YouTube and Drive).

Each chapter gets its own folder:

```
chNN-topic/
  notes.md   # key concepts, diagrams, trade-offs, interview talking points, reviewer Q&A
  *.py       # a small runnable build of the chapter's core idea
```

Python 3, standard library first. Run each chapter's code from inside its folder.

## Progress

| # | Chapter | Build idea | Owner | Status |
|---|---------|-----------|-------|--------|
| 1 | Scale from zero to millions of users | Simulated load balancer + cache-aside cache | Both | ⬜ |
| 2 | Back-of-the-envelope estimation | Estimation calculator (QPS, storage) | Both | ⬜ |
| 3 | A framework for system design interviews | Interview checklist template | Both | ⬜ |
| 4 | Design a rate limiter | Token bucket, sliding window and other algorithms | Friend | ⬜ |
| 5 | Design consistent hashing | Hash ring with virtual nodes | Me | ⬜ |
| 6 | Design a key-value store | Replicated KV store with quorum and vector clocks | Friend | ⬜ |
| 7 | Unique ID generator in distributed systems | Snowflake ID generator | Me | ⬜ |
| 8 | Design a URL shortener | Base62 shortener + HTTP API | Friend | ⬜ |
| 9 | Design a web crawler | BFS crawler with URL frontier and politeness | Me | ⬜ |
| 10 | Design a notification system | Queue-based notification workers with retries | Friend | ⬜ |
| 11 | Design a news feed system | Fan-out on write vs. on read | Me | ⬜ |
| 12 | Design a chat system | WebSocket chat server | Friend | ⬜ |
| 13 | Design a search autocomplete system | Trie with top-k caching | Me | ⬜ |
| 14 | Design YouTube | Upload/transcode pipeline simulation | Friend | ⬜ |
| 15 | Design Google Drive | File chunking, delta sync, versioning | Me | ⬜ |
| 16 | The learning continues | Review and further reading | Both | ⬜ |

Legend: ⬜ not started · 🟨 in progress · ✅ done
