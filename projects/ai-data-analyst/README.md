# Agentic AI Data Analyst

An upload-first Streamlit portal that uses a LangGraph workflow to understand a CSV/XLSX dataset, select useful report modules, calculate evidence, and present an initial executive-friendly briefing.

## Why this is agentic

The workflow is decomposed into stateful nodes:

1. Source — accepts the uploaded dataset.
2. Schema — infers logical types and data quality metadata.
3. Planner — selects reports based on detected data patterns.
4. Analysis — computes deterministic summaries and relationships.
5. Insight — produces evidence-grounded observations.
6. Review — checks that the workflow produced a valid result.

The current milestone does not require an LLM API. This makes the public demo reliable and keeps the numerical analysis deterministic. An optional model can later improve planning and narrative generation without replacing the calculation layer.

## Run locally

```bash
cd projects/ai-data-analyst
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## Free and deployment modes

- **No API mode:** LangGraph plus deterministic Python tools. Works locally and on Streamlit hosting without an LLM key.
- **Local model mode:** Connect an Ollama model during local development. The model stays on the developer machine.
- **Free hosted model mode:** Optionally connect a provider free tier through Streamlit Secrets. The application must retain the deterministic fallback.

Never commit API keys to GitHub. Public demos should use synthetic or non-sensitive datasets when external model calls are enabled.

## Links

- [Portfolio repository](https://github.com/bneelkamal/ai-portfolio)
- [Project source](https://github.com/bneelkamal/ai-portfolio/tree/main/projects/ai-data-analyst)
- [Architecture](./architecture.md)
- [Live Streamlit demo](#) — to be added after deployment.

## Next milestones

- Add public URL ingestion for HTML tables, CSV/XLSX links, JSON, and text pages.
- Add a report recommender with explanations for every selected report.
- Add visualization and reviewer agents as explicit graph nodes.
- Add optional grounded summarization through a free-tier model.
- Add report downloads and evaluation datasets.
