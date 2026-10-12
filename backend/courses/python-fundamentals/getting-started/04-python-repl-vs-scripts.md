---
slug: python-repl-vs-scripts
track: python-fundamentals
trackTitle: "Python Fundamentals"
trackOrder: 1
chapter: getting-started
chapterTitle: "Chapter 1 — Getting Started"
chapterOrder: 1
title: "Python REPL vs Scripts"
difficulty: beginner
order: 4
estimatedMinutes: 10
tags: [python, repl, scripts, basics]
---

## Learning Objective

Understand the difference between the interactive REPL and script files, and know when to use each.

## Explanation

Python gives you two main ways to run code:

**1. REPL (Read-Eval-Print Loop)** — an interactive prompt. You type one line, Python runs it immediately and shows the result. Start it with `python` or `python3` with no arguments:

```
$ python
>>> 2 + 3
5
>>> name = "Alice"
>>> print(f"Hi {name}")
Hi Alice
```

`>>>` is the prompt. `...` is the continuation prompt for multi-line blocks.

**2. Scripts** — text files ending in `.py` containing a full program. You run them with `python filename.py`. The interpreter executes the file top to bottom.

```bash
python hello.py
```

Use the REPL for experimentation and the script for anything you want to save, share, or re-run.

## Why It Matters

Beginners who only use scripts miss fast feedback. Professionals who only use the REPL lose reproducibility. Knowing both makes you faster: test an idea in the REPL in 5 seconds, then paste the working code into a script. Every Python workflow — notebooks, debugging, testing — builds on this distinction.

## Example

```python
# In the REPL (type line by line):
>>> x = 10
>>> y = 20
>>> x + y
30
>>> for i in range(3):
...     print(f"count: {i}")
...
count: 0
count: 1
count: 2
```

## Code

```python
# hello.py — a script file you can save and re-run
import sys

def greet(name: str) -> str:
    return f"Hello, {name}!"

def main() -> None:
    # sys.argv holds command-line arguments
    # sys.argv[0] is the script name itself
    name = sys.argv[1] if len(sys.argv) > 1 else "World"
    print(greet(name))
    print(f"Python version check passed!")

if __name__ == "__main__":
    main()
```

Run it:

```bash
python hello.py
# Hello, World!

python hello.py Alice
# Hello, Alice!
```

## Code Explanation

Line 2: `import sys` gives access to command-line arguments.
Lines 4-5: `greet()` is a reusable function — scripts let you organize code into functions.
Lines 7-11: `main()` reads `sys.argv`. If the user passed a name, use it; otherwise default to "World".
Line 13: `if __name__ == "__main__":` means "run this only when executed as a script, not when imported". This is a standard Python idiom.
Line 14: Call `main()` to start the program.

In the REPL there is no `__main__` guard needed — every line runs immediately.

## Common Mistakes

- Pasting `>>>` prompts into a script file — `>>> print("hi")` is a syntax error in a `.py` file
- Typing `python hello.py` inside the REPL instead of the terminal
- Forgetting to exit the REPL — use `exit()` or Ctrl+D (Mac/Linux) / Ctrl+Z then Enter (Windows)
- Saving experiments only in REPL history and losing them — move working code to a file

## Best Practices

- Use the REPL to test a single function, expression, or library call before adding it to your project
- Use `python -i script.py` to run a script then drop into the REPL with its variables loaded for inspection
- Prefer `ipython` or `ptpython` for a better REPL (history, autocomplete) once comfortable
- Keep scripts under version control; REPL sessions are throwaway
- Add `if __name__ == "__main__":` to every runnable script

## Exercise

1. Start the REPL and compute `7 * 6`, then define a variable `city = "Berlin"` and print `f"I live in {city}"`.
2. Create a file `greet.py` with a `greet(name)` function and a `main()` that greets the name from `sys.argv` (default "Pythonista"). Run it with and without an argument.

## Solution

```python
# REPL session (type interactively):
# >>> 7 * 6
# 42
# >>> city = "Berlin"
# >>> print(f"I live in {city}")
# I live in Berlin

# greet.py
import sys

def greet(name: str) -> str:
    return f"Hello, {name}! Welcome to Python."

def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "Pythonista"
    print(greet(name))

if __name__ == "__main__":
    main()
```

## Mini Quiz

```yaml
- question: "What does REPL stand for?"
  options: ["Read-Eval-Print Loop", "Run-Every-Python-Line", "Rapid-Edit-Program-Launch", "Read-Execute-Program-Library"]
  answer: 0
  explanation: "REPL = Read-Eval-Print Loop: read input, evaluate it, print the result, loop."
- question: "How do you run a script file named app.py?"
  options: ["python app.py", "run app.py", "app.py python", "execute app.py"]
  answer: 0
  explanation: "Run scripts from the terminal with `python app.py`."
- question: "What does `if __name__ == '__main__':` do?"
  options: [
    "Checks the file name",
    "Runs the block only when the file is executed as a script, not when imported",
    "Always runs the block",
    "Prevents the script from running"
  ]
  answer: 1
  explanation: "When imported, __name__ is the module name. When run directly, it is '__main__'."
```
