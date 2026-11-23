
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
OUTPUT = ROOT / "data" / "processed"

OUTPUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(
    RAW / "bitext_customer_support.csv",
    dtype="str"
)

# Group repeated customer instructions
duplicates = (
    df.groupby("instruction")
    .agg(
        occurrences=("instruction", "size"),
        category_count=("category", "nunique"),
        intent_count=("intent", "nunique"),
        categories=("category", lambda x: " | ".join(sorted(x.unique()))),
        intents=("intent", lambda x: " | ".join(sorted(x.unique())))
    )
    .reset_index()
)

duplicates = duplicates[duplicates["occurrences"] > 1]

# Identify potentially conflicting labels
conflicts = duplicates[
    (duplicates["category_count"] > 1) |
    (duplicates["intent_count"] > 1)
]

# Save the complete duplicate audit
report_path = OUTPUT / "bitext_duplicate_audit.csv"
duplicates.sort_values(
    "occurrences",
    ascending=False
).to_csv(report_path, index=False)

print("=" * 55)
print("BITEXT DUPLICATE INVESTIGATION")
print("=" * 55)

print("\nUnique repeated instructions:", len(duplicates))
print("Instructions with conflicting categories/intents:", len(conflicts))
print("Instructions with consistent labels:", len(duplicates) - len(conflicts))

print("\nTop 15 repeated instructions:")
print(
    duplicates.sort_values(
        "occurrences",
        ascending=False
    )[["instruction", "occurrences", "categories", "intents"]]
    .head(15)
    .to_string(index=False)
)

print("\nPotential label conflicts:")
print(
    conflicts[
        ["instruction", "occurrences", "categories", "intents"]
    ].head(15).to_string(index=False)
)

print("\nAudit saved to:", report_path)
print("\nINVESTIGATION COMPLETED")
