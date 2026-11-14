# Data Card: Metadata Completeness & Governance Readiness Monitor

**Project:** Continuous Intelligence — Project 04: Rolling Monitoring  
**Author:** Sabriya Sowers  
**Date:** November 2026  
**Data type:** Synthetic healthcare metadata; simulated weekly observations

## Overview

This project uses a synthetic metadata inventory to demonstrate how rolling statistics can monitor data governance readiness over time. It builds on the metadata inventory developed for Project 03. The data describes **metadata assets**, not patients or clinical encounters.

The historical observations are **simulated for educational purposes**. They must not be interpreted as measurements of an actual healthcare organization.

## Data Sources and Files

| File | Contents | Rows |
|---|---|---:|
| `data/metadata_inventory.csv` | Synthetic metadata inventory carried forward from Project 03 | 60 |
| `data/governance_inventory_timeseries.csv` | Twelve simulated weekly snapshots of the 60 metadata assets | 720 |
| `data/governance_metrics_timeseries.csv` | One summary of governance metrics per simulated week | 12 |
| `artifacts/governance_rolling_metrics.csv` | Weekly metrics and their five-week rolling averages | 12 |

The original instructor-provided system metrics in `data/system_metrics_timeseries.csv` are a separate example and are not the source of the governance measurements.

## Inventory Fields

The source metadata inventory includes fields such as:

- `asset_id` — identifier for a metadata asset.
- `data_owner` — assigned owner, when populated.
- `data_steward` — assigned steward, when populated.
- `description` — descriptive information about the asset.
- `business_definition` — business meaning or definition of the asset.
- `data_classification` — classification information associated with the asset.

These fields support an educational demonstration of metadata documentation and accountability.

## How the Historical Data Was Created

The script `src/cintel/generate_governance_history.py` generates twelve weekly snapshots based on the 60-asset inventory. This produces 720 asset-week records. It then summarizes the snapshots into twelve weekly metric rows.

The **final simulated week matches the Project 03 inventory**. Earlier weeks are generated to illustrate how governance metrics might change over time; they are not recovered historical records.

To regenerate the simulated datasets from the project root:

```powershell
uv run python src/cintel/generate_governance_history.py
```

## Governance Metrics

| Metric | Meaning | Preferred direction |
|---|---|---|
| `metadata_completeness_pct` | Percentage of assets meeting the project's metadata completeness criteria | Higher |
| `ownership_pct` | Percentage of assets with an assigned data owner | Higher |
| `stewardship_pct` | Percentage of assets with an assigned data steward | Higher |
| `documentation_gaps_pct` | Percentage of assets with missing descriptive documentation | Lower |

The exact rules for determining completeness and documentation gaps are implemented in the project's Python code. These are project-specific measures, not universal governance standards.

## Rolling Monitoring

The script `src/cintel/governance_monitor.py` sorts weekly summaries chronologically and calculates **five-week rolling averages** for all four governance metrics using Polars.

The first four weeks do not have complete five-week windows, so their rolling-average fields are null. With twelve weekly observations, eight weeks have full five-week rolling averages.

Run the pipeline with:

```powershell
uv run python -m cintel.governance_monitor
```

The resulting file is `artifacts/governance_rolling_metrics.csv`.

An interactive Marimo dashboard in `src/cintel/governance_app.py` allows users to select a metric and explore different rolling-window sizes.

## Intended Uses

- Practice time-series processing and rolling-average calculations.
- Explore trends in metadata completeness, ownership, stewardship, and documentation gaps.
- Demonstrate a possible approach to governance readiness reporting.
- Support a student portfolio showing Python, Polars, testing, and visualization skills.

## Limitations and Responsible Use

- **Synthetic data:** None of the governance history represents actual organizational measurements.
- **Simulated trends:** Any apparent improvement or decline was generated for demonstration and is not evidence of real-world change.
- **Small scope:** The inventory contains 60 assets and only twelve weekly observations.
- **Metric definitions:** Completeness and documentation measures depend on project-specific rules and may not generalize to other organizations.
- **No alerts or validation of operational sources:** The project demonstrates monitoring calculations, not a production data governance platform.
- **No PHI:** The dataset is intended to contain synthetic metadata, not patient-level protected health information.

Do not use these outputs for real operational decisions or represent them as actual healthcare organization performance.

## Related Project Files

- [README.md](README.md) — project overview, setup, and results.
- [docs/index.md](docs/index.md) — experiment report and interpretation.
- [Synthetic data generator](src/cintel/generate_governance_history.py)
- [Governance monitoring pipeline](src/cintel/governance_monitor.py)
- [Governance dashboard](src/cintel/governance_app.py)
