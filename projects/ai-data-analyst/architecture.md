# Agentic Architecture

```text
Streamlit Portal
      |
      v
Source Node
      |
      v
Schema Node
      |
      v
Planner Node
      |
      v
Analysis Node
      |
      v
Insight Node
      |
      v
Review Node
      |
      v
Charts, reports, warnings, and executive briefing
```

## State

LangGraph carries a shared state object containing:

- Input DataFrame.
- Schema metadata.
- Selected report plan.
- Computed analysis results.
- Insights.
- Validation warnings.

## Design principle

The system separates **decision-making** from **calculation**. Agent nodes can choose which tools to run, but pandas performs the calculations and Plotly renders the visualizations. This reduces hallucination risk and makes the result reproducible.

## Model strategy

The graph works without a model. A future model adapter can be added only for:

- Natural-language report planning.
- Executive-language rewriting.
- Follow-up question interpretation.

The adapter must receive compact, derived statistics rather than unrestricted raw files. It must also have a deterministic fallback when the key is unavailable or the quota is exhausted.

## Future URL branch

```text
Source Node
   |
   +--> File loader
   |
   +--> Public URL loader
           +--> CSV/XLSX/JSON
           +--> HTML tables
           +--> JSON-LD
           +--> Text-only page
```

The URL loader will enforce HTTP(S)-only access, timeouts, response-size limits, public-source restrictions, and clear extraction warnings. Login-protected, paywalled, CAPTCHA-protected, or inaccessible pages will not be bypassed.
