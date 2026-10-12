---
slug: pipeline-setup
track: final-project
trackTitle: "Final Project: Data Analysis Pipeline"
trackOrder: 6
chapter: data-pipeline
chapterTitle: "Chapter 1 — Building a Data Analysis Pipeline"
chapterOrder: 1
title: "Project Setup and Requirements"
difficulty: advanced
order: 1
estimatedMinutes: 20
tags: [python, pipeline, project-setup, final-project]
---

## Learning Objective

Set up a professional Python project structure for a data analysis pipeline with modern tooling.

## Explanation

A production-ready data pipeline needs:
- **Project structure** following Python packaging standards
- **Dependency management** with `pyproject.toml`
- **Configuration** via environment variables and config files
- **Logging** for observability
- **Testing** with pytest
- **Type checking** with mypy
- **Code formatting** with ruff/black

We'll build a pipeline that can ingest data from multiple sources, clean it, transform it, analyze it, visualize results, and export — all configurable and extensible.

## Why It Matters

Jupyter notebooks are great for exploration, but production pipelines need structure, testing, and maintainability. This project teaches you to build data systems that survive in production.

## Example

```bash
# Project structure
data-pipeline/
├── pyproject.toml          # Project config, dependencies, tool settings
├── src/
│   └── pipeline/
│       ├── __init__.py
│       ├── config.py       # Settings management
│       ├── ingest/         # Data ingestion
│       ├── clean/          # Data cleaning
│       ├── transform/      # Feature engineering
│       ├── analyze/        # Analysis & ML
│       ├── visualize/      # Charts & dashboards
│       ├── export/         # Output formats
│       └── orchestrator.py # Pipeline runner
├── tests/                  # Unit & integration tests
├── data/                   # Sample data (gitignored)
├── configs/                # YAML pipeline configs
├── logs/                   # Runtime logs
├── .env.example            # Environment template
├── .gitignore
└── README.md
```

## Code

```toml
# pyproject.toml
[project]
name = "data-pipeline"
version = "0.1.0"
description = "Modular data analysis pipeline"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "pandas>=2.1",
    "numpy>=1.24",
    "pydantic>=2.5",
    "pydantic-settings>=2.1",
    "pyyaml>=6.0",
    "loguru>=0.7",
    "plotly>=5.17",
    "scikit-learn>=1.3",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4",
    "pytest-cov>=4.1",
    "ruff>=0.1",
    "mypy>=1.7",
    "black>=23.0",
    "jupyter>=1.0",
]
viz = ["streamlit>=1.28"]
api = ["fastapi>=0.104", "uvicorn>=0.24"]

[tool.ruff]
target-version = "py311"
line-length = 100
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "PL"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
disallow_untyped_defs = false

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

```python
# src/pipeline/config.py
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import yaml

class Settings(BaseSettings):
    """Application settings from environment variables."""
    app_name: str = "Data Pipeline"
    log_level: str = "INFO"
    data_dir: str = "./data"
    output_dir: str = "./output"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

def load_pipeline_config(path: str) -> dict:
    """Load pipeline configuration from YAML file."""
    with open(path) as f:
        return yaml.safe_load(f)
```

```python
# src/pipeline/__init__.py
"""Data Analysis Pipeline - Modular, configurable data processing."""

from pipeline.config import settings, load_pipeline_config

__version__ = "0.1.0"
__all__ = ["settings", "load_pipeline_config"]
```

```yaml
# configs/pipeline.yaml
pipeline:
  name: "customer-analysis"
  description: "Analyze customer behavior data"
  
steps:
  - name: "load-data"
    type: "ingest"
    config:
      source: "csv"
      path: "data/customers.csv"
  
  - name: "clean-data"
    type: "clean"
    config:
      drop_na_threshold: 0.5
      remove_duplicates: true
  
  - name: "feature-engineering"
    type: "transform"
    config:
      operations:
        - type: "encode_categorical"
          columns: ["region", "segment"]
        - type: "scale_numeric"
          columns: ["age", "income"]
  
  - name: "analyze"
    type: "analyze"
    config:
      method: "clustering"
      n_clusters: 4
  
  - name: "visualize"
    type: "visualize"
    config:
      charts:
        - type: "scatter"
          x: "age"
          y: "income"
          color: "cluster"
        - type: "bar"
          x: "segment"
          y: "count"
  
  - name: "export"
    type: "export"
    config:
      format: "parquet"
      path: "output/results.parquet"
```

## Code Explanation

`pyproject.toml` — modern Python packaging (PEP 621). Defines metadata, dependencies, and tool configs.
`config.py` — Pydantic Settings for type-safe configuration from env vars and `.env`.
`pipeline.yaml` — Declarative pipeline definition. Each step has a type and config. The orchestrator reads this and executes steps in order.

## Common Mistakes

- Putting code directly in scripts instead of packages — use `src/` layout
- Hardcoding paths — use config files and environment variables
- Committing `.env` or `data/` — add to `.gitignore`
- Mixing business logic with I/O — separate pure functions from side effects

## Best Practices

- Use `src/` layout for clean imports: `from pipeline.config import settings`
- Pin dependencies in `pyproject.toml` for reproducibility
- Use `pydantic-settings` for config validation
- Keep pipeline steps as pure functions when possible
- Write tests for each step in isolation

## Exercise

Create a new Python project with the structure above. Add a `Makefile` with targets: `install`, `test`, `lint`, `typecheck`, `run`.

## Solution

```makefile
# Makefile
.PHONY: install test lint typecheck run

install:
	pip install -e ".[dev]"

test:
	pytest -v

lint:
	ruff check src tests

typecheck:
	mypy src

run:
	python -m pipeline.orchestrator configs/pipeline.yaml

dev: install
	pre-commit install
```

## Mini Quiz

```yaml
- question: "What is the purpose of `pyproject.toml`?"
  options: [
    "Runtime configuration",
    "Project metadata and build configuration",
    "Environment variables",
    "Pipeline step definitions"
  ]
  answer: 1
  explanation: "pyproject.toml (PEP 621) defines project metadata, dependencies, and tool configurations."
- question: "Why use `src/` layout?"
  options: [
    "Required by Python",
    "Prevents accidental imports from source tree",
    "Faster execution",
    "Required for packaging"
  ]
  answer: 1
  explanation: "src/ layout ensures you test the installed package, not the source files directly."
- question: "What does `pydantic-settings` provide?"
  options: [
    "Database ORM",
    "Type-safe configuration from env vars",
    "Async HTTP client",
    "Data validation only"
  ]
  answer: 1
  explanation: "pydantic-settings extends Pydantic to load settings from environment variables and .env files with validation."
```