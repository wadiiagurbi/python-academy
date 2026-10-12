---
slug: what-is-python
track: python-fundamentals
trackTitle: "Python Fundamentals"
trackOrder: 1
chapter: getting-started
chapterTitle: "Chapter 1 — Getting Started"
chapterOrder: 1
title: "What is Python?"
difficulty: beginner
order: 1
estimatedMinutes: 8
tags: [python, basics, introduction]
---

## Learning Objective

Understand what Python is, why it's popular, and what you can build with it.

## Explanation

Python is a high-level, interpreted programming language created by Guido van Rossum and first released in 1991. It's designed to be readable and expressive — code that reads almost like English. Python emphasizes simplicity and clarity, making it an ideal first language while remaining powerful enough for experts.

Python is **interpreted**, meaning you don't compile it before running. The Python interpreter reads your code line by line and executes it immediately. This makes development fast — write code, run it, see results instantly.

Python is **dynamically typed** — you don't declare variable types. The interpreter figures out types at runtime. This flexibility speeds up prototyping but requires good testing.

## Why It Matters

Python consistently ranks among the top 3 most popular programming languages worldwide (TIOBE, GitHub, Stack Overflow). It's used by Google, Netflix, NASA, Instagram, Spotify, and countless startups. Learning Python opens doors to web development, data science, AI/ML, automation, scientific computing, and more.

## Example

```python
# A simple Python program
print("Hello, World!")
```

## Code

```python
# This is a comment - Python ignores it
print("Hello, Python Academy!")

# Variables
language = "Python"
year = 2026
is_awesome = True

# Print with f-strings (formatted strings)
print(f"Learning {language} in {year}: {is_awesome}")
```

## Code Explanation

Line 1: A comment starting with `#` — Python ignores everything after `#` on that line.
Line 2: `print()` outputs text to the console.
Line 5-7: Variable assignment. Python infers types: `str`, `int`, `bool`.
Line 10: An f-string (formatted string literal) — `{variable}` inserts the variable's value.

## Common Mistakes

- Forgetting parentheses: `print "hello"` (works in Python 2, **syntax error in Python 3**)
- Mixing tabs and spaces for indentation — Python uses indentation for blocks
- Using `=` (assignment) instead of `==` (comparison) in conditions

## Best Practices

- Use 4 spaces per indentation level (never tabs)
- Write comments for "why", not "what" — code shows what
- Follow PEP 8 style guide (use `ruff` or `black` to auto-format)
- Use descriptive variable names: `user_count` not `uc`

## Exercise

Write a program that prints your name, age, and favorite programming language using variables and an f-string.

## Solution

```python
name = "Alex"
age = 28
favorite_language = "Python"
print(f"My name is {name}, I'm {age} years old, and I love {favorite_language}!")
```

## Mini Quiz

```yaml
- question: "What symbol starts a single-line comment in Python?"
  options: ["//", "#", "/*", "--"]
  answer: 1
  explanation: "The # symbol starts a comment. Everything after it on that line is ignored."
- question: "Which of these is a valid variable name in Python?"
  options: ["2cool", "my-variable", "my_variable", "class"]
  answer: 2
  explanation: "Variable names must start with a letter or underscore, can contain letters, numbers, underscores. 'class' is a reserved keyword."
```