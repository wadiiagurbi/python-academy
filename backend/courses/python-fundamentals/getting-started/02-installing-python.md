---
slug: installing-python
track: python-fundamentals
trackTitle: "Python Fundamentals"
trackOrder: 1
chapter: getting-started
chapterTitle: "Chapter 1 — Getting Started"
chapterOrder: 1
title: "Installing Python"
difficulty: beginner
order: 2
estimatedMinutes: 12
tags: [python, installation, setup]
---

## Learning Objective

Install Python 3.11+, verify the installation, and set up a development environment.

## Explanation

Python runs on Windows, macOS, and Linux. The official installer from python.org is the most reliable way to get started. For data science work, consider **Anaconda** or **Miniconda** which bundle Python with scientific packages. For web development, the standard installer plus `pip` (Python's package manager) is perfect.

**Key tools you'll use:**
- `python3` — the interpreter
- `pip` — package installer (comes with Python 3.4+)
- `venv` — built-in virtual environment tool
- `pipx` — for installing CLI tools in isolated environments

## Why It Matters

A proper Python setup prevents "works on my machine" issues. Virtual environments isolate project dependencies — each project gets its own `site-packages` directory. This means Project A can use Django 4.2 while Project B uses Django 5.0 without conflicts.

## Example

```bash
# Check Python version
python3 --version
# Python 3.11.9

# Check pip version
pip --version

# Create a virtual environment
python3 -m venv .venv

# Activate it (Linux/macOS)
source .venv/bin/activate

# Activate it (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Install a package
pip install requests
```

## Code

```bash
# Complete setup for a new project
mkdir my-project
cd my-project
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\Activate.ps1 on Windows
pip install --upgrade pip
pip install requests pandas jupyter
```

## Code Explanation

1. `mkdir my-project` creates a project directory
2. `python3 -m venv .venv` creates a virtual environment in `.venv/`
3. `source .venv/bin/activate` activates it — your shell prompt changes to show `(.venv)`
4. `pip install --upgrade pip` updates pip to latest
5. `pip install ...` installs packages into the isolated environment

## Common Mistakes

- Installing packages globally with `pip install` instead of in a venv
- Forgetting to activate the venv before running code
- Using `python` instead of `python3` on systems where `python` points to Python 2
- Not adding `.venv/` to `.gitignore` — never commit virtual environments!

## Best Practices

- Always use a virtual environment per project
- Add `.venv/` to your `.gitignore`
- Use `pip install -r requirements.txt` for reproducible installs
- Pin versions in `requirements.txt`: `requests==2.31.0`
- Consider `pip-tools` or `uv` for dependency management

## Exercise

Create a new project directory, set up a virtual environment, activate it, and install the `requests` package. Verify by running `python -c "import requests; print(requests.__version__)"`.

## Solution

```bash
mkdir learn-python
cd learn-python
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install requests
python -c "import requests; print(requests.__version__)"
```

## Mini Quiz

```yaml
- question: "What command creates a virtual environment named '.venv'?"
  options: ["python -m venv .venv", "python -m virtualenv .venv", "venv create .venv", "python venv .venv"]
  answer: 0
  explanation: "The built-in venv module is invoked with 'python -m venv <path>'."
- question: "Why should you use virtual environments?"
  options: ["They make Python run faster", "They isolate project dependencies", "They are required by pip", "They automatically install packages"]
  answer: 1
  explanation: "Virtual environments give each project its own isolated site-packages, preventing version conflicts between projects."
```