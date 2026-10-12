---
slug: fastapi-intro
track: web-development
trackTitle: "Web Development (FastAPI)"
trackOrder: 4
chapter: fastapi-basics
chapterTitle: "Chapter 1 — FastAPI Basics"
chapterOrder: 1
title: "Building Your First FastAPI Application"
difficulty: intermediate
order: 1
estimatedMinutes: 20
tags: [python, fastapi, web, api]
---

## Learning Objective

Create a FastAPI application with routes, request validation, and automatic API documentation.

## Explanation

**FastAPI** is a modern, fast web framework for building APIs with Python 3.7+. Key features:
- **Automatic OpenAPI/Swagger docs** at `/docs` and `/redoc`
- **Request validation** via Pydantic models
- **Type hints** for editor support and runtime validation
- **Async support** for high concurrency
- **Dependency injection** for clean architecture

FastAPI is built on **Starlette** (ASGI) and **Pydantic**. It's used by Netflix, Uber, Microsoft, and more.

## Why It Matters

FastAPI combines the ease of Flask with the performance of Node.js/Go. Automatic validation and docs save huge development time. It's the go-to choice for modern Python APIs.

## Example

```python
# main.py
from fastapi import FastAPI

app = FastAPI(title="My API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}

@app.get("/hello/{name}")
async def hello(name: str):
    return {"greeting": f"Hello, {name}!"}

# Run: uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API docs!

## Code

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from enum import Enum

app = FastAPI(
    title="Task Manager API",
    description="A simple task management API",
    version="1.0.0",
)

# Pydantic models for validation
class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: TaskStatus = TaskStatus.TODO

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    
    class Config:
        from_attributes = True

# In-memory storage (replace with DB in production)
tasks_db: List[Task] = []
next_id = 1

@app.get("/tasks", response_model=List[Task])
async def list_tasks(
    status: Optional[TaskStatus] = Query(None, description="Filter by status"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    filtered = tasks_db
    if status:
        filtered = [t for t in filtered if t.status == status]
    return filtered[offset:offset + limit]

@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: TaskCreate):
    global next_id
    new_task = Task(id=next_id, **task.model_dump())
    tasks_db.append(new_task)
    next_id += 1
    return new_task

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskCreate):
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in task_update.model_dump().items():
        setattr(task, field, value)
    return task

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    global tasks_db
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_db = [t for t in tasks_db if t.id != task_id]

# Run with: uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Code Explanation

Line 1-3: Imports. `FastAPI` creates the app. `HTTPException` for errors. `Query` for query params.
Lines 7-16: Pydantic models define request/response shapes with validation (`min_length`, `max_length`, `Enum`).
Line 19: `Task` extends `TaskBase` adding `id`. `from_attributes=True` enables ORM mode.
Lines 27-35: GET with query parameters. `Query()` adds validation and docs.
Line 38: POST with request body validation. `status_code=201` for created.
Lines 44-52: Path parameter with 404 handling via `HTTPException`.
Lines 55-62: PUT for full update.
Lines 65-70: DELETE with 204 No Content.

## Common Mistakes

- Forgetting `async` on route handlers that do I/O
- Using mutable defaults in Pydantic models: `tags: list = []` — use `Field(default_factory=list)`
- Not raising `HTTPException` for errors — FastAPI won't return proper status codes
- Mixing `response_model` with manual `JSONResponse` — let FastAPI handle serialization

## Best Practices

- Define Pydantic models in separate `schemas.py` for reuse
- Use `response_model` for automatic serialization and docs
- Use `Query`, `Path`, `Body`, `Header`, `Cookie` for parameter validation
- Structure apps with routers: `app.include_router(tasks_router, prefix="/tasks")`
- Use dependency injection for DB sessions, auth, etc.

## Exercise

Add a `PATCH /tasks/{task_id}` endpoint that accepts partial updates (only provided fields). Use `TaskUpdate` model with all optional fields.

## Solution

```python
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[TaskStatus] = None

@app.patch("/tasks/{task_id}", response_model=Task)
async def patch_task(task_id: int, task_update: TaskUpdate):
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    return task
```

## Mini Quiz

```yaml
- question: "Where does FastAPI serve automatic API documentation?"
  options: ["/docs", "/swagger", "/api-docs", "/openapi"]
  answer: 0
  explanation: "FastAPI serves Swagger UI at /docs and ReDoc at /redoc automatically."
- question: "What does `Field(..., min_length=1)` mean?"
  options: [
    "Optional field with minimum length 1",
    "Required field with minimum length 1",
    "Field with default value 1",
    "Field that accepts 1 item"
  ]
  answer: 1
  explanation: "Ellipsis (...) means required. min_length=1 validates string length."
- question: "Which status code should POST return on successful creation?"
  options: ["200", "201", "202", "204"]
  answer: 1
  explanation: "201 Created is the correct status for successful resource creation."
```