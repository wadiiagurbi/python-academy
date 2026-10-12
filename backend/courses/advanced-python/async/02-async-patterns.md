---
slug: async-patterns
track: advanced-python
trackTitle: "Advanced Python"
trackOrder: 3
chapter: async
chapterTitle: "Chapter 1 — Asynchronous Programming"
chapterOrder: 1
title: "Async Patterns: Tasks, Queues and Concurrency"
difficulty: advanced
order: 2
estimatedMinutes: 25
tags: [python, async, asyncio, concurrency]
---

## Learning Objective

Coordinate concurrent work with tasks, TaskGroups, queues, semaphores, and timeouts.

## Explanation

`asyncio.gather()` runs a fixed set of coroutines. Real systems need more:

- **`asyncio.create_task()`** — schedule a coroutine to run in the background, get a `Task` handle.
- **`asyncio.TaskGroup`** (Python 3.11+) — structured concurrency: all child tasks finish or fail together.
- **`asyncio.Queue`** — producer/consumer pipeline with backpressure.
- **`asyncio.Semaphore`** — limit concurrency (e.g., max 5 HTTP requests).
- **`asyncio.wait_for()` / `asyncio.timeout()`** — bound how long you wait.
- **`asyncio.to_thread()`** — run blocking sync code without freezing the loop.

## Why It Matters

Production async code is not "await everything with gather". You need cancellation, rate limits, retries, and background workers. These patterns separate toy demos from reliable scrapers, gateways, and streaming pipelines.

## Example

```python
import asyncio

async def worker(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name} done"

async def main():
    # Tasks run in background
    t1 = asyncio.create_task(worker("A", 1.0))
    t2 = asyncio.create_task(worker("B", 0.5))
    print(await t1)
    print(await t2)

asyncio.run(main())
```

## Code

```python
import asyncio
import random

async def fetch(item: int) -> str:
    await asyncio.sleep(random.uniform(0.1, 0.5))
    if item == 3:
        raise ValueError("bad item 3")
    return f"result-{item}"

# 1. TaskGroup — structured concurrency (3.11+)
async def with_task_group():
    results: dict[int, str] = {}
    try:
        async with asyncio.TaskGroup() as tg:
            for i in range(5):
                tg.create_task(store(i, results))
    except Exception as e:
        print(f"TaskGroup failed: {e}")
    print(results)

async def store(i: int, out: dict):
    out[i] = await fetch(i)

# 2. Producer / consumer with Queue
async def producer(queue: asyncio.Queue):
    for i in range(6):
        await queue.put(i)
        print(f"produced {i}")
    await queue.put(None)  # sentinel = done

async def consumer(queue: asyncio.Queue):
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        print(f"  consumed {item} -> {await fetch(item)}")
        queue.task_done()

async def with_queue():
    queue: asyncio.Queue = asyncio.Queue(maxsize=2)  # backpressure
    prod = asyncio.create_task(producer(queue))
    cons = asyncio.create_task(consumer(queue))
    await asyncio.gather(prod, cons)
    await queue.join()

# 3. Semaphore + timeout for rate-limited I/O
sem = asyncio.Semaphore(2)

async def limited_fetch(i: int) -> dict:
    async with sem:
        try:
            async with asyncio.timeout(1.0):
                return {"id": i, "data": await fetch(i)}
        except asyncio.TimeoutError:
            return {"id": i, "error": "timeout"}
        except Exception as e:
            return {"id": i, "error": str(e)}

async def with_limits():
    results = await asyncio.gather(*[limited_fetch(i) for i in range(6)])
    for r in results:
        print(r)

# 4. Offload blocking code
def blocking_hash(n: int) -> int:
    import hashlib
    return int(hashlib.sha256(str(n).encode()).hexdigest(), 16)

async def with_thread():
    # Runs in a thread, loop stays responsive
    digest = await asyncio.to_thread(blocking_hash, 42)
    print(f"hash: {str(digest)[:12]}...")

async def main():
    print("--- TaskGroup ---")
    await with_task_group()
    print("--- Queue ---")
    await with_queue()
    print("--- Limits ---")
    await with_limits()
    print("--- Thread ---")
    await with_thread()

if __name__ == "__main__":
    asyncio.run(main())
```

## Code Explanation

`TaskGroup` cancels siblings if one fails and re-raises — no orphan tasks.
`Queue(maxsize=2)` blocks the producer when full (backpressure). Sentinel `None` signals completion; `task_done()`/`join()` track progress.
`Semaphore(2)` allows only 2 `limited_fetch` bodies at once.
`asyncio.timeout(1.0)` cancels the inner await on expiry, raising `TimeoutError`.
`asyncio.to_thread()` runs CPU-bound or blocking sync code in a worker thread.

## Common Mistakes

- Fire-and-forget `create_task()` without awaiting or storing — exceptions vanish, tasks get GC'd
- Using `gather()` without `return_exceptions=True` when partial failure is OK — one error cancels everything
- Blocking the loop with `time.sleep()`, `requests.get()`, or heavy CPU in async functions
- Unbounded concurrency (1000 simultaneous connections) — always use Semaphore or Queue maxsize
- Forgetting sentinel / `task_done()` — consumer hangs forever on `queue.join()`

## Best Practices

- Prefer `TaskGroup` over raw `create_task` + `gather` for structured lifetimes
- Use `Queue` for pipelines, `Semaphore` for rate limits, `timeout()` for every network call
- Use `gather(..., return_exceptions=True)` for best-effort batch jobs, then inspect results
- Offload blocking I/O and CPU work with `asyncio.to_thread()`
- Name tasks: `create_task(coro(), name="fetch-1")` for debuggable logs

## Exercise

Write `crawl(urls: list[str], limit: int = 3) -> list[dict]` that fetches each URL (simulate with `asyncio.sleep`) concurrently with max `limit`, 2s timeout per URL, collecting errors as dicts instead of raising.

## Solution

```python
import asyncio
import random

async def fake_get(url: str) -> str:
    await asyncio.sleep(random.uniform(0.1, 0.5))
    if "bad" in url:
        raise ValueError(f"failed {url}")
    return f"body of {url}"

async def crawl(urls: list[str], limit: int = 3) -> list[dict]:
    sem = asyncio.Semaphore(limit)

    async def one(url: str) -> dict:
        async with sem:
            try:
                async with asyncio.timeout(2.0):
                    return {"url": url, "body": await fake_get(url)}
            except Exception as e:
                return {"url": url, "error": str(e)}

    return list(await asyncio.gather(*[one(u) for u in urls]))

# Test
async def main():
    print(await crawl(["a", "bad-1", "b", "c"], limit=2))

asyncio.run(main())
```

## Mini Quiz

```yaml
- question: "What does `asyncio.TaskGroup` provide over `gather()`?"
  options: [
    "Faster execution",
    "Structured concurrency: children finish or cancel together",
    "No need for async functions",
    "Automatic retries"
  ]
  answer: 1
  explanation: "TaskGroup ensures all child tasks complete; if one fails, the rest are cancelled."
- question: "Why use `asyncio.Semaphore(5)`?"
  options: [
    "To run exactly 5 tasks",
    "To limit to 5 concurrent entries",
    "To timeout after 5 seconds",
    "To create 5 threads"
  ]
  answer: 1
  explanation: "Semaphore caps concurrency — only 5 holders inside `async with sem` at once."
- question: "How do you run blocking sync code in async?"
  options: ["await it directly", "asyncio.to_thread(func)", "threading.sleep()", "asyncio.gather()"]
  answer: 1
  explanation: "asyncio.to_thread() runs the function in a worker thread without blocking the event loop."
```
