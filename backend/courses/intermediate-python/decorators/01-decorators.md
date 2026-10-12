---
slug: decorators
track: intermediate-python
trackTitle: "Intermediate Python"
trackOrder: 2
chapter: decorators
chapterTitle: "Chapter 2 — Decorators"
chapterOrder: 2
title: "Decorators and Function Wrappers"
difficulty: intermediate
order: 1
estimatedMinutes: 20
tags: [python, decorators, functions, metaprogramming]
---

## Learning Objective

Create and use decorators to modify function behavior without changing their code.

## Explanation

A **decorator** is a function that takes another function and extends its behavior. It's syntactic sugar:

```python
@my_decorator
def my_function():
    pass

# Equivalent to:
my_function = my_decorator(my_function)
```

Decorators enable cross-cutting concerns: logging, timing, authentication, caching, validation.

## Why It Matters

Decorators are everywhere in Python: `@property`, `@staticmethod`, `@classmethod`, `@app.route()`, `@lru_cache()`, pytest fixtures. Understanding them lets you write cleaner, more reusable code.

## Example

```python
import time
from functools import wraps

def timer(func):
    """Decorator that prints execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

@timer
def slow_function(n):
    time.sleep(n)
    return n * 2

print(slow_function(0.5))
# slow_function took 0.5001s
# 1.0
```

## Code

```python
import time
import functools
from typing import Callable, Any

# Basic decorator with functools.wraps (preserves metadata)
def debug(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")
        return result
    return wrapper

# Decorator with arguments
def repeat(times: int):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

# Class-based decorator
class CountCalls:
    def __init__(self, func: Callable):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call {self.count} to {self.func.__name__}")
        return self.func(*args, **kwargs)

# Practical decorators
def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (attempt + 1))
        return wrapper
    return decorator

def cache_result(func: Callable) -> Callable:
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

# Usage
@debug
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

@repeat(3)
def say_hi():
    return "Hi!"

@CountCalls
def add(a: int, b: int) -> int:
    return a + b

@retry(max_attempts=3, delay=0.1)
def flaky_operation():
    import random
    if random.random() < 0.7:
        raise ValueError("Random failure")
    return "Success!"

@cache_result
def expensive_computation(n: int) -> int:
    print(f"Computing for {n}...")
    return sum(i * i for i in range(n))

# Test
print(greet("Alice", greeting="Hi"))
# Calling greet(name='Alice', greeting='Hi')
# greet returned 'Hi, Alice!'
# Hi, Alice!

print(say_hi())
# ['Hi!', 'Hi!', 'Hi!']

print(add(2, 3))  # Call 1 to add -> 5
print(add(5, 7))  # Call 2 to add -> 12

print(expensive_computation(1000))
print(expensive_computation(1000))  # Uses cache!
```

## Code Explanation

`@functools.wraps(func)` — copies `__name__`, `__doc__`, `__annotations__` from original function.
Decorator with args: `repeat(times)` returns the actual decorator.
Class decorator: implements `__call__` to be callable, tracks state in `self`.
Practical examples: `retry` for transient failures, `cache_result` for memoization.

## Common Mistakes

- Forgetting `@functools.wraps` — breaks introspection, help(), debugging
- Decorator without args called as `@decorator` vs `@decorator()`
- Mutable default in closure: `def decorator(cache={})` — shared across decorated functions!
- Not handling `*args, **kwargs` properly in wrapper

## Best Practices

- Always use `@functools.wraps(func)`
- Use `@functools.lru_cache` for memoization instead of custom cache
- Keep decorators simple — one job per decorator
- Stack decorators bottom-to-top: `@a @b def f()` = `a(b(f()))`
- Use `Callable[[ArgTypes], ReturnType]` for type hints

## Exercise

Write a decorator `@validate_types` that checks function argument types match type hints at runtime. Raise `TypeError` on mismatch.

## Solution

```python
import functools
import inspect

def validate_types(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        hints = func.__annotations__
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        
        for param_name, value in bound.arguments.items():
            if param_name in hints:
                expected = hints[param_name]
                if not isinstance(value, expected):
                    raise TypeError(
                        f"{func.__name__}(): argument '{param_name}' "
                        f"must be {expected.__name__}, got {type(value).__name__}"
                    )
        return func(*args, **kwargs)
    return wrapper

@validate_types
def add(a: int, b: int) -> int:
    return a + b

add(1, 2)      # OK
add(1, "two")  # TypeError
```

## Mini Quiz

```yaml
- question: "What does `@functools.wraps(func)` do?"
  options: [
    "Makes the function faster",
    "Preserves the original function's metadata",
    "Caches the function result",
    "Adds type checking"
  ]
  answer: 1
  explanation: "wraps copies __name__, __doc__, __annotations__, etc. from the wrapped function."
- question: "How do you create a decorator that accepts arguments?"
  options: [
    "def decorator(args): ...",
    "def decorator(func): return decorator(args)",
    "def decorator(args): return lambda func: wrapper",
    "def decorator(args): def decorator(func): ... return decorator"
  ]
  answer: 3
  explanation: "A decorator with args is a function returning a decorator: def outer(args): def inner(func): ... return inner"
- question: "What's wrong with `def deco(cache={})`?"
  options: [
    "Syntax error",
    "Cache shared across all decorated functions",
    "Cache never expires",
    "No problem"
  ]
  answer: 1
  explanation: "Default dict is created once at function definition, shared across all calls."
```