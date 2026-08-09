from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

COLORS = ["#2563EB", "#7C3AED", "#059669", "#EA580C", "#DB2777", "#0891B2", "#CA8A04"]


def _title(value: str) -> str:
    return str(value).replace("_", " ").replace("-", " ").title()


def _base(title: str, subtitle: str | None = None) -> dict[str, Any]:
    config: dict[str, Any] = {
        "chart": {"backgroundColor": "#FFFFFF", "plotBackgroundColor": "#FFFFFF", "borderRadius": 8, "animation": True},
        "colors": COLORS,
        "title": {"text": title, "style": {"color": "#111827", "fontWeight": "600"}},
        "credits": {"enabled": False},
        "legend": {"itemStyle": {"color": "#374151"}},
        "xAxis": {"labels": {"style": {"color": "#4B5563"}}, "gridLineColor": "#E5E7EB"},
        "yAxis": {"labels": {"style": {"color": "#4B5563"}}, "gridLineColor": "#E5E7EB"},
        "tooltip": {"shared": True, "backgroundColor": "#FFFFFF", "borderColor": "#D1D5DB", "style": {"color": "#111827"}},
    }
    if subtitle:
        config["subtitle"] = {"text": subtitle, "style": {"color": "#6B7280"}}
    return config


def _histogram(df: pd.DataFrame, column: str) -> dict[str, Any] | None:
    values = pd.to_numeric(df[column], errors="coerce").dropna()
    if values.empty or values.nunique() < 2:
        return None
    counts, edges = np.histogram(values, bins=min(12, max(5, int(np.sqrt(len(values))))))
    config = _base(f"Distribution of {_title(column)}", "Dynamic Highcharts histogram")
    config.update({"chart": {"type": "column", "backgroundColor": "#FFFFFF", "animation": True}, "xAxis": {"categories": [f"{edges[i]:.2f}–{edges[i + 1]:.2f}" for i in range(len(counts))], "title": {"text": _title(column)}}, "yAxis": {"title": {"text": "Frequency"}}, "series": [{"type": "column", "name": "Frequency", "data": counts.tolist(), "color": COLORS[0]}]})
    return config


def _categorical(df: pd.DataFrame, column: str) -> dict[str, Any] | None:
    counts = df[column].astype(str).replace("nan", "Missing").value_counts().head(12)
    if counts.empty:
        return None
    config = _base(f"Top values of {_title(column)}")
    config.update({"chart": {"type": "bar", "backgroundColor": "#FFFFFF", "animation": True}, "xAxis": {"categories": counts.index.astype(str).tolist(), "title": {"text": None}}, "yAxis": {"title": {"text": "Records"}}, "series": [{"type": "bar", "name": "Records", "data": counts.tolist()}]})
    return config


def _pie(df: pd.DataFrame, column: str) -> dict[str, Any] | None:
    counts = df[column].astype(str).replace("nan", "Missing").value_counts().head(8)
    if counts.empty:
        return None
    config = _base(f"Composition of {_title(column)}")
    config.update({"chart": {"type": "pie", "backgroundColor": "#FFFFFF", "animation": True}, "series": [{"type": "pie", "name": "Records", "data": [{"name": str(name), "y": int(value)} for name, value in counts.items()]}]})
    return config


def _trend(df: pd.DataFrame, date_column: str, numeric_column: str) -> dict[str, Any] | None:
    frame = pd.DataFrame({"date": pd.to_datetime(df[date_column], errors="coerce"), "value": pd.to_numeric(df[numeric_column], errors="coerce")}).dropna()
    if frame.empty:
        return None
    grouped = frame.groupby(frame["date"].dt.to_period("M"))["value"].mean().reset_index()
    config = _base(f"{_title(numeric_column)} over time", f"Grouped by {_title(date_column)}")
    config.update({"chart": {"type": "spline", "backgroundColor": "#FFFFFF", "animation": True}, "xAxis": {"categories": [str(v) for v in grouped["date"]], "title": {"text": _title(date_column)}}, "yAxis": {"title": {"text": _title(numeric_column)}}, "series": [{"type": "spline", "name": _title(numeric_column), "data": grouped["value"].round(3).tolist()}]})
    return config


def _scatter(df: pd.DataFrame, x_column: str, y_column: str) -> dict[str, Any] | None:
    frame = df[[x_column, y_column]].apply(pd.to_numeric, errors="coerce").dropna().head(2000)
    if len(frame) < 2:
        return None
    config = _base(f"{_title(y_column)} vs {_title(x_column)}")
    config.update({"chart": {"type": "scatter", "zoomType": "xy", "backgroundColor": "#FFFFFF", "animation": True}, "xAxis": {"title": {"text": _title(x_column)}}, "yAxis": {"title": {"text": _title(y_column)}}, "series": [{"type": "scatter", "name": "Observations", "data": [[float(x), float(y)] for x, y in frame.itertuples(index=False, name=None)]}]})
    return config


def build_dynamic_charts(df: pd.DataFrame, schema: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    numeric = [item["column"] for item in schema if item["logical_type"] == "numeric"]
    categorical = [item["column"] for item in schema if item["logical_type"] == "categorical"]
    dates = [item["column"] for item in schema if item["logical_type"] == "datetime"]
    charts = {"Distributions": [], "Segments": [], "Trends": [], "Relationships": []}
    for column in numeric:
        chart = _histogram(df, column)
        if chart:
            charts["Distributions"].append(chart)
    for column in categorical:
        for builder in (_categorical, _pie):
            chart = builder(df, column)
            if chart:
                charts["Segments"].append(chart)
    for date_column in dates:
        for numeric_column in numeric[:4]:
            chart = _trend(df, date_column, numeric_column)
            if chart:
                charts["Trends"].append(chart)
    for index, x_column in enumerate(numeric[:4]):
        for y_column in numeric[index + 1:index + 4]:
            chart = _scatter(df, x_column, y_column)
            if chart:
                charts["Relationships"].append(chart)
    return charts
