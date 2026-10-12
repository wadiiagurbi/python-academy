---
slug: oop-classes-objects
track: intermediate-python
trackTitle: "Intermediate Python"
trackOrder: 2
chapter: oop
chapterTitle: "Chapter 1 — Object-Oriented Programming"
chapterOrder: 1
title: "Classes and Objects"
difficulty: intermediate
order: 1
estimatedMinutes: 20
tags: [python, oop, classes, objects]
---

## Learning Objective

Define classes, create objects, and understand the relationship between them.

## Explanation

Python is an object-oriented language. Everything is an object — integers, strings, functions, modules. **Classes** are blueprints for creating objects. **Objects** (instances) are concrete realizations of a class with their own state (attributes) and behavior (methods).

Key concepts:
- **`class`** keyword defines a class
- **`__init__`** initializer sets up instance state
- **`self`** refers to the instance (convention, not keyword)
- **Methods** are functions defined inside a class
- **Attributes** store per-instance data

## Why It Matters

OOP organizes code around data and behavior. It enables encapsulation (bundling data with methods), inheritance (reusing code), and polymorphism (same interface, different behavior). Most Python libraries use OOP extensively.

## Example

```python
class Dog:
    """A simple dog class."""
    
    species = "Canis familiaris"  # Class attribute (shared)
    
    def __init__(self, name: str, age: int):
        self.name = name      # Instance attribute
        self.age = age        # Instance attribute
        self.tricks = []      # Instance attribute (mutable!)
    
    def bark(self) -> str:
        return f"{self.name} says woof!"
    
    def add_trick(self, trick: str) -> None:
        self.tricks.append(trick)

# Create instances
dog1 = Dog("Buddy", 3)
dog2 = Dog("Luna", 5)

print(dog1.bark())           # Buddy says woof!
print(dog2.bark())           # Luna says woof!

dog1.add_trick("sit")
dog1.add_trick("stay")
print(dog1.tricks)           # ['sit', 'stay']
print(dog2.tricks)           # [] — separate lists!
```

## Code

```python
# More complete example with validation
class BankAccount:
    """A bank account with deposit/withdraw functionality."""
    
    def __init__(self, owner: str, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self.owner = owner
        self._balance = float(initial_balance)  # Private by convention
        self._transactions = []
    
    @property
    def balance(self) -> float:
        """Read-only property for balance."""
        return self._balance
    
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
        self._transactions.append(("deposit", amount))
    
    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            return False  # Insufficient funds
        self._balance -= amount
        self._transactions.append(("withdraw", amount))
        return True
    
    def statement(self) -> str:
        lines = [f"Account: {self.owner}", f"Balance: ${self._balance:.2f}"]
        for txn_type, amount in self._transactions:
            lines.append(f"  {txn_type.capitalize()}: ${amount:.2f}")
        return "\n".join(lines)

# Usage
account = BankAccount("Alice", 100.0)
account.deposit(50.0)
account.withdraw(30.0)
print(account.statement())
# Account: Alice
# Balance: $120.00
#   Deposit: $50.00
#   Withdraw: $30.00
```

## Code Explanation

Line 4: Docstring documents the class.
Line 7: Class attribute `species` shared by all instances.
Lines 9-13: `__init__` runs on instantiation. `self.name` creates instance attributes.
Line 18: Methods receive `self` automatically.
Line 29: Each instance gets its own `tricks` list (created in `__init__`).

BankAccount example:
- `_balance` prefix `_` signals "private" (convention only)
- `@property` makes `balance` readable like an attribute
- Validation in methods prevents invalid state
- `_transactions` tracks history

## Common Mistakes

- Mutable default arguments in `__init__`: `def __init__(self, items=[])` — shared across instances!
- Forgetting `self` in method definitions
- Modifying class attributes through instances: `dog1.species = "Wolf"` creates instance attribute, doesn't change class
- Not calling `super().__init__()` in subclasses

## Best Practices

- Use type hints for `__init__` parameters and method signatures
- Use `@property` for computed/validated attributes
- Prefix "private" attributes with `_` (single underscore)
- Keep `__init__` simple — do one thing well
- Use `@dataclass` for data-heavy classes (Python 3.7+)

## Exercise

Create a `Rectangle` class with `width` and `height` properties. Add `area()` and `perimeter()` methods. Validate that dimensions are positive.

## Solution

```python
class Rectangle:
    def __init__(self, width: float, height: float):
        if width <= 0 or height <= 0:
            raise ValueError("Dimensions must be positive")
        self._width = width
        self._height = height
    
    @property
    def width(self) -> float:
        return self._width
    
    @property
    def height(self) -> float:
        return self._height
    
    def area(self) -> float:
        return self._width * self._height
    
    def perimeter(self) -> float:
        return 2 * (self._width + self._height)

# Test
rect = Rectangle(5, 3)
print(f"Area: {rect.area()}")        # 15
print(f"Perimeter: {rect.perimeter()}")  # 16
```

## Mini Quiz

```yaml
- question: "What is the purpose of `self` in a method?"
  options: [
    "Refers to the class itself",
    "Refers to the instance calling the method",
    "Is a reserved keyword like 'this'",
    "Stores class-level data"
  ]
  answer: 1
  explanation: "self is the conventional name for the instance parameter. Python passes it automatically."
- question: "Why is `def __init__(self, items=[])` dangerous?"
  options: [
    "It's slower",
    "The default list is shared across all instances",
    "It causes a syntax error",
    "It prevents inheritance"
  ]
  answer: 1
  explanation: "Default arguments are evaluated once at class definition. All instances without explicit items share the same list."
- question: "What does `@property` do?"
  options: [
    "Makes a method callable like an attribute",
    "Makes an attribute private",
    "Creates a class attribute",
    "Defines a static method"
  ]
  answer: 0
  explanation: "@property decorator lets you access a method like an attribute: obj.balance instead of obj.balance()."
```