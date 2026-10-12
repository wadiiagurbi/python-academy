---
slug: inheritance-polymorphism
track: intermediate-python
trackTitle: "Intermediate Python"
trackOrder: 2
chapter: oop
chapterTitle: "Chapter 1 — Object-Oriented Programming"
chapterOrder: 1
title: "Inheritance and Polymorphism"
difficulty: intermediate
order: 2
estimatedMinutes: 20
tags: [python, oop, inheritance, polymorphism]
---

## Learning Objective

Use inheritance to reuse code and polymorphism to write flexible, extensible designs.

## Explanation

**Inheritance** lets a child class reuse and extend a parent class:

```python
class Animal:
    def speak(self):
        return "..."

class Dog(Animal):  # Dog inherits from Animal
    def speak(self):
        return "Woof!"
```

Key tools:
- `super().__init__()` — call parent initializer
- **Method overriding** — child redefines parent method
- `isinstance(obj, Class)` — check type including inheritance
- **MRO** (Method Resolution Order) — order Python searches parents, see with `Class.__mro__`
- **Polymorphism** — same interface, different behavior: call `.speak()` on any `Animal` without knowing the exact subclass
- **Duck typing** — "if it quacks like a duck", Python cares about behavior, not declared type

## Why It Matters

Inheritance removes duplication (one `User` base, many roles). Polymorphism lets frameworks call your code without knowing its type (plugins, handlers, ORM models). Most libraries — Django, FastAPI, SQLAlchemy — rely on subclassing.

## Example

```python
class Employee:
    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary

    def bonus(self) -> float:
        return self.salary * 0.05

class Manager(Employee):
    def bonus(self) -> float:  # override
        return self.salary * 0.15 + 1000

staff = [Employee("Alice", 50000), Manager("Bob", 80000)]
for person in staff:  # polymorphism!
    print(f"{person.name}: bonus ${person.bonus():.2f}")
```

## Code

```python
from abc import ABC, abstractmethod

# Abstract base — defines interface, cannot instantiate
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        ...

    def describe(self) -> str:
        return f"{type(self).__name__} with area {self.area():.2f}"

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2

# Multiple inheritance + super() + MRO
class LoggedMixin:
    def log(self, msg: str) -> None:
        print(f"[{type(self).__name__}] {msg}")

class LoggedCircle(Circle, LoggedMixin):
    def area(self) -> float:
        result = super().area()
        self.log(f"area={result:.2f}")
        return result

# Polymorphic function — works with any Shape
def total_area(shapes: list[Shape]) -> float:
    return sum(s.area() for s in shapes)

shapes: list[Shape] = [Rectangle(3, 4), Circle(2), LoggedCircle(1)]
print(f"Total: {total_area(shapes):.2f}")
for s in shapes:
    print(s.describe())
    print(f"  isinstance Shape? {isinstance(s, Shape)}")

print(LoggedCircle.__mro__)
```

## Code Explanation

`class Shape(ABC)` with `@abstractmethod` enforces that subclasses implement `area()` — instantiating `Shape()` raises `TypeError`.
`Rectangle` and `Circle` override `area()` with their own formulas.
`LoggedCircle(Circle, LoggedMixin)` shows multiple inheritance; `super().area()` calls the next class in MRO.
`total_area()` is polymorphic — it only requires `.area()`, not a specific subclass.
`isinstance()` respects inheritance. `__mro__` shows lookup order.

## Common Mistakes

- Forgetting `super().__init__()` in child `__init__` — parent state never initialized
- Overriding without matching signature — breaks polymorphism (Liskov violation)
- Deep inheritance hierarchies (3+ levels) — prefer composition
- Using `type(x) == Dog` instead of `isinstance(x, Animal)` — misses subclasses
- Diamond inheritance confusion — check `Class.__mro__` to debug

## Best Practices

- Inherit for "is-a" relationships; compose for "has-a"
- Keep hierarchies shallow (1-2 levels)
- Use `ABC` + `@abstractmethod` for plugin interfaces
- Always call `super().__init__()` when overriding `__init__`
- Program to interfaces (duck typing) rather than concrete classes

## Exercise

Create a `Vehicle` base with `max_speed` and `range_km()` (abstract). Subclass `ElectricCar` (battery_kwh, efficiency) and `GasCar` (tank_liters, consumption). Add a polymorphic `trip_cost()` method.

## Solution

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, max_speed: float):
        self.max_speed = max_speed

    @abstractmethod
    def range_km(self) -> float:
        ...

    @abstractmethod
    def trip_cost(self, distance_km: float) -> float:
        ...

class ElectricCar(Vehicle):
    def __init__(self, max_speed: float, battery_kwh: float, kwh_per_100km: float):
        super().__init__(max_speed)
        self.battery_kwh = battery_kwh
        self.kwh_per_100km = kwh_per_100km

    def range_km(self) -> float:
        return self.battery_kwh / self.kwh_per_100km * 100

    def trip_cost(self, distance_km: float, price_per_kwh: float = 0.30) -> float:
        return distance_km / 100 * self.kwh_per_100km * price_per_kwh

class GasCar(Vehicle):
    def __init__(self, max_speed: float, tank_liters: float, liters_per_100km: float):
        super().__init__(max_speed)
        self.tank_liters = tank_liters
        self.liters_per_100km = liters_per_100km

    def range_km(self) -> float:
        return self.tank_liters / self.liters_per_100km * 100

    def trip_cost(self, distance_km: float, price_per_liter: float = 1.80) -> float:
        return distance_km / 100 * self.liters_per_100km * price_per_liter

fleet: list[Vehicle] = [ElectricCar(180, 60, 15), GasCar(200, 50, 7)]
for v in fleet:
    print(f"{type(v).__name__}: range {v.range_km():.0f}km, 100km cost ${v.trip_cost(100):.2f}")
```

## Mini Quiz

```yaml
- question: "What does `super().__init__()` do in a child class?"
  options: [
    "Creates a new parent object",
    "Calls the parent initializer to set up inherited state",
    "Skips initialization",
    "Returns the parent class"
  ]
  answer: 1
  explanation: "super() delegates to the parent in MRO order, ensuring inherited attributes are initialized."
- question: "What is polymorphism?"
  options: [
    "Multiple inheritance",
    "Same interface, different implementations",
    "Copying objects",
    "Private methods"
  ]
  answer: 1
  explanation: "Polymorphism lets you call the same method on different types, each behaving its own way."
- question: "Why use ABC with @abstractmethod?"
  options: [
    "Faster code",
    "Enforce subclasses implement required methods",
    "Prevent inheritance",
    "Auto-generate methods"
  ]
  answer: 1
  explanation: "Abstract methods must be overridden; instantiating the base without them raises TypeError."
```
