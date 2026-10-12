---
slug: sklearn-basics
track: data-science
trackTitle: "Data Science & ML"
trackOrder: 5
chapter: sklearn
chapterTitle: "Chapter 4 — Machine Learning with Scikit-learn"
chapterOrder: 4
title: "Supervised Learning: Classification and Regression"
difficulty: intermediate
order: 1
estimatedMinutes: 30
tags: [python, sklearn, machine-learning, classification, regression]
---

## Learning Objective

Build, train, and evaluate machine learning models using scikit-learn.

## Explanation

**scikit-learn** (sklearn) provides simple, consistent APIs for ML. Core concepts:
- **Estimator** — any object with `fit()` and `predict()`
- **Transformer** — has `fit()`, `transform()`, `fit_transform()`
- **Pipeline** — chains transformers + estimator
- **Model Selection** — cross-validation, grid search

Key steps: data preparation → train/test split → model selection → training → evaluation → tuning.

## Why It Matters

Sklearn is the foundation of Python ML. Its consistent API lets you swap models easily. Pipelines prevent data leakage. Cross-validation gives reliable performance estimates.

## Example

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

# Load data
data = load_iris()
X, y = data.data, data.target

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Pipeline: scale + model
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=200, random_state=42))
])

# Train
pipe.fit(X_train, y_train)

# Predict
y_pred = pipe.predict(X_test)

# Evaluate
print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(classification_report(y_test, y_pred, target_names=data.target_names))
```

## Code

```python
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import (
    train_test_split, cross_val_score, GridSearchCV, KFold
)
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score
)
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

# Regression example: California Housing
data = fetch_california_housing(as_frame=True)
df = data.frame
X = df.drop("MedHouseVal", axis=1)
y = df["MedHouseVal"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Preprocessing for numeric features
numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_features)
])

# Models to compare
models = {
    "LinearRegression": LinearRegression(),
    "Ridge": Ridge(alpha=1.0),
    "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42),
    "GradientBoosting": GradientBoostingRegressor(random_state=42),
}

for name, model in models.items():
    pipe = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model)
    ])
    
    # Cross-validation
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(pipe, X_train, y_train, cv=cv, 
                            scoring="neg_root_mean_squared_error")
    print(f"{name}: RMSE = {-scores.mean():.4f} (+/- {scores.std():.4f})")
    
    # Train on full train set
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    print(f"  Test RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")
    print(f"  Test R²: {r2_score(y_test, y_pred):.4f}")

# Hyperparameter tuning with GridSearchCV
param_grid = {
    "model__n_estimators": [50, 100, 200],
    "model__max_depth": [5, 10, None],
}
rf_pipe = Pipeline([
    ("preprocessor", preprocessor),
    ("model", RandomForestRegressor(random_state=42))
])

grid = GridSearchCV(rf_pipe, param_grid, cv=3, 
                   scoring="neg_root_mean_squared_error", n_jobs=-1)
grid.fit(X_train, y_train)
print(f"Best params: {grid.best_params_}")
print(f"Best CV RMSE: {-grid.best_score_:.4f}")

# Feature importance (for tree models)
best_rf = grid.best_estimator_
importances = best_rf.named_steps["model"].feature_importances_
feature_names = X.columns
for name, imp in sorted(zip(feature_names, importances), key=lambda x: -x[1])[:5]:
    print(f"  {name}: {imp:.4f}")

# Classification with preprocessing
from sklearn.datasets import load_breast_cancer

cancer = load_breast_cancer(as_frame=True)
X_c, y_c = cancer.data, cancer.target

Xc_train, Xc_test, yc_train, yc_test = train_test_split(
    X_c, y_c, test_size=0.2, random_state=42, stratify=y_c
)

clf_pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", SVC(kernel="rbf", probability=True, random_state=42))
])

clf_pipe.fit(Xc_train, yc_train)
yc_pred = clf_pipe.predict(Xc_test)
yc_proba = clf_pipe.predict_proba(Xc_test)[:, 1]

from sklearn.metrics import roc_auc_score, confusion_matrix
print(f"ROC-AUC: {roc_auc_score(yc_test, yc_proba):.4f}")
print(f"Confusion Matrix:\n{confusion_matrix(yc_test, yc_pred)}")
```

## Code Explanation

`Pipeline` — chains steps, ensures same preprocessing on train/test.
`ColumnTransformer` — applies different transformers to different columns.
`cross_val_score` — K-fold CV, returns array of scores.
`GridSearchCV` — exhaustive search over parameter grid with CV.
`feature_importances_` — tree-based feature importance.

## Common Mistakes

- Fitting scaler on full dataset before split — **data leakage!** Always fit on train only.
- Not using `Pipeline` — manual preprocessing easy to mess up.
- Using default hyperparameters — always tune!
- Ignoring class imbalance in classification — use `stratify` and `class_weight`.
- Not setting `random_state` — non-reproducible results.

## Best Practices

- Always use `Pipeline` + `ColumnTransformer` for preprocessing
- Use `cross_val_score` for reliable performance estimates
- Use `GridSearchCV` or `RandomizedSearchCV` for tuning
- Save models with `joblib.dump(model, "model.joblib")`
- Track experiments with MLflow or Weights & Biases

## Exercise

Build a complete ML pipeline for the `load_wine` dataset:
1. Load data, split train/test
2. Create pipeline with scaling + RandomForestClassifier
3. Tune `n_estimators` and `max_depth` with GridSearchCV
4. Report best CV score and test accuracy

## Solution

```python
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier

data = load_wine(as_frame=True)
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", RandomForestClassifier(random_state=42))
])

param_grid = {
    "clf__n_estimators": [50, 100, 200],
    "clf__max_depth": [3, 5, 7, None],
}

grid = GridSearchCV(pipe, param_grid, cv=5, scoring="accuracy", n_jobs=-1)
grid.fit(X_train, y_train)

print(f"Best: {grid.best_params_}")
print(f"CV Accuracy: {grid.best_score_:.4f}")
print(f"Test Accuracy: {grid.score(X_test, y_test):.4f}")
```

## Mini Quiz

```yaml
- question: "Why use Pipeline instead of manual preprocessing?"
  options: [
    "It's faster",
    "Prevents data leakage by fitting only on training data",
    "Required by sklearn",
    "Automatically does cross-validation"
  ]
  answer: 1
  explanation: "Pipeline ensures transformers are fit only on training folds during CV, not on test data."
- question: "What does `cross_val_score` return?"
  options: [
    "Single best score",
    "Array of scores for each fold",
    "Best hyperparameters",
    "Trained model"
  ]
  answer: 1
  explanation: "Returns array of scores, one per CV fold. Use .mean() for aggregate."
- question: "When should you use `stratify=y` in train_test_split?"
  options: [
    "Always",
    "For regression only",
    "For classification with imbalanced classes",
    "Never"
  ]
  answer: 2
  explanation: "stratify preserves class proportions in train/test splits, crucial for imbalanced data."
```