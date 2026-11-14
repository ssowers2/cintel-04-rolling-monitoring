# cintel-04-rolling-monitoring

[![Python 3.14](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](pyproject.toml)
[![CI](https://github.com/ssowers2/cintel-04-rolling-monitoring/actions/workflows/ci-python-zensical.yml/badge.svg)](https://github.com/ssowers2/cintel-04-rolling-monitoring/actions/workflows/ci-python-zensical.yml)
[![Documentation](https://img.shields.io/badge/docs-site-blue?logo=github)](https://ssowers2.github.io/cintel-04-rolling-monitoring/)

[![uv managed](https://img.shields.io/badge/uv-managed-DE5FE9)](https://docs.astral.sh/uv/)
[![ty type checked](https://img.shields.io/badge/ty-type_checked-2F80ED)](https://docs.astral.sh/ty/)
[![Zensical docs](https://img.shields.io/badge/Zensical-docs-purple)](https://zensical.org/)
[![MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

> Monitor time-series measurements using rolling statistics, with an applied example focused on metadata completeness and data governance readiness.

## Project Overview

**Author:** Sabriya Sowers
**Date:** November 2026

This project introduces rolling monitoring, a technique used to analyze measurements collected over time.

The goal is to understand how rolling averages can smooth short-term fluctuations and make longer-term trends easier to identify.

The project includes two applications:

1. **Original system monitoring example:** Uses operational system metrics to demonstrate rolling averages.
2. **Metadata Completeness & Governance Readiness Monitor:** Applies the same technique to simulated healthcare data governance metrics.

The governance customization builds on my Project 03 metadata inventory by introducing a time-series component to monitor governance readiness over multiple weeks.

The project is configured in [pyproject.toml](pyproject.toml).

## Data

### Original System Metrics

The original example uses time-series system metrics from the `data/` folder.

The pipeline processes 60 observations.

Each observation includes:

- `timestamp` — time of observation.
- `requests` — number of requests handled.
- `errors` — number of failed requests.
- `total_latency_ms` — total response time in milliseconds.

**Source:** `data/system_metrics_timeseries.csv`

### Governance Monitoring Data

For my customization, I reused the synthetic healthcare metadata inventory developed in Project 03.

The inventory contains 60 metadata assets with fields related to ownership, stewardship, descriptions, business definitions, and data classification.

I created a reproducible Python script to generate 12 weekly snapshots from this inventory.

The resulting datasets include:

| Dataset | Description | Records |
|---|---|---:|
| `metadata_inventory.csv` | Original synthetic metadata inventory from Project 03 | 60 |
| `governance_inventory_timeseries.csv` | Simulated weekly metadata snapshots | 720 |
| `governance_metrics_timeseries.csv` | Weekly governance metric summaries | 12 |
| `governance_rolling_metrics.csv` | Weekly summaries with five-week rolling averages | 12 |

The final simulated week preserves the original Project 03 inventory values.

Earlier weeks were generated to simulate changes in metadata completeness and governance readiness.

**Important:** All historical observations are synthetic and were created for educational purposes. They do not represent actual organizational performance or patient information.

## Approach

### Original Rolling Monitoring Pipeline

The original pipeline uses Polars to:

1. Read and sort observations by timestamp.
2. Calculate rolling averages over a defined window.
3. Save the monitoring results for interpretation.
4. Log the pipeline process.

The original example used a rolling window of three observations.

For my controlled experiment, I increased the window size to five observations.

### Governance Monitoring Pipeline

I applied the same rolling monitoring approach to data governance metrics.

The governance pipeline:

1. Reads the weekly governance metrics.
2. Sorts the observations chronologically.
3. Calculates five-week rolling averages.
4. Saves the results as a CSV artifact.
5. Logs the pipeline execution.

The four governance metrics are:

| Metric | Description | Desired Direction |
|---|---|---|
| Metadata completeness | Percentage of assets with required descriptive metadata populated | Higher |
| Ownership coverage | Percentage of assets with an assigned data owner | Higher |
| Stewardship coverage | Percentage of assets with an assigned data steward | Higher |
| Documentation gaps | Percentage of assets missing a description or business definition | Lower |

Rolling averages provide a smoother view of changes in these metrics over time.

The first four observations do not have five-week rolling averages because there are not yet enough observations to fill the window.

## Run the Project

Follow the [Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/) to set up your machine and Python environment.

Open a VS Code terminal in the project root.

### Run the Original Monitoring Pipeline

```shell
uv run python -m cintel.rolling_monitor
```

**Output:** `artifacts/rolling_metrics.csv`

### Generate the Governance Time-Series Data

```shell
uv run python src/cintel/generate_governance_history.py
```

This creates:

- `data/governance_inventory_timeseries.csv`
- `data/governance_metrics_timeseries.csv`

### Run the Governance Monitoring Pipeline

```shell
uv run python -m cintel.governance_monitor
```

**Output:** `artifacts/governance_rolling_metrics.csv`

## Interactive Marimo Applications

This project includes two reactive Marimo applications.

### Original Rolling Monitoring App

```shell
uv run marimo run src/cintel/app.py
```

The original application demonstrates rolling monitoring using system performance metrics.

### Governance Readiness Dashboard

```shell
uv run marimo run src/cintel/governance_app.py
```

To open the dashboard in editing mode:

```shell
uv run marimo edit src/cintel/governance_app.py
```

The governance dashboard includes:

- An interactive rolling-window slider.
- A dropdown for selecting governance metrics.
- A line chart comparing weekly values with rolling averages.
- An interactive table of weekly governance measurements.
- Explanations of the metrics and their interpretation.

The dashboard starts with a five-week rolling window. The slider allows users to explore how changing the window size affects the displayed trends.

The command-line governance pipeline continues to use a fixed five-week window.

To stop a running Marimo application, press **Ctrl + C** in the VS Code terminal.

## Results

### Original Rolling Monitoring Results

The original pipeline successfully processed 60 time-series observations.

Both the three-observation and five-observation configurations executed successfully.

The pipeline writes its results to:

`artifacts/rolling_metrics.csv`

### Governance Monitoring Results

The governance data-generation script successfully created:

- 720 simulated asset-week records.
- 12 weekly governance summaries.

The governance monitoring pipeline successfully loaded all 12 weekly summaries and calculated rolling averages for the four governance metrics.

The results are saved to:

`artifacts/governance_rolling_metrics.csv`

### Interpretation

The simulated metadata completeness measurements generally improve across the 12-week observation period, although individual weekly values fluctuate.

The five-week rolling average provides a smoother representation of the overall trend.

This illustrates how rolling monitoring could help data governance teams distinguish short-term variation from broader changes in metadata quality.

For governance monitoring:

- Increasing metadata completeness may indicate improved documentation.
- Increasing ownership coverage may indicate clearer accountability.
- Increasing stewardship coverage may indicate stronger stewardship participation.
- Decreasing documentation gaps may indicate improvements in metadata quality.

These interpretations are illustrative because the historical observations were simulated.

## Custom Modifications

### Experiment 1: Increasing the Rolling Window Size

**What I changed:**

I modified the rolling window size in `src/cintel/rolling_monitor.py` from three to five observations.

**Why I chose this modification:**

I wanted to understand how increasing the window size affects rolling averages and the ability to identify trends in system performance.

**My prediction:**

I predicted that increasing the window size would produce smoother rolling averages and reduce the impact of short-term fluctuations because more observations would be included in each calculation.

**What actually happened:**

Both versions of the pipeline executed successfully and processed 60 time-series records.

The original pipeline used a window size of three, while the modified pipeline used a window size of five.

The modified pipeline generated updated results in `artifacts/rolling_metrics.csv`.

The original and modified numerical results were not directly compared to quantify the smoothing effect.

**What I learned:**

I learned that changing the window size affects how rolling averages are calculated.

A larger window includes more observations, which can help smooth short-term fluctuations but may also delay the detection of sudden changes.

#### Experiment Summary

| Measurement | Original | Modified |
|---|---|---|
| Window size | 3 | 5 |
| Records processed | 60 | 60 |
| Pipeline execution | Successful | Successful |
| Output file | `rolling_metrics.csv` | `rolling_metrics.csv` |

**Modified code:**

```python
WINDOW_SIZE: int = 5
```

### Experiment 2: Applying Rolling Monitoring to Data Governance

**What I changed:**

I created a separate governance monitoring pipeline and interactive dashboard using synthetic healthcare metadata.

**Why I chose this customization:**

Data governance programs depend on accurate metadata, clearly assigned ownership, stewardship responsibilities, and complete documentation.

I wanted to explore how rolling monitoring could help measure progress in these areas over time.

**My approach:**

I reused my Project 03 synthetic metadata inventory, generated 12 weeks of simulated observations, and calculated governance metrics for each week.

I then applied five-week rolling averages to the weekly measurements.

**What happened:**

The governance pipeline successfully processed 12 weekly summaries and created rolling monitoring results.

The Marimo dashboard displayed the weekly metrics alongside their rolling averages.

**What I learned:**

Rolling monitoring is not limited to technical system performance.

The same approach can be applied to data governance metrics to help identify patterns, evaluate progress, and highlight areas that may need additional attention.

I also learned how to connect data generation, time-series processing, automated testing, and interactive visualization within one Python project.

## Automated Testing and Verification

The project uses pytest for automated testing.

Run all tests:

```shell
uv run pytest -v
```

The latest full test execution completed successfully:

| Test | Result |
|---|---|
| Five-week rolling-average calculation | Passed |
| Governance monitoring pipeline | Passed |
| Original rolling monitoring pipeline | Passed |
| Original application test | Passed |

**Results:** Four tests passed.

**Overall code coverage:** 33.19%.

**Required coverage:** 20%.

The project exceeded its required coverage threshold.

The governance monitoring and original rolling monitoring modules each achieved 97% coverage in the reported test run.

The Marimo dashboard was also reviewed interactively in the browser, although its individual cells were not covered by the automated tests.

## Project Files

| File | Purpose |
|---|---|
| `src/cintel/rolling_monitor.py` | Original rolling monitoring pipeline |
| `src/cintel/governance_monitor.py` | Governance rolling monitoring pipeline |
| `src/cintel/generate_governance_history.py` | Synthetic weekly governance data generator |
| `src/cintel/app.py` | Original Marimo application |
| `src/cintel/governance_app.py` | Interactive governance dashboard |
| `src/cintel/utils_system.py` | Shared system monitoring utility functions |
| `data/metadata_inventory.csv` | Project 03 synthetic metadata inventory |
| `data/governance_inventory_timeseries.csv` | Simulated weekly metadata snapshots |
| `data/governance_metrics_timeseries.csv` | Weekly governance summary metrics |
| `artifacts/governance_rolling_metrics.csv` | Generated governance rolling averages |
| `tests/test_governance_monitor.py` | Automated rolling monitoring tests |
| `docs/index.md` | Project documentation |

## Limitations

This project is an educational demonstration.

The governance data is synthetic and does not contain real patient or organizational performance information.

The 12-week historical sequence was generated to demonstrate monitoring techniques rather than document actual historical changes.

The rolling averages describe the simulated measurements and should not be interpreted as evidence of improvements within a real healthcare organization.

In a production environment, governance metrics would need to be collected consistently from authoritative data sources, with clearly defined measurement rules and ongoing validation.

## Project Documentation

The [hosted documentation site](https://ssowers2.github.io/cintel-04-rolling-monitoring/) is published using Zensical and GitHub Pages.

The documentation presents the project's data, methods, results, visualizations, interpretation, and conclusions.

The documentation source is maintained in [docs/index.md](docs/index.md).

## CI/CD and GitHub Actions

This project includes continuous integration and continuous deployment (CI/CD) workflows for checking project files and publishing documentation.

GitHub Actions include:

- [CI: Python and Documentation Checks](https://github.com/ssowers2/cintel-04-rolling-monitoring/actions/workflows/ci-python-zensical.yml)
- [CD: Documentation Deployment](https://github.com/ssowers2/cintel-04-rolling-monitoring/actions/workflows/deploy-zensical.yml)

## Developer Reference

Follow the [Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/) for detailed setup instructions and troubleshooting.

### Initialize and Update the Python Environment

With the project open in VS Code, run:

```shell
uvx pup-clean --delete
uv self update
uv python pin 3.14
uv python install
uv lock --upgrade
uv sync
uv audit
```

### Set Up and Run Git Hooks

Git hooks perform automated checks before commits.

```shell
uvx prek install --force
uvx prek update --freeze --cooldown-days 7

git add -A
uvx prek run --all-files
# Repeat if changes were made
uvx prek run --all-files
```

Review changed files before staging them, especially generated artifacts and local Marimo files.

### Run Common Chores

Run linters, formatters, type checks, tests, and build the documentation.

```shell
uv run ruff check . --fix
uv run ruff format .

uv run ty check
uv run python -m pytest
uv run python -m zensical build
```

### Git Add, Commit, and Push

After making useful changes, save your work to GitHub.

```shell
git status
git add README.md docs/index.md
git commit -m "Update Project 04 documentation"
git push
```

Adjust the files in `git add` to match the changes being committed.

## Developer Notes

- Use the **Up Arrow** and **Down Arrow** in the terminal to recall previous commands.
- Use **Ctrl + F** to search for text in a file.
- Save changes in VS Code before running project commands.
- Run formatting and linting checks before committing Python changes.

## Developer Tools

This project uses professional Python tools for development, testing, documentation, and code quality.

- [uv](https://docs.astral.sh/uv/) — Python environments and dependencies.
- [Polars](https://pola.rs/) — Data processing and rolling calculations.
- [Marimo](https://marimo.io/) — Reactive Python dashboard.
- [Altair](https://altair-viz.github.io/) — Interactive charting.
- [Ruff](https://docs.astral.sh/ruff/) — Python linting and formatting, configured in [.ruff.toml](.ruff.toml).
- [ty](https://docs.astral.sh/ty/) — Python type checking.
- [pytest](https://docs.pytest.org/) — Automated Python testing, configured in [.pytest.toml](.pytest.toml).
- [prek](https://prek.j178.dev/) — Git hooks and automated checks, configured in [prek.toml](prek.toml).
- [Zensical](https://zensical.org/) — Project documentation, configured in [zensical.toml](zensical.toml).

## Links

- [GitHub Repository](https://github.com/ssowers2/cintel-04-rolling-monitoring)
- [Hosted Documentation](https://ssowers2.github.io/cintel-04-rolling-monitoring/)
- [Project Documentation Source](docs/index.md)
- [Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/)
- [Citation](CITATION.cff)
- [License](LICENSE)
