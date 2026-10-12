---
slug: your-first-python-script
track: python-fundamentals
trackTitle: "Python Fundamentals"
trackOrder: 1
chapter: getting-started
chapterTitle: "Chapter 1 — Getting Started"
chapterOrder: 1
title: "Your First Python Script"
difficulty: beginner
order: 3
estimatedMinutes: 10
tags: [python, script, hello-world]
---

## Learning Objective

Write, save, and run a Python script from the command line.

## Explanation

A Python script is just a text file with a `.py` extension containing Python code. You can write it in any text editor (VS Code, PyCharm, Vim, Notepad++). The Python interpreter reads the file top to bottom and executes each statement.

**REPL vs Scripts:**
- **REPL** (Read-Eval-Print Loop): Interactive, great for experimenting. Run `python3` with no arguments.
- **Scripts**: Saved to files, reusable, better for real programs.

## Why It Matters

Running scripts is how you execute real programs. Every Python application starts as a script (or module). Understanding the edit-save-run cycle is fundamental to development.

## Example

```bash
# Create a file
echo 'print("Hello from a script!")' > hello.py

# Run it
python3 hello.py
# Output: Hello from a script!
```

## Code

```python
# hello.py - My first Python script
"""
A simple script that greets the user.
Run with: python3 hello.py
"""

def greet(name: str) -> str:
    """Return a greeting for the given name."""
    return f"Hello, {name}! Welcome to Python Academy."

if __name__ == "__main__":
    # This block runs only when script is executed directly
    user_name = "Student"
    message = greet(user_name)
    print(message)
    
    # Also demonstrate command-line arguments
    import sys
    if len(sys.argv) > 1:
        print(f"Extra argument received: {sys.argv[1]}")
```

## Code Explanation

Line 1: Comment describing the file.
Lines 3-5: A **docstring** (triple-quoted string) — documents the module.
Lines 7-9: A **function** with type hints (`name: str` parameter, `-> str` return type).
Line 12: `if __name__ == "__main__":` — this block runs only when the file is executed directly, not when imported.
Line 15: `sys.argv` gives command-line arguments as a list. `sys.argv[0]` is the script name.

## Common Mistakes

- Forgetting to save the file before running
- Running `python3 hello.py` from the wrong directory
- Indentation errors — Python uses indentation for blocks (4 spaces standard)
- Naming your script the same as a standard library module (e.g., `random.py`)

## Best Practices

- Always include `if __name__ == "__main__":` guard
- Add a module docstring at the top
- Use type hints for function signatures
- Keep scripts focused — one main purpose per file
- Use `.py` extension (not `.pyw` or others)

## Exercise

Create a script `greet.py` that:
1. Defines a function `create_greeting(name, greeting="Hello")` returning a formatted string
2. Calls it with your name and prints the result
3. Accepts an optional command-line argument for the name

## Solution

```python
# greet.py
import sys

def create_greeting(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "World"
    print(create_greeting(name))
```

Run: `python3 greet.py Alice` → `Hello, Alice!`

## Mini Quiz

```yaml
- question: "What does the `if __name__ == '__main__':` block do?"
  options: [
    "Runs when the module is imported",
    "Runs only when the script is executed directly",
    "Defines the main function",
    "Imports the main module"
  ]
  answer: 1
  explanation: "Python sets __name__ to '__main__' when running a script directly, but to the module name when imported."
- question: "What is `sys.argv[0]`?"
  options: ["First command-line argument", "Script name/path", "Number of arguments", "Python version"]
  answer: 1
  explanation: "sys.argv[0] is always the script name. Arguments start at index 1."
```