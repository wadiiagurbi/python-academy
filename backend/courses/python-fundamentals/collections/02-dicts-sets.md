---
slug: dicts-sets
track: python-fundamentals
trackTitle: "Python Fundamentals"
trackOrder: 1
chapter: collections
chapterTitle: "Chapter 3 — Collections"
chapterOrder: 3
title: "Dictionaries and Sets"
difficulty: beginner
order: 2
estimatedMinutes: 18
tags: [python, dict, set, collections]
---

## Learning Objective

Store and look up key-value data with dicts and unique collections with sets.

## Explanation

**Dicts** (`dict`) store `key: value` pairs. Created with `{ }` or `dict()`. Keys must be immutable (str, int, tuple). Lookup by key is very fast (hash table).

```python
user = {"name": "Alice", "age": 30}
print(user["name"])        # Alice
print(user.get("email"))   # None (no error!)
```

**Sets** (`set`) store unique, unordered values. Created with `{1, 2, 3}` or `set()`. Note: `{}` is an empty dict, not a set — use `set()` for empty set. Sets support math operations: union `|`, intersection `&`, difference `-`.

## Why It Matters

Dicts model real-world entities (users, configs, JSON APIs). Sets deduplicate data and test membership faster than lists. Together they power counting, grouping, caching, and most data-processing code.

## Example

```python
# Dict basics
scores = {"Alice": 95, "Bob": 87}
scores["Charlie"] = 92       # Add
scores["Bob"] = 90           # Update
print(scores.get("Dave", 0)) # 0 with default

# Set basics
tags = {"python", "web", "python"}  # duplicate removed
print(tags)                  # {'python', 'web'} (order varies)
print("python" in tags)      # True — fast!

# Set math
a = {1, 2, 3}
b = {3, 4, 5}
print(a | b)  # {1, 2, 3, 4, 5} union
print(a & b)  # {3} intersection
print(a - b)  # {1, 2} difference
```

## Code

```python
# Dict patterns
user = {"name": "Alice", "age": 30, "city": "NYC"}

# Safe access
print(user["name"])                 # Direct (KeyError if missing)
print(user.get("email", "n/a"))     # Safe with default

# Iteration
for key, value in user.items():
    print(f"{key}: {value}")

for key in user.keys():
    print(key)

for value in user.values():
    print(value)

# Dict comprehension — counting words
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counts = {w: words.count(w) for w in set(words)}
print(counts)  # {'apple': 3, 'banana': 2, 'cherry': 1}

# Better counting with get()
counts2: dict[str, int] = {}
for w in words:
    counts2[w] = counts2.get(w, 0) + 1
print(counts2)

# Merging dicts (Python 3.9+)
defaults = {"theme": "light", "lang": "en"}
overrides = {"theme": "dark"}
config = defaults | overrides
print(config)  # {'theme': 'dark', 'lang': 'en'}

# Sets for dedup + membership
nums = [3, 1, 4, 1, 5, 9, 2, 6, 5]
unique = sorted(set(nums))
print(unique)  # [1, 2, 3, 4, 5, 6, 9]

# Set comprehension
squares = {x**2 for x in range(6)}
print(squares)  # {0, 1, 4, 9, 16, 25}
```

## Code Explanation

`user.get(key, default)` avoids `KeyError` — prefer it for optional keys.
`.items()`, `.keys()`, `.values()` iterate pairs, keys, values.
`counts2[w] = counts2.get(w, 0) + 1` is the classic counting pattern.
`defaults | overrides` merges dicts (right side wins). Also `dict.update()` or `{**a, **b}`.
`set(list)` removes duplicates. `sorted()` returns a deterministic order since sets are unordered.

## Common Mistakes

- `{}` creates an empty dict, not a set — use `set()` for empty set
- `dict[key]` on missing key raises `KeyError` — use `.get()` with default
- Using a list as dict key: `{[1,2]: "x"}` raises `TypeError` (unhashable)
- Assuming set order: `{"b", "a"}` may print in any order
- Modifying a dict while iterating it — iterate over `list(d.items())` or build a new dict

## Best Practices

- Use `.get()` with defaults for optional keys
- Prefer dict/set comprehensions over manual loops
- Use `collections.Counter` for counting and `defaultdict` for grouping
- Type-hint dicts: `dict[str, int]`
- Use `in` for membership: `if key in my_dict:` and `if item in my_set:`

## Exercise

Write a function `word_counts(text: str) -> dict[str, int]` that lowercases text, splits on whitespace, and returns word frequencies. Also return the set of unique words.

## Solution

```python
def word_counts(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts

# Test
text = "Hello hello world"
print(word_counts(text))       # {'hello': 2, 'world': 1}
print(set(text.lower().split()))  # {'hello', 'world'}
```

## Mini Quiz

```yaml
- question: "How do you create an empty set?"
  options: ["{}", "set()", "[]", "{:}"]
  answer: 1
  explanation: "{} is an empty dict. Use set() for an empty set."
- question: "What does `d.get('k', 0)` do if 'k' is missing?"
  options: ["Raises KeyError", "Returns 0", "Returns None", "Creates the key"]
  answer: 1
  explanation: "get() returns the default (0) instead of raising KeyError."
- question: "What is `{1, 2} & {2, 3}`?"
  options: ["{1, 2, 3}", "{2}", "{1}", "set()"]
  answer: 1
  explanation: "& is intersection — elements in both sets: {2}."
```
