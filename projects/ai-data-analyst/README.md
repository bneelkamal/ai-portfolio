# Agentic AI Data Analyst

An upload-first Streamlit analytics portal that accepts CSV/XLSX files or public URLs, validates the source, extracts usable data, autonomously recommends relevant reports, and presents an executive-friendly briefing.

## Current features

- CSV/XLSX upload with pre-parse security validation.
- SHA-256 integrity hash and visible validation status.
- XLSX container, macro, embedded-object, and external-link checks.
- Optional ClamAV scanning with strict deployment mode.
- Public URL ingestion for CSV, Excel, JSON, HTML tables, and text metadata.
- Built-in Sales, Customer Churn, and Fraud sample datasets.
- Visible report recommendations with explanations.
- LangGraph workflow for schema, planning, analysis, insight, and review.
- Deterministic calculations with no API-key requirement.

## Report recommendation examples

- Numeric fields → distributions and outlier review.
- Date plus numeric fields → time trends.
- Multiple numeric fields → relationships.
- Categorical fields → segment comparison.
- Missing values → data-quality review.

The recommender is deterministic and explainable. An optional model can later refine report planning, but it must not replace the evidence layer.

## Security limitation

Structural checks are not a malware guarantee. Production deployments should run ClamAV or an approved isolated scanning service. Public demos should use synthetic or non-sensitive data.
