---
slug: cleaning-transformation
track: final-project
trackTitle: "Final Project: Data Analysis Pipeline"
trackOrder: 6
chapter: data-pipeline
chapterTitle: "Chapter 1 — Building a Data Analysis Pipeline"
chapterOrder: 1
title: "Data Cleaning and Transformation"
difficulty: advanced
order: 3
estimatedMinutes: 25
tags: [python, pipeline, cleaning, transformation, pandas]
---

## Learning Objective

Build reusable cleaning and feature-engineering steps with pure, tested functions.

## Explanation

Raw data has missing values, duplicates, wrong dtypes, outliers, and inconsistent categories. A pipeline separates:

- **Cleaning** — make data correct: drop/threshold nulls, deduplicate, fix dtypes, normalize strings, handle outliers.
- **Transformation** — make data useful: encode categoricals, scale numerics, create features, aggregate.

Write each step as a **pure function** `(df, config) -> df` — no I/O inside. The orchestrator wires them together from YAML config, making steps testable and reorderable.

## Why It Matters

Notebooks hide cleaning in cells that run out of order. Production pipelines must be deterministic, logged, and tested. Pure-function steps let you unit-test cleaning without files or DBs and reuse them across projects.

## Example

```python
import pandas as pd

def drop_high_null_cols(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    keep = df.columns[df.isna().mean() < threshold]
    return df[keep].copy()

# df = pd.read_csv("customers.csv")
# clean = drop_high_null_cols(df, threshold=0.5)
```

## Code

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# --- Cleaning steps (pure functions) ---
def remove_duplicates(df: pd.DataFrame, subset: list[str] | None = None) -> pd.DataFrame:
    before = len(df)
    out = df.drop_duplicates(subset=subset, keep="first").copy()
    print(f"Dedup: {before} -> {len(out)} rows")
    return out

def fix_dtypes(df: pd.DataFrame, date_cols: list[str] | None = None) -> pd.DataFrame:
    out = df.copy()
    for col in (date_cols or []):
        out[col] = pd.to_datetime(out[col], errors="coerce")
    # Downcast numerics to save memory
    for col in out.select_dtypes(include=["int64"]).columns:
        out[col] = pd.to_numeric(out[col], downcast="integer")
    for col in out.select_dtypes(include=["float64"]).columns:
        out[col] = pd.to_numeric(out[col], downcast="float")
    return out

def handle_missing(
    df: pd.DataFrame,
    drop_threshold: float = 0.5,
    fill_numeric: str = "median",
    fill_categorical: str = "mode",
) -> pd.DataFrame:
    out = df.copy()
    # Drop columns that are mostly null
    out = out.loc[:, out.isna().mean() < drop_threshold]
    for col in out.columns:
        if out[col].isna().sum() == 0:
            continue
        if pd.api.types.is_numeric_dtype(out[col]):
            fill = out[col].median() if fill_numeric == "median" else out[col].mean()
            out[col] = out[col].fillna(fill)
        else:
            out[col] = out[col].fillna(out[col].mode().iloc[0] if not out[col].mode().empty else "unknown")
    return out

def normalize_strings(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in cols:
        out[col] = out[col].astype("string").str.strip().str.lower()
    return out

# --- Transformation steps ---
def encode_and_scale(
    df: pd.DataFrame, categorical: list[str], numeric: list[str]
) -> pd.DataFrame:
    out = df.copy()
    # One-hot encode
    if categorical:
        enc = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
        arr = enc.fit_transform(out[categorical])
        encoded = pd.DataFrame(
            arr, columns=enc.get_feature_names_out(categorical), index=out.index
        )
        out = pd.concat([out.drop(columns=categorical), encoded], axis=1)
    # Standardize numerics
    if numeric:
        scaler = StandardScaler()
        out[numeric] = scaler.fit_transform(out[numeric])
    return out

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if {"age", "income"} <= set(out.columns):
        out["income_per_age"] = out["income"] / out["age"].clip(lower=1)
    return out

# --- Compose from config ---
def run_cleaning(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    df = remove_duplicates(df, subset=cfg.get("dedupe_subset"))
    df = fix_dtypes(df, date_cols=cfg.get("date_cols", []))
    df = handle_missing(df, drop_threshold=cfg.get("drop_na_threshold", 0.5))
    df = normalize_strings(df, cols=cfg.get("normalize_cols", []))
    df = add_features(df)
    df = encode_and_scale(
        df,
        categorical=cfg.get("categorical", []),
        numeric=cfg.get("numeric", []),
    )
    return df

# Example
if __name__ == "__main__":
    raw = pd.DataFrame({
        "name": [" Alice ", "BOB", "Alice ", None],
        "age": [25, None, 25, 40],
        "income": [50000, 80000, 50000, 60000],
        "region": ["East", "West", "East", "East"],
        "signup": ["2024-01-01", "bad-date", "2024-01-01", "2024-02-01"],
    })
    cfg = {
        "dedupe_subset": ["name", "age", "income"],
        "date_cols": ["signup"],
        "normalize_cols": ["name", "region"],
        "categorical": ["region"],
        "numeric": ["age", "income"],
    }
    print(run_cleaning(raw, cfg))
```

## Code Explanation

`remove_duplicates` / `fix_dtypes` / `handle_missing` / `normalize_strings` each copy-then-transform — pure and testable.
`handle_missing` drops high-null columns first, then median/mode imputation per dtype.
`encode_and_scale` uses `OneHotEncoder(handle_unknown="ignore")` so unseen categories at inference do not crash; `StandardScaler` centers numerics.
`run_cleaning` reads a config dict (loaded from YAML) and applies steps in order — the orchestrator pattern.

## Common Mistakes

- In-place mutation without `.copy()` — callers see surprise side effects
- Fitting scaler/encoder on full data then splitting — leakage! Fit on train, transform test
- `fillna(mean)` on skewed data — median is safer for income-like columns
- One-hot encoding high-cardinality IDs (user_id) — explodes columns; use target/frequency encoding instead
- Dropping all null rows with `dropna()` — loses most data; prefer threshold + imputation

## Best Practices

- Keep steps pure: `(df, config) -> df`, I/O only at edges
- Log row counts and null rates before/after each step
- Validate with `pandera` or `great_expectations` schemas after cleaning
- Persist fitted encoders/scalers with `joblib` for inference parity
- Unit-test each step with tiny synthetic DataFrames

## Exercise

Write `clean_prices(df)` that: strips `$` and commas from a `price` string column, coerces to numeric, drops rows where price is null or <= 0, and adds `log_price = log1p(price)`.

## Solution

```python
import pandas as pd
import numpy as np

def clean_prices(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["price"] = (
        out["price"].astype("string")
        .str.replace(r"[$,]", "", regex=True)
        .str.strip()
    )
    out["price"] = pd.to_numeric(out["price"], errors="coerce")
    out = out[out["price"].notna() & (out["price"] > 0)].copy()
    out["log_price"] = np.log1p(out["price"])
    return out.reset_index(drop=True)

# Test
raw = pd.DataFrame({"price": ["$1,000", " $20.5 ", "bad", "$0", None]})
print(clean_prices(raw))
#    price  log_price
# 0  1000.0   6.908755
# 1    20.5   3.068053
```

## Mini Quiz

```yaml
- question: "Why should cleaning steps be pure functions?"
  options: [
    "Faster execution",
    "Testable without I/O and safely reorderable",
    "Required by pandas",
    "Smaller memory"
  ]
  answer: 1
  explanation: "Pure (df, config) -> df functions are deterministic, easy to unit-test, and composable."
- question: "Why fit scalers only on training data?"
  options: [
    "Test data is larger",
    "To prevent leakage of test statistics into training",
    "Scalers only work on train",
    "It is faster"
  ]
  answer: 1
  explanation: "Fitting on full data leaks test distribution. Fit on train, transform both."
- question: "What is a good first action for a column that is 80% null?"
  options: [
    "Fill with mean",
    "Drop the column (threshold rule)",
    "Forward-fill",
    "Duplicate it"
  ]
  answer: 1
  explanation: "Mostly-null columns carry little signal; dropping above a threshold (e.g., 0.5) is standard."
```
