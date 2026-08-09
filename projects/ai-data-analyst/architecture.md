# Agentic Architecture

```text
Streamlit Portal
      |
      +--> File input: CSV / Excel
      |
      +--> URL input: CSV / Excel / JSON / HTML / text
                    |
                    v
          Source validation and extraction
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
            Charts and briefing
```

## URL branch

The URL extractor first checks for direct tabular formats, then HTML tables, and finally falls back to page-level text metadata. The output is normalized into a DataFrame so the same downstream analytics workflow can be reused.

## Safety boundaries

- HTTP(S) only.
- No localhost or private-network targets.
- Request timeout and maximum response size.
- No login, paywall, CAPTCHA, or anti-bot bypass.
- Clear source attribution and extraction warnings.
- No permanent storage of source content in the demo.

## Agentic principle

The graph separates decision-making from calculation. Agent nodes can choose which tools and reports to run, but pandas performs the calculations and Plotly renders the visualizations. An optional language model may improve planning and narrative generation, but it is not the numerical source of truth.
