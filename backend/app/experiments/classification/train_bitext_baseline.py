
from pathlib import Path

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# --------------------------------------------------
# 1. Define project paths
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[4]

PROCESSED = ROOT / "data" / "processed"

TRAIN_PATH = PROCESSED / "bitext_train.csv"
VALIDATION_PATH = PROCESSED / "bitext_validation.csv"


# --------------------------------------------------
# 2. Load datasets
# --------------------------------------------------

train_df = pd.read_csv(TRAIN_PATH)
validation_df = pd.read_csv(VALIDATION_PATH)

print("Training dataset:", train_df.shape)
print("Validation dataset:", validation_df.shape)


# --------------------------------------------------
# 3. Separate input (X) and target (y)
# --------------------------------------------------

X_train = train_df["instruction"]
y_train = train_df["intent"]

X_validation = validation_df["instruction"]
y_validation = validation_df["intent"]


# --------------------------------------------------
# 4. Convert text into numerical features using TF-IDF
# --------------------------------------------------

tfidf = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    max_features=20000,
    stop_words="english"
)

X_train_tfidf = tfidf.fit_transform(X_train)

X_validation_tfidf = tfidf.transform(X_validation)

print("\nTF-IDF feature shapes:")
print("Training:", X_train_tfidf.shape)
print("Validation:", X_validation_tfidf.shape)


# --------------------------------------------------
# 5. Train Logistic Regression
# --------------------------------------------------

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

model.fit(X_train_tfidf, y_train)

print("\nModel training completed!")


# --------------------------------------------------
# 6. Make predictions
# --------------------------------------------------

y_pred = model.predict(X_validation_tfidf)


# --------------------------------------------------
# 6.1 Error analysis
# --------------------------------------------------

errors = validation_df[
    ["instruction", "category", "intent"]
].copy()

errors["predicted_intent"] = y_pred

# Keep only incorrectly classified messages
errors = errors[
    errors["intent"] != errors["predicted_intent"]
].copy()

# Save errors for investigation
error_path = PROCESSED / "bitext_baseline_errors.csv"

errors.to_csv(error_path, index=False)

print("\nERROR ANALYSIS")
print("-" * 45)

print("Total validation errors:", len(errors))
print("Error percentage:", round(len(errors) / len(validation_df) * 100, 2), "%")

print("\nFirst 10 misclassified examples:")
print(errors.head(10).to_string(index=False))

print("\nError report saved to:", error_path)



# --------------------------------------------------
# 7. Evaluate model performance
# --------------------------------------------------

accuracy = accuracy_score(y_validation, y_pred)

print("\nAccuracy:", round(accuracy, 4))

print("\nClassification Report:")
print(
    classification_report(
        y_validation,
        y_pred,
        zero_division=0
    )
)

print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_validation,
        y_pred,
        labels=model.classes_
    )
)
