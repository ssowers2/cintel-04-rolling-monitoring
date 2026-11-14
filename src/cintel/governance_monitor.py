"""Monitor synthetic data governance metrics over time.

Author: Sabriya Sowers
Project: Continuous Intelligence - Project 04

Purpose:
    Read weekly governance metrics generated from the
    Project 03 metadata inventory.

    Calculate five-week rolling averages to monitor
    metadata completeness, ownership, stewardship,
    and documentation gaps over time.

Input:
    data/governance_metrics_timeseries.csv

Output:
    artifacts/governance_rolling_metrics.csv

Run:
    uv run python -m cintel.governance_monitor

Note:
    Historical observations are simulated for
    educational purposes.
"""

# === IMPORTS ===

import logging
from pathlib import Path
from typing import Final

from datafun_toolkit.logger import get_logger, log_header, log_path
import polars as pl

# === CONFIGURE LOGGER ===

LOG: logging.Logger = get_logger("P4-GOV", level="DEBUG")

# === DEFINE PATHS AND SETTINGS ===

ROOT_DIR: Final[Path] = Path.cwd()
DATA_DIR: Final[Path] = ROOT_DIR / "data"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"

DATA_FILE: Final[Path] = DATA_DIR / "governance_metrics_timeseries.csv"

OUTPUT_FILE: Final[Path] = ARTIFACTS_DIR / "governance_rolling_metrics.csv"

WINDOW_SIZE: Final[int] = 5

METRICS: Final[tuple[str, ...]] = (
    "metadata_completeness_pct",
    "ownership_pct",
    "stewardship_pct",
    "documentation_gaps_pct",
)


# === MAIN FUNCTION ===


def main() -> None:
    """Load governance metrics, calculate rolling means, and save results."""
    log_header(LOG, "CINTEL")

    LOG.info("========================")
    LOG.info("START governance monitoring")
    LOG.info("========================")

    log_path(LOG, "ROOT_DIR", ROOT_DIR)
    log_path(LOG, "DATA_FILE", DATA_FILE)
    log_path(LOG, "OUTPUT_FILE", OUTPUT_FILE)

    # STEP 1: READ AND SORT DATA

    df: pl.DataFrame = pl.read_csv(
        DATA_FILE,
        try_parse_dates=True,
    ).sort("week")

    LOG.info(f"Loaded {df.height} weekly governance records")

    # STEP 2: COMPUTE ROLLING AVERAGES

    LOG.info(f"WINDOW_SIZE: {WINDOW_SIZE}")

    rolling_expressions = [
        pl.col(metric)
        .rolling_mean(window_size=WINDOW_SIZE)
        .alias(f"{metric}_rolling_mean")
        for metric in METRICS
    ]

    df_with_rolling: pl.DataFrame = df.with_columns(rolling_expressions)

    LOG.info("Computed governance rolling averages")

    # STEP 3: SAVE RESULTS

    ARTIFACTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    df_with_rolling.write_csv(OUTPUT_FILE)

    log_path(LOG, "OUTPUT_FILE", OUTPUT_FILE)

    LOG.info("========================")
    LOG.info("Governance pipeline executed successfully!")
    LOG.info("========================")
    LOG.info("END governance monitoring")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    main()
