
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
OUTPUT = ROOT / "data" / "processed"

OUTPUT.mkdir(parents=True, exist_ok=True)


def profile_text(df, column):
    lengths = df[column].fillna("").str.len()

    print(f"\nText analysis: {column}")
    print(f"Minimum length: {lengths.min()}")
    print(f"Maximum length: {lengths.max()}")
    print(f"Average length: {lengths.mean():.2f}")
    print(f"Median length: {lengths.median():.2f}")
    print(f"Empty records: {(lengths == 0).sum()}")


def profile_bitext():
    print("\n" + "=" * 60)
    print("BITEXT DATA QUALITY PROFILE")
    print("=" * 60)

    df = pd.read_csv(
        RAW / "bitext_customer_support.csv",
        dtype="str"
    )

    print("\nCategories:")
    print(df["category"].value_counts().sort_index())

    print("\nIntents:")
    print(df["intent"].value_counts().sort_index())

    profile_text(df, "instruction")
    profile_text(df, "response")

    print("\nRepeated instructions:")
    print(df["instruction"].duplicated().sum())

    print("\nRepeated responses:")
    print(df["response"].duplicated().sum())

    print("\nUnique flags:", df["flags"].nunique())


def profile_banking77():
    print("\n" + "=" * 60)
    print("BANKING77 DATA QUALITY PROFILE")
    print("=" * 60)

    train = pd.read_csv(
        RAW / "banking77_train.csv",
        dtype="str"
    )

    test = pd.read_csv(
        RAW / "banking77_test.csv",
        dtype="str"
    )

    print("\nTraining category distribution:")
    print(train["category"].value_counts().sort_index())

    print("\nTesting category distribution:")
    print(test["category"].value_counts().sort_index())

    train_labels = set(train["category"])
    test_labels = set(test["category"])

    print("\nLabels in training:", len(train_labels))
    print("Labels in testing:", len(test_labels))

    print("Labels missing from training:", test_labels - train_labels)
    print("Labels missing from testing:", train_labels - test_labels)

    profile_text(train, "text")
    profile_text(test, "text")

    print("\nDuplicate training messages:",
          train["text"].duplicated().sum())

    print("Duplicate testing messages:",
          test["text"].duplicated().sum())

    overlap = set(train["text"]) & set(test["text"])

    print("Exact text overlap between train and test:", len(overlap))


if __name__ == "__main__":
    profile_bitext()
    profile_banking77()

    print("\n" + "=" * 60)
    print("DATA QUALITY PROFILING COMPLETED")
    print("=" * 60)
