---
slug: orchestration-api
track: final-project
trackTitle: "Final Project: Data Analysis Pipeline"
trackOrder: 6
chapter: data-pipeline
chapterTitle: "Chapter 1 — Building a Data Analysis Pipeline"
chapterOrder: 1
title: "Orchestration and API Exposure"
difficulty: advanced
order: 4
estimatedMinutes: 25
tags: [python, pipeline, orchestration, fastapi, api]
---

## Learning Objective

Orchestrate pipeline steps from YAML config and expose results via FastAPI.

## Explanation

**Orchestration** runs steps in order, passes data between them, handles errors, and logs progress. A minimal orchestrator:

1. Loads `pipeline.yaml` (step list).
2. Dispatches each step type (`ingest`, `clean`, `transform`, `analyze`, `export`) to a function.
3. Shares a `context` dict (DataFrames, metrics, paths).
4. Stops or continues on failure per config.

Then **expose** results: a FastAPI app serves the latest parquet/CSV, metrics JSON, and triggers re-runs. This turns a batch script into a service teammates can query.

## Why It Matters

Manual `python step1.py && python step2.py` breaks with ordering bugs and no observability. Orchestration gives one command (`python -m pipeline.orchestrator configs/pipeline.yaml`), repeatable runs, and clear logs. An API layer makes results consumable without re-running notebooks.

## Example

```python
# orchestrator.py (simplified)
STEPS = {
    "ingest": lambda ctx, cfg: ctx.update(data=load_csv(cfg["path"])),
    "clean": lambda ctx, cfg: ctx.update(data=clean(ctx["data"])),
}

def run(pipeline_cfg: dict):
    ctx = {}
    for step in pipeline_cfg["steps"]:
        print(f"Running {step['name']}...")
        STEPS[step["type"]](ctx, step.get("config", {}))
    return ctx
```

## Code

```python
# src/pipeline/orchestrator.py
from __future__ import annotations
import time
import traceback
from pathlib import Path
import yaml
import pandas as pd
from loguru import logger

# Import your step functions
# from pipeline.clean import run_cleaning
# from pipeline.ingest import load_data

def load_pipeline_config(path: str | Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)

def execute_step(step: dict, ctx: dict) -> dict:
    name, stype, cfg = step["name"], step["type"], step.get("config", {})
    logger.info(f"Step '{name}' ({stype}) started")
    t0 = time.perf_counter()
    try:
        if stype == "ingest":
            ctx["data"] = pd.read_csv(cfg["path"])
        elif stype == "clean":
            from pipeline.clean import run_cleaning  # lazy import
            ctx["data"] = run_cleaning(ctx["data"], cfg)
        elif stype == "export":
            out = Path(cfg["path"])
            out.parent.mkdir(parents=True, exist_ok=True)
            if cfg.get("format", "parquet") == "parquet":
                ctx["data"].to_parquet(out, index=False)
            else:
                ctx["data"].to_csv(out, index=False)
            ctx["export_path"] = str(out)
        else:
            raise ValueError(f"Unknown step type: {stype}")
        logger.info(f"Step '{name}' done in {time.perf_counter() - t0:.2f}s")
        return {"status": "ok", "name": name}
    except Exception as e:
        logger.error(f"Step '{name}' failed: {e}\n{traceback.format_exc()}")
        return {"status": "failed", "name": name, "error": str(e)}

def run_pipeline(config_path: str | Path, stop_on_error: bool = True) -> dict:
    cfg = load_pipeline_config(config_path)
    ctx: dict = {}
    results = []
    for step in cfg.get("steps", []):
        res = execute_step(step, ctx)
        results.append(res)
        if res["status"] == "failed" and stop_on_error:
            break
    return {"results": results, "rows": len(ctx.get("data", [])), "export": ctx.get("export_path")}

if __name__ == "__main__":
    import sys
    summary = run_pipeline(sys.argv[1] if len(sys.argv) > 1 else "configs/pipeline.yaml")
    print(summary)
```

```python
# src/pipeline/api.py — expose results via FastAPI
from fastapi import FastAPI, HTTPException
from pathlib import Path
import pandas as pd

app = FastAPI(title="Data Pipeline API", version="1.0.0")
OUTPUT = Path("output/results.parquet")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/results")
async def get_results(limit: int = 10, offset: int = 0):
    if not OUTPUT.exists():
        raise HTTPException(404, "No results yet. Run the pipeline first.")
    df = pd.read_parquet(OUTPUT)
    total = len(df)
    page = df.iloc[offset:offset + limit].to_dict(orient="records")
    return {"total": total, "limit": limit, "offset": offset, "data": page}

@app.post("/run")
async def trigger_run(config: str = "configs/pipeline.yaml"):
    from pipeline.orchestrator import run_pipeline
    summary = run_pipeline(config)
    return summary

# Run: uvicorn pipeline.api:app --reload
```

## Code Explanation

`load_pipeline_config` parses YAML into a dict of steps.
`execute_step` dispatches on `type`, times execution, logs start/done/fail, and stores outputs in shared `ctx`.
`run_pipeline` loops steps, optionally stopping on first failure, returning a summary.
`api.py` serves `/health` (liveness), `/results` (paginated parquet read), `/POST /run` (trigger). Pagination via `iloc[offset:...]` avoids dumping huge frames.

## Common Mistakes

- Hardcoding step order in Python instead of YAML — config should drive order
- Sharing mutable global state between steps — pass explicit `ctx`
- `/run` triggering long pipelines synchronously — use `BackgroundTasks` or a job queue (Celery/ARQ) in production
- Reading full parquet per request without pagination or caching — slow under load
- No idempotency — re-runs duplicate outputs; write to versioned paths or overwrite atomically

## Best Practices

- One CLI entry: `python -m pipeline.orchestrator <config.yaml>`
- Log step name, duration, row counts; emit metrics JSON per run
- Version outputs: `output/2026-09-20/results.parquet`
- Use FastAPI `BackgroundTasks` for `/run` to return immediately with a job id
- Add tests: orchestrator with tiny CSV + temp output dir; API with `TestClient`

## Exercise

Extend the orchestrator with a `validate` step type that asserts required columns exist and fails the run with a clear error if not. Add a test with a missing column.

## Solution

```python
def validate_columns(df: pd.DataFrame, required: list[str]) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

# In execute_step, add:
# elif stype == "validate":
#     validate_columns(ctx["data"], cfg["required_columns"])

# Test
import pandas as pd
try:
    validate_columns(pd.DataFrame({"a": [1]}), ["a", "b"])
except ValueError as e:
    print(e)  # Missing required columns: ['b']
```

## Mini Quiz

```yaml
- question: "What is the orchestrator's job?"
  options: [
    "Train models",
    "Run configured steps in order with shared context and logging",
    "Serve HTTP requests",
    "Clean data only"
  ]
  answer: 1
  explanation: "The orchestrator loads YAML, dispatches each step type, threads context through, and logs."
- question: "Why paginate `/results` with limit/offset?"
  options: [
    "Required by FastAPI",
    "Avoid loading huge results into one response",
    "Faster parquet writes",
    "Better validation"
  ]
  answer: 1
  explanation: "Slicing with iloc returns a page, keeping responses small and fast."
- question: "How should long pipeline runs be triggered from an API?"
  options: [
    "Block the request until done",
    "Background task / job queue returning a job id",
    "Restart the server",
    "Run in the browser"
  ]
  answer: 1
  explanation: "Long jobs should run in background (BackgroundTasks, Celery) so the API stays responsive."
```
