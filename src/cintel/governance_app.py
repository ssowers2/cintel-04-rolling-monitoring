"""Reactive Marimo dashboard for synthetic governance monitoring.

Project 04: Rolling Monitoring

Run locally:
    uv run marimo edit src/cintel/governance_app.py
    uv run marimo run src/cintel/governance_app.py

Data:
    data/governance_metrics_timeseries.csv

All historical observations are simulated for educational purposes.
"""

import marimo

__generated_with = "0.25.2"

app = marimo.App(width="full")


# === CELL 1: IMPORTS ===


@app.cell
def _():
    from pathlib import Path

    import altair as alt
    import marimo as mo
    import polars as pl

    return Path, alt, mo, pl


# === CELL 2: TITLE AND INTRODUCTION ===


@app.cell
def _(mo):
    mo.md("""
    # Metadata Completeness & Governance Readiness Monitor

    **Project 04 | Rolling Monitoring**

    This interactive dashboard explores how governance readiness
    changes across 12 weeks of simulated metadata observations.

    Use the rolling-window slider to compare weekly performance
    against smoothed trends.

    **Data source:** Synthetic healthcare metadata inventory
    carried forward from Project 03.

    **Note:** Historical measurements are simulated.
    No patient information is included.
    """)


# === CELL 3: LOAD GOVERNANCE DATA ===


@app.cell
def _(Path, pl):
    data_file = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "governance_metrics_timeseries.csv"
    )

    df = pl.read_csv(
        data_file,
        try_parse_dates=True,
    ).sort("week")

    return (df,)


# === CELL 4: ROLLING WINDOW SLIDER ===


@app.cell
def _(mo):
    window_size = mo.ui.slider(
        start=1,
        stop=10,
        value=5,
        step=1,
        label="Rolling window (weeks)",
    )

    window_size  # noqa: B018
    return (window_size,)


# === CELL 5: CALCULATE ROLLING AVERAGES ===


@app.cell
def _(df, pl, window_size):
    metrics = [
        "metadata_completeness_pct",
        "ownership_pct",
        "stewardship_pct",
        "documentation_gaps_pct",
    ]

    df_rolling = df.with_columns(
        [
            pl.col(metric)
            .rolling_mean(window_size=window_size.value)
            .round(2)
            .alias(f"{metric}_rolling_mean")
            for metric in metrics
        ]
    )

    return (df_rolling,)


# === CELL 6: GOVERNANCE METRIC SELECTOR ===


@app.cell
def _(mo):
    metric_selector = mo.ui.dropdown(
        options={
            "Metadata completeness": "metadata_completeness_pct",
            "Ownership coverage": "ownership_pct",
            "Stewardship coverage": "stewardship_pct",
            "Documentation gaps": "documentation_gaps_pct",
        },
        value="Metadata completeness",
        label="Select governance metric",
    )

    metric_selector  # noqa: B018
    return (metric_selector,)


# === CELL 7: INTERACTIVE LINE CHART ===


@app.cell
def _(alt, df_rolling, metric_selector, mo, pl, window_size):
    selected_metric = metric_selector.value

    chart_data = (
        df_rolling.select(
            [
                "week",
                selected_metric,
                f"{selected_metric}_rolling_mean",
            ]
        )
        .rename(
            {
                selected_metric: "Weekly value",
                f"{selected_metric}_rolling_mean": "Rolling average",
            }
        )
        .unpivot(
            index="week",
            variable_name="Series",
            value_name="Percentage",
        )
        .filter(pl.col("Percentage").is_not_null())
        .to_pandas()
    )

    chart = (
        alt.Chart(chart_data)
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X("week:T", title="Week"),
            y=alt.Y(
                "Percentage:Q",
                title="Percentage (%)",
                scale=alt.Scale(domain=[0, 100]),
            ),
            color=alt.Color(
                "Series:N",
                title="Metric",
            ),
            tooltip=[
                alt.Tooltip("week:T", title="Week"),
                alt.Tooltip("Series:N", title="Series"),
                alt.Tooltip(
                    "Percentage:Q",
                    title="Percentage",
                    format=".2f",
                ),
            ],
        )
        .properties(
            title=(f"Weekly Performance vs. {window_size.value}-Week Rolling Average"),
            width=650,
            height=360,
        )
        .interactive()
    )

    mo.ui.altair_chart(chart)


# === CELL 8: GOVERNANCE DATA TABLE ===


@app.cell
def _(df_rolling, mo):
    mo.vstack(
        [
            mo.md("## Weekly Governance Monitoring Data"),
            mo.ui.table(df_rolling),
        ]
    )


# === CELL 9: INTERPRETATION ===


@app.cell
def _(mo):
    mo.md("""
    ## Understanding the Results

    **Weekly values** show governance performance at each
    simulated observation.

    **Rolling averages** smooth short-term fluctuations to
    make longer-term trends easier to identify.

    The first observations have no rolling average until
    enough weeks are available to fill the selected window.

    ### Governance Interpretation

    - **Metadata completeness:** Measures the percentage of
      assets with required metadata fields populated.
    - **Ownership coverage:** Measures assets with an
      assigned data owner.
    - **Stewardship coverage:** Measures assets with an
      assigned data steward.
    - **Documentation gaps:** Measures assets missing a
      description or business definition.

    Higher completeness, ownership, and stewardship percentages
    generally indicate stronger governance readiness.

    Lower documentation-gap percentages indicate improvement.

    These results are simulated and should not be interpreted
    as actual organizational performance.
    """)


# === CELL 10: CLOSING ===


@app.cell
def _(mo):
    mo.md("""
    ---

    **Continuous Intelligence | Project 04**

    Metadata Completeness & Governance Readiness Monitor

    Built with Python, Polars, Altair, and Marimo.
    """)


# === CONDITIONAL EXECUTION GUARD ===


if __name__ == "__main__":
    app.run()
