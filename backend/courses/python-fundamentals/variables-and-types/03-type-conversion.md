---
slug: type-conversion
track: python-fundamentals
trackTitle: "Python Fundamentals"
trackOrder: 1
chapter: variables-and-types
chapterTitle: "Chapter 2 — Variables & Data Types"
chapterOrder: 2
title: "Type Conversion and Casting"
difficulty: beginner
order: 3
estimatedMinutes: 12
tags: [python, types, casting, conversion]
---

## Learning Objective

Convert values between str, int, float, and bool safely and handle conversion errors.

## Explanation

**Type conversion (casting)** means creating a value of a new type from an existing value using `int()`, `float()`, `str()`, `bool()`, `list()`, `tuple()`.

Two kinds:

- **Implicit** — Python does it automatically: `3 + 4.5` gives `7.5` (int promoted to float).
- **Explicit** — you call the constructor: `int("42")` gives `42`.

Conversions can fail. `int("hello")` raises `ValueError`. User input from `input()` is always `str`, so you almost always need to convert it.

Truthiness for `bool()`: `0`, `0.0`, `""`, `[]`, `{}`, `None` are `False`; most other values are `True`.

## Why It Matters

Almost every program mixes types: reading CSV data (all strings), parsing user input, formatting output, doing math. A wrong conversion crashes your program or silently produces wrong results. Mastering casting prevents the most common beginner `ValueError` and `TypeError`.

## Example

```python
# Explicit conversion
age_str = "28"
age = int(age_str)          # 28
price = float("19.99")      # 19.99
label = str(42)             # "42"

# Implicit promotion
result = 3 + 4.5            # 7.5 (float)

# bool() truthiness
print(bool(0))              # False
print(bool(""))             # False
print(bool("hello"))        # True
print(bool([]))             # False
```

## Code

```python
# Safe conversion patterns
raw_age = "29"
raw_price = "19.99"
raw_bad = "twenty"

# Basic casts
age = int(raw_age)
price = float(raw_price)
print(f"Age: {age} ({type(age).__name__}), Price: {price}")

# int() from float truncates toward zero
print(int(3.9))    # 3
print(int(-3.9))   # -3 (not -4!)

# Rounding vs truncating
print(round(3.5))  # 4
print(round(2.675, 2))  # 2.67 (floating-point quirk!)

# Safe conversion with error handling
def safe_int(value: str, default: int = 0) -> int:
    try:
        return int(value.strip())
    except (ValueError, AttributeError):
        return default

print(safe_int(" 42 "))     # 42
print(safe_int("abc"))      # 0
print(safe_int("3.9"))      # 0 (int() rejects decimal strings!)

# Correct way: string -> float -> int
print(int(float("3.9")))    # 3

# input() is always str — convert immediately
# n = int(input("Enter a number: "))

# Joining and splitting (str <-> list)
words = ["red", "green", "blue"]
csv_line = ",".join(words)          # "red,green,blue"
back_to_list = csv_line.split(",")  # ["red", "green", "blue"]
print(csv_line, back_to_list)
```

## Code Explanation

Lines 6-7: `int()` and `float()` parse numeric strings.
Lines 10-11: `int()` truncates, it does not round. Use `round()` for rounding.
Lines 17-22: `safe_int()` wraps conversion in try/except and strips whitespace. Returns a default on failure — a robust pattern for user input.
Line 28: `int("3.9")` fails. Chain `int(float(...))` when input may contain decimals.
Lines 34-36: `",".join(list)` and `str.split()` convert between strings and lists.

## Common Mistakes

- `int("3.9")` — ValueError; use `int(float("3.9"))` or `float()` directly
- `int("")` or `int(None)` — ValueError / TypeError; validate first
- Forgetting `input()` returns str: `"5" + "5"` is `"55"`, not `10`
- `round(2.675, 2)` giving `2.67` — floating-point representation, not a bug in your code
- Using `bool("False")` expecting `False` — any non-empty string is `True`!

## Best Practices

- Validate and convert at the boundary (user input, file I/O, API responses)
- Use try/except for conversions that may fail; provide defaults or clear error messages
- Prefer `float()` for decimal input, then convert to `int` if needed
- Use f-strings `f"{value}"` or `str(value)` for display, not concatenation with `+`
- Compare `bool("False") is True` — remember to parse flags explicitly: `value.lower() == "true"`

## Exercise

Write a function `parse_price(raw: str) -> float` that strips whitespace and `$`, converts to float, and returns `0.0` on failure. Test with `"$19.99 "`, `"abc"`, `"42"`.

## Solution

```python
def parse_price(raw: str) -> float:
    try:
        cleaned = raw.strip().replace("$", "")
        return float(cleaned)
    except (ValueError, AttributeError):
        return 0.0

# Test
print(parse_price("$19.99 "))  # 19.99
print(parse_price("abc"))      # 0.0
print(parse_price("42"))       # 42.0
```

## Mini Quiz

```yaml
- question: "What does `int('3.9')` do?"
  options: ["Returns 3", "Returns 4", "Raises ValueError", "Returns 3.9"]
  answer: 2
  explanation: "int() cannot parse decimal strings. Use int(float('3.9')) to get 3."
- question: "What is `bool('False')`?"
  options: ["False", "True", "Error", "None"]
  answer: 1
  explanation: "Any non-empty string is truthy, even the string 'False'."
- question: "What type does `input()` return?"
  options: ["int", "str", "It depends on input", "bool"]
  answer: 1
  explanation: "input() always returns str. Convert with int() or float() as needed."
```
