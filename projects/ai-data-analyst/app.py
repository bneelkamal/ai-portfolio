from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from agent_graph import run_agentic_analysis
from web_ingestion import extract_public_url

st.set_page_config(page_title="Agentic AI Data Analyst", page_icon="📊", layout="wide")
st.title("Agentic AI Data Analyst")
st.caption("Upload a file or paste a public URL. The agent graph selects useful reports and presents the evidence.")

with st.sidebar:
    st.header("Data source")
    source_type = st.radio("Choose input", ["Upload file", "Public URL"])
    df = None
    source_label = ""
    source_warning = None
    text_preview = None

    if source_type == "Upload file":
        uploaded = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"])
        if uploaded is not None:
            try:
                df = pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded)
                source_label = uploaded.name
            except Exception as exc:
                st.error(f"Could not read this file: {exc}")
    else:
        url = st.text_input("Public URL", placeholder="https://example.com/data.csv")
        if st.button("Fetch and analyze URL", type="primary") and url.strip():
            try:
                st.session_state["url_result"] = extract_public_url(url)
            except Exception as exc:
                st.session_state["url_error"] = str(exc)
        result = st.session_state.get("url_result")
        if result:
            df = result["dataframe"]
            source_label = result["title"]
            source_warning = result.get("warning")
            text_preview = result.get("text_preview")
        if st.session_state.get("url_error"):
            st.error(st.session_state.pop("url_error"))

    st.caption("Public URL mode does not bypass logins, paywalls, CAPTCHAs, or anti-bot controls.")

if df is None:
    st.info("Upload a CSV/XLSX file or enter a public URL to begin.")
    st.stop()

if source_warning:
    st.warning(source_warning)
if text_preview:
    with st.expander("Extracted page text preview"):
        st.write(text_preview)

with st.spinner("Running the agentic analysis workflow..."):
    result = run_agentic_analysis(df)

schema = result["schema"]
metrics = st.columns(4)
metrics[0].metric("Rows", f"{len(df):,}")
metrics[1].metric("Columns", f"{len(df.columns):,}")
metrics[2].metric("Reports selected", len(result["report_plan"]))
metrics[3].metric("Missing cells", f"{int(df.isna().sum().sum()):,}")
st.caption(f"Source: {source_label}")

st.subheader("Agent-selected reports")
st.write(" · ".join(report.replace("_", " ").title() for report in result["report_plan"]))
for insight in result["insights"]:
    st.markdown(f"- {insight}")

for warning in result.get("warnings", []):
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
st.caption("LangGraph orchestration · file and public URL ingestion · deterministic evidence layer")
