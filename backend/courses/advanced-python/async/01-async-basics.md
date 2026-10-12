---
slug: async-basics
track: advanced-python
trackTitle: "Advanced Python"
trackOrder: 3
chapter: async
chapterTitle: "Chapter 1 — Asynchronous Programming"
chapterOrder: 1
title: "Async/Await Basics"
difficulty: advanced
order: 1
estimatedMinutes: 25
tags: [python, async, await, asyncio]
---

## Learning Objective

Write asynchronous Python code using `async`/`await` and `asyncio` for concurrent I/O operations.

## Explanation

**Synchronous** code runs sequentially — each operation blocks until complete. **Asynchronous** code can pause (`await`) and let other code run while waiting for I/O (network, disk, database).

Key concepts:
- **`async def`** — defines a coroutine (returns a coroutine object)
- **`await`** — pauses the coroutine until the awaited thing completes
- **`asyncio.run()`** — runs the top-level coroutine
- **`asyncio.gather()`** — runs multiple coroutines concurrently
- **Event loop** — manages and schedules coroutines

`async`/`await` is syntactic sugar over generators. It makes async code read like synchronous code.

## Why It Matters

I/O-bound programs (web servers, scrapers, API clients) spend most time waiting. Async lets you handle thousands of concurrent connections with a single thread. FastAPI, aiohttp, and modern Python web frameworks are built on asyncio.

## Example

```python
import asyncio
import time

async def fetch_data(name: str, delay: float) -> str:
    """Simulate an async I/O operation."""
    print(f"{name}: starting")
    await asyncio.sleep(delay)  # Non-blocking sleep
    print(f"{name}: done")
    return f"Result from {name}"

async def main():
    # Run sequentially (slow)
    start = time.perf_counter()
    result1 = await fetch_data("Task 1", 1.0)
    result2 = await fetch_data("Task 2", 1.0)
    print(f"Sequential: {time.perf_counter() - start:.2f}s")
    
    # Run concurrently (fast)
    start = time.perf_counter()
    results = await asyncio.gather(
        fetch_data("Task A", 1.0),
        fetch_data("Task B", 1.0),
        fetch_data("Task C", 1.0),
    )
    print(f"Concurrent: {time.perf_counter() - start:.2f}s")
    print(results)

asyncio.run(main())
# Sequential: ~2.00s
# Concurrent: ~1.00s
```

## Code

```python
import asyncio
import aiohttp
from typing import List

async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
    """Fetch a single URL asynchronously."""
    try:
        async with session.get(url) as response:
            text = await response.text()
            return {"url": url, "status": response.status, "length": len(text)}
    except Exception as e:
        return {"url": url, "error": str(e)}

async def fetch_multiple(urls: List[str]) -> List[dict]:
    """Fetch multiple URLs concurrently with a shared session."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# Timeout and error handling
async def fetch_with_timeout(url: str, timeout: float = 5.0) -> dict:
    try:
        async with aiohttp.ClientSession() as session:
            async with asyncio.timeout(timeout):
                async with session.get(url) as response:
                    return {"url": url, "status": response.status}
    except asyncio.TimeoutError:
        return {"url": url, "error": "Timeout"}
    except Exception as e:
        return {"url": url, "error": str(e)}

# Semaphore for rate limiting
async def fetch_limited(urls: List[str], max_concurrent: int = 3) -> List[dict]:
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def limited_fetch(url: str):
        async with semaphore:
            return await fetch_with_timeout(url)
    
    return await asyncio.gather(*[limited_fetch(u) for u in urls])

# Example usage
if __name__ == "__main__":
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/404",
    ]
    results = asyncio.run(fetch_multiple(urls))
    for r in results:
        print(r)
```

## Code Explanation

`async with aiohttp.ClientSession()` — async context manager for connection pooling.
`asyncio.gather(*tasks)` — runs all tasks concurrently, returns results in order.
`asyncio.timeout()` (Python 3.11+) — cancels if operation takes too long.
`asyncio.Semaphore` — limits concurrent operations (rate limiting).

## Common Mistakes

- Using `time.sleep()` instead of `await asyncio.sleep()` — blocks the event loop!
- Forgetting `await` on async functions — returns coroutine, doesn't execute
- Creating new `ClientSession` per request — reuse one session!
- Not handling exceptions — one failure cancels all in `gather()` (use `return_exceptions=True`)
- Mixing sync and async code without `run_in_executor()`

## Best Practices

- Use `asyncio.run()` only at the entry point
- Reuse `aiohttp.ClientSession` across requests
- Use `asyncio.gather(return_exceptions=True)` for graceful partial failures
- Limit concurrency with `Semaphore` to avoid overwhelming servers
- Use `asyncio.to_thread()` for blocking CPU-bound work
- Profile with `asyncio.run(..., debug=True)` for slow callbacks

## Exercise

Write an async function `fetch_all_with_retry(urls: list[str], max_retries: int = 3) -> list[dict]` that fetches all URLs with exponential backoff retry on failure.

## Solution

```python
import asyncio
import aiohttp
import random

async def fetch_with_retry(
    session: aiohttp.ClientSession,
    url: str,
    max_retries: int = 3
) -> dict:
    for attempt in range(max_retries):
        try:
            async with session.get(url) as response:
                if response.status < 500:
                    return {"url": url, "status": response.status}
        except Exception:
            pass
        
        if attempt < max_retries - 1:
            wait = 2 ** attempt + random.uniform(0, 0.1)
            await asyncio.sleep(wait)
    
    return {"url": url, "error": "Max retries exceeded"}

async def fetch_all_with_retry(urls: list[str], max_retries: int = 3) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_retry(session, url, max_retries) for url in urls]
        return await asyncio.gather(*tasks)
```

## Mini Quiz

```yaml
- question: "What does `await asyncio.sleep(1)` do?"
  options: [
    "Blocks the thread for 1 second",
    "Pauses the coroutine, allowing others to run",
    "Sleeps the entire program",
    "Creates a new thread"
  ]
  answer: 1
  explanation: "asyncio.sleep is non-blocking. The event loop runs other tasks during the wait."
- question: "How do you run multiple coroutines concurrently?"
  options: [
    "Call them in a loop",
    "Use asyncio.gather()",
    "Use threading",
    "Use multiprocessing"
  ]
  answer: 1
  explanation: "asyncio.gather() schedules all coroutines and runs them concurrently on the event loop."
- question: "Why reuse aiohttp.ClientSession?"
  options: [
    "It's required by the API",
    "Connection pooling and keep-alive",
    "It's faster to create",
    "It handles authentication"
  ]
  answer: 1
  explanation: "ClientSession maintains a connection pool with keep-alive, dramatically improving performance for multiple requests."
```