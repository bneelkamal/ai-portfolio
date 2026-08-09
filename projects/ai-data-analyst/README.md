# Agentic AI Data Analyst

An upload-first Streamlit analytics portal that accepts CSV/XLSX files or public URLs, extracts usable data, uses a LangGraph workflow to select reports, and presents an executive-friendly briefing.

## Inputs

- CSV, XLSX, and XLS files.
- Direct public CSV, Excel, or JSON URLs.
- Public HTML pages containing tables.
- Text-only public pages, represented by page-level metadata when no table is available.

## Agent workflow

1. Source — accepts a file or extracted URL result.
2. Schema — infers logical types and data quality metadata.
3. Planner — selects reports based on detected data patterns.
4. Analysis — computes deterministic summaries and relationships.
5. Insight — produces evidence-grounded observations.
6. Review — checks that the workflow produced a valid result.

The current milestone does not require an LLM API. This makes the public demo reliable and keeps numerical analysis deterministic.

## Responsible URL access

The demo accepts public HTTP(S) URLs only. It uses request timeouts and response-size limits, rejects local/private-network destinations, and does not bypass authentication, paywalls, CAPTCHAs, or anti-bot controls. Users should respect website terms and robots guidance.

## Run locally

```bash
cd projects/ai-data-analyst
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## Links

- [Portfolio repository](https://github.com/bneelkamal/ai-portfolio)
- [Project source](https://github.com/bneelkamal/ai-portfolio/tree/main/projects/ai-data-analyst)
- [Architecture](./architecture.md)
- [Live Streamlit demo](#) — to be added after deployment.

## Next milestones

- Add report recommendation explanations.
- Add explicit visualization and reviewer agents.
- Add workbook sheet selection and multi-table comparison.
- Add optional grounded summarization through a free-tier model.
- Add downloadable HTML/PDF reports.
- Add a Kaggle validation notebook.
