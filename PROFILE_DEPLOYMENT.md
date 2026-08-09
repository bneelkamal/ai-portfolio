# Streamlit AI Portfolio Landing Page

## Entrypoint

Deploy only the root portfolio application through Streamlit Community Cloud:

```text
portfolio_app.py
```

The AI Data Analyst is an internal page of the same Streamlit application:

```text
pages/01_AI_Data_Analyst.py
```

## Deployment steps

1. Open Streamlit Community Cloud.
2. Connect the `bneelkamal/ai-portfolio` GitHub repository.
3. Select the `main` branch.
4. Set the main file path to `portfolio_app.py`.
5. Deploy the app.
6. Use the app navigation to open **Agentic AI Data Analyst**.

The result is one profile URL containing the portfolio home page and project pages. Do not deploy `projects/ai-data-analyst/app.py` as a second Streamlit application.

## Before publishing

Replace placeholder links in `portfolio_app.py`:

- LinkedIn URL.
- Contact email.
- Future external project links.

Do not add API keys or private research data to this public repository.
