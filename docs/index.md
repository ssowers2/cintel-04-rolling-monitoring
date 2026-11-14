# Rolling Monitoring of System Metrics

Continuous Intelligence | Project 04 | Experiment Report

**Author:** Sabriya Sowers

**Date:** November 2026

## Overview

This project investigates how rolling statistics
can reveal patterns in system behavior over time.

Individual measurements may fluctuate.
Rolling analysis provides a way to examine
recent behavior while reducing short-term variation.

For this project, I completed a small technical
experiment by increasing the rolling window size
from 3 to 5 observations.

After completing the experiment, I plan to customize
the project into a Metadata Completeness &
Governance Readiness Monitor.

## Data

The dataset used in my pipeline contains 60
time-series observations.

Each observation includes:

- Timestamp.
- Number of requests.
- Number of errors.
- Total latency in milliseconds.

[View Project Dataset](https://github.com/ssowers2/cintel-04-rolling-monitoring/blob/main/data/system_metrics_timeseries.csv)

## Methods

The pipeline uses Polars to sort observations
by timestamp and calculate rolling averages.

Rolling averages are calculated for:

- Requests.
- Errors.
- Total latency.

The original pipeline used a rolling window
of 3 observations.

For my experiment, I increased the window
size to 5 observations.

Each completed window now summarizes the
current observation and the four preceding
observations.

The first four rows do not have a complete
five-observation window available for
calculating the rolling averages.

## Results

I ran the pipeline before and after making
my technical modification.

Both runs successfully processed 60
time-series records.

The original pipeline used a window size
of 3, while the modified pipeline used
a window size of 5.

### Pipeline Execution Results

| Measurement | Original | Modified |
|-------------|----------|----------|
| Window size | 3 | 5 |
| Records processed | 60 | 60 |
| Pipeline execution | Successful | Successful |
| Output file | rolling_metrics.csv | rolling_metrics.csv |

The modified pipeline successfully generated
updated results in `artifacts/rolling_metrics.csv`.

The execution logs confirmed that the new
window size was applied.

However, I have not yet compared the
calculated rolling-average values to
confirm whether the results became smoother.

[View Rolling Monitoring Results](https://github.com/ssowers2/cintel-04-rolling-monitoring/blob/main/artifacts/rolling_metrics.csv)

## Interpretation

The experiment demonstrated how changing
a single setting affects the rolling
monitoring calculation.

Increasing the window size from 3 to 5
means that each rolling average includes
more observations.

A larger window generally reduces the
impact of short-term fluctuations and
can make longer-term trends easier to see.

However, it may also respond more slowly
to sudden changes in system performance.

A comparison of the original and modified
CSV values would be needed to confirm
the actual smoothing effect in this dataset.

## Limitations

Rolling averages smooth short-term variation,
but may delay detection of sudden changes.

The original pipeline used a fixed
three-observation window, while my modified
pipeline uses five observations.

Different window sizes may reveal
different patterns.

The experiment confirmed successful execution
but did not include a numerical comparison
of the original and modified rolling averages.

The pipeline does not yet classify anomalies
or issue monitoring alerts.

## Custom Modifications

### Experiment: Increasing the Rolling Window Size

**What I changed:**

I changed the rolling window size from 3 to 5
observations in `src/cintel/rolling_monitor.py`.

**Why I chose this modification:**

I wanted to understand how increasing the
window size would affect rolling averages
and the ability to identify trends in
system performance.

**My prediction:**

If I increase the rolling window size
from 3 to 5, I expect the rolling averages
to be smoother because each calculation
will include more observations.

**What actually happened:**

I ran the original pipeline with a window
size of 3 and then ran it again with a
window size of 5.

Both runs successfully processed 60
time-series records.

The modified pipeline generated updated
results in `artifacts/rolling_metrics.csv`.

The execution logs confirmed that the
new window size was applied successfully.

I have not yet compared the calculated
values to confirm the smoothing effect.

**What I learned:**

I learned that the rolling window size
determines how many observations are
included in each average.

A larger window can help smooth
short-term fluctuations, but it may
also respond more slowly to sudden
changes in the data.

### Modified Code

The original setting was:

```python
WINDOW_SIZE: int = 3
```

I changed it to:

```python
WINDOW_SIZE: int = 5
```

This was the only technical modification
made for the controlled experiment.

## Planned Project Customization

### Metadata Completeness & Governance Readiness Monitor

After completing the rolling-window experiment,
I plan to customize this project into a
**Metadata Completeness & Governance Readiness Monitor**.

This builds on my previous project, which
measured data governance readiness at
a single point in time.

For Project 04, I want to add a time-based
component to monitor how those measurements
change over time.

Using synthetic healthcare metadata,
I plan to track:

- Metadata completeness.
- Data ownership assignments.
- Data stewardship assignments.
- Documentation gaps.

I will use rolling analytics to examine
changes in these metrics over time.

The goal is to identify trends,
monitor improvements, and highlight
areas that may need additional data
governance attention.

This customization will demonstrate
how continuous monitoring can support
data governance and data quality improvement.

## Conclusion

Rolling monitoring adds a temporal
perspective to system analysis.

My experiment demonstrated how changing
the rolling window size affects the number
of observations included in each calculation.

Both versions of the pipeline executed
successfully, confirming that my
technical modification was applied.

This project also provides a foundation
for my planned data governance monitor,
which will use rolling analytics to
evaluate metadata completeness and
governance readiness over time.

## Documentation Index

- **Home** - this landing page.
- [Project Instructions](project-instructions.md)
- [Glossary](glossary.md)
- [API](api.md)
- [Reactive App](./app/index.html)

## Project Links

- [GitHub Repository](https://github.com/ssowers2/cintel-04-rolling-monitoring)
- [Rolling Monitoring Pipeline](https://github.com/ssowers2/cintel-04-rolling-monitoring/blob/main/src/cintel/rolling_monitor.py)
- [Project Dataset](https://github.com/ssowers2/cintel-04-rolling-monitoring/blob/main/data/system_metrics_timeseries.csv)
- [Results and Artifacts](https://github.com/ssowers2/cintel-04-rolling-monitoring/tree/main/artifacts)
- [Published Documentation](https://ssowers2.github.io/cintel-04-rolling-monitoring/)

## Project Resources

- [Project Instructions](project-instructions.md)
- [Professional Python Guide](https://denisecase.github.io/pro-analytics-02/)
- [Professional Python Project Explainer](https://pup-pack.github.io/professional-python-project-explainer/)
- [Suggested Datasets](https://denisecase.github.io/pro-analytics-02/reference/datasets/cintel/)
