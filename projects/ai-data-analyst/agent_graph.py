from __future__ import annotations

from typing import Any, TypedDict

import pandas as pd
from langgraph.graph import END, StateGraph


class AnalystState(TypedDict, total=False):
    dataframe: pd.DataFrame
    schema: list[dict[str, Any]]
    report_plan: list[str]
    analysis: dict[str, Any]
    insights: list[str]
    warnings: list[str]


def _type_of(series: pd.Series) -> str:
    if pd.api.types.is_bool_dtype(series):
        return "boolean"
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    parsed = pd.to_datetime(series, errors="coerce")
    if series.dtype == "object" and parsed.notna().mean() >= 0.85:
        return "datetime"
    if series.nunique(dropna=True) <= min(20, max(5, len(series) // 20)):
        return "categorical"
    return "text"


def source_node(state: AnalystState) -> AnalystState:
    df = state["dataframe"].copy()
    return {"dataframe": df, "warnings": []}


def schema_node(state: AnalystState) -> AnalystState:
    df = state["dataframe"]
    schema = []
    for column in df.columns:
        series = df[column]
        logical_type = _type_of(series)
        if logical_type == "datetime" and not pd.api.types.is_datetime64_any_dtype(series):
            df[column] = pd.to_datetime(series, errors="coerce")
        schema.append({
            "column": str(column),
            "logical_type": logical_type,
            "dtype": str(series.dtype),
            "missing_pct": round(float(series.isna().mean() * 100), 2),
            "unique_values": int(series.nunique(dropna=True)),
        })
    return {"dataframe": df, "schema": schema}


def planner_node(state: AnalystState) -> AnalystState:
    kinds = {item["logical_type"] for item in state["schema"]}
    plan = ["overview", "data_quality"]
    if "numeric" in kinds:
        plan.append("distributions")
    if "categorical" in kinds:
        plan.append("segment_comparison")
    if "datetime" in kinds and "numeric" in kinds:
        plan.append("time_trend")
    numeric_count = sum(item["logical_type"] == "numeric" for item in state["schema"])
    if numeric_count >= 2:
        plan.append("relationships")
    return {"report_plan": plan}


def analysis_node(state: AnalystState) -> AnalystState:
    df = state["dataframe"]
    numeric = [item["column"] for item in state["schema"] if item["logical_type"] == "numeric"]
    categorical = [item["column"] for item in state["schema"] if item["logical_type"] == "categorical"]
    missing = {item["column"]: item["missing_pct"] for item in state["schema"] if item["missing_pct"] > 0}
    summary = {column: {key: float(value) for key, value in df[column].describe().to_dict().items()} for column in numeric}
    correlations = df[numeric].corr().round(3).to_dict() if len(numeric) >= 2 else {}
    category_counts = {column: df[column].astype(str).value_counts().head(10).to_dict() for column in categorical}
    return {"analysis": {"numeric_summary": summary, "correlations": correlations, "category_counts": category_counts, "missingness": missing}}


def insight_node(state: AnalystState) -> AnalystState:
    df = state["dataframe"]
    analysis = state["analysis"]
    insights = [f"The dataset contains {len(df):,} rows and {len(df.columns):,} columns."]
    insights.append(f"The autonomous planner selected {len(state['report_plan'])} report modules.")
    missing = analysis["missingness"]
    if missing:
        column = max(missing, key=missing.get)
        insights.append(f"The highest missingness is in '{column}' at {missing[column]:.1f}%.")
    else:
        insights.append("No missing values were detected.")
    if analysis["correlations"]:
        insights.append("A relationship report was selected because multiple numeric fields were detected.")
    return {"insights": insights}


def review_node(state: AnalystState) -> AnalystState:
    warnings = list(state.get("warnings", []))
    if not state.get("report_plan"):
        warnings.append("No report modules were selected.")
    if not state.get("schema"):
        warnings.append("Schema analysis returned no columns.")
    return {"warnings": warnings}


def build_graph():
    graph = StateGraph(AnalystState)
    graph.add_node("source", source_node)
    graph.add_node("schema", schema_node)
    graph.add_node("planner", planner_node)
    graph.add_node("analysis", analysis_node)
    graph.add_node("insight", insight_node)
    graph.add_node("review", review_node)
    graph.set_entry_point("source")
    graph.add_edge("source", "schema")
    graph.add_edge("schema", "planner")
    graph.add_edge("planner", "analysis")
    graph.add_edge("analysis", "insight")
    graph.add_edge("insight", "review")
    graph.add_edge("review", END)
    return graph.compile()


def run_agentic_analysis(df: pd.DataFrame) -> AnalystState:
    return build_graph().invoke({"dataframe": df})
