
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"

PROCESSED.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42


def normalize_text(series):
    """Normalize whitespace without changing the original wording."""
    return (
        series.astype("str")
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


def prepare_bitext():
    print("\nPreparing Bitext dataset...")

    df = pd.read_csv(
        RAW / "bitext_customer_support.csv",
        dtype="str"
    )

    original_count = len(df)

    # Normalize text columns
    df["instruction"] = normalize_text(df["instruction"])
    df["response"] = normalize_text(df["response"])

    # Remove exact duplicate classification examples
    classification_df = df.drop_duplicates(
        subset=["instruction", "category", "intent"]
    ).copy()

    removed = original_count - len(classification_df)

    # Stratified train/validation/test split
    train, temporary = train_test_split(
        classification_df,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=classification_df["intent"]
    )

    validation, test = train_test_split(
        temporary,
        test_size=0.50,
        random_state=RANDOM_STATE,
        stratify=temporary["intent"]
    )

    train.to_csv(
        PROCESSED / "bitext_train.csv", index=False
    )
    validation.to_csv(
        PROCESSED / "bitext_validation.csv", index=False
    )
    test.to_csv(
        PROCESSED / "bitext_test.csv", index=False
    )

    # Preserve unique customer-response knowledge separately
    knowledge = df[
        ["instruction", "category", "intent", "response"]
    ].drop_duplicates()

    knowledge.to_csv(
        PROCESSED / "bitext_knowledge.csv", index=False
    )

    print("Original records:", original_count)
    print("Records removed as duplicate examples:", removed)
    print("Classification records:", len(classification_df))
    print("Training records:", len(train))
    print("Validation records:", len(validation))
    print("Testing records:", len(test))
    print("Knowledge records:", len(knowledge))
    print("Unique intents:", classification_df["intent"].nunique())



def prepare_banking77():
    print("\nPreparing Banking77 dataset...")

    # Load original datasets
    train = pd.read_csv(
        RAW / "banking77_train.csv",
        dtype="str"
    )

    test = pd.read_csv(
        RAW / "banking77_test.csv",
        dtype="str"
    )

    original_train_count = len(train)
    original_test_count = len(test)

    # Normalize text
    train["text"] = normalize_text(train["text"])
    test["text"] = normalize_text(test["text"])

    # Remove exact duplicate message-label pairs from training only
    train = train.drop_duplicates(
        subset=["text", "category"]
    ).copy()

    duplicates_removed = original_train_count - len(train)

    # Remove normalized text overlap with official test set
    test_messages = set(test["text"])

    before = len(train)

    train = train[
        ~train["text"].isin(test_messages)
    ].copy()

    removed_overlap = before - len(train)

    # Split remaining training data into training and validation
    # Keep the official test set separate and unchanged in record count
    train_data, validation = train_test_split(
        train,
        test_size=0.15,
        random_state=RANDOM_STATE,
        stratify=train["category"]
    )

    # Save processed datasets
    train_data.to_csv(
        PROCESSED / "banking77_train.csv",
        index=False
    )

    validation.to_csv(
        PROCESSED / "banking77_validation.csv",
        index=False
    )

    test.to_csv(
        PROCESSED / "banking77_test.csv",
        index=False
    )

    # Display processing summary
    print("\nBANKING77 PROCESSING SUMMARY")
    print("-" * 45)

    print("Original training records:", original_train_count)
    print("Duplicate training records removed:", duplicates_removed)
    print("Train-test overlapping messages removed:", removed_overlap)

    print("Final training records:", len(train_data))
    print("Validation records:", len(validation))
    print("Official testing records:", len(test))

    print("Training categories:", train_data["category"].nunique())
    print("Validation categories:", validation["category"].nunique())
    print("Testing categories:", test["category"].nunique())

    print("\nBanking77 preprocessing completed.")


if __name__ == "__main__":
    prepare_bitext()
    prepare_banking77()

    print("\nDATASET PREPROCESSING COMPLETED")
