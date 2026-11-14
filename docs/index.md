# Rolling Monitoring of System Metrics and Governance Readiness

Continuous Intelligence | Project 04 | Experiment Report

**Author:** Sabriya Sowers
**Date:** November 2026

## Overview

This project investigates how rolling statistics can reveal patterns in measurements over time. Individual observations may fluctuate, while rolling averages help show broader trends by reducing short-term variation.

I first completed the instructor's controlled experiment by changing the rolling window for system metrics from 3 to 5 observations. I then extended the project into a **Metadata Completeness & Governance Readiness Monitor**, using synthetic healthcare metadata from my Project 03 inventory.

The original system monitoring example and my governance customization are separate components of the same project.

## Data

### Original System Metrics

The instructor's dataset, [`data/system_metrics_timeseries.csv`](https://github.com/ssowers2/cintel-04-rolling-monitoring/blob/main/data/system_metrics_timeseries.csv), contains 60 time-series observations. Each observation includes:

- `timestamp` — time of observation.
- `requests` — number of requests.
- `errors` — number of errors.
- `total_latency_ms` — total latency in milliseconds.

### Synthetic Governance Metrics

My customization starts with 60 synthetic healthcare metadata assets from Project 03. Each asset includes fields used to assess governance readiness, such as owner, steward, description, business definition, and classification.

A Python generator creates 12 simulated weekly snapshots, producing:

| Dataset | Purpose | Records |
|---|---|---:|
| `data/metadata_inventory.csv` | Source synthetic metadata inventory | 60 |
| `data/governance_inventory_timeseries.csv` | Simulated asset-level weekly snapshots | 720 |
| `data/governance_metrics_timeseries.csv` | Aggregated weekly governance metrics | 12 |
| `artifacts/governance_rolling_metrics.csv` | Weekly metrics and rolling averages | 12 |

The last simulated week matches the Project 03 inventory. Earlier weeks were generated for the exercise; they are **not actual historical observations**. The data does not contain real patient information or organizational performance measurements.

## Methods

### Original Rolling Monitoring Experiment

The original pipeline uses Polars to sort the system measurements by timestamp and calculate rolling averages for requests, errors, and total latency.

The instructor's starting window was 3 observations. I changed it to 5 observations in `src/cintel/rolling_monitor.py`:

```python
WINDOW_SIZE: int = 5
```

Each completed five-observation window includes the current observation and the four preceding observations. The first four rows do not have enough observations for a complete five-observation rolling average.

### Governance Monitoring Customization

I created two additional Python scripts:

1. `src/cintel/generate_governance_history.py` generates simulated weekly metadata snapshots and governance summaries.
2. `src/cintel/governance_monitor.py` reads the weekly summaries, sorts them by week, and calculates five-week rolling averages with Polars.

The governance monitor tracks four metrics:

| Metric | Meaning | Desired Direction |
|---|---|---|
| Metadata completeness | Share of assets with required descriptive metadata populated | Higher |
| Ownership coverage | Share of assets assigned a data owner | Higher |
| Stewardship coverage | Share of assets assigned a data steward | Higher |
| Documentation gaps | Share of assets missing a description or business definition | Lower |

The first four weeks have no five-week rolling average because a complete window is not yet available.

### Interactive Visualization

I created `src/cintel/governance_app.py` as a separate Marimo dashboard. It includes a rolling-window slider, a governance metric dropdown, an Altair line chart comparing weekly measurements with their rolling average, and a table of the weekly data.

The dashboard starts with a five-week window, but the slider lets users explore different window sizes. The command-line governance pipeline uses a fixed five-week window.

To run the dashboard locally from the repository root:

```shell
uv run marimo run src/cintel/governance_app.py
```

To run the original instructor app:

```shell
uv run marimo run src/cintel/app.py
```

## Results

### Original Experiment Results

Both the original and modified system monitoring pipelines successfully processed 60 records.

| Measurement | Original | Modified |
|---|---|---|
| Rolling window | 3 observations | 5 observations |
| Records processed | 60 | 60 |
| Pipeline execution | Successful | Successful |
| Output file | `rolling_metrics.csv` | `rolling_metrics.csv` |

The modified pipeline generated updated results in `artifacts/rolling_metrics.csv`, and the execution logs confirmed the new window size was used. I did not make a numerical before-and-after comparison to quantify smoothing in this dataset.

[View original rolling monitoring results](https://github.com/ssowers2/cintel-04-rolling-monitoring/blob/main/artifacts/rolling_metrics.csv)

### Governance Monitoring Results

The governance generator produced 720 simulated asset-week records and 12 weekly summary records. The governance pipeline processed the 12 summaries and calculated five-week rolling averages for metadata completeness, ownership coverage, stewardship coverage, and documentation gaps.

The Marimo dashboard successfully displayed the weekly values and rolling trends. In the simulated data, metadata completeness generally rises over the 12 weeks, with some week-to-week fluctuations. The rolling average shows a smoother pattern than the individual weekly observations.

### Automated Verification

I ran the project's automated tests using:

```shell
uv run pytest -v
```

The latest full test run reported:

| Test | Result |
|---|---|
| Five-week rolling-average calculation | Passed |
| Governance monitoring pipeline | Passed |
| Original rolling monitoring pipeline | Passed |
| Original application test | Passed |

**Four tests passed. Overall coverage was 32.24%, exceeding the required 20%.** Both rolling monitoring modules reached 97% coverage in that run. The interactive Marimo dashboard was reviewed locally in the browser but its individual cells were not exercised by the automated tests.

## Interpretation

### Original Experiment

Increasing the rolling window from 3 to 5 includes more observations in each calculation. In general, a larger window can reduce the influence of short-term fluctuations, but it can also respond more slowly to sudden changes. A direct numerical comparison of both output files would be needed to confirm the amount of smoothing in the original system dataset.

### Governance Customization

Rolling monitoring can also help evaluate data governance readiness. For example, trends in ownership and stewardship coverage can show whether accountability assignments are becoming more complete, while documentation-gap trends can highlight areas needing attention.

The synthetic dashboard demonstrates how weekly fluctuations and a smoothed trend can tell different parts of the story. The results illustrate a monitoring approach; they do not demonstrate real-world governance improvement.

## Limitations

- The original controlled experiment verified successful execution but did not include a numerical comparison of the 3- and 5-observation results.
- Rolling averages can make sudden changes less visible, depending on the window size.
- The governance history is simulated, not collected from a real organization over 12 weeks.
- The governance metrics depend on the completeness rules used to calculate them; real-world use would require agreed definitions and validated sources.
- The project does not automatically classify anomalies or send monitoring alerts.
- The governance dashboard has been tested locally in Marimo; this report does not claim it is deployed as a separate browser-hosted dashboard.

## Custom Modifications

### Experiment 1: Increasing the Rolling Window Size

**What I changed:** I changed `WINDOW_SIZE` in `src/cintel/rolling_monitor.py` from 3 to 5 observations.

**Why I chose this modification:** I wanted to understand how the number of observations in a rolling average affects the interpretation of system performance trends.

**My prediction:** I expected the five-observation average to be smoother because each calculation includes more observations.

**What actually happened:** Both versions processed 60 records successfully, and the modified pipeline generated a new `artifacts/rolling_metrics.csv`. I did not directly compare the numerical values to confirm the smoothing effect.

**What I learned:** Window size is an important monitoring choice. Larger windows can make trends easier to follow but may also delay the visibility of sudden changes.

**Original setting:**

```python
WINDOW_SIZE: int = 3
```

**Modified setting:**

```python
WINDOW_SIZE: int = 5
```

### Experiment 2: Metadata Completeness & Governance Readiness Monitor

**What I changed:** I added a synthetic governance time-series generator, a governance rolling monitoring pipeline, automated tests, and an interactive Marimo dashboard. I kept the instructor's original system monitoring example intact.

**Why I chose this customization:** My Project 03 work measured metadata readiness at one point in time. I wanted to explore how the same governance metrics could be monitored over multiple weeks.

**My approach:** I generated 12 simulated weekly snapshots from 60 synthetic metadata assets, summarized four governance metrics by week, and calculated five-week rolling averages.

**What actually happened:** The data generator produced 720 asset-week records and 12 weekly summaries. The governance pipeline ran successfully, the dashboard displayed the data and trends, and all four automated tests passed.

**What I learned:** Rolling analytics can be useful beyond traditional system performance monitoring. They can provide a consistent way to review metadata completeness, accountability assignments, and documentation gaps over time. I also gained experience connecting data generation, Polars processing, automated testing, and reactive visualization.

## Conclusion

This project helped me understand how rolling statistics add a time-based perspective to monitoring. My original experiment showed how changing the rolling window changes the observations included in each calculation.

I extended that idea into a Metadata Completeness & Governance Readiness Monitor using simulated healthcare metadata. The customization demonstrates how a data governance team could monitor trends in completeness, ownership, stewardship, and documentation gaps rather than relying only on a single snapshot.

The most important limitation is that the historical governance values are simulated. The project demonstrates a repeatable technical approach, not evidence of actual organizational change.

## Documentation Index

- **Home** — Project 04 overview and experiment report.
- [Project Instructions](project-instructions.md)
- [Glossary](glossary.md)
- [API Documentation](api.md)
- [GitHub Repository](https://github.com/ssowers2/cintel-04-rolling-monitoring)

### Interactive Applications

- [Original Rolling Monitoring App (Source Code)](https://github.com/ssowers2/cintel-04-rolling-monitoring/blob/main/src/cintel/app.py)
- [Governance Readiness Dashboard (Source Code)](https://github.com/ssowers2/cintel-04-rolling-monitoring/blob/main/src/cintel/governance_app.py)

Both applications can be run locally using Marimo. Publishing the interactive dashboards to GitHub Pages is a separate deployment step.

## Project Links

### My Governance Monitoring Customization

- [Interactive Governance Dashboard (Python Source)](https://github.com/ssowers2/cintel-04-rolling-monitoring/blob/main/src/cintel/governance_app.py)
- [Governance Monitoring Pipeline](https://github.com/ssowers2/cintel-04-rolling-monitoring/blob/main/src/cintel/governance_monitor.py)
- [Governance History Generator](https://github.com/ssowers2/cintel-04-rolling-monitoring/blob/main/src/cintel/generate_governance_history.py)
- [Synthetic Metadata Inventory](https://github.com/ssowers2/cintel-04-rolling-monitoring/blob/main/data/metadata_inventory.csv)
- [Weekly Governance Metrics](https://github.com/ssowers2/cintel-04-rolling-monitoring/blob/main/data/governance_metrics_timeseries.csv)
- [Weekly Governance Inventory Snapshots](https://github.com/ssowers2/cintel-04-rolling-monitoring/blob/main/data/governance_inventory_timeseries.csv)
- [Governance Rolling Results](https://github.com/ssowers2/cintel-04-rolling-monitoring/blob/main/artifacts/governance_rolling_metrics.csv)

### Original Rolling Monitoring Example

- [Original Marimo Application](https://github.com/ssowers2/cintel-04-rolling-monitoring/blob/main/src/cintel/app.py)
- [Original Rolling Monitoring Pipeline](https://github.com/ssowers2/cintel-04-rolling-monitoring/blob/main/src/cintel/rolling_monitor.py)
- [System Metrics Dataset](https://github.com/ssowers2/cintel-04-rolling-monitoring/blob/main/data/system_metrics_timeseries.csv)
- [Original Rolling Results](https://github.com/ssowers2/cintel-04-rolling-monitoring/blob/main/artifacts/rolling_metrics.csv)

### Project Website and Documentation

- [GitHub Repository](https://github.com/ssowers2/cintel-04-rolling-monitoring)
- [Published Project Documentation](https://ssowers2.github.io/cintel-04-rolling-monitoring/)

## Project Resources

- [Project Instructions](project-instructions.md)
- [Professional Python Guide](https://denisecase.github.io/pro-analytics-02/)
- [Professional Python Project Explainer](https://pup-pack.github.io/professional-python-project-explainer/)
- [Suggested Datasets](https://denisecase.github.io/pro-analytics-02/reference/datasets/cintel/)
