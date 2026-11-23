
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "processed"


def load(name):
    return pd.read_csv(DATA / name, dtype="str")


def check_splits(name, files, text_column, label_column):
    print(f"\n{'=' * 55}")
    print(name)
    print("=" * 55)

    datasets = {split: load(file) for split, file in files.items()}

    for split, df in datasets.items():
        print(f"\n{split}: {len(df):,} records")
        print("Unique labels:", df[label_column].nunique())
        print("Missing values:", df[[text_column, label_column]].isna().sum().sum())
        print("Empty messages:", (df[text_column].str.strip() == "").sum())
        print("Duplicate message-label pairs:",
              df.duplicated(subset=[text_column, label_column]).sum())

    # Compare normalized messages across every pair of splits.
    split_names = list(datasets.keys())

    print("\nCross-split message overlap:")

    for i in range(len(split_names)):
        for j in range(i + 1, len(split_names)):
            a = split_names[i]
            b = split_names[j]

            overlap = (
                set(datasets[a][text_column].str.strip())
                & set(datasets[b][text_column].str.strip())
            )

            print(f"{a} vs {b}: {len(overlap)} overlapping messages")

    # Verify label coverage across splits.
    all_labels = set().union(
        *(set(df[label_column]) for df in datasets.values())
    )

    for split, df in datasets.items():
        missing = all_labels - set(df[label_column])
        print(f"{split} missing labels:", len(missing))

    return datasets


if __name__ == "__main__":

    bitext = check_splits(
        "BITEXT VALIDATION",
        {
            "Train": "bitext_train.csv",
            "Validation": "bitext_validation.csv",
            "Test": "bitext_test.csv",
        },
        "instruction",
        "intent",
    )

    banking = check_splits(
        "BANKING77 VALIDATION",
        {
            "Train": "banking77_train.csv",
            "Validation": "banking77_validation.csv",
            "Test": "banking77_test.csv",
        },
        "text",
        "category",
    )

    knowledge = load("bitext_knowledge.csv")

    print("\n" + "=" * 55)
    print("BITEXT KNOWLEDGE DATASET")
    print("=" * 55)
    print("Knowledge records:", len(knowledge))
    print("Unique intents:", knowledge["intent"].nunique())

    print("\nVALIDATION COMPLETED")
