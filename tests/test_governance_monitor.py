"""Test five-week rolling averages for governance monitoring."""

import polars as pl


def test_five_week_rolling_average() -> None:
    """Verify that rolling averages use five observations."""
    df = pl.DataFrame({"value": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0]})

    result = df.with_columns(
        pl.col("value").rolling_mean(window_size=5).alias("rolling_average")
    )

    actual = result["rolling_average"].to_list()

    assert actual[:4] == [None, None, None, None]
    assert actual[4] == 30.0
    assert actual[5] == 40.0


def test_governance_pipeline(tmp_path, monkeypatch) -> None:
    """Verify the governance pipeline creates correct rolling metrics."""
    from cintel import governance_monitor

    # Create a temporary input file with six weekly observations.
    input_file = tmp_path / "governance_metrics.csv"
    output_file = tmp_path / "governance_rolling_metrics.csv"

    df = pl.DataFrame(
        {
            "week": [
                "2026-09-07",
                "2026-09-14",
                "2026-09-21",
                "2026-09-28",
                "2026-10-05",
                "2026-10-12",
            ],
            "metadata_completeness_pct": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0],
            "ownership_pct": [50.0] * 6,
            "stewardship_pct": [60.0] * 6,
            "documentation_gaps_pct": [40.0] * 6,
        }
    )
    df.write_csv(input_file)

    # Redirect pipeline paths to temporary test files.
    monkeypatch.setattr(governance_monitor, "DATA_FILE", input_file)
    monkeypatch.setattr(governance_monitor, "OUTPUT_FILE", output_file)
    monkeypatch.setattr(governance_monitor, "ARTIFACTS_DIR", tmp_path)

    # Run the actual governance monitoring pipeline.
    governance_monitor.main()

    # Verify the generated output.
    assert output_file.exists()

    result = pl.read_csv(output_file)

    assert result.height == 6
    assert result["metadata_completeness_pct_rolling_mean"].to_list() == [
        None,
        None,
        None,
        None,
        30.0,
        40.0,
    ]
    assert result["ownership_pct_rolling_mean"][4] == 50.0
    assert result["stewardship_pct_rolling_mean"][4] == 60.0
    assert result["documentation_gaps_pct_rolling_mean"][4] == 40.0


def test_original_rolling_monitor(tmp_path, monkeypatch) -> None:
    """Verify the original system monitoring pipeline still works."""
    from cintel import rolling_monitor

    input_file = tmp_path / "system_metrics.csv"
    output_file = tmp_path / "rolling_metrics.csv"

    df = pl.DataFrame(
        {
            "timestamp": [
                "2026-11-01",
                "2026-11-02",
                "2026-11-03",
                "2026-11-04",
                "2026-11-05",
                "2026-11-06",
            ],
            "requests": [10, 20, 30, 40, 50, 60],
            "errors": [1, 2, 3, 4, 5, 6],
            "total_latency_ms": [100, 200, 300, 400, 500, 600],
        }
    )
    df.write_csv(input_file)

    monkeypatch.setattr(rolling_monitor, "DATA_FILE", input_file)
    monkeypatch.setattr(rolling_monitor, "OUTPUT_FILE", output_file)
    monkeypatch.setattr(rolling_monitor, "ARTIFACTS_DIR", tmp_path)

    rolling_monitor.main()

    assert output_file.exists()

    result = pl.read_csv(output_file)

    assert result.height == 6
    assert result["requests_rolling_mean"][4] == 30.0
    assert result["requests_rolling_mean"][5] == 40.0
