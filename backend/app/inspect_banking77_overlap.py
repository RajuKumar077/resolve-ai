
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "processed"

train = pd.read_csv(DATA / "banking77_train.csv", dtype="str")
test = pd.read_csv(DATA / "banking77_test.csv", dtype="str")

print("=" * 60)
print("BANKING77 OVERLAP INVESTIGATION")
print("=" * 60)

# Find messages appearing in both splits
overlap = set(train["text"]) & set(test["text"])

print("\nOverlapping messages:", len(overlap))

for message in sorted(overlap):
    print("\nMessage:", repr(message))

    print("Training records:")
    print(
        train.loc[
            train["text"] == message,
            ["text", "category"]
        ].to_string(index=False)
    )

    print("Testing records:")
    print(
        test.loc[
            test["text"] == message,
            ["text", "category"]
        ].to_string(index=False)
    )

# Inspect duplicate records within the official test set
duplicates = test[
    test.duplicated(subset=["text", "category"], keep=False)
].sort_values("text")

print("\n" + "=" * 60)
print("DUPLICATES INSIDE TEST SET")
print("=" * 60)

if duplicates.empty:
    print("No duplicate records found.")
else:
    print(duplicates.to_string(index=False))

# Check whether duplicate text has conflicting labels
conflicts = (
    test.groupby("text")["category"]
    .nunique()
)

conflicts = conflicts[conflicts > 1]

print("\nMessages with conflicting test labels:", len(conflicts))

print("\nINVESTIGATION COMPLETED")
