---
slug: basic-data-types
track: python-fundamentals
trackTitle: "Python Fundamentals"
trackOrder: 1
chapter: variables-and-types
chapterTitle: "Chapter 2 — Variables & Data Types"
chapterOrder: 2
title: "Basic Data Types: Numbers, Strings, Booleans"
difficulty: beginner
order: 2
estimatedMinutes: 15
tags: [python, data-types, numbers, strings, booleans]
---

## Learning Objective

Master Python's core built-in data types: integers, floats, strings, and booleans.

## Explanation

Python has a rich set of built-in types. The most fundamental:

- **`int`** — Arbitrary precision integers (no overflow!)
- **`float`** — IEEE 754 double-precision floating point
- **`str`** — Unicode text sequences (immutable)
- **`bool`** — `True` and `False` (subclass of `int`: `True == 1`, `False == 0`)

There's also `complex` for complex numbers, `bytes`/`bytearray` for binary data, and `NoneType` for the `None` singleton.

## Why It Matters

Every program manipulates data. Understanding type behavior — especially numeric precision, string encoding, and boolean logic — prevents subtle bugs.

## Example

```python
# Numbers
age = 25                    # int
price = 19.99               # float
scientific = 1.5e-10        # scientific notation
complex_num = 3 + 4j        # complex

# Strings
name = "Alice"              # double quotes
city = 'New York'           # single quotes
multiline = """Line 1
Line 2"""                   # triple quotes

# Booleans
is_student = True
has_graduated = False

# None
result = None               # absence of value
```

## Code

```python
# Numeric operations
a, b = 10, 3
print(f"Addition: {a + b}")        # 13
print(f"Subtraction: {a - b}")     # 7
print(f"Multiplication: {a * b}")  # 30
print(f"Division: {a / b}")        # 3.333... (always float)
print(f"Floor division: {a // b}") # 3 (integer division)
print(f"Modulo: {a % b}")          # 1 (remainder)
print(f"Power: {a ** b}")          # 1000

# Float precision gotcha
print(f"0.1 + 0.2 = {0.1 + 0.2}")  # 0.30000000000000004
# Fix: use decimal module for money
from decimal import Decimal
print(Decimal('0.1') + Decimal('0.2'))  # 0.3

# String operations
first, last = "Alice", "Smith"
full = first + " " + last           # concatenation
print(full)
print(f"Length: {len(full)}")       # 11
print(f"Upper: {full.upper()}")     # ALICE SMITH
print(f"Lower: {full.lower()}")     # alice smith
print(f"Split: {full.split()}")     # ['Alice', 'Smith']
print(f"Replace: {full.replace('Alice', 'Bob')}")  # Bob Smith

# Boolean logic
x, y = True, False
print(f"and: {x and y}")   # False
print(f"or: {x or y}")     # True
print(f"not: {not x}")     # False

# Truthiness - everything has a boolean value
print(bool(0))      # False
print(bool(42))     # True
print(bool(""))     # False
print(bool("hi"))   # True
print(bool([]))     # False
print(bool([1]))    # True
```

## Code Explanation

Numeric operators: `/` always returns float, `//` floor division returns int.
Float precision: binary floating point can't represent 0.1 exactly — use `decimal.Decimal` for financial calculations.
Strings: rich methods for manipulation. `split()` without args splits on whitespace.
Booleans: `and`/`or` short-circuit (return actual operand, not just True/False).
Truthiness: empty/zero → False, non-empty/non-zero → True.

## Common Mistakes

- Using `==` with floats: `0.1 + 0.2 == 0.3` is False!
- Forgetting strings are immutable: `s[0] = 'X'` raises TypeError
- Confusing `is` (identity) with `==` (equality) — only use `is` for `None`, `True`, `False`
- `and`/`or` return the operand, not `True`/`False`: `[] or "default"` returns `"default"`

## Best Practices

- Use `Decimal` for money/currency
- Use f-strings for formatting: `f"{value:.2f}"`
- Use `is None` / `is not None` for None checks
- Leverage truthiness: `if items:` not `if len(items) > 0:`
- Use `str.isdigit()`, `str.isalpha()` for validation

## Exercise

Write a function `calculate_discount(price: float, discount_percent: float) -> Decimal` that returns the discounted price using `Decimal` for precision. Test with `price=19.99, discount_percent=20`.

## Solution

```python
from decimal import Decimal, ROUND_HALF_UP

def calculate_discount(price: float, discount_percent: float) -> Decimal:
    price_dec = Decimal(str(price))
    discount = Decimal(str(discount_percent)) / Decimal('100')
    discounted = price_dec * (Decimal('1') - discount)
    return discounted.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

# Test
result = calculate_discount(19.99, 20)
print(result)  # 15.99
```

## Mini Quiz

```yaml
- question: "What is the result of `0.1 + 0.2 == 0.3` in Python?"
  options: ["True", "False"]
  answer: 1
  explanation: "Binary floating point precision error. 0.1 + 0.2 = 0.30000000000000004"
- question: "Which string method splits on whitespace by default?"
  options: ["split(' ')", "split()", "split('\\n')", "split(',')"]
  answer: 1
  explanation: "str.split() with no arguments splits on any whitespace and handles multiple spaces."
- question: "What does `[] or 'default'` evaluate to?"
  options: ["True", "False", "[]", "'default'"]
  answer: 3
  explanation: "or returns the first truthy operand, or the last if all falsy. Empty list is falsy."
```