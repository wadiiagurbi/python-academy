---
slug: groupby-merge
track: data-science
trackTitle: "Data Science & ML"
trackOrder: 5
chapter: pandas
chapterTitle: "Chapter 1 — Pandas Fundamentals"
chapterOrder: 1
title: "GroupBy, Merge and Joins"
difficulty: intermediate
order: 2
estimatedMinutes: 25
tags: [python, pandas, groupby, merge]
---

## Learning Objective

Aggregate with groupby and combine DataFrames with merge, join, and concat.

## Explanation

**GroupBy** follows split-apply-combine: split rows into groups, apply an aggregation, combine results.

```python
df.groupby("category")["price"].mean()
```

**Combining**:
- `pd.merge(df1, df2, on="key", how="inner")` — SQL-style joins: `inner`, `left`, `right`, `outer`, `cross`.
- `df.join()` — join on index.
- `pd.concat([df1, df2])` — stack rows (`axis=0`) or columns (`axis=1`).
- `pivot_table()` — spreadsheet-style cross-tab.

## Why It Matters

Real analysis is never one table. You aggregate sales by region, join orders to customers, stack monthly files. GroupBy + merge are 80% of data-wrangling work.

## Example

```python
import pandas as pd

orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4],
    "customer": ["Alice", "Bob", "Alice", "Bob"],
    "amount": [50, 30, 20, 80],
})

# GroupBy
print(orders.groupby("customer")["amount"].sum())
# customer
# Alice    70
# Bob     110

# Merge
customers = pd.DataFrame({
    "customer": ["Alice", "Bob"],
    "city": ["NYC", "LA"],
})
print(pd.merge(orders, customers, on="customer", how="left"))
```

## Code

```python
import pandas as pd
import numpy as np

sales = pd.DataFrame({
    "region": ["East", "East", "West", "West", "East"],
    "rep": ["Alice", "Bob", "Alice", "Bob", "Alice"],
    "amount": [100, 200, 150, 300, 250],
    "units": [2, 5, 3, 7, 4],
})

# Named aggregations (clean output)
summary = (
    sales.groupby("region")
    .agg(
        total_sales=("amount", "sum"),
        avg_sale=("amount", "mean"),
        total_units=("units", "sum"),
        deals=("amount", "count"),
    )
    .reset_index()
)
print(summary)

# Multiple keys + transform (broadcast back to rows)
sales["region_avg"] = sales.groupby("region")["amount"].transform("mean")
print(sales)

# Merge flavors
customers = pd.DataFrame({"rep": ["Alice", "Bob", "Cara"], "team": ["A", "B", "A"]})
quotas = pd.DataFrame({"rep": ["Alice", "Bob"], "quota": [400, 400]})

print(pd.merge(sales, quotas, on="rep", how="left"))   # keep all sales
print(pd.merge(sales, quotas, on="rep", how="inner"))  # only matches

# Validate merge cardinality!
merged = pd.merge(sales, quotas, on="rep", how="left", validate="many_to_one")

# Concat monthly files
jan = pd.DataFrame({"month": ["jan"], "sales": [100]})
feb = pd.DataFrame({"month": ["feb"], "sales": [150]})
year = pd.concat([jan, feb], ignore_index=True)
print(year)

# Pivot table
pivot = sales.pivot_table(
    index="region", columns="rep", values="amount",
    aggfunc="sum", fill_value=0, margins=True, margins_name="Total"
)
print(pivot)
```

## Code Explanation

`.agg(total_sales=("amount", "sum"))` names output columns explicitly — preferred over dict syntax.
`.transform("mean")` returns same-length Series for per-row features.
`how="left"` keeps all left rows (NaN where no match); `inner` keeps only matches. `validate="many_to_one"` raises if assumptions break — catches duplicate keys early.
`pd.concat(ignore_index=True)` reindexes after stacking.
`pivot_table` with `margins=True` adds totals; `fill_value=0` replaces NaN.

## Common Mistakes

- Forgetting `reset_index()` after groupby — grouped keys stay in index, breaking merges
- Duplicate join keys causing row explosion — check with `validate=` and `.duplicated()`
- Mismatched dtypes on join keys (`int` vs `str`) — merge returns empty!
- `pd.concat` without `ignore_index=True` — duplicate index labels
- Chained assignment after groupby filter — use `.loc[]`

## Best Practices

- Always pass `validate=` to merge (`one_to_one`, `many_to_one`, etc.)
- Check dtypes of join keys before merging
- Use named aggregations for readable output
- Prefer `transform` for per-row group features vs merging aggregates back
- Use `category` dtype for group keys in large frames

## Exercise

Given `orders(customer, amount)` and `customers(customer, city)`: compute total amount per city via merge + groupby. Handle customers with no orders.

## Solution

```python
import pandas as pd

orders = pd.DataFrame({
    "customer": ["Alice", "Bob", "Alice"],
    "amount": [50, 30, 20],
})
customers = pd.DataFrame({
    "customer": ["Alice", "Bob", "Cara"],
    "city": ["NYC", "LA", "NYC"],
})

merged = pd.merge(customers, orders, on="customer", how="left")
merged["amount"] = merged["amount"].fillna(0)
per_city = merged.groupby("city", as_index=False).agg(total=("amount", "sum"))
print(per_city)
#   city  total
# 0   LA   30.0
# 1  NYC   70.0
```

## Mini Quiz

```yaml
- question: "What does `df.groupby('cat')['val'].transform('mean')` return?"
  options: [
    "One row per group",
    "Same-length Series with group means broadcast to rows",
    "A scalar",
    "A new DataFrame"
  ]
  answer: 1
  explanation: "transform broadcasts the aggregate back to each original row."
- question: "Which merge keeps all left rows?"
  options: ["inner", "left", "right", "cross"]
  answer: 1
  explanation: "how='left' keeps every left row, filling NaN where no right match exists."
- question: "What does `validate='many_to_one'` do?"
  options: [
    "Speeds up merge",
    "Raises if merge keys violate expected cardinality",
    "Sorts the result",
    "Drops duplicates"
  ]
  answer: 1
  explanation: "validate checks key uniqueness assumptions and raises on violation, catching explosions early."
```
