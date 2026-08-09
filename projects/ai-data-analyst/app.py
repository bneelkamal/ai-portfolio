from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from agent_graph import run_agentic_analysis

st.set_page_config(page_title="Agentic AI Data Analyst", page_icon="📊", layout="wide")
st.title("Agentic AI Data Analyst")
st.caption("Drop a CSV or Excel file. The agent graph profiles the data, selects useful reports, and presents the evidence.")

with st.sidebar:
    st.header("Input")
    uploaded = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"])
    st.caption("No API key is required for this deterministic agentic MVP.")

if uploaded is None:
    st.info("Upload a file to start the analysis workflow.")
    st.stop()

try:
    df = pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded)
except Exception as exc:
    st.error(f"Could not read this file: {exc}")
    st.stop()

with st.spinner("Running the agentic analysis workflow..."):
    result = run_agentic_analysis(df)

schema = result["schema"]
analysis = result["analysis"]

metrics = st.columns(4)
metrics[0].metric("Rows", f"{len(df):,}")
metrics[1].metric("Columns", f"{len(df.columns):,}")
metrics[2].metric("Reports selected", len(result["report_plan"]))
metrics[3].metric("Missing cells", f"{int(df.isna().sum().sum()):,}")

st.subheader("Agent-selected reports")
st.write(" · ".join(report.replace("_", " ").title() for report in result["report_plan"]))

for insight in result["insights"]:
    st.markdown(f"- {insight}")

if result.get("warnings"):
    for warning in result["warnings"]:
        st.warning(warning)

tabs = st.tabs(["Schema", "Distributions", "Relationships", "Preview"])

with tabs[0]:
    st.dataframe(pd.DataFrame(schema), use_container_width=True, hide_index=True)

with tabs[1]:
    numeric = [item["column"] for item in schema if item["logical_type"] == "numeric"]
    if numeric:
        selected = st.selectbox("Numeric field", numeric)
        st.plotly_chart(px.histogram(df, x=selected, template="plotly_white", title=f"Distribution of {selected}"), use_container_width=True)
    else:
        st.info("No numeric fields were detected.")

with tabs[2]:
    numeric = [item["column"] for item in schema if item["logical_type"] == "numeric"]
    if len(numeric) >= 2:
        x, y = st.columns(2)
        x_col = x.selectbox("X field", numeric)
        y_col = y.selectbox("Y field", numeric, index=1)
        st.plotly_chart(px.scatter(df, x=x_col, y=y_col, template="plotly_white", title=f"{y_col} vs {x_col}"), use_container_width=True)
    else:
        st.info("At least two numeric fields are needed for a relationship chart.")

with tabs[3]:
    st.dataframe(df.head(100), use_container_width=True, hide_index=True)

st.divider()
st.caption("LangGraph orchestration · deterministic evidence layer · Streamlit portal")
