---
slug: if-statements
track: python-fundamentals
trackTitle: "Python Fundamentals"
trackOrder: 1
chapter: control-flow
chapterTitle: "Chapter 4 — Control Flow"
chapterOrder: 4
title: "Conditional Statements: if, elif, else"
difficulty: beginner
order: 1
estimatedMinutes: 15
tags: [python, control-flow, conditionals]
---

## Learning Objective

Write conditional logic using if, elif, and else statements with proper indentation.

## Explanation

Control flow statements let your program make decisions. Python uses **indentation** (not braces) to define blocks.

```python
if condition:
    # block runs if condition is True
elif other_condition:
    # runs if first is False and this is True
else:
    # runs if all above are False
```

Conditions evaluate to `True` or `False`. Python's truthiness: `None`, `0`, `""`, `[]`, `{}`, `set()` are falsy; everything else is truthy.

## Why It Matters

Almost every program needs conditional logic. Understanding Python's indentation-based blocks and truthiness prevents subtle bugs.

## Example

```python
age = 20
has_ticket = True

if age >= 18 and has_ticket:
    print("Entry allowed")
elif age >= 18:
    print("Ticket required")
else:
    print("Too young")
```

## Code

```python
# Basic if/elif/else
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Score: {score}, Grade: {grade}")

# Truthiness examples
values = [0, 1, "", "hello", [], [1,2], {}, {"a":1}, None, True, False]

for v in values:
    print(f"{repr(v):10} -> {bool(v)}")

# Ternary expression
status = "adult" if age >= 18 else "minor"
print(status)

# Multiple conditions
username = "alice"
is_admin = False
is_active = True

if username == "admin" or is_admin:
    access = "full"
elif is_active:
    access = "user"
else:
    access = "denied"

# Walrus operator (Python 3.8+) - assign and test
data = [1, 2, 3, 4, 5]
if (n := len(data)) > 3:
    print(f"List has {n} items, more than 3")

# Match statement (Python 3.10+) - pattern matching
command = "start"

match command:
    case "start" | "run":
        print("Starting...")
    case "stop" | "quit":
        print("Stopping...")
    case "restart":
        print("Restarting...")
    case _:
        print(f"Unknown command: {command}")
```

## Code Explanation

Lines 3-12: `elif` chain — first matching condition wins. No `switch` in Python <3.10.
Lines 15-18: Truthiness demonstration — useful for `if value:` checks.
Line 21: Ternary `X if condition else Y` — inline if/else expression.
Lines 24-30: `or`/`and` for compound conditions. Short-circuit evaluation.
Lines 33-35: Walrus `:=` assigns and returns value in expression.
Lines 38-48: `match`/`case` — structural pattern matching (Python 3.10+). `|` for alternatives, `_` for default.

## Common Mistakes

- Wrong indentation — Python requires consistent 4 spaces
- Using `=` instead of `==` in conditions
- Forgetting `:` after condition
- `if x = 5:` — syntax error (assignment, not comparison)
- Truthiness confusion: `if items:` vs `if items is not None:`

## Best Practices

- Use `elif` chains instead of nested `if`
- Prefer `if not items:` over `if len(items) == 0:`
- Use `in` for membership: `if status in ("active", "pending"):`
- Parenthesize complex conditions for readability
- Use `match` for multiple equality checks on same value (3.10+)

## Exercise

Write a function `classify_number(n: int) -> str` that returns:
- "zero" if n is 0
- "positive even" if n > 0 and even
- "positive odd" if n > 0 and odd
- "negative even" if n < 0 and even
- "negative odd" if n < 0 and odd

## Solution

```python
def classify_number(n: int) -> str:
    if n == 0:
        return "zero"
    sign = "positive" if n > 0 else "negative"
    parity = "even" if n % 2 == 0 else "odd"
    return f"{sign} {parity}"

# Test
for n in [-3, -2, 0, 2, 3]:
    print(f"{n}: {classify_number(n)}")
```

## Mini Quiz

```yaml
- question: "What does `if []:` evaluate to?"
  options: ["True", "False", "Error", "Empty list"]
  answer: 1
  explanation: "Empty list is falsy in Python. bool([]) == False."
- question: "Which is the correct syntax for elif?"
  options: ["else if", "elif", "elseif", "elsif"]
  answer: 1
  explanation: "Python uses 'elif' (short for else if)."
- question: "What does the walrus operator `:=` do?"
  options: [
    "Compares two values",
    "Assigns and returns the value in an expression",
    "Creates a new variable",
    "Checks equality"
  ]
  answer: 1
  explanation: "The walrus operator (:=) assigns a value to a variable as part of a larger expression."
```