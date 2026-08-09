from __future__ import annotations

from io import BytesIO

import pandas as pd
import plotly.express as px
import streamlit as st

from agent_graph import run_agentic_analysis
from report_recommender import recommend_reports
from sample_data import get_sample_datasets
from security import validate_upload
from web_ingestion import extract_public_url

st.set_page_config(page_title="Agentic AI Data Analyst", page_icon="📊", layout="wide")
st.title("Agentic AI Data Analyst")
st.caption("Drop a file, paste a public URL, or try a sample dataset. The portal selects useful reports automatically.")


def show_security(report: dict) -> None:
    st.subheader("Security and integrity")
    left, right = st.columns([1, 2])
    left.metric("Status", "Accepted" if report["accepted"] else "Rejected")
    left.caption(f"SHA-256: {report['sha256'][:16]}…")
    with right:
        for check in report["checks"]:
            status = check.get("status", "unknown").upper()
            detail = check.get("detail", "")
            st.write(f"**{check['name']}**: {status} {detail}")
        for warning in report["warnings"]:
            st.warning(warning)


with st.sidebar:
    st.header("Data source")
    source_type = st.radio("Choose input", ["Upload file", "Public URL", "Sample dataset"])
    df = None
    source_label = ""
    source_warning = None
    text_preview = None

    if source_type == "Upload file":
        uploaded = st.file_uploader("Upload CSV or XLSX", type=["csv", "xlsx"])
        if uploaded is not None:
            raw = uploaded.getvalue()
            security_report = validate_upload(uploaded.name, raw)
            show_security(security_report)
            if security_report["accepted"]:
                try:
                    df = pd.read_csv(BytesIO(raw)) if uploaded.name.lower().endswith(".csv") else pd.read_excel(BytesIO(raw))
                    source_label = uploaded.name
                except Exception as exc:
                    st.error(f"Could not parse this file: {exc}")
            else:
                st.error("The file was rejected before analysis.")

    elif source_type == "Public URL":
        url = st.text_input("Public URL", placeholder="https://example.com/data.csv")
        if st.button("Fetch and analyze URL", type="primary") and url.strip():
            try:
                st.session_state["url_result"] = extract_public_url(url)
                st.session_state.pop("url_error", None)
            except Exception as exc:
                st.session_state["url_error"] = str(exc)
        if st.session_state.get("url_error"):
            st.error(st.session_state["url_error"])
        url_result = st.session_state.get("url_result")
        if url_result:
            df = url_result["dataframe"]
            source_label = url_result["title"]
            source_warning = url_result.get("warning")
            text_preview = url_result.get("text_preview")

    else:
        samples = get_sample_datasets()
        selected_sample = st.selectbox("Choose a sample", list(samples))
        df = samples[selected_sample]
        source_label = f"Sample: {selected_sample}"
        st.success("Trusted synthetic sample selected.")

    st.caption("Public URL mode does not bypass logins, paywalls, CAPTCHAs, or anti-bot controls.")

if df is None:
    st.info("Choose a source to begin.")
    st.stop()

if source_warning:
    st.warning(source_warning)

with st.spinner("Running the agentic analysis workflow..."):
    result = run_agentic_analysis(df)

schema = result["schema"]
recommendations = recommend_reports(schema)
selected_reports = result["report_plan"]

metrics = st.columns(4)
metrics[0].metric("Rows", f"{len(df):,}")
metrics[1].metric("Columns", f"{len(df.columns):,}")
metrics[2].metric("Reports recommended", len(recommendations))
metrics[3].metric("Missing cells", f"{int(df.isna().sum().sum()):,}")
st.caption(f"Source: {source_label}")

st.subheader("Explore the data")
tab_schema, tab_distributions, tab_relationships, tab_preview = st.tabs(
    ["Schema", "Distributions", "Relationships", "Preview"]
)

with tab_schema:
    st.dataframe(pd.DataFrame(schema), use_container_width=True, hide_index=True)

with tab_distributions:
    numeric = [item["column"] for item in schema if item["logical_type"] == "numeric"]
    if numeric:
        selected = st.selectbox("Numeric field", numeric)
        st.plotly_chart(
            px.histogram(df, x=selected, template="plotly_white", title=f"Distribution of {selected}"),
            use_container_width=True,
        )
    else:
        st.info("No numeric fields were detected.")

with tab_relationships:
    numeric = [item["column"] for item in schema if item["logical_type"] == "numeric"]
    if len(numeric) >= 2:
        x, y = st.columns(2)
        x_col = x.selectbox("X field", numeric)
        y_col = y.selectbox("Y field", numeric, index=1)
        st.plotly_chart(
            px.scatter(df, x=x_col, y=y_col, template="plotly_white", title=f"{y_col} vs {x_col}"),
            use_container_width=True,
        )
    else:
        st.info("At least two numeric fields are needed for a relationship chart.")

with tab_preview:
    st.dataframe(df.head(100), use_container_width=True, hide_index=True)

st.subheader("Recommended analysis")
st.caption("Based on the detected fields, data quality, and relationships.")
recommendation_labels = [
    "Overview",
    "Data quality",
    "Distributions",
    "Segment comparison",
    "Time trends",
    "Relationships",
]
st.write(" · ".join(recommendation_labels))

with st.expander("Why these analyses were selected"):
    st.markdown(
        """
        - **Overview:** establishes dataset size and structure.
        - **Data quality:** checks missing values and structural issues.
        - **Distributions:** reviews numeric-field patterns.
        - **Segment comparison:** compares measures across categories.
        - **Time trends:** compares measures over time.
        - **Relationships:** explores correlations between numeric fields.
        """
    )

with st.expander("Technical details"):
    st.caption(
        f"{len(selected_reports)} analysis modules selected · "
        f"{len(df):,} rows · {len(df.columns)} columns"
    )
    for insight in result["insights"]:
        st.markdown(f"- {insight}")
    for warning in result.get("warnings", []):
        st.warning(warning)
    if text_preview:
        st.write(text_preview)

st.divider()
st.caption("LangGraph orchestration · secure input checks · automatic report recommendations · Streamlit portal")