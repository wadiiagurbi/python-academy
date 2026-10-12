---
slug: context-managers
track: intermediate-python
trackTitle: "Intermediate Python"
trackOrder: 2
chapter: decorators
chapterTitle: "Chapter 2 — Decorators"
chapterOrder: 2
title: "Context Managers with with and contextlib"
difficulty: intermediate
order: 2
estimatedMinutes: 18
tags: [python, context-managers, with, resources]
---

## Learning Objective

Manage resources safely with `with` statements, custom context managers, and `contextlib`.

## Explanation

A **context manager** sets something up, runs your block, then tears it down — even on errors. The `with` statement automates this:

```python
with open("data.txt") as f:
    content = f.read()
# File closed automatically, even if read() raised!
```

Two ways to create one:

1. **Class-based** — implement `__enter__` and `__exit__`.
2. **Generator-based** — use `@contextmanager` from `contextlib` with `yield`.

Common uses: files, locks, DB sessions, timers, temporary directory changes, suppressing exceptions.

## Why It Matters

Forgetting to close files, release locks, or roll back transactions causes leaks and deadlocks. Context managers make cleanup automatic and exception-safe. They are the standard pattern for any resource with a lifetime.

## Example

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(label: str):
    start = time.perf_counter()
    try:
        yield  # your block runs here
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label}: {elapsed:.3f}s")

with timer("sleep"):
    time.sleep(0.2)
# sleep: 0.200s
```

## Code

```python
from contextlib import contextmanager, suppress, redirect_stdout
import io
import os
import tempfile

# 1. Class-based context manager
class TempDir:
    def __enter__(self) -> str:
        self._tmp = tempfile.TemporaryDirectory()
        path = self._tmp.name
        print(f"Entering {path}")
        return path

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        print("Cleaning up temp dir")
        self._tmp.cleanup()
        return False  # False = do not suppress exceptions

with TempDir() as path:
    print(f"Working in {path}")

# 2. Generator-based with @contextmanager
@contextmanager
def change_dir(target: str):
    prev = os.getcwd()
    os.chdir(target)
    try:
        yield target
    finally:
        os.chdir(prev)

# 3. Reusable DB-session style manager
@contextmanager
def transaction():
    print("BEGIN")
    try:
        yield {"queries": []}
        print("COMMIT")
    except Exception:
        print("ROLLBACK")
        raise

with transaction() as txn:
    txn["queries"].append("INSERT ...")
    print("doing work...")

# 4. Standard library helpers
# suppress() — ignore specific exceptions
with suppress(FileNotFoundError):
    os.remove("does-not-exist.txt")
print("No error raised!")

# redirect_stdout() — capture prints
buf = io.StringIO()
with redirect_stdout(buf):
    print("captured!")
print(f"Got: {buf.getvalue().strip()}")
```

## Code Explanation

Class protocol: `__enter__` returns the value bound by `as`. `__exit__` receives exception info; return `True` to suppress, `False` to re-raise.
Generator protocol: code before `yield` is setup, `yield` value is bound by `as`, code after (in `finally`) is teardown — always runs.
`transaction()` shows commit/rollback branching on exception.
`suppress()` and `redirect_stdout()` are batteries-included helpers — prefer them over hand-rolled code.

## Common Mistakes

- Forgetting `yield` in `@contextmanager` — function never pauses for the block
- Yielding inside try without `finally` — teardown skipped on exception
- Returning `True` from `__exit__` accidentally — silently swallows errors
- Opening files without `with`: `f = open(...)` leaks if exception occurs before `close()`
- Nesting too many `with` blocks — use `with a() as x, b() as y:` on one line or `ExitStack`

## Best Practices

- Always use `with open(...)` for files
- Prefer `@contextmanager` for simple cases, class-based for reusable stateful managers
- Put cleanup in `finally` inside generator managers
- Use `contextlib.ExitStack` for dynamic numbers of context managers
- Document what the manager sets up and guarantees on exit

## Exercise

Write a `@contextmanager` called `in_memory_log()` that yields a list, appends `"enter"` on setup and `"exit"` on teardown, and captures any exception message into the list before re-raising.

## Solution

```python
from contextlib import contextmanager

@contextmanager
def in_memory_log():
    log: list[str] = []
    log.append("enter")
    try:
        yield log
    except Exception as e:
        log.append(f"error: {e}")
        raise
    finally:
        log.append("exit")

# Test
with in_memory_log() as log:
    log.append("work")
print(log)  # ['enter', 'work', 'exit']

try:
    with in_memory_log() as log2:
        raise ValueError("boom")
except ValueError:
    print(log2)  # ['enter', 'error: boom', 'exit']
```

## Mini Quiz

```yaml
- question: "What methods does a class-based context manager implement?"
  options: ["__init__ and __call__", "__enter__ and __exit__", "__open__ and __close__", "__start__ and __stop__"]
  answer: 1
  explanation: "__enter__ runs on entry (value bound by `as`), __exit__ runs on exit with exception info."
- question: "Where does the `with` block run in a `@contextmanager` function?"
  options: ["Before yield", "At the yield", "After yield", "It does not run"]
  answer: 1
  explanation: "Code before yield is setup; the with-body executes at yield; code after yield is teardown."
- question: "What does `with suppress(FileNotFoundError):` do?"
  options: [
    "Raises the error loudly",
    "Ignores FileNotFoundError inside the block",
    "Deletes the file",
    "Retries the block"
  ]
  answer: 1
  explanation: "suppress() swallows the listed exceptions so the block continues silently."
```
