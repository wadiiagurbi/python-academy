---
slug: loops-for-while
track: python-fundamentals
trackTitle: "Python Fundamentals"
trackOrder: 1
chapter: control-flow
chapterTitle: "Chapter 4 — Control Flow"
chapterOrder: 4
title: "Loops: for and while"
difficulty: beginner
order: 2
estimatedMinutes: 18
tags: [python, loops, for, while]
---

## Learning Objective

Iterate with for loops and while loops, and control them with break, continue, and else.

## Explanation

**`for`** iterates over a sequence (list, string, range, dict, file). Use it when you know what to iterate.

```python
for fruit in ["apple", "banana"]:
    print(fruit)
```

**`while`** repeats while a condition is `True`. Use it when iterations depend on a changing condition (user input, convergence, polling).

```python
n = 3
while n > 0:
    print(n)
    n -= 1
```

Control keywords: `break` exits the loop, `continue` skips to next iteration, `else` on a loop runs if no `break` occurred.

## Why It Matters

Loops automate repetition — processing rows, retrying operations, polling sensors, game loops. Choosing `for` vs `while` correctly and avoiding infinite loops is a core programming skill.

## Example

```python
# for with range and enumerate
for i in range(3):
    print(f"step {i}")

for index, name in enumerate(["Alice", "Bob"]):
    print(f"{index}: {name}")

# while with break
while True:
    cmd = input("Type 'quit': ")
    if cmd == "quit":
        break
    print(f"You typed: {cmd}")
```

## Code

```python
# for patterns
fruits = ["apple", "banana", "cherry"]

for f in fruits:
    print(f)

# range(start, stop, step)
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8

# enumerate() instead of range(len())
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")

# zip() for parallel iteration
names = ["Alice", "Bob"]
scores = [95, 87]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# break / continue / else
for n in range(2, 10):
    if n % 2 == 0:
        continue  # skip evens
    print(f"odd: {n}")
else:
    print("Loop finished without break")

# while pattern with counter
countdown = 3
while countdown > 0:
    print(countdown)
    countdown -= 1
print("Go!")

# while with sentinel + break
attempts = 0
while attempts < 3:
    password = "secret"  # pretend input()
    if password == "secret":
        print("Access granted")
        break
    attempts += 1
else:
    print("Locked out")

# List comprehension (for-expression alternative)
squares = [x**2 for x in range(6)]
print(squares)  # [0, 1, 4, 9, 16, 25]
```

## Code Explanation

`range(0, 10, 2)` generates 0 to 8 stepping by 2 (stop is exclusive).
`enumerate(list, start=1)` yields (index, item) — cleaner than `range(len(...))`.
`zip()` stops at the shortest input.
`continue` skips the rest of the body for that iteration.
`for...else` / `while...else`: `else` runs only if the loop was not exited via `break` — useful for search patterns.
`while` must update its condition (`countdown -= 1`) or it loops forever.

## Common Mistakes

- Infinite `while True` without `break` or condition update
- Modifying a list while iterating it — iterate over a copy `for x in lst[:]:` or build a new list
- Off-by-one with `range()`: `range(10)` is 0-9, not 1-10
- Forgetting `:` after `for` / `while` line
- Using `break` when you meant `continue` (and vice versa)

## Best Practices

- Prefer `for` over `while` when iterating a known collection
- Use `enumerate()` and `zip()` instead of manual indexing
- Keep `while` conditions simple; always ensure progress toward exit
- Use list comprehensions for simple transforms: `[f(x) for x in items if cond]`
- Extract complex loop bodies into functions for readability

## Exercise

Write a function `find_first_even(nums: list[int]) -> int | None` that returns the first even number using a for loop with break/else, or `None` if there is none. Also write `countdown(n)` using while.

## Solution

```python
def find_first_even(nums: list[int]) -> int | None:
    for n in nums:
        if n % 2 == 0:
            return n
    return None

def countdown(n: int) -> None:
    while n > 0:
        print(n)
        n -= 1
    print("Go!")

# Test
print(find_first_even([1, 3, 7, 8, 10]))  # 8
print(find_first_even([1, 3, 5]))         # None
countdown(3)
```

## Mini Quiz

```yaml
- question: "What does `range(3)` produce?"
  options: ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "3, 2, 1"]
  answer: 1
  explanation: "range(3) yields 0, 1, 2. Stop is exclusive, start defaults to 0."
- question: "What does `continue` do?"
  options: ["Exits the loop", "Skips to next iteration", "Restarts the loop", "Pauses the loop"]
  answer: 1
  explanation: "continue skips the rest of the current iteration and moves to the next one."
- question: "When does a loop's `else` block run?"
  options: ["Always", "When the loop finishes without break", "When break is hit", "On error"]
  answer: 1
  explanation: "Loop else runs only if the loop completed normally (no break)."
```
