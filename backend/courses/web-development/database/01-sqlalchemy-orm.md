---
slug: sqlalchemy-orm
track: web-development
trackTitle: "Web Development (FastAPI)"
trackOrder: 4
chapter: database
chapterTitle: "Chapter 4 — Database with SQLAlchemy"
chapterOrder: 4
title: "SQLAlchemy ORM and Async Database Access"
difficulty: intermediate
order: 1
estimatedMinutes: 25
tags: [python, sqlalchemy, orm, database, async]
---

## Learning Objective

Use SQLAlchemy 2.0 async ORM for database operations in FastAPI.

## Explanation

**SQLAlchemy** is Python's most popular ORM. Version 2.0 introduces:
- **Unified async API** with `async_session` and `AsyncSession`
- **Mapped classes** with type annotations (no more `__tablename__` strings)
- **Select/Insert/Update/Delete** with modern `select()` construct

Key concepts:
- **Engine** — connection pool factory
- **Session** — unit of work, tracks changes
- **Model** — Python class mapped to table
- **Relationship** — foreign keys with object navigation

## Why It Matters

Raw SQL is error-prone and hard to maintain. ORM gives you type-safe queries, migration management, and database-agnostic code. Async support enables high-concurrency FastAPI apps.

## Example

```python
from sqlalchemy import Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    posts: Mapped[list["Post"]] = relationship(back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="posts")

# Engine & Session
engine = create_async_engine("sqlite+aiosqlite:///blog.db", echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Create tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

## Code

```python
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

async def create_user(session: AsyncSession, email: str, name: str) -> User:
    user = User(email=email, name=name)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_user(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_user_with_posts(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(
        select(User)
        .options(selectinload(User.posts))  # Eager load
        .where(User.id == user_id)
    )
    return result.scalar_one_or_none()

async def list_users(session: AsyncSession, limit: int = 10, offset: int = 0) -> list[User]:
    result = await session.execute(
        select(User).limit(limit).offset(offset).order_by(User.id)
    )
    return list(result.scalars().all())

async def update_user(session: AsyncSession, user_id: int, **kwargs) -> User | None:
    user = await get_user(session, user_id)
    if not user:
        return None
    for key, value in kwargs.items():
        setattr(user, key, value)
    await session.commit()
    await session.refresh(user)
    return user

async def delete_user(session: AsyncSession, user_id: int) -> bool:
    user = await get_user(session, user_id)
    if not user:
        return False
    await session.delete(user)
    await session.commit()
    return True

# Complex queries
async def get_user_post_counts(session: AsyncSession) -> list[tuple[User, int]]:
    result = await session.execute(
        select(User, func.count(Post.id).label("post_count"))
        .outerjoin(Post, User.id == Post.author_id)
        .group_by(User.id)
        .order_by(func.count(Post.id).desc())
    )
    return list(result.all())

# FastAPI dependency
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

# Usage in FastAPI route
# @app.get("/users/{user_id}")
# async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
#     user = await get_user_with_posts(db, user_id)
#     if not user:
#         raise HTTPException(404, "User not found")
#     return user
```

## Code Explanation

`Mapped[type] = mapped_column(...)` — type-annotated ORM mapping (SQLAlchemy 2.0).
`relationship(back_populates=...)` — bidirectional relationship.
`async_sessionmaker(engine, expire_on_commit=False)` — prevents lazy-load issues after commit.
`selectinload()` — eager loading via JOIN, avoids N+1 queries.
`session.execute(select(...))` — modern select syntax, returns `Result`.
`scalar_one_or_none()` — returns single object or None, raises if multiple.

## Common Mistakes

- Forgetting `await session.commit()` — changes not persisted
- Using sync `Session` in async code — blocks event loop!
- Lazy loading after commit with `expire_on_commit=True` — use `expire_on_commit=False`
- N+1 queries — always use `selectinload()` or `joinedload()` for relationships
- Not closing sessions — use async context manager or dependency injection

## Best Practices

- Use `AsyncSession` dependency in FastAPI routes
- Define models in separate `models.py`
- Use Alembic for migrations: `alembic revision --autogenerate -m "message"`
- Index foreign keys and frequently queried columns
- Use `selectinload` for collections, `joinedload` for single objects

## Exercise

Create a `Comment` model with `content`, `created_at`, `post_id` (FK), and `author_id` (FK). Add relationships to `Post` and `User`. Write a query to get all comments for a post with author names.

## Solution

```python
from datetime import datetime
from sqlalchemy import DateTime, func

class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    post: Mapped["Post"] = relationship(back_populates="comments")
    author: Mapped["User"] = relationship()

# Add to Post
Post.comments: Mapped[list["Comment"]] = relationship(back_populates="post")

# Query
async def get_post_comments(session: AsyncSession, post_id: int):
    result = await session.execute(
        select(Comment)
        .options(selectinload(Comment.author))
        .where(Comment.post_id == post_id)
        .order_by(Comment.created_at)
    )
    return list(result.scalars().all())
```

## Mini Quiz

```yaml
- question: "What does `expire_on_commit=False` do?"
  options: [
    "Prevents committing",
    "Keeps objects usable after commit",
    "Disables auto-commit",
    "Speeds up commits"
  ]
  answer: 1
  explanation: "Without it, SQLAlchemy expires all attributes after commit, triggering lazy loads on next access."
- question: "How do you eagerly load a relationship?"
  options: [
    "session.load(User.posts)",
    "select(User).options(selectinload(User.posts))",
    "User.posts.load()",
    "session.eager_load('posts')"
  ]
  answer: 1
  explanation: "selectinload() generates a separate SELECT with IN clause, efficient for collections."
- question: "What is `scalar_one_or_none()`?"
  options: [
    "Returns first column of first row or None",
    "Returns single object or None, raises if multiple",
    "Returns all rows as scalars",
    "Returns None always"
  ]
  answer: 1
  explanation: "Returns exactly one result or None. Raises if zero or multiple rows found."
```