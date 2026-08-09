from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def _title(value: str) -> str:
    return str(value).replace("_", " ").replace("-", " ").title()


def _base(title: str, subtitle: str | None = None) -> dict[str, Any]:
    config: dict[str, Any] = {
        "chart": {"animation": False},
        "title": {"text": title},
        "credits": {"enabled": False},
        "tooltip": {"shared": True},
    }
    if subtitle:
        config["subtitle"] = {"text": subtitle}
    return config


def _histogram(df: pd.DataFrame, column: str) -> dict[str, Any] | None:
    values = pd.to_numeric(df[column], errors="coerce").dropna()
    if values.empty or values.nunique() < 2:
        return None
    bins = min(12, max(5, int(np.sqrt(len(values)))))
    counts, edges = np.histogram(values, bins=bins)
    categories = [f"{edges[i]:.2f}–{edges[i + 1]:.2f}" for i in range(len(counts))]
    config = _base(f"Distribution of {_title(column)}", "Dynamic Highcharts histogram")
    config.update({
        "chart": {"type": "column", "animation": False},
        "xAxis": {"categories": categories, "title": {"text": _title(column)}},
        "yAxis": {"title": {"text": "Frequency"}},
        "series": [{"type": "column", "name": "Frequency", "data": counts.tolist()}],
    })
    return config


def _categorical(df: pd.DataFrame, column: str) -> dict[str, Any] | None:
    counts = df[column].astype(str).replace("nan", "Missing").value_counts().head(12)
    if counts.empty:
        return None
    config = _base(f"Top values of {_title(column)}")
    config.update({
        "chart": {"type": "bar", "animation": False},
        "xAxis": {"categories": counts.index.tolist(), "title": {"text": None}},
        "yAxis": {"title": {"text": "Records"}},
        "series": [{"type": "bar", "name": "Records", "data": counts.tolist()}],
    })
    return config


def _pie(df: pd.DataFrame, column: str) -> dict[str, Any] | None:
    counts = df[column].astype(str).replace("nan", "Missing").value_counts().head(8)
    if counts.empty:
        return None
    config = _base(f"Composition of {_title(column)}")
    config.update({
        "chart": {"type": "pie", "animation": False},
        "series": [{
            "type": "pie",
            "name": "Records",
            "data": [{"name": str(name), "y": int(value)} for name, value in counts.items()],
        }],
    })
    return config


def _trend(df: pd.DataFrame, date_column: str, numeric_column: str) -> dict[str, Any] | None:
    dates = pd.to_datetime(df[date_column], errors="coerce")
    values = pd.to_numeric(df[numeric_column], errors="coerce")
    frame = pd.DataFrame({"date": dates, "value": values}).dropna()
    if frame.empty:
        return None
    grouped = frame.groupby(frame["date"].dt.to_period("M"))["value"].mean().reset_index()
    categories = [str(value) for value in grouped["date"]]
    config = _base(f"{_title(numeric_column)} over time", f"Grouped by {_title(date_column)}")
    config.update({
        "chart": {"type": "spline", "animation": False},
        "xAxis": {"categories": categories, "title": {"text": _title(date_column)}},
        "yAxis": {"title": {"text": _title(numeric_column)}},
        "series": [{"type": "spline", "name": _title(numeric_column), "data": grouped["value"].round(3).tolist()}],
    })
    return config


def _scatter(df: pd.DataFrame, x_column: str, y_column: str) -> dict[str, Any] | None:
    frame = df[[x_column, y_column]].apply(pd.to_numeric, errors="coerce").dropna().head(2000)
    if len(frame) < 2:
        return None
    config = _base(f"{_title(y_column)} vs {_title(x_column)}")
    config.update({
        "chart": {"type": "scatter", "zoomType": "xy", "animation": False},
        "xAxis": {"title": {"text": _title(x_column)}},
        "yAxis": {"title": {"text": _title(y_column)}},
        "series": [{
            "type": "scatter",
            "name": "Observations",
            "data": [[float(x), float(y)] for x, y in frame.itertuples(index=False, name=None)],
        }],
    })
    return config


def build_dynamic_charts(df: pd.DataFrame, schema: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    numeric = [item["column"] for item in schema if item["logical_type"] == "numeric"]
    categorical = [item["column"] for item in schema if item["logical_type"] == "categorical"]
    datetime_columns = [item["column"] for item in schema if item["logical_type"] == "datetime"]
    charts: dict[str, list[dict[str, Any]]] = {
        "Distributions": [],
        "Segments": [],
        "Trends": [],
        "Relationships": [],
    }
    for column in numeric:
        chart = _histogram(df, column)
        if chart:
            charts["Distributions"].append(chart)
    for column in categorical:
        for builder in (_categorical, _pie):
            chart = builder(df, column)
            if chart:
                charts["Segments"].append(chart)
    if datetime_columns and numeric:
        for date_column in datetime_columns:
            for numeric_column in numeric[:4]:
                chart = _trend(df, date_column, numeric_column)
                if chart:
                    charts["Trends"].append(chart)
    if len(numeric) >= 2:
        for index, x_column in enumerate(numeric[:4]):
            for y_column in numeric[index + 1 : index + 4]:
                chart = _scatter(df, x_column, y_column)
                if chart:
                    charts["Relationships"].append(chart)
    return charts
