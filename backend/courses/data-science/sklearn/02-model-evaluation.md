---
slug: model-evaluation
track: data-science
trackTitle: "Data Science & ML"
trackOrder: 5
chapter: sklearn
chapterTitle: "Chapter 4 — Machine Learning with Scikit-learn"
chapterOrder: 4
title: "Model Evaluation and Validation"
difficulty: intermediate
order: 2
estimatedMinutes: 25
tags: [python, sklearn, evaluation, metrics, validation]
---

## Learning Objective

Evaluate classifiers and regressors with the right metrics and reliable cross-validation.

## Explanation

Accuracy alone misleads (95% accuracy on 95% negative data = useless model). Use:

**Classification**: `accuracy`, `precision` (of predicted positives, how many correct?), `recall` (of actual positives, how many found?), `f1` (harmonic mean), `confusion_matrix`, `roc_auc_score`, `classification_report`.

**Regression**: `mean_absolute_error` (MAE), `mean_squared_error` / RMSE, `r2_score`.

**Validation**: `cross_val_score` with `StratifiedKFold` (classification) or `KFold` (regression). `cross_validate` returns multiple metrics + fit times. Never tune on the test set — split train/validation/test or use nested CV.

## Why It Matters

Wrong metric = wrong model choice. Optimizing accuracy on imbalanced fraud data misses all fraud. Proper CV prevents overfitting optimism and leakage, giving honest estimates before deployment.

## Example

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression

X, y = load_iris(return_X_y=True)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(LogisticRegression(max_iter=200), X, y, cv=cv)
print(f"Accuracy: {scores.mean():.3f} +/- {scores.std():.3f}")
```

## Code

```python
import numpy as np
from sklearn.datasets import load_breast_cancer, fetch_california_housing
from sklearn.model_selection import (
    train_test_split, StratifiedKFold, KFold,
    cross_validate, learning_curve
)
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score,
    mean_absolute_error, mean_squared_error, r2_score,
    RocCurveDisplay
)

# --- Classification: breast cancer ---
X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

clf = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=1000, random_state=42)),
])
clf.fit(X_train, y_train)
pred = clf.predict(X_test)
proba = clf.predict_proba(X_test)[:, 1]

print(f"Accuracy:  {accuracy_score(y_test, pred):.3f}")
print(f"Precision: {precision_score(y_test, pred):.3f}")
print(f"Recall:    {recall_score(y_test, pred):.3f}")
print(f"F1:        {f1_score(y_test, pred):.3f}")
print(f"ROC-AUC:   {roc_auc_score(y_test, proba):.3f}")
print(confusion_matrix(y_test, pred))
print(classification_report(y_test, pred))

# Multi-metric CV (no leakage: scaler inside pipeline!)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_res = cross_validate(
    clf, X, y, cv=cv,
    scoring=["accuracy", "f1", "roc_auc"],
)
for m in ["test_accuracy", "test_f1", "test_roc_auc"]:
    print(f"{m}: {cv_res[m].mean():.3f} +/- {cv_res[m].std():.3f}")

# --- Regression: California housing (subset for speed) ---
Xr, yr = fetch_california_housing(return_X_y=True)
Xr, yr = Xr[:2000], yr[:2000]
Xtr, Xte, ytr, yte = train_test_split(Xr, yr, test_size=0.2, random_state=42)

reg = Pipeline([("scaler", StandardScaler()), ("reg", Ridge())])
reg.fit(Xtr, ytr)
p = reg.predict(Xte)
print(f"MAE: {mean_absolute_error(yte, p):.3f}")
print(f"RMSE: {np.sqrt(mean_squared_error(yte, p)):.3f}")
print(f"R2:   {r2_score(yte, p):.3f}")

kfold = KFold(n_splits=5, shuffle=True, random_state=42)
reg_scores = cross_validate(reg, Xr, yr, cv=kfold, scoring=["neg_root_mean_squared_error", "r2"])
print(f"CV RMSE: {-reg_scores['test_neg_root_mean_squared_error'].mean():.3f}")
```

## Code Explanation

`stratify=y` preserves class ratios in splits — critical for imbalanced data.
`cross_validate(scoring=[...])` computes several metrics per fold; `test_` prefix in results.
`roc_auc_score` needs probabilities (`predict_proba`), not hard predictions.
Pipelines inside CV ensure the scaler fits only on each train fold — fitting outside leaks test info.
Regression: MAE is robust to outliers, RMSE penalizes large errors, R² measures variance explained.

## Common Mistakes

- Reporting test accuracy on imbalanced data without precision/recall/F1
- Fitting scaler/vectorizer before `train_test_split` — leakage! Put it in a Pipeline
- Tuning hyperparameters on the test set — use CV on train, evaluate once on test
- Using plain `KFold` for classification — use `StratifiedKFold` to preserve ratios
- Comparing `predict()` to `predict_proba()` for ROC-AUC — AUC needs scores/probabilities

## Best Practices

- Always use Pipeline + CV; set `random_state` for reproducibility
- Report confusion matrix + precision/recall/F1 for classifiers, MAE/RMSE/R² for regressors
- Use `StratifiedKFold(n_splits=5)` for classification, `KFold` for regression
- Plot learning curves to diagnose bias vs variance
- Save the best estimator with `joblib` and log metrics per experiment

## Exercise

On `load_wine`, build a scaler + classifier pipeline, run 5-fold stratified CV reporting accuracy and macro-F1, then fit on train and report test confusion matrix.

## Solution

```python
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier

X, y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", RandomForestClassifier(n_estimators=100, random_state=42)),
])

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
res = cross_validate(pipe, X_train, y_train, cv=cv, scoring=["accuracy", "f1_macro"])
print(f"CV acc: {res['test_accuracy'].mean():.3f}, F1-macro: {res['test_f1_macro'].mean():.3f}")

pipe.fit(X_train, y_train)
print(confusion_matrix(y_test, pipe.predict(X_test)))
print(classification_report(y_test, pipe.predict(X_test)))
```

## Mini Quiz

```yaml
- question: "When is accuracy misleading?"
  options: [
    "Balanced classes",
    "Imbalanced classes",
    "Large datasets",
    "Cross-validation"
  ]
  answer: 1
  explanation: "On imbalanced data, predicting the majority class gives high accuracy but zero recall on minorities."
- question: "What is the difference between precision and recall?"
  options: [
    "They are the same",
    "Precision = correct among predicted positive; recall = found among actual positive",
    "Precision is for regression",
    "Recall ignores false negatives"
  ]
  answer: 1
  explanation: "Precision guards against false positives; recall guards against false negatives."
- question: "Why put the scaler inside the Pipeline during CV?"
  options: [
    "Faster",
    "Prevents leakage by fitting only on train folds",
    "Required syntax",
    "Higher accuracy"
  ]
  answer: 1
  explanation: "Fitting outside CV leaks test statistics into training. Pipeline fits per-fold correctly."
```
