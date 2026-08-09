from __future__ import annotations

from io import BytesIO

import pandas as pd
import streamlit as st
import streamlit_highcharts as hct

from agent_graph import run_agentic_analysis
from chart_builder import build_dynamic_charts
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
chart_groups = build_dynamic_charts(df, schema)
chart_count = sum(len(charts) for charts in chart_groups.values())

metrics = st.columns(4)
metrics[0].metric("Rows", f"{len(df):,}")
metrics[1].metric("Columns", f"{len(df.columns):,}")
metrics[2].metric("Charts generated", chart_count)
metrics[3].metric("Missing cells", f"{int(df.isna().sum().sum()):,}")
st.caption(f"Source: {source_label}")

st.subheader("Explore the data")
tab_schema, tab_distributions, tab_segments, tab_trends, tab_relationships, tab_preview = st.tabs(
    ["Schema", "Distributions", "Segments", "Trends", "Relationships", "Preview"]
)

with tab_schema:
    st.dataframe(pd.DataFrame(schema), use_container_width=True, hide_index=True)

for tab, group_name in ((tab_distributions, "Distributions"), (tab_segments, "Segments"), (tab_trends, "Trends"), (tab_relationships, "Relationships")):
    with tab:
        charts = chart_groups[group_name]
        if not charts:
            st.info(f"No applicable {group_name.lower()} charts were detected for this dataset.")
        else:
            for chart in charts:
                hct.streamlit_highcharts(chart, 520)

with tab_preview:
    st.dataframe(df.head(100), use_container_width=True, hide_index=True)

st.subheader("Recommended analysis")
st.caption("Based on the detected fields, data quality, and relationships.")
recommendation_labels = ["Overview", "Data quality", "Distributions", "Segment comparison", "Time trends", "Relationships"]
st.write(" · ".join(recommendation_labels))

with st.expander("Why these analyses were selected"):
    st.markdown("""
    - **Overview:** establishes dataset size and structure.
    - **Data quality:** checks missing values and structural issues.
    - **Distributions:** reviews numeric-field patterns.
    - **Segment comparison:** compares measures across categories.
    - **Time trends:** compares measures over time.
    - **Relationships:** explores correlations between numeric fields.
    """)

with st.expander("Technical details"):
    st.caption(f"{len(selected_reports)} analysis modules selected · {len(df):,} rows · {len(df.columns)} columns")
    st.caption(f"{chart_count} dynamic Highcharts visualizations generated.")
    for insight in result["insights"]:
        st.markdown(f"- {insight}")
    for warning in result.get("warnings", []):
        st.warning(warning)
    if text_preview:
        st.write(text_preview)

st.divider()
st.caption("LangGraph orchestration · secure input checks · dynamic Highcharts visualizations · Streamlit portal")
