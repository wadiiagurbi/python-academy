---
slug: data-ingestion
track: final-project
trackTitle: "Final Project: Data Analysis Pipeline"
trackOrder: 6
chapter: data-pipeline
chapterTitle: "Chapter 1 — Building a Data Analysis Pipeline"
chapterOrder: 1
title: "Data Ingestion Abstraction"
difficulty: advanced
order: 2
estimatedMinutes: 25
tags: [python, pipeline, ingestion, abstraction, protocol]
---

## Learning Objective

Build a flexible data ingestion layer using the Strategy pattern and Protocol-based abstraction.

## Explanation

Data comes from many sources: CSV, JSON, APIs, databases, Parquet. A good pipeline decouples **what** data to load from **how** to load it. We use:
- **Protocol** (structural subtyping) for type-safe abstraction
- **Concrete implementations** for each source
- **Factory** to create the right ingestor

This makes the pipeline configurable via YAML — no code changes needed to switch sources.

## Why It Matters

Hardcoding data loading creates brittle pipelines. Abstraction lets you swap sources, add new formats, and test with mock data. This is the foundation of a production-grade pipeline.

## Example

```python
# Define the protocol
from typing import Protocol
import pandas as pd

class Ingestor(Protocol):
    def load(self) -> pd.DataFrame: ...

# CSV implementation
class CSVIngestor:
    def __init__(self, path: str, **kwargs):
        self.path = path
        self.kwargs = kwargs
    
    def load(self) -> pd.DataFrame:
        return pd.read_csv(self.path, **self.kwargs)

# JSON implementation
class JSONIngestor:
    def __init__(self, path: str, **kwargs):
        self.path = path
        self.kwargs = kwargs
    
    def load(self) -> pd.DataFrame:
        return pd.read_json(self.path, **self.kwargs)

# Usage
ingestor = CSVIngestor("data/train.csv")
df = ingestor.load()
```

## Code

```python
from typing import Protocol, Any
import pandas as pd
from abc import ABC, abstractmethod
import requests
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

class Ingestor(Protocol):
    """Protocol for data ingestors. Any class with load() -> DataFrame qualifies."""
    def load(self) -> pd.DataFrame: ...

# Base class with common functionality
class BaseIngestor(ABC):
    def __init__(self, config: dict[str, Any]):
        self.config = config
    
    @abstractmethod
    def load(self) -> pd.DataFrame:
        pass

class CSVIngestor(BaseIngestor):
    def load(self) -> pd.DataFrame:
        return pd.read_csv(
            self.config["path"],
            sep=self.config.get("sep", ","),
            encoding=self.config.get("encoding", "utf-8"),
            dtype=self.config.get("dtype"),
            parse_dates=self.config.get("parse_dates"),
            **self.config.get("pandas_kwargs", {})
        )

class JSONIngestor(BaseIngestor):
    def load(self) -> pd.DataFrame:
        return pd.read_json(
            self.config["path"],
            orient=self.config.get("orient", "records"),
            lines=self.config.get("lines", False),
            **self.config.get("pandas_kwargs", {})
        )

class ParquetIngestor(BaseIngestor):
    def load(self) -> pd.DataFrame:
        return pd.read_parquet(
            self.config["path"],
            columns=self.config.get("columns"),
            **self.config.get("pandas_kwargs", {})
        )

class APIIngestor(BaseIngestor):
    def load(self) -> pd.DataFrame:
        response = requests.get(
            self.config["url"],
            params=self.config.get("params"),
            headers=self.config.get("headers"),
            timeout=self.config.get("timeout", 30)
        )
        response.raise_for_status()
        data = response.json()
        
        # Handle different JSON structures
        if isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, dict):
            if "data" in data:
                return pd.DataFrame(data["data"])
            elif "results" in data:
                return pd.DataFrame(data["results"])
        return pd.DataFrame([data])

class SQLIngestor(BaseIngestor):
    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self._engine: Engine | None = None
    
    @property
    def engine(self) -> Engine:
        if self._engine is None:
            self._engine = create_engine(self.config["connection_string"])
        return self._engine
    
    def load(self) -> pd.DataFrame:
        query = self.config["query"]
        params = self.config.get("params")
        return pd.read_sql(query, self.engine, params=params)

# Factory for creating ingestors
INGESTOR_REGISTRY: dict[str, type[BaseIngestor]] = {
    "csv": CSVIngestor,
    "json": JSONIngestor,
    "parquet": ParquetIngestor,
    "api": APIIngestor,
    "sql": SQLIngestor,
}

def create_ingestor(source_type: str, config: dict[str, Any]) -> Ingestor:
    """Factory function to create ingestor from config."""
    if source_type not in INGESTOR_REGISTRY:
        raise ValueError(f"Unknown source type: {source_type}. "
                        f"Available: {list(INGESTOR_REGISTRY.keys())}")
    return INGESTOR_REGISTRY[source_type](config)

# Pipeline step integration
def run_ingest_step(step_config: dict[str, Any]) -> pd.DataFrame:
    """Execute an ingest step from pipeline config."""
    source_type = step_config["config"]["source"]
    ingestor = create_ingestor(source_type, step_config["config"])
    df = ingestor.load()
    
    # Basic validation
    if df.empty:
        raise ValueError(f"Ingestion returned empty DataFrame for {step_config['name']}")
    
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns from {source_type}")
    return df

# Example YAML config for ingestion step
"""
steps:
  - name: "load-customers"
    type: "ingest"
    config:
      source: "csv"
      path: "data/customers.csv"
      parse_dates: ["signup_date"]
      dtype:
        customer_id: "int64"
        email: "string"
"""
```

## Code Explanation

`Protocol` — structural typing. Any class with `load() -> pd.DataFrame` is an `Ingestor`. No inheritance required.
`BaseIngestor` — abstract base class with shared config handling.
Factory pattern — `create_ingestor()` maps string type to concrete class.
Config-driven — YAML specifies source type and parameters, code stays generic.
Extensible — add new ingestor by implementing `Ingestor` and registering it.

## Common Mistakes

- Using concrete classes directly instead of protocol — couples code to implementation
- Not validating config — fail fast with clear errors
- Loading huge files into memory — use chunking for large datasets
- Not handling authentication for APIs — use headers/env vars
- SQL injection in SQLIngestor — use parameterized queries

## Best Practices

- Define protocols for all pluggable components
- Use factory for object creation
- Keep config in YAML, not code
- Add new sources by implementing protocol + registering
- Use dependency injection in pipeline orchestrator

## Exercise

Add an `ExcelIngestor` that reads `.xlsx` files using `pd.read_excel()`. Support multiple sheets via `sheet_name` config. Register it in the factory.

## Solution

```python
class ExcelIngestor(BaseIngestor):
    def load(self) -> pd.DataFrame:
        return pd.read_excel(
            self.config["path"],
            sheet_name=self.config.get("sheet_name", 0),
            engine=self.config.get("engine", "openpyxl"),
            **self.config.get("pandas_kwargs", {})
        )

INGESTOR_REGISTRY["excel"] = ExcelIngestor
```

## Mini Quiz

```yaml
- question: "What is a Protocol in Python?"
  options: [
    "A base class",
    "Structural subtyping - defines required methods without inheritance",
    "A network protocol",
    "A decorator"
  ]
  answer: 1
  explanation: "Protocol (from typing) enables structural subtyping - any class with matching methods qualifies."
- question: "What pattern does `create_ingestor` implement?"
  options: ["Singleton", "Factory", "Observer", "Strategy"]
  answer: 1
  explanation: "Factory pattern - creates objects based on configuration without exposing instantiation logic."
- question: "Why use Protocol over abstract base class?"
  options: [
    "Faster",
    "No inheritance required - more flexible",
    "Required for type hints",
    "Better performance"
  ]
  answer: 1
  explanation: "Protocol allows any class with the right methods to qualify, no inheritance needed. Great for third-party classes."
```