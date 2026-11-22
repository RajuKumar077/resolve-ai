
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"

FILES = [
    "bitext_customer_support.csv",
    "banking77_train.csv",
    "banking77_test.csv",
]


def inspect_dataset(filename):
    file_path = RAW_DIR / filename

    print("\n" + "=" * 65)
    print(f"DATASET: {filename}")
    print("=" * 65)

    df = pd.read_csv(file_path)

    print(f"\nShape: {df.shape}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print(f"\nDuplicate rows: {df.duplicated().sum()}")

    print("\nUnique values per column:")
    print(df.nunique())

    print("\nPossible category / intent distributions:")

    for column in df.select_dtypes(include="object").columns:
        unique_count = df[column].nunique()

        if 1 < unique_count <= 100:
            print(f"\n{column} ({unique_count} unique values):") 
            print(df[column].value_counts().head(10))

    print("\nSample records:")
    print(df.head(3).to_string(index=False, max_cols=8))


if __name__ == "__main__":
    for filename in FILES:
        inspect_dataset(filename)
