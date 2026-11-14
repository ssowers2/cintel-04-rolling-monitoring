"""Reactive Marimo dashboard for synthetic governance monitoring.

Project 04: Rolling Monitoring

Run locally:
    uv run marimo edit src/cintel/governance_app.py
    uv run marimo run src/cintel/governance_app.py

For a static WASM export, publish governance_metrics_timeseries.csv in the
app's public/ directory and make Polars and Altair available in the browser.

All historical observations are simulated for educational purposes.
"""

import marimo

__generated_with = "0.25.2"

app = marimo.App(width="full")


@app.cell
async def _():
    import sys

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(["polars", "altair"])

    import altair as alt
    import marimo as mo
    import polars as pl

    return alt, mo, pl, sys


@app.cell
def _(mo):
    mo.md("""
    # Metadata Completeness & Governance Readiness Monitor

    **Project 04 | Rolling Monitoring**

    This interactive dashboard explores how governance readiness changes
    across 12 weeks of simulated metadata observations.

    Use the rolling-window slider to compare weekly performance against
    smoothed trends.

    **Data source:** Synthetic healthcare metadata inventory carried forward
    from Project 03.

    **Note:** Historical measurements are simulated. No patient information
    is included.
    """)


@app.cell
def _(mo, pl, sys):
    notebook_location = mo.notebook_location()
    if notebook_location is None:
        raise RuntimeError("Unable to determine notebook location.")

    filename = "governance_metrics_timeseries.csv"
    if sys.platform == "emscripten":
        from pyodide.http import open_url  # ty: ignore[unresolved-import]

        data_url = notebook_location / "public" / filename
        df = pl.read_csv(open_url(str(data_url)), try_parse_dates=True)
    else:
        data_path = notebook_location.parents[1] / "data" / filename
        df = pl.read_csv(data_path, try_parse_dates=True)

    df = df.sort("week")
    return (df,)


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
        .with_columns(pl.col("week").cast(pl.String))
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
        .to_dicts()
    )

    chart = (
        alt.Chart(alt.Data(values=chart_data))
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X("week:T", title="Week"),
            y=alt.Y(
                "Percentage:Q",
                title="Percentage (%)",
                scale=alt.Scale(domain=[0, 100]),
            ),
            color=alt.Color("Series:N", title="Metric"),
            tooltip=[
                alt.Tooltip("week:T", title="Week"),
                alt.Tooltip("Series:N", title="Series"),
                alt.Tooltip("Percentage:Q", title="Percentage", format=".2f"),
            ],
        )
        .properties(
            title=f"Weekly Performance vs. {window_size.value}-Week Rolling Average",
            width=650,
            height=360,
        )
        .interactive()
    )

    mo.ui.altair_chart(chart)


@app.cell
def _(df_rolling, mo):
    mo.vstack(
        [
            mo.md("## Weekly Governance Monitoring Data"),
            mo.ui.table(df_rolling),
        ]
    )


@app.cell
def _(mo):
    mo.md("""
    ## Understanding the Results

    **Weekly values** show governance performance at each simulated observation.

    **Rolling averages** smooth short-term fluctuations to make longer-term
    trends easier to identify.

    The first observations have no rolling average until enough weeks are
    available to fill the selected window.

    ### Governance Interpretation

    - **Metadata completeness:** Percentage of assets with required metadata.
    - **Ownership coverage:** Assets with an assigned data owner.
    - **Stewardship coverage:** Assets with an assigned data steward.
    - **Documentation gaps:** Assets missing a description or business definition.

    Higher completeness, ownership, and stewardship percentages generally
    indicate stronger governance readiness. Lower documentation-gap
    percentages indicate improvement.

    These results are simulated and do not represent actual organizational
    performance.
    """)


@app.cell
def _(mo):
    mo.md("""
    ---

    **Continuous Intelligence | Project 04**

    Metadata Completeness & Governance Readiness Monitor

    Built with Python, Polars, Altair, and Marimo.
    """)


if __name__ == "__main__":
    app.run()
