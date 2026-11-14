# cintel-04-rolling-monitoring

[![Python 3.14](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](pyproject.toml)
[![CI](https://github.com/ssowers2/cintel-04-rolling-monitoring/actions/workflows/ci-python-zensical.yml/badge.svg)](https://github.com/ssowers2/cintel-04-rolling-monitoring/actions/workflows/ci-python-zensical.yml)
[![Documentation](https://img.shields.io/badge/docs-site-blue?logo=github)](https://ssowers2.github.io/cintel-04-rolling-monitoring/)

[![uv managed](https://img.shields.io/badge/uv-managed-DE5FE9)](https://docs.astral.sh/uv/)
[![ty type checked](https://img.shields.io/badge/ty-type_checked-2F80ED)](https://docs.astral.sh/ty/)
[![Zensical docs](https://img.shields.io/badge/Zensical-docs-purple)](https://zensical.org/)
[![MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

> Monitor time-series measurements using rolling statistics.

## Project Overview

**Author:** Sabriya Sowers

**Date:** November 2026

This project introduces rolling monitoring.

The goal is to study measurements over time
and use rolling statistics to reveal changes in system behavior.

The project is configured in
[pyproject.toml](pyproject.toml).

## Data

The example uses time-series system metrics from `data/`.

The pipeline processes 60 time-series records.

Each observation includes:

- `timestamp` - time of observation.
- `requests` - number of requests handled.
- `errors` - number of failed requests.
- `total_latency_ms` - total response time in milliseconds.

## Approach

The pipeline uses Polars to:

1. Read and order observations by timestamp.
2. Calculate rolling averages over a defined window.
3. Save the monitoring results for interpretation.

The original pipeline uses a rolling window of 3 observations.
For my experiment, I increased the window size to 5 observations.

Explore these project components:

- [pyproject.toml](pyproject.toml) - project configuration and dependencies.
- [src/cintel/rolling_monitor.py](src/cintel/rolling_monitor.py) - rolling monitoring pipeline.
- [data/](data/) - time-series data.
- [artifacts/](artifacts/) - generated monitoring results.
- [tests/](tests/) - automated tests.
- [.github/workflows/](.github/workflows/) - automated checks and documentation deployment.
- [docs/](docs/) - project documentation.

## Run the Project

Follow the [Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/)
to set up your machine and project environment.

From a VS Code terminal in the project root:

```shell
uv run python -m cintel.rolling_monitor
```

## Run the Reactive App

From a VS Code terminal in the project root
(hit CTRL + C to quit):

```shell
uv run marimo run src/cintel/app.py
```

## Results

The pipeline calculates rolling averages and writes
`artifacts/rolling_metrics.csv`.

Review the rolling measurements to understand
how smoothing can reveal trends and reduce short-term variation.

Successful execution produces a terminal message:

```text
========================
Pipeline executed successfully!
========================
```

A `project.log` file is created in the project root.

This confirms that the Python pipeline executes
and the logging system works.

## Custom Modifications

### Experiment: Increasing the Rolling Window Size

**What I changed:**

For this experiment, I modified the rolling window size in
`src/cintel/rolling_monitor.py` from 3 to 5 observations.

**Why I chose this modification:**

I wanted to understand how increasing the window size affects
rolling averages and the ability to identify trends in system
performance.

**My prediction:**

I predicted that increasing the window size would produce
smoother rolling averages and reduce the impact of short-term
fluctuations because more observations would be included
in each calculation.

**What actually happened:**

Both versions of the pipeline executed successfully and
processed 60 time-series records.

The original pipeline used a window size of 3,
while the modified pipeline used a window size of 5.

The modified pipeline generated updated results in
`artifacts/rolling_metrics.csv`.

The calculated values have not yet been compared
to confirm the smoothing effect.

**What I learned:**

I learned that changing the window size affects how rolling
averages are calculated.

A larger window includes more observations, which can help
smooth short-term fluctuations but may also delay the
detection of sudden changes.

### Experiment Summary

| Measurement | Original | Modified |
|-------------|----------|----------|
| Window size | 3 | 5 |
| Records processed | 60 | 60 |
| Pipeline execution | Successful | Successful |
| Output file | rolling_metrics.csv | rolling_metrics.csv |

**Modified Code:**

```python
WINDOW_SIZE: int = 5
```

The modification demonstrates how changing one setting
can affect time-series monitoring.

## Planned Project Customization

After completing the rolling-window experiment, I plan
to customize this project into a **Metadata Completeness
& Governance Readiness Monitor**.

This project builds on my previous work with data governance
metrics by adding a time-based monitoring component.

Using synthetic healthcare metadata, I plan to track:

- Metadata completeness.
- Data ownership assignments.
- Data stewardship assignments.
- Documentation gaps.

The goal is to use rolling analytics to monitor governance
readiness over time, identify trends, and highlight areas
that may need additional attention.

This customization will demonstrate how rolling monitoring
can support data governance and data quality improvement.

## Verification

Run the automated tests:

```shell
uv run pytest
```

## Project Documentation

The [hosted documentation site](https://ssowers2.github.io/cintel-04-rolling-monitoring/)
is published using Zensical and GitHub Pages.

The documentation site is used to present the project report,
covering sections such as data, methods, results,
visualizations, interpretation, and conclusions.

The experiment is also documented in
[docs/index.md](docs/index.md).

## CI/CD and GitHub Actions

This project includes continuous integration and continuous
deployment (CI/CD) to check project files and publish the docs.

GitHub Actions include:

- [CI: Python and Documentation Checks](https://github.com/ssowers2/cintel-04-rolling-monitoring/actions/workflows/ci-python-zensical.yml)
- [CD: Documentation Deployment](https://github.com/ssowers2/cintel-04-rolling-monitoring/actions/workflows/deploy-zensical.yml)

## Developer Reference

Follow the
[Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/)
for **detailed instructions and troubleshooting**.

### Initialize and Update the Python Environment

With the project open in VS Code, open a VS Code terminal.
Paste each command and hit Enter or Return after to run it.

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

Set up and run the Git hooks to perform
basic checks automatically before
any changes get pushed to GitHub.

In the VS Code terminal,
paste each command and hit Enter or Return after to run it.

```shell
uvx prek install --force
uvx prek update --freeze --cooldown-days 7

git add -A
uvx prek run --all-files
# repeat if changes were made
uvx prek run --all-files
```

### Run Common Chores

Run linters, formatters, type checks, tests, and
build the documentation.

```shell
uv run ruff check . --fix
uv run ruff format .

uv run ty check
uv run python -m pytest
uv run python -m zensical build
```

### Git add-commit-push to GitHub

After making useful changes, save your work to GitHub.

```shell
git add -A
git commit -m "describe your changes in quotes"
git push -u origin main
```

## Developer Notes

- Use the **UP ARROW** and **DOWN ARROW** in the terminal to scroll through past commands.
- Use `CTRL+F` to find (and replace) text within a file.

## Developer Tools

This project uses professional Python tools to support development,
testing, documentation, and code quality.

- [uv](https://docs.astral.sh/uv/) - Python environments and dependencies.
- [Ruff](https://docs.astral.sh/ruff/) - Python linting and formatting, configured in [.ruff.toml](.ruff.toml).
- [ty](https://docs.astral.sh/ty/) - Python type checking.
- [pytest](https://docs.pytest.org/) - automated Python testing, configured in [.pytest.toml](.pytest.toml).
- [prek](https://prek.j178.dev/) - Git hooks and automated checks, configured in [prek.toml](prek.toml).
- [Zensical](https://zensical.org/) - project documentation, configured in [zensical.toml](zensical.toml).

## Links

- [GitHub Repository](https://github.com/ssowers2/cintel-04-rolling-monitoring)
- [Hosted Documentation](https://ssowers2.github.io/cintel-04-rolling-monitoring/)
- [Project Documentation Source](docs/index.md)
- [Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/)
- [Citation](CITATION.cff)
- [License](LICENSE)
