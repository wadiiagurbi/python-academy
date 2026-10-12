---
slug: collections-lists-tuples
track: python-fundamentals
trackTitle: "Python Fundamentals"
trackOrder: 1
chapter: collections
chapterTitle: "Chapter 3 — Collections"
chapterOrder: 3
title: "Lists and Tuples"
difficulty: beginner
order: 1
estimatedMinutes: 18
tags: [python, lists, tuples, collections]
---

## Learning Objective

Master Python's two fundamental sequence types: mutable lists and immutable tuples.

## Explanation

**Lists** (`list`) are ordered, mutable collections. Created with `[ ]`. Support indexing, slicing, appending, removing, sorting.

**Tuples** (`tuple`) are ordered, immutable collections. Created with `( )` or just commas. Used for fixed data, multiple return values, dictionary keys.

Both support:
- Indexing: `seq[0]`, `seq[-1]`
- Slicing: `seq[1:4]`, `seq[::2]`
- Iteration: `for item in seq`
- `len()`, `in`, `+`, `*`

## Why It Matters

Lists are the workhorse of Python data manipulation. Tuples provide lightweight immutable records. Choosing the right one affects performance and correctness.

## Example

```python
# List - mutable
colors = ["red", "green", "blue"]
colors.append("yellow")      # Add to end
colors.insert(0, "purple")   # Insert at index
colors[1] = "cyan"           # Modify

# Tuple - immutable
point = (3, 4)
x, y = point                 # Unpacking
# point[0] = 5               # TypeError!

# Both support slicing
print(colors[1:3])           # ['cyan', 'blue']
print(point[::-1])           # (4, 3) - reversed
```

## Code

```python
# List methods demo
numbers = [3, 1, 4, 1, 5]
print(f"Original: {numbers}")

numbers.append(9)           # Add to end
numbers.extend([2, 6])      # Extend with iterable
numbers.insert(0, 0)        # Insert at index
print(f"After adds: {numbers}")

popped = numbers.pop()      # Remove and return last
removed = numbers.pop(2)    # Remove at index
numbers.remove(1)           # Remove first occurrence of value
print(f"After removes: {numbers}")

numbers.sort()              # In-place sort
print(f"Sorted: {numbers}")

reversed_nums = sorted(numbers, reverse=True)  # New sorted list
print(f"Reverse sorted: {reversed_nums}")

# List comprehensions - Pythonic!
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
matrix = [[i*j for j in range(3)] for i in range(3)]
print(f"Squares: {squares}")
print(f"Evens: {evens}")
print(f"Matrix: {matrix}")

# Tuple use cases
def get_coordinates():
    return (10, 20)  # Multiple return values

x, y = get_coordinates()  # Unpacking

# Named tuple - lightweight record
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y', 'z'])
origin = Point(0, 0, 0)
print(f"Origin: x={origin.x}, y={origin.y}, z={origin.z}")

# Tuple as dict key (must be immutable)
locations = {
    (40.7128, -74.0060): "New York",
    (34.0522, -118.2437): "Los Angeles",
}
```

## Code Explanation

List methods: `append`, `extend`, `insert`, `pop`, `remove`, `sort` (in-place) vs `sorted()` (returns new).
List comprehensions: `[expr for item in iterable if condition]` — Pythonic, fast, readable.
Tuples: unpacking `x, y = point`, multiple return values, `namedtuple` for named fields.
Tuples as dict keys: only immutable types can be keys.

## Common Mistakes

- `list.sort()` returns `None` (modifies in place), use `sorted()` for new list
- Modifying list while iterating: use `[x for x in lst if condition]` instead
- Forgetting tuples need trailing comma for single element: `(1,)` not `(1)`
- Using list when tuple is more appropriate (fixed data, dict keys)

## Best Practices

- Use list comprehensions over `map()`/`filter()` for readability
- Prefer tuples for fixed-size, heterogeneous data
- Use `enumerate()` instead of `range(len())`: `for i, item in enumerate(lst)`
- Use `zip()` for parallel iteration: `for a, b in zip(list1, list2)`
- Consider `collections.deque` for frequent left-side operations

## Exercise

Write a function `unique_sorted(items: list) -> list` that returns a new list with unique elements from `items`, sorted ascending. Use a set for deduplication.

## Solution

```python
def unique_sorted(items: list) -> list:
    return sorted(set(items))

# Test
print(unique_sorted([3, 1, 4, 1, 5, 9, 2, 6, 5]))  # [1, 2, 3, 4, 5, 6, 9]
```

## Mini Quiz

```yaml
- question: "What does `list.sort()` return?"
  options: ["The sorted list", "None", "A new sorted list", "Number of elements"]
  answer: 1
  explanation: "sort() modifies the list in place and returns None. Use sorted() for a new list."
- question: "How do you create a single-element tuple?"
  options: ["(1)", "(1,)", "[1]", "{1}"]
  answer: 1
  explanation: "The trailing comma makes it a tuple. (1) is just a parenthesized integer."
- question: "Which is more memory efficient for a fixed collection of 3 coordinates?"
  options: ["List", "Tuple"]
  answer: 1
  explanation: "Tuples are more memory efficient and faster for fixed data since they're immutable."
```