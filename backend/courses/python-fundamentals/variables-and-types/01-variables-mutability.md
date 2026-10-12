---
slug: variables-and-mutability
track: python-fundamentals
trackTitle: "Python Fundamentals"
trackOrder: 1
chapter: variables-and-types
chapterTitle: "Chapter 2 — Variables & Data Types"
chapterOrder: 2
title: "Variables and Mutability"
difficulty: beginner
order: 1
estimatedMinutes: 15
tags: [python, variables, mutability]
---

## Learning Objective

Understand variable assignment, mutability vs immutability, and how Python's object model works.

## Explanation

In Python, **variables are labels attached to objects**, not boxes containing values. When you write `x = 42`, Python:
1. Creates an integer object `42` in memory
2. Makes the name `x` refer to that object

**Assignment creates a reference**, not a copy. This is crucial for understanding mutable vs immutable objects.

**Immutable objects** cannot change after creation: `int`, `float`, `str`, `tuple`, `bool`, `frozenset`.
**Mutable objects** can be modified in place: `list`, `dict`, `set`, `bytearray`.

## Why It Matters

Mutability affects how data flows through your program. Passing a list to a function allows the function to modify it. Passing a string does not. This is a common source of bugs.

## Example

```python
# Immutable: integers
x = 10
y = x      # y refers to the SAME object
x = 20     # x now refers to a NEW object (20)
print(y)   # 10 — y unchanged!

# Mutable: lists
a = [1, 2, 3]
b = a      # b refers to the SAME list
a.append(4)  # modifies the list IN PLACE
print(b)   # [1, 2, 3, 4] — b sees the change!
```

## Code

```python
# Demonstrating mutability
original_list = [1, 2, 3]
reference = original_list

print(f"Before: original={original_list}, reference={reference}")
print(f"Same object? {original_list is reference}")  # True

reference.append(4)  # Mutate through reference

print(f"After:  original={original_list}, reference={reference}")
print(f"Same object? {original_list is reference}")  # Still True!

# Contrast with immutable
original_str = "hello"
ref_str = original_str
print(f"\nString before: original='{original_str}', ref='{ref_str}'")
print(f"Same object? {original_str is ref_str}")

# Strings are immutable - this creates a NEW string
ref_str = ref_str + " world"
print(f"String after:  original='{original_str}', ref='{ref_str}'")
print(f"Same object? {original_str is ref_str}")  # False now!
```

## Code Explanation

Lines 3-4: Both variables point to the same list object.
Line 7: `append()` mutates the list in place — both variables see the change.
Line 15: String concatenation creates a **new** string object. `original_str` is unchanged.

The `is` operator checks **identity** (same object in memory), not equality.

## Common Mistakes

- Expecting `list1 = list2` to create a copy (it creates a reference)
- Using mutable default arguments: `def func(items=[]):` — the list is shared across all calls!
- Modifying a list while iterating over it
- Assuming strings can be changed in place: `s[0] = 'X'` raises TypeError

## Best Practices

- Use `list.copy()` or `list[:]` or `copy.copy()` for shallow copies
- Use `copy.deepcopy()` for nested structures
- **Never use mutable default arguments** — use `None` and create inside:
  ```python
  def add_item(item, items=None):
      if items is None:
          items = []
      items.append(item)
      return items
  ```
- Prefer immutable data when possible (tuples, frozensets, dataclasses with `frozen=True`)

## Exercise

Write a function `add_to_list(item, my_list=[])` that demonstrates the mutable default argument bug. Then fix it using the `None` pattern.

## Solution

```python
# BUGGY VERSION
def add_to_list_buggy(item, my_list=[]):
    my_list.append(item)
    return my_list

print(add_to_list_buggy(1))  # [1]
print(add_to_list_buggy(2))  # [1, 2] - BUG! List persists

# FIXED VERSION
def add_to_list_fixed(item, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(item)
    return my_list

print(add_to_list_fixed(1))  # [1]
print(add_to_list_fixed(2))  # [2] - Correct!
```

## Mini Quiz

```yaml
- question: "What happens when you assign a list to another variable?"
  options: [
    "Creates a copy of the list",
    "Creates a reference to the same list",
    "Creates a new empty list",
    "Raises an error"
  ]
  answer: 1
  explanation: "Assignment in Python creates a reference, not a copy. Both variables point to the same object."
- question: "Which of these is immutable?"
  options: ["list", "dict", "set", "tuple"]
  answer: 3
  explanation: "Tuples are immutable sequences. Lists, dicts, and sets are mutable."
- question: "Why is `def func(items=[])` dangerous?"
  options: [
    "It's slower",
    "The default list is shared across all calls",
    "It causes a syntax error",
    "It only works once"
  ]
  answer: 1
  explanation: "Default arguments are evaluated once at function definition time. The same list object is reused."
```