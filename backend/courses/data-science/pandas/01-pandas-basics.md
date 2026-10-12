---
slug: pandas-basics
track: data-science
trackTitle: "Data Science & ML"
trackOrder: 5
chapter: pandas
chapterTitle: "Chapter 1 — Pandas Fundamentals"
chapterOrder: 1
title: "DataFrames and Series"
difficulty: intermediate
order: 1
estimatedMinutes: 25
tags: [python, pandas, dataframe, data-analysis]
---

## Learning Objective

Create, manipulate, and analyze data using Pandas DataFrames and Series.

## Explanation

**Pandas** is the cornerstone of Python data analysis. Two core objects:
- **`Series`** — 1D labeled array (like a column)
- **`DataFrame`** — 2D labeled table (like a spreadsheet or SQL table)

Both have **indexes** (row labels) and **columns** (for DataFrames). Labels enable powerful alignment and join operations.

## Why It Matters

Real-world data is messy. Pandas handles missing data, type conversion, grouping, merging, time series, and I/O (CSV, Excel, SQL, Parquet, JSON). It's the foundation for all Python data science.

## Example

```python
import pandas as pd
import numpy as np

# Series
s = pd.Series([1, 3, 5, np.nan, 7], index=['a', 'b', 'c', 'd', 'e'])
print(s)
# a    1.0
# b    3.0
# c    5.0
# d    NaN
# e    7.0

# DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['NYC', 'LA', 'Chicago']
})
print(df)
#       name  age     city
# 0    Alice   25      NYC
# 1      Bob   30       LA
# 2  Charlie   35  Chicago
```

## Code

```python
import pandas as pd
import numpy as np

# Create DataFrame from various sources
data = {
    'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones'],
    'category': ['Electronics', 'Accessories', 'Accessories', 'Electronics', 'Accessories'],
    'price': [999.99, 29.99, 79.99, 299.50, 149.99],
    'stock': [15, 100, 50, 20, 75],
    'rating': [4.5, 4.2, 4.7, 4.3, 4.6]
}
df = pd.DataFrame(data)

# Inspect
print(df.info())           # Columns, types, non-null counts
print(df.describe())       # Statistics for numeric columns
print(df.head(3))          # First 3 rows
print(df.dtypes)           # Column types

# Selection
print(df['product'])                   # Series
print(df[['product', 'price']])        # DataFrame with 2 columns
print(df.loc[0])                       # Row by label
print(df.iloc[0])                      # Row by position
print(df.loc[0:2, 'product':'price'])  # Slice rows and columns

# Boolean indexing
expensive = df[df['price'] > 100]
electronics = df[df['category'] == 'Electronics']
high_rated = df[(df['rating'] > 4.4) & (df['stock'] > 10)]

# Adding/modifying columns
df['price_with_tax'] = df['price'] * 1.1
df['in_stock'] = df['stock'] > 0
df.loc[df['price'] > 200, 'tier'] = 'premium'
df['tier'] = df['tier'].fillna('standard')

# String operations
df['product_upper'] = df['product'].str.upper()
df['is_accessory'] = df['category'].str.contains('Accessory')

# Missing data
df.loc[1, 'rating'] = np.nan
print(df.isna().sum())      # Count missing per column
df_filled = df.fillna({'rating': df['rating'].mean()})
df_dropped = df.dropna(subset=['rating'])

# GroupBy aggregation
category_stats = df.groupby('category').agg(
    avg_price=('price', 'mean'),
    total_stock=('stock', 'sum'),
    count=('product', 'count')
).reset_index()
print(category_stats)

# Sorting
df_sorted = df.sort_values('price', ascending=False)

# Apply custom function
def price_category(price):
    if price < 50: return 'budget'
    elif price < 200: return 'mid'
    return 'premium'

df['price_tier'] = df['price'].apply(price_category)
```

## Code Explanation

`pd.DataFrame(dict)` — creates DataFrame from column dict.
`.info()`, `.describe()`, `.head()` — essential inspection.
`df['col']` returns Series, `df[['col1', 'col2']]` returns DataFrame.
`.loc[]` — label-based, `.iloc[]` — position-based indexing.
Boolean indexing: `df[condition]` filters rows.
`groupby().agg()` — powerful aggregation with named outputs.
`.apply()` — apply custom function element-wise.

## Common Mistakes

- `df['new'] = value` creates column, but `df.new = value` creates attribute (avoid!)
- Chained assignment warning: `df[df['a'] > 0]['b'] = 1` — use `df.loc[df['a'] > 0, 'b'] = 1`
- Forgetting `inplace=True` or reassignment: `df.dropna()` returns new DF, doesn't modify
- String methods need `.str` accessor: `df['col'].str.upper()` not `df['col'].upper()`

## Best Practices

- Use `.loc[]` and `.iloc[]` for explicit indexing
- Chain operations with method chaining: `df.query().groupby().agg()`
- Specify `dtype` in `read_csv()` for large files
- Use `category` dtype for low-cardinality strings (memory efficient)
- Profile with `df.memory_usage(deep=True)`

## Exercise

Load a CSV (create one with `df.to_csv('products.csv', index=False)`), then:
1. Filter products with price > 100
2. Group by category, compute mean price and total stock
3. Save results to new CSV

## Solution

```python
# Save sample data
df.to_csv('products.csv', index=False)

# Load and analyze
df = pd.read_csv('products.csv')
expensive = df[df['price'] > 100]
summary = expensive.groupby('category').agg(
    avg_price=('price', 'mean'),
    total_stock=('stock', 'sum')
).reset_index()
summary.to_csv('expensive_summary.csv', index=False)
print(summary)
```

## Mini Quiz

```yaml
- question: "What does `df.loc[0]` return?"
  options: ["First column", "First row as Series", "First row as DataFrame", "First cell"]
  answer: 1
  explanation: "df.loc[0] returns the row with index label 0 as a Series."
- question: "How do you select multiple columns?"
  options: ["df['col1', 'col2']", "df[['col1', 'col2']]", "df.col1, df.col2", "df.loc[:, 'col1':'col2']"]
  answer: 1
  explanation: "Double brackets: df[['col1', 'col2']] returns a DataFrame with those columns."
- question: "What is the `.str` accessor used for?"
  options: ["Accessing string columns", "String methods on Series", "Creating string columns", "Converting to string"]
  answer: 1
  explanation: ".str provides vectorized string methods like .upper(), .contains(), .split() on Series."
```