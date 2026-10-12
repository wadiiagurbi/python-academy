# Python Academy — From Scratch to Advanced

A complete, beginner-friendly learning platform that takes a learner with **zero Python knowledge** through Python fundamentals, intermediate concepts, advanced topics, web development with FastAPI, data science & ML, and finishes with a real Data Analysis Pipeline project built incrementally across the final chapter.

The platform itself is a working full-stack application: a FastAPI JSON API backend and a Vue 3 + Vuetify SPA frontend, with real authentication, progress tracking, quizzes, search, and a visual Data Pipeline Builder — all serving as a live example of the concepts the course teaches.

## Project Overview

- **29 lessons included (165 planned)** across 6 tracks (Python Fundamentals, Intermediate Python, Advanced Python, Web Development, Data Science & ML, Final Project), each following a fixed structure: Learning Objective, Explanation, Why It Matters, Example, Code, Code Explanation, Common Mistakes, Best Practices, Exercise, Solution, Mini Quiz.
- Lesson content is **Markdown + YAML frontmatter**, stored as files under `backend/courses/` — never hardcoded into the frontend, never duplicated into the database.
- A FastAPI backend exposes that content (and real user accounts, progress, quizzes, search, and the Data Pipeline Builder) as a JSON API.
- A Vue 3 + Vuetify SPA consumes that API: course navigation, lesson pages with syntax highlighting and copy-to-clipboard, interactive quizzes, dark mode, search, a dashboard, and a visual Pipeline Builder with Chart.js visualizations.
- **Final Project**: A complete Data Analysis Pipeline that learners build step-by-step — ingest → clean → transform → analyze → visualize → export — with a working visual builder and execution engine.

## Architecture

```
python-academy/
├── backend/                     # FastAPI API (Python 3.11+)
│   ├── app/
│   │   ├── api/                 # API routes (thin controllers)
│   │   ├── core/                # Config, security, database, exceptions
│   │   ├── models/              # SQLAlchemy models (User, Progress, Quiz, Pipeline)
│   │   ├── schemas/             # Pydantic DTOs (request/response)
│   │   ├── services/            # Business logic (ContentLoader, Auth, Progress, Quiz, Pipeline)
│   │   ├── repositories/        # Data access layer
│   │   └── exceptions/          # Custom exceptions
│   ├── courses/                 # Lesson content — Markdown + YAML frontmatter
│   │   ├── python-fundamentals/
│   │   ├── intermediate-python/
│   │   ├── advanced-python/
│   │   ├── web-development/
│   │   ├── data-science/
│   │   └── final-project/
│   ├── migrations/              # Alembic migrations
│   ├── tests/                   # pytest unit + integration tests
│   ├── pyproject.toml
│   └── .env
├── frontend/                    # Vue 3 + Vite + Vuetify SPA
│   ├── src/
│   │   ├── api/                 # Axios client (JWT header injection)
│   │   ├── stores/              # Pinia: auth, courses, theme, pipeline
│   │   ├── router/              # Vue Router (auth guards)
│   │   ├── components/          # AppSidebar, CodeBlock, QuizWidget, MarkdownContent, PipelineBuilder, PipelineResults, ChartWidget
│   │   ├── views/               # DashboardView, LessonView, PipelineBuilderView, SearchView, etc.
│   │   └── utils/               # Markdown rendering (markdown-it + highlight.js)
│   ├── package.json
│   └── vite.config.js
└── README.md
```

### Architecture Decisions

- **Controller → DTO → Service → Repository → Model.** Every write endpoint follows this chain. Controllers never contain business logic or raw queries.
- **Markdown is the single source of truth for lesson content.** `ContentLoader` scans `backend/courses/**/*.md` at request time (cached per process), parses YAML frontmatter and Markdown sections, and returns structured DTOs. Adding a lesson is just adding a file — no code change, no migration, no frontend change.
- **The database stores application data, not course content**: users, progress (`LessonCompletion`), quiz attempts (`QuizAttempt`), and Data Pipeline projects (`DataPipeline`). Lesson text is never duplicated into a table.
- **Stateless JWT auth**, not sessions — the frontend is a separate SPA origin in development, and a stateless API scales horizontally without shared session storage.
- **One exception handler, not per-controller try/catch.** All `/api/*` errors return consistent JSON with `{"error": {"message": ..., "details": ...}}` shape.
- **Quiz answers server-side only** — never sent to the client before grading.
- **Final Project = Real Feature** — The Data Pipeline Builder is a working part of the platform, not hypothetical.

## Requirements

- Python 3.11+ with `sqlite3` (built-in)
- Node.js 20+ / npm
- (Optional) PostgreSQL 14+ for production

## Installation

### Backend

```bash
cd backend
pip install -e ".[dev]"
# Or with uv (recommended):
uv pip install -e ".[dev]"
```

Environment variables live in `backend/.env`. The defaults work out of the box for local development:

```dotenv
# Database — SQLite by default, zero setup required
DATABASE_URL="sqlite+aiosqlite:///./data/python_academy.db"
# For PostgreSQL:
# DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/python_academy"

# JWT signing key — CHANGE IN PRODUCTION!
SECRET_KEY="your-super-secret-key-change-in-production-min-32-chars"

# CORS — allows the local Vite dev server to call the API
CORS_ALLOW_ORIGINS='["http://localhost:5173", "http://127.0.0.1:5173"]'
```

Run database migrations:

```bash
alembic upgrade head
```

### Frontend

```bash
cd frontend
npm install
```

`frontend/.env` points the frontend at the backend:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## Running the App

```bash
# Terminal 1 — backend
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2 — frontend
cd frontend
npm run dev
```

Open the URL Vite prints (typically `http://localhost:5173/`). Register an account to unlock progress tracking, quizzes, and the Data Pipeline Builder.

## Running Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run build
```

## Course Content: Format and How to Add a Lesson

Every lesson is one Markdown file under `backend/courses/<track>/<chapter>/NN-slug.md`:

```markdown
---
slug: python-variables
track: python-fundamentals
trackTitle: "Python Fundamentals"
trackOrder: 1
chapter: variables-and-types
chapterTitle: "Chapter 2 — Variables & Data Types"
chapterOrder: 2
title: "Variables and Data Types"
difficulty: beginner
order: 3
estimatedMinutes: 12
tags: [python, basics, variables]
---

## Learning Objective

Understand how to create and use variables in Python, and recognize the basic data types.

## Explanation

Variables in Python are references to objects. When you write `x = 42`, Python creates an integer object with value 42 and makes `x` refer to it...

## Why It Matters

Variables are the foundation of every program. Understanding how Python handles them prevents common bugs...

## Example

```python
name = "Alice"
age = 30
height = 5.75
is_student = True
```

## Code

```python
name = "Alice"
age = 30
print(f"{name} is {age} years old")
```

## Code Explanation

The code demonstrates variable assignment and f-string formatting...

## Common Mistakes

- Using a variable before assignment raises `NameError`
- Variable names cannot start with a number

## Best Practices

- Use descriptive names (`user_count` not `uc`)
- Use `snake_case` for variables and functions

## Exercise

Create variables for your name, age, and favorite color, then print them.

## Solution

```python
my_name = "Bob"
my_age = 25
favorite_color = "blue"
print(f"{my_name}, {my_age}, {favorite_color}")
```

## Mini Quiz

```yaml
- question: "What is the output of `type(42)`?"
  options: ["<class 'int'>", "<class 'float'>", "<class 'str'>", "int"]
  answer: 0
  explanation: "In Python, `type(42)` returns the int class."
```
```

To add a lesson: drop a new `.md` file following this format anywhere under `backend/courses/`. `ContentLoader` discovers it automatically on the next request — no code change, no registration step. All 11 sections are required, or the file is treated as malformed (logged and skipped, never crashes the API).

Global lesson ordering (used for Previous/Next navigation) is `[trackOrder, chapterOrder, order]` — keep those numbers consistent within a chapter/track when adding lessons.

## Tracks and Chapters

| Track | Order | Chapters | Lessons |
|-------|-------|----------|---------|
| Python Fundamentals | 1 | 4 | 11 |
| Intermediate Python | 2 | 2 | 4 |
| Advanced Python | 3 | 1 | 2 |
| Web Development (FastAPI) | 4 | 2 | 4 |
| Data Science & ML | 5 | 2 | 4 |
| Final Project: Data Pipeline | 6 | 1 | 4 |

> **Note:** 29 lessons across 12 chapters are currently included under `backend/courses/`; the full curriculum plan targets ~165 lessons.

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/health` | public | Liveness check |
| GET | `/api/courses` | public | Full course tree |
| GET | `/api/courses/lessons/{slug}` | public | One lesson's full content |
| GET | `/api/courses/search?q=` | public | Search lessons |
| POST | `/api/auth/register` | public | Create account |
| POST | `/api/auth/login` | public | Exchange credentials for JWT |
| POST | `/api/auth/refresh` | public | Exchange refresh token for a new token pair |
| GET | `/api/auth/me` | JWT | Current user |
| GET | `/api/progress` | JWT | Completion %, quiz stats, last lesson |
| POST/DELETE | `/api/progress/lessons/{slug}/complete` | JWT | Mark lesson complete/incomplete |
| POST | `/api/quizzes/{slug}/attempt` | JWT | Submit and grade quiz |
| GET/POST | `/api/pipelines` | JWT | List/create pipelines |
| GET/PUT/DELETE | `/api/pipelines/{id}` | JWT | Read/update/delete pipeline |
| POST | `/api/pipelines/{id}/execute` | JWT | Execute pipeline |

## Final Project: Data Analysis Pipeline

The final course chapter (`backend/courses/final-project/`, 10 lessons) teaches the learner to build a Data Analysis Pipeline — and that Pipeline Builder is **not hypothetical**: it's the real, working feature in this app. The lessons quote and explain the actual source files, and `/pipelines` in the frontend is a fully working visual builder with drag-and-drop steps, configuration, execution, and Chart.js visualizations.

### Pipeline Steps Taught Across 10 Lessons

| Lesson | Topic | Real Code in Platform |
|--------|-------|----------------------|
| 01 | Project Setup & Requirements | `pyproject.toml`, config, logging |
| 02 | Data Ingestion Abstraction | `Ingestor` protocol + CSV/JSON/API implementations |
| 03 | Data Validation with Pydantic | Schema validation, error reporting |
| 04 | Cleaning & Transformation Pipeline | Composable `Transformer` classes |
| 05 | Exploratory Data Analysis | Pandas profiling, correlation matrix |
| 06 | Feature Engineering | Date parsing, encoding, scaling |
| 07 | Model Training & Evaluation | Scikit-learn pipeline, cross-validation |
| 08 | Pipeline Orchestration | DAG execution, caching, retries |
| 09 | API Deployment with FastAPI | `/predict` endpoint, model serialization |
| 10 | Monitoring & Production Readiness | Logging, metrics, health checks |

## Tech Stack

### Backend
- **FastAPI** 0.110+ with async/await
- **SQLAlchemy 2.0** (async) + **Alembic** for migrations
- **Pydantic v2** for validation/serialization
- **python-jose** + **passlib[bcrypt]** for JWT auth
- **SQLite** (dev) / **PostgreSQL** (prod)
- **pytest** + **httpx** for testing

### Frontend
- **Vue 3** + **Vite** 5
- **Vuetify 3** (Material Design 3)
- **Pinia** for state management
- **Vue Router 4** with auth guards
- **Axios** with interceptors
- **markdown-it** + **highlight.js** for lesson rendering
- **Chart.js** + **vue-chartjs** for pipeline visualizations

## License

MIT