---
slug: pydantic-validation
track: web-development
trackTitle: "Web Development (FastAPI)"
trackOrder: 4
chapter: fastapi-basics
chapterTitle: "Chapter 1 — FastAPI Basics"
chapterOrder: 1
title: "Pydantic Validation and Settings"
difficulty: intermediate
order: 2
estimatedMinutes: 20
tags: [python, fastapi, pydantic, validation]
---

## Learning Objective

Validate request data with Pydantic v2 models, custom validators, and nested schemas.

## Explanation

**Pydantic** validates data at runtime using type hints. In Pydantic v2 (used by FastAPI):

- `BaseModel` defines a schema. Instantiation validates and coerces.
- `Field()` adds constraints: `min_length`, `max_length`, `gt`, `lt`, `pattern`.
- `@field_validator()` checks a single field; `@model_validator()` checks the whole model.
- Models nest: a `User` can contain an `Address`.
- `model_dump()` serializes to dict; `model_dump_json()` to JSON.
- `ConfigDict` configures behavior (`str_strip_whitespace`, `extra="forbid"`).

FastAPI uses these models for request bodies, responses, and query params — invalid data becomes a `422` response automatically.

## Why It Matters

Without validation, bad input causes crashes deep in your code or corrupt DB rows. Pydantic moves checks to the boundary with clear errors and free OpenAPI docs. It is the backbone of every FastAPI endpoint.

## Example

```python
from pydantic import BaseModel, Field, ValidationError

class UserIn(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=0, le=130)

try:
    UserIn(name="A", age=-5)
except ValidationError as e:
    print(e.errors())
# 2 errors: name too short, age out of range
```

## Code

```python
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
from pydantic import ConfigDict
from typing import Optional

class Address(BaseModel):
    street: str = Field(min_length=1, max_length=100)
    city: str = Field(min_length=1, max_length=50)
    zip_code: str = Field(pattern=r"^\d{5}(-\d{4})?$")

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    age: Optional[int] = Field(default=None, ge=13, le=130)
    address: Optional[Address] = None
    tags: list[str] = Field(default_factory=list, max_length=10)

    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if v.lower() == v or v.upper() == v:
            raise ValueError("must contain mixed case")
        if not any(c.isdigit() for c in v):
            raise ValueError("must contain a digit")
        return v

    @model_validator(mode="after")
    def check_consistency(self):
        # Example cross-field rule
        if self.age is not None and self.age < 18 and self.address is None:
            raise ValueError("minors must provide an address")
        return self

# Valid
user = UserCreate(
    username="alice_01",
    email="alice@example.com",
    password="S3cretPass",
    age=16,
    address={"street": "123 Main", "city": "NYC", "zip_code": "10001"},
)
print(user.model_dump())

# Invalid — see structured errors
try:
    UserCreate(username="ab", email="not-an-email", password="weak")
except Exception as e:
    from pydantic import ValidationError
    if isinstance(e, ValidationError):
        for err in e.errors():
            print(err["loc"], "->", err["msg"])

# Partial update model (PATCH pattern)
class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=30)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(default=None, ge=13, le=130)

patch = UserUpdate(username="bob")
print(patch.model_dump(exclude_unset=True))  # {'username': 'bob'}
```

## Code Explanation

`Field(pattern=...)` enforces regex; `EmailStr` validates email format (needs `email-validator` package).
`default_factory=list` avoids shared mutable defaults.
`@field_validator("password")` runs after type coercion; raise `ValueError` to fail validation.
`@model_validator(mode="after")` sees the whole model (`self`) for cross-field rules.
`model_dump(exclude_unset=True)` returns only provided fields — ideal for PATCH.
`ConfigDict(extra="forbid")` rejects unknown fields; `str_strip_whitespace` trims strings.

## Common Mistakes

- `tags: list = []` as default — shared list! Use `Field(default_factory=list)`
- Forgetting `@classmethod` on `@field_validator` methods
- Using `Optional[str]` without default `None` — still required in v2!
- Expecting `Field(max_length=...)` on int — length applies to strings/collections; use `le`/`ge` for numbers
- Not installing `email-validator` — `EmailStr` fails at import without it

## Best Practices

- Separate `Create`, `Update`, and `Read` models (`UserCreate`, `UserUpdate`, `UserRead`)
- Use `exclude_unset=True` for PATCH, `response_model` for outputs
- Forbid extras on strict inputs: `extra="forbid"`
- Keep validators small and pure; raise `ValueError` with clear messages
- Reuse nested models (`Address`) instead of flat fields

## Exercise

Create a `ProductCreate` model: `name` (3-100 chars), `price` (gt 0, le 100000), `sku` (pattern uppercase letters/digits/dashes), `stock` (ge 0, default 0). Add a validator ensuring `price` has at most 2 decimals.

## Solution

```python
from pydantic import BaseModel, Field, field_validator

class ProductCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    price: float = Field(gt=0, le=100_000)
    sku: str = Field(pattern=r"^[A-Z0-9-]+$")
    stock: int = Field(default=0, ge=0)

    @field_validator("price")
    @classmethod
    def max_two_decimals(cls, v: float) -> float:
        if round(v, 2) != v:
            raise ValueError("price must have at most 2 decimals")
        return v

# Test
print(ProductCreate(name="Laptop", price=999.99, sku="LAP-001").model_dump())
# ProductCreate(name='Laptop', price=999.99, sku='LAP-001', stock=0) + validation
```

## Mini Quiz

```yaml
- question: "What does `Field(default_factory=list)` do?"
  options: [
    "Shares one list across instances",
    "Creates a new list per instance",
    "Makes the field required",
    "Validates list length"
  ]
  answer: 1
  explanation: "default_factory calls list() for each instance, avoiding shared mutable defaults."
- question: "When should you use `@model_validator(mode='after')`?"
  options: [
    "To validate a single field",
    "To validate across multiple fields",
    "To serialize the model",
    "To skip validation"
  ]
  answer: 1
  explanation: "Model validators see the whole model, enabling cross-field rules."
- question: "What does `model_dump(exclude_unset=True)` return?"
  options: [
    "All fields",
    "Only fields explicitly provided",
    "Only required fields",
    "JSON string"
  ]
  answer: 1
  explanation: "exclude_unset returns only set fields — perfect for PATCH partial updates."
```
