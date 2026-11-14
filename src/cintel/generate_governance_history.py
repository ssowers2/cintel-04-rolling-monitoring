"""Generate reproducible, entirely simulated weekly metadata snapshots.

Run from Project 04 repository root after copying Project 03's
metadata_inventory.csv into data/:
    python generate_governance_history.py
"""

from __future__ import annotations

import csv
from datetime import date, timedelta
from pathlib import Path
import random

SOURCE = Path("data/metadata_inventory.csv")
OUTPUT = Path("data/governance_inventory_timeseries.csv")
METRICS = Path("data/governance_metrics_timeseries.csv")

FIELDS = (
    "data_owner",
    "data_steward",
    "description",
    "business_definition",
    "data_classification",
)

GOOD = {
    "data_owner": "Assigned",
    "data_steward": "Assigned",
    "description": "Complete",
    "business_definition": "Complete",
}

SEED = 404
WEEKS = 12
LAST_WEEK = date(2026, 11, 9)


def main() -> None:
    """Generate synthetic weekly governance snapshots and summary metrics."""
    with SOURCE.open(newline="", encoding="utf-8-sig") as f:
        original = list(csv.DictReader(f))

    if not original or len({r["asset_id"] for r in original}) != len(original):
        raise ValueError("Inventory must contain unique asset IDs")

    rng = random.Random(SEED)
    snapshots = []
    weekly = []

    for i in range(WEEKS):
        week = (LAST_WEEK - timedelta(weeks=WEEKS - 1 - i)).isoformat()

        rows = []

        for item in original:
            row = dict(item)

            for field in FIELDS:
                value = item[field]

                # Earlier simulated weeks have more missing values.
                # Occasional temporary improvements create setbacks
                # before the final snapshot.

                if i < WEEKS - 1:
                    missing_chance = 0.38 * (WEEKS - 1 - i) / (WEEKS - 1)

                    if value != "Missing" and rng.random() < missing_chance:
                        row[field] = "Missing"

                    elif value == "Missing" and rng.random() < 0.06:
                        row[field] = GOOD.get(field, "Internal")

            rows.append({"week": week, **row})

        snapshots.extend(rows)
        n = len(rows)

        weekly.append(
            {
                "week": week,
                "metadata_completeness_pct": round(
                    100
                    * sum(
                        all(
                            r[c] != "Missing"
                            for c in (
                                "description",
                                "business_definition",
                                "data_classification",
                            )
                        )
                        for r in rows
                    )
                    / n,
                    2,
                ),
                "ownership_pct": round(
                    100 * sum(r["data_owner"] == "Assigned" for r in rows) / n,
                    2,
                ),
                "stewardship_pct": round(
                    100 * sum(r["data_steward"] == "Assigned" for r in rows) / n,
                    2,
                ),
                "documentation_gaps_pct": round(
                    100
                    * sum(
                        r["description"] == "Missing"
                        or r["business_definition"] == "Missing"
                        for r in rows
                    )
                    / n,
                    2,
                ),
            }
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    for path, rows in (
        (OUTPUT, snapshots),
        (METRICS, weekly),
    ):
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    print(f"Created {OUTPUT} ({len(snapshots)} asset-week records)")
    print(f"Created {METRICS} ({len(weekly)} weekly summaries)")
    print("Final week matches Project 03 inventory exactly.")


if __name__ == "__main__":
    main()
